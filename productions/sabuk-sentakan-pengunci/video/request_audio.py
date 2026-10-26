"""Resolve narration only from the project's selected voice provenance."""
from pathlib import Path
import json,sys
V=Path(__file__).resolve().parent;R=V.parents[2]
sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'))
from dotenv import dotenv_values
voice=dotenv_values(R/'.env').get('ELEVENLABS_VOICE_ID')
assert voice,'Missing ELEVENLABS_VOICE_ID in root .env'
plan=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'))
tags={0:'[curious]',1:'[explaining]',7:'[focused]',9:'[slower]',12:'[explaining]',14:'[curious]',15:'[clear]'}
text='\n\n'.join((tags.get(n,'')+' '+s['text']).strip() for n,s in enumerate(plan))
request=dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=dict(source='project_env',key='ELEVENLABS_VOICE_ID'),tts_model='eleven_v4',lines=[dict(id='narration',text=text)])
(V/'audio_request.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(provider=request['provider'],model=request['tts_model'],entries=1,spoken_words=sum(len(s['text'].split()) for s in plan))))
