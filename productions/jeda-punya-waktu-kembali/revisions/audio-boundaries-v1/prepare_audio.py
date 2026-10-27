from pathlib import Path
import hashlib,json,subprocess,wave
import numpy as np
B=Path(__file__).resolve().parent;V=B/'video';Q=V/'verification';Q.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
m=json.loads((V/'audio_meta.json').read_text());s=json.loads((V/'scenes.json').read_text());words=m['voices'][0]['words'];src=V/m['voices'][0]['path']
dest=V/'assets/audio';dest.mkdir(parents=True,exist_ok=True)
raw=dest/'narration-decoded.wav'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-ar','48000','-ac','1','-c:a','pcm_s16le',str(raw)],check=True)
with wave.open(str(raw),'rb') as f:rate=f.getframerate();pcm=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').copy()
pauses={1:.4,2:.4,4:.9,6:.6,7:.35,9:.45,10:.35,11:.6,12:.9,13:.35,14:.35,15:.35}
off=0;cuts=[]
for scene in s:
    off+=len(scene['vo'].split())
    if scene['n'] in pauses:
        a,b=words[off-1]['end'],words[off]['start'];cut=round((a+b)/2*rate)
        cuts.append(dict(after_scene=scene['n'],original_time=cut/rate,seconds=pauses[scene['n']],sample=cut))
segments=[];cursor=0
for c in cuts:segments.extend([pcm[cursor:c['sample']],np.zeros(round(c['seconds']*rate),dtype='<i2')]);cursor=c['sample']
segments.append(pcm[cursor:]);combined=np.concatenate(segments)
placed=dest/'narration-with-pauses.wav'
with wave.open(str(placed),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(combined.tobytes())
adjusted=[]
for word in words:
    adjusted.append({**word,'start':round(word['start']+sum(c['seconds'] for c in cuts if c['original_time']<=word['start']),4),'end':round(word['end']+sum(c['seconds'] for c in cuts if c['original_time']<word['end']),4)})
placement=dict(source=m['voices'][0]['path'],source_sha256=sha(src),path=placed.relative_to(V).as_posix(),sha256=sha(placed),original_duration_s=m['total_duration_s'],duration_s=len(combined)/rate,pauses=cuts,words=adjusted,reason='Six seconds of explicit silence inserted at inter-sentence gaps for the pause/return story; no speech speed change or paid resynthesis; original audio and native alignment retained.')
dump(V/'placement.json',placement)
mix=dest/'narration-mix.wav';filt='loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json'
p=subprocess.run(['ffmpeg','-hide_banner','-y','-i',str(placed),'-af',filt,'-ar','48000','-ac','1',str(mix)],capture_output=True,text=True,encoding='utf-8');(Q/'mix-processing.log').write_text(p.stderr,encoding='utf-8');p.check_returncode()
level=json.loads(p.stderr[p.stderr.rfind('{'):p.stderr.rfind('}')+1])
duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(mix)]))
assert abs(duration-placement['duration_s'])<.03
dump(V/'mix.json',dict(path=mix.relative_to(V).as_posix(),source=placement['path'],source_sha256=sha(placed),sha256=sha(mix),filter=filt,duration_s=duration,input_lufs=float(level['input_i']),input_true_peak_dbfs=float(level['input_tp']),reason='Measured speech level adjusted to speech-forward -18 LUFS target with -1.5 dBTP ceiling. No tonal diagnosis; original source and alignment retained.',listening='Perceptual listening unavailable. Decode, level, waveform and timing checks only.'))
print(json.dumps(dict(original=m['total_duration_s'],placed=duration,inserted_s=sum(pauses.values()),measured_lufs=level['input_i'],measured_peak=level['input_tp'])))
