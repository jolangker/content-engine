"""Freeze existing sounds, place cues on mechanism events, retain provenance."""
from pathlib import Path
import json,hashlib,sys,shutil,subprocess
V=Path(__file__).resolve().parent;R=V.parents[2]
sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'))
from sound_design import digest,motion_digest
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
D=V/'assets/audio/sfx';D.mkdir(parents=True,exist_ok=True)
assets=[]
sources=[('hinge','productions/pensil-jepit-dan-maju/video/assets/audio/sfx','hinge'),('metal','productions/pensil-jepit-dan-maju/video/assets/audio/sfx','metal'),('editorial','productions/pensil-jepit-dan-maju/video/assets/audio/sfx','editorial'),('air','productions/tangki-dua-katup/video/assets/audio/sfx','section-reveal')]
for ident,rel,oldid in sources:
 origin=R/rel;items=json.loads((origin/'assets.json').read_text(encoding='utf-8'));item=next(x for x in items if x['id']==oldid);src=origin/Path(item['path']).name
 assert digest(src)==item['sha256'];dest=D/src.name;shutil.copy2(src,dest)
 item.update(id=ident,path=dest.relative_to(V).as_posix(),reuse_source=src.relative_to(R).as_posix(),episode_role='Stylized dry contact/lever Foley or editorial flow/thermal handoff, not a recorded tape measure. No newly generated sound.')
 item['duration_s']=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(dest)]))
 assets.append(item)
 for request in origin.rglob('*.request.json'):
  target=D/'provenance'/request.name;target.parent.mkdir(parents=True,exist_ok=True)
  if not target.exists():shutil.copy2(request,target)
dump(D/'assets.json',assets)
(D/'CREDITS.md').write_text('# Audio provenance\n\nBundled media-use SFX manifest inspected first. Bundled Pixabay click and previously filtered whoosh carry Pixabay Content License: https://pixabay.com/service/license-summary/ . Frozen historical ElevenLabs hinge/latch and metal-contact cues reused byte-for-byte with source prompt/request hashes in assets.json, https://elevenlabs.io/terms-of-use . These sounds are stylized illustrative guidance; no tape-measure field recording is claimed. No new SFX generation or treatment. No BGM: leave room for speech and small interactions.\n',encoding='utf-8')
events=json.loads((V/'motion-events.json').read_text(encoding='utf-8'));timing=json.loads((V/'timing.json').read_text(encoding='utf-8'));cues=[]
for n,event in enumerate(events):
 ident=event['asset']
 if event['kind']=='shell-reveal':ident='air'
 asset=next(x for x in assets if x['id']==ident)
 cues.append(dict(id=f'sfx-{n+1:02}-{event["kind"]}',scene=event['scene'],asset=ident,purpose=('Stylized editorial attention handoff' if ident in ['air','editorial'] else 'Representative dry material '+event['kind'])+'; not literal tape measure acoustics',trigger=f'Visible {event["kind"]} at analytic progress {event["progress"]}; nearest30fps frame',start=event['start'],duration=min(asset['duration_s'],90-event['start']),volume={'air':.7,'editorial':.22,'metal':.52,'hinge':.38}[ident],track=4+n%4))
plan=dict(version=1,decisions=dict(narration=dict(mode='use',reason='One preserved ElevenLabs eleven_v4 recording, root-env voice, acoustic scene cuts, one final normalization.'),bgm=dict(mode='none',reason='Keep small mechanical events and narration clear.'),sfx=dict(mode='use',reason='Existing media-use assets and frozen episode treatments; material contacts plus distinct softer editorial attention handoffs.')),assets=assets,cues=cues,timing_sha256=digest(V/'timing.json'),narration_sha256=digest(V/'assets/audio/narration-master.wav'),motion_sources={f'compositions/{s["id"]}.html':motion_digest(V/f'compositions/{s["id"]}.html') for s in timing['scenes']},silence='Coupled reel/blade movement shares a restrained travel cue. Hidden energy storage and guide inspection use distinct editorial accents. Holding a locked blade is intentionally quiet; continuing spring bias is not made into an invented motor sound. The detent snap, tongue contact and release receive separate frame-aligned material cues. No continuous winding field recording is claimed.',creative_listening='Unavailable: verify timing, loudness and encoded cue presence objectively; do not claim perceptual or phone-speaker approval.')
dump(V/'sound_design.json',plan)
pkg=json.loads((V/'package.json').read_text(encoding='utf-8'))
for verb in ['check','render']:pkg['scripts'][verb]=f'python ../../../.agents/skills/shortform-production/scripts/sound_design.py --video . --check && npx --yes hyperframes@0.8.216 {verb}'
dump(V/'package.json',pkg)
print(json.dumps(dict(assets=len(assets),cues=len(cues))))
