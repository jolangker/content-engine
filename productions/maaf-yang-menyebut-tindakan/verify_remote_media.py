"""Verify public served bytes without changing the queued post or deployment."""
from pathlib import Path
import hashlib,json,sys,urllib.request,urllib.error
P=Path(__file__).resolve().parent
url=sys.argv[1]
request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
try:
    with urllib.request.urlopen(request,timeout=40) as response:
        data=response.read();status=response.status
    expected=json.loads((P/'video/verification/export.json').read_text(encoding='utf-8'))
    record=dict(status='passed',http_status=status,public_media_access=True,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),matches_local_export=hashlib.sha256(data).hexdigest()==expected['sha256'])
    assert record['matches_local_export'] and record['bytes']==expected['bytes']
except urllib.error.HTTPError as e:
    record=dict(status='error',http_status=e.code,public_media_access=False,response_server=e.headers.get('Server'),content_type=e.headers.get('Content-Type'),body_excerpt=e.read(1000).decode(errors='replace'))
(P/'video/verification/trypost-media.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record));raise SystemExit(0 if record['status']=='passed' else 1)
