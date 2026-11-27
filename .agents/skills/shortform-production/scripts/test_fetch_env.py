"""Offline unit tests for fetch_env.py Doppler secret fetcher; no network calls."""
import base64
import io
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

from fetch_env import (
    DOPPLER_DOWNLOAD_URL,
    fetch_doppler_env,
    main,
    parse_env_keys,
    write_env_atomic,
)


class _FakeResponse:
    def __init__(self, body: str, status: int = 200):
        self._raw = body.encode('utf-8')
        self.status = status

    def read(self) -> bytes:
        return self._raw

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class FetchEnvTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_fetch_doppler_env_service_token_headers_and_url(self):
        captured = {}

        def fake_urlopen(req, timeout=30):
            captured['url'] = req.full_url
            captured['auth'] = req.get_header('Authorization')
            return _FakeResponse('ELEVENLABS_API_KEY="sk_test_123"\nTRYPOST_API_KEY="tp_456"')

        with patch('fetch_env.urllib.request.urlopen', side_effect=fake_urlopen):
            content = fetch_doppler_env('dp.st.prd.secret123')

        self.assertEqual(captured['url'], f'{DOPPLER_DOWNLOAD_URL}?format=env')
        expected_auth = 'Basic ' + base64.b64encode(b'dp.st.prd.secret123:').decode('ascii')
        self.assertEqual(captured['auth'], expected_auth)
        self.assertTrue(content.endswith('\n'))
        self.assertEqual(parse_env_keys(content), ['ELEVENLABS_API_KEY', 'TRYPOST_API_KEY'])

    def test_fetch_doppler_env_with_project_and_config(self):
        captured = {}

        def fake_urlopen(req, timeout=30):
            captured['url'] = req.full_url
            return _FakeResponse('TRYPOST_BASE_URL="https://trypost.example.test"\n')

        with patch('fetch_env.urllib.request.urlopen', side_effect=fake_urlopen):
            fetch_doppler_env('dp.pt.personal', project='content-engine', config='prd')

        self.assertIn('format=env', captured['url'])
        self.assertIn('project=content-engine', captured['url'])
        self.assertIn('config=prd', captured['url'])

    def test_fetch_doppler_env_rejects_partial_project_config(self):
        with self.assertRaises(ValueError):
            fetch_doppler_env('dp.pt.personal', project='content-engine')
        with self.assertRaises(ValueError):
            fetch_doppler_env('dp.pt.personal', config='prd')

    def test_fetch_doppler_env_http_error_never_leaks_token(self):
        err_body = io.BytesIO(json.dumps({'messages': ['Invalid token']}).encode('utf-8'))
        http_err = urllib.error.HTTPError(DOPPLER_DOWNLOAD_URL, 401, 'Unauthorized', {}, err_body)
        with patch('fetch_env.urllib.request.urlopen', side_effect=http_err):
            with self.assertRaises(RuntimeError) as ctx:
                fetch_doppler_env('dp.st.prd.supersecretvalue')
        self.assertIn('HTTP 401', str(ctx.exception))
        self.assertIn('Invalid token', str(ctx.exception))
        self.assertNotIn('supersecretvalue', str(ctx.exception))

    def test_write_env_atomic_sets_0600_permissions(self):
        target = write_env_atomic(self.root, 'ELEVENLABS_API_KEY="sk_1"\n')
        self.assertEqual(target, self.root / '.env')
        self.assertEqual(target.read_text(encoding='utf-8'), 'ELEVENLABS_API_KEY="sk_1"\n')
        if os.name == 'posix':
            mode = stat.S_IMODE(target.stat().st_mode)
            self.assertEqual(mode, 0o600)

    def test_main_writes_env_and_never_prints_secret_values(self):
        payload = (
            'TRYPOST_BASE_URL="https://trypost.example.test"\n'
            'TRYPOST_API_KEY="SUPER_SECRET_TRYPOST"\n'
            'ELEVENLABS_API_KEY="SUPER_SECRET_ELEVEN"\n'
            'ELEVENLABS_VOICE_ID="voice_abc"\n'
        )
        stdout = io.StringIO()
        with (
            patch('fetch_env.urllib.request.urlopen', return_value=_FakeResponse(payload)),
            patch.dict(os.environ, {'DOPPLER_TOKEN': 'dp.st.prd.token'}, clear=False),
            patch('sys.stdout', stdout),
        ):
            code = main(['--root', str(self.root), '--json'])

        self.assertEqual(code, 0)
        out = stdout.getvalue()
        self.assertNotIn('SUPER_SECRET_TRYPOST', out)
        self.assertNotIn('SUPER_SECRET_ELEVEN', out)
        self.assertNotIn('dp.st.prd.token', out)
        parsed = json.loads(out)
        self.assertTrue(parsed['ok'])
        self.assertEqual(parsed['key_count'], 4)
        self.assertEqual(parsed['expected_missing'], [])
        self.assertEqual(parsed['optional_gdrive_present'], [])
        self.assertEqual(len(parsed['optional_gdrive_missing']), 4)
        self.assertTrue((self.root / '.env').exists())

    def test_run_checks_invokes_gdrive_only_when_all_keys_present(self):
        from fetch_env import OPTIONAL_GDRIVE_KEYS, run_checks

        class _Proc:
            returncode = 0
            stdout = '{"status": "ok"}'
            stderr = ''

        with patch('fetch_env.subprocess.run', return_value=_Proc()) as mock_run:
            skipped = run_checks(self.root, {'GOOGLE_CLIENT_ID'})
            self.assertIn('skipped', skipped['gdrive'])
            mock_run.assert_not_called()

            checked = run_checks(self.root, set(OPTIONAL_GDRIVE_KEYS))
            self.assertEqual(checked['gdrive'], 'ok')
            self.assertEqual(mock_run.call_count, 1)
            cmd = mock_run.call_args[0][0]
            self.assertTrue(cmd[1].endswith('gdrive.py'))
            self.assertEqual(cmd[-1], 'check')


if __name__ == '__main__':
    unittest.main()
