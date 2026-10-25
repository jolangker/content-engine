from pathlib import Path
import hashlib,importlib.util,json
B=Path(__file__).resolve().parent;R=B.parent.parent;V=B/'video'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
spec=importlib.util.spec_from_file_location('sd',R/'.agents/skills/shortform-production/scripts/sound_design.py');sd=importlib.util.module_from_spec(spec);spec.loader.exec_module(sd)
scenes=read(V/'scenes.json');source=read(V/'assets/board/audio/sfx/manifest.json');mix=read(V/'mix.json')
assets=[]
for a in source['assets']:
    path='assets/board/audio/sfx/'+a['file']
    assert sha(V/path)==a['sha256']
    assets.append(dict(id=a['id'],path=path,sha256=sha(V/path),duration=a['duration'],source=dict(board='ruang-di-antara v1.2',provenance=a['source'],credits='assets/board/audio/sfx/CREDITS.md')))
events=[(3,'contact',.22,'Changed-plan card lands on the shared topic',.60,False),(7,'connection',.68,'Both routes meet the agreed return plan',.65,True),(9,'contact',.45,'Proposed 20:00 appointment becomes visible',.55,False),(12,'connection',.68,'Returning actor reconnects with the unfinished issue',.65,True),(13,'air',.45,'The update proposes a different appointment direction',.50,False),(14,'contact',.68,'The original topic is taken up again at the shared table',.60,True)]
cues=[]
for n,a,frac,purpose,volume,draw in events:
    s=scenes[n-1];asset=next(x for x in assets if x['id']==a);local=s['duration']*frac+min(.85,s['duration']*.16)+(.25 if draw else 0)
    cues.append(dict(id=f'sfx-f{n:02}-{a}',asset=a,scene=f'f{n:02}',purpose=purpose,trigger=f'Semantic beat at {frac:.2f} of measured scene, landing at local {local:.4f}s'+(' after line draw completes' if draw else ''),start=round(s['start']+local,4),duration=asset['duration'],volume=volume,track=3))
plan=dict(version=1,decisions=dict(narration=dict(mode='use',reason='Intimate continuous narration at original speed; six seconds editorial silence and measured loudness preparation preserved in placement.json and mix.json.'),bgm=dict(mode='none',reason='The pause and return should be heard as actual space; an emotional bed would soften the open waiting moment.'),sfx=dict(mode='use',reason='Six restrained licensed material cues follow actual proposal, agreement and return actions. No cue quota and no sound on every cut.')),timing_sha256=sha(V/'timing.json'),narration_sha256=sha(V/mix['path']),motion_sources={f'compositions/frames/f{s["n"]:02}.html':sd.motion_digest(V/f'compositions/frames/f{s["n"]:02}.html') for s in scenes},assets=assets,cues=cues,silence='Frame 04 departure is deliberately unscored. No sounds in the cooling interval 11. Frame 12 connection is restrained after the return route completes. Final 1.2s reflective tail has no new cue.')
(V/'sound_design.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(sd.apply_plan(V)))
