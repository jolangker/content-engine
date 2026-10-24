from pathlib import Path
import json,sys,hashlib,datetime,requests,re
V=Path(__file__).resolve().parent;P=V.parent
token=Path(sys.argv[1]);receipt=P/'PUBLISHING.json'
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(d):receipt.write_text(json.dumps(d,indent=2),encoding='utf-8')
try:
    creds=json.loads(token.read_text(encoding='utf-8'))
    d=json.loads(receipt.read_text(encoding='utf-8'));a=d['assets'][0];src=P/a['local_file']
    assert hashlib.sha256(src.read_bytes()).hexdigest()==a['sha256']
    fields=dict(creds['upload_params']);assert fields['public_id']==a['public_id']
    if fields['overwrite'] is not False:
        assert re.search(r'-[0-9a-f]{32}$',a['public_id']) and a.get('collision_preflight',{}).get('total_count')==0
        assert a.get('requested_overwrite') is False and a.get('signing_note')
    a['signed_overwrite']=fields['overwrite']
    fields={k:('true' if v else 'false') if isinstance(v,bool) else v for k,v in fields.items()}
    fields.update(api_key=creds['api_key'],signature=creds['signature'])
    host=creds['host'].removeprefix('https://').rstrip('/')
    a['attempt_started_at']=now();save(d)
    try:
        with src.open('rb') as f:
            r=requests.post(f'https://{host}/v1_1/{creds["cloud_name"]}/video/upload',data=fields,files={'file':(src.name,f,'video/mp4')},timeout=(20,180))
    except requests.RequestException:
        a.update(status='unknown',error='Upload transport outcome unknown; search exact public_id before retry.');save(d);raise
    result=r.json()
    if not r.ok or 'error' in result:
        a.update(status='error',http_status=r.status_code,error=result.get('error'));save(d);raise RuntimeError('Cloudinary upload rejected; see receipt')
    a.update(status='uploaded',asset_id=result['asset_id'],resource_type=result['resource_type'],secure_url=result['secure_url'],uploaded_at=result.get('created_at'),remote_bytes=result.get('bytes'),width=result.get('width'),height=result.get('height'),duration=result.get('duration'));save(d)
    assert result['public_id']==a['public_id'];assert result['bytes']==a['bytes'];assert (result['width'],result['height'])==(1080,1920)
    h=hashlib.sha256();n=0
    with requests.get(a['secure_url'],stream=True,timeout=(20,180)) as remote:
        remote.raise_for_status();content_type=remote.headers.get('Content-Type','');assert content_type.startswith('video/')
        for chunk in remote.iter_content(1024*1024):h.update(chunk);n+=len(chunk)
    assert n==a['bytes'];assert h.hexdigest()==a['sha256']
    a.update(status='verified',verified_at=now(),remote_sha256=h.hexdigest(),content_type=content_type);save(d)
    print(json.dumps(dict(status=a['status'],asset_id=a['asset_id'],secure_url=a['secure_url'],bytes=n,sha256=h.hexdigest())))
finally:
    token.unlink(missing_ok=True)
