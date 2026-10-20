import json, pathlib, shutil

P=pathlib.Path(__file__).resolve().parent
V=P/'video'
scenes=json.loads((P/'scenes.json').read_text(encoding='utf-8'))
for folder in ['assets/fonts','compositions/frames','capture/extracted','verification']:
    (V/folder).mkdir(parents=True,exist_ok=True)
for f in (P.parent.parent/'boards/ruang-di-antara/assets').iterdir():
    if f.suffix in ['.ttf','.txt']: shutil.copy2(f,V/'assets/fonts'/f.name)
spec='''---
name: ruang-di-antara-v1.1
canvas: { width: 1080, height: 1920, fps: 30 }
colors:
  canvas: "#F3EDE3"
  ink: "#302B28"
  accent: "#A34F3F"
  sand: "#D8C8B5"
typography:
  display: { fontFamily: "Newsreader", weight: 400, size: 108, lineHeight: 1.06 }
  body: { fontFamily: "DM Sans", weight: 400, size: 42, lineHeight: 1.3 }
  label: { fontFamily: "DM Sans", weight: 500, size: 30, lineHeight: 1.3 }
  captions: { fontFamily: "DM Sans", weight: 500, size: 46, lineHeight: 1.25 }
spacing:
  safeLeft: 88
  safeRight: 144
  safeTop: 160
  keyContentBottom: 1480
  captionTop: 1550
  captionBottom: 1740
---

# Episode design

Approved Ruang di Antara v1.1, from boards/ruang-di-antara/DIRECTION.md and EDITORIAL.md. Text-led editorial reflection shares the frame with two organic faceless forms. Sparse cream distance is intentional. Use one charcoal pressure scene (04), cream/sand reading text on charcoal. No gradients, decorative grain, stock media, gender coding, diagnosis, UI cards or unrelated accents. Local Newsreader and DM Sans fonts with OFL licenses.

Actors carry relationship motion: one moves closer, the other withdraws, then both stop at an agreed distance. A return path closes only when dialogue resumes. No camera zoom is needed. Smooth power3 motion, sequential reveals aligned with words, stillness after a meaningful action; no bouncing or ambient loops.

Content is confined to x88–936, y160–1480. Captions occupy y1550–1740 and remain separate from exact screen copy. Avoid long duplicated narration on screen. Distinct states: interrupted connection, pursuit, repeated path, shifted topic, unknown motive, open space, explicit agreement, spoken intent, agreed time, return action, renewed conversation, missed agreement, safety boundary, closing path.
'''
(V/'frame.md').write_text(spec,encoding='utf-8')
(V/'capture/extracted/visible-text.txt').write_text('$shortform-production --board=ruang-di-antara --topic=auto --delivery=draft --automation\n\n'+(P/'EPISODE.md').read_text(encoding='utf-8'),encoding='utf-8')
(V/'capture/extracted/tokens.json').write_text(json.dumps({'title':'Jeda yang kembali','description':'A conflict pause and a clear agreement to return','colors':['#F3EDE3','#302B28','#A34F3F','#D8C8B5'],'fonts':['Newsreader','DM Sans']},indent=2),encoding='utf-8')
tags={0:'[intimate, curious, conversational]',2:'[clear, explanatory]',4:'[gentle, thoughtful]',6:'[grounded, practical]',7:'[calm, sincere]',9:'[matter-of-fact]',12:'[serious, steady]',13:'[reflective, leave space]'}
tagged='\n\n'.join((tags.get(i,'')+' '+s['vo']).strip() for i,s in enumerate(scenes))
req={'provider':'elevenlabs','lang':'id','voice':'nPczCjzI2devNBz1zQrb','tts_model':'eleven_v4','speed':1.0,'lines':[{'id':'narration','text':tagged}],'bgm':{'mode':'none'}}
(V/'audio_request.json').write_text(json.dumps(req,ensure_ascii=False,indent=2),encoding='utf-8')
script='# SCRIPT — Jeda yang kembali\n\nVersion v1, agent-verified under delegated automation. 187 spoken words.\n\n**Voice:** ElevenLabs / Brian / nPczCjzI2devNBz1zQrb / eleven_v4\n**Voice direction:** Intimate, observant Indonesian lo–gua; clarify without diagnosing. Full script in one synthesis request.\n'
for i,s in enumerate(scenes):
    script+=f"\n## Line {i+1} — {s['title']} (Frame {i+1})\n\n**Time:** estimated, approximately 6–7 seconds; replace with measured alignment.\n**Delivery:** {tags.get(i,'Continue naturally in the preceding register.')}\n\n    {s['vo']}\n\n**On-screen:** {s['text']}\n**Support:** {s['support']}\n"
(P/'SCRIPT.md').write_text(script,encoding='utf-8');(V/'SCRIPT.md').write_text(script,encoding='utf-8')
research=json.loads((pathlib.Path.home()/'AppData/Local/Temp/jeda-research.json').read_text(encoding='utf-8'))
(P/'research-extract.json').write_text(json.dumps(research,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared 14 scenes, 187 spoken words, one Brian/eleven_v4 request.')
