"""Tie source-verified reused cues to actual motion and acoustic/frame timing."""
from pathlib import Path
import json,sys,subprocess
V=Path(__file__).resolve().parent;R=V.parents[2]
sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'))
from sound_design import digest,motion_digest
assets=json.loads((V/'assets/audio/sfx/assets.json').read_text(encoding='utf-8'))
events=json.loads((V/'motion-events.json').read_text(encoding='utf-8'));timing=json.loads((V/'timing.json').read_text(encoding='utf-8'))
observed={x['scene']:x['resetEvents'] for x in json.loads((V/'verification/motion.json').read_text(encoding='utf-8'))['results']}
scenes={x['id']:x for x in timing['scenes']}
for event in events:
 if event['role']=='metal' and ('coasting' in event['action'] or 'reset' in event['action']):
  s=scenes[event['scene']];local=event['time']-s['start'];choices=[t for t in observed[event['scene']] if t>.2 and t<s['duration']-.3]
  if not choices:raise ValueError('No measured pawl reset for '+event['scene'])
  event['time']=s['start']+min(choices,key=lambda t:abs(t-local))
  event['action']+=' (observed pawl return at output-frame sample)'
 if event['scene']=='s06-approach':
  s=scenes[event['scene']];event.update(time=round((s['start']+s['duration']*.12)*30)/30,role='travel',action='input approach begins before drive-face contact')
cues=[]
for a in assets:a['duration_s']=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(V/a['path'])]))
for n,e in enumerate(sorted(events,key=lambda x:x['time'])):
 ident='editorial' if e['role']=='editorial' else 'hinge' if e['role']=='travel' else 'metal';a=next(a for a in assets if a['id']==ident)
 cues.append(dict(id=f'sfx-{n+1:03}-{e["scene"]}',scene=e['scene'],asset=ident,purpose=e['role']+' cue: '+e['action'],trigger=e['action']+'; visual onset rounded to nearest30fps frame',start=round(e['time']*30)/30,duration=min(a['duration_s'],90-e['time']),volume=.3 if ident=='editorial' else .48 if ident=='hinge' else .62,track=4+n%4))
plan=dict(version=1,decisions=dict(narration=dict(mode='use',reason='Preserved one continuous ElevenLabs eleven_v4 recording, measured quiet pause placement and final normalization; derived tempo recorded in audio_boundaries.json.'),bgm=dict(mode='none',reason='Expose the difference between speech, travel and dry pawl contacts.'),sfx=dict(mode='use',reason='Frozen material cues reused with source hashes after inspecting bundled media-use library; soft editorial cue on section only. No generation.')),assets=assets,cues=cues,timing_sha256=digest(V/'timing.json'),narration_sha256=digest(V/'assets/audio/narration-master.wav'),motion_sources={f'compositions/{s["id"]}.html':motion_digest(V/f'compositions/{s["id"]}.html') for s in timing['scenes']},silence='Quiet acoustic seams preserve complete utterances. Bearing support reading is intentionally quiet. Sustained coasting shares representative repeated tooth-contact cues; no cue is claimed as a literal product recording. No generic transition whooshes.',creative_listening='Unavailable; waveform/onset/level evidence only.')
(V/'sound_design.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
package=json.loads((V/'package.json').read_text(encoding='utf-8'))
for verb in ['check','render']:package['scripts'][verb]=f'python ../../../.agents/skills/shortform-production/scripts/sound_design.py --video . --check && npx --yes hyperframes@0.8.206 {verb}'
(V/'package.json').write_text(json.dumps(package,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(cues=len(cues),assets=len(assets))))
