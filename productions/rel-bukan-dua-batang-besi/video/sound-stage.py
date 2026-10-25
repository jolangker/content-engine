from pathlib import Path
import json,hashlib,re,subprocess,importlib.util
import numpy as np
V=Path(__file__).resolve().parent;ROOT=V.parents[2]
def read(p):return json.loads((V/p).read_text(encoding='utf-8'))
def write(p,v):(V/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def decode(p):return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar','48000','-f','f32le','pipe:1'],capture_output=True,check=True).stdout,dtype='<f4').copy()
timing=read('timing.json');plan=read('scene-plan.json');words=timing['words'];offset=timing['voice_offset']
def clean(t):return re.sub(r'[^\w]','',t.lower())
marks=[[(.48,'besi'),(.69,'Beres')],[(.36,'besar'),(.60,'turun')],[(.40,'rel'),(.75,'bawahnya')],[(.66,'rel')],[(.50,'bersudut'),(.75,'mengunci')],[(.40,'bantalan'),(.80,'santai')],[(.65,'basah')],[(.35,'jalur'),(.45,'drainase'),(.80,'pembuangan')],[],[(.37,'kotor'),(.60,'celahnya'),(.86,'diganti')],[(.28,'berubah'),(.70,'bantalan'),(.95,'jalur')],[(.65,'sistem'),(.91,'dipakai')]]
for si,s in enumerate(plan):
    points=[[0,0]]
    for phase,anchor in marks[si]:
        candidates=[w for w in words[s['word_start']:s['word_end']+1] if clean(w['text'])==clean(anchor)]
        if not candidates:raise ValueError('Missing anchor '+anchor)
        w=candidates[0];u=(offset+w['end']-s['start'])/s['duration'];u=min(.985,max(.015,u))
        if u<=points[-1][0] or phase<=points[-1][1]:raise ValueError('Nonmonotonic motion marks')
        points.append([u,phase])
    points.append([1,1]);s['phase_points']=points
write('scene-plan.json',plan);timing['scenes']=plan;write('timing.json',timing)
def event(si,phase):
    s=plan[si];pts=s['phase_points'];j=next(i for i in range(1,len(pts)) if pts[i][1]>=phase);a,b=pts[j-1:j+1];u=a[0]+(phase-a[1])/(b[1]-a[1])*(b[0]-a[0]);return s['start']+u*s['duration']
assets=[];durations={};treatments=[]
for source in sorted((V/'assets/audio/sfx').glob('*.mp3')):
    id=source.stem;out=source.with_suffix('.wav');samples=decode(source)
    peak=float(np.max(np.abs(samples)));threshold=peak*.075;cross=np.flatnonzero(np.abs(samples)>threshold)
    first=max(0,int(cross[0])-round(.012*48000))
    # Impact samples begin 12ms before first firm contact; retain all source material in MP3.
    if id in ['steel-contact','concrete-set','clip-seat','splash']:
        energy=np.convolve(samples.astype(float)**2,np.ones(240)/240,mode='same');strong=int(np.argmax(energy));first=max(first,strong-round(.018*48000))
    if id not in ['train-pass','tamping','drain-water','ballast-pour']:
        samples=samples[first:]
    else:samples=samples[first:]
    # Peak-referenced material cues, bounded gain, no speculative spectral correction.
    target_db=-9 if id not in ['drain-water','train-pass','tamping'] else -15
    samples=samples*(10**(target_db/20)/max(np.max(np.abs(samples)),1e-9))
    fade=min(240,len(samples)//10);samples[:fade]*=np.linspace(0,1,fade);samples[-fade:]*=np.linspace(1,0,fade)
    import wave
    with wave.open(str(out),'wb') as f:f.setparams((1,2,48000,0,'NONE',''));f.writeframes((samples.clip(-.99,.99)*32767).astype('<i2').tobytes())
    durations[id]=len(samples)/48000
    assets.append(dict(id=id,path=out.relative_to(V).as_posix(),sha256=sha(out),source='ElevenLabs eleven_text_to_sound_v2 original designed Foley; request receipt beside source MP3. No suitable reusable asset/Openverse match.'))
    treatments.append(dict(id=id,source_sha256=sha(source),output_sha256=sha(out),trim_start_s=first/48000,target_peak_dbfs=target_db,duration=durations[id]))
write('verification/sfx-treatments.json',treatments)
cues=[]
def cue(id,asset,si,phase,length,vol,purpose):
    start=event(si,phase);duration=min(length,durations[asset],timing['duration']-start)
    cues.append(dict(id='sfx-'+id,asset=asset,scene=plan[si]['id'],purpose=purpose,trigger=f"{purpose}; seek-state phase {phase}, aligned to native narration anchor map",start=round(start,6),duration=round(duration,6),volume=vol,track=12 if asset not in ['drain-water','train-pass'] else 13))
cue('rail-seat','steel-contact',0,.48,.75,.62,'Rail contacts bare ground')
cue('wheel-contact','steel-contact',1,.36,.6,.38,'Wheel tread meets rail head')
cue('sleeper-seat','concrete-set',2,.40,.9,.68,'Sleeper finishes approach to rail seat')
cue('spring-clip','clip-seat',3,.66,.75,.80,'Generic clip seats over rail foot')
cue('ballast-cascade','ballast-pour',4,.13,2.9,.72,'Angular ballast visibly pours beneath panel')
cue('stone-contact','concrete-set',4,.72,.55,.28,'Stone sample contact and settle')
cue('shoulder-cascade','ballast-pour',5,.10,2.0,.60,'Shoulder ballast fills beside sleeper ends')
cue('chair-unfold','chair',5,.63,1.3,.66,'Chair unfolds on verge pad')
cue('puddle-step','splash',6,.17,.8,.75,'Boot steps into shallow visible puddle')
cue('chair-lift','chair',6,.58,1.0,.45,'Builder lifts chair out of the puddle')
cue('channel-water','drain-water',7,.48,3.0,.62,'Schematic flow enters side drain after its placement')
cue('outlet-water','drain-water',8,.20,3.0,.55,'Water follows lower outlet')
cue('fines-fall','ballast-pour',9,.12,1.0,.30,'Fine aggregate falls into stone voids')
cue('cleaning-screen','ballast-pour',9,.65,1.2,.46,'Material separates at cleaning screen')
cue('tamp-insert','tamping',10,.43,2.0,.65,'Tines descend then squeeze beneath the sleeper')
cue('tamp-withdraw','steel-contact',10,.86,.5,.35,'Maintenance head withdraws')
cue('train-roll','train-pass',11,.10,4.2,.65,'Train rolls on completed route')
cue('chair-payoff','chair',11,.88,.85,.48,'Builder sits and chair accepts weight')
# Reuse the previous episode's generated rain texture, never count it as interaction Foley.
rain_source=ROOT/'productions/hujan-bukan-sekadar-ember/video/assets/audio/rain-loop.mp3'
if not rain_source.exists():
    candidates=list((ROOT/'productions/hujan-bukan-sekadar-ember/video').rglob('*rain*.mp3'))
    if candidates:rain_source=candidates[0]
if rain_source.exists():
    import shutil
    rain_path=V/'assets/audio/sfx/rain-reused.wav';subprocess.run(['ffmpeg','-v','error','-y','-i',str(rain_source),'-t','8','-af','afade=t=in:d=0.2,afade=t=out:st=7.3:d=0.7','-ar','48000','-ac','1',str(rain_path)],check=True)
    assets.append(dict(id='rain-reused',path=rain_path.relative_to(V).as_posix(),sha256=sha(rain_path),source='Reuse: hujan-bukan-sekadar-ember generated ElevenLabs rain-loop; original request receipt preserved in that episode. Ambience only.'))
    durations['rain-reused']=len(decode(rain_path))/48000
    cue('rain-location','rain-reused',6,.01,min(plan[6]['duration']*.8,7.8),.08,'Rain establishes weather; separate from material cues')
sd=dict(version=1,decisions=dict(narration=dict(mode='use',reason='One continuous conversational Indonesian explanation; root .env ElevenLabs eleven_v4 voice.'),bgm=dict(mode='none',reason='Board permits no music; narration, material interactions and brief comic quiet carry rhythm.'),sfx=dict(mode='use',reason='Discrete physically motivated construction, stone, water, maintenance and chair cues; rain is separate ambience.')),
 timing_sha256=sha(V/'timing.json'),narration_sha256=sha(V/'assets/audio/narration-master.wav'),motion_sources={},assets=assets,cues=cues,silence='No generic whooshes, decorative pings, invented mechanism clicks or sound on force arrows. Flow notation uses water texture only. Perceptual listening unavailable; balance, timbre and comic timing remain unverified by ears.')
spec=importlib.util.spec_from_file_location('sound',ROOT/'.agents/skills/shortform-production/scripts/sound_design.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
sd['motion_sources']={'world.js':m.motion_digest(V/'world.js'),'scene-data.js':'pending'}
write('sound_design.json',sd)
print(json.dumps(dict(assets=len(assets),cues=len(cues),phase_maps=len(plan))))
