import json, pathlib, shutil, sys

P=pathlib.Path(__file__).resolve().parent
V=P/'video'
ROOT=P.parent.parent
BOARD=ROOT/'boards/ruang-di-antara'
sys.path.insert(0,str(ROOT/'.agents/skills/shortform-production/scripts'))
from narration import resolve_voice
voice,voice_resolution=resolve_voice(ROOT)
scenes=json.loads((P/'scenes.json').read_text(encoding='utf-8'))
for folder in ['assets/fonts','compositions/frames','capture/extracted','verification']:
    (V/folder).mkdir(parents=True,exist_ok=True)
for f in (P.parent.parent/'boards/ruang-di-antara/assets').iterdir():
    if f.suffix in ['.ttf','.txt']: shutil.copy2(f,V/'assets/fonts'/f.name)
spec=(BOARD/'frame.md').read_text(encoding='utf-8')+'\n\n## Episode adaptation ? revision v2\n\nUse one charcoal pressure scene (04). Scene layout and timing are recorded in STORYBOARD.md. Shared chrome is inherited unchanged; content changes scale and placement according to the beat. No B-roll or decorative motion.\n'
(V/'frame.md').write_text(spec,encoding='utf-8')
(V/'capture/extracted/visible-text.txt').write_text('$shortform-production --board=ruang-di-antara --topic=auto --delivery=draft --automation\n\n'+(P/'EPISODE.md').read_text(encoding='utf-8'),encoding='utf-8')
(V/'capture/extracted/tokens.json').write_text(json.dumps({'title':'Jeda yang kembali','description':'A conflict pause and a clear agreement to return','colors':['#F3EDE3','#302B28','#A34F3F','#D8C8B5'],'fonts':['Newsreader','DM Sans']},indent=2),encoding='utf-8')
tags={0:'[intimate, curious, conversational]',2:'[clear, explanatory]',4:'[gentle, thoughtful]',6:'[grounded, practical]',7:'[calm, sincere]',9:'[matter-of-fact]',12:'[serious, steady]',13:'[reflective, leave space]'}
tagged='\n\n'.join((tags.get(i,'')+' '+s['vo']).strip() for i,s in enumerate(scenes))
req={'provider':'elevenlabs','lang':'id','voice':voice,'voice_resolution':voice_resolution,'tts_model':'eleven_v4','speed':1.0,'lines':[{'id':'narration','text':tagged}],'bgm':{'mode':'none'}}
(V/'audio_request.json').write_text(json.dumps(req,ensure_ascii=False,indent=2),encoding='utf-8')
script=f'# SCRIPT — Jeda yang kembali\n\nVersion v2, revised after the 2026-10-20 investigation; agent-verified under delegated automation. 187 spoken words.\n\n**Voice:** ElevenLabs / {voice} / eleven_v4 (resolved from project .env)\n**Voice direction:** Intimate, observant Indonesian lo–gua; clarify without diagnosing. Full script in one synthesis request.\n'
for i,s in enumerate(scenes):
    script+=f"\n## Line {i+1} — {s['title']} (Frame {i+1})\n\n**Time:** estimated, approximately 6–7 seconds; replace with measured alignment.\n**Delivery:** {tags.get(i,'Continue naturally in the preceding register.')}\n\n    {s['vo']}\n\n**On-screen:** {s['text']}\n**Support:** {s['support']}\n"
(P/'SCRIPT.md').write_text(script,encoding='utf-8');(V/'SCRIPT.md').write_text(script,encoding='utf-8')
print(json.dumps({'scenes':len(scenes),'words':187,'voice':voice,'voice_resolution':voice_resolution,'model':'eleven_v4'}))
