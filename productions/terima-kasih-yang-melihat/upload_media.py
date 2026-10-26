"""POST a signed one-shot upload; never persist or print the signed URL/token."""
import base64
import json
from pathlib import Path
import sys
import urllib.error
import urllib.request
import uuid

def clean(obj):
    if isinstance(obj,dict):return {k:clean(v) for k,v in obj.items() if not any(s in k.lower() for s in ('token','signature','url','secret','authorization'))}
    if isinstance(obj,list):return [clean(v) for v in obj]
    if isinstance(obj,str) and ('http://' in obj or 'https://' in obj):return '[URL withheld]'
    return obj

def main():
    config=json.loads(base64.b64decode(sys.argv[1]))
    f=Path(config['file']);boundary='media-'+uuid.uuid4().hex
    head=(f'--{boundary}\r\nContent-Disposition: form-data; name="{config["field_name"]}"; filename="{f.name}"\r\nContent-Type: video/mp4\r\n\r\n').encode()
    body=head+f.read_bytes()+f'\r\n--{boundary}--\r\n'.encode()
    request=urllib.request.Request(config['upload_url'],data=body,headers={'Content-Type':f'multipart/form-data; boundary={boundary}'},method='POST')
    try:
        with urllib.request.urlopen(request,timeout=180) as response:
            raw=response.read();status=response.status
        parsed=json.loads(raw)
        if not 200<=status<300 or parsed.get('error') or parsed.get('success') is False:
            print(json.dumps({'status':'error','http_status':status,'response':clean(parsed)}));return 1
        print(json.dumps({'status':'uploaded','http_status':status,'response':clean(parsed)}))
        return 0
    except urllib.error.HTTPError as e:
        try:detail=clean(json.loads(e.read()))
        except Exception:detail='Non-JSON error body withheld'
        print(json.dumps({'status':'error','http_status':e.code,'response':detail}));return 1
    except Exception as e:
        print(json.dumps({'status':'unknown','error_class':type(e).__name__}));return 1
if __name__=='__main__':raise SystemExit(main())
