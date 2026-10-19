"""Read-only check of the configured ElevenLabs model and voice; never print keys."""
from pathlib import Path
import json
import os
import urllib.request
import urllib.error

prod=Path(__file__).resolve().parent
root=prod.parents[1]
for raw in (root/'.env').read_text(encoding='utf-8-sig').splitlines():
    line=raw.strip()
    if not line or line.startswith('#') or '=' not in line:
        continue
    k,v=line.removeprefix('export ').split('=',1)
    os.environ.setdefault(k.strip(),v.strip().strip('\"\''))
key=os.environ.get('ELEVENLABS_API_KEY','')
if not key:
    raise SystemExit('ELEVENLABS_API_KEY is not configured')
result={'requested_model':'eleven_v4','requested_voice':'nPczCjzI2devNBz1zQrb'}
def get(path):
    req=urllib.request.Request('https://api.elevenlabs.io'+path,headers={'xi-api-key':key})
    try:
        with urllib.request.urlopen(req,timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        return {'error_status':e.code,'detail':e.read().decode('utf-8','replace').replace(key,'[redacted]')}
models=get('/v1/models')
if isinstance(models,list):
    result['available_model_ids']=[m.get('model_id') for m in models]
    result['model_available']=any(m.get('model_id')=='eleven_v4' for m in models)
else:
    result['models_error']=models
voice=get('/v1/voices/nPczCjzI2devNBz1zQrb')
result['voice_name']=voice.get('name')
if 'error_status' in voice:
    result['voice_error']=voice
(prod/'video'/'elevenlabs_preflight.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
