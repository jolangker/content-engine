"""Regenerate approved full narration once; keep v1 playback assets intact."""
from pathlib import Path
import asyncio
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.media/tts-packages'))
import edge_tts

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def normalize(text):
    return ''.join(re.findall(r'\w+', text.lower()))

async def main():
    script = (ROOT.parent / 'SCRIPT.md').read_text(encoding='utf-8')
    text = script.split('## Narasi utuh', 1)[1].split('## Pembagian beat', 1)[0].strip()
    frames = json.loads((ROOT / 'boards/frame-manifest.json').read_text(encoding='utf-8'))
    assert normalize(text) == normalize(' '.join(f['vo'] for f in frames))
    out = ROOT / 'assets/voice/narration-v2'
    out.mkdir(parents=True, exist_ok=True)
    mp3 = out / 'narration-ardi-full.mp3'
    if mp3.exists():
        raise FileExistsError('v2 already exists; inspect before generating another take')
    request = {'provider': 'edge-tts', 'voice': 'id-ID-ArdiNeural', 'rate': '+15%',
               'lang': 'id', 'lines': [{'id': 'narration', 'text': text}], 'bgm': {'mode': 'none'}}
    write_json(out / 'audio_request.json', request)
    words = []
    partial = mp3.with_suffix('.partial.mp3')
    communicate = edge_tts.Communicate(text, voice=request['voice'], rate=request['rate'], boundary='WordBoundary')
    with partial.open('wb') as audio:
        async for chunk in communicate.stream():
            if chunk['type'] == 'audio':
                audio.write(chunk['data'])
            elif chunk['type'] == 'WordBoundary':
                words.append({'id': f'w{len(words)}', 'text': chunk['text'],
                              'start': chunk['offset'] / 10_000_000,
                              'end': (chunk['offset'] + chunk['duration']) / 10_000_000})
    probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(partial)], text=True))
    duration = float(probe['format']['duration'])
    assert words and partial.stat().st_size > 1000
    assert normalize(' '.join(w['text'] for w in words)) == normalize(text)
    assert all(0 <= w['start'] < w['end'] <= duration + .1 for w in words)
    assert all(a['end'] <= b['start'] + .001 for a, b in zip(words, words[1:]))
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(partial), '-f', 'null', '-'], check=True, capture_output=True)
    mp3.write_bytes(partial.read_bytes())
    partial.unlink()
    scene_map, cursor = [], 0
    for frame in frames:
        start = cursor
        target = normalize(frame['vo'])
        combined = ''
        while cursor < len(words) and len(combined) < len(target):
            combined += normalize(words[cursor]['text'])
            cursor += 1
        assert combined == target, frame['n']
        scene_map.append({'frame': frame['n'], 'word_start': start, 'word_end_exclusive': cursor,
                          'speech_start_s': words[start]['start'], 'speech_end_s': words[cursor - 1]['end'],
                          'text': frame['vo']})
    assert cursor == len(words)
    for i, scene in enumerate(scene_map):
        scene['scene_start_s'] = 0 if i == 0 else scene['speech_start_s']
        scene['scene_end_s'] = scene_map[i + 1]['speech_start_s'] if i + 1 < len(scene_map) else duration
    voice = {'id': 'narration', 'provider': 'edge-tts', 'voice': request['voice'], 'rate': request['rate'],
             'path': mp3.relative_to(ROOT).as_posix(), 'duration_s': duration, 'start_s': 0,
             'words': words, 'text': text, 'timing_source': 'native Microsoft WordBoundary'}
    metadata = {'version': 2, 'voices': [voice], 'sfx': [], 'bgm': None,
                'total_duration_s': duration, 'scene_map': scene_map,
                'composition_sync': 'pending; preview/export v1 still use original scene audio'}
    write_json(out / 'audio_meta.json', metadata)
    write_json(out / 'narration-ardi-full.words.json', words)
    receipt = {'voice': request['voice'], 'rate': request['rate'], 'text': text,
               'edge_tts_version': edge_tts.__version__, 'synthesis_calls': 1,
               'sha256': hashlib.sha256(mp3.read_bytes()).hexdigest(), 'duration_s': duration,
               'word_count': len(words), 'normalized_text_match': True,
               'monotonic_word_timestamps': True, 'ffmpeg_full_decode': 'passed'}
    write_json(out / 'verification.json', receipt)
    ledger = ROOT / '.media/manifest.jsonl'
    with ledger.open('a', encoding='utf-8') as fp:
        fp.write(json.dumps({'type': 'voice', 'path': voice['path'], 'provider': 'edge-tts',
                             'version': 2, 'voice': request['voice'], 'rate': request['rate'],
                             'duration_s': duration, 'word_timestamps': 'native',
                             'source_text': text, 'authorization': 'User requested regenerate audio'}, ensure_ascii=False) + '\n')
    print(json.dumps({'path': voice['path'], 'duration_s': duration, 'words': len(words), 'scene_map': scene_map}, ensure_ascii=False))

asyncio.run(main())
