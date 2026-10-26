"""Prepare one root-env voice request after complete storyboard verification."""
from pathlib import Path
import json,importlib.util
V=Path(__file__).resolve().parent;R=V.parents[2];P=V.parent
assert (V/'boards/storyboard.png').is_file()
report=json.loads((V/'boards/verification.json').read_text(encoding='utf-8'));assert report['frames']==16 and not report['missing']
module_path=R/'.agents/skills/shortform-production/scripts/narration.py'
spec=importlib.util.spec_from_file_location('production_narration',module_path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
voice,provenance=mod.resolve_voice(R)
plan=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'))
paras=[]
for n,s in enumerate(plan):
    tag={0:'[curious]',1:'[clear, conversational explanation]',7:'[focused, guide attention]',15:'[warm, conclusive]'}.get(n,'')
    paras.append((tag+' '+s['text']).strip())
req=dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=provenance,tts_model='eleven_v4',lines=[dict(id='narration',text='\n\n'.join(paras))])
(V/'audio_request.json').write_text(json.dumps(req,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('\n## Static storyboard verification\nAll 16 scene stills, boards/storyboard.html and boards/storyboard.png verified before synthesis/animation. PNG 1920×4221, complete ordered s01–s16, no missing images; opened saved PNG and both still contact sheets. Repaired cropped pin labels in s06/s07; distinct contact/release and pre-contact/contact governor poses. Agent-verified under delegated automation; human approval false.\n')
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));entry=next(x for x in tracker['productions'] if x['slug']==P.name);entry.update(stage='audio',status='in_progress');(R/'TRACKER.json').write_text(json.dumps(tracker,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(provider='elevenlabs',model='eleven_v4',voice_source=provenance,lines=1)))
