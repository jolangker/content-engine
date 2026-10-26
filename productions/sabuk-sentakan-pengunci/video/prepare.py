"""Freeze the selected story, evidence, design and estimated shot plan."""
from pathlib import Path
import json, hashlib, shutil
V=Path(__file__).resolve().parent; P=V.parent; R=V.parents[2]
def write(p,s): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8')
def dump(p,x): write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
rows=[
('mystery',6.8,'Pelan bisa. Disentak terkunci.','Ditarik pelan, sabuk ini memanjang. Disentak, malah mengunci. Apa yang berubah di dalamnya?','whole','Opening mystery: compare the same belt under gentle and suddenly accelerating withdrawal.'),
('reel',4.6,'Tarikan memutar gulungan','Pita itu terhubung ke gulungan. Saat ditarik, gulungannya ikut berputar.','reel','First discovery: visible ribbon travel drives the spool; no component catalogue.'),
('rewind',4.8,'Pegas menariknya kembali','Pegas di sisi gulungan menarik pita kembali saat tidak lagi ditahan.','spring','Expose the spring on the opposite end, retaining the shaft landmark.'),
('variant',5.2,'Buka sisi penguncinya','Sekarang buka sisi penguncinya. Kita lihat satu desain dengan roda inersia bergigi.','explode','Reveal the inspected patent variant; axial separation is an explanatory transformation.'),
('train',5.8,'Satu putaran diteruskan','Roda penggerak menempel pada poros gulungan. Giginya memutar roda kecil yang terhubung ke roda inersia.','train','Show driver, pinion and inertia wheel connection; clutch coupling simplified, not omitted conceptually.'),
('normal',5.2,'Saat tarikan normal','Saat tarikan normal, roda inersia ikut berputar. Pelat pembawanya tetap di tempat.','normal','Normal rotation with fixed carrier establishes the reference state.'),
('bias',4.7,'Pelat dijaga pegas','Pegas kecil menahan pelat itu, sehingga pengunci masih berjarak dari gigi gulungan.','bias','Introduce the carrier bias spring only now, at its restraining function.'),
('jerk',4.4,'Lalu, satu sentakan','Lalu, tarikan mendadak mempercepat gulungan. Tetapi roda inersia menolak perubahan putaran yang tiba-tiba.','jerk','Input acceleration precedes carrier response; not a constant-speed threshold claim.'),
('resist',5.6,'Inersia menahan perubahan','Hambatan inilah pemicunya. Dorongan antargigi kini bisa mengalahkan tarikan pegas penahan pelat.','resist','Show opposing bias and gear force; no invented numeric threshold.'),
('climb',7.3,'Poros kecil ikut berpindah','Roda kecil tidak cuma berputar. Porosnya bergerak mengitari roda penggerak, sambil membawa pelat.','climb','Signature interaction: pinion climbs around driver, carrier rotates; enlarged and slowed.'),
('arm',4.9,'Pelat membawa lengan','Pelat yang bergeser membawa lengan. Ujung lengan itu mendorong bagian belakang pengunci.','arm','Continue carrier state and show the bifurcated arm contacting the pawl projection.'),
('engage',6.5,'Pengunci masuk ke gigi','Pengunci berayun masuk ke roda bergigi yang menyatu dengan gulungan. Perhatikan titik pertemuannya.','engage','Secondary diagnostic macro: gap, approach, seating, load. Reel stops at contact.'),
('stop',4.8,'Gulungan berhenti melepas pita','Begitu giginya tertahan, gulungan berhenti melepas pita. Tarikan kini diteruskan ke rangka lewat pengunci.','stop','Follow load from belt through spool ratchet to frame-mounted pawl.'),
('roles',5.3,'Sensor memicu. Pengunci menahan.','Jadi, roda inersia memicu gerakan. Pengunci dan roda bergigilah yang menahan gulungan.','roles','Functional contrast on the physical assembly, not abstract cards.'),
('compare',7.1,'Tarikan sama, respons berbeda','Bandingkan lagi. Tarikan halus memutar roda. Sentakan menggerakkan pelat, lalu pengunci masuk.','compare','Matched opening proof, same silhouette; purposeful replay in section.'),
('answer',7.0,'Perubahan gerak memicu kunci','Di desain ini, perubahan gerak pita memicu penguncian. Sensor gerak kendaraan memakai jalur lain.','answer','Return to recognizable belt and locked internal cause; explicitly scope out vehicle sensing.')]
plan=[];t=0
assert abs(sum(r[1] for r in rows)-90)<1e-6
for n,(name,d,title,text,view,purpose) in enumerate(rows,1):
    plan.append(dict(id=f's{n:02}-{name}',start=round(t,6),end=round(t+d,6),duration=d,title=title,text=text,view=view,purpose=purpose));t+=d
dump(V/'scene-plan.json',plan)
target=dict(source='board',board_accounts_file='boards/di-balik-benda/ACCOUNTS.json',board_accounts_sha256=hashlib.sha256((R/'boards/di-balik-benda/ACCOUNTS.json').read_bytes()).hexdigest(),accounts=json.loads((R/'boards/di-balik-benda/ACCOUNTS.json').read_text())['accounts'])
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:
    f.write('''
## Topic selection and narrative

Ten candidates presented in conversation: seatbelt retractor, tape measure, socket ratchet, soap pump, wheel lighter, automatic umbrella, cassette take-up, oscillating fan, correction tape, mechanical bicycle bell. Seatbelt selected because recognition and the slow-pull/jerk mystery are strong, with sourceable coupled gear, inertia, carrier, lever and ratchet motion. The narrow mechanism has a visible proof rather than a part-count advantage. Alternatives remain research leads. No claim of trending status or predicted retention.

## Hook selection, before script drafting

1. “Ditarik pelan, sabuk ini memanjang. Disentak, malah mengunci. Apa yang berubah di dalamnya?” Familiar-behavior comparison; promises the internal cause.
2. “Roda kecil ini bisa memicu pengunci sabuk. Bagaimana geraknya sampai menahan gulungan?” Component-to-load-path explanation.
3. “Tarikan sabuk itu sendiri ikut menggerakkan penguncinya. Kok bisa?” Input-as-actuator surprise.

Recommended and selected: 1, by the agent under explicit delegated automation. Options presented before drafting SCRIPT.md. Human approval is false/unset.

Central question: why gentle withdrawal is allowed while suddenly accelerating withdrawal triggers the inspected design. Chain: what moves with the ribbon → what normally stays still → what inertia changes → how the carrier moves → what actually holds the reel. First discovery planned at 8–11 seconds; measured speech timing supersedes the estimate. Signature event: s10 pinion-center orbit and carrier rotation. Contact proof: s12 pawl seating. Opening/ending pair: s01 with s15–s16.

## Publishing targets

```json
'''+json.dumps(target,ensure_ascii=False,indent=2)+'''
```

Preflight: workspace 01a171dd-5281-730d-af07-f2168d17add7, Admin's Workspace; requires_approval=false, publishes_directly=true. Account 01a172c9-3761-700a-9798-00febaa9fa90, instagram dibalikbenda.id, connected. instagram_reel: max 900s / 314572800 bytes; caption 2200 characters / five hashtags. Queue daily 10:00 Asia/Jakarta. Actual queue slot will be observed at creation.

## Research verification

Primary source body and original figures 1–3 read/inspected, and a separate technical patent body cross-checked. SOURCES.md maps every causal relationship. Source illustrations are reference evidence only, not copied film assets. No product fit, repair procedure, crash-performance or trigger-threshold claims. Context7 tools are absent from the loaded tool catalog; installed HyperFrames 0.8.206 CLI documentation/help and project-local contracts are the technical fallback. Jina search/read used for subject research. SeatBeltsPlus was a bot-check page and is excluded from evidence.

## Script verification

Script v1 agent-verified for the exact patent variant, native Indonesian delivery, and a 90-second 16-shot plan. Strongest observation time reserved for carrier orbit and pawl engagement. Original schematic geometry, enlarged clearance, removed shell and slowed motion will be labelled; no measured dimensions or tooth ratio asserted.
''')
brief=(P/'EPISODE.md').read_text(encoding='utf-8');write(V/'BRIEF.md',brief)
script='# Locked script v1\n\nIndonesian narration, agent-verified under delegated automation. Timing below is estimated until native audio alignment is measured. All claims map to SOURCES.md C1–C7.\n\n'
for s in plan:script+=f"## {s['id']} · {s['start']:g}–{s['end']:g}s\n\nNarration: {s['text']}\n\nOn screen: {s['title']}\n\nVisual: {s['purpose']}\n\n"
write(P/'SCRIPT.md',script);write(V/'SCRIPT.md',script)
write(P/'SOURCES.md','''# Evidence ledger

Research date: 2026-10-27. Jina discovery followed by source-body reads. Original patent drawing sheet inspected visually. Facts below are paraphrased, not quotations. The film is an original explanatory schematic of one described implementation, not a claim about every vehicle.

## Sources and scope

A. [US3918658A — Seat belt retractor having inertial device activated by two stimuli](https://patents.google.com/patent/US3918658A/en). Primary source: abstract, summary, preferred embodiment, figures 1–3, claims. Selected pathway: accelerated webbing withdrawal → inertia-wheel resistance → driven pinion climbs around shaft gear → movable plate rotates → arm rocks pawl into reel ratchet. Original figure inspected in research/patent-figure.png. Parts: shaft 3 / webbing 4; driver 9; movable plate 8; pinion 14 / spindle 13; inertia wheel 19 coupled by clutch 17/22; arm 26 / pawl projection 31; pawl 27; ratchet 32; bias spring 33. Pendulum 52/54/55 and lever 56 are the separate vehicle-sensitive input, expressly outside this film's mechanical cycle.

B. [US5485971A — Seat belt retractor](https://patents.google.com/patent/US5485971A/en). Independent primary technical corroboration of spring-biased rewind, webbing/reel coupling, vehicle and webbing sensing as distinct inputs, and a frame-supported pawl stopping a shaft-fixed ratchet. Its lock plate guide-slot geometry is different and is not merged into A.

C. [US3819126A — Seat belt retractor with gear wheel actuated locking means](https://patents.google.com/patent/US3819126A/en). Body read as a variant cross-check. Supports conventional spiral rewind spring and ratchet/reel/pawl function; different clutch/stop architecture. No C-specific stop or threshold is transferred to the selected A illustration.

SeatBeltsPlus returned a security-verification page; excluded. Social-media snippets were discovery noise, not evidence or creative references. No downloaded PDF was used for text extraction.

## Claim and geometry map

| ID | Script/visual statement | Support and qualifications |
| --- | --- | --- |
| C1 | Ribbon withdrawal rotates its reel; reel is biased to rewind | A background/summary and shaft 3/webbing 4; B spiral spring 6; C spiral spring 20. Spring inset is conventional functional illustration, not A-specific spring dimensions. |
| C2 | Driver fixed to shaft drives pinion, coupled to inertia wheel | A 9/14/13/19 and clutch 17/22. Show pinion and wheel on one spindle with a coupling seam. Do not show an inertia wheel freely disconnected from its pinion or replace it with a centrifugal weight. |
| C3 | Ordinary withdrawal rotates wheel while carrier remains restrained and pawl clear | A summary and spring 33/plate 8/pawl 27. No universal speed or acceleration threshold. |
| C4 | Sudden accelerating withdrawal produces inertia resistance sufficient to overcome carrier bias | A summary: resistance to sudden accelerating rotation exceeds spring bias. Explain acceleration/change of motion, not fast constant speed alone. |
| C5 | Pinion climbs/orbits around driver, moving carrier; arm acts on pawl extension | A summary, 8/9/14/26/31 and figures 1–3. Carrier rotation about reel shaft and gear-mesh center distance preserved. Driver/pinion tooth count is illustrative; kinematic external-mesh relation is enforced. |
| C6 | Pawl engages shaft-fixed ratchet, preventing pay-out; frame reacts load | A 27/29/31/32 and abstract; B confirms pawl supported on frame and shaft-fixed ratchet. Pawl tip seats against a tooth face; the reel and its driver stop together. Inertia wheel is the trigger, not the crash-load holding part. |
| C7 | Vehicle-sensitive sensing can use another pathway | A pendulum/lever inhibition of inertia wheel. Only stated as a distinction; no crash simulation, pretensioner or load-limiter explanation. |

## Simplifications and media provenance

Original layered 2.5D illustrations; material gradients, shaded side faces and overlap. Axial layers separated to expose the shaft gear; spatial gaps, tooth size, carrier angle and timing enlarged. Film labels identify cutaway, enlarged/slowed signature event and illustrative spacing. The combined side inspection is an explicitly separated axial-layer view: ratchet sits behind driver, inertia wheel outside pinion; it does not imply coplanar intersecting parts. The pendulum pathway is omitted from the selected input explanation and acknowledged in the ending. Ratios, trigger angles and motion durations are illustrative and not engineering specifications. All sources support explanation only, not inspection/repair advice.

Board fonts and licenses are copied locally. SFX selection starts with the media-use manifest; physical-material gaps may reuse frozen production assets with source provenance. Any such cue is an illustrative sound, not a recording of this patent design. No generated SFX are requested or authorized by a mere asset gap. Music intentionally absent.
''')
write(V/'STORYLINES.md','''# Storyline choice

Five sketches: familiar slow/jerk contrast with causal inspection; gear-to-load chain via axial reveals; one continuous sectional tour; two synchronized specimens; reverse inquiry starting from the seated pawl. Selected three alternatives below.

1. Selected: One belt, two responses. A seat-side belt silhouette opens on slow withdrawal then a short stop. A linked series of original 2.5D cutaways carries the same shaft/blue wheel landmark into the enlarged carrier and pawl events, then returns to the initial belt. First 2s: already-visible ribbon and reel, gentle ribbon travel under “Pelan bisa”. Beats: contrast → reel → return spring → sensor side → normal bias → accelerating pull → carrier orbit → pawl → load → matched proof. Mineral bench, Manrope, shaded metal/polymer. Narration foreground, sparse synchronized material cues, no BGM.
2. Not built: Follow the pull. A continuous sectional tour follows an orange force cue from belt to tooth and into the fixed support; the question is who carries force. First 2s: belt pulling against an already seated pawl. Cause-first sound and return-to-context reveal, same board medium.
3. Not built, bold: Two identical specimens. Gentle and sudden pulls alternate in a vertically stacked comparison that collapses into one macro at the carrier. First 2s: simultaneously visible free and locked reels. More analytical and dense on a phone; selected story has clearer progressive component introduction.
''')
write(V/'SPEC.md','''GOAL: The viewer explains that accelerating webbing withdrawal triggers this inertia-wheel/gear/carrier pathway, while a pawl and reel ratchet actually hold the reel.
OUTPUT: HyperFrames, 1080x1920, 30fps, 90 seconds = 2700 frames.
LOOK: Di Balik Benda v5. Canvas #ECEEE9, surface #F8F9F5, ink #172B3B, muted #536775; orange input #C94422, blue inspected component #2459C4, teal output #167580. Manrope 800 titles 70–76px, tracking -3px; labels Manrope 36px; caption Manrope 600 44px; annotations IBM Plex Mono 28px. Local fonts. 2.5D illustrated metal and polymer only: 8–18px shaded side thickness, upper-left light, metal gradients, physical occlusion, restrained 2.5D reframing. No true 3D or flat standalone infographic scenes.
SAFE: essential copy x108–903, y200–1320; mechanism x85–925, y415–1080; caption y1190, max two lines. Nothing essential below 1330 or under right action rail.
OBJECTS: recognizable woven dark belt, tongue and seat-side reel shell; U-frame and shaft; layered ratchet/driver, carrier plate and fixed support; small meshing pinion and coaxial inertia wheel/coupling; bias spring, arm and pivoted pawl. Original geometry, source A topology and axis relationships. 24:12 illustrative external gears, center distance 168 units, orbital formula pinion angle = 3*carrierAngle - 2*driverAngle. All coupled movements preserve mesh. Reel ratchet stops at pawl seating.
MOTION: deterministic state function driven by paused scene GSAP timeline; no random/timers. Physical gear rotation linear except accelerating input; carrier displacement over 45–70 frames; observation holds 12–30 frames; stabilized contact macros. A hard cut or matching landmark connects views; no generic transition effect.
SHOTS: scene-plan.json is the 16-shot source, STORYBOARD.md expands questions, first uses, state, attention, source and sound. Estimated first discovery 8–11s. Longest critical observation: s10 orbit and s12 pawl contact. s01 opening matches s15/16 proof.
SOUND: single continuous tagged ElevenLabs eleven_v4 narration with root-env voice. Measured native alignment governs final scene boundaries. Existing media-use editorial click and licensed frozen material sounds, event onset rounded to nearest 30fps frame. No music, no new SFX generation. No unverified listening claim.
BANNED: default dark void; floating tiny mechanism; logo/chapter cards; decorative HUD; arbitrary exploded inventory; identical loop repeated under changed text; full-screen flat diagrams; centrifugal weight substituted for inertia wheel; gears rotating after pawl seating; title motion while reading; glow/particles; fake dimensions, thresholds or performance claims; one generic click for all actions; borders or small corner brand.
QA: every shot midpoint and phone sheet; frame0; seam strips; four carrier poses; four pawl poses; mesh equation and fixed center distance; no ratchet rotation after seating; caption alignment and clearance; full decode, exact 90s, loudness and actual SFX presence. Listening may be unavailable; record it.
''')
shutil.copy2(R/'boards/di-balik-benda/frame.md',V/'frame.md')
for name in ['manrope.ttf','ibm-plex-mono.ttf','Manrope-OFL.txt','IBM-Plex-Mono-OFL.txt']:
    src=R/'boards/di-balik-benda/assets'/name
    if not src.exists():src=R/'boards/di-balik-benda/assets/fonts'/name
    dst=V/'assets/fonts'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));assert not any(x['slug']==P.name for x in tracker['productions'])
tracker['productions'].append(dict(slug=P.name,topic='US3918658A webbing-sensitive seatbelt retractor: reel, inertia wheel, meshing pinion, movable carrier, arm and pawl/ratchet locking',board='di-balik-benda',stage='script',status='complete',path='productions/'+P.name));dump(R/'TRACKER.json',tracker)
print(json.dumps(dict(scenes=len(plan),seconds=t,words=sum(len(s['text'].split()) for s in plan))))
