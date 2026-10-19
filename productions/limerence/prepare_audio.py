"""Prepare one full-script ElevenLabs request without changing spoken words."""
from pathlib import Path
import json
import re

prod=Path(__file__).resolve().parent
script=(prod/'SCRIPT.md').read_text(encoding='utf-8')
spoken=script.split('## Reading copy\n\n',1)[1].split('\n## Timing and delivery',1)[0].strip()
paras=spoken.split('\n\n')
tags={0:'[warm, conversational, unhurried] ',4:'[clear, measured] ',6:'[observant] ',9:'[gentle, matter-of-fact] ',11:'[reflective] ',13:'[softly, thoughtful] '}
tagged='\n\n'.join(tags.get(i,'')+p for i,p in enumerate(paras))
assert re.sub(r'\[[^\]]*\]\s*','',tagged)==spoken
request={'provider':'elevenlabs','lang':'id','voice':'nPczCjzI2devNBz1zQrb','tts_model':'eleven_v4','speed':1.0,'lines':[{'id':'narration','text':tagged}],'bgm':{'mode':'none'}}
(prod/'video'/'audio_request.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'provider':request['provider'],'voice':request['voice'],'tts_model':request['tts_model'],'requests':1,'spoken_words':len(spoken.split()),'delivery_shifts':len(tags)}))
