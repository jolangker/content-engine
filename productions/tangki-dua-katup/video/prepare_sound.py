from pathlib import Path
import json,hashlib,sys,importlib.util
V=Path(__file__).resolve().parent;ROOT=V.parents[2]
spec=importlib.util.spec_from_file_location('sound',ROOT/'.agents/skills/shortform-production/scripts/sound_design.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
scenes=json.loads((V/'timing.json').read_text(encoding='utf-8'));audio=json.loads((V/'placed_audio.json').read_text(encoding='utf-8'));assets=json.loads((V/'assets/audio/sfx/assets.json').read_text(encoding='utf-8'))
cues=[]
def cue(i,frac,asset,duration,purpose,trigger,volume=.45):
 s=scenes[i-1];t=round((s['start']+s['duration']*frac)*30)/30
 cues.append(dict(id=f'sfx-{s["id"]}-{len(cues)+1:02}',asset=asset,scene=s['id'],purpose=purpose,trigger=trigger,start=round(t,6),duration=round(duration,5),volume=volume,track=4 if asset.startswith('water') else 5,sync='visual key-pose onset rounded to nearest output frame; error <= 1/60s'))
def water(i,frac=0,asset='water-flow',endfrac=1,volume=.45):
 s=scenes[i-1];duration=(endfrac-frac)*s['duration'];cue(i,frac,asset,min(duration,11.95),'Sustain visible water transfer','Same shot key-pose flow onset/continuation',volume)
cue(1,0,'section-reveal',.42,'Editorial exterior-to-section inspection','Start of selective section reveal',.7)
water(1,.35,endfrac=1,volume=.5)
cue(2,0,'section-reveal',.42,'Editorial lid/section reveal','Lid separation and section transparency begin',.7)
cue(3,.2,'chain-contact',.22,'Stylized attention handoff to outlet valve','First valve emphasis begins',.26)
cue(3,.6,'chain-contact',.22,'Stylized attention handoff to fill valve','Second valve emphasis begins',.26)
cue(4,.2,'handle-contact',.52,'Handle rotates lever','Press and lever motion begin')
cue(4,.2,'chain-contact',.22,'Chain takes up tension','Chain endpoint begins rising',.38)
cue(5,.2,'chain-contact',.22,'Flapper lifting contact','Further lever/flapper lift begins',.35)
water(5,.2)
water(6)
cue(7,0,'handle-contact',.52,'Handle released while flapper remains open','Lever return begins',.3)
water(7)
water(8,0,endfrac=1,volume=.3)
water(8,0,'water-refill',endfrac=1,volume=.36)
water(9,0,endfrac=1,volume=.4)
water(9,0,'water-refill',endfrac=1,volume=.36)
water(10,0,endfrac=.58,volume=.35)
cue(10,.58,'rubber-seat',.38,'Flapper seals outlet','Flapper reaches zero angle; main flush flow stops',.55)
water(10,0,'water-refill',endfrac=1,volume=.38)
water(11,0,'water-refill',endfrac=1,volume=.44)
water(12,0,'water-refill',endfrac=.75,volume=.4)
cue(12,.75,'rubber-seat',.38,'Soft stylized shutoff confirmation','Fill/refill opacity reaches zero',.3)
water(13,0,'water-refill',volume=.45)
water(14,0,'water-refill',volume=.35)
water(14,.45,endfrac=1,volume=.42)
cue(15,0,'handle-contact',.52,'Cycle replay begins','Lever/flapper begin actuating',.4)
water(15,0,endfrac=.54,volume=.42)
water(15,.14,'water-refill',endfrac=.96,volume=.42)
cue(15,.54,'rubber-seat',.38,'Cycle replay outlet closes','Flapper reaches its seat',.45)
cue(15,.96,'rubber-seat',.38,'Cycle replay refill stops','Full water level; fill switches off',.28)
cue(16,.45,'section-reveal',.42,'Editorial reassembly','Lid/front illustration close',.65)
lanes={'water-flow':4,'water-refill':5,'handle-contact':6,'chain-contact':7,'rubber-seat':8,'section-reveal':9}
for c in cues:c['track']=lanes[c['asset']]
for asset in lanes:
 ordered=sorted([c for c in cues if c['asset']==asset],key=lambda c:c['start'])
 for a,b in zip(ordered,ordered[1:]):
  if a['start']+a['duration']>b['start']:a['duration']=round(b['start']-a['start'],6)
plan=dict(version=1,decisions=dict(narration=dict(mode='use',volume=.9,reason='One native-speed ElevenLabs eleven_v4 recording; existing inter-sentence pauses expanded for mechanism observation; normalized -16 LUFS.'),bgm=dict(mode='none',reason='Unscored inspection; foreground narration and material/water cues.'),sfx=dict(mode='use',reason='Every designed interaction mapped to material accents or sustained water; editorial inspection cues differentiated from literal physical acoustics.')),assets=assets,cues=cues,timing_sha256=sha(V/'timing.json'),narration_sha256=sha(V/audio['path']),motion_sources={f'compositions/frames/{s["id"]}.html':m.motion_digest(V/f'compositions/frames/{s["id"]}.html') for s in scenes},creative_listening='Direct perceptual listening unavailable in this session. Native word alignment, waveform presence and levels verified separately; no human or perceptual approval claimed.',narration_processing={k:v for k,v in audio.items() if k!='words'},intentional_silence='Anatomy holds and state observation pauses may be quiet. No new physical transfer occurs in final ready-state hold. Float control is represented by the ongoing fill texture; no invented audible diaphragm click.')
(V/'sound_design.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'assets':len(assets),'cues':len(cues)}))
