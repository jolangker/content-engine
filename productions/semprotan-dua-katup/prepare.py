from pathlib import Path
import json, shutil, subprocess, importlib.util
P=Path(__file__).resolve().parent; R=P.parent.parent; V=P/'video'
def write(path,text): path.write_text(text,encoding='utf-8')
def dump(path,obj): write(path,json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
write(V/'BRIEF.md','''---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "A trigger pump alternates discharge and refill using pressure and two check valves."
destination: instagram-reels
aspect: 1080x1920
language: id
audience: curious Indonesian general viewers
length: 90s
angle: one complete conventional trigger-pump cycle
board: di-balik-benda-v3
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
pre_render_authorization: delegated by the user's --automation instruction
endpoint: publishing
delivery: publish
---

## Intent
Original sectional illustrations explain trigger input, piston displacement, inlet/outlet gating, nozzle output, spring return, refill and bottle venting. Follow one blue piston seal through the views. No stock footage or branded product.

## Notes
Inherit ../../../../boards/di-balik-benda/frame.md. The 90-second, 30 fps output includes Indonesian continuous ElevenLabs eleven_v4 narration and spoken-word captions. Static storyboard artifacts, including a complete PNG, are required before synthesis even though storyboard:no delegates human checkpoints. Agent verification replaces human approval. Target: My Organization, Instagram dibalikbenda.id, connected channel 6adccfe4778b240e2fafeaf9. Original schematic geometry, not to scale; a conventional spring-return design, not a universal or continuous-spray design. External publication and hosting are explicitly authorized. Do not reuse another episode's audio.
''')
shortlist=[
('Pompa semprotan botol','How do two check valves turn alternating piston motion into directed spray and refill? Trace lever, piston, valves, return and vent.','APG manufacturer guide; selected: strong evidence and distinct pressure/flow stages'),
('Dongkrak hidraulis','How does repeated movement of a small pump lift a larger ram? Show inlet, delivery and release paths.','Enerpac hydraulic hand-pump documentation lead; requires variant-specific geometry'),
('Kompresor piston','How does crank rotation alternate intake and discharge? Follow connecting rod, piston and reed valves.','Atlas Copco compressor documentation lead'),
('Pelampung tangki toilet','How does falling water open a fill valve and rising water shut it? Follow float and control linkage.','Fluidmaster fill-valve documentation lead; variant must be fixed'),
('Escapement jam','How do a wheel, pallet and balance meter stored energy? Follow locking, impulse and release.','Watchmaking technical-manual lead; detailed contact timing costly'),
('Derailleur sepeda','How does a shift move a chain between sprockets? Trace cage and tooth pickup.','Shimano technical documentation lead; geometry demanding'),
('Retraktor sabuk','Why can slow withdrawal work while sudden motion locks? Separate sensing and pawl engagement.','Automotive supplier patent lead; safety claims excluded'),
('Termostat ketel','How can a bimetal element trip the switch? Trace steam path and reset.','Strix technical documentation lead; exact design needed'),
('Kopling bor','What slips when the set torque is exceeded? Follow preload, ramp and detent.','Power-tool manufacturer patent lead; no numerical torque claim'),
('Penggerak wiper','How does rotating input produce a reversing sweep? Follow crank and coupled links.','Wiper linkage manufacturer documentation lead; alternate lower-depth choice')]
rows='\n'.join(f'| {i+1} | {a} | {b} | {c} |' for i,(a,b,c) in enumerate(shortlist))
write(P/'EPISODE.md',f'''# Episode: Two valves inside a trigger sprayer

- Scheduled run: produksi-harian-di-balik-benda, 2026-10-25 10:00 Asia/Jakarta.
- User invocation: `$shortform-production --board=di-balik-benda --topic=auto --automation --delivery=publish --channel=instagram:dibalikbenda.id`
- topic_selection: auto; delegated agent choice, not human approval.
- Board: [DIRECTION v3](../../boards/di-balik-benda/DIRECTION.md), [editorial](../../boards/di-balik-benda/EDITORIAL.md), [canonical frame](../../boards/di-balik-benda/frame.md), [shot direction](../../boards/di-balik-benda/SHOT-DIRECTION.md).
- Topic: one conventional spring-return trigger sprayer with two one-way valves; primed pumping cycle plus a clearly separate priming explanation. Not an all-plastic or continuous-spray product demonstration.
- Format: exactly 90 seconds, 1080x1920, 30 fps; Indonesian; original shaded sectional diagrams and continuous narration.
- Overlap check: tracker and filesystem reviewed. Sewing lockstitch, cylinder lock, open differential and relationship episode ask different questions. Older pen, zipper, clothespin and cable-tie subjects excluded. Existing differential folder and tracker modifications belong to earlier work and must remain outside this run's commit.
- execution_policy: automation; automation_after: none; automation_state: active; human_review: none.
- pre_render_authorization: delegated by user's --automation instruction. Static storyboard and PNG remain required, agent-verified before narration/animation.
- Endpoint: publishing; delivery: immediate publish; no stage cap.
- Organization: My Organization, 691274923530437a1a02ed9f. Account and channel checked live on 2026-10-25.
- Exact channel: Instagram dibalikbenda.id, 6adccfe4778b240e2fafeaf9, business, connected, unlocked, automatic posting, Asia/Jakarta.
- Settings: Reel; share to feed true; synthetic narration disclosure true. No partnership or performance claims.
- Audio: project-root default voice and eleven_v4; one tagged full-script request. BGM and SFX to be resolved before audio completion.
- Preview: none started; no inherited preview owned by this production.
- Usage: initial CLI read 97% session, 89% weekly remaining, known; this does not reserve allowance.

## Topic shortlist and delegated selection

| # | Topic | Brief / audience question | Evidence lead and comparison |
| --- | --- | --- | --- |
{rows}

Selected #1: lever-to-piston motion, valve seating/unseating and opposite flow paths produce several distinct causal interactions in one coherent cycle. Evidence leads for unselected candidates are research directions, not verified episode claims. APG guide fetched and patent description cross-checked. No trending claim.

## Hook selection before drafting

1. "Kenapa semprotan botol tidak menyedot cairan kembali dari ujungnya?" Opens on the two-valve routing question; recommended and selected.
2. "Jari kamu cuma bergerak sedikit. Di dalamnya, dua katup bergantian bekerja." Opens on input-to-flow coordination.
3. "Saat kamu melepas pemicu, semprotan ini justru sedang mengisi ulang." Opens on the less visible return stroke.

Agent selected #1 after research under active automation. The script answers it by contrasting pressure and refill states, without promising that every nozzle has identical internals.

## State

Brief and research verified; script agent-verified. Next: complete 16-pose static storyboard before paid narration. No human approval claimed.
''')
write(P/'SOURCES.md','''# Evidence and claim map

Research date: 2026-10-25. Tavily search and extract used. A raw-content search option failed validation, and initial extraction printing failed Windows encoding; plain extraction with UTF-8 succeeded. Complete results saved in research-extract.json; no search fallback needed.

S1. APG Packaging, manufacturer guide, https://apackaginggroup.com/blogs/news/all-plastic-trigger-sprayer-guide . The "How a trigger sprayer works" section states lever drives piston, pressure closes inlet and opens outlet, nozzle forms the output, return resets, dip tube refills. It separately distinguishes conventional metal springs from all-plastic return designs. The venting section explains replacement air and bottle collapse. Use only these operating principles; no recyclability or commercial claims.

S2. Original technical disclosure US20140014691A1, https://patents.google.com/patent/US20140014691A1/en . Detailed description around FIG. 1 states spring-driven piston return draws liquid through dip tube/check valve; opposite stroke drives discharge. This is a pre-compression variant, used only to cross-check fluid routing and reset, not to import its exact valve geometry or threshold into a generic sprayer.

| Claim | Evidence | Boundary |
| --- | --- | --- |
| C1: trigger drives piston into cylinder, reducing liquid chamber volume | S1 cycle 1–2; S2 FIG.1 description | Original schematic lever/cylinder orientation, not a manufacturer's drawing |
| C2: discharge pressure seats inlet and opens outlet, directing fluid to nozzle | S1 cycle 2; S2 discharge description | Ball symbols represent one-way function; real valve shapes vary |
| C3: nozzle forms spray, stream or foam | S1 cycle 3 and nozzle options | Show spray only; no particle size or internal swirl claim |
| C4: return spring moves piston back, chamber expands and draws liquid via tube | S1 cycle 4–5 and conventional spring distinction; S2 spring return | Pressure drawn schematically; liquid is not visibly compressed |
| C5: outlet closes on refill while inlet opens, preventing inlet-to-bottle return during discharge and nozzle backflow on refill | S1 coordinated two-valve cycle; S2 check valve / opposing valve mechanism | Schematic ball seats and exaggerated clearances |
| C6: air replaces dispensed liquid through vent | S1 venting section | Functional separate path only; exact vent geometry omitted |
| C7: priming differs from the already liquid-filled working cycle | S1 says test priming; S2 pump cylinder draws from dip tube | Limit wording to initially air-filled chamber needing pumping until liquid reaches it; no fixed number of strokes |

## Visual provenance
All diagrams are original SVG, with conventional spring-return pump principles. Removed shell, fluid arrows, exaggerated valve travel and non-scale spacing are labeled. The illustrative liquid level is a reference, not a measured dose; short demonstrations do not imply visible bottle depletion per stroke. No spray chemistry, safety, efficiency or universality claim. No source image copied. Board fonts copied with their licenses.
''')
data=[
('whole','Dua katup. Satu arah.','Kenapa tidak tersedot dari ujung?','Kenapa semprotan botol tidak menyedot cairan kembali dari ujungnya? Jawabannya ada pada dua katup yang bergantian membuka.',7,'Show the familiar output and the question; one complete explanatory cycle, label replay.'),
('explode','Buka kepala pompa','Pemicu → piston → katup → nosel','Kita lihat pompa pemicu konvensional. Di balik cangkangnya ada piston, pegas, jalur masuk, dan jalur keluar.',6,'Separate functional assemblies along retained axes without pretending this is operating motion.'),
('chamber','Satu ruang berubah volume','Piston biru menjadi patokan','Piston membatasi sebuah ruang pompa. Segel di sisinya membantu cairan tetap berada di jalur yang dirancang.',5,'Cutaway exposes blue piston seal and the fluid chamber; no nozzle flow yet.'),
('press','Jari mendorong piston','Ruang pompa mengecil','Saat pemicu ditarik, tuas mendorong piston ke dalam. Ruang cairan mengecil, sehingga tekanannya naik.',6,'Concurrent lever rotation, linkage motion, piston translation and spring compression; hold input end.'),
('inlet','Jalur masuk menutup','Cairan tidak kembali ke botol','Tekanan itu menekan katup masuk ke dudukannya. Jalan kembali menuju botol tertutup.',5,'Macro inlet valve stays on seat while upper chamber is pressurized.'),
('outlet','Jalur keluar membuka','Tekanan mengangkat katup keluar','Pada jalur satunya, tekanan membuka katup keluar. Cairan kini punya jalan menuju nosel.',6,'Macro outlet ball lifts downstream; distinguish opened clearance and fixed seat.'),
('spray','Cairan menjadi semprotan','Nosel membentuk pola keluaran','Cairan melewati nosel, lalu keluar sebagai semprotan. Bentuk nosel menentukan pola yang dihasilkan.',5,'Trace through outlet into an enlarged nozzle and discrete outgoing droplets; no inward droplets.'),
('spring','Lepas jari, pegas kembali','Energi tersimpan mengembalikan piston','Begitu jari melepas pemicu, pegas yang tadi tertekan mengembalikan piston dan tuas.',6,'Spring expands while piston and lever return, same blue seal landmark.'),
('expand','Ruang pompa membesar','Tekanan di dalam turun','Ruang pompa membesar lagi. Tekanan di dalamnya turun dibandingkan cairan di botol.',5,'Volume grows with retreating piston; chamber comparison before/after, no fluid compression.'),
('close','Ujung tidak menjadi jalan masuk','Katup keluar duduk kembali','Sekarang katup keluar menutup. Udara atau cairan dari ujung tidak ditarik kembali lewat jalur itu.',6,'Outlet reseats before inlet refill path is emphasized; reverse-flow stop is diagrammatic.'),
('refill','Giliran katup masuk membuka','Cairan naik dari botol','Sebaliknya, katup masuk membuka. Cairan dari botol naik melalui pipa celup, mengisi ruang pompa.',6,'Upstream tube flow, inlet lift and open clearance occur together during return stroke.'),
('ready','Satu dosis berikutnya siap','Ruang terisi, piston kembali','Saat piston kembali, ruang itu sudah terisi untuk tekanan berikutnya. Dua katup mengarahkan aliran secara bergantian.',5,'Trace filled chamber and both resting valve states; no invented interlock.'),
('vent','Botol juga perlu udara pengganti','Ventilasi berbeda dari jalur semprot','Cairan yang meninggalkan botol perlu digantikan udara. Jalur ventilasi membantu botol tidak terus mengempis.',6,'Whole-bottle context with separate headspace vent; do not route air through liquid outlet.'),
('prime','Kalau pompa masih berisi udara?','Pemompaan awal / priming','Pada awal pemakaian, ruang pompa bisa masih berisi udara. Beberapa gerakan awal membawa cairan sampai ke pompa.',6,'Explicit alternate initial state, rising liquid front through dip tube; stroke count not literal.'),
('compare','Tekan dan lepas berbeda tugas','Tekan: keluar · lepas: isi ulang','Jadi, menekan pemicu mengeluarkan cairan. Melepasnya menyiapkan isian berikutnya. Katup masuk dan keluar bertukar peran.',6,'Aligned pressure/refill comparison with opposing valve openings, not two identical loops.'),
('final','Gerak bolak-balik, aliran searah','Dua langkah menjadi satu siklus','Gerakan tangan memang bolak-balik. Tetapi dua katup membuat aliran utamanya tetap searah: dari botol menuju nosel.',4,'Return to original bottle; one coordinated cycle and readable final hold.')]
assert sum(x[4] for x in data)==90
scenes=[];t=0
for i,(view,title,subtitle,vo,duration,purpose) in enumerate(data):
    scenes.append(dict(number=i+1,id=f's{i+1:02}-{view}',view=view,title=title,subtitle=subtitle,vo=vo,duration=duration,start=t,purpose=purpose));t+=duration
dump(V/'scene-plan.json',dict(duration=90,scenes=scenes))
script='# Script — agent-verified v1\n\nIndonesian narration, estimated 90 seconds. Diagram labels are separate from spoken captions. No human approval claimed.\n\n'
for s in scenes: script+=f'## {s["number"]:02} — {s["title"]}\n\n{s["vo"]}\n\nOn screen: {s["title"]}; {s["subtitle"]}. Evidence: C1–C7 as mapped in SOURCES.md.\n\n'
write(P/'SCRIPT.md',script);write(V/'SCRIPT.md',script)
sb='''---
format: 1080x1920
duration: 90s
message: "Two valves direct a trigger pump's discharge and refill strokes."
arc: familiar output → pressure stroke → return and refill → complete cycle
audience: curious Indonesian general viewers
mode: autonomous
music: none
---

## Video direction
Inherit board v3 palette, Manrope and IBM Plex Mono. Pale bench, shaded mineral shell, orange finger/trigger input, blue piston seal landmark, teal flow output. Original functional cross-section; disassembly and macros retain axes. Caption keep-out: y=1550–1740, annotations above y=1470; no UI badges. Hard cuts mark different explanatory questions. Source boundaries in ../SOURCES.md apply to geometry and arrows. Static storyboard required before synthesis; agent review replaces human layout approval. Mechanical motion is a shared scalar state with SVG attribute updates, following svg-icon-enrichment and control-target-sync principles. No worker delegation permission supplied: execute the frame-worker fallback serially, keeping each composition independently mounted. No repeated identical operating loop in three consecutive shots.
'''
for s in scenes:
    sb+=f'\n## Frame {s["number"]} — {s["title"]}\n\n- status: built\n- src: compositions/frames/{s["id"]}.html\n- duration: {s["duration"]}s\n- start: {s["start"]}s\n- transition_in: cut\n- poster: {s["duration"]*.6:.2f}s\n- scene: {s["purpose"]}\n- voiceover: "{s["vo"]}"\n- blueprint: compose\n- motion: svg-icon-enrichment, control-target-sync\n- focal: original {s["view"]} pump section\n- roles: pump foreground; anchored labels supporting; pale bench background\n- evidence: ../SOURCES.md C1–C7\n\nNew information: {s["purpose"]}\nState continuity: blue piston seal, left input/right output axis. Macros show the same inlet or outlet seat. Priming is explicitly a different initial condition.\nScene 1 (0–0.5s): establish the named view and its question.\nScene 2 (0.5–{s["duration"]*.8:.2f}s): show the causally relevant action in continuous intermediate poses. Diagnostic poses: before input, contact/clearance change, flow consequence.\nScene 3 ({s["duration"]*.8:.2f}–{s["duration"]}s): hold the outcome; keep fixed seats and housing stationary.\nRhythm: {"longer contact observation" if s["view"] in ["inlet","outlet","refill","close"] else "orientation, transfer or system consequence"}. On-screen words: {s["title"]}; {s["subtitle"]}.\n'
write(V/'STORYBOARD.md',sb)
shutil.copy2(R/'boards/di-balik-benda/frame.md',V/'frame.md')
(V/'assets/fonts').mkdir(parents=True,exist_ok=True)
for n in ['manrope.ttf','ibm-plex-mono.ttf','Manrope-OFL.txt','IBM-Plex-Mono-OFL.txt']:shutil.copy2(R/'boards/di-balik-benda/assets'/n,V/'assets/fonts'/n)
(V/'capture/extracted').mkdir(parents=True,exist_ok=True)
write(V/'capture/extracted/visible-text.txt','User invocation: $shortform-production --board=di-balik-benda --topic=auto --automation --delivery=publish --channel=instagram:dibalikbenda.id\nSelected topic: conventional trigger sprayer pump with two check valves.\n'+(P/'SOURCES.md').read_text(encoding='utf-8'))
dump(V/'capture/extracted/tokens.json',dict(title='Semprotan dua katup',description='Conventional trigger pump cycle',colors=[],fonts=[]))
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'))
dump(P/'run-baseline.json',dict(scheduled_run='2026-10-25T10:00:00+07:00',initial_tracker=tracker,initial_git_status=subprocess.check_output(['git','status','--short'],cwd=R,text=True)))
assert not any(x['slug']==P.name for x in tracker['productions'])
tracker['productions'].append(dict(slug=P.name,topic='Conventional trigger sprayer: lever, piston, inlet/outlet check valves, spring return, refill and bottle venting',board='di-balik-benda',stage='storyboard',status='in_progress',path='productions/'+P.name))
dump(R/'TRACKER.json',tracker)
spec=importlib.util.spec_from_file_location('narration',R/'.agents/skills/shortform-production/scripts/narration.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
voice=mod.resolve_voice(R)
if isinstance(voice,tuple):voice=voice[0]
tags=['[curious, clear]','[explaining patiently]','[focused]','[guiding the listener]','[precise]','[slightly brighter]','[clear]','[gentle emphasis]','[explaining]','[precise]','[guiding]','[assured]','[matter-of-fact]','[curious]','[contrasting clearly]','[warm, concluding]']
dump(V/'audio_request.json',dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=dict(source='project_env',key='ELEVENLABS_VOICE_ID'),tts_model='eleven_v4',speed=1.0,lines=[dict(id='narration',text='\n\n'.join(tag+' '+s['vo'] for tag,s in zip(tags,scenes)))],bgm=dict(mode='none')))
print(json.dumps(dict(scenes=len(scenes),duration=t,words=sum(len(s['vo'].split()) for s in scenes),voice=voice)))
