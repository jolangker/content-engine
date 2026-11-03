"""Verify public exact bytes and read-back identity before completing queue delivery."""
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import json,hashlib,requests
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
intent=json.loads((V/'posting-intent.json').read_text(encoding='utf-8'));post=json.loads((V/'remote-post-verified.json').read_text(encoding='utf-8'));receipt=json.loads((P/'PUBLISHING.json').read_text(encoding='utf-8'));asset=receipt['assets'][0];record=receipt['posts'][0]
assert post['status']=='scheduled' and post['schedule_mode']=='queue'
assert post['social_account']['id']==intent['social_account_id'] and post['social_account']['username']=='dibalikbenda.id' and post['platform']=='instagram'
assert post['content']==intent['content'] and post['content_type']=='instagram_reel'
assert len(post['media'])==1 and post['media'][0]['id']==asset['media_id']
scheduled=datetime.fromisoformat(post['scheduled_at']).replace(tzinfo=timezone.utc)
assert scheduled>datetime.now(timezone.utc)
media=post['media'][0];response=requests.get(media['url'],timeout=90);response.raise_for_status()
served=hashlib.sha256(response.content).hexdigest()
assert len(response.content)==asset['bytes'] and served==asset['sha256']
asset.update(served_url=media['url'],public_http_status=response.status_code,served_bytes=len(response.content),served_sha256=served)
stamp=datetime.now(timezone.utc).isoformat();local=scheduled.astimezone(ZoneInfo('Asia/Jakarta')).isoformat()
record.update(scheduled_at_local=local,timezone='Asia/Jakarta',completion_evidence='Read-back confirms exact inherited connected account, caption, Reel type, one attached media and queue schedule; unauthenticated public media GET matches exact export bytes and SHA256.',verified_at=stamp)
receipt['completed_at']=stamp
(P/'PUBLISHING.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Queue delivery complete\nTrypost Admin\'s Workspace, Instagram @dibalikbenda.id. Post {post["id"]}, observed scheduled / queue, UTC {post["scheduled_at"]}, local {local}. Exact copy/type/account/media read back; public HTTP200 copy has identical{asset["bytes"]}bytes and SHA256{served}. Receipt: PUBLISHING.json. Scheduling complete; publication is future and not monitored. No live publication claimed.\n\nExport verification:90.000s,2700frames,1080x1920,30fps,H.264/yuv420p,AAC48kHz; full decode passed. Agent inspected all16 decoded proof frames. All16 encoded SFX matches within0.334ms;15 encoded acoustic boundaries passed. Mix-13.7LUFS,-1.7dBTP,zero clipping. Listening unavailable. Pipeline preview stopped; final status not-running, PID8896 gone and port3002 no listener.\n\nNext action: requested Git commit, excluding pre-existing work on video-nearby-copy and unrelated tracker text. Video remains editable through HyperFrames; renderer suggested hyperframes open . for desktop editing.\n')
with (V/'REVIEW.md').open('a',encoding='utf-8') as f:f.write(f'\n## Export and delivery evidence\nVerified90s/2700frames, H.264/AAC, full decode and16 decoded proof frames. Audio-13.7LUFS/-1.7dBTP with zero clipping; all16 cue matches and15 encoded boundaries pass. Export SHA256{served}. Pipeline preview stopped and listener/process absence verified. Queue read-back and public exact-byte verification pass; actual schedule{local}. This is scheduled, not a claim of publication.\n')
t=R/'TRACKER.json';tracker=json.loads(t.read_text(encoding='utf-8'));next(x for x in tracker['productions'] if x['slug']==P.name).update(stage='publishing',status='complete');t.write_text(json.dumps(tracker,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all((R/x['path']).is_dir() for x in tracker['productions'])
print(json.dumps(dict(status='complete',post_id=post['id'],scheduled_at_local=local,public_http_status=response.status_code,served_sha256=served)))
