"""Close delegated preview review and prepare the verified delivery render."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent;V=P/'video'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
assert read(V/'verification/hyperframes-check.json')['ok']
assert read(V/'verification/seek-consistency.json')['same_state_after_reverse_seek']
preview=read(V/'verification/preview-report.json');assert preview['status']==200 and not preview['errors'];assert preview['playback_samples'][-1]['clock']==['01:30/01:30']
note='''
## Preview and delegated render authorization

Pipeline-owned preview: project productions/jeda-balasan-dan-dugaan/video, PID20344, port3002, http://127.0.0.1:3002/#project/video. Created by this run; hold through render and verified export, then stop before packaging/upload. HTTP200 and full 00:00–01:30 player progression, narration readiness and no page errors verified. The preview was exposed to the user as an editing surface; no human approval claimed.

Active visible scene states at 18 forward/reverse seeks are identical. An initial test compared all mounted offscreen neighbors and failed because the preview virtualizes them; the corrected test scopes to the expected active scene and checks actual path/transform/opacity states. No visual drift was found and no composition change was needed.

Independent visual review inspected the storyboard, 64 phase samples, two beat/phone sheets and all 15 seam sheets: no P0/P1 findings. Dark turns, caption clearance, actor continuity and focal scale pass. These are image-based checks, not perceptual audio review. Full technical and creative verification authorizes the exact current version's delivery render under --automation.
'''
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(note)
with (V/'REVIEW.md').open('a',encoding='utf-8') as f:f.write(note)
for name in ('verify_export.py','upload_media.py','record_delivery.py','verify_remote_media.py','publishing_prepare.py'):
    s=(P.parent/'terima-kasih-yang-melihat'/name).read_text(encoding='utf-8').replace('terima-kasih-yang-melihat',P.name).replace('Terima kasih yang melihat','Jeda balasan dan dugaan')
    (P/name).write_text(s,encoding='utf-8')
print('Delegated preview review complete; export authorized.')
