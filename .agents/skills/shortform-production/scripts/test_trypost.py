"""Offline unit tests for the Trypost REST API client; no network calls."""
import io
import json
from pathlib import Path
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

from trypost import TrypostClient, TrypostError, USER_AGENT, build_multipart_file, main, resolve_config


class _FakeResponse:
    def __init__(self, payload: object, status: int = 200):
        self._raw = json.dumps(payload).encode('utf-8') if not isinstance(payload, bytes) else payload
        self.status = status

    def read(self) -> bytes:
        return self._raw

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class TrypostTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / '.env').write_text(
            'TRYPOST_BASE_URL="https://trypost.example.test/api/" # api root\n'
            'TRYPOST_API_KEY=secret-token-value\n',
            encoding='utf-8',
        )

    def test_resolve_config_parses_and_normalizes(self):
        base, key = resolve_config(self.root)
        self.assertEqual(base, 'https://trypost.example.test/api')
        self.assertEqual(key, 'secret-token-value')

    def test_resolve_config_rejects_missing_or_placeholders(self):
        for content in (
            '',
            'TRYPOST_BASE_URL=your-trypost-base-url\nTRYPOST_API_KEY=real-key\n',
            'TRYPOST_BASE_URL=https://trypost.example.test/api\nTRYPOST_API_KEY=your-trypost-api-key\n',
            'TRYPOST_BASE_URL=not-a-url\nTRYPOST_API_KEY=real-key\n',
        ):
            with self.subTest(content=content):
                (self.root / '.env').write_text(content, encoding='utf-8')
                with self.assertRaises(ValueError):
                    resolve_config(self.root)

    def test_request_sends_bearer_auth_and_custom_user_agent(self):
        seen = []

        def fake_open(req, timeout=None):
            seen.append((req.get_method(), req.full_url, dict(req.header_items()), req.data, timeout))
            return _FakeResponse({'id': 'ws-1', 'name': 'Test Workspace'})

        client = TrypostClient('https://trypost.example.test/api', 'secret-token-value', opener=fake_open)
        ws = client.get_workspace()
        self.assertEqual(ws['id'], 'ws-1')
        method, url, headers, data, _ = seen[0]
        self.assertEqual(method, 'GET')
        self.assertEqual(url, 'https://trypost.example.test/api/workspace')
        self.assertEqual(headers['Authorization'], 'Bearer secret-token-value')
        self.assertEqual(headers['Accept'], 'application/json')
        self.assertEqual(headers['User-agent'], USER_AGENT)
        self.assertIsNone(data)

    def test_list_accounts_fetch_all_paginates(self):
        pages = {
            '1': {'data': [{'id': 'a1'}], 'current_page': 1, 'last_page': 2, 'total': 2},
            '2': {'data': [{'id': 'a2'}], 'current_page': 2, 'last_page': 2, 'total': 2},
        }

        def fake_open(req, timeout=None):
            page = req.full_url.split('page=')[-1]
            return _FakeResponse(pages[page])

        client = TrypostClient('https://trypost.example.test/api', 'k', opener=fake_open)
        result = client.list_accounts(fetch_all=True)
        self.assertEqual([a['id'] for a in result['data']], ['a1', 'a2'])
        self.assertEqual(result['pages_fetched'], 2)

    def test_upload_media_builds_multipart_form(self):
        sample = self.root / 'clip.mp4'
        sample.write_bytes(b'\x00\x00\x00\x18ftypmp42')
        body, content_type = build_multipart_file('media', sample, boundary='TESTBOUND')
        self.assertEqual(content_type, 'multipart/form-data; boundary=TESTBOUND')
        self.assertIn(b'name="media"; filename="clip.mp4"', body)
        self.assertIn(b'Content-Type: video/mp4', body)
        self.assertIn(b'ftypmp42', body)

        seen = []

        def fake_open(req, timeout=None):
            seen.append((req.get_method(), req.full_url, dict(req.header_items()), req.data))
            return _FakeResponse({'upload_token': 'tok-1'})

        client = TrypostClient('https://trypost.example.test/api', 'k', opener=fake_open)
        resp = client.upload_media(sample)
        self.assertEqual(resp['upload_token'], 'tok-1')
        self.assertEqual(seen[0][0], 'POST')
        self.assertEqual(seen[0][1], 'https://trypost.example.test/api/uploads')
        self.assertTrue(seen[0][2]['Content-type'].startswith('multipart/form-data; boundary='))

    def test_http_error_surfaces_structured_trypost_error(self):
        def fake_open(req, timeout=None):
            raise urllib.error.HTTPError(
                req.full_url, 422, 'Unprocessable Entity', {},
                io.BytesIO(json.dumps({'message': 'Invalid payload'}).encode('utf-8')),
            )

        client = TrypostClient('https://trypost.example.test/api', 'k', opener=fake_open)
        with self.assertRaises(TrypostError) as ctx:
            client.create_post({'social_account_id': 'acc-1'})
        self.assertEqual(ctx.exception.status, 422)
        self.assertEqual(ctx.exception.body, {'message': 'Invalid payload'})

    def test_cli_check_never_leaks_api_key(self):
        stdout = io.StringIO()
        stderr = io.StringIO()

        def fake_open(req, timeout=None):
            return _FakeResponse({'id': 'ws-1', 'name': 'Demo'})

        with patch('trypost.urllib.request.urlopen', side_effect=fake_open), \
             patch('sys.stdout', stdout), patch('sys.stderr', stderr):
            code = main(['--root', str(self.root), 'check'])
        self.assertEqual(code, 0)
        out = stdout.getvalue()
        self.assertNotIn('secret-token-value', out)
        parsed = json.loads(out)
        self.assertEqual(parsed['status'], 'ok')
        self.assertEqual(parsed['transport'], 'api')
        self.assertEqual(parsed['workspace']['id'], 'ws-1')


if __name__ == '__main__':
    unittest.main()
