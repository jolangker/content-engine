"""Persist planned and observed Trypost states without upload credentials."""
from pathlib import Path
import json,hashlib,datetime,sys,re,requests
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2];receipt=P/'PUBLISHING.json'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fingerprint(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def save(d):receipt.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
mode=sys.argv[1]
if mode=='prepare':
    assert not receipt.exists(),'Reconcile the existing attempt first'
    export=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));assert sha(P/export['file'])==export['sha256']
    ep=(P/'EPISODE.md').read_text(encoding='utf-8');match=re.search(r'## Publishing targets\s+```json\s*(.*?)```',ep,re.S);targets=json.loads(match.group(1))['accounts'];assert len(targets)==1
    target=targets[0];content=(P/'CAPTION.txt').read_text(encoding='utf-8').strip();assert len(content)<=2200
    payload={**target,'content':content,'content_type':'instagram_reel','media':{'export_sha256':export['sha256']},'meta':{},'requested_delivery':'queue','queue':'next','requested_due_at':None}
    d=dict(schema_version=2,assets=[dict(provider='trypost',workspace_id=target['workspace_id'],local_file=export['file'],sha256=export['sha256'],bytes=export['bytes'],status='planned',source='local_upload',attempt_started_at=now())],posts=[{**target,'content_type':'instagram_reel','export_sha256':export['sha256'],'payload_sha256':fingerprint(payload),'payload':payload,'requested_delivery':'queue','requested_due_at':None,'attempt_started_at':now(),'status':'planned'}]);save(d)
    t=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));next(x for x in t['productions'] if x['slug']==P.name).update(stage='publishing',status='in_progress');(R/'TRACKER.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='planned',sha256=export['sha256'],payload_sha256=fingerprint(payload))))
elif mode=='uploaded':
    d=json.loads(receipt.read_text(encoding='utf-8'));d['assets'][0].update(status='uploaded',uploaded_at=now());save(d);print('Upload outcome saved without temporary credentials')
elif mode=='record':
    observed=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8-sig'));body=observed.get('post',observed);d=json.loads(receipt.read_text(encoding='utf-8'));post=d['posts'][0]
    assert body['content'].replace('\r\n','\n').strip()==post['payload']['content'].replace('\r\n','\n').strip(),'Provider copy mismatch'
    assert body.get('content_type')=='instagram_reel'
    if body['content']!=post['payload']['content']:
        post.setdefault('payload_history',[]).append(dict(payload=post['payload'].copy(),payload_sha256=post['payload_sha256'],reason='Original local newline intent retained; provider readback newline normalization only'))
        post['payload']['content']=body['content'];post['payload_sha256']=fingerprint(post['payload'])
    if post.get('provider_result') and post['provider_result'].get('content')!=body['content']:
        post.setdefault('provider_history',[]).append(dict(observed=post['provider_result'],reason=post.get('copy_error','prior provider readback retained')))
    post.update(trypost_post_id=body['id'],status=body['status'],scheduled_at=body.get('scheduled_at'),published_at=body.get('published_at'),observed_at=now(),provider_result=body,copy_verified=True)
    if post.get('copy_error'):post['copy_correction']=post.pop('copy_error')
    media=body.get('media',[]);post['media_ids']=[m['id'] for m in media if 'id' in m]
    assert len(media)==1 and media[0]['type']=='video'
    asset=d['assets'][0];asset.update(status='attached',trypost_post_id=body['id'],attached_at=now(),media_id=media[0]['id'],public_url=media[0]['url']);save(d)
    print(json.dumps(dict(post_id=body['id'],status=body['status'],scheduled_at=body.get('scheduled_at'),media_ids=post['media_ids'])))
elif mode=='public':
    d=json.loads(receipt.read_text(encoding='utf-8'));asset=d['assets'][0];url=asset['public_url'];r=requests.get(url,stream=True,timeout=90);r.raise_for_status();h=hashlib.sha256();size=0
    for part in r.iter_content(1024*1024):h.update(part);size+=len(part)
    assert h.hexdigest()==asset['sha256'] and size==asset['bytes']
    asset.update(status='verified',verified_at=now(),public_http_status=r.status_code,public_sha256=h.hexdigest(),public_bytes=size);save(d);print(json.dumps(dict(http=r.status_code,bytes=size,sha256=h.hexdigest(),match=True)))
elif mode=='complete':
    d=json.loads(receipt.read_text(encoding='utf-8'));assert all(a['status']=='verified' for a in d['assets']);assert all(p['status'] in ('scheduled','published') for p in d['posts']);post=d['posts'][0]
    due=datetime.datetime.fromisoformat(post['scheduled_at']).replace(tzinfo=datetime.timezone.utc);local=due.astimezone(datetime.timezone(datetime.timedelta(hours=7)))
    assert post['status']=='published' or due>datetime.datetime.now(datetime.timezone.utc)
    with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Queue delivery completed\nTrypost post {post["trypost_post_id"]}, observed {post["status"]}; actual schedule {post["scheduled_at"]} UTC / {local.isoformat()} Asia/Jakarta. Exact caption, instagram_reel type, account and attached media read back. Public served MP4 HTTP 200, bytes and SHA-256 equal the verified local export. Endpoint is scheduling, not a claim of live publication. Receipt: PUBLISHING.json. No future monitoring started. Next: requested repository commit after completed pipeline.\n')
    t=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));next(x for x in t['productions'] if x['slug']==P.name).update(stage='publishing',status='complete');(R/'TRACKER.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=post['status'],scheduled_utc=post['scheduled_at'],scheduled_jakarta=local.isoformat(),post_id=post['trypost_post_id'])))
