"""Tie reused cue assets to measured speech, actual events and scene source hashes."""
from pathlib import Path
import json,hashlib,re,subprocess
V=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def motion_sha(p):return hashlib.sha256(re.sub(r'\s+data-hf-id=(?:"[^"]*"|\x27[^\x27]*\x27)','',p.read_text(encoding='utf-8')).encode()).hexdigest()
assets=json.loads((V/'assets/audio/sfx/assets.json').read_text(encoding='utf-8'));events=json.loads((V/'motion-events.json').read_text(encoding='utf-8'));timing=json.loads((V/'timing.json').read_text(encoding='utf-8'));cues=[]
for a in assets:a['duration_s']=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(V/a['path'])]))
for n,event in enumerate(sorted(events,key=lambda e:e['time'])):
    role=event['role'];ident='editorial' if role=='editorial' else 'hinge' if role=='travel' else 'metal';a=next(x for x in assets if x['id']==ident)
    gain=.3 if role=='editorial' else .42 if role=='travel' else .65
    cues.append(dict(id=f'sfx-{n+1:03}-{event["scene"]}',scene=event['scene'],asset=ident,purpose=role+' cue for '+event['action'],trigger=event['action']+'; actual animation onset rounded to nearest output frame',start=event['time'],duration=min(a['duration_s'],90-event['time']),volume=gain,track=4+n%4,role=role))
plan=dict(version=1,decisions=dict(narration=dict(mode='use',reason='One continuous ElevenLabs eleven_v4 recording; source preserved, derived pitch-preserving tempo 1.08 and gain treatment to fit the 90s board.'),bgm=dict(mode='none',reason='Keep narration and distinction between dry gear/contact and editorial cues exposed; no competing music bed.'),sfx=dict(mode='use',reason='Source-verified frozen material travel and metallic contact cues; bundled soft editorial click. No new generation.')),assets=assets,cues=cues,timing_sha256=sha(V/'timing.json'),narration_sha256=sha(V/'assets/audio/narration-master.wav'),motion_sources={f'compositions/{s["id"]}.html':motion_sha(V/f'compositions/{s["id"]}.html') for s in timing},silence='The carrier-bias explanation, seated pawl, fixed load-path and final proof holds are intentionally quiet under narration. Sustained coupled motion shares its onset cue. No click on every tooth or whoosh on every cut.',creative_listening='Unavailable: waveform/timing/level evidence only; auditory and phone-speaker review not claimed.')
(V/'sound_design.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Retain the original static still labels as estimates; canonical scene plan now uses measured audio.
doc=(V/'STORYBOARD.md').read_text(encoding='utf-8')
for n,s in enumerate(timing,1):
    doc=re.sub(rf'(## Frame {n}: [^\n]*?)\([^\n]*s\)',lambda m:m[1]+f'({s["start"]:.3f}–{s["end"]:.3f}s, measured)',doc,count=1)
    pattern=rf'(## Frame {n}:.*?\n- status: )built(\n- duration: )[^\n]+'
    doc=re.sub(pattern,lambda m:m[1]+'animated'+m[2]+f'{s["duration"]:.6f}s',doc,count=1,flags=re.S)
doc=re.sub(r'\n## Measured timing and sound\n.*?(?=\n## |\Z)','',doc,flags=re.S)
doc+='\n## Measured timing and sound\n\nNative narration 95.44s, preserved. Derived pitch-preserving tempo 1.08, onset 0.3s. Canonical timing.json and caption groups follow native timestamps divided by 1.08. All 200 words mapped. Original pre-audio board is preserved in boards/revisions/pre-audio; final board v2 uses measured labels and revised layouts for shots 10/12/15. No auditory or independent post-tempo transcription verification. Cue onsets are rounded to 30fps; visual events remain within half an output frame.\n'
(V/'STORYBOARD.md').write_text(doc,encoding='utf-8')
print(json.dumps(dict(cues=len(cues),assets=len(assets),measured_scenes=len(timing))))
