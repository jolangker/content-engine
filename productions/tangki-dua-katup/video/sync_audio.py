from pathlib import Path
import json,re,subprocess,hashlib,wave
import numpy as np
V=Path(__file__).resolve().parent
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(x):return re.sub(r'[^\w]','',x.lower())
meta=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'));voice=meta['voices'][0];words=voice['words'];plan=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'))
expected=[norm(w) for s in plan for w in s['vo'].split()]
assert expected==[norm(w['text']) for w in words], 'Native alignment text must match script before timing is used'
source=V/voice['path'];rate=48000
raw=subprocess.run(['ffmpeg','-v','error','-i',str(source),'-ac','1','-ar',str(rate),'-f','f32le','pipe:1'],capture_output=True,check=True).stdout
samples=np.frombuffer(raw,dtype='<f4').copy();native_duration=len(samples)/rate
# Split inside existing inter-sentence silence, then add clearly recorded
# observation gaps. Speech itself remains at native speed and pitch.
cuts=[0.0];wordcuts=[0];n=0
for s in plan[:-1]:
 n+=len(s['vo'].split());wordcuts.append(n);cuts.append((words[n-1]['end']+words[n]['start'])/2)
cuts.append(native_duration);wordcuts.append(len(words))
target=89.2;extra=target-native_duration
assert extra>=0,'Narration exceeds target; do not silently speed it'
weights=[.45,.3,.35,.55,.95,.65,.85,.75,.4,1.1,.7,.95,.5,.45,1.5,.65]
gaps=[extra*w/sum(weights) for w in weights]
segments=[];updated=[];timing=[];cursor=0
for i,s in enumerate(plan):
 start_idx=round(cuts[i]*rate);end_idx=round(cuts[i+1]*rate)
 seg=samples[start_idx:end_idx];gap=np.zeros(round(gaps[i]*rate),dtype=np.float32)
 segments.extend([seg,gap]);local_start=cursor
 for w in words[wordcuts[i]:wordcuts[i+1]]:
  z=dict(w);z['start']=round(w['start']-cuts[i]+local_start+.3,6);z['end']=round(w['end']-cuts[i]+local_start+.3,6);updated.append(z)
 cursor+=(len(seg)+len(gap))/rate
 a=0 if i==0 else local_start+.3
 b=90 if i==15 else cursor+.3
 timing.append(dict(s,start=round(a,6),end=round(b,6),duration=round(b-a,6),poster=round(a+(b-a)*.62,6),word_range=[wordcuts[i],wordcuts[i+1]],observation_gap_s=round(len(gap)/rate,6)))
out=np.concatenate(segments);audio_dir=V/'assets/audio';audio_dir.mkdir(parents=True,exist_ok=True)
native=audio_dir/'narration-observation.wav'
with wave.open(str(native),'wb') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes())
master=audio_dir/'narration-master.wav'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(native),'-af','loudnorm=I=-16:TP=-1.5:LRA=9','-ar',str(rate),'-ac','1',str(master)],check=True)
dump(V/'timing.json',timing);dump(V/'placed_audio.json',dict(path='assets/audio/narration-master.wav',offset=.3,duration=round(cursor,6),source_path=voice['path'],source_sha256=digest(source),sha256=digest(master),source_duration=native_duration,tempo=1,observation_gaps_s=gaps,words=updated))
groups=[]
for s in timing:
 ws=updated[s['word_range'][0]:s['word_range'][1]];chunk=[]
 for j,w in enumerate(ws):
  chunk.append(w)
  if len(' '.join(x['text'] for x in chunk))>=72 or re.search(r'[.!?]$',w['text']) or j==len(ws)-1:
    groups.append(dict(text=' '.join(x['text'] for x in chunk),start=chunk[0]['start'],end=min(s['end']-.02,chunk[-1]['end']+.1),scene=s['id']));chunk=[]
for i,g in enumerate(groups):
 s=next(s for s in timing if s['id']==g['scene'])
 limit=min(s['end']-.03,groups[i+1]['start']-.03 if i+1<len(groups) else 89.8)
 g['end']=max(g['end'],min(limit,g['start']+.5+.3*len(g['text'].split())))
dump(V/'caption_groups.json',groups)
ex=V.parent/'exports';ex.mkdir(exist_ok=True)
def stamp(t,sep=','):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02}{sep}{ms:03}'
(ex/'tangki-dua-katup.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(g["start"])} --> {stamp(g["end"])}\n{g["text"]}' for i,g in enumerate(groups))+'\n',encoding='utf-8')
(ex/'tangki-dua-katup.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{stamp(g["start"],".")} --> {stamp(g["end"],".")}\n{g["text"]}' for g in groups)+'\n',encoding='utf-8')
print(json.dumps({'native_duration':native_duration,'placed_duration':cursor,'tempo':1,'added_observation_s':sum(gaps),'words':len(updated),'captions':len(groups),'scene_durations':[round(s['duration'],2) for s in timing]}))
