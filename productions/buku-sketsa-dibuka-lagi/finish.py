"""Close this queue endpoint after exact readback and public-byte verification."""
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1];V=P/'video';Q=V/'verification'
receipt=json.loads((P/'PUBLISHING.json').read_text(encoding='utf-8'));post=receipt['posts'][0];asset=receipt['assets'][0]
public=json.loads((Q/'trypost-media.json').read_text(encoding='utf-8'));export=json.loads((Q/'export.json').read_text(encoding='utf-8'));cleanup=json.loads((Q/'preview-cleanup.json').read_text(encoding='utf-8'))
assert post['status']=='scheduled' and asset['status']=='verified'
assert public['matches_local_export'] and public['sha256']==export['sha256']==asset['sha256']
assert cleanup['status']=='passed' and not cleanup['recorded_process_still_owns_port']
scheduled=datetime.fromisoformat(post['scheduled_at']).replace(tzinfo=timezone.utc);assert scheduled>datetime.now(timezone.utc)
local=scheduled.astimezone(ZoneInfo('Asia/Jakarta')).isoformat()
post['scheduled_at_local']=local;post['timezone']='Asia/Jakarta';post['verification']['public_served_media']='HTTP200, exact SHA-256 and byte count match local export'
asset['public_served_copy_verification']=dict(http_status=200,sha256=public['sha256'],bytes=public['bytes'],matches_local_export=True,evidence='video/verification/trypost-media.json')
(P/'PUBLISHING.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
note=f'''\n## Queue endpoint completed — 2026-11-04

Trypost readback confirms scheduled status, queue mode, exact caption, instagram_reel, account and attached MP4 identity. Post {post['trypost_post_id']}; media {asset['media_id']}. Workspace {post['workspace_name']} ({post['workspace_id']}), Instagram @{post['handle']} ({post['social_account_id']}). Actual schedule {post['scheduled_at']} UTC = {local} (Asia/Jakarta). All inherited targets complete. This is scheduled, not live publication; no future monitor authorized.

Export: {export['file']}, {export['duration_s']:.6f}s, 2701 frames, 1080x1920/30fps H264/AAC, {export['bytes']} bytes, SHA-256 {export['sha256']}. Public Trypost served copy returns HTTP200 and identical hash/bytes. Full decode, sixteen proof scenes, forty-five exact seam frames, fifteen encoded quiet boundaries and six SFX matches passed. Perceptual listening unavailable; sound measured, not heard. CONTENT_PACKAGE.md, exports/{P.name}.srt and PUBLISHING.json match this exact version.

Pipeline-owned preview stopped; status not-running, recorded PID no longer owns port3002. Editor project remains available locally; `npx --yes hyperframes@0.9.1 open .` from video/ opens the HyperFrames desktop app if desired. HyperFrames CLI requested technical feedback and received a clean-render report without private content or paths.

Next action: create the user-requested scoped Git commit containing this production and only its tracker insertion; preserve pre-existing unrelated tracker changes and video-nearby-copy files. No further production, upload or scheduling work remains.
'''
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(note)
with (V/'BRIEF.md').open('a',encoding='utf-8') as f:f.write('\n## Delivered result\n\nAgent-verified v1 complete through Trypost queue. '+local+' Asia/Jakarta, Instagram @eliansatya / Admin\'s Workspace. See ../PUBLISHING.json and ../EPISODE.md for exact receipt and evidence. No human approval claimed. Temporary preview released.\n')
f=R/'TRACKER.json';d=json.loads(f.read_text(encoding='utf-8-sig'));row=next(x for x in d['productions'] if x['slug']==P.name);row.update(stage='publishing',status='complete');f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');assert (R/row['path']).is_dir()
print(json.dumps(dict(stage='publishing',status='complete',post_id=post['trypost_post_id'],scheduled_at_local=local,export_sha256=export['sha256'])))
