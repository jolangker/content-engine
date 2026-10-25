from pathlib import Path
import json,hashlib,subprocess,shutil,re,html,wave
import numpy as np
from scipy.ndimage import maximum_filter1d, uniform_filter1d
V=Path(__file__).resolve().parent;R=V.parents[2]
def js(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
meta=json.loads((V/'audio_meta.json').read_text(encoding='utf-8'));voice=meta['voices'][0]
words=voice['words'];plan=json.loads((V/'scene-plan.json').read_text())
assert len(words)==sum(len(s['text'].split()) for s in plan)
def norm(s):return re.sub(r'\W','',s.lower())
expected=' '.join(s['text'] for s in plan).split()
assert [norm(w['text']) for w in words]==[norm(w) for w in expected], 'Alignment words differ from locked script'
offset=.45
# Native speech retained; loudness normalization and edge padding only, no tempo change.
(V/'assets/audio').mkdir(parents=True,exist_ok=True)
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(V/voice['path']),'-ac','1','-ar','48000','-f','f32le','pipe:1'])
native=np.frombuffer(raw,dtype='<f4').astype(float)
level_run=subprocess.run(['ffmpeg','-hide_banner','-i',str(V/voice['path']),'-af','loudnorm=I=-16:TP=-2:LRA=9:print_format=json','-f','null','NUL'],capture_output=True,text=True,check=True)
levels=json.loads(re.findall(r'\{[^{}]+\}',level_run.stderr)[-1])
gain=10**((-16-float(levels['input_i']))/20)
# Offline anticipatory peak control changes gain only, never sample positions.
# 10 ms neighbourhood protection, 40 ms smoothing, no post-limiter make-up.
local_peak=maximum_filter1d(np.abs(native),size=961,mode='nearest')
allowed=np.minimum(gain,10**(-2/20)/np.maximum(local_peak,1e-9))
envelope=np.minimum(allowed,uniform_filter1d(allowed,size=1921,mode='nearest'))
master=np.zeros(90*48000);onset=round(offset*48000);master[onset:onset+len(native)]=native*envelope
with wave.open(str(V/'assets/audio/narration-master.wav'),'wb') as wav:
    wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(48000);wav.writeframes(np.round(master*32767).astype('<i2').tobytes())
js(V/'normalization.json',{'method':'Sample-indexed gain, offline anticipatory peak control and padding; no timing-sensitive streaming filter','input_lufs':float(levels['input_i']),'target_gain':gain,'minimum_gain':float(envelope.min()),'maximum_gain':float(envelope.max()),'peak_cap_dbfs':-2,'protection_ms':20,'smoothing_ms':40,'onset_samples':onset,'sample_rate':48000,'duration_samples':len(master),'source_samples':len(native)})
placed=[{**w,'start':round(w['start']+offset,6),'end':round(min(w['end'],voice['duration_s'])+offset,6)} for w in words]
actual_duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(V/'assets/audio/narration-master.wav')]))
js(V/'placed_audio.json',{'source':voice['path'],'source_sha256':sha(V/voice['path']),'path':'assets/audio/narration-master.wav','sha256':sha(V/'assets/audio/narration-master.wav'),'offset':offset,'tempo':1,'words':placed,'duration_s':actual_duration,'processing':'Sample-indexed gain toward -16 LUFS with offline anticipatory -2 dBFS peak control; exact 450 ms onset and tail padding; native speech speed.'})
count=0
for n,s in enumerate(plan):
    size=len(s['text'].split());s['first_word_index']=count;s['last_word_index']=count+size-1
    s['start']=0 if n==0 else max(0,placed[count]['start']-.12)
    count+=size
for n,s in enumerate(plan):
    s['end']=plan[n+1]['start'] if n+1<len(plan) else 90
    original=s['duration'];s['duration']=round(s['end']-s['start'],6);s['motion_scale']=s['duration']/original
js(V/'timing.json',plan)

groups=[];buf=[]
for w in placed:
    if buf and (len(buf)>=4 or len(' '.join(x['text'] for x in buf+[w]))>36 or w['start']-buf[-1]['end']>.18):groups.append(buf);buf=[]
    buf.append(w)
    if re.search(r'[.?!]$',w['text']):groups.append(buf);buf=[]
if buf:groups.append(buf)
def stamp(t,sep=','):
    x=round(t*1000);return f'{x//3600000:02}:{x//60000%60:02}:{x//1000%60:02}{sep}{x%1000:03}'
out=[];srt=[];vtt=['WEBVTT\n'];tweens=[]
for i,g in enumerate(groups):
    a=g[0]['start'];b=min(groups[i+1][0]['start'] if i+1<len(groups) else 89.5,g[-1]['end']+.16)
    text=' '.join(x['text'] for x in g);ident=f'cap-{i:03}'
    out.append(f'<div id="{ident}" class="cap clip" data-start="{a}" data-duration="{b-a}" data-layout-allow-caption-zone><div class="caption-block">{html.escape(text)}</div></div>')
    srt.append(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{text}\n');vtt.append(f'{stamp(a,".")} --> {stamp(b,".")}\n{text}\n')
css="""@font-face{font-family:Manrope;src:url('assets/fonts/manrope.ttf')}#root{position:absolute;inset:0;pointer-events:none}.cap{position:absolute;left:108px;top:1500px;width:848px;min-height:150px;text-align:center;font:600 46px/1.3 Manrope;color:#172B3B}.caption-block{display:inline-block;max-width:848px;padding:18px 26px;background:#F8F9F5;border-radius:14px;white-space:normal}*{box-sizing:border-box}"""
content='<template><style>'+css+'</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920">'+''.join(out)+'</div><script>const tl=gsap.timeline({paused:true});const clock={v:0};tl.to(clock,{v:90,duration:90,ease:"none"});window.__timelines["captions"]=tl;</script></template>'
(V/'compositions/captions.html').write_text(content,encoding='utf-8')
E=V.parent/'exports';E.mkdir(exist_ok=True)
(E/'stapler-kaki-menutup-v1.srt').write_text('\n'.join(srt),encoding='utf-8');(E/'stapler-kaki-menutup-v1.vtt').write_text('\n'.join(vtt),encoding='utf-8')
js(V/'caption-groups.json',[{'start':g[0]['start'],'end':g[-1]['end'],'text':' '.join(w['text'] for w in g)} for g in groups])

# Reuse frozen material cues from a previous production; no paid SFX synthesis.
origin=R/'productions/tangki-dua-katup/video/assets/audio/sfx'
assets=json.loads((origin/'assets.json').read_text())
selected=[]
dest=V/'assets/audio/sfx';dest.mkdir(parents=True,exist_ok=True)
for old_id,new_id,name in [('handle-contact','hinge','handle-contact.wav'),('chain-contact','metal','chain-contact.wav')]:
    entry=next(a for a in assets if a['id']==old_id);src=origin/name;assert sha(src)==entry['sha256']
    shutil.copy2(src,dest/name)
    entry={**entry,'id':new_id,'path':'assets/audio/sfx/'+name,'reuse_source':'productions/tangki-dua-katup/video/'+entry['path'],'episode_role':'Illustrative dry cover travel/return' if new_id=='hinge' else 'Restrained illustrative steel contact, not recorded stapler audio'}
    selected.append(entry)
    req='chair.request.json' if new_id=='hinge' else 'clip-seat.request.json'
    shutil.copy2(origin/'sources'/req,dest/req)
src=R/'.agents/skills/media-use/audio/assets/sfx/click-soft.mp3';shutil.copy2(src,dest/'editorial-click.mp3')
selected.append({'id':'editorial','path':'assets/audio/sfx/editorial-click.mp3','sha256':sha(src),'duration_s':.4,'source':{'provider':'bundled Pixabay SFX','url':'https://pixabay.com/service/license-summary/','role':'soft editorial inspection cue, not physical audio'}})
shutil.copy2(R/'.agents/skills/media-use/audio/assets/sfx/CREDITS.md',dest/'BUNDLED_CREDITS.md')
js(dest/'assets.json',selected)
print(json.dumps({'native_voice_seconds':voice['duration_s'],'placed_duration':90,'words':len(placed),'groups':len(groups),'scene_starts':[round(x['start'],2) for x in plan]}))
