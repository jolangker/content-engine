"""Trypost REST API client for publishing, account lookup, and performance analytics.

Preferred transport over MCP when TRYPOST_BASE_URL and TRYPOST_API_KEY are configured
in Doppler (primary) or the project root .env (fallback). Uses only the Python standard
library and never prints credentials.
"""
from __future__ import annotations

import argparse
import json
import mimetypes
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
import env_loader


USER_AGENT = 'content-engine/1.0'
PLACEHOLDER_URLS = {'', 'your-trypost-base-url'}
PLACEHOLDER_KEYS = {'', 'your-trypost-api-key'}
DEFAULT_TIMEOUT = 60


def read_env(root: Path) -> dict[str, str]:
    return env_loader.read_env(root)


def find_project_root(start: Path | None = None) -> Path:
    return env_loader.find_project_root(start)


def resolve_config(root: Path) -> tuple[str, str]:
    env = read_env(root)
    base_url = env.get('TRYPOST_BASE_URL', '').strip().rstrip('/')
    api_key = env.get('TRYPOST_API_KEY', '').strip()
    if base_url.lower() in PLACEHOLDER_URLS or not base_url.startswith(('http://', 'https://')):
        raise ValueError('Set a valid TRYPOST_BASE_URL in Doppler or the project root .env')
    if api_key.lower() in PLACEHOLDER_KEYS:
        raise ValueError('Set TRYPOST_API_KEY in Doppler or the project root .env')
    return base_url, api_key


class TrypostError(RuntimeError):
    def __init__(self, message: str, *, status: int | None = None, body: object = None):
        super().__init__(message)
        self.status = status
        self.body = body


def build_multipart_file(field_name: str, file_path: Path, boundary: str | None = None) -> tuple[bytes, str]:
    boundary = boundary or f'----ContentEngineTrypost{uuid.uuid4().hex}'
    mime_type = mimetypes.guess_type(file_path.name)[0] or 'application/octet-stream'
    filename = file_path.name.replace('"', '_')
    header = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'
        f'Content-Type: {mime_type}\r\n\r\n'
    ).encode('utf-8')
    footer = f'\r\n--{boundary}--\r\n'.encode('utf-8')
    payload = header + file_path.read_bytes() + footer
    return payload, f'multipart/form-data; boundary={boundary}'


def _parse_response_body(raw: bytes) -> object:
    text = raw.decode('utf-8', errors='replace').strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


class TrypostClient:
    def __init__(self, base_url: str, api_key: str, *, timeout: int = DEFAULT_TIMEOUT,
                 opener=None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self._opener = opener

    def _headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json',
            'User-Agent': USER_AGENT,
        }
        if extra:
            headers.update(extra)
        return headers

    def request(self, method: str, path: str, *, params: list[tuple[str, str]] | None = None,
                json_body: object = None, raw_body: bytes | None = None,
                content_type: str | None = None) -> object:
        clean_path = '/' + path.lstrip('/')
        url = self.base_url + clean_path
        if params:
            query = urllib.parse.urlencode(params, doseq=True)
            url = f'{url}?{query}'

        extra_headers: dict[str, str] = {}
        data: bytes | None = raw_body
        if json_body is not None:
            data = json.dumps(json_body, ensure_ascii=False).encode('utf-8')
            extra_headers['Content-Type'] = 'application/json'
        elif content_type:
            extra_headers['Content-Type'] = content_type

        req = urllib.request.Request(url, data=data, headers=self._headers(extra_headers), method=method.upper())
        opener = self._opener or urllib.request.urlopen
        try:
            with opener(req, timeout=self.timeout) as resp:
                return _parse_response_body(resp.read())
        except urllib.error.HTTPError as exc:
            parsed = _parse_response_body(exc.read())
            raise TrypostError(f'HTTP {exc.code} {method.upper()} {clean_path}', status=exc.code, body=parsed) from None
        except urllib.error.URLError as exc:
            raise TrypostError(f'Network error on {method.upper()} {clean_path}: {exc.reason}') from None

    def get_workspace(self) -> object:
        return self.request('GET', '/workspace')

    def list_accounts(self, *, page: int | None = None, fetch_all: bool = False) -> object:
        if not fetch_all:
            params = [('page', str(page))] if page is not None else None
            return self.request('GET', '/social-accounts', params=params)
        collected: list[object] = []
        current = 1
        last_page = 1
        total = None
        while current <= last_page:
            resp = self.request('GET', '/social-accounts', params=[('page', str(current))])
            if not isinstance(resp, dict):
                return resp
            collected.extend(resp.get('data', []))
            last_page = int(resp.get('last_page') or current)
            total = resp.get('total', len(collected))
            current += 1
        return {'data': collected, 'total': total, 'pages_fetched': last_page}

    def list_content_types(self) -> object:
        return self.request('GET', '/content-types')

    def list_posts(self, *, page: int | None = None, status: str | None = None,
                   social_account_id: str | None = None, search: str | None = None) -> object:
        params: list[tuple[str, str]] = []
        if page is not None:
            params.append(('page', str(page)))
        if status:
            params.append(('status', status))
        if social_account_id:
            params.append(('social_account_id', social_account_id))
        if search:
            params.append(('search', search))
        return self.request('GET', '/posts', params=params or None)

    def get_post(self, post_id: str) -> object:
        return self.request('GET', f'/posts/{post_id}')

    def create_post(self, payload: dict) -> object:
        return self.request('POST', '/posts', json_body=payload)

    def update_post(self, post_id: str, payload: dict) -> object:
        return self.request('PUT', f'/posts/{post_id}', json_body=payload)

    def delete_post(self, post_id: str) -> object:
        return self.request('DELETE', f'/posts/{post_id}')

    def upload_media(self, file_path: Path) -> object:
        if not file_path.is_file():
            raise FileNotFoundError(f'Media file not found: {file_path}')
        body, content_type = build_multipart_file('media', file_path)
        return self.request('POST', '/uploads', raw_body=body, content_type=content_type)

    def attach_media(self, post_id: str, *, upload_token: str | None = None,
                     url: str | None = None, alt: str | None = None) -> object:
        if bool(upload_token) == bool(url):
            raise ValueError('Provide exactly one of upload_token or url')
        payload: dict[str, object] = {}
        if upload_token:
            payload['upload_token'] = upload_token
        if url:
            payload['url'] = url
        if alt is not None:
            payload['alt'] = alt
        return self.request('POST', f'/posts/{post_id}/media', json_body=payload)

    def get_post_metrics(self, post_id: str) -> object:
        return self.request('GET', f'/posts/{post_id}/metrics')

    def get_analytics(self, *, range_preset: str | None = None, start: str | None = None,
                      end: str | None = None, channels: list[str] | None = None) -> object:
        params: list[tuple[str, str]] = []
        if range_preset:
            params.append(('range', range_preset))
        if start:
            params.append(('start', start))
        if end:
            params.append(('end', end))
        for ch in channels or []:
            params.append(('channels[]', ch))
        return self.request('GET', '/analytics', params=params or None)

    def get_channel_insights(self, account_id: str, *, range_preset: str | None = None,
                             start: str | None = None, end: str | None = None) -> object:
        params: list[tuple[str, str]] = []
        if range_preset:
            params.append(('range', range_preset))
        if start:
            params.append(('start', start))
        if end:
            params.append(('end', end))
        return self.request('GET', f'/channels/{account_id}/insights', params=params or None)

    def list_channel_publications(self, account_id: str, *, range_preset: str | None = None,
                                  start: str | None = None, end: str | None = None,
                                  page: int | None = None) -> object:
        params: list[tuple[str, str]] = []
        if range_preset:
            params.append(('range', range_preset))
        if start:
            params.append(('start', start))
        if end:
            params.append(('end', end))
        if page is not None:
            params.append(('page', str(page)))
        return self.request('GET', f'/channels/{account_id}/insights/publications', params=params or None)

    def list_free_slots(self, account_id: str) -> object:
        return self.request('GET', f'/channels/{account_id}/queue/slots')

    def get_posting_schedule(self, account_id: str) -> object:
        return self.request('GET', f'/channels/{account_id}/posting-schedule')

    def get_tiktok_creator_info(self, account_id: str) -> object:
        return self.request('GET', f'/social-accounts/{account_id}/tiktok-creator-info')


def _load_json_arg(json_str: str | None, json_file: str | None) -> dict:
    if json_file:
        data = json.loads(Path(json_file).read_text(encoding='utf-8-sig'))
    elif json_str:
        data = json.loads(json_str)
    else:
        raise ValueError('Provide --json or --json-file')
    if not isinstance(data, dict):
        raise ValueError('JSON payload must be an object')
    return data


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Trypost REST API client (default transport before MCP).')
    parser.add_argument('--root', type=Path, default=None, help='Project root containing .env')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, help='HTTP timeout in seconds')
    sub = parser.add_subparsers(dest='command', required=True)

    sub.add_parser('check', help='Verify TRYPOST_BASE_URL + TRYPOST_API_KEY via GET /workspace')
    sub.add_parser('workspace', help='Get current workspace and caller permissions')

    p_acc = sub.add_parser('accounts', help='List connected social accounts')
    p_acc.add_argument('--page', type=int, default=None)
    p_acc.add_argument('--all', action='store_true', dest='fetch_all', help='Fetch all pages')

    sub.add_parser('content-types', help='List platform content types and media rules')

    p_posts = sub.add_parser('posts', help='List posts')
    p_posts.add_argument('--page', type=int, default=None)
    p_posts.add_argument('--status', default=None)
    p_posts.add_argument('--social-account-id', default=None)
    p_posts.add_argument('--search', default=None)

    p_get = sub.add_parser('get-post', help='Get one post by ID')
    p_get.add_argument('post_id')

    p_create = sub.add_parser('create-post', help='Create a post from JSON')
    p_create.add_argument('--json', dest='json_str', default=None)
    p_create.add_argument('--json-file', default=None)

    p_update = sub.add_parser('update-post', help='Update a post by ID from JSON')
    p_update.add_argument('post_id')
    p_update.add_argument('--json', dest='json_str', default=None)
    p_update.add_argument('--json-file', default=None)

    p_del = sub.add_parser('delete-post', help='Delete a post by ID')
    p_del.add_argument('post_id')

    p_up = sub.add_parser('upload-media', help='Upload a local media file via POST /uploads')
    p_up.add_argument('file_path', type=Path)

    p_att = sub.add_parser('attach-media', help='Attach uploaded token or URL to a post')
    p_att.add_argument('post_id')
    p_att.add_argument('--upload-token', default=None)
    p_att.add_argument('--url', default=None)
    p_att.add_argument('--alt', default=None)

    p_met = sub.add_parser('post-metrics', help='Get saved analytics metrics for a published post')
    p_met.add_argument('post_id')

    p_an = sub.add_parser('analytics', help='Get workspace analytics report')
    p_an.add_argument('--range', dest='range_preset', default=None)
    p_an.add_argument('--start', default=None)
    p_an.add_argument('--end', default=None)
    p_an.add_argument('--channel', action='append', dest='channels', default=None)

    p_ci = sub.add_parser('channel-insights', help='Get insights for one social account')
    p_ci.add_argument('account_id')
    p_ci.add_argument('--range', dest='range_preset', default=None)
    p_ci.add_argument('--start', default=None)
    p_ci.add_argument('--end', default=None)

    p_cp = sub.add_parser('channel-publications', help='List ranked publications for one social account')
    p_cp.add_argument('account_id')
    p_cp.add_argument('--range', dest='range_preset', default=None)
    p_cp.add_argument('--start', default=None)
    p_cp.add_argument('--end', default=None)
    p_cp.add_argument('--page', type=int, default=None)

    p_slots = sub.add_parser('free-slots', help='List free queue slots for one social account')
    p_slots.add_argument('account_id')

    p_sched = sub.add_parser('posting-schedule', help='Get posting schedule for one social account')
    p_sched.add_argument('account_id')

    p_tt = sub.add_parser('tiktok-creator-info', help='Get TikTok creator info for a TikTok social account')
    p_tt.add_argument('account_id')

    p_req = sub.add_parser('request', help='Send a raw authenticated request to any Trypost API route')
    p_req.add_argument('method', choices=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
    p_req.add_argument('path')
    p_req.add_argument('--query', action='append', default=[], help='Repeatable key=value query parameter')
    p_req.add_argument('--json', dest='json_str', default=None)
    p_req.add_argument('--json-file', default=None)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    root = find_project_root(args.root)
    try:
        base_url, api_key = resolve_config(root)
        client = TrypostClient(base_url, api_key, timeout=args.timeout)
        cmd = args.command
        if cmd == 'check':
            ws = client.get_workspace()
            result: object = {'status': 'ok', 'transport': 'api', 'base_url': base_url, 'workspace': ws}
        elif cmd == 'workspace':
            result = client.get_workspace()
        elif cmd == 'accounts':
            result = client.list_accounts(page=args.page, fetch_all=args.fetch_all)
        elif cmd == 'content-types':
            result = client.list_content_types()
        elif cmd == 'posts':
            result = client.list_posts(page=args.page, status=args.status,
                                       social_account_id=args.social_account_id, search=args.search)
        elif cmd == 'get-post':
            result = client.get_post(args.post_id)
        elif cmd == 'create-post':
            result = client.create_post(_load_json_arg(args.json_str, args.json_file))
        elif cmd == 'update-post':
            result = client.update_post(args.post_id, _load_json_arg(args.json_str, args.json_file))
        elif cmd == 'delete-post':
            result = client.delete_post(args.post_id)
        elif cmd == 'upload-media':
            result = client.upload_media(args.file_path)
        elif cmd == 'attach-media':
            result = client.attach_media(args.post_id, upload_token=args.upload_token, url=args.url, alt=args.alt)
        elif cmd == 'post-metrics':
            result = client.get_post_metrics(args.post_id)
        elif cmd == 'analytics':
            result = client.get_analytics(range_preset=args.range_preset, start=args.start,
                                          end=args.end, channels=args.channels)
        elif cmd == 'channel-insights':
            result = client.get_channel_insights(args.account_id, range_preset=args.range_preset,
                                                 start=args.start, end=args.end)
        elif cmd == 'channel-publications':
            result = client.list_channel_publications(args.account_id, range_preset=args.range_preset,
                                                      start=args.start, end=args.end, page=args.page)
        elif cmd == 'free-slots':
            result = client.list_free_slots(args.account_id)
        elif cmd == 'posting-schedule':
            result = client.get_posting_schedule(args.account_id)
        elif cmd == 'tiktok-creator-info':
            result = client.get_tiktok_creator_info(args.account_id)
        elif cmd == 'request':
            params = []
            for item in args.query:
                if '=' not in item:
                    raise ValueError(f'Expected key=value for --query, got {item!r}')
                k, v = item.split('=', 1)
                params.append((k, v))
            body = _load_json_arg(args.json_str, args.json_file) if (args.json_str or args.json_file) else None
            result = client.request(args.method, args.path, params=params or None, json_body=body)
        else:
            raise ValueError(f'Unknown command: {cmd}')
    except TrypostError as exc:
        err = {'status': 'error', 'transport': 'api', 'message': str(exc), 'http_status': exc.status, 'body': exc.body}
        print(json.dumps(err, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
    except Exception as exc:
        err = {'status': 'error', 'transport': 'api', 'message': str(exc)}
        print(json.dumps(err, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
