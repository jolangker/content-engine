"""Build the exact one-recording request after complete storyboard verification."""
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent;R=P.parents[1];V=P/'video'
sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'))
from narration import resolve_voice
voice,provenance=resolve_voice(R,board='ruang-di-antara')
lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'))
request=dict(provider='elevenlabs',board='ruang-di-antara',lang='id',voice=voice,voice_resolution=provenance,tts_model='eleven_v4',lines=[dict(id='narration',text='\n\n'.join(('['+x['tags']+'] ' if x['tags'] else '')+x['text'] for x in lines))])
(V/'audio_request.json').write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('''
## Static storyboard verified before synthesis

Complete boards/storyboard.html and 1440x3183 boards/storyboard.png include sixteen ordered 1080x1920 stills. Saved PNG visually inspected: all scenes present, readable and unclipped, fixed chrome consistent, precisely two dark turns 08/11. Door handle/frame, tied bag, dish rims, faucet/basin and lid/ribbed outside bin are recognizable; wide scenes, close objects and speaker spaces vary focal scale. Viewer silhouette and partner remain distinct across palette changes. Agent accepted v1 layouts under delegation, no human approval. No supporting paragraphs in video. Narration-only POV check also applied to exact synthesis wording; tags only change delivery, all audible speaker cues retained. Next: one native narration synthesis, acoustic placement, captions and bounded motion.
''')
print(json.dumps(dict(provider=request['provider'],model=request['tts_model'],lines=1,voice_source=provenance['source'])))
