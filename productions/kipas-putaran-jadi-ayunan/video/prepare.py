"""Freeze the delegated production, evidence and pre-audio scene plan."""
from pathlib import Path
import json, shutil
V=Path(__file__).resolve().parent; P=V.parent; R=V.parents[2]
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def dump(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
rows=[
('mystery',5,'Kenapa bisa bolak-balik?','Baling-balingnya terus searah. Kenapa kepala kipas bisa bergerak bolak-balik?','whole','Recognizable fan: continuous blade rotation and head yaw.'),
('branch',5,'Satu motor, dua jalur','Pada tipe mekanis ini, satu motor menggerakkan baling-baling sekaligus mekanisme ayunan di belakangnya.','side','First discovery: front blade and rear worm share a shaft.'),
('worm',5,'Putaran masuk dari belakang','Bagian belakang poros berbentuk ulir. Ulir ini meneruskan putaran ke rangkaian roda gigi.','gear','Introduce worm at its functional contact; mark schematic teeth.'),
('reduction',5,'Roda gigi meneruskan gerak','Rangkaian itu menggerakkan piringan di bawah rumah roda gigi. Piringan berputar bersama pin di tepinya.','gear','Worm, spindle and carrier disk form a connected power path.'),
('eccentric',5,'Piringan berputar, pin mengorbit','Perhatikan pin ini. Letaknya menjauh dari pusat, sehingga pin berjalan melingkar ketika piringan berputar.','disc','Crank center versus eccentric pin; no claimed product dimensions.'),
('rod',5,'Pin membawa batang','Pin tersambung ke batang penghubung. Sambungannya bisa berputar, jadi batang mengikuti perjalanan pin tanpa terlepas.','link','Pin bearing and rigid rod follow one another.'),
('anchor',6,'Ujung satunya tertahan','Ujung batang yang lain terpasang pada jangkar di penyangga. Jangkar ini tetap, tidak ikut kepala kipas.','link','Expose stationary anchor A and distinct head pivot O.'),
('constraint',7,'Jarak ini harus tetap','Inilah kuncinya. Batang tidak memanjang. Saat pin bergerak, rumah roda gigi harus bergeser mengelilingi poros kepala.','macro','Signature: eccentric motion, fixed rod length and yaw response solved together.'),
('push',6,'Kepala terdorong ke satu sisi','Rumah roda gigi terikat pada badan motor. Jadi, ketika mekanisme bergerak, seluruh kepala ikut berayun ke satu sisi.','link','Housing and motor are one rigid moving assembly.'),
('turn',6,'Pin terus berputar','Pin terus mengitari piringan. Setelah melewati bagian lintasannya, arah gerak kepala berbalik, meskipun piringan tetap berputar searah.','link','Crank continues while head reaches a smooth turning point.'),
('return',5,'Lalu kembali ke sisi lain','Batang kini membawa kepala ke sisi lain. Gerakan melingkar berubah menjadi ayunan melalui sambungan-sambungan ini.','macro','Return stroke with same closure and landmarks.'),
('pivot',5,'Penyangga menjadi acuan','Poros di leher menopang kepala yang berayun. Jangkar batang tetap berada pada penyangga sebagai acuannya.','link','Show two fixed but different points; no floating base.'),
('clutch',6,'Kenop memutus jalur ayunan','Pada tipe ini, kenop yang diangkat melepas kopling mekanisme ayunan. Piringan berhenti digerakkan, dan kepala mempertahankan arahnya.','clutch','Conceptual clutch separation, not unsupported internal ball geometry.'),
('blade',5,'Baling-baling tetap jalan','Baling-baling tetap berputar karena poros motor masih menggerakkannya. Yang dilepas hanya jalur menuju mekanisme ayunan.','side','Fixed head with running front blade and stopped disk.'),
('engage',6,'Disambungkan, ayunan kembali','Ketika kenop ditekan, jalur ayunan tersambung lagi. Roda gigi, piringan, dan batang kembali bekerja bersama.','clutch','Reengagement followed by resumed coupled motion.'),
('answer',8,'Putaran jadi ayunan','Jadi, motor tidak perlu bolak-balik. Pin berputar, batang menjaga jarak terhadap penyangga, dan kepala berayun. Itulah gerakan yang terlihat dari luar.','proof','Matched opening: exterior and exposed linkage demonstrate cause.'),
]
plan=[];t=0
for n,(key,d,title,text,view,job) in enumerate(rows,1):
 plan.append(dict(id=f's{n:02}-{key}',key=key,start=t,end=t+d,duration=d,title=title,text=text,view=view,job=job));t+=d
assert t==90
dump(V/'scene-plan.json',plan)
accounts=json.loads((R/'boards/di-balik-benda/ACCOUNTS.json').read_text(encoding='utf-8'))['accounts']
brief='''# Fan: continuous rotation becomes a head swing

board: di-balik-benda
board_revision: 6
topic_selection: auto
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
human_approved: false
pre_render_authorization: delegated by the user's --automation
requested_endpoint: publishing
delivery: queue
schedule: next configured slot, no displacement
commit: after pipeline completion

## Scope and direction
One new Indonesian 90-second explainer, 1080x1920, 30fps, 2700 frames, 16 shots. Curious general audience. Explain mechanical fan oscillation using the conventional motor/worm/clutch/carrier-disc/connecting-arm topology described in US7811059B2. Fixed illustrative crank radius: do not explain the patent's additional variable-angle control. Exact gearing ratios, speeds and dimensions are not product measurements. No repair or disassembly instructions. Not all fans use this mechanism.

Selected board [editorial](../../boards/di-balik-benda/EDITORIAL.md), [frame](../../boards/di-balik-benda/frame.md), SHOT-DIRECTION.md and DIRECTION.md v6. Illustrated 2.5D inspection bench, shaded thickness, fixed pale mineral ground #ECEEE9, ink #172B3B. Orange input, blue inspected linkage, teal output head. Large centered mechanism within x80..1000/y430..1410. Lower captions inherit actual stapler style: Manrope600 46px/1.3 at x108/y1500/width848, fitted pale blocks, at most two lines. This explicit board preference governs lower placement; leave room around platform controls, avoid right action rail, retain sidecars.

Narration uses one tagged ElevenLabs eleven_v4 request, voice resolved from root .env by maintained narration.py. BGM intentionally absent to expose speech and movement cues. SFX existing media-use assets and source-verified frozen material cues only, no new generation. Continuous gearing shares low-level representative cues; no claim of literal fan recording. Verify acoustic scene cuts and source-preserving observation pauses. Listening limits recorded honestly.

## Delegated topic selection
Ten candidates were presented in conversation before selection: mechanical oscillating fan, steam kettle, tape measure, hydraulic closer, iris aperture, pendulum escapement, reversible screwdriver, umbrella, mechanical pencil, toaster. Selected fan under --topic=auto. All eight rubric criteria: recognition strong (household fan); curiosity strong (continuous input versus reversing output); visual proof strong (fixed anchor and constant-length rod); causal depth strong (shared motor, gearing, eccentric, constraint, clutch); discovery strong (stationary anchor hidden under moving housing); motion diversity strong (rotation, yaw, pivoting, clutch travel); evidence strong (primary patent); scope workable (16 shots with fixed radius). Kettle/closer offer flow/thermal explanations but need more invisible-state encoding; iris/clock have stronger geometry demands; tape/pencil/screwdriver offer a narrower chain. No trends claimed.

Overlap checked TRACKER plus all production folder names, including unregistered roda-beda-putaran: this is a new question and mechanism, distinct from freehub coasting, music-box governor, seatbelt restraint, stapler, pump, cistern, lock and sewing. No recurring run: this invocation creates one episode.

## Hook selection before script
1. “Baling-balingnya terus searah. Kenapa kepala kipas bisa bergerak bolak-balik?” Behavior contrast; promises the crank-linkage answer.
2. “Satu motor, dua gerakan. Bagaimana kipas melakukannya?” Power-path angle; promises two branches.
3. “Kenop ditarik, kepala berhenti. Kenapa baling-baling tetap jalan?” State comparison; promises clutch isolation.
Recommended and selected 1 under delegated automation; not human approval. Research supports each. Script written after this selection.

## Story contract
First discovery at5–10s: shared shaft powers both front blades and rear mechanism. Linked questions: how power reaches rear disc → why pin orbits → why a rod cannot simply orbit freely → how fixed anchor forces head yaw → why clutch stops only this branch. Signature at35–48s: rigid rod holds its length between fixed anchor and orbiting pin while the head pivots. Show 4 diagnostic poses and emphasize two distinct fixed pivots. Opening and ending pair a running fan with now-visible hidden linkage. Head, gearbox and carrier-center positions move as one rigid assembly; stationary base never follows the head. Physical closure solved analytically at every seek. Stable landmarks: blue anchor A, dark neck pivot O, orange eccentric pin P.

## Publishing targets
Full inherited list from board ACCOUNTS.json:
'''
brief+='\n```json\n'+json.dumps(accounts,indent=2)+'\n```\n'
brief+='''
Preflight verified Admin's Workspace /01a171dd-5281-730d-af07-f2168d17add7; connected Instagram @dibalikbenda.id /01a172c9-3761-700a-9798-00febaa9fa90. Caller publishes directly, requires_approval false. Current content rules: instagram_reel, one video max900s/314572800bytes, caption2200 chars/5 hashtags. Configured queue in Asia/Jakarta; observed next slot2026-10-30T03:00Z (10:00WIB), recheck at delivery. Use queue next, no top insertion. Package and local upload authorized by user's queue endpoint.

Usage at start: session94%, weekly73% remaining. Context7 tools unavailable; pinned installed CLI documentation and command help used for execution. No skill upgrades performed. Existing untracked creative-direction skill is unrelated user work and excluded from this commit.

## Current state
Brief, research and script agent-verified. Next: visually verify full static storyboard before synthesis or animation. No preview started.
'''
write(P/'EPISODE.md',brief);write(V/'BRIEF.md',brief)
write(P/'SOURCES.md','''# Evidence and limits

Primary source body read through Jina MCP on2026-10-29, not just search snippets.

A. [US7811059B2 — Variable angle oscillating fan](https://patents.google.com/patent/US7811059B2/en). Motor shaft26 drives front blade14 and rear worm28. Clutch/worm unit16 transfers motion to toothed spindle18 meshing carrier disk20. Swinging arm30 joins guide pin34 beside stationary stand support36 and crank pin40 on disk20. Gear housing24 is secured to rear motor housing22. Knob44 down engages oscillation; up disengages while fan runs in a steady direction. This patent also adds variable-angle adjustment; this episode deliberately illustrates only its conventional oscillation topology at one illustrative radius.

B. [US1005429A — Oscillating fan](https://patents.google.com/patent/US1005429A/en). Primary historical corroboration of motor frame pivot, rear worm, gear reduction, crank/link and stationary stand reaction. Its lever and zero-throw control differ; do not combine its control geometry with A.

Rejected lead: WO2021186372A1 is a different moving-duct topology and is not evidence for the episode's moving motor head. Its text was inspected and excluded.

## Claim map
Shots1/2/14/16: continuous shared motor and front/rear branches → A shaft26/blade14/worm28 and knob44 description. Shots3/4: worm-unit/spindle/carrier power path → A unit16/spindle18/disk20. Tooth numbers and reduction speed are schematic, no numeric ratio claim. Shots5/6: eccentric pin orbit and articulated rod → A crank40 and arm30. Shots7–12: rod joins fixed stand guide34 to carrier crank40, housing24 fixed to motor22; head supported on stand → A. Constant rod length, analytic closure and smooth reversal are geometric implications of that topology, labeled explanatory modeling. Shots13–15: knob up disconnects oscillation, blade remains driven; knob down resumes → A. Internal clutch parts shown only as conceptual coupling faces, not an invented ball/detent design. No electronics, motor reversal, safety advice or claims about every fan.

## Illustration and sound boundaries
Original SVG geometry with shaded thickness, simplified housing, two-stage gear path, illustrated fixed crank radius. Gear teeth are schematic; not manufacturing tolerances, calibrated motion speed or real product dimensions. Planar linkage satisfies exact constant-length closure with both fixed pivots retained. Side/top views are deliberately reoriented and retain landmark colors. Gear rotations slowed for observation. No repair directions. Foley reused under original provenance and labeled illustrative. All factual narration and on-screen explanatory statements remain inside the map above.
''')
script='# Locked narration v1\n\nHook1 selected by agent under user automation. Timings below are estimates pending measured audio.\n\n'
for s in plan:script+=f'## {s["id"]} · {s["start"]}–{s["end"]}s\n\n{s["text"]}\n\nOn-screen title: {s["title"]}\n\n'
write(P/'SCRIPT.md',script.rstrip()+'\n');write(V/'SCRIPT.md',script.rstrip()+'\n')
write(V/'STORYLINES.md','''# Delegated storyline selection
Five seeds: follow one shaft; fixed-anchor mystery; knob comparison; exploded inventory; history of oscillation. Drop inventory/history because they delay causal proof.
1. Selected: familiar behavior, then follow power through shaded parts to a constant-length linkage; matched exterior/cutaway ending. First2s show blade spinning and head yaw. Pale bench, Manrope, dry foley, no music.
2. Knob comparison: alternating fixed/oscillating states, trace missing branch backwards; same medium, clutch-led sound. First2s pull knob.
3. Bold alternative: one continuous dive into the eccentric pin, then pull back to discover its fixed anchor; same medium and slow material cues. First2s macro pin movement, recognition weaker.
Selected1 under --automation, stronger exterior recognition. No extra storyline gate.
''')
spec='''GOAL: Viewer can explain why a continuously rotating fan motor produces a reversing head swing.
OUTPUT: HyperFrames1080x1920,30fps.
TIME:90s=2700frames.
LOOK: boardv6 mineral#ECEEE9, surface#F8F9F5, ink#172B3B, input#C94422, active#2459C4, output#167580. Manrope800 title70px/1.1, Manrope600 caption46px/1.3, Plex28px note. Illustrated metal gradients and side faces, depth10–16px, contact shadow10% opacity; no true3D.
OBJECTS: recognizable caged fan blades, motor housing, neck and stand, rear worm and gearing, carrier disk with offset pin, rigid bearing-ended rod, fixed anchor, conceptual clutch and knob.
MOTION: analytic four-bar closure every frame, motor rotation independent of head yaw; smooth physical rotary motion, reframe cuts preserve landmarks; editorial reveals only power2out0.3s. No arbitrary elastic metal.
BANNED: flat standalone diagrams, tiny objects, unanchored rods, fixed gearbox while head turns, fake motor reversals, arbitrary repeated loops, glow, dark voids, grain, decorative HUD, invented technical tolerances, front-loaded component inventory. Board explicitly requests pale canvas/centered mechanism/lower captions.
QA: all16 shot midpoints;4 poses at fixed-anchor signature;both head reversal points;clutch before/after;first and final matched proof;word captions no more2lines.
SHOTS:\n'''
spec+='\n'.join(f'{round(s["start"]*30)}..{round(s["end"]*30)-1}: {s["id"]}; {s["job"]}; title {s["title"]}; local material cue at functional motion onset; next dependency follows.' for s in plan)
write(V/'SPEC.md',spec+'\n')
story='---\nformat: 1080x1920\nduration: 90s\nmode: autonomous\nmessage: A constant-length rod anchored to the stand turns rotary input into head yaw.\narc: Behavior → shared motor → eccentric → fixed anchor → constraint → clutch → proof\naudience: Curious Indonesian general audience\n---\n'
for n,s in enumerate(plan,1):
 story+=f'\n## Frame {n} — {s["title"]}\n\n- status: built\n- src: compositions/{s["id"]}.html\n- duration: {s["duration"]}s\n- poster: {s["start"]+s["duration"]*.55:.3f}s\n- transition_in: cut\n- scene: {s["job"]}\n- voiceover: {s["text"]}\n- reads: title stable0..{s["duration"]}s; active mechanism central; short spoken caption at lower anchor\n- sound: illustrative material travel/contact cue; shared continuous action, no BGM\n\nNew discovery: {s["job"]} Question answered by visible transfer, next shot follows dependency. First-use part appears in function. 2.5D shaded parts, top/side framing chosen to expose relationship; A fixed anchor/O neck/P pin landmarks retained. Attention passes from orange input to blue linkage and teal output. Diagnostic poses: initial, input advance, constrained response, held result; signature frame8 uses four measured closure poses. Explicit slow schematic observation, no dimensional claim.\n'
write(V/'STORYBOARD.md',story)
shutil.copy2(R/'boards/di-balik-benda/frame.md',V/'frame.md')
for name in ['manrope.ttf','ibm-plex-mono.ttf']:
 src=R/'productions/freehub-roda-tetap-melaju/video/assets/fonts'/name; dest=V/'assets/fonts'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
for f in (R/'productions/freehub-roda-tetap-melaju/video/assets/fonts').glob('*'):
 if f.suffix not in ['.ttf','.woff','.woff2']:shutil.copy2(f,V/'assets/fonts'/f.name)
t=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'))
assert not any(x['slug']==P.name for x in t['productions'])
t['productions'].append(dict(slug=P.name,topic='Mechanical oscillating fan: shared motor, worm gearing, eccentric carrier pin, fixed-anchor connecting rod, head pivot and oscillation clutch',board='di-balik-benda',stage='storyboard',status='in_progress',path=P.relative_to(R).as_posix()))
dump(R/'TRACKER.json',t)
print(json.dumps(dict(scenes=len(plan),duration=t and 90,words=sum(len(s['text'].split()) for s in plan))))
