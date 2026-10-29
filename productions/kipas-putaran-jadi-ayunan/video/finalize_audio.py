"""Place one preserved recording on acoustic scene/frame anchors, then normalize."""
from pathlib import Path
import json,hashlib,subprocess,re,sys,shutil
import numpy as np
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'))
import audio_boundaries as a
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
plan=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'));meta=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'));voice=meta['voices'][0];words=voice['words']
norm=lambda s:re.sub(r'\W','',s.lower())
expected=' '.join(s['text'] for s in plan).split()
assert [norm(w['text']) for w in words]==[norm(w) for w in expected], 'Provider alignment differs from locked script'
source=a.decode(V/voice['path']);native_duration=len(source)/a.RATE
tempo=1 if native_duration<=84 else native_duration/83
master=source
if tempo!=1:
 master=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(V/voice['path']),'-af',f'atempo={tempo:.12f}','-ac','1','-ar','48000','-f','f32le','pipe:1']),dtype='<f4').copy()
 words=[dict(w,start=w['start']/tempo,end=w['end']/tempo) for w in words]
pre=.25;tail=.5;budget=90-len(master)/a.RATE-pre-tail
assert budget>15*.19, 'Insufficient observation time; retain completed source for recovery'
weights=[1,1,1,1,1.3,1.4,1.4,1,1,1,1.4,1.2,1,1,1.3]
pauses=[budget*x/sum(weights) for x in weights]
ends=[];count=0
for s in plan:count+=len(s['text'].split());ends.append(count)
placed,moved,boundaries,utterances=a.place(master,words,ends,pauses,pre)
assert len(placed)<=90*a.RATE
placed=np.pad(placed,(0,90*a.RATE-len(placed)))
starts=[0]+[b['visual_s'] for b in boundaries];finish=starts[1:]+[90]
scenes=[dict(s,**u,start=start,end=end,duration=end-start,start_frame=round(start*30),end_frame=round(end*30)) for s,u,start,end in zip(plan,utterances,starts,finish)]
timing=dict(duration_s=90,voice_duration_s=native_duration,tempo=tempo,words=moved,scenes=scenes,basis='Native recording retained; pitch-preserving derived treatment only when needed; acoustic quiet splices then one normalization. Integer30fps cuts. Individual word timing remains estimated.')
dump(V/'timing.json',timing)
before=V/'assets/audio/narration-before-level.wav';dest=V/'assets/audio/narration-master.wav'
a.write_pcm(before,placed);normalization=a.normalize_after_placement(before,dest)
receipt=dict(version=2,path='assets/audio/narration-master.wav',sha256=a.digest(dest),source=voice['path'],source_sha256=a.digest(V/voice['path']),duration_s=90,duration=90,pre_roll_s=pre,speech_speed=tempo,native_recording_preserved=True,speech_samples_preserved_before_normalization=(tempo==1),derived_master_samples_preserved_before_normalization=True,normalization=normalization,timestamp_precision='Acoustic scene anchors; word times remain estimates.',sample_rate=48000,fps=30,timing_sha256=a.digest(V/'timing.json'),boundaries=boundaries)
dump(V/'audio_boundaries.json',receipt);dump(V/'placed_audio.json',dict(**receipt,words=moved))
caps=[]
for s in scenes:
 buf=[]
 for w in moved[s['word_start']:s['word_end']]:
  if buf and (len(buf)>=4 or len(' '.join(x['text'] for x in buf+[w]))>34 or w['start']-buf[-1]['end']>.16):
   caps.append(dict(start=buf[0]['start'],end=min(s['end'],buf[-1]['end']+.1),text=' '.join(x['text'] for x in buf)));buf=[]
  buf.append(w)
  if re.search(r'[.?!]$',w['text']):caps.append(dict(start=buf[0]['start'],end=min(s['end'],buf[-1]['end']+.1),text=' '.join(x['text'] for x in buf)));buf=[]
 if buf:caps.append(dict(start=buf[0]['start'],end=min(s['end'],buf[-1]['end']+.1),text=' '.join(x['text'] for x in buf)))
for g,nxt in zip(caps,caps[1:]):g['end']=min(g['end'],nxt['start'])
dump(V/'caption-groups.json',caps)
def stamp(t,sep=','):
 x=round(t*1000);return f'{x//3600000:02}:{x//60000%60:02}:{x//1000%60:02}{sep}{x%1000:03}'
for ext,sep in [('srt',','),('vtt','.')]:
 body='\n\n'.join(f'{n+1}\n{stamp(g["start"],sep)} --> {stamp(g["end"],sep)}\n{g["text"]}' for n,g in enumerate(caps))+'\n'
 out=P/'exports'/f'{P.name}-v1.{ext}';out.parent.mkdir(exist_ok=True);out.write_text(('WEBVTT\n\n' if ext=='vtt' else '')+body,encoding='utf-8')
D=V/'assets/audio/sfx';D.mkdir(parents=True,exist_ok=True);origin=R/'productions/stapler-kaki-menutup/video/assets/audio/sfx'
old=json.loads((origin/'assets.json').read_text(encoding='utf-8'));assets=[]
for ident,name in [('hinge','handle-contact.wav'),('metal','chain-contact.wav'),('editorial','editorial-click.mp3')]:
 item=next(x for x in old if x['id']==ident);assert a.digest(origin/name)==item['sha256'];shutil.copy2(origin/name,D/name)
 assets.append(dict(item,reuse_source=(origin/name).relative_to(R).as_posix(),episode_role='Stylized fan linkage travel or metal contact; editorial inspection cue. Not a literal recording of this mechanism.'))
for name in ['chair.request.json','clip-seat.request.json','BUNDLED_CREDITS.md']:
 if (origin/name).exists():shutil.copy2(origin/name,D/name)
dump(D/'assets.json',assets)
(D/'CREDITS.md').write_text('# Sound provenance\n\nBundled Pixabay editorial click (license-summary in assets.json); historical project-generated ElevenLabs material cues reused byte-for-byte with original request provenance in assets.json. No new SFX generation or treatment. Foley illustrates contacts and travel; it is not a recording of a commercial fan. Music intentionally absent.\n',encoding='utf-8')
story=(V/'STORYBOARD.md').read_text(encoding='utf-8')
story+='\n## Measured scene windows\n\nStatic board above retains pre-audio estimates. Canonical animation follows these integer-frame acoustic anchors.\n\n| Scene | Start | End | First spoken word | Last spoken word |\n| --- | --- | --- | --- | --- |\n'
story+='\n'.join(f'| {s["id"]} | {s["start"]:.6f} | {s["end"]:.6f} | {s["speech_start"]:.6f} | {s["speech_end"]:.6f} |' for s in scenes)+'\n'
(V/'STORYBOARD.md').write_text(story,encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Audio placement\nOne ElevenLabs eleven_v4 synthesis, root-env voice, native{native_duration:.3f}s, {len(words)} words. Original cache preserved. Derived pitch-preserving tempo={tempo:.8f} chosen only if native recording leaves insufficient observation time. Source at native tempo is retained. Every derived-master sample preserved across verified quiet splices; one final normalization targets-16LUFS/-2dBTP.15 verified acoustic cuts, integer30fps map; final master90s. Individual word timings are estimates reanchored to utterances, not independent forced alignment. {len(caps)} short caption groups. Existing media-use manifest inspected before frozen material cue reuse. Music absent intentionally. Listening unavailable; no auditory or phone-speaker approval claimed.\n')
print(json.dumps(dict(native_seconds=native_duration,tempo=tempo,boundaries=len(boundaries),words=len(words),captions=len(caps),scene_seconds=[round(s['duration'],3) for s in scenes])))
