from pathlib import Path
import json,requests,hashlib,datetime
P=Path(__file__).resolve().parent;receipt=P/'PUBLISHING.json';r=json.loads(receipt.read_text(encoding='utf-8'));a=r['assets'][-1];url=a['observed_media']['url'];now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
headers={'User-Agent':'Mozilla/5.0'}
response=requests.get(url,headers=headers,timeout=(20,120));response.raise_for_status()
assert response.headers.get('Content-Type','').startswith('video/')
sha=hashlib.sha256(response.content).hexdigest();assert sha==a['sha256'] and len(response.content)==a['bytes'],'Public served video differs from verified export'
sample=requests.get(url,headers={**headers,'Range':'bytes=0-1023'},timeout=(20,40));sample.raise_for_status()
assert sample.status_code==206 and sample.content==response.content[:1024]
a.update(status='verified',verified_at=now(),public_media_check=dict(status='verified',checked_at=now(),url=url,http_status=response.status_code,bytes=len(response.content),sha256=sha,range_http_status=sample.status_code,content_range=sample.headers.get('Content-Range')))
p=r['posts'][-1]
assert p['status']=='draft' and p['content_matches_package']
p['publication_started_at']=now()
old=dict(payload=p['payload'],payload_sha256=p['payload_sha256'])
p.setdefault('payload_history',[]).append(old)
p['payload']={**p['payload'],'media_source':{**p['payload']['media_source'],'media_id':a['media_id']}}
p['payload_sha256']=hashlib.sha256(json.dumps(p['payload'],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
receipt.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(public_media='verified',bytes=len(response.content),sha256=sha,range_status=sample.status_code,post_id=p['trypost_post_id'],caption_verified=True)))
