from pathlib import Path
import json, hashlib, importlib.util
BASE=Path(__file__).resolve().parent; ROOT=BASE.parent.parent; V=BASE/'video'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('sd',ROOT/'.agents/skills/shortform-production/scripts/sound_design.py'); sd=importlib.util.module_from_spec(spec);spec.loader.exec_module(sd)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
scenes=read(V/'scenes.json');m=read(V/'audio_meta.json');source=read(V/'assets/board/audio/sfx/manifest.json')
assets=[]
for a in source['assets']:
    path='assets/board/audio/sfx/'+a['file']
    assets.append(dict(id=a['id'],path=path,sha256=sha(V/path),duration=a['duration'],source=dict(board='ruang-di-antara v1.2',provenance=a['source'],credits='assets/board/audio/sfx/CREDITS.md')))
events=[(3,'contact',.44,'Marked work sheet enters the fictional account',.65),(8,'connection',.68,'Return question completes the listening loop',.70),(11,'air',.68,'Tentative route gives way to the corrected route',.55),(14,'connection',.68,'Speaker request reaches the listener',.65),(15,'contact',.68,'Solution note lands on the shared table',.65)]
cues=[]
for n,asset,frac,purpose,gain in events:
    s=scenes[n-1]; a=next(x for x in assets if x['id']==asset)
    cues.append(dict(id=f'sfx-f{n:02}-{asset}',asset=asset,scene=f'f{n:02}',purpose=purpose,trigger=f'Beat 4 at local {s["duration"]*frac:.3f}s' if frac==.68 else f'Beat 3 at local {s["duration"]*frac:.3f}s',start=round(s['start']+s['duration']*frac,4),duration=a['duration'],volume=gain,track=3))
placed=read(V/'mix.json')['path'] if (V/'mix.json').exists() else m['voices'][0]['path']
plan=dict(version=1,decisions=dict(narration=dict(mode='use',reason='Intimate continuous narration carries the distinction and examples; loudness preparation preserves the original TTS cache.'),bgm=dict(mode='none',reason='An intimate conversation and its pauses carry the arc; no bed to flatten the two dramatic turns.'),sfx=dict(mode='use',reason='Five restrained material accents land on a work sheet, checked understanding, correction, request and shared solution.')),timing_sha256=sha(V/'timing.json'),narration_sha256=sha(V/placed),motion_sources={f'compositions/frames/f{s["n"]:02}.html':sd.motion_digest(V/f'compositions/frames/f{s["n"]:02}.html') for s in scenes},assets=assets,cues=cues,silence='No automatic transition sounds. Frames 04 and 12 use speech and a withheld cue; final reflective hold is quiet.')
(V/'sound_design.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(sd.apply_plan(V)))
