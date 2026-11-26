#!/usr/bin/env python3
"""Fetch project .env secrets from Doppler into the repository root.

Uses only the Python standard library, writes .env atomically with 0600 permissions,
and never prints secret values or tokens.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import getpass
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

DOPPLER_DOWNLOAD_URL = 'https://api.doppler.com/v3/configs/config/secrets/download'
USER_AGENT = 'content-engine/1.0'
DEFAULT_TIMEOUT = 30
EXPECTED_KEYS = (
    'TRYPOST_BASE_URL',
    'TRYPOST_API_KEY',
    'ELEVENLABS_API_KEY',
    'ELEVENLABS_VOICE_ID',
)
ADC_B64_KEY = 'GOOGLE_COLAB_ADC_JSON_B64'
ADC_RAW_KEY = 'GOOGLE_COLAB_ADC_JSON'
ADC_REQUIRED_SCOPE = 'https://www.googleapis.com/auth/colaboratory'


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / 'TRACKER.json').exists() or (candidate / '.env.example').exists():
            return candidate
    return current


def default_adc_path() -> Path:
    configured = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '').strip()
    if configured:
        return Path(configured).expanduser()
    return Path.home() / '.config' / 'gcloud' / 'application_default_credentials.json'


def find_colab_binary() -> str | None:
    found = shutil.which('colab')
    if found:
        return found
    candidate = Path.home() / '.local' / 'bin' / 'colab'
    if candidate.is_file() and os.access(candidate, os.X_OK):
        return str(candidate)
    return None


def fetch_doppler_env(
    token: str,
    *,
    project: str | None = None,
    config: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> str:
    clean_token = token.strip()
    if not clean_token:
        raise ValueError('Doppler token is empty. Set DOPPLER_TOKEN or pass --token-stdin.')
    if bool(project) != bool(config):
        raise ValueError('Pass both --project and --config together, or omit both when using a scoped Service Token.')

    params: dict[str, str] = {'format': 'env'}
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
            'Accept': 'text/plain',
            'User-Agent': USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode('utf-8')
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

    if not body.strip():
        raise RuntimeError('Doppler returned an empty .env payload.')
    return body if body.endswith('\n') else f'{body}\n'


def _unquote_env_value(raw_value: str) -> str:
    value = raw_value.strip()
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        inner = value[1:-1]
        return (
            inner.replace('\\n', '\n')
            .replace('\\r', '\r')
            .replace('\\t', '\t')
            .replace('\\"', '"')
            .replace('\\\\', '\\')
        )
    if len(value) >= 2 and value[0] == "'" and value[-1] == "'":
        return value[1:-1]
    return value


def parse_env_items(content: str) -> dict[str, str]:
    items: dict[str, str] = {}
    for raw in content.splitlines():
        line = raw.strip().removeprefix('export ')
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, raw_value = line.split('=', 1)
        clean_key = key.strip()
        if clean_key:
            items[clean_key] = _unquote_env_value(raw_value)
    return items


def parse_env_keys(content: str) -> list[str]:
    return list(parse_env_items(content).keys())


def decode_adc_payload(items: dict[str, str]) -> str | None:
    b64_value = items.get(ADC_B64_KEY, '').strip()
    raw_value = items.get(ADC_RAW_KEY, '').strip()
    if b64_value:
        source_key = ADC_B64_KEY
        try:
            decoded_bytes = base64.b64decode(b64_value, validate=True)
            json_text = decoded_bytes.decode('utf-8').strip()
        except (binascii.Error, ValueError, UnicodeDecodeError):
            raise ValueError(f'{ADC_B64_KEY} is not valid base64-encoded UTF-8 JSON.') from None
    elif raw_value:
        source_key = ADC_RAW_KEY
        json_text = raw_value
    else:
        return None

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError:
        raise ValueError(f'{source_key} does not contain valid JSON.') from None

    if not isinstance(parsed, dict) or not parsed.get('type'):
        raise ValueError(f'{source_key} must decode to an ADC JSON object containing a "type" field.')
    return json.dumps(parsed, indent=2) + '\n'


def write_env_atomic(root: Path, content: str) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    target = root / '.env'
    fd, tmp_name = tempfile.mkstemp(prefix='.env.tmp.', dir=str(root))
    tmp_path = Path(tmp_name)
    try:
        os.chmod(tmp_path, 0o600)
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            handle.write(content)
        os.replace(tmp_path, target)
        os.chmod(target, 0o600)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise
    return target


def write_adc_atomic(adc_path: Path, payload: str) -> Path:
    adc_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix='.adc.tmp.', dir=str(adc_path.parent))
    tmp_path = Path(tmp_name)
    try:
        os.chmod(tmp_path, 0o600)
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            handle.write(payload)
        os.replace(tmp_path, adc_path)
        os.chmod(adc_path, 0o600)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise
    return adc_path


def run_checks(root: Path, keys: set[str], *, adc_path: Path | None = None) -> dict[str, str]:
    scripts_dir = Path(__file__).resolve().parent
    results: dict[str, str] = {}

    if 'ELEVENLABS_API_KEY' in keys:
        proc = subprocess.run(
            [sys.executable, str(scripts_dir / 'narration.py'), '--project-root', str(root), '--check-api'],
            capture_output=True,
            text=True,
            check=False,
        )
        results['elevenlabs'] = 'ok' if proc.returncode == 0 else f'failed: {(proc.stderr or proc.stdout).strip()}'
    else:
        results['elevenlabs'] = 'skipped (ELEVENLABS_API_KEY not in .env)'

    if 'TRYPOST_BASE_URL' in keys and 'TRYPOST_API_KEY' in keys:
        proc = subprocess.run(
            [sys.executable, str(scripts_dir / 'trypost.py'), '--root', str(root), 'check'],
            capture_output=True,
            text=True,
            check=False,
        )
        results['trypost'] = 'ok' if proc.returncode == 0 else f'failed: {(proc.stderr or proc.stdout).strip()}'
    else:
        results['trypost'] = 'skipped (TRYPOST_BASE_URL/TRYPOST_API_KEY not in .env)'

    if ADC_B64_KEY in keys or ADC_RAW_KEY in keys:
        colab_bin = find_colab_binary()
        if not colab_bin:
            results['colab_adc'] = 'failed: colab CLI not installed (run uv tool install google-colab-cli)'
        else:
            env = os.environ.copy()
            if adc_path is not None:
                env['GOOGLE_APPLICATION_CREDENTIALS'] = str(adc_path)
            proc = subprocess.run(
                [colab_bin, '--auth=adc', 'whoami'],
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )
            if proc.returncode != 0:
                results['colab_adc'] = f'failed: {(proc.stderr or proc.stdout).strip()}'
            elif ADC_REQUIRED_SCOPE not in (proc.stdout or ''):
                results['colab_adc'] = f'failed: ADC credentials missing required scope {ADC_REQUIRED_SCOPE}'
            else:
                results['colab_adc'] = 'ok'

    return results


def resolve_token(*, token_stdin: bool) -> str:
    if token_stdin:
        return sys.stdin.read().strip()
    env_token = os.environ.get('DOPPLER_TOKEN', '').strip()
    if env_token:
        return env_token
    if sys.stdin.isatty():
        return getpass.getpass('Doppler token: ').strip()
    raise ValueError('No Doppler token provided. Set DOPPLER_TOKEN or pass --token-stdin.')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Fetch .env from Doppler into the project root.')
    parser.add_argument('--root', type=Path, default=None, help='Project root directory (defaults to repo root)')
    parser.add_argument('--project', default=None, help='Doppler project (only needed for personal/service-account tokens)')
    parser.add_argument('--config', default=None, help='Doppler config (only needed for personal/service-account tokens)')
    parser.add_argument('--token-stdin', action='store_true', help='Read Doppler token from stdin')
    parser.add_argument('--adc-path', type=Path, default=None, help='Destination path for restored Google Colab ADC JSON')
    parser.add_argument('--no-adc', action='store_true', help='Skip restoring GOOGLE_COLAB_ADC_JSON(_B64) to disk')
    parser.add_argument('--check', action='store_true', help='Run ElevenLabs, Trypost, and Colab ADC checks after writing .env')
    parser.add_argument('--json', action='store_true', dest='as_json', help='Print machine-readable summary without secret values')
    args = parser.parse_args(argv)

    try:
        root = args.root.resolve() if args.root else find_project_root()
        token = resolve_token(token_stdin=args.token_stdin)
        content = fetch_doppler_env(token, project=args.project, config=args.config)
        items = parse_env_items(content)
        keys = list(items.keys())
        target = write_env_atomic(root, content)
        adc_target: Path | None = None
        if not args.no_adc:
            adc_payload = decode_adc_payload(items)
            if adc_payload is not None:
                dest = args.adc_path.expanduser().resolve() if args.adc_path else default_adc_path()
                adc_target = write_adc_atomic(dest, adc_payload)
        present_expected = [k for k in EXPECTED_KEYS if k in keys]
        missing_expected = [k for k in EXPECTED_KEYS if k not in keys]
        checks = run_checks(root, set(keys), adc_path=adc_target) if args.check else None
    except (ValueError, RuntimeError, OSError) as exc:
        print(f'fetch_env: {exc}', file=sys.stderr)
        return 1

    summary: dict[str, object] = {
        'ok': True,
        'path': str(target),
        'key_count': len(keys),
        'keys': keys,
        'expected_present': present_expected,
        'expected_missing': missing_expected,
    }
    if adc_target is not None:
        summary['adc_restored'] = True
        summary['adc_path'] = str(adc_target)
    if checks is not None:
        summary['checks'] = checks
        if any(status.startswith('failed:') for status in checks.values()):
            summary['ok'] = False

    if args.as_json:
        print(json.dumps(summary, indent=2))
    else:
        print(f'Wrote {target} ({len(keys)} keys, mode 0600)')
        if adc_target is not None:
            print(f'Restored Colab ADC credentials to {adc_target} (mode 0600)')
        print(f'Expected keys present: {", ".join(present_expected) or "(none)"}')
        if missing_expected:
            print(f'Expected keys missing: {", ".join(missing_expected)}')
        if checks is not None:
            for name, status in checks.items():
                print(f'Check {name}: {status}')

    return 0 if summary['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
