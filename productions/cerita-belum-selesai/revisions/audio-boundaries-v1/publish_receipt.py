from pathlib import Path
import json,sys,datetime
P=Path(__file__).resolve().parent;path=P/'PUBLISHING.json';r=json.loads(path.read_text(encoding='utf-8'));o=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'));now=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=r['posts'][-1];a=r['assets'][-1]
p.setdefault('observations',[]).append(dict(observed_at=now,event=sys.argv[2],status=o.get('status'),publish_status=o.get('publish_status'),error_message=o.get('error_message')))
p.update(trypost_post_id=o['id'],status=o['status'],provider_status=o['status'],publish_status=o.get('publish_status'),observed_at=now,scheduled_at=o.get('scheduled_at'),published_at=o.get('published_at'),service_url=o.get('platform_url'),error_message=o.get('error_message'),observed_content=o.get('content'),observed_content_type=o.get('content_type'),observed_meta=o.get('meta'),created_at=o.get('created_at'),media_ids=[m['id'] for m in o.get('media',[])])
if o.get('social_account'):p['observed_account']=o['social_account']
if o.get('media'):
    m=o['media'][0];a.update(status='attached',media_id=m['id'],trypost_post_id=o['id'],attached_at=a.get('attached_at',now),observed_media=m)
if a.get('public_media_check',{}).get('status')=='verified':a['status']='verified'
expected=(P/'publish-caption.txt').read_text(encoding='utf-8').replace('\r\n','\n')
actual=o.get('content','').replace('\r\n','\n')
p['content_matches_package']=actual==expected
path.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert o.get('social_account',{}).get('id')==p['social_account_id']
assert o.get('content_type')==p['content_type'] and len(o.get('media',[]))==1
assert o['media'][0]['size']==a['bytes'] and o['media'][0]['meta']['duration']==86
if '--require-content' in sys.argv:assert p['content_matches_package'],'Caption mismatch'
print(json.dumps(dict(post_id=p['trypost_post_id'],status=p['status'],content_matches_package=p['content_matches_package'],media_id=a.get('media_id'))))
