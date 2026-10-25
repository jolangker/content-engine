from pathlib import Path
import importlib.util,json
V=Path(__file__).resolve().parent;ROOT=V.parents[2]
spec=importlib.util.spec_from_file_location('narration',ROOT/'.agents/skills/shortform-production/scripts/narration.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
voice,resolution=m.resolve_voice(ROOT)
plan=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'))
tags={0:'[curious, inviting]',1:'[clear and measured]',3:'[guide attention, concrete]',7:'[slightly emphasize the connection]',9:'[calm and precise]',12:'[explanatory]',14:'[warm, satisfying conclusion]'}
text='\n\n'.join((tags.get(i,'')+' '+s['vo']).strip() for i,s in enumerate(plan))
req=dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=resolution,tts_model='eleven_v4',speed=1,lines=[dict(id='narration',text=text)],bgm=dict(mode='none'))
(V/'audio_request.json').write_text(json.dumps(req,ensure_ascii=False,indent=2),encoding='utf-8')
with (V.parent/'EPISODE.md').open('a',encoding='utf-8') as f:
 f.write('\n## Static storyboard verification\n\n16/16 styled composition stills inspected in scene order; `video/boards/storyboard.html` and complete `video/boards/storyboard.png` (1920×4035) exist. Browser verified 16 correct ordered images with nonzero dimensions. Initial SVG overflow into titles was repaired with a visual crop; every final still was recaptured and PNG inspected. Whole assembly, controlled section, lever/chain, flapper contact, float, refill and overflow macros vary scale and explanatory task. Board fonts, semantic colors, shaded side faces and assembly landmarks retained. Agent-verified under delegated authorization, not human approval.\n\n## Narration request\n\nProvider ElevenLabs, model eleven_v4, voice '+voice+' resolved from root `.env` ELEVENLABS_VOICE_ID; one tagged full-script input. No inherited shell or prior-production voice selection. BGM intentionally absent; material and water interaction cues are required and frozen separately.\n')
print(json.dumps({'provider':'elevenlabs','model':'eleven_v4','voice':voice,'scenes':16,'words':len(' '.join(s['vo'] for s in plan).split())}))
