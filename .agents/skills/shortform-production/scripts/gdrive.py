"""Google Drive deliverables archiver (OAuth 2.0 + Drive API v3 resumable uploads).

Archives verified production deliverables (exports/* + CONTENT_PACKAGE.md) into
<Root>/<board-slug>/<production-slug>/ on My Drive using only the Python standard
library. Reads configuration from Doppler (primary) with per-key fallback to root .env,
and never prints OAuth client secrets or access tokens.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import mimetypes
from pathlib import Path
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
import env_loader


USER_AGENT = 'content-engine/1.0'
OAUTH_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
OAUTH_TOKEN_URL = 'https://oauth2.googleapis.com/token'
DRIVE_API_BASE = 'https://www.googleapis.com/drive/v3'
DRIVE_UPLOAD_BASE = 'https://www.googleapis.com/upload/drive/v3'
DRIVE_SCOPE = 'https://www.googleapis.com/auth/drive'
FOLDER_MIME = 'application/vnd.google-apps.folder'
STANDALONE_BOARD_DIR = '_standalone'

DEFAULT_TIMEOUT = 120
DEFAULT_CHUNK_SIZE = 8 * 1024 * 1024  # 8 MiB (must be a multiple of 256 KiB)
IGNORED_FILENAMES = {'.DS_Store', 'Thumbs.db', 'desktop.ini'}

CONFIG_KEYS = (
    'GOOGLE_CLIENT_ID',
    'GOOGLE_CLIENT_SECRET',
    'GOOGLE_REFRESH_TOKEN',
    'GOOGLE_DRIVE_ROOT_FOLDER_ID',
)
PLACEHOLDER_VALUES = {
    '',
    'your-google-client-id',
    'your-google-client-secret',
    'your-google-refresh-token',
    'your-google-drive-root-folder-id',
}


class GDriveError(RuntimeError):
    def __init__(self, message: str, *, status: int | None = None, body: object = None):
        super().__init__(message)
        self.status = status
        self.body = body


@dataclass(frozen=True)
class GDriveConfig:
    client_id: str
    client_secret: str
    refresh_token: str
    root_folder_id: str


def _clean_config_value(env: dict[str, str], key: str) -> str:
    value = env.get(key, '').strip()
    if value.lower() in PLACEHOLDER_VALUES:
        return ''
    return value


def resolve_config(root: Path, *, opener=None) -> tuple[GDriveConfig | None, dict[str, object]]:
    env, meta = env_loader.load_env(root, opener=opener)
    cleaned = {key: _clean_config_value(env, key) for key in CONFIG_KEYS}
    present = [k for k, v in cleaned.items() if v]
    if not present:
        return None, meta
    missing = [k for k, v in cleaned.items() if not v]
    if missing:
        raise ValueError(
            'Incomplete Google Drive configuration in Doppler/.env; missing: ' + ', '.join(missing)
        )
    return (
        GDriveConfig(
            client_id=cleaned['GOOGLE_CLIENT_ID'],
            client_secret=cleaned['GOOGLE_CLIENT_SECRET'],
            refresh_token=cleaned['GOOGLE_REFRESH_TOKEN'],
            root_folder_id=cleaned['GOOGLE_DRIVE_ROOT_FOLDER_ID'],
        ),
        meta,
    )


def _parse_body(raw: bytes) -> object:
    text = raw.decode('utf-8', errors='replace').strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _escape_drive_q(value: str) -> str:
    return value.replace('\\', '\\\\').replace("'", "\\'")


def file_md5(path: Path) -> str:
    digest = hashlib.md5()
    with path.open('rb') as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def exchange_oauth_token(
    form_fields: dict[str, str],
    *,
    timeout: int = DEFAULT_TIMEOUT,
    opener=None,
) -> dict:
    encoded = urllib.parse.urlencode(form_fields).encode('utf-8')
    req = urllib.request.Request(
        OAUTH_TOKEN_URL,
        data=encoded,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'User-Agent': USER_AGENT,
        },
        method='POST',
    )
    open_fn = opener or urllib.request.urlopen
    try:
        with open_fn(req, timeout=timeout) as resp:
            parsed = _parse_body(resp.read())
    except urllib.error.HTTPError as exc:
        parsed = _parse_body(exc.read())
        err_code = parsed.get('error') if isinstance(parsed, dict) else None
        err_desc = parsed.get('error_description') if isinstance(parsed, dict) else None
        detail = f' ({err_code}: {err_desc})' if err_code else ''
        raise GDriveError(f'Google OAuth token request failed (HTTP {exc.code}){detail}', status=exc.code, body=parsed) from None
    except urllib.error.URLError as exc:
        raise GDriveError(f'Google OAuth token endpoint unreachable: {exc.reason}') from None

    if not isinstance(parsed, dict) or not parsed.get('access_token'):
        raise GDriveError('Google OAuth token response did not include an access_token')
    return parsed


def build_auth_url(client_id: str, redirect_uri: str, state: str) -> str:
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': DRIVE_SCOPE,
        'access_type': 'offline',
        'prompt': 'consent',
        'state': state,
    }
    return f'{OAUTH_AUTH_URL}?{urllib.parse.urlencode(params)}'


class GDriveClient:
    def __init__(
        self,
        config: GDriveConfig,
        *,
        timeout: int = DEFAULT_TIMEOUT,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        opener=None,
    ):
        self.config = config
        self.timeout = timeout
        self.chunk_size = chunk_size
        self._opener = opener
        self._access_token: str | None = None

    def _open(self, req: urllib.request.Request):
        open_fn = self._opener or urllib.request.urlopen
        return open_fn(req, timeout=self.timeout)

    def get_access_token(self) -> str:
        if self._access_token:
            return self._access_token
        token_data = exchange_oauth_token(
            {
                'client_id': self.config.client_id,
                'client_secret': self.config.client_secret,
                'refresh_token': self.config.refresh_token,
                'grant_type': 'refresh_token',
            },
            timeout=self.timeout,
            opener=self._opener,
        )
        self._access_token = str(token_data['access_token'])
        return self._access_token

    def _auth_headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Accept': 'application/json',
            'User-Agent': USER_AGENT,
        }
        if extra:
            headers.update(extra)
        return headers

    def _request_json(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, str] | None = None,
        json_body: object = None,
    ) -> dict:
        full_url = f'{url}?{urllib.parse.urlencode(params)}' if params else url
        data: bytes | None = None
        extra: dict[str, str] = {}
        if json_body is not None:
            data = json.dumps(json_body, ensure_ascii=False).encode('utf-8')
            extra['Content-Type'] = 'application/json; charset=UTF-8'
        req = urllib.request.Request(full_url, data=data, headers=self._auth_headers(extra), method=method)
        try:
            with self._open(req) as resp:
                parsed = _parse_body(resp.read())
        except urllib.error.HTTPError as exc:
            parsed = _parse_body(exc.read())
            raise GDriveError(f'HTTP {exc.code} {method} {url}', status=exc.code, body=parsed) from None
        except urllib.error.URLError as exc:
            raise GDriveError(f'Network error on {method} {url}: {exc.reason}') from None
        if not isinstance(parsed, dict):
            raise GDriveError(f'Unexpected non-object response from {method} {url}')
        return parsed

    def check_root_folder(self) -> dict:
        folder_id = urllib.parse.quote(self.config.root_folder_id, safe='')
        meta = self._request_json(
            'GET',
            f'{DRIVE_API_BASE}/files/{folder_id}',
            params={'fields': 'id,name,mimeType,trashed,webViewLink'},
        )
        if meta.get('mimeType') != FOLDER_MIME:
            raise GDriveError(f'GOOGLE_DRIVE_ROOT_FOLDER_ID ({self.config.root_folder_id}) is not a Google Drive folder')
        if meta.get('trashed'):
            raise GDriveError(f'GOOGLE_DRIVE_ROOT_FOLDER_ID ({self.config.root_folder_id}) is in the trash')
        return {
            'id': meta['id'],
            'name': meta.get('name'),
            'web_view_link': meta.get('webViewLink') or f'https://drive.google.com/drive/folders/{meta["id"]}',
        }

    def find_folder(self, parent_id: str, name: str) -> dict | None:
        query = (
            f"name = '{_escape_drive_q(name)}' "
            f"and '{_escape_drive_q(parent_id)}' in parents "
            f"and mimeType = '{FOLDER_MIME}' "
            f"and trashed = false"
        )
        data = self._request_json(
            'GET',
            f'{DRIVE_API_BASE}/files',
            params={
                'q': query,
                'fields': 'files(id,name,webViewLink)',
                'pageSize': '10',
                'orderBy': 'createdTime asc',
            },
        )
        files = data.get('files', [])
        if not files:
            return None
        folder = files[0]
        return {
            'id': folder['id'],
            'name': folder['name'],
            'web_view_link': folder.get('webViewLink') or f'https://drive.google.com/drive/folders/{folder["id"]}',
        }

    def ensure_folder(self, parent_id: str, name: str) -> dict:
        existing = self.find_folder(parent_id, name)
        if existing:
            return existing
        created = self._request_json(
            'POST',
            f'{DRIVE_API_BASE}/files',
            params={'fields': 'id,name,webViewLink'},
            json_body={
                'name': name,
                'mimeType': FOLDER_MIME,
                'parents': [parent_id],
            },
        )
        return {
            'id': created['id'],
            'name': created['name'],
            'web_view_link': created.get('webViewLink') or f'https://drive.google.com/drive/folders/{created["id"]}',
        }

    def list_files(self, folder_id: str) -> list[dict]:
        query = (
            f"'{_escape_drive_q(folder_id)}' in parents "
            f"and trashed = false "
            f"and mimeType != '{FOLDER_MIME}'"
        )
        results: list[dict] = []
        page_token: str | None = None
        while True:
            params: dict[str, str] = {
                'q': query,
                'fields': 'nextPageToken,files(id,name,md5Checksum,size,modifiedTime,webViewLink)',
                'pageSize': '100',
            }
            if page_token:
                params['pageToken'] = page_token
            data = self._request_json('GET', f'{DRIVE_API_BASE}/files', params=params)
            results.extend(data.get('files', []))
            page_token = data.get('nextPageToken')
            if not page_token:
                break
        return results

    def upload_file(self, folder_id: str, local_path: Path, *, existing_file_id: str | None = None) -> dict:
        if not local_path.is_file():
            raise FileNotFoundError(f'Deliverable file not found: {local_path}')
        total_size = local_path.stat().st_size
        mime_type = mimetypes.guess_type(local_path.name)[0] or 'application/octet-stream'

        if existing_file_id:
            method = 'PATCH'
            init_url = (
                f'{DRIVE_UPLOAD_BASE}/files/{urllib.parse.quote(existing_file_id, safe="")}'
                f'?{urllib.parse.urlencode({"uploadType": "resumable", "fields": "id,name,md5Checksum,size,modifiedTime,webViewLink"})}'
            )
            metadata: dict[str, object] = {'name': local_path.name}
        else:
            method = 'POST'
            init_url = (
                f'{DRIVE_UPLOAD_BASE}/files'
                f'?{urllib.parse.urlencode({"uploadType": "resumable", "fields": "id,name,md5Checksum,size,modifiedTime,webViewLink"})}'
            )
            metadata = {'name': local_path.name, 'parents': [folder_id]}

        init_body = json.dumps(metadata, ensure_ascii=False).encode('utf-8')
        init_req = urllib.request.Request(
            init_url,
            data=init_body,
            headers=self._auth_headers({
                'Content-Type': 'application/json; charset=UTF-8',
                'X-Upload-Content-Type': mime_type,
                'X-Upload-Content-Length': str(total_size),
            }),
            method=method,
        )
        try:
            with self._open(init_req) as resp:
                session_uri = resp.headers.get('Location') or resp.headers.get('location')
        except urllib.error.HTTPError as exc:
            parsed = _parse_body(exc.read())
            raise GDriveError(f'Failed to start resumable upload for {local_path.name} (HTTP {exc.code})', status=exc.code, body=parsed) from None
        except urllib.error.URLError as exc:
            raise GDriveError(f'Network error starting upload for {local_path.name}: {exc.reason}') from None

        if not session_uri:
            raise GDriveError(f'Google Drive did not return a resumable upload Location header for {local_path.name}')

        if total_size == 0:
            put_req = urllib.request.Request(
                session_uri,
                data=b'',
                headers={
                    'Authorization': f'Bearer {self.get_access_token()}',
                    'Content-Type': mime_type,
                    'Content-Length': '0',
                    'User-Agent': USER_AGENT,
                },
                method='PUT',
            )
            return self._send_final_chunk(put_req, local_path.name)

        offset = 0
        with local_path.open('rb') as handle:
            while offset < total_size:
                chunk = handle.read(self.chunk_size)
                if not chunk:
                    break
                end = offset + len(chunk) - 1
                put_req = urllib.request.Request(
                    session_uri,
                    data=chunk,
                    headers={
                        'Authorization': f'Bearer {self.get_access_token()}',
                        'Content-Type': mime_type,
                        'Content-Length': str(len(chunk)),
                        'Content-Range': f'bytes {offset}-{end}/{total_size}',
                        'User-Agent': USER_AGENT,
                    },
                    method='PUT',
                )
                is_last = end + 1 >= total_size
                if is_last:
                    return self._send_final_chunk(put_req, local_path.name)
                try:
                    with self._open(put_req) as resp:
                        if resp.status in (200, 201):
                            parsed = _parse_body(resp.read())
                            if isinstance(parsed, dict):
                                return parsed
                except urllib.error.HTTPError as exc:
                    if exc.code == 308:
                        offset = end + 1
                        continue
                    parsed = _parse_body(exc.read())
                    raise GDriveError(
                        f'Chunk upload failed for {local_path.name} (HTTP {exc.code})',
                        status=exc.code,
                        body=parsed,
                    ) from None
                except urllib.error.URLError as exc:
                    raise GDriveError(f'Network error uploading {local_path.name}: {exc.reason}') from None
                offset = end + 1

        raise GDriveError(f'Resumable upload ended without completion response for {local_path.name}')

    def _send_final_chunk(self, req: urllib.request.Request, filename: str) -> dict:
        try:
            with self._open(req) as resp:
                parsed = _parse_body(resp.read())
        except urllib.error.HTTPError as exc:
            parsed = _parse_body(exc.read())
            raise GDriveError(f'Final upload chunk failed for {filename} (HTTP {exc.code})', status=exc.code, body=parsed) from None
        except urllib.error.URLError as exc:
            raise GDriveError(f'Network error finalizing upload for {filename}: {exc.reason}') from None
        if not isinstance(parsed, dict) or not parsed.get('id'):
            raise GDriveError(f'Google Drive returned invalid file metadata after uploading {filename}')
        return parsed


def load_tracker(root: Path) -> dict:
    tracker_path = root / 'TRACKER.json'
    if not tracker_path.exists():
        return {'boards': [], 'productions': []}
    data = json.loads(tracker_path.read_text(encoding='utf-8-sig'))
    if not isinstance(data, dict):
        raise ValueError('TRACKER.json must contain a JSON object')
    return data


def resolve_production(root: Path, slug: str, *, board_override: str | None = None) -> tuple[str, Path]:
    tracker = load_tracker(root)
    matches = [entry for entry in tracker.get('productions', []) if entry.get('slug') == slug]
    if len(matches) > 1:
        raise ValueError(f'Multiple productions registered in TRACKER.json for slug {slug!r}')
    if matches:
        entry = matches[0]
        board_name = board_override if board_override is not None else (entry.get('board') or STANDALONE_BOARD_DIR)
        rel_path = entry.get('path') or f'productions/{slug}'
    else:
        rel_path = f'productions/{slug}'
        candidate = (root / rel_path).resolve()
        if not candidate.is_dir():
            raise FileNotFoundError(f'Production {slug!r} not found in TRACKER.json or at {rel_path}')
        board_name = board_override or STANDALONE_BOARD_DIR

    prod_dir = (root / rel_path).resolve()
    if not prod_dir.is_relative_to(root.resolve()):
        raise ValueError(f'Production path escapes workspace root: {rel_path}')
    if not prod_dir.is_dir():
        raise FileNotFoundError(f'Production directory does not exist: {rel_path}')
    return board_name, prod_dir


def collect_deliverables(prod_dir: Path) -> list[Path]:
    files: list[Path] = []
    seen_names: set[str] = set()
    exports_dir = prod_dir / 'exports'
    if exports_dir.is_dir():
        for item in sorted(exports_dir.iterdir(), key=lambda p: p.name.lower()):
            if not item.is_file():
                continue
            if item.name in IGNORED_FILENAMES or item.name.startswith('.'):
                continue
            files.append(item)
            seen_names.add(item.name)

    package_file = prod_dir / 'CONTENT_PACKAGE.md'
    if package_file.is_file():
        if package_file.name in seen_names:
            raise ValueError(f'Duplicate deliverable filename {package_file.name!r} in {prod_dir}')
        files.append(package_file)
    return files


def _now_iso_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def sync_production(
    client: GDriveClient,
    root: Path,
    slug: str,
    *,
    board_override: str | None = None,
    dry_run: bool = False,
    board_folder_cache: dict[str, dict] | None = None,
) -> dict:
    board_dir_name, prod_dir = resolve_production(root, slug, board_override=board_override)
    deliverables = collect_deliverables(prod_dir)
    if not deliverables:
        return {
            'status': 'no_deliverables',
            'slug': slug,
            'board': board_dir_name,
            'remote_path': f'{board_dir_name}/{slug}',
            'files': [],
            'counts': {'uploaded': 0, 'updated': 0, 'skipped': 0},
        }

    cache = board_folder_cache if board_folder_cache is not None else {}
    board_folder: dict | None = cache.get(board_dir_name)
    slug_folder: dict | None = None

    if dry_run:
        if board_folder is None:
            board_folder = client.find_folder(client.config.root_folder_id, board_dir_name)
            if board_folder is not None:
                cache[board_dir_name] = board_folder
        if board_folder is not None:
            slug_folder = client.find_folder(board_folder['id'], slug)
    else:
        if board_folder is None:
            board_folder = client.ensure_folder(client.config.root_folder_id, board_dir_name)
            cache[board_dir_name] = board_folder
        slug_folder = client.ensure_folder(board_folder['id'], slug)

    existing_by_name: dict[str, dict] = {}
    if slug_folder is not None:
        for item in client.list_files(slug_folder['id']):
            existing_by_name.setdefault(item['name'], item)

    records: list[dict] = []
    counts = {'uploaded': 0, 'updated': 0, 'skipped': 0}

    for local_file in deliverables:
        local_md5 = file_md5(local_file)
        local_bytes = local_file.stat().st_size
        existing = existing_by_name.get(local_file.name)

        if existing and (existing.get('md5Checksum') or '').lower() == local_md5.lower():
            counts['skipped'] += 1
            records.append({
                'name': local_file.name,
                'action': 'skipped',
                'file_id': existing['id'],
                'web_view_link': existing.get('webViewLink') or f'https://drive.google.com/file/d/{existing["id"]}/view',
                'bytes': local_bytes,
                'md5': local_md5,
                'modified_time': existing.get('modifiedTime'),
            })
            continue

        if dry_run:
            action = 'would_update' if existing else 'would_upload'
            counts['updated' if existing else 'uploaded'] += 1
            records.append({
                'name': local_file.name,
                'action': action,
                'file_id': existing['id'] if existing else None,
                'web_view_link': existing.get('webViewLink') if existing else None,
                'bytes': local_bytes,
                'md5': local_md5,
                'modified_time': existing.get('modifiedTime') if existing else None,
            })
            continue

        assert slug_folder is not None
        uploaded = client.upload_file(
            slug_folder['id'],
            local_file,
            existing_file_id=existing['id'] if existing else None,
        )
        remote_md5 = (uploaded.get('md5Checksum') or '').lower()
        if remote_md5 and remote_md5 != local_md5.lower():
            raise GDriveError(
                f'MD5 mismatch after uploading {local_file.name}: local={local_md5} remote={remote_md5}'
            )
        action = 'updated' if existing else 'uploaded'
        counts['updated' if existing else 'uploaded'] += 1
        records.append({
            'name': local_file.name,
            'action': action,
            'file_id': uploaded['id'],
            'web_view_link': uploaded.get('webViewLink') or f'https://drive.google.com/file/d/{uploaded["id"]}/view',
            'bytes': local_bytes,
            'md5': local_md5,
            'modified_time': uploaded.get('modifiedTime'),
        })

    return {
        'status': 'dry_run' if dry_run else 'ok',
        'slug': slug,
        'board': board_dir_name,
        'remote_path': f'{board_dir_name}/{slug}',
        'folder_id': slug_folder['id'] if slug_folder else None,
        'folder_url': slug_folder['web_view_link'] if slug_folder else None,
        'synced_at': _now_iso_utc(),
        'files': records,
        'counts': counts,
    }


def _has_local_exports(prod_dir: Path) -> bool:
    exports_dir = prod_dir / 'exports'
    if not exports_dir.is_dir():
        return False
    return any(
        item.is_file() and item.name not in IGNORED_FILENAMES and not item.name.startswith('.')
        for item in exports_dir.iterdir()
    )


def sync_all_productions(
    client: GDriveClient,
    root: Path,
    *,
    board_filter: str | None = None,
    dry_run: bool = False,
) -> dict:
    tracker = load_tracker(root)
    board_folder_cache: dict[str, dict] = {}
    synced: list[dict] = []
    skipped_no_exports: list[str] = []
    errors: list[dict] = []

    for entry in tracker.get('productions', []):
        slug = entry.get('slug')
        if not slug:
            continue
        entry_board = entry.get('board') or STANDALONE_BOARD_DIR
        if board_filter and entry_board != board_filter:
            continue
        rel_path = entry.get('path') or f'productions/{slug}'
        prod_dir = (root / rel_path).resolve()
        if not prod_dir.is_dir() or not _has_local_exports(prod_dir):
            skipped_no_exports.append(slug)
            continue
        try:
            synced.append(
                sync_production(
                    client,
                    root,
                    slug,
                    dry_run=dry_run,
                    board_folder_cache=board_folder_cache,
                )
            )
        except Exception as exc:
            errors.append({'slug': slug, 'error': str(exc)})

    return {
        'status': 'error' if errors else ('dry_run' if dry_run else 'ok'),
        'synced_count': len(synced),
        'skipped_no_exports_count': len(skipped_no_exports),
        'error_count': len(errors),
        'synced': synced,
        'skipped_no_exports': skipped_no_exports,
        'errors': errors,
    }


def run_interactive_auth(
    root: Path,
    *,
    client_id: str | None = None,
    client_secret: str | None = None,
    port: int = 0,
    no_browser: bool = False,
    timeout: int = DEFAULT_TIMEOUT,
) -> int:
    env = env_loader.read_env(root)
    resolved_id = (client_id or _clean_config_value(env, 'GOOGLE_CLIENT_ID')).strip()
    resolved_secret = (client_secret or _clean_config_value(env, 'GOOGLE_CLIENT_SECRET')).strip()
    if not resolved_id or not resolved_secret:
        print(
            'Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in Doppler/.env or pass --client-id and --client-secret.',
            file=sys.stderr,
        )
        return 1

    expected_state = secrets.token_urlsafe(24)
    received: dict[str, str | None] = {'code': None, 'state': None, 'error': None}

    class _CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != '/callback':
                self.send_response(404)
                self.end_headers()
                return
            query = urllib.parse.parse_qs(parsed.query)
            received['code'] = (query.get('code') or [None])[0]
            received['state'] = (query.get('state') or [None])[0]
            received['error'] = (query.get('error') or [None])[0]
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            body = (
                '<html><body><h2>Google Drive authorization received</h2>'
                '<p>You can close this tab and return to your terminal.</p></body></html>'
            )
            self.wfile.write(body.encode('utf-8'))

        def log_message(self, format, *args):
            return

    server = HTTPServer(('127.0.0.1', port), _CallbackHandler)
    actual_port = server.server_address[1]
    redirect_uri = f'http://127.0.0.1:{actual_port}/callback'
    auth_url = build_auth_url(resolved_id, redirect_uri, expected_state)

    print('Open this URL in your browser to authorize Google Drive access:')
    print(auth_url)
    if not no_browser:
        webbrowser.open(auth_url)

    try:
        while received['code'] is None and received['error'] is None:
            server.handle_request()
    finally:
        server.server_close()

    if received['error']:
        print(f'Authorization failed: {received["error"]}', file=sys.stderr)
        return 1
    if received['state'] != expected_state:
        print('Authorization state mismatch (possible CSRF); aborting.', file=sys.stderr)
        return 1
    if not received['code']:
        print('No authorization code returned by Google.', file=sys.stderr)
        return 1

    token_data = exchange_oauth_token(
        {
            'code': received['code'],
            'client_id': resolved_id,
            'client_secret': resolved_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        },
        timeout=timeout,
    )
    refresh_token = token_data.get('refresh_token')
    if not refresh_token:
        print(
            'Google did not return a refresh_token. Revoke prior app access at https://myaccount.google.com/permissions and rerun auth.',
            file=sys.stderr,
        )
        return 1

    print('\nSuccess! Store this value in Doppler (primary) or your local .env (fallback):')
    print(f'GOOGLE_REFRESH_TOKEN={refresh_token}')
    print('\nTip: Publish your Google Cloud OAuth consent screen to "In Production" so the refresh token does not expire after 7 days.')
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Google Drive deliverables archiver (Doppler primary -> .env fallback).'
    )
    parser.add_argument('--root', type=Path, default=None, help='Project root containing TRACKER.json / .env')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, help='HTTP timeout in seconds')
    sub = parser.add_subparsers(dest='command', required=True)

    p_auth = sub.add_parser('auth', help='Run one-time browser OAuth 2.0 flow to obtain GOOGLE_REFRESH_TOKEN')
    p_auth.add_argument('--client-id', default=None)
    p_auth.add_argument('--client-secret', default=None)
    p_auth.add_argument('--port', type=int, default=0, help='Localhost callback port (0 = random free port)')
    p_auth.add_argument('--no-browser', action='store_true', help='Print auth URL without opening a browser')

    sub.add_parser('check', help='Verify OAuth credentials and access to GOOGLE_DRIVE_ROOT_FOLDER_ID')

    p_sync = sub.add_parser('sync', help='Sync one production deliverables folder to Google Drive')
    p_sync.add_argument('slug', help='Production slug')
    p_sync.add_argument('--board', default=None, help='Override board folder name (defaults to TRACKER.json board)')
    p_sync.add_argument('--dry-run', action='store_true', help='Plan actions without creating folders or uploading files')
    p_sync.add_argument(
        '--graceful',
        action='store_true',
        help='Exit 0 with status=not_configured when Google Drive keys are unset (used by content_package)',
    )

    p_all = sub.add_parser('sync-all', help='Backfill all productions in TRACKER.json that have local exports/')
    p_all.add_argument('--board', default=None, help='Filter to one board slug')
    p_all.add_argument('--dry-run', action='store_true', help='Plan actions without creating folders or uploading files')

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    root = env_loader.find_project_root(args.root)

    if args.command == 'auth':
        return run_interactive_auth(
            root,
            client_id=args.client_id,
            client_secret=args.client_secret,
            port=args.port,
            no_browser=args.no_browser,
            timeout=args.timeout,
        )

    retry_cmd = None
    if args.command == 'sync':
        retry_cmd = f'python .agents/skills/shortform-production/scripts/gdrive.py sync {args.slug}'

    try:
        config, env_meta = resolve_config(root)
        if config is None:
            payload: dict[str, object] = {
                'status': 'not_configured',
                'env_source': env_meta['source'],
                'message': 'Google Drive credentials (GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET/GOOGLE_REFRESH_TOKEN/GOOGLE_DRIVE_ROOT_FOLDER_ID) are not configured in Doppler or .env.',
            }
            if args.command == 'sync' and args.graceful:
                print(json.dumps(payload, ensure_ascii=False, indent=2))
                return 0
            print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
            return 1

        client = GDriveClient(config, timeout=args.timeout)
        if args.command == 'check':
            folder = client.check_root_folder()
            result: dict[str, object] = {
                'status': 'ok',
                'env_source': env_meta['source'],
                'root_folder': folder,
            }
        elif args.command == 'sync':
            result = sync_production(client, root, args.slug, board_override=args.board, dry_run=args.dry_run)
            result['env_source'] = env_meta['source']
            if result['status'] == 'no_deliverables':
                print(json.dumps(result, ensure_ascii=False, indent=2), file=sys.stderr)
                return 1
        elif args.command == 'sync-all':
            result = sync_all_productions(client, root, board_filter=args.board, dry_run=args.dry_run)
            result['env_source'] = env_meta['source']
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result['error_count'] == 0 else 1
        else:
            raise ValueError(f'Unknown command: {args.command}')
    except GDriveError as exc:
        err: dict[str, object] = {
            'status': 'error',
            'message': str(exc),
            'http_status': exc.status,
            'body': exc.body,
        }
        if retry_cmd:
            err['retry_command'] = retry_cmd
        print(json.dumps(err, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
    except Exception as exc:
        err = {'status': 'error', 'message': str(exc)}
        if retry_cmd:
            err['retry_command'] = retry_cmd
        print(json.dumps(err, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
