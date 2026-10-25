from pathlib import Path
import json,importlib.util,re,hashlib,subprocess,sys
V=Path(__file__).resolve().parent;ROOT=V.parents[2]
spec=importlib.util.spec_from_file_location('narration',ROOT/'.agents/skills/shortform-production/scripts/narration.py');n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
plan=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'))
voice,provenance=n.resolve_voice(ROOT)
tags={0:'[curious, conversational]',1:'[calm, explaining]',5:'[quietly pleased]',6:'[briefly surprised, dry humor]',7:'[clear, practical]',11:'[warm, satisfied]'}
text='\n\n'.join((tags.get(i,'')+' '+s['vo']).strip() for i,s in enumerate(plan))
request=dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=provenance,tts_model='eleven_v4',speed=1,lines=[dict(id='narration',text=text)],bgm=dict(mode='none'))
(V/'audio_request.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if '--prepare-only' in sys.argv:print(json.dumps(n.synthesize(V,ROOT,check=True)));raise SystemExit
print(json.dumps(n.synthesize(V,ROOT)),flush=True)

from elevenlabs import ElevenLabs
client=ElevenLabs(api_key=n.read_env(ROOT)['ELEVENLABS_API_KEY'])
items=[
('steel-contact',2.0,'One heavy steel rail being lowered and coming to rest with a dull metallic clunk and a brief realistic metallic resonance. Close dry Foley, no voices, no music.'),
('concrete-set',2.0,'One heavy concrete sleeper carefully lowered onto a gravel bed: short coarse scrape then solid muted stone contact. Dry realistic construction Foley, no voices, no music.'),
('clip-seat',1.5,'A strong small steel spring rail fastening clip slides into position and seats with one short firm metal clack. Close dry real material Foley, no cartoon ping, no music.'),
('ballast-pour',4.0,'Crushed angular stone gravel poured onto a pile: a dense rough cascade of small sharp stone contacts, then settling crunches. Dry close construction Foley, no machine engine, no voices, no music.'),
('chair',2.0,'A folding metal and fabric outdoor chair unfolds with short hinge friction, one latch clack and a brief restrained fabric creak. Real dry Foley, no music, no voices.'),
('splash',1.5,'One work boot steps into a shallow puddle on concrete with a brief wet splat and tiny splashes, then stillness. Close dry Foley, no voices, no music.'),
('drain-water',4.0,'A small stream of water trickles through an open concrete drainage channel, close detailed water texture with a few light drips. No music, no voices.'),
('tamping',3.0,'Short railway maintenance tamping action: hydraulic mechanism lowers, rapid coarse metallic vibration and gravel compression, then stops. Dry close mechanical Foley without music or voices.'),
('train-pass',5.0,'A short pass of a modern train at moderate speed, wheels rolling on continuous welded steel rail, low rumble and airy pass, no horn, no music, no voices.'),
]
asset_dir=V/'assets/audio/sfx';asset_dir.mkdir(parents=True,exist_ok=True)
for id,dur,prompt in items:
    p=asset_dir/f'{id}.mp3';receipt=p.with_suffix('.request.json');payload=dict(text=prompt,duration_seconds=dur,model_id='eleven_text_to_sound_v2',prompt_influence=.55,loop=False)
    identity=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    if p.exists() and receipt.exists():
        prior=json.loads(receipt.read_text())
        if prior['request_sha256']!=identity or prior['audio_sha256']!=hashlib.sha256(p.read_bytes()).hexdigest():raise ValueError('SFX cache mismatch '+id)
        print('reused '+id,flush=True);continue
    if p.exists():raise ValueError('Incomplete sound asset, preserve for recovery: '+id)
    try:
        out=b''.join(client.text_to_sound_effects.convert(**payload,output_format='mp3_44100_128',request_options={'max_retries':0,'timeout_in_seconds':120}))
    except Exception as e:
        print(json.dumps(dict(error=type(e).__name__,asset=id)),flush=True);raise SystemExit(1)
    p.write_bytes(out)
    receipt.write_text(json.dumps(dict(provider='elevenlabs',gap='No suitable existing board/production/bundled asset; Openverse resolver returned no match.',request_sha256=identity,payload=payload,audio_sha256=hashlib.sha256(out).hexdigest()),indent=2)+'\n')
    print('generated '+id,flush=True)
