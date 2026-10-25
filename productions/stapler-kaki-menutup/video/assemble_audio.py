"""Replace only the intermediate render's audio from the exact frozen clip plan."""
from pathlib import Path
import json,subprocess,hashlib,wave
import numpy as np
V=Path(__file__).resolve().parent;P=V.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def samples(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','48000','-ac','1','-f','f32le','pipe:1']),dtype='<f4').astype(float)
plan=json.loads((V/'sound_design.json').read_text());mix=samples(V/'assets/audio/narration-master.wav');assert len(mix)==90*48000
assets={x['id']:x for x in plan['assets']}
for cue in plan['cues']:
    source=samples(V/assets[cue['asset']]['path']);count=min(len(source),round(cue['duration']*48000));start=round(cue['start']*48000);mix[start:start+count]+=source[:count]*cue['volume']
assert max(abs(mix))<.98,'Unexpected summing peak'
master=V/'assets/audio/export-mix.wav'
with wave.open(str(master),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes(np.round(mix*32767).astype('<i2').tobytes())
video=P/'exports/stapler-kaki-menutup-v1.mp4';intermediate=P/'exports/stapler-kaki-menutup-picture-master.mp4'
assert video.is_file() and not intermediate.exists();video.rename(intermediate)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(intermediate),'-i',str(master),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t','90','-movflags','+faststart',str(video)],check=True)
def picture_hash(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','pipe:1']).decode().strip()
a,b=picture_hash(intermediate),picture_hash(video);assert a==b
report={'method':'Audio-only assembly from the exact narration and 19 top-level SFX clips; sample-indexed onsets and gains. HyperFrames picture stream copied without re-encoding.','picture_source':intermediate.relative_to(P).as_posix(),'picture_stream_hash':a,'picture_stream_identical':True,'audio_mix_sha256':sha(master),'sound_plan_sha256':sha(V/'sound_design.json'),'final_sha256':sha(video),'cues':len(plan['cues'])}
(V/'verification/audio-assembly.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
