"""Resolve project voice settings and synthesize one request with verified caching."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess


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


def synthesize(video: Path, root: Path, *, check: bool = False, client=None) -> dict:
    request = json.loads((video / 'audio_request.json').read_text(encoding='utf-8'))
    payload = generation_payload(request, root, board=production_board(video, root))
    identity = fingerprint(payload)
    dest = video / '.media/audio/voice' / f'narration-{identity[:20]}.mp3'
    result = cached_result(dest, identity)
    summary = {'provider': payload['provider'], 'voice': payload['voice_id'], 'model': payload['model_id'],
               'request_sha256': identity, 'path': dest.relative_to(video).as_posix(), 'cache_hit': result is not None}
    if check:
        return summary
    if result is None:
        # A corrupt/incomplete cache is preserved for diagnosis, never overwritten.
        if any(p.exists() for p in (dest, dest.with_suffix('.alignment.json'), dest.with_suffix('.request.json'))):
            raise ValueError('Incomplete or corrupt audio cache; preserve and move that cache set before an explicit retry')
        if client is None:
            from elevenlabs.client import ElevenLabs
            key = os.environ.get('ELEVENLABS_API_KEY') or read_env(root).get('ELEVENLABS_API_KEY')
            if not key:
                raise ValueError('ELEVENLABS_API_KEY is missing')
            client = ElevenLabs(api_key=key)
        response = client.text_to_speech.convert_with_timestamps(
            **{k: v for k, v in payload.items() if k != 'provider'},
            request_options={'max_retries': 0, 'timeout_in_seconds': 180},
        )
        result = response.model_dump()
        encoded = result.pop('audio_base64', None) or result.pop('audio_base_64', None)
        if not encoded:
            raise ValueError('Provider returned no audio bytes')
        audio_bytes = base64.b64decode(encoded, validate=True)
        if not audio_bytes:
            raise ValueError('Provider returned empty audio')
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(audio_bytes)
        alignment = dest.with_suffix('.alignment.json')
        alignment.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        dest.with_suffix('.request.json').write_text(json.dumps({
            **summary, 'voice_resolution': request.get('voice_resolution'), 'payload': payload,
            'audio_sha256': file_hash(dest), 'alignment_sha256': file_hash(alignment),
        }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    words = words_from_alignment(result)
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(dest)],
                           capture_output=True, text=True, check=True)
    duration = float(json.loads(probe.stdout)['format']['duration'])
    meta = {'tts_provider': payload['provider'], 'voice_id': payload['voice_id'], 'tts_model': payload['model_id'],
            'voice_resolution': request.get('voice_resolution'), 'request_sha256': identity,
            'voices': [{'id': 'narration', 'path': dest.relative_to(video).as_posix(), 'duration_s': duration, 'words': words}],
            'sfx': [], 'bgm': None, 'bgm_pending': False, 'total_duration_s': duration}
    meta = merge_supplemental_audio(video, meta)
    (video / 'audio_meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {**summary, 'duration_s': duration, 'words': len(words)}


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
    parser.add_argument('--check', action='store_true', help='Validate identity and cache without calling the API or writing files')
    args = parser.parse_args()
    try:
        print(json.dumps(synthesize(args.video.resolve(), args.project_root.resolve(), check=args.check)))
    except Exception as error:
        # Provider exceptions can contain request headers. Report only their class/status.
        detail = str(error) if isinstance(error, ValueError) else type(error).__name__
        print(json.dumps({'error': detail, 'status_code': getattr(error, 'status_code', None)}))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
