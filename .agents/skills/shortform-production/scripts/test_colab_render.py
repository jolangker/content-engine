"""Offline unit tests for colab_render.py Google Colab offload wrapper; no network calls."""
import io
import json
import os
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch

from colab_render import (
    REMOTE_ARCHIVE_PATH,
    REMOTE_LOG_PATH,
    REMOTE_PROJECT_DIR,
    REQUIRED_COLAB_SCOPE,
    build_remote_runner_script,
    main,
    offload_render,
    pack_project_tarball,
    resolve_remote_output,
)


class _FakeProc:
    def __init__(self, returncode: int = 0, stdout: str = '', stderr: str = ''):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class ColabRenderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / 'video'
        self.project.mkdir()
        (self.project / 'index.html').write_text('<!doctype html><html></html>\n', encoding='utf-8')
        (self.project / 'assets').mkdir()
        (self.project / 'assets' / 'voice.mp3').write_bytes(b'ID3-audio')
        (self.project / 'node_modules').mkdir()
        (self.project / 'node_modules' / 'junk.js').write_text('ignored\n', encoding='utf-8')
        (self.project / '.git').mkdir()
        (self.project / '.git' / 'HEAD').write_text('ref: refs/heads/main\n', encoding='utf-8')
        (self.project / '.hyperframes').mkdir()
        (self.project / '.hyperframes' / 'cache.bin').write_bytes(b'cache')
        (self.project / 'verification').mkdir()
        (self.project / 'verification' / 'old.mp4').write_bytes(b'old-video')
        (self.project / '.env').write_text('ELEVENLABS_API_KEY=secret\n', encoding='utf-8')
        (self.project / '.DS_Store').write_bytes(b'mac')

        self.adc_file = self.root / 'adc.json'
        self.adc_file.write_text(
            json.dumps({'type': 'authorized_user', 'client_id': 'cid', 'refresh_token': 'rt'}),
            encoding='utf-8',
        )

    def test_pack_project_tarball_excludes_heavy_and_secret_paths(self):
        dest = self.root / 'project.tar.gz'
        count, size = pack_project_tarball(self.project, dest, extra_excludes=('*.bak',))
        self.assertEqual(count, 2)
        self.assertGreater(size, 0)
        with tarfile.open(dest, 'r:gz') as tf:
            names = sorted(tf.getnames())
        self.assertEqual(names, ['assets/voice.mp3', 'index.html'])

    def test_build_remote_runner_script_compiles_cleanly(self):
        script_default = build_remote_runner_script(
            remote_archive=REMOTE_ARCHIVE_PATH,
            remote_project_dir=REMOTE_PROJECT_DIR,
            remote_output_rel='colab-out/proof.mp4',
            remote_log_path=REMOTE_LOG_PATH,
            quality='draft',
            fps='30',
            resolution='portrait',
            extra_args=('--strict',),
        )
        compile(script_default, '<remote-default>', 'exec')
        self.assertIn('h264_nvenc', script_default)
        self.assertIn('--browser-gpu', script_default)

        script_custom = build_remote_runner_script(
            remote_archive=REMOTE_ARCHIVE_PATH,
            remote_project_dir=REMOTE_PROJECT_DIR,
            remote_output_rel='out/final.mp4',
            remote_log_path=REMOTE_LOG_PATH,
            quality='delivery',
            render_cmd='npx hyperframes render --quality delivery -o out/final.mp4 --gpu',
        )
        compile(script_custom, '<remote-custom>', 'exec')

    def test_resolve_remote_output_rejects_traversal(self):
        self.assertEqual(resolve_remote_output(Path('/tmp/exports/v1.mp4'), None), 'colab-out/v1.mp4')
        self.assertEqual(resolve_remote_output(Path('/tmp/v1.mp4'), 'verification/proof.mp4'), 'verification/proof.mp4')
        with self.assertRaises(ValueError):
            resolve_remote_output(Path('/tmp/v1.mp4'), '../outside.mp4')

    def test_offload_render_happy_path_and_global_auth_flag_order(self):
        calls = []
        local_out = self.root / 'exports' / 'episode.mp4'

        def fake_run(cmd, **kwargs):
            calls.append(cmd)
            if cmd[1:] == ['--help']:
                return _FakeProc(0, stdout='Usage: colab')
            if 'download' in cmd:
                Path(cmd[-1]).write_bytes(b'\x00\x00\x00\x18ftypmp42fakevideo')
                return _FakeProc(0)
            return _FakeProc(0, stdout='ok\n')

        with (
            patch.dict(os.environ, {'GOOGLE_APPLICATION_CREDENTIALS': str(self.adc_file)}, clear=False),
            patch('colab_render.find_colab_binary', return_value='/usr/bin/colab'),
            patch('colab_render.probe_duration_seconds', return_value=42.5),
            patch('colab_render.subprocess.run', side_effect=fake_run),
        ):
            result = offload_render(
                project_dir=self.project,
                local_output=local_out,
                quality='delivery',
            )

        self.assertTrue(result['ok'])
        self.assertEqual(result['gpu'], 'L4')
        self.assertTrue(result['session_stopped'])
        self.assertEqual(result['duration_seconds'], 42.5)
        self.assertGreater(result['output_bytes'], 0)

        # Every non-help colab call must place --auth=adc immediately after binary.
        subcommands = [c[2] for c in calls if c[1:] != ['--help']]
        self.assertEqual(subcommands, ['new', 'upload', 'exec', 'download', 'stop'])
        for c in calls:
            if c[1:] != ['--help']:
                self.assertEqual(c[1], '--auth=adc')

    def test_offload_render_falls_back_from_l4_to_t4(self):
        calls = []
        local_out = self.root / 'verification' / 'proof.mp4'

        def fake_run(cmd, **kwargs):
            calls.append(cmd)
            if cmd[1:] == ['--help']:
                return _FakeProc(0)
            if 'new' in cmd and '--gpu' in cmd and 'L4' in cmd:
                return _FakeProc(1, stderr='400 L4 quota unavailable')
            if 'download' in cmd:
                Path(cmd[-1]).write_bytes(b'mp4data')
                return _FakeProc(0)
            return _FakeProc(0)

        with (
            patch.dict(os.environ, {'GOOGLE_APPLICATION_CREDENTIALS': str(self.adc_file)}, clear=False),
            patch('colab_render.find_colab_binary', return_value='/usr/bin/colab'),
            patch('colab_render.probe_duration_seconds', return_value=None),
            patch('colab_render.subprocess.run', side_effect=fake_run),
            patch('sys.stderr', io.StringIO()),
        ):
            result = offload_render(project_dir=self.project, local_output=local_out, quality='draft')

        self.assertEqual(result['gpu'], 'T4')
        new_calls = [c for c in calls if len(c) > 2 and c[2] == 'new']
        self.assertEqual(len(new_calls), 2)
        self.assertIn('L4', new_calls[0])
        self.assertIn('T4', new_calls[1])
        self.assertEqual(calls[-1][2], 'stop')

    def test_render_failure_fetches_last_50_log_lines_before_teardown(self):
        events = []
        local_out = self.root / 'out.mp4'

        def fake_run(cmd, **kwargs):
            if cmd[1:] == ['--help']:
                return _FakeProc(0)
            sub = cmd[2]
            if sub == 'exec' and '-f' in cmd:
                events.append('render_exec_fail')
                return _FakeProc(1, stderr='Chromium crashed')
            if sub == 'exec' and kwargs.get('input'):
                events.append('fetch_tail_log')
                self.assertIn('[-50:]', kwargs['input'])
                return _FakeProc(0, stdout='LINE49: WebGL context lost\nLINE50: exit 1\n')
            events.append(sub)
            return _FakeProc(0)

        with (
            patch.dict(os.environ, {'GOOGLE_APPLICATION_CREDENTIALS': str(self.adc_file)}, clear=False),
            patch('colab_render.find_colab_binary', return_value='/usr/bin/colab'),
            patch('colab_render.subprocess.run', side_effect=fake_run),
        ):
            with self.assertRaises(RuntimeError) as ctx:
                offload_render(project_dir=self.project, local_output=local_out)

        self.assertEqual(events, ['new', 'upload', 'render_exec_fail', 'fetch_tail_log', 'stop'])
        self.assertIn('Last 50 lines of /content/render.log', str(ctx.exception))
        self.assertIn('WebGL context lost', str(ctx.exception))

    def test_zero_byte_download_fails_and_still_stops_session(self):
        events = []
        local_out = self.root / 'empty.mp4'

        def fake_run(cmd, **kwargs):
            if cmd[1:] == ['--help']:
                return _FakeProc(0)
            events.append(cmd[2])
            if cmd[2] == 'download':
                Path(cmd[-1]).write_bytes(b'')
            return _FakeProc(0)

        with (
            patch.dict(os.environ, {'GOOGLE_APPLICATION_CREDENTIALS': str(self.adc_file)}, clear=False),
            patch('colab_render.find_colab_binary', return_value='/usr/bin/colab'),
            patch('colab_render.subprocess.run', side_effect=fake_run),
        ):
            with self.assertRaises(RuntimeError) as ctx:
                offload_render(project_dir=self.project, local_output=local_out)

        self.assertIn('zero bytes', str(ctx.exception))
        self.assertEqual(events, ['new', 'upload', 'exec', 'download', 'stop'])

    def test_missing_adc_fails_before_provisioning_any_vm(self):
        missing_adc = self.root / 'nonexistent_adc.json'
        calls = []

        def fake_run(cmd, **kwargs):
            calls.append(cmd)
            return _FakeProc(0)

        with (
            patch.dict(os.environ, {'GOOGLE_APPLICATION_CREDENTIALS': str(missing_adc)}, clear=False),
            patch('colab_render.find_colab_binary', return_value='/usr/bin/colab'),
            patch('colab_render.subprocess.run', side_effect=fake_run),
        ):
            with self.assertRaises(RuntimeError) as ctx:
                offload_render(project_dir=self.project, local_output=self.root / 'out.mp4')

        self.assertIn('Google ADC credentials file not found', str(ctx.exception))
        self.assertEqual(calls, [['/usr/bin/colab', '--help']])

    def test_cli_check_and_dry_run_modes(self):
        stdout_check = io.StringIO()

        def fake_check_run(cmd, **kwargs):
            if cmd[1:] == ['--help']:
                return _FakeProc(0)
            if len(cmd) > 2 and cmd[2] == 'whoami':
                return _FakeProc(0, stdout=f'email: ok@example.com\nscopes: openid {REQUIRED_COLAB_SCOPE}\n')
            raise AssertionError(f'Unexpected command: {cmd}')

        with (
            patch.dict(os.environ, {'GOOGLE_APPLICATION_CREDENTIALS': str(self.adc_file)}, clear=False),
            patch('colab_render.find_colab_binary', return_value='/usr/bin/colab'),
            patch('colab_render.subprocess.run', side_effect=fake_check_run),
            patch('sys.stdout', stdout_check),
        ):
            rc = main(['--check', '--json'])
        self.assertEqual(rc, 0)
        parsed_check = json.loads(stdout_check.getvalue())
        self.assertTrue(parsed_check['ok'])
        self.assertEqual(parsed_check['whoami'], 'ok')

        stdout_dry = io.StringIO()
        with (
            patch('colab_render.find_colab_binary', return_value='/usr/bin/colab'),
            patch('colab_render.subprocess.run', return_value=_FakeProc(0)),
            patch('sys.stdout', stdout_dry),
        ):
            rc_dry = main([
                '--project',
                str(self.project),
                '--output',
                str(self.root / 'exports' / 'demo.mp4'),
                '--quality',
                'draft',
                '--dry-run',
                '--json',
            ])
        self.assertEqual(rc_dry, 0)
        parsed_dry = json.loads(stdout_dry.getvalue())
        self.assertTrue(parsed_dry['dry_run'])
        self.assertEqual(parsed_dry['packed_files'], 2)
        self.assertEqual(parsed_dry['remote_output'], '/content/project/colab-out/demo.mp4')


if __name__ == '__main__':
    unittest.main()
