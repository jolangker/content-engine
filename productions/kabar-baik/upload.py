"""Upload this verified original using a one-use MCP signing credential outside the repository."""
from pathlib import Path
import json,sys,requests,hashlib,datetime
P=Path(__file__).resolve().parent
credential=Path(sys.argv[1]); c=json.loads(credential.read_text(encoding='utf-8-sig'))
receipt_path=P/'PUBLISHING.json';r=json.loads(receipt_path.read_text(encoding='utf-8'));a=r['assets'][-1]
f=P/a['local_file'];assert hashlib.sha256(f.read_bytes()).hexdigest()==a['sha256']
assert c['upload_params']['public_id']==a['public_id']
signed_overwrite=c['upload_params']['overwrite']
if str(signed_overwrite).lower() not in ('false','0'):
    assert a.get('preflight',{}).get('exact_public_id_absent') is True
    assert a.get('requested_overwrite') is False
    assert a['public_id'].endswith(a['unique_suffix'])
a['signed_overwrite']=signed_overwrite
form={k:(str(v).lower() if isinstance(v,bool) else v) for k,v in c['upload_params'].items()}
form.update(api_key=c['api_key'],signature=c['signature'])
url=f'https://{c["host"]}/v1_1/{c["cloud_name"]}/video/upload'
try:
    with f.open('rb') as source:
        response=requests.post(url,data=form,files={'file':(f.name,source,'video/mp4')},timeout=(20,180))
    body=response.json()
    if not response.ok or 'error' in body:
        a.update(status='error',error=body,http_status=response.status_code)
        receipt_path.write_text(json.dumps(r,indent=2),encoding='utf-8')
        raise RuntimeError(f'Cloudinary upload rejected: HTTP {response.status_code}')
    a.update(status='uploaded',asset_id=body['asset_id'],public_id=body['public_id'],resource_type=body['resource_type'],secure_url=body['secure_url'],uploaded_at=body['created_at'],remote_bytes=body['bytes'],width=body['width'],height=body['height'],duration=body['duration'])
    receipt_path.write_text(json.dumps(r,indent=2),encoding='utf-8')
finally:
    credential.unlink(missing_ok=True)
download=requests.get(a['secure_url'],stream=True,timeout=(20,180));download.raise_for_status()
assert 'video/' in download.headers.get('content-type','')
h=hashlib.sha256();size=0
for chunk in download.iter_content(1024*1024):h.update(chunk);size+=len(chunk)
assert size==a['bytes'] and h.hexdigest()==a['sha256'],'Hosted original differs from verified local file'
a.update(status='verified',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),download_sha256=h.hexdigest(),download_bytes=size,content_type=download.headers.get('content-type'))
receipt_path.write_text(json.dumps(r,indent=2),encoding='utf-8')
print(json.dumps(dict(status=a['status'],secure_url=a['secure_url'],bytes=size,sha256=h.hexdigest())))
