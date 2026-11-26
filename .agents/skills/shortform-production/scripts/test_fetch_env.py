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
    ADC_REQUIRED_SCOPE,
    DOPPLER_DOWNLOAD_URL,
    decode_adc_payload,
    fetch_doppler_env,
    main,
    parse_env_items,
    parse_env_keys,
    run_checks,
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


class _FakeProc:
    def __init__(self, returncode: int = 0, stdout: str = '', stderr: str = ''):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


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
        self.assertTrue((self.root / '.env').exists())

    def test_main_restores_colab_adc_b64_with_0600_and_never_leaks_secret(self):
        adc_obj = {
            'type': 'authorized_user',
            'client_id': 'client-123.apps.googleusercontent.com',
            'client_secret': 'SUPER_SECRET_CLIENT',
            'refresh_token': 'SUPER_SECRET_REFRESH_TOKEN',
        }
        adc_b64 = base64.b64encode(json.dumps(adc_obj).encode('utf-8')).decode('ascii')
        payload = (
            'TRYPOST_BASE_URL="https://trypost.example.test"\n'
            'TRYPOST_API_KEY="tp_key"\n'
            'ELEVENLABS_API_KEY="el_key"\n'
            'ELEVENLABS_VOICE_ID="voice_abc"\n'
            f'GOOGLE_COLAB_ADC_JSON_B64="{adc_b64}"\n'
        )
        adc_dest = self.root / 'gcloud' / 'application_default_credentials.json'
        stdout = io.StringIO()
        with (
            patch('fetch_env.urllib.request.urlopen', return_value=_FakeResponse(payload)),
            patch.dict(os.environ, {'DOPPLER_TOKEN': 'dp.st.prd.token'}, clear=False),
            patch('sys.stdout', stdout),
        ):
            code = main(['--root', str(self.root), '--adc-path', str(adc_dest), '--json'])

        self.assertEqual(code, 0)
        out = stdout.getvalue()
        self.assertNotIn('SUPER_SECRET_REFRESH_TOKEN', out)
        self.assertNotIn('SUPER_SECRET_CLIENT', out)
        self.assertNotIn(adc_b64, out)
        parsed = json.loads(out)
        self.assertTrue(parsed['ok'])
        self.assertTrue(parsed['adc_restored'])
        self.assertEqual(parsed['adc_path'], str(adc_dest.resolve()))
        self.assertTrue(adc_dest.exists())
        self.assertEqual(json.loads(adc_dest.read_text(encoding='utf-8')), adc_obj)
        if os.name == 'posix':
            self.assertEqual(stat.S_IMODE(adc_dest.stat().st_mode), 0o600)

    def test_decode_adc_payload_raw_and_validation_errors(self):
        raw_items = parse_env_items(
            'GOOGLE_COLAB_ADC_JSON=\'{"type":"authorized_user","refresh_token":"rt_123"}\'\n'
        )
        decoded = decode_adc_payload(raw_items)
        self.assertIsNotNone(decoded)
        self.assertEqual(json.loads(decoded)['type'], 'authorized_user')

        with self.assertRaises(ValueError) as ctx:
            decode_adc_payload({'GOOGLE_COLAB_ADC_JSON_B64': 'not!!valid!!b64_SECRET_LEAK'})
        self.assertNotIn('SECRET_LEAK', str(ctx.exception))

        bad_json_b64 = base64.b64encode(b'{"missing_type": "SECRET_VAL"}').decode('ascii')
        with self.assertRaises(ValueError) as ctx2:
            decode_adc_payload({'GOOGLE_COLAB_ADC_JSON_B64': bad_json_b64})
        self.assertNotIn('SECRET_VAL', str(ctx2.exception))

    def test_run_checks_verifies_colab_adc_scope(self):
        adc_path = self.root / 'adc.json'
        adc_path.write_text('{"type": "authorized_user"}\n', encoding='utf-8')
        seen_cmds = []

        def fake_run(cmd, **kwargs):
            seen_cmds.append((cmd, kwargs.get('env', {}).get('GOOGLE_APPLICATION_CREDENTIALS')))
            return _FakeProc(0, stdout=f'email: user@example.com\nscopes: openid {ADC_REQUIRED_SCOPE}\n')

        with (
            patch('fetch_env.find_colab_binary', return_value='/usr/local/bin/colab'),
            patch('fetch_env.subprocess.run', side_effect=fake_run),
        ):
            results = run_checks(self.root, {'GOOGLE_COLAB_ADC_JSON_B64'}, adc_path=adc_path)

        self.assertEqual(results['colab_adc'], 'ok')
        self.assertEqual(seen_cmds[0][0], ['/usr/local/bin/colab', '--auth=adc', 'whoami'])
        self.assertEqual(seen_cmds[0][1], str(adc_path))

        def fake_missing_scope(cmd, **kwargs):
            return _FakeProc(0, stdout='email: user@example.com\nscopes: openid cloud-platform\n')

        with (
            patch('fetch_env.find_colab_binary', return_value='/usr/local/bin/colab'),
            patch('fetch_env.subprocess.run', side_effect=fake_missing_scope),
        ):
            results_bad = run_checks(self.root, {'GOOGLE_COLAB_ADC_JSON_B64'}, adc_path=adc_path)
        self.assertTrue(results_bad['colab_adc'].startswith('failed:'))
        self.assertIn('colaboratory', results_bad['colab_adc'])


if __name__ == '__main__':
    unittest.main()
