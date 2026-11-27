"""Offline unit tests for env_loader.py (Doppler REST API primary -> per-key .env fallback)."""
import base64
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

import env_loader


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


class EnvLoaderTests(unittest.TestCase):
    def setUp(self):
        env_loader.clear_cache()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def tearDown(self):
        env_loader.clear_cache()

    def test_dotenv_fallback_when_no_doppler_token(self):
        (self.root / '.env').write_text(
            'export TRYPOST_API_KEY="local-key"\n'
            'ELEVENLABS_VOICE_ID=local-voice # inline comment\n',
            encoding='utf-8',
        )
        with patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'shell-ignored', 'DOPPLER_TOKEN': ''}, clear=False):
            values, meta = env_loader.load_env(self.root)

        self.assertEqual(values, {'TRYPOST_API_KEY': 'local-key', 'ELEVENLABS_VOICE_ID': 'local-voice'})
        self.assertNotIn('ELEVENLABS_API_KEY', values)
        self.assertEqual(meta['source'], 'dotenv')
        self.assertFalse(meta['doppler_ok'])
        self.assertTrue(meta['dotenv_loaded'])
        self.assertIsNone(meta['doppler_error'])

    def test_doppler_primary_with_per_key_dotenv_layering(self):
        (self.root / '.env').write_text(
            'TRYPOST_API_KEY="local-old"\n'
            'GOOGLE_DRIVE_ROOT_FOLDER_ID="local-only-folder"\n',
            encoding='utf-8',
        )
        captured = {}

        def fake_open(req, timeout=15):
            captured['url'] = req.full_url
            captured['auth'] = req.get_header('Authorization')
            return _FakeResponse({
                'TRYPOST_API_KEY': 'doppler-live-key',
                'ELEVENLABS_API_KEY': 'doppler-el-key',
            })

        with patch.dict(os.environ, {'DOPPLER_TOKEN': 'dp.st.prd.token123', 'TRYPOST_API_KEY': 'shell-ignored'}, clear=False):
            values, meta = env_loader.load_env(self.root, opener=fake_open)

        self.assertEqual(captured['url'], f'{env_loader.DOPPLER_DOWNLOAD_URL}?format=json')
        expected_auth = 'Basic ' + base64.b64encode(b'dp.st.prd.token123:').decode('ascii')
        self.assertEqual(captured['auth'], expected_auth)
        self.assertEqual(values['TRYPOST_API_KEY'], 'doppler-live-key')
        self.assertEqual(values['ELEVENLABS_API_KEY'], 'doppler-el-key')
        self.assertEqual(values['GOOGLE_DRIVE_ROOT_FOLDER_ID'], 'local-only-folder')
        self.assertEqual(meta['source'], 'doppler+dotenv')
        self.assertTrue(meta['doppler_ok'])

    def test_doppler_forwards_project_and_config_when_both_set(self):
        captured = {}

        def fake_open(req, timeout=15):
            captured['url'] = req.full_url
            return _FakeResponse({'ELEVENLABS_API_KEY': 'sk-1'})

        with patch.dict(
            os.environ,
            {
                'DOPPLER_TOKEN': 'dp.pt.personal',
                'DOPPLER_PROJECT': 'content-engine',
                'DOPPLER_CONFIG': 'prd',
            },
            clear=False,
        ):
            values, meta = env_loader.load_env(self.root, opener=fake_open)

        self.assertIn('format=json', captured['url'])
        self.assertIn('project=content-engine', captured['url'])
        self.assertIn('config=prd', captured['url'])
        self.assertEqual(values['ELEVENLABS_API_KEY'], 'sk-1')
        self.assertEqual(meta['source'], 'doppler')
        self.assertFalse(meta['dotenv_loaded'])

    def test_doppler_failure_falls_back_gracefully_to_dotenv_without_leaking_token(self):
        (self.root / '.env').write_text('TRYPOST_API_KEY="fallback-local"\n', encoding='utf-8')
        err_body = io.BytesIO(json.dumps({'messages': ['Invalid token']}).encode('utf-8'))
        http_err = urllib.error.HTTPError(env_loader.DOPPLER_DOWNLOAD_URL, 401, 'Unauthorized', {}, err_body)

        def fake_open(req, timeout=15):
            raise http_err

        with patch.dict(os.environ, {'DOPPLER_TOKEN': 'dp.st.prd.supersecret'}, clear=False):
            values, meta = env_loader.load_env(self.root, opener=fake_open)

        self.assertEqual(values['TRYPOST_API_KEY'], 'fallback-local')
        self.assertEqual(meta['source'], 'dotenv')
        self.assertFalse(meta['doppler_ok'])
        self.assertIn('HTTP 401', meta['doppler_error'])
        self.assertNotIn('supersecret', meta['doppler_error'])

    def test_doppler_token_can_bootstrap_from_dotenv(self):
        (self.root / '.env').write_text('DOPPLER_TOKEN="dp.st.prd.fromdotenv"\n', encoding='utf-8')

        def fake_open(req, timeout=15):
            return _FakeResponse({'TRYPOST_API_KEY': 'from-doppler'})

        with patch.dict(os.environ, {'DOPPLER_TOKEN': ''}, clear=False):
            values, meta = env_loader.load_env(self.root, opener=fake_open)

        self.assertEqual(values['TRYPOST_API_KEY'], 'from-doppler')
        self.assertTrue(meta['doppler_ok'])

    def test_in_memory_cache_avoids_repeat_requests(self):
        calls = 0

        def fake_open(req, timeout=15):
            nonlocal calls
            calls += 1
            return _FakeResponse({'TRYPOST_API_KEY': 'cached-key'})

        with (
            patch.dict(os.environ, {'DOPPLER_TOKEN': 'dp.st.prd.cachetest'}, clear=False),
            patch('env_loader.urllib.request.urlopen', side_effect=fake_open),
        ):
            v1 = env_loader.read_env(self.root)
            v2 = env_loader.read_env(self.root)

        self.assertEqual(calls, 1)
        self.assertEqual(v1['TRYPOST_API_KEY'], 'cached-key')
        self.assertEqual(v2['TRYPOST_API_KEY'], 'cached-key')

    def test_unclosed_quote_in_dotenv_raises_value_error(self):
        (self.root / '.env').write_text('TRYPOST_API_KEY="unclosed\n', encoding='utf-8')
        with self.assertRaises(ValueError):
            env_loader.read_dotenv(self.root)


if __name__ == '__main__':
    unittest.main()
