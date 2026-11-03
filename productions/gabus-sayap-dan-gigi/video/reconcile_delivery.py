"""Persist an observed Trypost result without inventing a provider URL or status."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys
V=Path(__file__).resolve().parent;P=V.parent
result=json.loads((V/sys.argv[1]).read_text(encoding='utf-8'))
if 'structuredContent' in result:result=result['structuredContent']
if 'post' in result:result=result['post']
receipt=json.loads((P/'PUBLISHING.json').read_text(encoding='utf-8'));post=receipt['posts'][0];asset=receipt['assets'][0]
post_id=result.get('id');assert post_id,'Missing provider post ID'
if post.get('trypost_post_id'):assert post['trypost_post_id']==post_id
status=result.get('status');assert status in ['draft','scheduled','pending_approval','publishing','published','failed']
post.update(trypost_post_id=post_id,status=status,provider_status=status,last_verified_at=datetime.now(timezone.utc).isoformat(),observed=result)
for key in ['scheduled_at','published_at','platform_url','service_url','error_message','schedule_mode']:
 if key in result:post[key]=result[key]
media=result.get('media',[])
if media:
 ids=[str(x['id']) for x in media if isinstance(x,dict) and x.get('id')];assert ids
 post['media_ids']=ids;asset.update(status='verified',media_id=ids[0],trypost_post_id=post_id,verified_at=post['last_verified_at'])
(P/'PUBLISHING.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(post_id=post_id,status=status,scheduled_at=post.get('scheduled_at'),media_ids=post.get('media_ids'))))
