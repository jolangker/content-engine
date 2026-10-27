from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parent;rp=P/'PUBLISHING.json';r=json.loads(rp.read_text(encoding='utf-8-sig'))
a=r['assets'][-1];assert a['status']=='verified' and a['download_sha256']==a['sha256']
if r['posts']:raise RuntimeError('Reconcile existing post attempt before creating')
payload=dict(channelId='6ad6400e778b240e2f5a8060',text=(P/'caption.txt').read_text(encoding='utf-8').strip(),assets=[dict(video=dict(url=a['secure_url'],metadata=dict(thumbnailOffset=5357)))],metadata=dict(instagram=dict(type='reel',shouldShareToFeed=True,isAiGenerated=True)),mode='addToQueue',saveToDraft=True,schedulingType='automatic')
fingerprint=hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
post=dict(organization_id='691274923530437a1a02ed9f',organization_name='My Organization',channel_id=payload['channelId'],service='instagram',handle='eliansatya',export_sha256=a['sha256'],payload_sha256=fingerprint,requested_delivery='draft',requested_due_at=None,attempt_started_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='planned',payload=payload,duplicate_preflight='Fresh list_posts on target channel, all statuses, created after 2026-10-20T08:35:00Z returned no posts and no additional page; no previous creation exists for this production.')
r['posts'].append(post);rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(payload,ensure_ascii=False))
