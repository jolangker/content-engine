from pathlib import Path
import importlib.util,json,hashlib
from elevenlabs import ElevenLabs
P=Path(__file__).resolve().parent;R=P.parents[1];V=P/'video'
spec=importlib.util.spec_from_file_location('narration',R/'.agents/skills/shortform-production/scripts/narration.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
out=V/'assets/audio/rain-loop.mp3';out.parent.mkdir(parents=True,exist_ok=True)
payload=dict(text='Soft outdoor light rain landing on a tiled roof and grass, gentle scattered water droplets, intimate miniature garden atmosphere, steady fine rainfall, no thunder, no wind gusts, no voices, no music.',model_id='eleven_text_to_sound_v2',duration_seconds=12,prompt_influence=.55,loop=True)
identity=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest();receipt=out.with_suffix('.json')
if out.exists() and receipt.exists() and json.loads(receipt.read_text())['request_sha256']==identity:print('Reused verified requested rain loop.');raise SystemExit(0)
try:
    key=mod.read_env(R).get('ELEVENLABS_API_KEY')
    if not key:raise ValueError('Missing project ElevenLabs key')
    client=ElevenLabs(api_key=key)
    audio=client.text_to_sound_effects.convert(**payload,output_format='mp3_44100_128',request_options={'max_retries':0,'timeout_in_seconds':120})
    data=b''.join(audio);out.write_bytes(data)
    receipt.write_text(json.dumps(dict(provider='elevenlabs',request=payload,request_sha256=identity,audio_sha256=hashlib.sha256(data).hexdigest(),gap='Reuse scan had no rain/water asset; resolver returned chime, rejected as a semantic mismatch.'),indent=2),encoding='utf-8')
    print('Generated one 12-second looping rain effect; no retry or alternate provider.')
except Exception as e:
    print(json.dumps(dict(error=type(e).__name__,status_code=getattr(e,'status_code',None))));raise SystemExit(1)
