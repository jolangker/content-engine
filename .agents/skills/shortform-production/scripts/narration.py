"""Generate timed narration with the ElevenLabs CLI and reuse verified recordings."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


NATIVE_TAIL_TOLERANCE_S = 0.1


def read_env(root: Path) -> dict[str, str]:
    path = root / '.env'
    values = {}
    if path.exists():
        for raw in path.read_text(encoding='utf-8-sig').splitlines():
            line = raw.strip().removeprefix('export ')
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            value = value.strip()
            if value[:1] in ('"', "'"):
                quote = value[0]
                end = value.find(quote, 1)
                if end < 0:
                    raise ValueError(f'Unclosed quoted value for {key.strip()} in .env')
                value = value[1:end]
            else:
                value = re.split(r'\s+#', value, maxsplit=1)[0].strip()
            values[key.strip()] = value
    return values


def board_audio_path(root: Path, board: str) -> Path:
    tracker = json.loads((root / 'TRACKER.json').read_text(encoding='utf-8-sig'))
    matches = [entry for entry in tracker['boards'] if entry['slug'] == board]
    if len(matches) != 1:
        raise ValueError(f'Expected one registered board for {board!r}')
    folder = (root / matches[0]['path']).resolve()
    if not folder.is_relative_to(root.resolve()) or not folder.is_dir():
        raise ValueError(f'Invalid registered board path for {board!r}')
    return folder / 'AUDIO.json'


def production_board(video: Path, root: Path) -> str | None:
    tracker_path = root / 'TRACKER.json'
    if not tracker_path.exists():
        return None
    tracker = json.loads(tracker_path.read_text(encoding='utf-8-sig'))
    matches = [entry for entry in tracker['productions']
               if (root / entry['path'] / 'video').resolve() == video.resolve()]
    if len(matches) > 1:
        raise ValueError('Multiple productions registered for this video directory')
    return matches[0].get('board') if matches else None


def resolve_voice(root: Path, override: str | None = None, reason: str = '', *,
                  board: str | None = None) -> tuple[str, dict]:
    if override:
        if not reason.strip():
            raise ValueError('An episode voice override requires its user-authorized reason')
        return override, {'source': 'episode_override', 'reason': reason.strip()}
    if board is not None:
        path = board_audio_path(root, board)
        if path.exists():
            config = json.loads(path.read_text(encoding='utf-8-sig'))
            if not isinstance(config, dict) or type(config.get('schema_version')) is not int or config['schema_version'] != 1:
                raise ValueError(f'Expected schema_version=1 in {path}')
            voice = config.get('voice_id')
            if voice is not None and not isinstance(voice, str):
                raise ValueError(f'voice_id must be a string or null in {path}')
            if voice and voice.strip():
                if voice.strip() == 'your-elevenlabs-voice-id':
                    raise ValueError(f'Replace the placeholder voice_id in {path}')
                return voice.strip(), {'source': 'board_config', 'board': board,
                                       'path': path.relative_to(root.resolve()).as_posix(), 'key': 'voice_id'}
    voice = read_env(root).get('ELEVENLABS_VOICE_ID', '').strip()
    if not voice or voice == 'your-elevenlabs-voice-id':
        raise ValueError('Set ELEVENLABS_VOICE_ID in the project root .env; no fallback voice is selected')
    return voice, {'source': 'project_env', 'key': 'ELEVENLABS_VOICE_ID'}


def generation_payload(request: dict, root: Path, *, board: str | None = None) -> dict:
    if board is not None and request.get('board') not in (None, board):
        raise ValueError('Request board differs from the registered production board')
    board = board if board is not None else request.get('board')
    resolution = request.get('voice_resolution', {'source': 'project_env'})
    if resolution.get('source') == 'episode_override':
        if not request.get('voice'):
            raise ValueError('An episode voice override requires a voice ID')
        voice, _ = resolve_voice(root, request.get('voice'), resolution.get('reason', ''))
    elif resolution.get('source') in ('project_env', 'board_config'):
        if resolution['source'] == 'board_config' and board is None:
            raise ValueError('A board_config request requires a board slug')
        voice, expected = resolve_voice(root, board=board)
        if (resolution['source'] != expected['source'] or
                (expected['source'] == 'board_config' and resolution != expected)):
            raise ValueError('Voice source changed; prepare the request again before synthesis')
    else:
        raise ValueError('Unknown voice_resolution source')
    if request.get('voice') != voice:
        raise ValueError('Request voice differs from the resolved voice; prepare the request again before synthesis')
    if request.get('provider') != 'elevenlabs' or request.get('tts_model') != 'eleven_v4':
        raise ValueError('This project requires explicit provider=elevenlabs and tts_model=eleven_v4')
    lines = request.get('lines', [])
    if len(lines) != 1 or lines[0].get('id') != 'narration' or not lines[0].get('text', '').strip():
        raise ValueError('Use one nonempty full-script line with id=narration')
    if request.get('speed', 1) != 1:
        raise ValueError('Keep narration at native speed')
    return {
        'provider': request['provider'], 'voice_id': voice,
        'model_id': request['tts_model'], 'text': lines[0]['text'],
        'language_code': request.get('lang', 'id'), 'output_format': 'mp3_44100_128',
        **({'voice_settings': request['voice_settings']} if 'voice_settings' in request else {}),
        **({'seed': request['seed']} if 'seed' in request else {}),
    }


def fingerprint(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cached_result(dest: Path, identity: str) -> dict | None:
    alignment = dest.with_suffix('.alignment.json')
    receipt = dest.with_suffix('.request.json')
    if not all(p.is_file() for p in (dest, alignment, receipt)):
        return None
    try:
        meta = json.loads(receipt.read_text(encoding='utf-8'))
        if (meta.get('request_sha256') != identity or
                meta.get('audio_sha256') != file_hash(dest) or
                meta.get('alignment_sha256') != file_hash(alignment)):
            return None
        return json.loads(alignment.read_text(encoding='utf-8'))
    except (ValueError, OSError):
        return None


def words_from_alignment(result: dict) -> list[dict]:
    if 'words' in result:
        words = result['words']
        if not isinstance(words, list) or not words:
            raise ValueError('Word timings must be a nonempty list')
        cleaned, previous_start, previous_end = [], -1, -1
        for word in words:
            text, start, end = word.get('text'), word.get('start'), word.get('end')
            if (not isinstance(text, str) or not text.strip() or '[' in text or ']' in text or
                    any(isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t)
                        for t in (start, end)) or
                    start < 0 or end <= start or start < previous_start or end < previous_end):
                raise ValueError('Invalid spoken-word timing; delivery tags do not belong in captions')
            previous_start, previous_end = start, end
            cleaned.append({'id': f'w{len(cleaned):04d}', 'text': text.strip(), 'start': start, 'end': end})
        return cleaned
    for key in ('normalized_alignment', 'alignment'):
        words = _alignment_words(result.get(key))
        if words:
            for i, word in enumerate(words):
                word['id'] = f'w{i:04d}'
            return words
    raise ValueError('Native alignment is missing or invalid; transcribe this exact audio without resynthesis')


def _alignment_words(align: dict | None) -> list[dict] | None:
    if not isinstance(align, dict):
        return None
    arrays = [align.get(k) for k in ('characters', 'character_start_times_seconds', 'character_end_times_seconds')]
    if not all(isinstance(a, list) and a for a in arrays) or len({len(a) for a in arrays}) != 1:
        return None
    words, current, in_tag = [], None, False
    previous_start = previous_end = -1
    for chunk, start, end in zip(*arrays):
        if (not isinstance(chunk, str) or not chunk or
                any(isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) for t in (start, end)) or
                start < 0 or end < start or start < previous_start or end < previous_end):
            return None
        previous_start, previous_end = start, end
        for char in chunk:
            if char == '[':
                if current:
                    words.append(current)
                current, in_tag = None, True
                continue
            if in_tag:
                if char == ']':
                    in_tag = False
                continue
            if char.isspace():
                if current:
                    words.append(current)
                current = None
            else:
                if current is None:
                    current = {'text': '', 'start': start, 'end': end}
                current['text'] += char
                current['end'] = end
    if current:
        words.append(current)
    return words if not in_tag and words and all(w['end'] > w['start'] for w in words) else None


def mcp_arguments(payload: dict) -> dict:
    """Only advertise fields supported by the connected creative speech tool."""
    if any(key in payload for key in ('voice_settings', 'seed')):
        raise ValueError('creative_generate_speech does not expose voice_settings or seed; resolve these settings before generation')
    return {'model_id': payload['model_id'], 'voice_id': payload['voice_id'],
            'prompt': payload['text'], 'generations_count': 1}


def validate_mcp_receipt(receipt: dict, payload: dict, identity: str, source: Path) -> dict:
    if receipt.get('request_sha256') != identity or receipt.get('tool') != 'creative_generate_speech':
        raise ValueError('MCP receipt does not match this narration request')
    expected = mcp_arguments(payload)
    args = receipt.get('arguments', {})
    if type(args.get('generations_count')) is not int or args['generations_count'] != 1:
        raise ValueError('MCP speech requires explicit generations_count=1 for a single take')
    if any(args.get(key) != value for key, value in expected.items()):
        raise ValueError('MCP speech arguments differ from the prepared request')
    if set(args) - (set(expected) | {'flow_id'}):
        raise ValueError('Unsupported MCP speech arguments in receipt')
    if receipt.get('audio_sha256') != file_hash(source):
        raise ValueError('Downloaded audio does not match the MCP receipt hash')
    if not all(receipt.get(key) for key in ('flow_id', 'node_id', 'session_ids', 'generation_id')):
        raise ValueError('MCP receipt requires flow, node, sessions, and selected generation IDs')
    if args.get('flow_id') not in (None, receipt['flow_id']):
        raise ValueError('MCP speech arguments belong to a different flow')
    response = receipt.get('response', {})
    if response.get('flow_id') not in (None, receipt['flow_id']):
        raise ValueError('MCP response belongs to a different flow')
    selected = [item for item in response.get('media', [])
                if item.get('generation_id') == receipt['generation_id'] and item.get('kind') == 'audio']
    if len(selected) != 1:
        raise ValueError('Selected generation is not a finished audio result in the MCP response')
    media = selected[0]
    if (media.get('model_id') not in (None, payload['model_id']) or
            media.get('prompt') not in (None, payload['text']) or
            media.get('voice', {}).get('voice_id') not in (None, payload['voice_id'])):
        raise ValueError('Selected MCP audio has a different model, text, or voice')
    # Persist stable provenance, not short-lived signed media URLs.
    return {key: receipt[key] for key in ('tool', 'arguments', 'flow_id', 'node_id', 'session_ids', 'generation_id')}


def cli_launcher() -> list[str]:
    executable = shutil.which('elevenlabs.exe' if os.name == 'nt' else 'elevenlabs')
    if executable:
        return [executable]
    if os.name == 'nt':
        shim = shutil.which('elevenlabs.cmd')
        if shim:
            folder = Path(shim).parent
            node = folder / 'node.exe'
            node = str(node) if node.is_file() else shutil.which('node.exe')
            entry = folder / 'node_modules/@elevenlabs/cli/bin/cli.js'
            # Use the npm entry point directly so cmd.exe never parses narration text.
            if node and entry.is_file():
                return [node, str(entry)]
    raise ValueError('ElevenLabs CLI not found on PATH. Install @elevenlabs/cli and run elevenlabs auth status.')


def run_cli(launcher: list[str], args: list[str], root: Path) -> str:
    proc = subprocess.run([*launcher, *args], cwd=root, capture_output=True, encoding='utf-8', errors='replace')
    if proc.returncode:
        # CLI diagnostics can contain request details. Only expose numeric error codes.
        code = re.search(r'"code"\s*:\s*(\d{3})|\bHTTP[/\s]+(\d{3})\b', proc.stderr)
        if code and (code[1] or code[2]) in ('401', '403'):
            raise ValueError(f'ElevenLabs CLI authentication or access failed (HTTP {code[1] or code[2]}). Check elevenlabs auth status and voice access.')
        status = f'HTTP {code[1] or code[2]}' if code else f'exit {proc.returncode}'
        raise ValueError(f'ElevenLabs CLI {args[0]} failed ({status})')
    return proc.stdout


def cli_response(payload: dict, root: Path) -> dict:
    launcher = cli_launcher()
    version = run_cli(launcher, ['--version'], root).strip()
    command = 'text-to-speech convert_with_timestamps'
    args = [
        *command.split(), f"--voice-id={payload['voice_id']}", f"--model-id={payload['model_id']}",
        f"--output-format={payload['output_format']}",
        f"--text={payload['text']}", '--no-retry', '--no-extract', '--format', 'raw',
    ]
    if payload['language_code'] is not None:
        args.append(f"--language-code={payload['language_code']}")
    for key in ('voice_settings', 'seed'):
        if key in payload:
            args.append(f"--{key.replace('_', '-')}={json.dumps(payload[key])}")
    try:
        response = json.loads(run_cli(launcher, args, root))
    except json.JSONDecodeError:
        raise ValueError('ElevenLabs CLI returned invalid speech JSON') from None
    return {'cli': {'version': version, 'command': command}, 'response': response,
            'request_sha256': fingerprint(payload)}


def atomic_write(path: Path, data: bytes) -> None:
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def write_json(path: Path, data: dict) -> None:
    atomic_write(path, (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def audio_duration(path: Path) -> float:
    if not shutil.which('ffprobe'):
        raise ValueError('Install ffprobe to verify the narration MP3 duration')
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,format_name', '-of', 'json', str(path)],
                           capture_output=True, text=True, check=True)
    info = json.loads(probe.stdout)['format']
    duration = float(info['duration'])
    if info.get('format_name') != 'mp3' or not math.isfinite(duration) or duration <= 0:
        raise ValueError('Expected a valid MP3 recording; convert the downloaded asset locally without resynthesis')
    return duration


def validate_asr_verification(result: dict) -> None:
    check = result.get('asr_verification')
    if isinstance(check, dict) and check.get('passed') is False and not check.get('overridden'):
        raise ValueError(
            f"ASR script verification failed (similarity={check.get('similarity')}, "
            f"tags_spoken={len(check.get('tags_spoken') or [])}, "
            f"number_mismatches={len(check.get('number_mismatches') or [])}); "
            'inspect mismatches, add approved phonetic aliases, or regenerate narration'
        )


def load_timings(timings: Path, audio: Path) -> dict:
    result = json.loads(timings.read_text(encoding='utf-8-sig'))
    if result.get('audio_sha256') != file_hash(audio):
        raise ValueError('Word timings belong to a different audio file; align this exact recording')
    validate_asr_verification(result)
    return result


def run_auto_alignment(audio: Path, payload: dict, request: dict) -> dict:
    import importlib.util
    helper_path = Path(__file__).with_name('align_narration.py')
    spec = importlib.util.spec_from_file_location('align_narration', helper_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    aliases = request.get('asr_aliases') if isinstance(request.get('asr_aliases'), dict) else None
    return mod.align_audio_to_script(
        audio,
        payload['text'],
        lang=payload.get('language_code') or 'id',
        aliases=aliases,
    )


def recover_cli_take(pending: Path, dest: Path, identity: str, timings: Path | None) -> tuple[dict, dict]:
    saved = json.loads(pending.read_text(encoding='utf-8'))
    if saved.get('request_sha256') != identity:
        raise ValueError(f'Saved CLI response belongs to a different request: {pending}')
    response = saved['response']
    try:
        audio = base64.b64decode(response['audio_base64'], validate=True)
    except (TypeError, KeyError, ValueError):
        raise ValueError(f'ElevenLabs CLI response contains no usable audio: {pending}') from None
    if not audio:
        raise ValueError(f'ElevenLabs CLI response contains empty audio: {pending}')
    if dest.is_file():
        if dest.read_bytes() != audio:
            raise ValueError(f'Pending CLI response does not match existing audio: {dest}')
    else:
        atomic_write(dest, audio)
    if timings:
        result = load_timings(timings, dest)
    else:
        result = {key: response.get(key) for key in ('alignment', 'normalized_alignment')}
    return result, {'transport': 'elevenlabs_cli', 'cli': saved['cli']}


def measured_words(result: dict, path: Path) -> tuple[list[dict], float]:
    words = words_from_alignment(result)
    duration = audio_duration(path)
    last = words[-1]
    if (last['start'] >= duration or (len(words) > 1 and words[-2]['end'] > duration)
            or last['end'] > duration + (0.05 if 'words' in result else NATIVE_TAIL_TOLERANCE_S)):
        raise ValueError('Word timings exceed the recording duration')
    # The native endpoint can put trailing punctuation slightly beyond the MP3.
    last['end'] = min(last['end'], duration)
    return words, duration


def write_metadata(video: Path, request: dict, payload: dict, summary: dict,
                   words: list[dict], duration: float, receipt: dict, alignment_info: dict | None = None) -> None:
    voice_entry = {'id': 'narration', 'path': summary['path'], 'duration_s': duration, 'words': words}
    if isinstance(alignment_info, dict):
        for key in ('alignment_method', 'align_model', 'asr_model', 'asr_verification'):
            if alignment_info.get(key) is not None:
                voice_entry[key] = alignment_info[key]
    meta = {'tts_provider': payload['provider'], 'voice_id': payload['voice_id'], 'tts_model': payload['model_id'],
            'voice_resolution': request.get('voice_resolution'), 'request_sha256': summary['request_sha256'],
            'voices': [voice_entry],
            'sfx': [], 'bgm': None, 'bgm_pending': False, 'total_duration_s': duration}
    if receipt.get('transport') in ('elevenlabs_cli', 'elevenlabs_mcp'):
        meta['tts_transport'] = receipt['transport']
        for key in ('cli', 'mcp'):
            if key in receipt:
                meta[key] = receipt[key]
    write_json(video / 'audio_meta.json', merge_supplemental_audio(video, meta))


def synthesize(video: Path, root: Path, *, check: bool = False, mcp_receipt: Path | None = None,
               audio: Path | None = None, timings: Path | None = None, auto_align: bool = False) -> dict:
    importing = mcp_receipt is not None or audio is not None
    if importing and not (mcp_receipt and audio and (timings or auto_align)):
        raise ValueError('MCP import requires --import-mcp, --audio, and either --timings or --auto-align.')
    if check and (importing or timings or auto_align):
        raise ValueError('--check runs alone without import or alignment flags.')
    if timings and auto_align:
        raise ValueError('Pass either --timings or --auto-align, not both.')
    if not (video / 'audio_request.json').is_file():
        raise ValueError(f'Missing audio_request.json in {video}')
    if check:
        return resolve_take(video, root, check=True)
    cache = video / '.media/audio/voice'
    cache.mkdir(parents=True, exist_ok=True)
    lock = cache / '.narration.lock'
    try:
        lock.mkdir()
    except FileExistsError:
        raise ValueError(f'Narration is locked: {lock}. Check whether another run is active.') from None
    try:
        return resolve_take(video, root, mcp_receipt=mcp_receipt, audio=audio, timings=timings, auto_align=auto_align)
    finally:
        lock.rmdir()


def resolve_take(video: Path, root: Path, *, check: bool = False, mcp_receipt: Path | None = None,
                 audio: Path | None = None, timings: Path | None = None, auto_align: bool = False) -> dict:
    request = json.loads((video / 'audio_request.json').read_text(encoding='utf-8-sig'))
    payload = generation_payload(request, root, board=production_board(video, root))
    identity = fingerprint(payload)
    dest = video / '.media/audio/voice' / f'narration-{identity[:20]}.mp3'
    alignment = dest.with_suffix('.alignment.json')
    receipt_path = dest.with_suffix('.request.json')
    pending = dest.with_suffix('.cli-response.json')
    result = cached_result(dest, identity)
    summary = {'provider': payload['provider'], 'voice': payload['voice_id'], 'model': payload['model_id'],
               'request_sha256': identity, 'path': dest.relative_to(video).as_posix(), 'cache_hit': result is not None}
    if result is None and (receipt_path.exists() or
                           (not pending.is_file() and (dest.exists() or alignment.exists()))):
        raise ValueError('Incomplete or corrupt audio cache; recover or archive it before starting a new take')
    if check:
        status = 'resume_cli' if pending.is_file() else 'awaiting_cli'
        if result is not None:
            status = 'cached'
        return {**summary, 'status': status}
    if result is not None:
        validate_asr_verification(result)
        words, duration = measured_words(result, dest)
        receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
    else:
        if mcp_receipt:
            if pending.exists():
                raise ValueError('A saved CLI take already exists for this request; resume it before importing MCP audio')
            saved = json.loads(mcp_receipt.read_text(encoding='utf-8-sig'))
            provenance = {'transport': 'elevenlabs_mcp',
                          'mcp': validate_mcp_receipt(saved, payload, identity, audio)}
            result = run_auto_alignment(audio, payload, request) if auto_align else load_timings(timings, audio)
            words, duration = measured_words(result, audio)
            atomic_write(dest, audio.read_bytes())
        else:
            if not pending.is_file():
                if timings:
                    raise ValueError('--timings requires a saved CLI response for this request')
                if not shutil.which('ffprobe'):
                    raise ValueError('Install ffprobe before generating narration')
                write_json(pending, cli_response(payload, root))
            result, provenance = recover_cli_take(pending, dest, identity, timings)
            try:
                words, duration = measured_words(result, dest)
            except ValueError as error:
                if auto_align and not timings:
                    result = run_auto_alignment(dest, payload, request)
                    words, duration = measured_words(result, dest)
                else:
                    raise ValueError(f'{error}. Saved CLI take: {dest}') from None
            except subprocess.CalledProcessError as error:
                raise ValueError(f'{error}. Saved CLI take: {dest}') from None
        result['audio_sha256'] = file_hash(dest)
        write_json(alignment, result)
        receipt = {**summary, **provenance, 'voice_resolution': request.get('voice_resolution'), 'payload': payload,
                   'audio_sha256': result['audio_sha256'], 'alignment_sha256': file_hash(alignment)}
        write_json(receipt_path, receipt)
        pending.unlink(missing_ok=True)
    write_metadata(video, request, payload, summary, words, duration, receipt, alignment_info=result)
    return {**summary, 'status': 'ready', 'duration_s': duration, 'words': len(words)}


def merge_supplemental_audio(video: Path, meta: dict) -> dict:
    """Voice generation must not erase media decisions owned by sound design."""
    previous = video / 'audio_meta.json'
    if previous.exists():
        old = json.loads(previous.read_text(encoding='utf-8-sig'))
        for key in ('sfx', 'bgm', 'bgm_pending'):
            if key in old:
                meta[key] = old[key]
    if (video / 'sound_design.json').exists():
        meta['sound_design'] = {'path': 'sound_design.json', 'needs_revalidation': True}
    return meta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', type=Path, required=True)
    parser.add_argument('--project-root', type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument('--check', action='store_true', help='Inspect request and cache without generating or writing')
    parser.add_argument('--import-mcp', type=Path, help='Receipt for a completed single-take MCP narration')
    parser.add_argument('--audio', type=Path, help='Downloaded MP3 for an MCP import')
    parser.add_argument('--timings', type=Path, help='Measured timing JSON bound to the saved MP3 by audio_sha256')
    parser.add_argument('--auto-align', action='store_true',
                        help='Run local ASR script check + Wav2Vec2 CTC forced alignment when native timings are absent')
    args = parser.parse_args()
    try:
        print(json.dumps(synthesize(args.video.resolve(), args.project_root.resolve(), check=args.check,
                                    mcp_receipt=args.import_mcp, audio=args.audio, timings=args.timings,
                                    auto_align=args.auto_align)))
    except Exception as error:
        # Provider exceptions can contain request headers. Report only their class/status.
        detail = str(error) if isinstance(error, ValueError) else type(error).__name__
        print(json.dumps({'error': detail, 'status_code': getattr(error, 'status_code', None)}))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
