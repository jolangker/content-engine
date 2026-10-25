from pathlib import Path
import importlib.util,json
P=Path(__file__).resolve().parent;R=P.parents[1];V=P/'video'
spec=importlib.util.spec_from_file_location('narration',R/'.agents/skills/shortform-production/scripts/narration.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
voice,resolution=mod.resolve_voice(R)
scenes=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'))
tags=['[curious, conversational]','[explaining calmly]','[guiding, clear and measured]','[quietly amused]','[matter-of-fact]','[warm, satisfied]']
text='\n\n'.join(tag+' '+s['vo'] for tag,s in zip(tags,scenes))
request=dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=resolution,tts_model='eleven_v4',speed=1.0,lines=[dict(id='narration',text=text)],bgm=dict(mode='none'))
(V/'audio_request.json').write_text(json.dumps(request,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared one full-script tagged request; voice source is the project root .env. No key printed.')
