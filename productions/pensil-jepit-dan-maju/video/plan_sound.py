"""Place existing sound assets on verified visible events, without generation."""
from pathlib import Path
import json,sys,subprocess
V=Path(__file__).resolve().parent;R=V.parents[2]
sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'))
from sound_design import digest,motion_digest
assets=json.loads((V/'assets/audio/sfx/assets.json').read_text(encoding='utf-8'))
for a in assets:a['duration_s']=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(V/a['path'])]))
events=json.loads((V/'motion-events.json').read_text(encoding='utf-8'));timing=json.loads((V/'timing.json').read_text(encoding='utf-8'))
cues=[]
for n,event in enumerate(events):
 ident='metal' if event['kind'] in ['ring-stop','regrip'] else 'hinge'
 asset=next(x for x in assets if x['id']==ident)
 cues.append(dict(id=f'sfx-{n+1:03}-{event["kind"]}',scene=event['scene'],asset=ident,purpose='Representative dry material '+event['kind']+'; not a literal recording of this pencil',trigger=f'Visible cycle phase{event["phase"]}; motion timestamp rounded to nearest30fps frame',start=event['start'],duration=min(asset['duration_s'],90-event['start']),volume=.46 if ident=='metal' else .34,track=4+n%4))
for key in ['grip','ring','retainer']:
 s=next(x for x in timing['scenes'] if x['key']==key);start=round((s['start']+.4)*30)/30;a=next(x for x in assets if x['id']=='editorial')
 cues.append(dict(id=f'sfx-inspection-{key}',scene=s['id'],asset='editorial',purpose='Soft editorial inspection handoff, not physical noise',trigger='Settled cutaway/detail attention onset',start=start,duration=a['duration_s'],volume=.24,track=8))
plan=dict(version=1,decisions=dict(narration=dict(mode='use',reason='One preserved ElevenLabs eleven_v4 recording; derived pitch-preserving pace1.1653, acoustic placement, final normalization.'),bgm=dict(mode='none',reason='Expose the small material contacts and speech without competing music.'),sfx=dict(mode='use',reason='Bundled manifest inspected first; existing frozen material travel/contact and bundled editorial cue reused byte-for-byte.')),assets=assets,cues=cues,timing_sha256=digest(V/'timing.json'),narration_sha256=digest(V/'assets/audio/narration-master.wav'),motion_sources={f'compositions/{s["id"]}.html':motion_digest(V/f'compositions/{s["id"]}.html') for s in timing['scenes']},silence='Friction between lead and tip is quiet under speech; soft editorial cue identifies that handoff. Short travel cues mark onsets, then observation holds are quiet. Static ring clamp/ready states require no invented impact. SFX tails end before acoustic cut margins.',creative_listening='Unavailable; measured onsets, levels and encoded cue matching only.')
(V/'sound_design.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
package=json.loads((V/'package.json').read_text(encoding='utf-8'))
for verb in ['check','render']:package['scripts'][verb]=f'python ../../../.agents/skills/shortform-production/scripts/sound_design.py --video . --check && npx --yes hyperframes@0.8.216 {verb}'
(V/'package.json').write_text(json.dumps(package,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(cues=len(cues),assets=len(assets))))
