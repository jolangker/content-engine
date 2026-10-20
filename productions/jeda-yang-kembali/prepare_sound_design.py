"""Prepare this episode's user-authorized selective SFX revision; preserve speech."""
from pathlib import Path
import json
import shutil
import sys

P = Path(__file__).resolve().parent
V = P / 'video'
ROOT = P.parents[1]
sys.path.insert(0, str(ROOT / '.agents/skills/shortform-production/scripts'))
from sound_design import AudioHTML, apply_plan, digest, local_file, motion_digest

CUES = [[2, 1.39, 'air', 0.45, 'pursuit', 'The first actor begins moving toward the withdrawing partner.'], [3, 2.736, 'contact', 0.45, 'cycle', 'The first response path completes; make the recurring interaction concrete.'], [6, 1.43, 'air', 0.43, 'space', 'The actors move apart to create space rather than end the conversation.'], [9, 2.347, 'contact', 0.55, 'return-point', 'The first trace reaches the explicit return-time agreement.'], [10, 2.88, 'connection', 0.55, 'return', 'The actors finish the return motion and the first return path lands.'], [13, 2.04, 'contact', 0.45, 'boundary', 'The first boundary trace completes while the actor retains distance.']]
timing = json.loads((V / 'timing.json').read_text(encoding='utf-8'))
scenes = timing.get('scenes', timing.get('frames'))
# Reuse frozen board variants; a new episode does not need new processing.
library_dir = ROOT / 'boards/ruang-di-antara/assets/audio/sfx'
library = json.loads((library_dir / 'manifest.json').read_text(encoding='utf-8'))
asset_dir = V / '.media/audio/sfx'
asset_dir.mkdir(parents=True, exist_ok=True)
if not (asset_dir / 'CREDITS.md').exists():
    shutil.copy2(library_dir / 'CREDITS.md', asset_dir / 'CREDITS.md')
assets = []
needed = {cue[2] for cue in CUES}
for entry in library['assets']:
    if entry['id'] not in needed:
        continue
    source = library_dir / entry['file']
    if digest(source) != entry['sha256']:
        raise ValueError('Shared SFX hash mismatch: ' + entry['id'])
    target = V / entry['path']
    if target.exists():
        if digest(target) != entry['sha256']:
            raise ValueError('Existing production SFX differs; resolve the revision explicitly: ' + entry['id'])
    else:
        shutil.copy2(source, target)
    assets.append({key:entry[key] for key in ('id','path','sha256','duration','source')})
if {asset['id'] for asset in assets} != needed:
    raise ValueError('A selected SFX is missing from the shared library; resolve a suitable asset first')
asset_by_id={a['id']:a for a in assets}
cues=[]
motion_sources={}
for number,offset,asset,volume,name,trigger in CUES:
    scene=scenes[number-1]
    src=scene.get('src','compositions/frames/'+scene.get('id','')+'.html')
    motion_sources[src]=motion_digest(V/src)
    start=round((scene['start']+offset)*30)/30
    cues.append({'id':'sfx-'+name,'scene':str(number),'asset':asset,
        'purpose':trigger,'trigger':src+' at local '+str(offset)+'s: '+trigger,
        'start':round(start,6),'duration':asset_by_id[asset]['duration'],'volume':volume,'track':4})
voice=next(a for a in AudioHTML((V/'index.html').read_text(encoding='utf-8')).audio if a.get('id')=='narration')
plan={'version':1,'revision':'sfx-2026-10-20','board_audio_revision':'2026-10-20',
    'authorization':'User accepted the pipeline, board and episode correction plan with gas perbaiki.',
    'decisions':{'narration':{'mode':'use','reason':'Preserve the existing verified full-script narration and speech timing.'},
        'bgm':{'mode':'none','reason':'Keep the intimate spoken reflection; isolated material cues provide contrast without a continuous bed.'},
        'sfx':{'mode':'use','reason':'Make concrete relational actions and changes in the diagram perceptible with sparse, restrained material accents.'}},
    'silence':'Uncued beats and the final reflective scene stay free of effects; no automatic transition accents.',
    'timing_sha256':digest(V/'timing.json'),'narration_sha256':digest(local_file(V,voice['src'])),
    'motion_sources':motion_sources,'assets':assets,'cues':cues,
    'replaces':['sfx-1','sfx-2'] if P.name=='limerence' else []}
(V/'sound_design.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Register frozen derivatives without duplicating existing ledger identities.
ledger = V / '.media/manifest.jsonl'
records = [json.loads(line) for line in ledger.read_text(encoding='utf-8').splitlines() if line.strip()] if ledger.exists() else []
known = {record.get('id') for record in records}
for asset in plan['assets']:
    identity = 'sfx_rda_' + asset['id'] + '_' + asset['sha256'][:12]
    if identity not in known:
        records.append({'id':identity,'type':'sfx','path':asset['path'],'source':'local',
            'description':'Ruang di Antara treated ' + asset['id'], 'duration':asset['duration'],
            'sha256':asset['sha256'],'provenance':asset['source']})
ledger.write_text(''.join(json.dumps(record,ensure_ascii=False)+'\n' for record in records),encoding='utf-8')

print(json.dumps(apply_plan(V)))
