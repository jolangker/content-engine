"""Insert measured reading pauses between ideas without changing the spoken samples."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import wave

P = Path(__file__).resolve().parent
V = P / 'video'
meta = json.loads((V / 'audio_meta.json').read_text(encoding='utf-8'))
source_meta_path = V / 'narration_source_meta.json'
if meta.get('pacing'):
    source = json.loads(source_meta_path.read_text(encoding='utf-8'))
    if source['request_sha256'] != meta['request_sha256']:
        raise SystemExit('Source identity changed; run the narration entry point before pacing')
else:
    source = copy.deepcopy(meta)
    source_meta_path.write_text(json.dumps(source, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

scenes = json.loads((P / 'scenes.json').read_text(encoding='utf-8'))
words = source['voices'][0]['words']
pauses = [.45, .45, .70, .65, .65, .70, .75, .55, .70, .65, .70, .75, .90]
assert len(pauses) == len(scenes) - 1
boundaries = []
offset = 0
for scene, pause in zip(scenes[:-1], pauses):
    offset += len(scene['vo'].split())
    split = (words[offset - 1]['end'] + words[offset]['start']) / 2
    boundaries.append({'word_index': offset, 'split_s': split, 'pause_s': pause})
audio_source = V / source['voices'][0]['path']
signature = hashlib.sha256(json.dumps({'request': source['request_sha256'], 'source_sha256': hashlib.sha256(audio_source.read_bytes()).hexdigest(),
                                      'boundaries': boundaries}, sort_keys=True).encode()).hexdigest()
out = audio_source.parent / f'narration-paced-{signature[:20]}.wav'
if not out.exists():
    decoded = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(audio_source), '-f', 's16le', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '1', '-'],
                             capture_output=True, check=True).stdout
    cursor, chunks = 0, []
    for boundary in boundaries:
        position = round(boundary['split_s'] * 44100) * 2
        chunks.extend([decoded[cursor:position], bytes(round(boundary['pause_s'] * 44100) * 2)])
        cursor = position
    chunks.append(decoded[cursor:])
    with wave.open(str(out), 'wb') as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(44100)
        handle.writeframes(b''.join(chunks))
with wave.open(str(out), 'rb') as handle:
    duration = handle.getnframes() / handle.getframerate()
derived = copy.deepcopy(source)
for index, word in enumerate(derived['voices'][0]['words']):
    shift = sum(item['pause_s'] for item in boundaries if index >= item['word_index'])
    word['start'] += shift
    word['end'] += shift
derived['voices'][0].update(path=out.relative_to(V).as_posix(), duration_s=duration, source_path=source['voices'][0]['path'])
derived['total_duration_s'] = duration
derived['pacing'] = {'method': 'insert_silence_between_ideas', 'source_duration_s': source['total_duration_s'],
                     'added_silence_s': sum(pauses), 'boundaries': boundaries, 'signature': signature,
                     'audio_sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'speech_rate_changed': False}
(V / 'audio_meta.json').write_text(json.dumps(derived, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'voice': source['voice_id'], 'source_duration_s': source['total_duration_s'], 'paced_duration_s': duration,
                  'added_silence_s': sum(pauses), 'words': len(words), 'speech_rate_changed': False}))
