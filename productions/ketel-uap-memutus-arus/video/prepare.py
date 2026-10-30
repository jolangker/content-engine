"""Freeze the selected episode before storyboard, narration and animation."""
from pathlib import Path
import json, shutil, hashlib, sys
V=Path(__file__).resolve().parent; P=V.parent; R=V.parents[2]
sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'))
from narration import resolve_voice
def write(p,s):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def dump(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
rows=[
 ('mystery','Kok tahu harus mati?',4,'whole','Airnya mendidih. Kok ketelnya tahu kapan harus mati?', 'Opening: powered kettle boils, switch rises and heater loses power.', 'whole'),
 ('steam','Uap membawa sinyal',6,'section','Pada ketel jenis ini, uap punya saluran menuju pemutus listrik. Kita ikuti jalurnya.', 'First discovery: reveal rear steam duct from headspace to external control, at 8s.', 'steam'),
 ('input','Mulai dari sakelar',5,'whole','Kita ulang dari awal. Saat sakelar ditekan, mekanisme di dalamnya menutup kontak.', 'Explicit rewind; input knob rotates over-centre lever; closed state maintained.', 'on'),
 ('circuit','Kontak bertemu',5,'contacts','Dua kontak logam bertemu. Rangkaian tersambung, sehingga arus dapat mengalir ke elemen pemanas.', 'Contact faces touch; current path illuminates only after contact.', 'close'),
 ('heater','Listrik menjadi panas',5,'heater','Hambatan elemen mengubah energi listrik menjadi panas. Panasnya diteruskan ke air di atasnya.', 'Concealed heater section and conduction into water; no steam jet yet.', 'heat'),
 ('boil','Air mulai mendidih',6,'section','Saat air mendidih, uap terbentuk dan memenuhi ruang di bawah tutup.', 'Bubbles rise; headspace vapour increases, lid remains closed.', 'boil'),
 ('route','Jalurnya turun',6,'duct','Sebagian uap masuk ke saluran khusus. Jalurnya membawa uap turun menuju unit pemutus.', 'Trace continuous headspace inlet, descending duct and lateral outlet.', 'route'),
 ('sensor','Di luar ruang air',5,'control','Di ujung saluran ada cakram peka panas. Letaknya di luar ruang air, bukan terendam.', 'Duct outlet heats dry bimetal; cut shell distinguishes wet/dry spaces.', 'sensor'),
 ('layers','Dua logam disatukan',6,'disc','Cakram ini dibuat dari dua logam yang disatukan. Ketika dipanaskan, keduanya memuai dengan besaran berbeda.', 'Explanatory separated layer view then bonded curved laminate.', 'layers'),
 ('curve','Bentuknya berubah',6,'disc','Karena terikat, perbedaan pemuaian mengubah kelengkungannya. Bentuk cakram dirancang untuk berpindah dengan gerakan sentak.', 'Bonded layers remain bonded; curvature grows before snap, displacement enlarged.', 'curve'),
 ('snap','Sentakannya memicu tuas',7,'snapmacro','Ketika cukup panas, cakram menyentak. Pada contoh mekanisme ini, gerak itu mendorong tuas melewati posisi tengahnya.', 'Signature: tongue approaches fixed pillar, bears on it, rotates lever through dead centre.', 'snap'),
 ('spring','Pegas mempertahankan posisi',6,'springmacro','Pegas kemudian membantu tuas berpindah ke posisi mati. Perhatikan batang penghubung yang ikut bergeser.', 'Over-centre spring passes pivot line, lever tab translates link.', 'trip'),
 ('open','Kontak terpisah',6,'contacts','Batang ini memisahkan kontak. Jalur listrik terputus, sehingga pasokan energi ke elemen berhenti.', 'Link stop displaces resilient contact strip; visible gap then current stops.', 'open'),
 ('residual','Panas belum langsung hilang',5,'heater','Pemanasnya mati, tetapi panas yang sudah tersimpan tidak langsung hilang. Gelembung mereda setelahnya.', 'Current stays absent; retained heat and bubbles decay rather than vanish instantly.', 'residual'),
 ('off','Tetap di posisi mati',5,'control','Mekanisme tetap di posisi mati. Untuk menyalakannya lagi, sakelar perlu ditekan kembali.', 'Disc cools back but over-centre lever and separated contacts remain off.', 'latch'),
 ('proof','Uap, gerak, lalu putus',7,'section','Jadi, pada ketel ini: air mendidih, uap memanaskan cakram, tuas bergerak, lalu kontak terputus. Itulah sebabnya ketel mati sendiri.', 'Matched opening proof: clearly labelled condensed replay through full causal chain.', 'proof'),
]
plan=[];t=0
for n,(key,title,d,view,text,action,mode) in enumerate(rows):
 plan.append(dict(id=f's{n+1:02}-{key}',key=key,title=title,start=t,end=t+d,duration=d,view=view,text=text,action=action,mode=mode));t+=d
assert t==90
dump(V/'scene-plan.json',plan)
accounts=R/'boards/di-balik-benda/ACCOUNTS.json'
targets=dict(source='board',board_accounts_file=accounts.relative_to(R).as_posix(),board_accounts_sha256=hashlib.sha256(accounts.read_bytes()).hexdigest(),accounts=json.loads(accounts.read_text())['accounts'])
write(P/'EPISODE.md', '''# Kettle: steam disconnects the circuit

board: di-balik-benda
board_revision: v6 (2026-10-27)
topic_selection: auto
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
human_approval: false
pre_render_authorization: delegated by the user's --automation instruction
requested_endpoint: publishing
delivery: queue
schedule: next configured slot, Asia/Jakarta, no custom time
commit: after the pipeline completes; include only this run's changes

## Brief and frozen direction
An Indonesian 90-second 1080x1920, 30fps illustrated 2.5D explanation for curious general viewers. Exact scope: steam-actuated snap-disc and over-centre mechanical switch; selected geometry is an original, simplified sectional interpretation of US4357520A, not a production drawing or universal kettle design. Keep the steam actuator distinct from the separate dry-boil protector, which is outside the explanation. Do not imply steam enters electrical contacts. Mechanism deliberately enlarged and operation slowed; heating time compressed. No repair directions.

Inherit [editorial](../../boards/di-balik-benda/EDITORIAL.md), [visual tokens](../../boards/di-balik-benda/frame.md), and [shot direction](../../boards/di-balik-benda/SHOT-DIRECTION.md). Caption treatment Manrope60046px at y1500, max2lines. Large fitted mechanism stage x80..1000/y430..1410. Narration ElevenLabs eleven_v4, root-env voice; separate existing SFX. BGM intentionally absent to expose small interaction sounds.

## Delegated topic decision
Shortlist presented in conversation: kettle, toaster, differential, salad spinner, automatic umbrella, tape measure, can opener, bicycle bell, wiper, pendulum clock. Existing tracker and production folder names inspected: selected question, actuation and takeaway do not duplicate sewing, lock, sprayer, cistern, stapler, music box, seatbelt, freehub, oscillating fan or mechanical pencil episodes. Wiper is related to the fan's rotary/oscillating linkage and therefore ranks lower for novelty. Kettle is selected for everyday recognition, a concrete shutoff question, and supported visible proof, not for ease of animation.

| Candidate | Recognition | Question | Visual proof | Causal depth | Discovery | Motion diversity | Evidence | Scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kettle | strong: daily boiling | strong: why off? | strong: duct/disc/contact | strong: four handoffs | strong: hidden dry sensor | strong: flow/flex/rotate/slide | strong: patent+engineering body | workable: one shutoff cycle |
| Toaster | strong | strong: why pop? | strong: latch/release | strong | strong | strong | workable: circuit variant needs lock | workable |
| Differential | strong encounter, hidden part | strong: unequal wheel speeds | workable: bevel mesh | strong | strong | workable: mainly rotation | workable | workable: complex tooth geometry |
| Salad spinner | workable | strong: press→spin | strong | strong | strong | strong | workable: US7621213B2 | workable |
| Umbrella | strong | strong: small button→opening | strong | strong | strong | strong | workable: US20090293925A1 | workable: telescoping variant |
| Tape measure | strong | strong: rewind | strong | workable | workable | strong | workable: US5210956A | workable |
| Can opener | strong | strong: cut+advance | strong | strong | strong | strong | workable: US1617142A | workable |
| Bicycle bell | strong | strong: repeated hits | strong | workable | strong | strong | workable: CN206466078U | workable |
| Wiper | strong | strong: turn→sweep | strong | strong | workable | strong | workable: EP0683076A1 | workable, related fan angle |
| Pendulum | strong | strong: paced gear motion | strong | strong | strong | strong | workable: authoritative educational lead | workable: select escapement |

All assessments are editorial, not retention predictions. Evidence leads for alternatives are discovery only, not completed claim verification.

## Hook checkpoint, before script drafting
1. “Airnya mendidih. Kok ketelnya tahu kapan harus mati?” — observable mystery and full causal promise. Recommended and selected under delegated automation.
2. “Uap ini punya jalur lain: menuju sakelar.” — hidden route opener.
3. “Dua lapis logam kecil ini ikut mematikan ketelmu.” — component-first opener.

Central mystery: why does a boiling kettle switch off? First discovery: uap menuju unit pemutus through the revealed duct, approximately8s. Chain: what carries the signal? → where does it arrive? → why does the disc change? → how does that separate contacts? Signature: steam-heated snap disc trips the over-centre lever, then link separates contacts. Opening and ending share kettle/lid/handle landmarks; final condensed replay exposes the cause. s03 explicitly rewinds after opening discovery. s16 explicitly replays, not an extra unexplained automatic cycle.

## Publishing targets
```json
'''+json.dumps(targets,indent=2)+'''
```
Preflight: Trypost Local, Admin's Workspace, exact board account connected, caller publishes directly; Instagram Reel supports90s. Queue configured10:00 daily Asia/Jakarta. No remote post created yet.

## State
Research and script agent-verified; storyboard is next. No human approvals asserted. Native narration and delivery files will be preserved. Listening capability unavailable unless a suitable tool becomes available.
''')
write(P/'SOURCES.md','''# Sources and claim map

Bodies read with Jina on2026-10-31; supporting evidence is separate from original illustration and editorial timing.

- S1: [US4357520A, John C. Taylor,1982](https://patents.google.com/patent/US4357520A/en). Primary selected control mechanism: headspace aperture43, passage44/channel47; steam actuator22 and tongue23, fixed pillar24; lever16, knife-edge pivot17, two over-centre C-springs19; lever portion26 engages link12; stop29 moves resilient strip27 and separates contacts7/8. Knob28 manually restores the lever. Separate dry-switch-on actuator9 is not the steam actuator and is omitted from the film's active chain.
- S2: [Royal Academy of Engineering, Ingenia, September2019](https://www.ingenia.org.uk/articles/how-do-kettles-know-when-to-switch-off). Explains resistance heating, steam duct typically through handle to dry control, bonded metals with different expansion, abrupt reversal of curved disc; diagram credited to Strix. Article body read, including actual mechanism paragraphs; boilerplate ignored.
- S3: [Chris Woodford, Explain That Stuff, kettle article](https://www.explainthatstuff.com/how-electric-kettles-work.html). Cross-check of steam duct, snap action, lever trips circuit; actual disassembly pictures and patent diagram. Also notes electronic temperature-control variants, so no universal claim.

| Claim / visual | Evidence | Boundary |
| --- | --- | --- |
| Closing contacts powers resistive element; heat reaches water | S1 contacts7/8 + element39; S2 heating description | Illustrative concealed heater; no numerical power/temperature claims |
| Boiling sends steam from headspace down dedicated passage | S1 aperture43/passage44/channel47; S2,S3 | Lid closed; duct geometry simplified, clear separation from contact chamber; vapour marks are schematic, not droplet scale |
| Sensor outside water, heated by steam | S1 actuator22 route; S2 | Steam-sensitive mechanical variant only, not every kettle |
| Bonded metals expand differently and curved actuator snaps | S2,S3 | Layer separation is explanatory assembly view only; layers remain bonded in operation; enlargement/slowing labelled |
| Tongue bears on pillar, lever trips through over-centre springs | S1 detailed description and FIG2/3 | Simplified 2.5D side section; two paired springs represented side-by-side; no fabricated switch dimensions |
| Lever portion moves link; strip/contact separate | S1 parts26/12/29/27/7/8 | Gap and stroke enlarged; electric flow is indicated only on closed circuit |
| Remains off until manual reset | S1 over-centre lever, knob28 | Cooling disc is not automatic restart; no reset under unsafe conditions shown |
| Heat does not vanish instantaneously when input stops | Inference from retained thermal energy, consistent with S2 heating | Qualitative explanatory physical inference; no cooling-time claim; heating/cooling duration compressed |

## Geometry and media
Original SVG illustration, not copied product art. Use S1 relationships, not a brand-specific replica; bulk materials and lever thickness are illustrative. Onscreen qualification names the steam-switch variant and slowed/enlarged section. Source diagrams guide hidden relationships; exported scenes do not reproduce source image pixels. Local board font files with OFL licenses. Existing sound assets retain their own provenance; stylized cues do not claim field-recorded kettle realism.
''')
script='# Ketel: uap memutus arus\n\nLanguage: Indonesian. Agent-verified under automation;90s planned. Narration separate from screen titles; exact measured windows follow timing.json.\n\n'
for s in plan:script+=f'## {s["id"]} ({s["start"]}–{s["end"]}s estimated)\n\n{s["text"]}\n\nOn-screen: **{s["title"]}**\n\n'
write(P/'SCRIPT.md',script);write(V/'SCRIPT.md',script)
write(V/'BRIEF.md',(P/'EPISODE.md').read_text(encoding='utf-8'))
write(V/'frame.md',(R/'boards/di-balik-benda/frame.md').read_text(encoding='utf-8'))
write(V/'SPEC.md','''GOAL: Viewer can follow steam→snap disc→lever/link→contact gap and explain the kettle shutoff.
OUTPUT: HyperFrames1080x1920,30fps. TIME:90s=2700frames. Board Di Balik Benda v6.
LOOK: ground#ECEEE9, surface#F8F9F5, ink#172B3B, muted#536775; input#C94422, inspected#2459C4, result#167580. Manrope800 titles70px/1.1 at108,205 width810; IBM Plex annotations>=30px. Captions Manrope60046px/1.3 x108/y1500 max848px2lines with18x26padding14radius. Stage80,430..1000,1410. Fit active geometry80–95% of limiting dimension. 2.5D metal/polymer side faces8–18units, consistent upper-left light; no true3D. No filters on footage; none used.
OBJECTS: jug kettle with lid, spout, handle, base; sectional water/air chamber and concealed heating element; independent steam duct; bimetal and tongue on pivot lever with fixed pillar; paired over-centre springs, slidable link, contact strip, fixed contact. The dry-boil protector is outside scope.
MOTION: deterministic analytic state from timeline time; GSAP paused once per scene. Smoothstep travel; snap is accelerated physical transition, not springy decorative easing. Exact same state for reverse seeking. Steam transport, differential curvature, lever rotation, link translation and contact opening have coupled dependencies. Intermediate contact poses and over-centre travel get separate observation windows. Flow paths update from time, not timers. Mark time compression and enlarged motion. Do not make bonded layers slide in operating shots.
SHOTS: scene-plan.json then measured timing.json;16 varied contextual, section, duct, heater, disc and contact views. s02first discovery;s11–13signature;s16matched proof. New event or sustained explanatory transfer within5s except documented result holds. Rewind and condensed replay labelled.
BANNED: dark void, decorative grids/HUD, cards replacing parts, neon/glow, random particles, orbiting cameras, isolated2Ddiagram scenes, floating contacts, steam crossing into live contacts, restart on cooling, a contact gap with current flowing, bare disc substituted for entire control, constant repeated generic click, unrelated CTA. Pale centered object framing and monospace annotations are board-required choices.
QA:16 styled pre-audio stills and complete boardPNG; actual full-film check; per-frame mechanical state constraints and reverse seeks; all scene starts/midpoints and seams at phone scale; four signature poses; actual decoded export frames,2700frames,full decode, loudness, acoustic cuts and residual SFX matching. Listening not available; do not claim it.
''')
write(V/'STORYLINES.md','# Storyline choice\n\n1. Why the kettle turns itself off: selected, familiar behavior with hidden steam/contact proof.\n2. Catalogue every kettle part: rejected; postpones discovery.\n3. Kettle malfunction diagnosis: rejected; repair/safety claims and model-specific diagnosis outside scope.\n')
story='---\nformat: 1080x1920\nduration: 90\nstyle: Di Balik Benda v6 illustrated 2.5D\n---\n\n# Visual storyboard\n\nAll operating spacing and timing illustrative; speech windows estimated until audio.\n'
for n,s in enumerate(plan):
 story+=f'\n## Frame {n+1}: {s["title"]} ({s["start"]}-{s["end"]}s)\n- act: '+('Discovery' if n<8 else 'Contact and proof')+f'\n- status: posed\n- id: {s["id"]}\n- reads: {s["title"]}\n- words: {s["text"]}\n- visual: {s["action"]}\n- framing: {s["view"]}, layered2.5D; fixed lid/handle or pillar/pivot landmark. Active bounds fitted within x80..1000/y430..1410; caption at1500 with60px clearance.\n- continuity: '+('explicit rewind from off to start' if n==2 else 'same component identity, preserve entry/exit state; s16explicit condensed replay')+f'\n- attention: initiating part→contact/transfer→response→result hold; one active cue.\n- poses: approach; contact/heat transfer; response; settled result.\n- sound: event-synchronized reused material cue or soft stylized editorial handoff; no music. Water/steam represented by soft editorial cues, not fake field sound; sustained transfer under narration can remain quiet after onset.\n- evidence: SOURCES S1–S3; qualitative residual heat inference labelled.\n'
write(V/'STORYBOARD.md',story)
for file in ['manrope.ttf','ibm-plex-mono.ttf','Manrope-OFL.txt','IBM-Plex-Mono-OFL.txt']:
 dest=V/'assets/fonts'/file;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/'boards/di-balik-benda/assets'/file,dest)
voice,provenance=resolve_voice(R)
tagged='[curious, clear conversational Indonesian] '+plan[0]['text']+'\n\n'+' '.join(s['text'] for s in plan[1:8])+'\n\n[patient, precise explanation] '+' '.join(s['text'] for s in plan[8:13])+'\n\n[calm, conclusive] '+' '.join(s['text'] for s in plan[13:])
dump(V/'audio_request.json',dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=provenance,tts_model='eleven_v4',lines=[dict(id='narration',text=tagged)]))
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'))
assert not any(x['slug']==P.name for x in tracker['productions'])
tracker['productions'].append(dict(slug=P.name,topic='Steam-actuated electric kettle shutoff: vapour duct, bonded bimetal snap actuator, over-centre lever/springs, sliding link and electrical contact separation',board='di-balik-benda',stage='storyboard',status='in_progress',path=P.relative_to(R).as_posix()))
dump(R/'TRACKER.json',tracker)
print(json.dumps(dict(shots=len(plan),seconds=t,words=sum(len(s['text'].split()) for s in plan))))
