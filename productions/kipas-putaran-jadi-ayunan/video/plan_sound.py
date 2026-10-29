"""Bind illustrative interaction cues to the film's actual frame-clock motion."""
from pathlib import Path
import json,sys,subprocess
V=Path(__file__).resolve().parent;R=V.parents[2]
sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'))
from sound_design import digest,motion_digest
assets=json.loads((V/'assets/audio/sfx/assets.json').read_text(encoding='utf-8'))
events=json.loads((V/'motion-events.json').read_text(encoding='utf-8'));timing=json.loads((V/'timing.json').read_text(encoding='utf-8'))
for a in assets:a['duration_s']=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(V/a['path'])]))
cues=[]
for n,e in enumerate(events):
 ident='editorial' if e['role']=='editorial' else 'metal' if e['role']=='metal' else 'hinge';a=next(x for x in assets if x['id']==ident)
 cues.append(dict(id=f'sfx-{n+1:03}-{e["scene"]}',scene=e['scene'],asset=ident,purpose=e['role']+' illustrative cue: '+e['action'],trigger=e['action']+'; motion event clock rounded to nearest30fps frame',start=e['time'],duration=min(a['duration_s'],90-e['time']),volume=.24 if ident=='editorial' else .34 if ident=='hinge' else .46,track=4+n%4))
plan=dict(version=1,decisions=dict(narration=dict(mode='use',reason='Preserved continuous ElevenLabs eleven_v4 source, derived pitch-preserving tempo, acoustic placement and final normalization.'),bgm=dict(mode='none',reason='Keep speech and the contrast between mechanism movement and clutch contact clear.'),sfx=dict(mode='use',reason='Existing media-use manifest checked first; source-verified frozen material cues and bundled editorial tick reused, no generation.')),assets=assets,cues=cues,timing_sha256=digest(V/'timing.json'),narration_sha256=digest(V/'assets/audio/narration-master.wav'),motion_sources={f'compositions/{s["id"]}.html':motion_digest(V/f'compositions/{s["id"]}.html') for s in timing['scenes']},silence='Continuous gearing/link travel is represented by a restrained cue at each inspected action onset, then intentionally quiet under narration. No sound for every tooth or blade. Neck support is an editorial cue, not a physical impact. Not a literal fan recording. Acoustic cut margins stay quiet.',creative_listening='Unavailable; source/onset/level and encoded cue evidence only.')
(V/'sound_design.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
package=json.loads((V/'package.json').read_text(encoding='utf-8'))
for verb in ['check','render']:package['scripts'][verb]=f'python ../../../.agents/skills/shortform-production/scripts/sound_design.py --video . --check && npx --yes hyperframes@0.8.206 {verb}'
(V/'package.json').write_text(json.dumps(package,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(cues=len(cues),assets=len(assets))))
