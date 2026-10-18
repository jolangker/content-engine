"""One full-script ElevenLabs synthesis with native alignment and no retries."""
from pathlib import Path
import base64, hashlib, json, os, re, subprocess
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT.parents[2] / '.env')
OUT = ROOT / 'assets/voice/narration-v3-elevenlabs'
OUT.mkdir(parents=True, exist_ok=True)

def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def norm(text):
    return ''.join(re.findall(r'\w+', text.lower()))

voice = os.environ['ELEVENLABS_VOICE_ID']
script = (ROOT.parent / 'SCRIPT.md').read_text(encoding='utf-8')
text = script.split('## Narasi utuh', 1)[1].split('## Pembagian beat', 1)[0].strip()
frames = json.loads((ROOT / 'boards/frame-manifest.json').read_text(encoding='utf-8'))
assert norm(text) == norm(' '.join(f['vo'] for f in frames))
mp3 = OUT / 'narration-elevenlabs-full.mp3'
assert not mp3.exists(), 'Existing take must be inspected before any new synthesis'
request = {'provider': 'elevenlabs', 'voice': voice, 'tts_model': 'eleven_multilingual_v2',
           'lang': 'id', 'speed': 1.0, 'lines': [{'id': 'narration', 'text': text}], 'bgm': {'mode': 'none'}}
save('audio_request.json', request)
client = ElevenLabs(api_key=os.environ['ELEVENLABS_API_KEY'], timeout=180)
response = client.text_to_speech.convert_with_timestamps(
    voice_id=voice, text=text, model_id=request['tts_model'], output_format='mp3_44100_128',
    request_options={'max_retries': 0})
mp3.write_bytes(base64.b64decode(response.audio_base_64))
alignments = {k: getattr(response, k).model_dump() if getattr(response, k) else None
              for k in ('normalized_alignment', 'alignment')}
save('native-alignment.json', alignments)
a = alignments['normalized_alignment'] or alignments['alignment']
assert a, 'Audio preserved, native alignment missing'
chars = a['characters']; starts = a['character_start_times_seconds']; ends = a['character_end_times_seconds']
assert len(chars) == len(starts) == len(ends)
words, current = [], None
for char, start, end in zip(chars, starts, ends):
    if char.isspace():
        if current:
            words.append(current); current = None
    else:
        if current is None:
            current = {'id': f'w{len(words)}', 'text': '', 'start': start, 'end': end}
        current['text'] += char; current['end'] = end
if current: words.append(current)
save('narration-elevenlabs-full.words.json', words)
probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(mp3)], text=True))
duration = float(probe['format']['duration'])
assert norm(' '.join(w['text'] for w in words)) == norm(text)
assert all(0 <= w['start'] < w['end'] <= duration + .1 for w in words)
assert all(a['end'] <= b['start'] + .001 for a,b in zip(words, words[1:]))
subprocess.run(['ffmpeg', '-v', 'error', '-i', str(mp3), '-f', 'null', '-'], check=True, capture_output=True)
scene_map, cursor = [], 0
for frame in frames:
    start, combined, target = cursor, '', norm(frame['vo'])
    while cursor < len(words) and len(combined) < len(target):
        combined += norm(words[cursor]['text']); cursor += 1
    assert combined == target
    scene_map.append({'frame': frame['n'], 'word_start': start, 'word_end_exclusive': cursor,
                      'speech_start_s': words[start]['start'], 'speech_end_s': words[cursor-1]['end']})
assert cursor == len(words)
for i, scene in enumerate(scene_map):
    scene['scene_start_s'] = 0 if i == 0 else scene['speech_start_s']
    scene['scene_end_s'] = scene_map[i+1]['speech_start_s'] if i+1 < len(scene_map) else duration
path = mp3.relative_to(ROOT).as_posix()
meta = {'version': 3, 'tts_provider': 'elevenlabs', 'voice_id': voice, 'tts_model': request['tts_model'],
        'voices': [{'id': 'narration', 'path': path, 'duration_s': duration, 'words': words, 'text': text}],
        'sfx': [], 'bgm': None, 'total_duration_s': duration, 'scene_map': scene_map,
        'composition_sync': 'pending; v1 preview/export retains previous audio'}
save('audio_meta.json', meta)
save('verification.json', {'provider': 'elevenlabs', 'voice_id': voice, 'model': request['tts_model'],
                         'synthesis_calls': 1, 'duration_s': duration, 'word_count': len(words),
                         'normalized_text_match': True, 'monotonic_word_timestamps': True,
                         'ffmpeg_full_decode': 'passed', 'sha256': hashlib.sha256(mp3.read_bytes()).hexdigest()})
with (ROOT / '.media/manifest.jsonl').open('a', encoding='utf-8') as fp:
    fp.write(json.dumps({'type': 'voice', 'path': path, 'provider': 'elevenlabs', 'voice': voice,
                         'model': request['tts_model'], 'duration_s': duration,
                         'authorization': 'User explicitly requested ElevenLabs', 'word_timestamps': 'native'}, ensure_ascii=False) + '\n')
print(json.dumps({'path': path, 'duration_s': duration, 'words': len(words), 'scene_map': scene_map}))
