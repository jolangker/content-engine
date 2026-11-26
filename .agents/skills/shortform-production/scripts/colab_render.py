#!/usr/bin/env python3
"""Offload HyperFrames video rendering to a Google Colab GPU instance via google-colab-cli.

Never runs HyperFrames rendering locally. Packages only necessary project files,
provisions an L4 GPU runtime (with T4 fallback) using --auth=adc, installs dependencies
and runs the render remotely with GPU/NVENC when available, downloads and verifies a
non-zero output file, fetches the last 50 log lines on failure before teardown, and
always terminates the Colab session in a cleanup guard.

Uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
from pathlib import Path
import shlex
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
from typing import Sequence

DEFAULT_SESSION = 'hyperframes-render'
DEFAULT_GPU = 'L4'
DEFAULT_FALLBACK_GPU = 'T4'
DEFAULT_AUTH = 'adc'
DEFAULT_QUALITY = 'delivery'
DEFAULT_LOG_LINES = 50
REMOTE_ARCHIVE_PATH = '/content/project.tar.gz'
REMOTE_PROJECT_DIR = '/content/project'
REMOTE_LOG_PATH = '/content/render.log'
REQUIRED_COLAB_SCOPE = 'https://www.googleapis.com/auth/colaboratory'

DEFAULT_EXCLUDED_DIRS = frozenset({
    'node_modules',
    '.git',
    '.hyperframes',
    '__pycache__',
    '.cache',
    '.venv',
    'venv',
    'colab-out',
    'verification',
    'exports',
    'renders',
})

DEFAULT_EXCLUDED_FILE_PATTERNS = (
    '.DS_Store',
    '.env',
    '.env.*',
    '*.pyc',
    '*.pyo',
    '*.tmp',
)

ADC_SETUP_HINT = (
    'gcloud auth application-default login '
    '--scopes=openid,https://www.googleapis.com/auth/cloud-platform,'
    'https://www.googleapis.com/auth/userinfo.email,'
    'https://www.googleapis.com/auth/colaboratory'
)


def find_colab_binary() -> str | None:
    """Locate the google-colab-cli executable on PATH or in ~/.local/bin."""
    found = shutil.which('colab')
    if found:
        return found
    candidate = Path.home() / '.local' / 'bin' / 'colab'
    if candidate.is_file() and os.access(candidate, os.X_OK):
        return str(candidate)
    return None


def ensure_colab_cli(*, auto_install: bool = False) -> str:
    """Verify google-colab-cli is installed and answers --help (installing if requested)."""
    colab_bin = find_colab_binary()
    if not colab_bin and auto_install:
        uv_bin = shutil.which('uv')
        install_cmd = (
            [uv_bin, 'tool', 'install', 'google-colab-cli']
            if uv_bin
            else [sys.executable, '-m', 'pip', 'install', '--no-input', 'google-colab-cli']
        )
        proc = subprocess.run(install_cmd, capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout).strip()
            raise RuntimeError(f'Failed to install google-colab-cli: {detail}')
        colab_bin = find_colab_binary()

    if not colab_bin:
        raise RuntimeError(
            'google-colab-cli (colab) is not installed. '
            'Install it via `uv tool install google-colab-cli` or `pip install google-colab-cli` '
            '(or pass --auto-install).'
        )

    probe = subprocess.run([colab_bin, '--help'], capture_output=True, text=True, check=False)
    if probe.returncode != 0:
        detail = (probe.stderr or probe.stdout).strip()
        raise RuntimeError(f'`colab --help` failed (exit {probe.returncode}): {detail}')
    return colab_bin


def resolve_adc_path() -> Path:
    configured = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '').strip()
    if configured:
        return Path(configured).expanduser()
    return Path.home() / '.config' / 'gcloud' / 'application_default_credentials.json'


def validate_adc_file() -> Path:
    """Ensure local Application Default Credentials JSON exists and parses cleanly."""
    adc_path = resolve_adc_path()
    if not adc_path.is_file() or adc_path.stat().st_size == 0:
        raise RuntimeError(
            f'Google ADC credentials file not found at {adc_path}. '
            f'Mint ADC locally with `{ADC_SETUP_HINT}` or restore GOOGLE_COLAB_ADC_JSON_B64 '
            'via `fetch_env.py`.'
        )
    try:
        parsed = json.loads(adc_path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f'Google ADC credentials file at {adc_path} is unreadable or invalid JSON: {exc}') from None
    if not isinstance(parsed, dict) or not parsed.get('type'):
        raise RuntimeError(f'Google ADC credentials file at {adc_path} must be a JSON object with a "type" field.')
    return adc_path


def check_prerequisites(*, auth: str = DEFAULT_AUTH, auto_install: bool = False) -> dict[str, object]:
    """Run non-destructive readiness checks (colab CLI, ADC file, whoami scopes)."""
    colab_bin = ensure_colab_cli(auto_install=auto_install)
    report: dict[str, object] = {
        'ok': True,
        'colab_bin': colab_bin,
        'auth': auth,
    }
    if auth == 'adc':
        adc_path = validate_adc_file()
        report['adc_path'] = str(adc_path)

    proc = subprocess.run(
        [colab_bin, f'--auth={auth}', 'whoami'],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        report['ok'] = False
        report['whoami'] = f'failed: {detail}'
        return report

    whoami_out = proc.stdout.strip()
    has_scope = REQUIRED_COLAB_SCOPE in whoami_out
    report['whoami'] = 'ok' if has_scope else f'missing required scope {REQUIRED_COLAB_SCOPE}'
    if not has_scope:
        report['ok'] = False
    return report


def _should_exclude(rel_path: Path, extra_excludes: Sequence[str]) -> bool:
    parts = rel_path.parts
    if any(part in DEFAULT_EXCLUDED_DIRS for part in parts[:-1]):
        return True
    name = rel_path.name
    if name in DEFAULT_EXCLUDED_DIRS and len(parts) >= 1:
        return True
    rel_posix = rel_path.as_posix()
    for pattern in (*DEFAULT_EXCLUDED_FILE_PATTERNS, *extra_excludes):
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel_posix, pattern):
            return True
        if any(fnmatch.fnmatch(part, pattern) for part in parts):
            return True
    return False


def pack_project_tarball(
    project_dir: Path,
    dest_tar: Path,
    *,
    extra_excludes: Sequence[str] = (),
) -> tuple[int, int]:
    """Create a filtered .tar.gz archive of project_dir excluding caches and node_modules."""
    if not project_dir.is_dir():
        raise ValueError(f'Project directory does not exist: {project_dir}')

    file_count = 0
    with tarfile.open(dest_tar, mode='w:gz') as archive:
        for root_str, dirnames, filenames in os.walk(project_dir):
            root_path = Path(root_str)
            rel_root = root_path.relative_to(project_dir)

            # Prune excluded directories in-place so os.walk skips them completely.
            kept_dirs: list[str] = []
            for dname in sorted(dirnames):
                rel_dir = rel_root / dname if rel_root != Path('.') else Path(dname)
                if not _should_exclude(rel_dir, extra_excludes):
                    kept_dirs.append(dname)
            dirnames[:] = kept_dirs

            for fname in sorted(filenames):
                rel_file = rel_root / fname if rel_root != Path('.') else Path(fname)
                if _should_exclude(rel_file, extra_excludes):
                    continue
                full_path = root_path / fname
                if not full_path.is_file():
                    continue
                archive.add(full_path, arcname=rel_file.as_posix())
                file_count += 1

    if file_count == 0:
        raise RuntimeError(f'No files left to upload from {project_dir} after applying exclusions.')
    return file_count, dest_tar.stat().st_size


def resolve_remote_output(local_output: Path, remote_output: str | None) -> str:
    """Return a clean relative output path under /content/project."""
    if remote_output:
        clean = remote_output.strip().lstrip('/')
        if '..' in Path(clean).parts or not clean:
            raise ValueError(f'Invalid --remote-output path: {remote_output!r}')
        return Path(clean).as_posix()
    return f'colab-out/{local_output.name}'


def build_remote_runner_script(
    *,
    remote_archive: str,
    remote_project_dir: str,
    remote_output_rel: str,
    remote_log_path: str,
    quality: str,
    fps: str | None = None,
    resolution: str | None = None,
    fmt: str | None = None,
    extra_args: Sequence[str] = (),
    render_cmd: str | None = None,
    enable_gpu_flags: bool = True,
) -> str:
    """Build the self-contained Python script executed on the Colab GPU runtime."""
    config = {
        'remote_archive': remote_archive,
        'remote_project_dir': remote_project_dir,
        'remote_output_rel': remote_output_rel,
        'remote_log_path': remote_log_path,
        'quality': quality,
        'fps': fps,
        'resolution': resolution,
        'fmt': fmt,
        'extra_args': list(extra_args),
        'render_cmd': render_cmd,
        'enable_gpu_flags': enable_gpu_flags,
    }
    config_json = json.dumps(config, indent=2)
    return f'''import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tarfile

CONFIG = json.loads({config_json!r})
LOG_PATH = Path(CONFIG['remote_log_path'])
PROJECT_DIR = Path(CONFIG['remote_project_dir'])
ARCHIVE_PATH = Path(CONFIG['remote_archive'])
OUTPUT_PATH = PROJECT_DIR / CONFIG['remote_output_rel']
SUDO = [] if os.geteuid() == 0 else ['sudo']


def log_line(msg, log_handle):
    line = msg if msg.endswith('\\n') else msg + '\\n'
    sys.stdout.write(line)
    sys.stdout.flush()
    log_handle.write(line)
    log_handle.flush()


def run_step(cmd, log_handle, *, cwd=None, check=True, shell=False):
    label = cmd if isinstance(cmd, str) else ' '.join(shlex.quote(str(c)) for c in cmd)
    log_line(f'[colab-render] $ {{label}}', log_handle)
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd) if cwd else None,
        shell=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    assert proc.stdout is not None
    for out_line in proc.stdout:
        sys.stdout.write(out_line)
        sys.stdout.flush()
        log_handle.write(out_line)
        log_handle.flush()
    rc = proc.wait()
    if check and rc != 0:
        log_line(f'[colab-render] Command exited with code {{rc}}: {{label}}', log_handle)
        raise SystemExit(rc)
    return rc


def node_major_version():
    if not shutil.which('node'):
        return 0
    proc = subprocess.run(['node', '-v'], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return 0
    raw = proc.stdout.strip().lstrip('v').split('.', 1)[0]
    try:
        return int(raw)
    except ValueError:
        return 0


def detect_gpu_and_nvenc(log_handle):
    has_gpu = False
    has_nvenc = False
    if shutil.which('nvidia-smi'):
        gpu_proc = subprocess.run(
            ['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader'],
            capture_output=True,
            text=True,
            check=False,
        )
        if gpu_proc.returncode == 0 and gpu_proc.stdout.strip():
            has_gpu = True
            log_line(f'[colab-render] GPU detected: {{gpu_proc.stdout.strip()}}', log_handle)
    if shutil.which('ffmpeg'):
        enc_proc = subprocess.run(
            ['ffmpeg', '-hide_banner', '-encoders'],
            capture_output=True,
            text=True,
            check=False,
        )
        if enc_proc.returncode == 0 and 'h264_nvenc' in enc_proc.stdout:
            has_nvenc = True
            log_line('[colab-render] FFmpeg h264_nvenc encoder available.', log_handle)
    return has_gpu, has_nvenc


def main():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open('w', encoding='utf-8') as log_handle:
        if not ARCHIVE_PATH.is_file():
            log_line(f'[colab-render] Missing uploaded archive: {{ARCHIVE_PATH}}', log_handle)
            raise SystemExit(2)

        if PROJECT_DIR.exists():
            shutil.rmtree(PROJECT_DIR)
        PROJECT_DIR.mkdir(parents=True, exist_ok=True)
        log_line(f'[colab-render] Extracting {{ARCHIVE_PATH}} -> {{PROJECT_DIR}}', log_handle)
        with tarfile.open(ARCHIVE_PATH, 'r:gz') as tf:
            tf.extractall(PROJECT_DIR)

        if node_major_version() < 22:
            log_line('[colab-render] Installing Node.js 22 LTS...', log_handle)
            run_step(
                'curl -fsSL https://deb.nodesource.com/setup_22.x | ' + ('sudo -E ' if SUDO else '') + 'bash - && '
                + ('sudo ' if SUDO else '') + 'DEBIAN_FRONTEND=noninteractive apt-get install -y -qq nodejs',
                log_handle,
                shell=True,
            )

        if not shutil.which('ffmpeg'):
            log_line('[colab-render] Installing ffmpeg...', log_handle)
            run_step(
                SUDO + ['apt-get', 'update', '-qq'],
                log_handle,
            )
            run_step(
                SUDO + ['apt-get', 'install', '-y', '-qq', '--no-install-recommends', 'ffmpeg'],
                log_handle,
            )

        if (PROJECT_DIR / 'package.json').is_file():
            if (PROJECT_DIR / 'package-lock.json').is_file():
                rc = run_step(['npm', 'ci', '--no-audit', '--no-fund'], log_handle, cwd=PROJECT_DIR, check=False)
                if rc != 0:
                    run_step(['npm', 'install', '--no-audit', '--no-fund'], log_handle, cwd=PROJECT_DIR)
            else:
                run_step(['npm', 'install', '--no-audit', '--no-fund'], log_handle, cwd=PROJECT_DIR)

        hf_check = subprocess.run(
            ['npx', '--no-install', 'hyperframes', '--version'],
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True,
            check=False,
        )
        if hf_check.returncode != 0 and not shutil.which('hyperframes'):
            run_step(['npm', 'install', '-g', 'hyperframes'], log_handle)

        run_step(['npx', 'hyperframes', 'browser', 'ensure'], log_handle, cwd=PROJECT_DIR, check=False)

        has_gpu, has_nvenc = detect_gpu_and_nvenc(log_handle)
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        if CONFIG['render_cmd']:
            run_step(['bash', '-lc', CONFIG['render_cmd']], log_handle, cwd=PROJECT_DIR)
        else:
            cmd = [
                'npx',
                'hyperframes',
                'render',
                '--quality',
                CONFIG['quality'],
                '--output',
                CONFIG['remote_output_rel'],
            ]
            if CONFIG['fps']:
                cmd.extend(['--fps', str(CONFIG['fps'])])
            if CONFIG['resolution']:
                cmd.extend(['--resolution', str(CONFIG['resolution'])])
            if CONFIG['fmt']:
                cmd.extend(['--format', str(CONFIG['fmt'])])

            extra = list(CONFIG['extra_args'])
            if CONFIG['enable_gpu_flags']:
                if has_gpu and has_nvenc and '--gpu' not in extra and '--no-gpu' not in extra:
                    cmd.append('--gpu')
                if has_gpu and '--browser-gpu' not in extra and '--no-browser-gpu' not in extra:
                    cmd.append('--browser-gpu')
            cmd.extend(extra)
            run_step(cmd, log_handle, cwd=PROJECT_DIR)

        if not OUTPUT_PATH.is_file() or OUTPUT_PATH.stat().st_size == 0:
            log_line(f'[colab-render] Expected output missing or empty: {{OUTPUT_PATH}}', log_handle)
            raise SystemExit(3)

        size_bytes = OUTPUT_PATH.stat().st_size
        log_line(f'[colab-render] Render complete: {{OUTPUT_PATH}} ({{size_bytes}} bytes)', log_handle)


main()
'''


def _colab_cmd(colab_bin: str, auth: str, *args: str) -> list[str]:
    return [colab_bin, f'--auth={auth}', *args]


def provision_session(
    colab_bin: str,
    *,
    auth: str,
    session: str,
    gpu: str,
    fallback_gpu: str | None,
) -> str:
    """Provision a Colab GPU session, falling back to fallback_gpu when primary fails."""
    candidates: list[str] = [gpu]
    if fallback_gpu and fallback_gpu.lower() != 'none' and fallback_gpu.upper() != gpu.upper():
        candidates.append(fallback_gpu)

    errors: list[str] = []
    for index, candidate in enumerate(candidates):
        cmd = _colab_cmd(colab_bin, auth, 'new', '-s', session, '--gpu', candidate)
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if proc.returncode == 0:
            return candidate
        detail = (proc.stderr or proc.stdout).strip() or f'exit {proc.returncode}'
        errors.append(f'{candidate}: {detail}')
        if index + 1 < len(candidates):
            print(
                f'colab_render: {candidate} GPU unavailable ({detail}); falling back to {candidates[index + 1]}...',
                file=sys.stderr,
            )

    raise RuntimeError('Failed to provision Colab GPU runtime: ' + ' | '.join(errors))


def fetch_remote_error_log(
    colab_bin: str,
    *,
    auth: str,
    session: str,
    remote_log_path: str = REMOTE_LOG_PATH,
    lines: int = DEFAULT_LOG_LINES,
) -> str:
    """Fetch the last N lines of the remote render log before stopping the session."""
    tail_code = (
        'from pathlib import Path\n'
        f'p = Path({remote_log_path!r})\n'
        'if p.is_file():\n'
        f'    data = p.read_text(encoding="utf-8", errors="replace").splitlines()\n'
        f'    print("\\n".join(data[-{int(lines)}:]))\n'
    )
    proc = subprocess.run(
        _colab_cmd(colab_bin, auth, 'exec', '-s', session, '--timeout', '30'),
        input=tail_code,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0 and proc.stdout.strip():
        return proc.stdout.strip()

    fallback = subprocess.run(
        _colab_cmd(colab_bin, auth, 'log', '-s', session, '-n', str(int(lines))),
        capture_output=True,
        text=True,
        check=False,
    )
    return (fallback.stdout or fallback.stderr or '').strip()


def stop_session(colab_bin: str, *, auth: str, session: str) -> tuple[bool, str]:
    """Terminate the Colab session to prevent leaking compute units."""
    proc = subprocess.run(
        _colab_cmd(colab_bin, auth, 'stop', '-s', session),
        capture_output=True,
        text=True,
        check=False,
    )
    detail = (proc.stderr or proc.stdout).strip()
    return proc.returncode == 0, detail


def probe_duration_seconds(media_path: Path) -> float | None:
    """Inspect downloaded video duration with local ffprobe when available."""
    ffprobe_bin = shutil.which('ffprobe')
    if not ffprobe_bin:
        return None
    proc = subprocess.run(
        [
            ffprobe_bin,
            '-v',
            'error',
            '-show_entries',
            'format=duration',
            '-of',
            'default=noprint_wrappers=1:nokey=1',
            str(media_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return None
    try:
        return round(float(proc.stdout.strip()), 3)
    except ValueError:
        return None


def offload_render(
    *,
    project_dir: Path,
    local_output: Path,
    remote_output: str | None = None,
    quality: str = DEFAULT_QUALITY,
    fps: str | None = None,
    resolution: str | None = None,
    fmt: str | None = None,
    extra_args: Sequence[str] = (),
    render_cmd: str | None = None,
    gpu: str = DEFAULT_GPU,
    fallback_gpu: str | None = DEFAULT_FALLBACK_GPU,
    session: str = DEFAULT_SESSION,
    auth: str = DEFAULT_AUTH,
    enable_gpu_flags: bool = True,
    extra_excludes: Sequence[str] = (),
    auto_install: bool = False,
    exec_timeout: float = 0.0,
    log_lines: int = DEFAULT_LOG_LINES,
    dry_run: bool = False,
) -> dict[str, object]:
    """Execute the full Google Colab GPU offload render lifecycle with guaranteed teardown."""
    resolved_project = project_dir.resolve()
    resolved_output = local_output.resolve()
    remote_output_rel = resolve_remote_output(resolved_output, remote_output)

    colab_bin = ensure_colab_cli(auto_install=auto_install)
    if auth == 'adc' and not dry_run:
        validate_adc_file()

    with tempfile.TemporaryDirectory(prefix='colab-render-') as tmpdir:
        tmp_path = Path(tmpdir)
        local_tar = tmp_path / 'project.tar.gz'
        file_count, tar_bytes = pack_project_tarball(
            resolved_project,
            local_tar,
            extra_excludes=extra_excludes,
        )
        runner_script = build_remote_runner_script(
            remote_archive=REMOTE_ARCHIVE_PATH,
            remote_project_dir=REMOTE_PROJECT_DIR,
            remote_output_rel=remote_output_rel,
            remote_log_path=REMOTE_LOG_PATH,
            quality=quality,
            fps=fps,
            resolution=resolution,
            fmt=fmt,
            extra_args=extra_args,
            render_cmd=render_cmd,
            enable_gpu_flags=enable_gpu_flags,
        )
        runner_path = tmp_path / 'remote_render.py'
        runner_path.write_text(runner_script, encoding='utf-8')

        if dry_run:
            return {
                'ok': True,
                'dry_run': True,
                'colab_bin': colab_bin,
                'auth': auth,
                'session': session,
                'gpu': gpu,
                'fallback_gpu': fallback_gpu,
                'project_dir': str(resolved_project),
                'packed_files': file_count,
                'archive_bytes': tar_bytes,
                'remote_output': f'{REMOTE_PROJECT_DIR}/{remote_output_rel}',
                'local_output': str(resolved_output),
            }

        session_allocated = False
        active_gpu = gpu
        teardown_ok = True
        teardown_detail = ''

        def _handle_signal(signum: int, _frame: object) -> None:
            raise KeyboardInterrupt(f'Received signal {signum}')

        prev_sigint = signal.getsignal(signal.SIGINT)
        prev_sigterm = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGINT, _handle_signal)
        signal.signal(signal.SIGTERM, _handle_signal)

        try:
            active_gpu = provision_session(
                colab_bin,
                auth=auth,
                session=session,
                gpu=gpu,
                fallback_gpu=fallback_gpu,
            )
            session_allocated = True

            upload_proc = subprocess.run(
                _colab_cmd(colab_bin, auth, 'upload', '-s', session, str(local_tar), REMOTE_ARCHIVE_PATH),
                capture_output=True,
                text=True,
                check=False,
            )
            if upload_proc.returncode != 0:
                detail = (upload_proc.stderr or upload_proc.stdout).strip()
                raise RuntimeError(f'Colab upload failed (exit {upload_proc.returncode}): {detail}')

            exec_proc = subprocess.run(
                _colab_cmd(
                    colab_bin,
                    auth,
                    'exec',
                    '-s',
                    session,
                    '--timeout',
                    str(exec_timeout),
                    '-f',
                    str(runner_path),
                ),
                capture_output=True,
                text=True,
                check=False,
            )
            if exec_proc.returncode != 0:
                error_tail = fetch_remote_error_log(
                    colab_bin,
                    auth=auth,
                    session=session,
                    remote_log_path=REMOTE_LOG_PATH,
                    lines=log_lines,
                )
                cli_err = (exec_proc.stderr or exec_proc.stdout).strip()
                msg_parts = [f'Colab render failed (exit {exec_proc.returncode}).']
                if error_tail:
                    msg_parts.append(f'Last {log_lines} lines of {REMOTE_LOG_PATH}:\n{error_tail}')
                elif cli_err:
                    msg_parts.append(f'CLI output:\n{cli_err}')
                raise RuntimeError('\n'.join(msg_parts))

            resolved_output.parent.mkdir(parents=True, exist_ok=True)
            remote_full_output = f'{REMOTE_PROJECT_DIR}/{remote_output_rel}'
            download_proc = subprocess.run(
                _colab_cmd(colab_bin, auth, 'download', '-s', session, remote_full_output, str(resolved_output)),
                capture_output=True,
                text=True,
                check=False,
            )
            if download_proc.returncode != 0:
                error_tail = fetch_remote_error_log(
                    colab_bin,
                    auth=auth,
                    session=session,
                    remote_log_path=REMOTE_LOG_PATH,
                    lines=log_lines,
                )
                detail = (download_proc.stderr or download_proc.stdout).strip()
                msg = f'Colab download failed (exit {download_proc.returncode}): {detail}'
                if error_tail:
                    msg += f'\nLast {log_lines} lines of {REMOTE_LOG_PATH}:\n{error_tail}'
                raise RuntimeError(msg)

            if not resolved_output.is_file() or resolved_output.stat().st_size == 0:
                raise RuntimeError(f'Downloaded output is missing or zero bytes: {resolved_output}')

            output_bytes = resolved_output.stat().st_size
            duration_s = probe_duration_seconds(resolved_output)
        finally:
            if session_allocated:
                teardown_ok, teardown_detail = stop_session(colab_bin, auth=auth, session=session)
                if not teardown_ok:
                    print(
                        f'WARNING: Failed to stop Colab session {session!r}: {teardown_detail}. '
                        f'Run `colab --auth={auth} stop -s {session}` immediately!',
                        file=sys.stderr,
                    )
            signal.signal(signal.SIGINT, prev_sigint)
            signal.signal(signal.SIGTERM, prev_sigterm)

    result: dict[str, object] = {
        'ok': True,
        'session': session,
        'gpu': active_gpu,
        'packed_files': file_count,
        'archive_bytes': tar_bytes,
        'local_output': str(resolved_output),
        'output_bytes': output_bytes,
        'session_stopped': teardown_ok,
    }
    if duration_s is not None:
        result['duration_seconds'] = duration_s
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Offload HyperFrames video rendering to Google Colab GPU via google-colab-cli.'
    )
    parser.add_argument('--check', action='store_true', help='Verify colab CLI and ADC authentication/scopes without starting a VM')
    parser.add_argument('--project', type=Path, help='Local HyperFrames project directory (e.g. productions/<slug>/video)')
    parser.add_argument('-o', '--output', type=Path, dest='local_output', help='Local output video path to write')
    parser.add_argument('--remote-output', default=None, help='Relative output path inside /content/project (default: colab-out/<filename>)')
    parser.add_argument('-q', '--quality', default=DEFAULT_QUALITY, help='HyperFrames quality preset: draft, looks, delivery, standard, high')
    parser.add_argument('--fps', default=None, help='Optional frame rate forwarded to hyperframes render --fps')
    parser.add_argument('--resolution', default=None, help='Optional resolution preset forwarded to hyperframes render --resolution')
    parser.add_argument('--format', dest='fmt', default=None, help='Optional output format forwarded to hyperframes render --format')
    parser.add_argument('--extra-arg', action='append', default=[], help='Additional flag forwarded to hyperframes render (repeatable)')
    parser.add_argument('--render-cmd', default=None, help='Custom bash render command executed inside /content/project')
    parser.add_argument('--gpu', default=DEFAULT_GPU, help='Primary Colab GPU accelerator (default: L4)')
    parser.add_argument('--fallback-gpu', default=DEFAULT_FALLBACK_GPU, help='Fallback Colab GPU if primary is unavailable (default: T4; "none" to disable)')
    parser.add_argument('-s', '--session', default=DEFAULT_SESSION, help='Colab session name (default: hyperframes-render)')
    parser.add_argument('--auth', choices=('adc', 'oauth2'), default=DEFAULT_AUTH, help='google-colab-cli auth mode (default: adc)')
    parser.add_argument('--no-gpu-encode', action='store_true', help='Do not auto-append --gpu / --browser-gpu flags to hyperframes render')
    parser.add_argument('--exclude', action='append', default=[], help='Additional glob/name exclusion when packing the project tarball (repeatable)')
    parser.add_argument('--auto-install', action='store_true', help='Install google-colab-cli automatically if missing')
    parser.add_argument('--timeout', type=float, default=0.0, help='Idle output timeout in seconds for colab exec (default: 0 = unlimited)')
    parser.add_argument('--log-lines', type=int, default=DEFAULT_LOG_LINES, help='Error log tail line count fetched before teardown (default: 50)')
    parser.add_argument('--dry-run', action='store_true', help='Validate and pack the project tarball without provisioning a Colab VM')
    parser.add_argument('--json', action='store_true', dest='as_json', help='Print machine-readable JSON output')
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.check:
            report = check_prerequisites(auth=args.auth, auto_install=args.auto_install)
            if args.as_json:
                print(json.dumps(report, indent=2))
            else:
                print(f"colab: {report['colab_bin']}")
                if 'adc_path' in report:
                    print(f"adc: {report['adc_path']}")
                print(f"whoami: {report['whoami']}")
            return 0 if report['ok'] else 1

        if not args.project or not args.local_output:
            parser.error('--project and --output are required unless --check is set.')

        result = offload_render(
            project_dir=args.project,
            local_output=args.local_output,
            remote_output=args.remote_output,
            quality=args.quality,
            fps=args.fps,
            resolution=args.resolution,
            fmt=args.fmt,
            extra_args=args.extra_arg,
            render_cmd=args.render_cmd,
            gpu=args.gpu,
            fallback_gpu=args.fallback_gpu,
            session=args.session,
            auth=args.auth,
            enable_gpu_flags=not args.no_gpu_encode,
            extra_excludes=args.exclude,
            auto_install=args.auto_install,
            exec_timeout=args.timeout,
            log_lines=args.log_lines,
            dry_run=args.dry_run,
        )
    except (ValueError, RuntimeError, OSError, KeyboardInterrupt) as exc:
        if args.as_json:
            print(json.dumps({'ok': False, 'error': str(exc)}, indent=2))
        else:
            print(f'colab_render: {exc}', file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(result, indent=2))
    elif result.get('dry_run'):
        print(
            f"Dry run OK: packed {result['packed_files']} files ({result['archive_bytes']} bytes) "
            f"from {result['project_dir']} -> {result['local_output']} (session {result['session']}, GPU {result['gpu']} / fallback {result['fallback_gpu']})"
        )
    else:
        dur_part = f", duration {result['duration_seconds']}s" if 'duration_seconds' in result else ''
        print(
            f"Rendered on Colab {result['gpu']} -> {result['local_output']} "
            f"({result['output_bytes']} bytes{dur_part}); session {result['session']} stopped."
        )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
