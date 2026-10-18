import os, re, json, base64, subprocess
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[2]
load_dotenv(PROJECT_ROOT / '.env')

OUT = ROOT / 'assets/voice/narration'
OUT.mkdir(parents=True, exist_ok=True)

def save(name, val):
    (OUT / name).write_text(json.dumps(val, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def norm(t):
    return ''.join(re.findall(r'\w+', t.lower()))

script_text = (ROOT.parent / 'SCRIPT.md').read_text(encoding='utf-8')
full_narration = script_text.split('## Narasi Utuh', 1)[1].split('## Pembagian Beat', 1)[0].strip()

# Bersihkan heading atau markdown dari narasi
clean_lines = []
for line in full_narration.split('\n'):
    l = line.strip()
    if not l or l.startswith('#') or l.startswith('---'):
        continue
    clean_lines.append(l)
narration_clean = ' '.join(clean_lines)

print("Target narration length:", len(narration_clean.split()), "words")

voice_id = os.environ.get('ELEVENLABS_VOICE_ID', 'JBFqnCBsd6RMkjVDRZzb') # default George / warm voice
api_key = os.environ.get('ELEVENLABS_API_KEY')

if not api_key:
    print("ERROR: ELEVENLABS_API_KEY not found in environment.")
    exit(1)

client = ElevenLabs(api_key=api_key, timeout=180)
print(f"Calling ElevenLabs API (model: eleven_multilingual_v2, voice: {voice_id})...")

response = client.text_to_speech.convert_with_timestamps(
    voice_id=voice_id,
    text=narration_clean,
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
    request_options={"max_retries": 0}
)

mp3_path = OUT / 'narration-full.mp3'
mp3_path.write_bytes(base64.b64decode(response.audio_base_64))

alignments = {
    k: getattr(response, k).model_dump() if getattr(response, k) else None
    for k in ('normalized_alignment', 'alignment')
}
save('native-alignment.json', alignments)

a = alignments['normalized_alignment'] or alignments['alignment']
assert a, "Native alignment missing"

chars = a['characters']
starts = a['character_start_times_seconds']
ends = a['character_end_times_seconds']

words, current = [], None
for char, start, end in zip(chars, starts, ends):
    if char.isspace():
        if current:
            words.append(current)
            current = None
    else:
        if current is None:
            current = {'id': f'w{len(words)}', 'text': '', 'start': start, 'end': end}
        current['text'] += char
        current['end'] = end
if current:
    words.append(current)

save('narration-full.words.json', words)

# Probe duration with ffprobe
probe = json.loads(subprocess.check_output([
    'ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(mp3_path)
], text=True))
duration = float(probe['format']['duration'])
print(f"Audio generated successfully! Total duration: {duration:.2f}s, words: {len(words)}")

# Save audio_meta.json
meta = {
    'version': 1,
    'tts_provider': 'elevenlabs',
    'voice_id': voice_id,
    'tts_model': 'eleven_multilingual_v2',
    'total_duration_s': round(duration + 1.0, 3), # +1s ending pause
    'audio_duration_s': round(duration, 3),
    'audio_path': mp3_path.relative_to(ROOT).as_posix(),
    'words_path': (OUT / 'narration-full.words.json').relative_to(ROOT).as_posix()
}
save('audio_meta.json', meta)
(ROOT / 'audio_meta.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
