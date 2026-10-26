"""Read a temporary one-shot upload contract without printing signed credentials."""
from pathlib import Path
import json,os,requests,sys
V=Path(__file__).resolve().parent;P=V.parent
tmp=Path(os.environ['TEMP'])/'codex-seatbelt-upload.json';contract=json.loads(tmp.read_text(encoding='utf-8-sig'));report=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));video=P/report['file']
assert video.stat().st_size<=min(contract['max_bytes'],314572800)
with video.open('rb') as f:r=requests.post(contract['upload_url'],files={contract.get('field_name','media'):(video.name,f,'video/mp4')},timeout=180)
try:body=r.json()
except ValueError:body={}
if r.status_code>=400:print(json.dumps(dict(http_status=r.status_code,error=body.get('message','upload rejected'))));sys.exit(1)
if body.get('error') or body.get('success') is False:print(json.dumps(dict(http_status=r.status_code,error='provider reported upload failure')));sys.exit(1)
print(json.dumps(dict(http_status=r.status_code,uploaded_bytes=video.stat().st_size,response_keys=list(body.keys()),success=True)))
