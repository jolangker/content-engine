"""Read an ephemeral signed descriptor outside the repo; do not log its values."""
from pathlib import Path
import json,sys,requests,hashlib,datetime
V=Path(__file__).resolve().parent;P=V.parent
config=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'));receipt=json.loads((P/'PUBLISHING.json').read_text(encoding='utf-8'));asset=receipt['assets'][0];file=P/asset['local_file']
assert asset['status']=='planned' and hashlib.sha256(file.read_bytes()).hexdigest()==asset['sha256']
assert file.stat().st_size<=min(config['max_bytes'],314572800)
def save(): (P/'PUBLISHING.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
try:
 with file.open('rb') as stream:r=requests.post(config['upload_url'],files={config.get('field_name','media'):(file.name,stream,'video/mp4')},timeout=180)
 body=r.json();success=r.status_code in (200,201) and not body.get('error')
 if not success:
  asset.update(status='error',error='Upload refused, HTTP '+str(r.status_code));save();raise SystemExit(asset['error'])
 asset.update(status='uploaded',uploaded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),upload_http_status=r.status_code);save()
 print(json.dumps(dict(status='uploaded',http_status=r.status_code,bytes=file.stat().st_size)))
except requests.RequestException as e:
 asset.update(status='unknown',error='Upload transport outcome unknown: '+type(e).__name__);save();raise SystemExit(asset['error'])
