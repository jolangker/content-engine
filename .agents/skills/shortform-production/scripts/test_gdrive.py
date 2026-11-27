"""Offline unit tests for gdrive.py (Google Drive deliverables archiver); no network calls."""
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
import urllib.error
import urllib.parse
from unittest.mock import patch

import env_loader
import gdrive


class _FakeHeaders(dict):
    def get(self, key, default=None):
        for k, v in self.items():
            if k.lower() == key.lower():
                return v
        return default


class _FakeResponse:
    def __init__(self, payload: object = None, *, status: int = 200, headers: dict[str, str] | None = None):
        if payload is None:
            self._raw = b''
        elif isinstance(payload, bytes):
            self._raw = payload
        else:
            self._raw = json.dumps(payload).encode('utf-8')
        self.status = status
        self.headers = _FakeHeaders(headers or {})

    def read(self) -> bytes:
        return self._raw

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class _FakeDriveServer:
    """In-memory mock of Google OAuth2 + Drive API v3 (folders + resumable uploads)."""

    def __init__(self, root_folder_id: str = 'root-1'):
        self.root_folder_id = root_folder_id
        self.folders: dict[str, dict] = {
            root_folder_id: {
                'id': root_folder_id,
                'name': 'Content Engine Deliverables',
                'mimeType': gdrive.FOLDER_MIME,
                'trashed': False,
                'webViewLink': f'https://drive.google.com/drive/folders/{root_folder_id}',
                'parents': [],
            }
        }
        self.files: dict[str, dict] = {}
        self.sessions: dict[str, dict] = {}
        self._next_id = 1
        self.calls: list[tuple[str, str]] = []

    def _new_id(self, prefix: str) -> str:
        val = f'{prefix}-{self._next_id}'
        self._next_id += 1
        return val

    def seed_folder(self, parent_id: str, name: str) -> str:
        fid = self._new_id('fld')
        self.folders[fid] = {
            'id': fid,
            'name': name,
            'mimeType': gdrive.FOLDER_MIME,
            'trashed': False,
            'webViewLink': f'https://drive.google.com/drive/folders/{fid}',
            'parents': [parent_id],
        }
        return fid

    def seed_file(self, parent_id: str, name: str, data: bytes) -> str:
        fid = self._new_id('file')
        self.files[fid] = {
            'id': fid,
            'name': name,
            'parents': [parent_id],
            'data': data,
            'md5Checksum': hashlib.md5(data).hexdigest(),
            'size': str(len(data)),
            'modifiedTime': '2026-11-27T00:00:00Z',
            'webViewLink': f'https://drive.google.com/file/d/{fid}/view',
        }
        return fid

    def opener(self, req, timeout=120):
        method = req.get_method()
        url = req.full_url
        self.calls.append((method, url))
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query)

        if url == gdrive.OAUTH_TOKEN_URL:
            return _FakeResponse({'access_token': 'ya29.fake-access-token', 'expires_in': 3600})

        if url.startswith('https://upload.example.test/session/'):
            sess = self.sessions[url]
            chunk = req.data or b''
            sess['buffer'].extend(chunk)
            content_range = req.get_header('Content-range')
            if content_range:
                span, total_str = content_range.removeprefix('bytes ').split('/')
                _, end_str = span.split('-')
                if int(end_str) + 1 < int(total_str):
                    raise urllib.error.HTTPError(url, 308, 'Resume Incomplete', {}, io.BytesIO(b''))
            data = bytes(sess['buffer'])
            md5 = hashlib.md5(data).hexdigest()
            if sess['existing_id']:
                fid = sess['existing_id']
                self.files[fid]['data'] = data
                self.files[fid]['md5Checksum'] = md5
                self.files[fid]['size'] = str(len(data))
                self.files[fid]['modifiedTime'] = '2026-11-27T02:00:00Z'
            else:
                fid = self._new_id('file')
                self.files[fid] = {
                    'id': fid,
                    'name': sess['name'],
                    'parents': [sess['parent_id']],
                    'data': data,
                    'md5Checksum': md5,
                    'size': str(len(data)),
                    'modifiedTime': '2026-11-27T01:00:00Z',
                    'webViewLink': f'https://drive.google.com/file/d/{fid}/view',
                }
            meta = {k: v for k, v in self.files[fid].items() if k != 'data'}
            return _FakeResponse(meta, status=200)

        if parsed.path.startswith('/upload/drive/v3/files'):
            body = json.loads((req.data or b'{}').decode('utf-8'))
            existing_id = None
            if method == 'PATCH':
                existing_id = parsed.path.rsplit('/', 1)[-1]
            sess_url = f'https://upload.example.test/session/{self._new_id("sess")}'
            self.sessions[sess_url] = {
                'name': body['name'],
                'parent_id': (body.get('parents') or [None])[0],
                'existing_id': existing_id,
                'buffer': bytearray(),
            }
            return _FakeResponse(None, status=200, headers={'Location': sess_url})

        if parsed.path == '/drive/v3/files' and method == 'GET':
            q = (query.get('q') or [''])[0]
            if f"mimeType = '{gdrive.FOLDER_MIME}'" in q:
                # Folder lookup
                matches = []
                for fld in self.folders.values():
                    if f"name = '{fld['name']}'" in q and any(f"'{p}' in parents" in q for p in fld['parents']):
                        matches.append(fld)
                return _FakeResponse({'files': matches})
            else:
                # File list inside folder
                matches = []
                for item in self.files.values():
                    if any(f"'{p}' in parents" in q for p in item['parents']):
                        matches.append({k: v for k, v in item.items() if k != 'data'})
                return _FakeResponse({'files': matches})

        if parsed.path == '/drive/v3/files' and method == 'POST':
            body = json.loads((req.data or b'{}').decode('utf-8'))
            fid = self.seed_folder(body['parents'][0], body['name'])
            return _FakeResponse(self.folders[fid])

        if parsed.path.startswith('/drive/v3/files/') and method == 'GET':
            fid = parsed.path.rsplit('/', 1)[-1]
            if fid in self.folders:
                return _FakeResponse(self.folders[fid])
            raise urllib.error.HTTPError(url, 404, 'Not Found', {}, io.BytesIO(b'{"error": "not found"}'))

        raise AssertionError(f'Unhandled mock Drive request: {method} {url}')


class GDriveTests(unittest.TestCase):
    def setUp(self):
        env_loader.clear_cache()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env_patch = patch.dict(os.environ, {'DOPPLER_TOKEN': ''}, clear=False)
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)

        self.tracker = {
            'boards': [{'slug': 'budidaya-di-halaman', 'status': 'approved', 'path': 'boards/budidaya-di-halaman'}],
            'productions': [
                {
                    'slug': 'ternak-cupang',
                    'topic': 'Betta backyard build',
                    'board': 'budidaya-di-halaman',
                    'stage': 'content_package',
                    'status': 'complete',
                    'path': 'productions/ternak-cupang',
                },
                {
                    'slug': 'episode-standalone',
                    'topic': 'No board episode',
                    'board': None,
                    'stage': 'content_package',
                    'status': 'complete',
                    'path': 'productions/episode-standalone',
                },
                {
                    'slug': 'belum-export',
                    'topic': 'Script only',
                    'board': 'budidaya-di-halaman',
                    'stage': 'script',
                    'status': 'complete',
                    'path': 'productions/belum-export',
                },
            ],
        }
        (self.root / 'TRACKER.json').write_text(json.dumps(self.tracker), encoding='utf-8')

        p1 = self.root / 'productions/ternak-cupang'
        (p1 / 'exports').mkdir(parents=True)
        (p1 / 'exports/ternak-cupang.mp4').write_bytes(b'A' * 1200)
        (p1 / 'exports/thumbnail.png').write_bytes(b'PNGDATA')
        (p1 / 'exports/ternak-cupang.srt').write_text('1\n00:00:00,000 --> 00:00:01,000\nHalo\n', encoding='utf-8')
        (p1 / 'exports/.DS_Store').write_bytes(b'junk')
        (p1 / 'CONTENT_PACKAGE.md').write_text('# Content Package\n', encoding='utf-8')

        p2 = self.root / 'productions/episode-standalone'
        (p2 / 'exports').mkdir(parents=True)
        (p2 / 'exports/episode-standalone.mp4').write_bytes(b'STANDALONE_MP4')
        (p2 / 'CONTENT_PACKAGE.md').write_text('# Standalone\n', encoding='utf-8')

        (self.root / 'productions/belum-export').mkdir(parents=True)
        (self.root / 'productions/belum-export/SCRIPT.md').write_text('# Script\n', encoding='utf-8')

    def _write_gdrive_env(self):
        (self.root / '.env').write_text(
            'GOOGLE_CLIENT_ID="cid-123"\n'
            'GOOGLE_CLIENT_SECRET="super-secret-client"\n'
            'GOOGLE_REFRESH_TOKEN="super-secret-refresh"\n'
            'GOOGLE_DRIVE_ROOT_FOLDER_ID="root-1"\n',
            encoding='utf-8',
        )

    def test_resolve_config_handles_unconfigured_partial_and_complete(self):
        cfg, _ = gdrive.resolve_config(self.root)
        self.assertIsNone(cfg)

        (self.root / '.env').write_text(
            'GOOGLE_CLIENT_ID="your-google-client-id"\n'
            'GOOGLE_CLIENT_SECRET="your-google-client-secret"\n',
            encoding='utf-8',
        )
        cfg, _ = gdrive.resolve_config(self.root)
        self.assertIsNone(cfg)

        (self.root / '.env').write_text('GOOGLE_CLIENT_ID="real-id"\n', encoding='utf-8')
        with self.assertRaises(ValueError) as ctx:
            gdrive.resolve_config(self.root)
        self.assertIn('GOOGLE_REFRESH_TOKEN', str(ctx.exception))

        self._write_gdrive_env()
        cfg, meta = gdrive.resolve_config(self.root)
        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.root_folder_id, 'root-1')
        self.assertEqual(meta['source'], 'dotenv')

    def test_sync_creates_board_and_slug_folders_uploads_chunked_and_skips_unchanged(self):
        self._write_gdrive_env()
        server = _FakeDriveServer('root-1')
        cfg, _ = gdrive.resolve_config(self.root)
        # Small chunk size forces multi-chunk HTTP 308 flow on 1200-byte MP4
        client = gdrive.GDriveClient(cfg, chunk_size=512, opener=server.opener)

        res1 = gdrive.sync_production(client, self.root, 'ternak-cupang')
        self.assertEqual(res1['status'], 'ok')
        self.assertEqual(res1['remote_path'], 'budidaya-di-halaman/ternak-cupang')
        self.assertEqual(res1['counts'], {'uploaded': 4, 'updated': 0, 'skipped': 0})
        names = [f['name'] for f in res1['files']]
        self.assertEqual(
            set(names),
            {'ternak-cupang.mp4', 'thumbnail.png', 'ternak-cupang.srt', 'CONTENT_PACKAGE.md'},
        )
        self.assertNotIn('.DS_Store', names)

        # Second sync with unchanged files skips all 4
        res2 = gdrive.sync_production(client, self.root, 'ternak-cupang')
        self.assertEqual(res2['counts'], {'uploaded': 0, 'updated': 0, 'skipped': 4})

        # Edit CONTENT_PACKAGE.md -> updates in-place (keeps exact same file_id)
        old_pkg_id = next(f['file_id'] for f in res1['files'] if f['name'] == 'CONTENT_PACKAGE.md')
        (self.root / 'productions/ternak-cupang/CONTENT_PACKAGE.md').write_text('# Updated copy\n', encoding='utf-8')
        res3 = gdrive.sync_production(client, self.root, 'ternak-cupang')
        self.assertEqual(res3['counts'], {'uploaded': 0, 'updated': 1, 'skipped': 3})
        new_pkg = next(f for f in res3['files'] if f['name'] == 'CONTENT_PACKAGE.md')
        self.assertEqual(new_pkg['action'], 'updated')
        self.assertEqual(new_pkg['file_id'], old_pkg_id)

    def test_dry_run_does_not_create_remote_folders_or_upload(self):
        self._write_gdrive_env()
        server = _FakeDriveServer('root-1')
        cfg, _ = gdrive.resolve_config(self.root)
        client = gdrive.GDriveClient(cfg, opener=server.opener)

        res = gdrive.sync_production(client, self.root, 'ternak-cupang', dry_run=True)
        self.assertEqual(res['status'], 'dry_run')
        self.assertIsNone(res['folder_id'])
        self.assertEqual(res['counts'], {'uploaded': 4, 'updated': 0, 'skipped': 0})
        self.assertTrue(all(f['action'] == 'would_upload' for f in res['files']))
        self.assertEqual(len(server.folders), 1)
        self.assertEqual(len(server.files), 0)

    def test_sync_all_backfills_only_productions_with_exports_and_uses_standalone(self):
        self._write_gdrive_env()
        server = _FakeDriveServer('root-1')
        cfg, _ = gdrive.resolve_config(self.root)
        client = gdrive.GDriveClient(cfg, opener=server.opener)

        res = gdrive.sync_all_productions(client, self.root)
        self.assertEqual(res['status'], 'ok')
        self.assertEqual(res['synced_count'], 2)
        self.assertEqual(res['skipped_no_exports'], ['belum-export'])
        paths = {item['slug']: item['remote_path'] for item in res['synced']}
        self.assertEqual(paths['ternak-cupang'], 'budidaya-di-halaman/ternak-cupang')
        self.assertEqual(paths['episode-standalone'], '_standalone/episode-standalone')

    def test_cli_graceful_not_configured_and_check_never_leaks_secrets(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with patch('sys.stdout', stdout), patch('sys.stderr', stderr):
            code = gdrive.main(['--root', str(self.root), 'sync', 'ternak-cupang', '--graceful'])
        self.assertEqual(code, 0)
        parsed = json.loads(stdout.getvalue())
        self.assertEqual(parsed['status'], 'not_configured')

        self._write_gdrive_env()
        server = _FakeDriveServer('root-1')
        stdout2 = io.StringIO()
        with (
            patch('gdrive.urllib.request.urlopen', side_effect=server.opener),
            patch('sys.stdout', stdout2),
        ):
            code2 = gdrive.main(['--root', str(self.root), 'check'])
        self.assertEqual(code2, 0)
        out2 = stdout2.getvalue()
        self.assertNotIn('super-secret-client', out2)
        self.assertNotIn('super-secret-refresh', out2)
        self.assertNotIn('ya29.fake-access-token', out2)
        parsed2 = json.loads(out2)
        self.assertEqual(parsed2['status'], 'ok')
        self.assertEqual(parsed2['root_folder']['id'], 'root-1')


if __name__ == '__main__':
    unittest.main()
