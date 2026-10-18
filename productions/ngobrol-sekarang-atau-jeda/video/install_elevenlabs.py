"""Install the verified full ElevenLabs take without another synthesis call."""
from pathlib import Path
import json, re, subprocess, sys

root = Path(__file__).resolve().parent
source = root / 'assets/voice/narration-v3-elevenlabs/audio_meta.json'
audio = json.loads(source.read_text(encoding='utf-8'))
assert audio['tts_provider'] == 'elevenlabs' and len(audio['voices']) == 1
voice = audio['voices'][0]
frames = json.loads((root / 'boards/frame-manifest.json').read_text(encoding='utf-8'))
audio['audio_duration_s'] = voice['duration_s']
audio['total_duration_s'] = round(voice['duration_s'] + 1.0, 6)
audio['continuous_narration'] = True
audio['composition_sync'] = 'installed; scene cues and captions use native alignment'
audio['source_metadata'] = source.relative_to(root).as_posix()
for frame, scene in zip(frames, audio['scene_map']):
    assert frame['n'] == scene['frame']
    start = scene['scene_start_s']
    end = scene['scene_end_s'] if frame['n'] < len(frames) else audio['total_duration_s']
    words = voice['words'][scene['word_start']:scene['word_end_exclusive']]
    frame.update(start=start, duration=round(end-start, 6), voice_offset=0,
                 voice_duration=round(scene['speech_end_s']-start,6), audio=voice['path'],
                 words=[dict(w, start=round(w['start']-start,6), end=round(w['end']-start,6)) for w in words])
    frame['poster'] = round(end-.7,3)
def save(name, data):
    (root/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save('audio_meta.json', audio)
save('timing.json',frames)
motion=json.loads((root/'index.motion.json').read_text(encoding='utf-8'))
motion['duration']=audio['total_duration_s']
save('index.motion.json',motion)
brief=(root/'BRIEF.md').read_text(encoding='utf-8')
brief=re.sub(r'^length: .*$',f"length: {audio['total_duration_s']}s",brief,flags=re.M)
brief=re.sub(r'^voice: .*$',f"voice: {audio['voice_id']}",brief,flags=re.M)
brief=re.sub(r'^voice_provider: .*$',"voice_provider: elevenlabs",brief,flags=re.M)
brief+='\n\n## Audio revision v3 — installed\n\nPengguna meminta ElevenLabs lalu “gas pasang”. George mengikuti konfigurasi proyek; model eleven_multilingual_v2, satu full-script synthesis. Narasi 59.118005 detik, dengan tahan penutup 1 detik. Satu track kontinu; scene, motion dan caption mengikuti alignment native. Preview baru perlu ditinjau sebelum ekspor. Keputusan Ardi dalam riwayat v1 tidak berlaku untuk audio terkini.\n'
(root/'BRIEF.md').write_text(brief,encoding='utf-8')
script=(root/'SCRIPT.md').read_text(encoding='utf-8')
script=re.sub(r'^\*\*Voice:\*\* .*$',f"**Voice:** ElevenLabs / George / {audio['voice_id']} — pilihan provider terbaru pengguna.",script,flags=re.M)
script=re.sub(r'^\*\*Voice settings:\*\* .*$',"**Voice settings:** eleven_multilingual_v2; speed default 1.0; satu narasi utuh, alignment native.",script,flags=re.M)
(root/'SCRIPT.md').write_text(script,encoding='utf-8')
subprocess.run([sys.executable,str(root/'animate_project.py')],check=True)
print('Installed one continuous ElevenLabs narration; duration:',audio['total_duration_s'])
