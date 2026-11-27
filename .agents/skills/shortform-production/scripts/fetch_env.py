#!/usr/bin/env python3
"""Fetch project .env secrets from Doppler into the repository root.

Uses only the Python standard library, writes .env atomically with 0600 permissions,
and never prints secret values or tokens.
"""
from __future__ import annotations

import argparse
import base64
import getpass
import json
import os
from pathlib import Path
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
OPTIONAL_GDRIVE_KEYS = (
    'GOOGLE_CLIENT_ID',
    'GOOGLE_CLIENT_SECRET',
    'GOOGLE_REFRESH_TOKEN',
    'GOOGLE_DRIVE_ROOT_FOLDER_ID',
)


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / 'TRACKER.json').exists() or (candidate / '.env.example').exists():
            return candidate
    return current


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


def parse_env_keys(content: str) -> list[str]:
    keys: list[str] = []
    seen: set[str] = set()
    for raw in content.splitlines():
        line = raw.strip().removeprefix('export ')
        if not line or line.startswith('#') or '=' not in line:
            continue
        key = line.split('=', 1)[0].strip()
        if key and key not in seen:
            keys.append(key)
            seen.add(key)
    return keys


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


def run_checks(root: Path, keys: set[str]) -> dict[str, str]:
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

    if all(k in keys for k in OPTIONAL_GDRIVE_KEYS):
        proc = subprocess.run(
            [sys.executable, str(scripts_dir / 'gdrive.py'), '--root', str(root), 'check'],
            capture_output=True,
            text=True,
            check=False,
        )
        results['gdrive'] = 'ok' if proc.returncode == 0 else f'failed: {(proc.stderr or proc.stdout).strip()}'
    else:
        results['gdrive'] = 'skipped (Google Drive keys not all configured)'

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
    parser.add_argument('--check', action='store_true', help='Run ElevenLabs and Trypost connectivity checks after writing .env')
    parser.add_argument('--json', action='store_true', dest='as_json', help='Print machine-readable summary without secret values')
    args = parser.parse_args(argv)

    try:
        root = args.root.resolve() if args.root else find_project_root()
        token = resolve_token(token_stdin=args.token_stdin)
        content = fetch_doppler_env(token, project=args.project, config=args.config)
        keys = parse_env_keys(content)
        target = write_env_atomic(root, content)
        present_expected = [k for k in EXPECTED_KEYS if k in keys]
        missing_expected = [k for k in EXPECTED_KEYS if k not in keys]
        present_gdrive = [k for k in OPTIONAL_GDRIVE_KEYS if k in keys]
        missing_gdrive = [k for k in OPTIONAL_GDRIVE_KEYS if k not in keys]
        checks = run_checks(root, set(keys)) if args.check else None
    except (ValueError, RuntimeError, OSError) as exc:
        print(f'fetch_env: {exc}', file=sys.stderr)
        return 1

    summary = {
        'ok': True,
        'path': str(target),
        'key_count': len(keys),
        'keys': keys,
        'expected_present': present_expected,
        'expected_missing': missing_expected,
        'optional_gdrive_present': present_gdrive,
        'optional_gdrive_missing': missing_gdrive,
    }
    if checks is not None:
        summary['checks'] = checks
        if any(status.startswith('failed:') for status in checks.values()):
            summary['ok'] = False

    if args.as_json:
        print(json.dumps(summary, indent=2))
    else:
        print(f'Wrote {target} ({len(keys)} keys, mode 0600)')
        print(f'Expected keys present: {", ".join(present_expected) or "(none)"}')
        if missing_expected:
            print(f'Expected keys missing: {", ".join(missing_expected)}')
        if checks is not None:
            for name, status in checks.items():
                print(f'Check {name}: {status}')

    return 0 if summary['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
