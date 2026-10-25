from pathlib import Path
import json,subprocess,hashlib
V=Path(__file__).resolve().parent/'video'
m=json.loads((V/'audio_meta.json').read_text(encoding='utf-8')); src=V/m['voices'][0]['path']
dest=V/'assets/audio/narration-mix.wav';dest.parent.mkdir(parents=True,exist_ok=True)
filt='loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json'
p=subprocess.run(['ffmpeg','-hide_banner','-y','-i',str(src),'-af',filt,'-ar','48000','-ac','1',str(dest)],capture_output=True,text=True,encoding='utf-8')
(V/'verification/mix-processing.log').write_text(p.stderr,encoding='utf-8');p.check_returncode()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(dest)]))
assert abs(duration-m['total_duration_s'])<.03
record=dict(path=dest.relative_to(V).as_posix(),source=src.relative_to(V).as_posix(),source_sha256=sha(src),sha256=sha(dest),filter=filt,duration_s=duration,reason='Native narration measured -25.21 LUFS / -5.17 dBTP; prepare a speech-forward mix at -18 LUFS with a -1.5 dBTP ceiling. Original generation and alignment remain unchanged.',listening='not available; measured level correction only, no tonal diagnosis')
(V/'mix.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record))
