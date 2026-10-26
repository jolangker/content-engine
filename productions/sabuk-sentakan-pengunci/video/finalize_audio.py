"""Place native narration, exact captions and reused source-verified material cues."""
from pathlib import Path
import json,hashlib,subprocess,re,wave,shutil
import numpy as np
from scipy.ndimage import maximum_filter1d,uniform_filter1d
V=Path(__file__).resolve().parent;R=V.parents[2];P=V.parent
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
meta=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'));voice=meta['voices'][0];words=voice['words'];plan=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'))
norm=lambda s:re.sub(r'\W','',s.lower())
expected=' '.join(s['text'] for s in plan).split()
assert [norm(w['text']) for w in words]==[norm(w) for w in expected], 'Native alignment differs from locked script'
offset=.3;tempo=1.08
native=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(V/voice['path']),'-af',f'atempo={tempo}','-ac','1','-ar','48000','-f','f32le','pipe:1']),dtype='<f4').astype(float)
assert len(native)/48000+offset<90, 'Treated speech exceeds the board duration; preserve recording for timing resolution'
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(V/voice['path']),'-af','loudnorm=I=-16:TP=-2:LRA=9:print_format=json','-f','null','NUL'],capture_output=True,text=True,check=True)
levels=json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1]);gain=10**((-16-float(levels['input_i']))/20)
peaks=maximum_filter1d(np.abs(native),size=961,mode='nearest');allowed=np.minimum(gain,10**(-2/20)/np.maximum(peaks,1e-9));envelope=np.minimum(allowed,uniform_filter1d(allowed,size=1921,mode='nearest'))
master=np.zeros(90*48000);start=round(offset*48000);master[start:start+len(native)]=native*envelope
out=V/'assets/audio/narration-master.wav';out.parent.mkdir(parents=True,exist_ok=True)
with wave.open(str(out),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes(np.round(master*32767).astype('<i2').tobytes())
dump(V/'normalization.json',dict(method='Pitch-preserving FFmpeg atempo=1.08, then sample-indexed gain and anticipatory peak cap',input_lufs=float(levels['input_i']),gain=gain,peak_cap_dbfs=-2,onset_samples=start,sample_rate=48000,duration_samples=len(master),treated_samples=len(native),tempo=tempo,source_preserved=True))
placed=[dict(w,start=round(w['start']/tempo+offset,6),end=round(min(w['end'],voice['duration_s'])/tempo+offset,6)) for w in words]
dump(V/'placed_audio.json',dict(source=voice['path'],source_sha256=sha(V/voice['path']),path='assets/audio/narration-master.wav',sha256=sha(out),offset=offset,tempo=tempo,words=placed,duration_s=90,alignment='Native timestamps divided by the pitch-preserving constant tempo factor; not independently re-transcribed.'))
count=0
for n,s in enumerate(plan):
    size=len(s['text'].split());s['first_word_index']=count;s['last_word_index']=count+size-1;s['start']=0 if n==0 else max(0,placed[count]['start']-.1);count+=size
for n,s in enumerate(plan):s['end']=plan[n+1]['start'] if n+1<len(plan) else 90;s['duration']=round(s['end']-s['start'],6)
dump(V/'timing.json',plan)
groups=[];buf=[]
for w in placed:
    if buf and (len(buf)>=4 or len(' '.join(x['text'] for x in buf+[w]))>36 or w['start']-buf[-1]['end']>.18):groups.append(buf);buf=[]
    buf.append(w)
    if re.search(r'[.?!]$',w['text']):groups.append(buf);buf=[]
if buf:groups.append(buf)
caps=[]
for n,g in enumerate(groups):
    end=min(groups[n+1][0]['start'] if n+1<len(groups) else 89.8,g[-1]['end']+.13)
    caps.append(dict(start=g[0]['start'],end=end,text=' '.join(w['text'] for w in g)))
dump(V/'caption-groups.json',caps)
def stamp(t,sep=','):
    x=round(t*1000);return f'{x//3600000:02}:{x//60000%60:02}:{x//1000%60:02}{sep}{x%1000:03}'
E=P/'exports';E.mkdir(exist_ok=True)
(E/(P.name+'-v1.srt')).write_text('\n'.join(f'{n+1}\n{stamp(g["start"])} --> {stamp(g["end"])}\n{g["text"]}\n' for n,g in enumerate(caps)),encoding='utf-8')
(E/(P.name+'-v1.vtt')).write_text('WEBVTT\n\n'+'\n'.join(f'{stamp(g["start"],".")} --> {stamp(g["end"],".")}\n{g["text"]}\n' for g in caps),encoding='utf-8')
# Bundled library inspected first: editorial click fits; material contact/travel
# gaps use existing frozen production cues, with no generation or new treatment.
D=V/'assets/audio/sfx';D.mkdir(parents=True,exist_ok=True);origin=R/'productions/stapler-kaki-menutup/video/assets/audio/sfx'
old=json.loads((origin/'assets.json').read_text(encoding='utf-8'));assets=[]
for ident,name in [('hinge','handle-contact.wav'),('metal','chain-contact.wav'),('editorial','editorial-click.mp3')]:
    a=next(x for x in old if x['id']==ident);assert sha(origin/name)==a['sha256'];shutil.copy2(origin/name,D/name)
    assets.append({**a,'reuse_source':(origin/name).relative_to(R).as_posix(),'episode_role':'Illustrative belt/gear/contact material cue; editorial inspection click. Not a recording of this retractor.'})
for name in ['chair.request.json','clip-seat.request.json','BUNDLED_CREDITS.md']:
    if (origin/name).exists():shutil.copy2(origin/name,D/name)
dump(D/'assets.json',assets)
(D/'CREDITS.md').write_text('# Sound provenance\n\nBundled Pixabay editorial click (see BUNDLED_CREDITS.md); material travel/contact reuse frozen historical project-generated ElevenLabs assets with original request provenance in assets.json and retained request receipts. No SFX generated for this episode. These are stylized illustrative cues, not measured recordings of this seatbelt mechanism. No music.\n',encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Measured audio\nElevenLabs eleven_v4, project-env voice, one continuous synthesis. Native {voice["duration_s"]}s; {len(words)} exact aligned words. The native recording exceeds the 90s board duration. Under routine delegated timing decisions, apply pitch-preserving atempo={tempo} to a derived copy only; original recording/cache remains intact. Treated speech {len(native)/48000:.3f}s, onset 0.3s, sample-indexed gain/peak control, padded to 90s. No resynthesis/retry. Captions/SRT/VTT follow native alignment divided by the constant tempo factor; not independently re-transcribed, so microalignment remains a review limit. First discovery starts {plan[1]["start"]:.3f}s. SFX: three source-verified frozen material/editorial cues; no generation. BGM intentionally absent. Auditory/phone-speaker listening unavailable; numerical evidence only.\n')
print(json.dumps(dict(native_seconds=voice['duration_s'],words=len(words),caption_groups=len(caps),scene_durations=[s['duration'] for s in plan])))
