from pathlib import Path
import json,sys,requests,hashlib,datetime
P=Path(__file__).resolve().parent;ticket=Path(sys.argv[1]); receipt=P/'PUBLISHING.json'
c=json.loads(ticket.read_text(encoding='utf-8'));r=json.loads(receipt.read_text(encoding='utf-8'));a=r['assets'][-1];f=P/a['local_file']
assert hashlib.sha256(f.read_bytes()).hexdigest()==a['sha256']
assert f.stat().st_size<=c['max_bytes']
try:
    with f.open('rb') as source:response=requests.post(c['upload_url'],files={c['field_name']:(f.name,source,'video/mp4')},timeout=(20,180))
    body=response.json()
    if not response.ok or 'error' in body:
        a.update(status='error',upload_http_status=response.status_code,error='Upload rejected; body checked without logging signed credentials')
        raise RuntimeError(f'Upload rejected: HTTP {response.status_code}')
    a.update(status='uploaded',upload_http_status=response.status_code,uploaded_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    print(json.dumps(dict(status='uploaded',http_status=response.status_code,response_keys=list(body))))
except requests.RequestException as e:
    a.update(status='unknown',error=type(e).__name__)
    raise RuntimeError(type(e).__name__) from None
finally:
    receipt.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');ticket.unlink(missing_ok=True)
