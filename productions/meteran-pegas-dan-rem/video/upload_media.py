"""Upload exact verified bytes using an ephemeral signed payload, never log secrets."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,requests,sys
V=Path(__file__).resolve().parent;P=V.parent
private=Path(sys.argv[1]);payload=json.loads(private.read_text(encoding='utf-8'));private.unlink()
receipt=json.loads((P/'PUBLISHING.json').read_text(encoding='utf-8'));a=receipt['assets'][0];f=P/a['local_file']
assert hashlib.sha256(f.read_bytes()).hexdigest()==a['sha256']
try:
 with f.open('rb') as stream:res=requests.post(payload['upload_url'],files={payload.get('field_name','media'):(f.name,stream,'video/mp4')},timeout=300)
 # Never print request URL or signed request body.
 if not res.ok:raise RuntimeError('Upload rejected: HTTP '+str(res.status_code))
 body=res.json();a.update(status='uploaded',uploaded_at=datetime.now(timezone.utc).isoformat())
 (P/'PUBLISHING.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='uploaded',http_status=res.status_code,bytes=f.stat().st_size,response_keys=list(body))))
except Exception as error:
 a.update(status='unknown',error=type(error).__name__)
 (P/'PUBLISHING.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 raise RuntimeError('Upload outcome requires reconciliation; '+type(error).__name__) from None
