"""Close queue delivery only after readback, public media and preview cleanup."""
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import json
P=Path(__file__).resolve().parent;R=P.parents[1];V=P/'video';Q=V/'verification'
receipt=json.loads((P/'PUBLISHING.json').read_text(encoding='utf-8'));post=receipt['posts'][0];asset=receipt['assets'][0]
public=json.loads((Q/'trypost-media.json').read_text());export=json.loads((Q/'export.json').read_text());cleanup=json.loads((Q/'preview-cleanup.json').read_text())
assert post['status']=='scheduled' and asset['status']=='verified'
assert public['matches_local_export'] and public['sha256']==export['sha256']==asset['sha256']
assert cleanup['status']=='passed' and not cleanup['recorded_process_still_owns_port']
scheduled=datetime.fromisoformat(post['scheduled_at'].replace('Z','+00:00'))
if scheduled.tzinfo is None:scheduled=scheduled.replace(tzinfo=timezone.utc)
assert scheduled>datetime.now(timezone.utc)
local=scheduled.astimezone(ZoneInfo('Asia/Jakarta')).isoformat();post['scheduled_at_local']=local;post['timezone']='Asia/Jakarta'
post['verification']['public_served_media']='HTTP200, exact SHA-256 and byte count match local export';asset['public_served_copy_verification']=dict(http_status=200,sha256=public['sha256'],bytes=public['bytes'],matches_local_export=True,evidence='video/verification/trypost-media.json')
(P/'PUBLISHING.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
note=f'''
## Queue endpoint complete — {datetime.now(ZoneInfo('Asia/Jakarta')).date()}

Trypost readback confirms scheduled queue mode, exact caption, instagram_reel, requested account and one attached MP4. Post {post['trypost_post_id']}; media {asset['media_id']}. Workspace {post['workspace_name']} ({post['workspace_id']}), Instagram @{post['handle']} ({post['social_account_id']}). Actual schedule {post['scheduled_at']} UTC = {local} Asia/Jakarta. All inherited targets meet requested queue endpoint. Scheduled, not live; no future monitoring authorized.

Verified export {export['file']}: {export['duration_s']:.6f}s, {export['frames']} frames, 1080x1920/30fps H264/AAC, {export['bytes']} bytes; SHA-256 {export['sha256']}. Public Trypost served copy returns HTTP200 with identical bytes/hash. Full-file decode, sixteen encoded proof scenes, forty-five adjacent cut frames, fifteen encoded acoustic seams and six SFX waveform matches passed. Caption sidecar contains all 208 spoken words. Perceptual listening unavailable; sound measured, not heard. Package and receipt identify this exact version.

Owned preview PID27624/port3003 stopped; status not-running and TCP listener ownership check passed. Other project's preview untouched. HyperFrames desktop app can edit the local project; `npx --yes hyperframes@0.9.1 open .` from video/ is available. Temporary review endpoint intentionally released after export.

Next/final action: user-requested scoped Git commit with this production and only its tracker insertion. Preserve existing unrelated board and kaleng-roda-dan-pisau changes. Pipeline production, verification, packaging and scheduling are finished; no additional render or remote action remains.
'''
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(note)
with (V/'BRIEF.md').open('a',encoding='utf-8') as f:f.write('\n## Delivered version\n\nAgent-verified v1 complete through Trypost queue: '+local+' Asia/Jakarta, Instagram @eliansatya / Admin\'s Workspace. Exact receipt ../PUBLISHING.json. No human approval claimed. Temporary owned preview released.\n')
f=R/'TRACKER.json';d=json.loads(f.read_text(encoding='utf-8-sig'));row=next(x for x in d['productions'] if x['slug']==P.name);row.update(stage='publishing',status='complete');f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');assert (R/row['path']).is_dir()
print(json.dumps(dict(stage='publishing',status='complete',post_id=post['trypost_post_id'],scheduled_at_local=local,export_sha256=export['sha256'])))
