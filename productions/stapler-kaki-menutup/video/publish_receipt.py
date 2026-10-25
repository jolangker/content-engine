from pathlib import Path
import json,hashlib,datetime,sys
V=Path(__file__).resolve().parent;P=V.parent;R=P.parents[1];receipt=P/'PUBLISHING.json'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(d):receipt.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if sys.argv[1]=='prepare':
    assert not receipt.exists(),'Reconcile existing attempt before preparing another'
    export=json.loads((V/'verification/export.json').read_text());assert sha(P/export['file'])==export['sha256']
    target=json.loads((R/'boards/di-balik-benda/ACCOUNTS.json').read_text())['accounts'][0]
    content=(P/'publish-caption.txt').read_text(encoding='utf-8');assert len(content)<=2200 and len([w for w in content.split() if w.startswith('#')])<=5
    payload={**target,'content':content,'content_type':'instagram_reel','media':{'export_sha256':export['sha256'],'cover_offset_ms':2000},'requested_delivery':'queue','queue':'next','requested_due_at':None}
    ph=hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    save({'schema_version':2,'assets':[{'provider':'trypost','workspace_id':target['workspace_id'],'local_file':export['file'],'sha256':export['sha256'],'bytes':export['bytes'],'status':'planned','source':'local_upload','attempt_started_at':now()}],'posts':[{**target,'content_type':'instagram_reel','export_sha256':export['sha256'],'payload_sha256':ph,'payload':payload,'requested_delivery':'queue','requested_due_at':None,'attempt_started_at':now(),'status':'planned'}]})
    print(json.dumps({'status':'planned','export_sha256':export['sha256'],'payload_sha256':ph}))
elif sys.argv[1]=='uploaded':
    d=json.loads(receipt.read_text());d['assets'][0].update(status='uploaded',uploaded_at=now());save(d);print('Upload receipt saved without temporary credentials')
elif sys.argv[1]=='record':
    observed=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8-sig'));d=json.loads(receipt.read_text());post=d['posts'][0]
    # Use exact provider-returned structures; no fabricated URLs or guessed IDs.
    body=observed.get('post',observed);post.update(trypost_post_id=body['id'],status=body['status'],scheduled_at=body.get('scheduled_at'),published_at=body.get('published_at'),observed_at=now(),provider_result=body)
    if body.get('content')!=post['payload']['content']:
        assert body['content'].replace('\r\n','\n')==post['payload']['content'].replace('\r\n','\n'),'Caption changed beyond transport line endings'
        post.setdefault('payload_history',[]).append({'payload':json.loads(json.dumps(post['payload'])),'payload_sha256':post['payload_sha256'],'reason':'Original local LF intent; exact submitted/read-back content uses CRLF from shell transport.'})
        post['payload']['content']=body['content'];post['payload_sha256']=hashlib.sha256(json.dumps(post['payload'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    media=body.get('media',[]);post['media_ids']=[m['id'] for m in media if 'id' in m]
    asset=d['assets'][0];asset.update(status='verified' if media else 'uploaded',trypost_post_id=body['id'],attached_at=now(),verified_at=now())
    if media:asset['media_id']=media[0]['id']
    save(d);print(json.dumps({'post_id':body['id'],'status':body['status'],'scheduled_at':body.get('scheduled_at'),'media_ids':post['media_ids']}))
