"""Bind the cue sheet to measured narration and exact motion source hashes."""
from pathlib import Path
import json,hashlib,re,subprocess
V=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def motion_sha(p):return hashlib.sha256(re.sub(r'\s+data-hf-id=(?:"[^"]*"|\x27[^\x27]*\x27)','',p.read_text(encoding='utf-8')).encode()).hexdigest()
assets=json.loads((V/'assets/audio/sfx/assets.json').read_text(encoding='utf-8'));events=json.loads((V/'motion-events.json').read_text(encoding='utf-8'));timing=json.loads((V/'timing.json').read_text(encoding='utf-8'));cues=[];note_count=0
for a in assets:a['duration_s']=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(V/a['path'])]))
for n,event in enumerate(sorted(events,key=lambda e:e['time'])):
    role=event['role']
    if role=='note':asset=f'note-{note_count%3+1}';note_count+=1;gain=.42;limit=1.3
    elif role=='editorial':asset='editorial';gain=.32;limit=.32
    elif role=='friction':asset='hinge';gain=.4;limit=.5
    else:asset='metal';gain=.62;limit=.2
    a=next(a for a in assets if a['id']==asset);start=event['time'];duration=min(a['duration_s'],limit,90-start)
    cues.append(dict(id=f'sfx-{n+1:03}-{event["scene"]}',scene=event['scene'],asset=asset,purpose=role+' cue for '+event['action'],trigger=event['action']+'; numerical event rounded to nearest 30fps frame',start=start,duration=duration,volume=gain,track=4+n%4,role=role))
plan=dict(version=1,decisions=dict(narration=dict(mode='use',reason='One native 88.88s ElevenLabs eleven_v4 request, root-env voice; gain/peak control and 0.3s onset only.'),bgm=dict(mode='none',reason='Intentionally unscored: heard instrument-note illustrations and narration carry the sound; a separate song would obscure the subject.'),sfx=dict(mode='use',reason='Material contact and editorial cues reused; three attributed CC BY music-box single-note recordings at pin-release events, not a claimed reproduction of the illustrated pattern.')),assets=assets,cues=cues,timing_sha256=sha(V/'timing.json'),narration_sha256=sha(V/'assets/audio/narration-master.wav'),motion_sources={f'compositions/{s["id"]}.html':motion_sha(V/f'compositions/{s["id"]}.html') for s in timing},silence='Labels and settled observation holds intentionally quiet. Sustained gears and spring motion share their onset cue; continuous simulated friction shares one restrained cue. Anatomy separation uses an editorial cue. No additional whoosh at every cut.',creative_listening='Unavailable: waveform/onset/level checks only; perceptual and phone-speaker listening not claimed.')
(V/'sound_design.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(cues=len(cues),note_releases=note_count,assets=len(assets))))
