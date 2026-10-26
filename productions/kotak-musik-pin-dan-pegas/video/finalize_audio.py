"""Keep native speech, place exact word timings, and freeze sourced cue assets."""
from pathlib import Path
import json,hashlib,subprocess,shutil,re,wave
import numpy as np
from scipy.ndimage import maximum_filter1d,uniform_filter1d
V=Path(__file__).resolve().parent;R=V.parents[2];P=V.parent
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def decode(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar','48000','-f','f32le','pipe:1']),dtype='<f4').astype(float)
def save(p,a):
    with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes(np.round(a*32767).astype('<i2').tobytes())
meta=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'));voice=meta['voices'][0];words=voice['words'];plan=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'))
expected=' '.join(s['text'] for s in plan).split();norm=lambda s:re.sub(r'\W','',s.lower())
assert [norm(w['text']) for w in words]==[norm(w) for w in expected], 'Alignment differs from locked script'
offset=.3;native=decode(V/voice['path']);assert len(native)/48000+offset<=90
run=subprocess.run(['ffmpeg','-hide_banner','-i',str(V/voice['path']),'-af','loudnorm=I=-16:TP=-2:LRA=9:print_format=json','-f','null','NUL'],capture_output=True,text=True,check=True)
levels=json.loads(re.findall(r'\{[^{}]+\}',run.stderr)[-1]);gain=10**((-16-float(levels['input_i']))/20)
peaks=maximum_filter1d(np.abs(native),size=961,mode='nearest');allowed=np.minimum(gain,10**(-2/20)/np.maximum(peaks,1e-9));envelope=np.minimum(allowed,uniform_filter1d(allowed,size=1921,mode='nearest'))
master=np.zeros(90*48000);start=round(offset*48000);master[start:start+len(native)]=native*envelope
(V/'assets/audio').mkdir(parents=True,exist_ok=True);save(V/'assets/audio/narration-master.wav',master)
dump(V/'normalization.json',dict(method='Sample-indexed gain and anticipatory peak cap; no tempo/filter delay',input_lufs=float(levels['input_i']),gain=gain,peak_cap_dbfs=-2,onset_samples=start,sample_rate=48000,duration_samples=len(master),source_samples=len(native)))
placed=[dict(w,start=round(w['start']+offset,6),end=round(min(w['end'],voice['duration_s'])+offset,6)) for w in words]
dump(V/'placed_audio.json',dict(source=voice['path'],source_sha256=sha(V/voice['path']),path='assets/audio/narration-master.wav',sha256=sha(V/'assets/audio/narration-master.wav'),offset=offset,tempo=1,words=placed,duration_s=90))
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
# Existing media-use library was examined first. Single-note gap resolved with documented CC BY recordings.
D=V/'assets/audio/sfx';D.mkdir(parents=True,exist_ok=True);assets=[]
origin=R/'productions/stapler-kaki-menutup/video/assets/audio/sfx'
old=json.loads((origin/'assets.json').read_text(encoding='utf-8'))
for ident,name in [('hinge','handle-contact.wav'),('metal','chain-contact.wav'),('editorial','editorial-click.mp3')]:
    a=next(a for a in old if a['id']==ident);assert sha(origin/name)==a['sha256'];shutil.copy2(origin/name,D/name)
    a={**a,'reuse_source':str((origin/name).relative_to(R)).replace('\\','/'),'episode_role':'Illustrative key/gear contact; editorial separation; not a recording of this music-box model'};assets.append(a)
for name in ['chair.request.json','clip-seat.request.json','BUNDLED_CREDITS.md']:shutil.copy2(origin/name,D/name)
retrieved=json.loads((D/'retrieved.json').read_text(encoding='utf-8'))
for n,a in enumerate(retrieved,1):
    source=V/a['path'];raw=decode(source);peak=maximum_filter1d(abs(raw),size=241);nz=np.where(peak>max(abs(raw))*.025)[0];trim=max(0,int(nz[0])-48)
    # Remove only leading silence, retain pitch and native decay. This is treatment of a recording, not synthesis.
    raw=raw[trim:];raw=raw*(10**(-13/20)/max(abs(raw)));out=D/f'note-{n}.wav';save(out,raw)
    assets.append(dict(id=f'note-{n}',path=out.relative_to(V).as_posix(),sha256=sha(out),duration_s=len(raw)/48000,source={**a['source'],'source_sha256':sha(source)},treatment=dict(trim_start_samples=trim,sample_rate=48000,peak_dbfs=-13,pitch_unchanged=True)))
dump(D/'assets.json',assets)
credits='# SFX credits\n\nSingle-note recordings from Music Box Samples by UbikPhonik, CC BY 4.0. Leading silence trimmed, gain adjusted; original pitches retained. Recordings are illustrative and come from a different music-box type.\n\n'
for a in retrieved:credits+=f'- [{a["source"]["title"]}]({a["source"]["url"]}) by UbikPhonik; [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).\n'
credits+='\nOther material cues reuse frozen historical project-generated ElevenLabs assets with original request receipts; editorial click is bundled Pixabay audio (see BUNDLED_CREDITS.md). No SFX were generated for this episode.\n'
(D/'CREDITS.md').write_text(credits,encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Narration and measured audio\nElevenLabs eleven_v4, project-env voice, one continuous request; native {voice["duration_s"]} seconds, {len(words)} exact aligned words. Placed at 0.3 seconds with native speech speed; peak-controlled gain and exact 90-second padding only. No synthesis retry. Captions and timing.json map all words to the locked script. SFX: reused material/editorial cues, plus three CC BY 4.0 real single-note music-box recordings by UbikPhonik; source credits included in publishing copy. BGM intentionally absent. Listening unavailable; objective evidence only, no phone-speaker or perceptual listening claimed.\n')
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));next(x for x in tracker['productions'] if x['slug']==P.name).update(stage='production',status='in_progress');dump(R/'TRACKER.json',tracker)
print(json.dumps(dict(native_seconds=voice['duration_s'],placed_seconds=90,words=len(placed),caption_groups=len(caps),scene_durations=[s['duration'] for s in plan],sfx_assets=len(assets))))
