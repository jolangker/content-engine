from pathlib import Path
import json,sys,shutil
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
def write(p,t): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def dump(p,x): write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
rows=[
('mystery','Turun, kok naik?','whole',5,'Sayapnya ditekan turun. Kenapa gabusnya malah naik?','Opposite wing and cork travel establishes the mystery.'),
('discover','Gigi mengangkat batang','head',6,'Di pangkal kedua sayap, ada gigi yang berkaitan dengan alur pada batang tengah.','First discovery: toothed sectors drive the annular shaft upward.'),
('orient','Satu batang, dua bagian','shaft',5,'Batang yang sama punya spiral di bawahnya. Bagian inilah yang menancap ke gabus.','Connect grooved shaft and lower worm, preserving their common axis.'),
('seat','Badan bertumpu di sini','base',5,'Mulainya begini. Kaki pembuka duduk di bibir botol, sementara ujung spiral menyentuh gabus.','Base seats on bottle rim and worm approaches cork.'),
('turn','Putaran masuk ke gabus','worm',5,'Ketika kepala diputar, spiral masuk semakin dalam. Batang tengah ikut bergerak turun.','Rotation and progressive penetration, body and cork stationary.'),
('grip','Spiral tertanam','cork',5,'Lihat penampangnya. Spiral sudah tertanam di dalam gabus. Sambungan ini nantinya membawa gabus naik.','Cutaway exposes embedded helix and retained cork engagement.'),
('guide','Turun lewat pemandu','guide',6,'Batangnya tetap lewat lubang pemandu di badan alat. Jadi gerak turun ini mencapai bagian bergigi.','Axial shaft motion passes through the stationary guide.'),
('rise','Batang turun, sayap naik','head',6,'Alur batang mendorong gigi di kedua sisi. Gigi berputar bersama sayap, mengelilingi porosnya.','Rack descent rotates both sectors and raises both wings.'),
('rings','Alurnya melingkar','rings',6,'Alur di bagian ini melingkari batang, berbeda dari spiral penusuk di bawah. Keduanya punya tugas berbeda.','Annular grooves remain available as shaft rotates; contrast worm pitch.'),
('pivot','Porosnya tetap di badan','pin',6,'Sekarang sayap sudah terangkat. Poros masing-masing tetap terpasang pada badan pembuka. Batang tengah masih bisa bergeser.','Fixed pivots and movable shaft establish extraction constraints.'),
('drive','Tekan sayap, balik geraknya','macro',7,'Saat sayap ditekan, sektor giginya berputar ke arah sebaliknya. Perhatikan titik pertemuannya: batang terdorong ke atas.','Signature: pitch-coupled contact, sector rotation and shaft rise.'),
('lever','Lengan panjang, sektor pendek','lever',6,'Ujung sayap menjadi tempat menekan. Lengan yang panjang memutar sektor bergigi yang lebih kecil di dekat poros.','Qualitative lever geometry with no numerical mechanical advantage.'),
('reaction','Tumpuannya tetap di botol','base',6,'Badan pembuka tetap bertumpu pada bibir botol. Jadi batang bisa naik relatif terhadap botol yang ditahan.','Reaction path from stationary sector support through body and rim.'),
('lift','Gabus mengikuti spiral','cork',5,'Karena spiral masih tertanam, gabus ikut tertarik. Gerak gigi diteruskan sepanjang batang hingga ke gabus.','Embedded worm and cork translate together, no extraction rotation.'),
('clear','Keluar dari leher botol','whole',5,'Saat gabus melewati bibir botol, hasil rangkaian gerak tadi terlihat: gabus sudah terangkat.','Cork bottom clears rim; bottle and support remain fixed.'),
('proof','Turun di sini, naik di tengah','proof',6,'Jadi, sayap turun memutar gigi. Gigi menaikkan batang. Dan spiral membawa gabus keluar.','Matched ending: repeat extraction with section showing all dependencies.')]
plan=[];start=0
for n,(key,title,view,d,text,action) in enumerate(rows):
 plan.append(dict(id=f's{n+1:02}-{key}',key=key,title=title,view=view,start=start,end=start+d,duration=d,text=text,action=action));start+=d
assert start==90
dump(V/'scene-plan.json',plan)
script='# Locked Indonesian narration v1\n\nAgent-verified under delegated automation; no human approval. Source mapping: ../SOURCES.md. Visual timing below is estimated until measured audio placement.\n\n'
for s in plan:script+=f'## {s["id"]} ({s["start"]}–{s["end"]}s)\n\n{s["text"]}\n\nOn-screen: {s["title"]}\n\n'
write(P/'SCRIPT.md',script);write(V/'SCRIPT.md',script)
write(V/'BRIEF.md',(P/'EPISODE.md').read_text(encoding='utf-8')+'\nAll scene, caption and SFX clocks derive from measured timing.json. Exact duration90s. Board caption position y1500 explicitly overrides the generic vertical template; user-approved board v6 supplies this placement. Listening unavailable: objective audio verification retained.\n')
write(V/'SPEC.md','''GOAL: Explain opposite wing/cork travel through one complete insertion/extraction cycle.
OUTPUT: HyperFrames 1080x1920, 30fps, 90s =2700 frames.
LOOK: board v6 #ECEEE9 ground, #172B3B ink, #C94422 input, #2459C4 active gears, #167580 output; Manrope800 68px/-2.5px heading, Manrope600 46px/1.3 captions, Plex28px note. Local fonts. Layered SVG shaded metal, 10px offset depth, restrained ground shadow; no true3D.
OBJECTS: twin-wing cork puller, central annular grooved shaft, attached helix, fixed pin supports, open base seated on thick bottle rim, brown porous cork. No bottle contents or brand.
MOTION: deterministic analytic sector/rack coupling; travel=64*angle(radians). Insertion rotates projected helix with axial descent, extraction translates worm/cork together without unscrewing. Joint angles and sweep fit every view. Camera fixed at each functional view; no decorative orbit. Physical movement linear, attention accents brief only.
SHOTS: scene-plan.json supplies16 unequal 5–7s estimates; measured audio replaces scene ranges without changing2700frames. First discovery shot2. Signature shot11. Opening/ending pair1/16. Macros contact and embedded helix. BGM absent intentionally; distinct material and editorial cues.
BANNED: flat silhouette-only geometry, arbitrary exploded distances, generic whooshes per cut, slipping teeth, body rising with cork, moving cork during initial insertion, rotating helix during extraction, spring claims, force ratios, dark void, neon, HUD, CTA end card, bullet slides, repeating one contact16times.
QA: all16 stills; shot11 approach/transfer/result; cork contact; shaft phase continuity; final proof. No sound or phone-speaker audition claimed.
''')
write(V/'STORYLINES.md','''# Resolved story directions
1. Opposite movements: extraction mystery, then trace worm insertion and return to matched extraction. Selected: clearest physical question and proof. Mineral 2.5D bench, material contact cues, Indonesian guide.
2. Follow the cork: begin inside a cut neck, track worm engagement and then pull out. Not selected: opening offers less object recognition.
3. The fixed support: one continuous sectional view traces force through rim, pivots and rack. Not selected: less framing variety over90s.
Project hook selection and board already resolve these decisions; no additional pitch gate under automation.
''')
shutil.copy2(R/'boards/di-balik-benda/frame.md',V/'frame.md')
for f in (R/'boards/di-balik-benda/assets').iterdir():
 if f.suffix=='.ttf' or 'OFL' in f.name: dest=V/'assets/fonts'/f.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'))
from narration import resolve_voice
voice,resolution=resolve_voice(R,board='di-balik-benda')
spoken='\n\n'.join(s['text'] for s in plan)
tagged='[curious, clear Indonesian, conversational pace] '+spoken.replace('Sekarang sayap sudah terangkat.','[explaining, deliberate] Sekarang sayap sudah terangkat.').replace('Jadi, sayap turun','[confident, warm] Jadi, sayap turun')
dump(V/'audio_request.json',dict(provider='elevenlabs',board='di-balik-benda',lang='id',voice=voice,voice_resolution=resolution,tts_model='eleven_v4',lines=[dict(id='narration',text=tagged)]))
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8-sig'));row=next(x for x in tracker['productions'] if x['slug']==P.name);row.update(stage='script',status='complete');dump(R/'TRACKER.json',tracker)
print(json.dumps(dict(shots=len(plan),seconds=start,words=len(spoken.split()),voice_source=resolution['source'])))
