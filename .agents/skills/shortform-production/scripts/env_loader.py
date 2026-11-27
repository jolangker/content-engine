"""Shared environment loader: Doppler REST API first, with per-key fallback to root .env.

Uses only the Python standard library, keeps fetched Doppler secrets in memory for the
duration of the process, ignores ordinary non-Doppler shell environment variables, and
never prints secret values or tokens.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request


DOPPLER_DOWNLOAD_URL = 'https://api.doppler.com/v3/configs/config/secrets/download'
USER_AGENT = 'content-engine/1.0'
DEFAULT_DOPPLER_TIMEOUT = 15
DOPPLER_TOKEN_PLACEHOLDERS = {'', 'your-doppler-token'}

# Cache Doppler fetch results per process: key -> (secrets_dict_or_None, error_str_or_None)
_DOPPLER_CACHE: dict[tuple[str, str, str], tuple[dict[str, str] | None, str | None]] = {}


def clear_cache() -> None:
    """Clear the in-memory Doppler fetch cache (primarily for tests)."""
    _DOPPLER_CACHE.clear()


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (
            (candidate / 'TRACKER.json').exists()
            or (candidate / '.env').exists()
            or (candidate / '.env.example').exists()
        ):
            return candidate
    return current


def parse_dotenv(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip().removeprefix('export ')
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        if value[:1] in ('"', "'"):
            quote = value[0]
            end = value.find(quote, 1)
            if end < 0:
                raise ValueError(f'Unclosed quoted value for {key} in .env')
            value = value[1:end]
        else:
            value = re.split(r'\s+#', value, maxsplit=1)[0].strip()
        if key:
            values[key] = value
    return values


def read_dotenv(root: Path) -> dict[str, str]:
    path = root / '.env'
    if not path.exists():
        return {}
    return parse_dotenv(path.read_text(encoding='utf-8-sig'))


def fetch_doppler_secrets(
    token: str,
    *,
    project: str | None = None,
    config: str | None = None,
    timeout: int = DEFAULT_DOPPLER_TIMEOUT,
    opener=None,
) -> dict[str, str]:
    clean_token = token.strip()
    if not clean_token:
        raise ValueError('Doppler token is empty')
    if bool(project) != bool(config):
        raise ValueError('DOPPLER_PROJECT and DOPPLER_CONFIG must be provided together')

    params: dict[str, str] = {'format': 'json'}
    if project and config:
        params['project'] = project.strip()
        params['config'] = config.strip()

    url = f'{DOPPLER_DOWNLOAD_URL}?{urllib.parse.urlencode(params)}'
    auth = base64.b64encode(f'{clean_token}:'.encode('utf-8')).decode('ascii')
    request = urllib.request.Request(
        url,
        method='GET',
        headers={
            'Authorization': f'Basic {auth}',
            'Accept': 'application/json',
            'User-Agent': USER_AGENT,
        },
    )
    open_fn = opener or urllib.request.urlopen
    try:
        with open_fn(request, timeout=timeout) as response:
            raw = response.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as exc:
        detail = ''
        try:
            payload = json.loads(exc.read().decode('utf-8', errors='replace'))
            messages = payload.get('messages')
            if isinstance(messages, list) and messages:
                detail = f': {"; ".join(str(m) for m in messages)}'
        except Exception:
            pass
        raise RuntimeError(f'Doppler API request failed (HTTP {exc.code}){detail}') from None
    except urllib.error.URLError as exc:
        raise RuntimeError(f'Doppler API unreachable: {exc.reason}') from None

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        raise RuntimeError('Doppler API returned invalid JSON') from None

    if not isinstance(parsed, dict):
        raise RuntimeError('Doppler API returned unexpected payload type')

    secrets: dict[str, str] = {}
    for key, value in parsed.items():
        if isinstance(key, str) and isinstance(value, str):
            secrets[key] = value
    return secrets


def _resolve_doppler_auth(local_env: dict[str, str]) -> tuple[str | None, str | None, str | None]:
    token = os.environ.get('DOPPLER_TOKEN', '').strip()
    if not token:
        token = local_env.get('DOPPLER_TOKEN', '').strip()
    if token.lower() in DOPPLER_TOKEN_PLACEHOLDERS:
        return None, None, None

    project = (os.environ.get('DOPPLER_PROJECT', '').strip() or local_env.get('DOPPLER_PROJECT', '').strip()) or None
    config = (os.environ.get('DOPPLER_CONFIG', '').strip() or local_env.get('DOPPLER_CONFIG', '').strip()) or None
    # Only forward project/config when both are supplied; scoped Service Tokens omit both.
    if not (project and config):
        project, config = None, None
    return token, project, config


def load_env(
    root: Path,
    *,
    use_cache: bool = True,
    timeout: int = DEFAULT_DOPPLER_TIMEOUT,
    opener=None,
) -> tuple[dict[str, str], dict[str, object]]:
    """Load secrets with Doppler REST API as primary source and per-key fallback to root .env.

    Ordinary non-Doppler shell environment variables are ignored so project configuration
    remains isolated to Doppler and the workspace .env file.
    """
    local_env = read_dotenv(root)
    token, project, config = _resolve_doppler_auth(local_env)
    if not token:
        return dict(local_env), {
            'source': 'dotenv' if local_env else 'none',
            'doppler_ok': False,
            'dotenv_loaded': bool(local_env),
            'doppler_error': None,
        }

    cache_key = (
        hashlib.sha256(token.encode('utf-8')).hexdigest(),
        project or '',
        config or '',
    )

    doppler_secrets: dict[str, str] | None = None
    doppler_error: str | None = None

    if use_cache and opener is None and cache_key in _DOPPLER_CACHE:
        doppler_secrets, doppler_error = _DOPPLER_CACHE[cache_key]
    else:
        try:
            doppler_secrets = fetch_doppler_secrets(
                token,
                project=project,
                config=config,
                timeout=timeout,
                opener=opener,
            )
        except (ValueError, RuntimeError) as exc:
            doppler_secrets = None
            doppler_error = str(exc)
        if use_cache and opener is None:
            _DOPPLER_CACHE[cache_key] = (doppler_secrets, doppler_error)

    if doppler_secrets is not None:
        merged = dict(local_env)
        merged.update(doppler_secrets)
        source = 'doppler+dotenv' if local_env else 'doppler'
        return merged, {
            'source': source,
            'doppler_ok': True,
            'dotenv_loaded': bool(local_env),
            'doppler_error': None,
        }

    return dict(local_env), {
        'source': 'dotenv' if local_env else 'none',
        'doppler_ok': False,
        'dotenv_loaded': bool(local_env),
        'doppler_error': doppler_error,
    }


def read_env(
    root: Path,
    *,
    use_cache: bool = True,
    timeout: int = DEFAULT_DOPPLER_TIMEOUT,
    opener=None,
) -> dict[str, str]:
    values, _ = load_env(root, use_cache=use_cache, timeout=timeout, opener=opener)
    return values
