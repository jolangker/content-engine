from pathlib import Path
import json,sys,datetime
B=Path(__file__).resolve().parent;path=B/'PUBLISHING.json';r=json.loads(path.read_text(encoding='utf-8'));o=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'));now=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=r['posts'][-1];a=r['assets'][-1]
p.update(trypost_post_id=o['id'],status=o['status'],provider_status=o['status'],publish_status=o.get('publish_status'),observed_at=now,scheduled_at=o.get('scheduled_at'),published_at=o.get('published_at'),service_url=o.get('platform_url'),error_message=o.get('error_message'),observed_content=o.get('content'),observed_content_type=o.get('content_type'),observed_meta=o.get('meta'),created_at=o.get('created_at'),media_ids=[m['id'] for m in o.get('media',[])])
p.setdefault('observations',[]).append(dict(observed_at=now,event=sys.argv[2],status=o['status']))
p['observed_account']=o.get('social_account');p['content_matches_package']=o.get('content','').replace('\r\n','\n')==(B/'publish-caption.txt').read_text(encoding='utf-8').replace('\r\n','\n')
if o.get('media'):
    media=o['media'][0];a.update(status='attached',media_id=media['id'],trypost_post_id=o['id'],attached_at=a.get('attached_at',now),observed_media=media)
path.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert o['status']=='draft' and p['content_matches_package']
assert o.get('social_account',{}).get('id')==p['social_account_id'] and o['content_type']==p['content_type'] and len(o['media'])==1
assert media['size']==a['bytes'] and abs(media['meta']['duration']-a['duration_s'])<1.05
assert o.get('scheduled_at') is None and o.get('published_at') is None
print(json.dumps(dict(post_id=o['id'],status=o['status'],media_id=media['id'],caption_verified=True)))
