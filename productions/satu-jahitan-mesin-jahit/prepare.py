from pathlib import Path
import json, shutil, sys

P=Path(__file__).resolve().parent; V=P/'video'; R=P.parent.parent
def write(path,text): path.write_text(text,encoding='utf-8')
scenes=[
('Satu jahitan, dua benang','Apa yang terjadi di bawah kain?','Jarumnya cuma naik turun. Tapi bagaimana dua benang bisa saling mengunci di dalam kain?',6,'whole',0,1,'A familiar machine sews a short seam, then reveals the concealed second thread.'),
('Lihat di bawah kain','Lockstitch · satu jarum','Kita lihat jahitan lurus dua benang, atau lockstitch, dengan kait yang berputar penuh.',5,'reveal',0,0,'Housing becomes transparent while the needle axis and cloth stay fixed.'),
('Dua sumber benang','Atas dari gulungan · bawah dari bobin','Benang atas melewati jarum. Benang bawah berasal dari bobin kecil di bawah kain.',6,'anatomy',0,0,'Separate thread sources along their real locations, retaining the housing landmark.'),
('Mata jarum di dekat ujung','Benang dibawa menembus kain','Perhatikan mata jarumnya: letaknya dekat ujung. Saat jarum turun, benang atas ikut menembus kain.',6,'needle',0,.24,'A macro follows the eye down through two fabric layers.'),
('Naik sedikit, muncul loop','Awal langkah naik','Sesudah mencapai titik terbawah, jarum mulai naik. Benang yang mengendur membentuk loop di sisi jarum.',6,'loop',.24,.32,'Hold a slow macro through bottom dead center, short rise, and loop opening.'),
('Kait masuk ke loop','Titik tangkap','Ujung kait datang tepat saat loop terbuka, lalu masuk dan menangkapnya.',5,'pickup',.32,.38,'Stable contact macro: hook tip approaches, crosses the opening, and retains the upper-thread loop.'),
('Loop dibawa berputar','Rumah bobin tetap pada tempatnya','Kait terus berputar, membawa loop mengelilingi rumah bobin. Rumahnya tidak ikut berputar bersama kait.',7,'wrap',.38,.57,'Pull out enough to distinguish rotating outer hook from stationary inner case.'),
('Ada lintasan di belakangnya','Dua sisi loop melewati rumah bobin','Satu sisi loop lewat di belakang rumah bobin. Sisi lainnya melewati bagian depan.',6,'rear',.57,.68,'An explanatory depth separation exposes rear and front limbs around the same case.'),
('Benang bawah ikut terlingkupi','Loop atas mengitari rumah bobin','Dengan melewati rumah bobin, loop benang atas mengelilingi benang bawah. Inilah pertemuan kedua benang.',6,'interlock',.68,.76,'Show loop cast-off and lower thread crossing within the upper loop; retain cyan thread continuity.'),
('Giliran tuas penarik','Dari memberi kelonggaran ke menarik','Di atas, tuas penarik tadi memberi kelonggaran. Kini tuas naik untuk menarik kembali benang atas.',6,'takeup',.76,.87,'Reframe upward: take-up lever lifts while the lower loop shrinks in the same causal action.'),
('Loop mengecil, kaitan naik','Benang atas menarik benang bawah','Loop mengecil. Benang atas menarik benang bawah menuju kain, sampai keduanya saling mengunci.',6,'tighten',.87,.96,'Follow the tightening red loop as it raises the cyan interlock into the cloth.'),
('Kaitan berada di dalam kain','Saat tegangan kedua benang seimbang','Pada tegangan yang seimbang, titik kaitannya berada di dalam lapisan kain.',5,'seam',.96,1,'Section macro resolves interlocking paths inside two fabric layers, without drawing a knot.'),
('Jarum bebas, kain bergeser','Penggerak kain di bawah sepatu','Setelah jarum keluar, gigi penggerak menggeser kain. Sepatu penekan menjaga kain tetap tertekan.',6,'feed',1,1,'Side section: needle is clear; dog rises, moves cloth, drops, and returns beneath the plate.'),
('Bersiap untuk tusukan berikutnya','Kain diam saat jarum masuk','Giginya turun lalu kembali di bawah pelat. Jarum turun lagi saat kain berhenti bergeser.',5,'reset',1,1.24,'Dog returns below the throat plate; next needle descent happens only after feed stops.'),
('Semua bergerak berurutan','Jarum → kait → penarik → kain','Jadi bukan jarum saja. Jarum membuat loop, kait menangkapnya, tuas mengencangkan, lalu kain bergeser.',7,'cycle',0,1,'One complete coordinated slow cycle, with attention handed among the four subassemblies.'),
('Dua benang saling mengunci','Satu siklus menjadi satu jahitan','Siklus yang teratur ini mengubah dua benang menjadi deretan jahitan.',6,'result',1,1,'Return to the recognisable whole and resolve the red/cyan seam, then hold the completed interlock.')]
plan={'duration':90,'fps':30,'scenes':[]}
total=sum(s[3] for s in scenes); t=0
for i,(title,sub,vo,dur,view,a,b,purpose) in enumerate(scenes,1):
    dur=dur*90/total
    plan['scenes'].append(dict(id=f's{i:02}',title=title,subtitle=sub,vo=vo,start=round(t,3),duration=round(dur,3),view=view,p0=a,p1=b,purpose=purpose));t+=dur
write(V/'scene-plan.json',json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
for d in ['assets/fonts','assets/audio','compositions','boards/stills','verification']:(V/d).mkdir(parents=True,exist_ok=True)
fonts=R/'productions/dua-katup-pompa-sabun/video/assets/fonts'
for f in fonts.iterdir(): shutil.copy2(f,V/'assets/fonts'/f.name)
shutil.copy2(R/'boards/di-balik-benda/frame.md',V/'frame.md')
write(V/'BRIEF.md','''---
workflow: hyperframes
type: faceless-explainer
flow: automation
storyboard: no
mode: autonomous
message: "Two threads interlock through a synchronized needle, rotary hook, take-up and feed cycle"
destination: platform-neutral vertical video
aspect: 1080x1920
language: id
length: 90s
audience: curious general Indonesian viewers
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
pre_render_authorization: delegated by the user's latest --automation instruction
until: export
---

## Intent
Continue the existing sewing-machine production with the approved Di Balik Benda v3 board, in the explicitly selected 2.5D style. Explain one single-needle type-301 lockstitch using the horizontal full-rotary-hook variant documented by JUKI. The hook's shaft is horizontal; the circular case is viewed from its face. Do not confuse it with a top-loading vertical-axis arrangement or oscillating shuttle.

## Execution
The latest user instruction replaces the former pending after-hook policy with immediate automation. Preserve the saved export-only endpoint. Research, hook and storyline selection, script, static board, audio, animation, technical/creative review, preview and local export are delegated. No publishing or content package is in scope. Human approval fields stay false.

The static storyboard is required before synthesis and animation, including boards/stills, storyboard.html and the complete storyboard.png. Agent verification replaces the human checkpoint. The refreshed CLI retired faceless-explainer into the current hyperframes skill; use that maintained film/explainer workflow instead of the retired skill's frame-worker pipeline.

## Notes
Original diagrams, not to scale; clearances, thread thickness and time are exaggerated. Expose the front shell, keep stationary case distinct from rotating outer hook, and show the loop passing in front and behind. Palette, Manrope, local fonts and annotation vocabulary inherit board v3. Speech follows the repository ElevenLabs eleven_v4 policy and root .env voice. Music and sound effects are optional under the selected board; prefer an unscored explanatory voice over false machine acoustics. Captions contain spoken words only.
''')
write(P/'SOURCES.md','''# Sources and claim boundaries

## Exact mechanism
Single-needle, two-thread lockstitch (301), using JUKI's **horizontal full-rotary hook** illustration. A horizontal shaft gives a front-facing circular hook/case in this explanatory view. This film does not depict an oscillating hook, chainstitch, or every household machine.

1. [JUKI — Basic Knowledge of Sewing, manufacturer training manual hosted by Raichert](https://raichert.com/wp-content/uploads/2021/03/Basic-Knowledge-Sewing.pdf). Saved locally under research/JUKI-Basic-Knowledge-Sewing.pdf. Printed pp. 6–7, figures II-14–20: two-thread lockstitch; initial needle rise forms loop; rotating outer hook catches loop; the limbs separate around the inner case; take-up supplies then retracts thread; upper thread lifts/interlaces lower thread. Printed pp. 22–24: hook geometry and the inner/outer distinction; pp. 33–34: take-up and synchronized movements; pp. 35–39: bottom feed and its phases; pp. 40–42: presser-foot function. Existing research/ PNGs inspected at printed pp. 6–7.
2. [Coats — Basic Stitch Types](https://www.coats.com/en/info-hub/basic-stitch-types). Manufacturer technical bulletin, fetched in RESEARCH-COATS.json. Independently supports loop formation at the scarf during initial needle rise, hook interlocking needle and bobbin threads, loop cast-off and stitch setting, and the scope of 301 single-needle lockstitch.
3. Union Special type-301 training PDF was found but its URL returned bot protection. It is a discovery lead only, not evidence used for hidden geometry.

## Claim map
| Claim | Evidence | Visual boundary |
| --- | --- | --- |
| Two thread sources; upper through the needle, lower from bobbin | JUKI p.6; Coats stitch-forming devices and 301 | Color makes identity visible; actual thread colors need not differ |
| Eye near needle tip carries upper thread through fabric | JUKI needle anatomy pp.15–17; stitch figures | Eye and scarf are enlarged |
| Loop forms during the short rise after bottom dead center | JUKI fig.II-16; Coats loop formation | Slow time, no numerical lift/timing specification |
| Hook tip enters loop; rotating outer hook carries it around stationary inner case | JUKI figs.II-16–18 and hook section | Front/rear limbs are depth-separated; no spinning inner case |
| Upper loop passes around lower-thread source, enabling interlacing | JUKI figs.II-18–20; Coats | No complete bobbin passes through cloth; no fabricated knot |
| Take-up supplies slack then tightens the loop, raising lower thread into the seam | JUKI p.7, pp.33–34 | No claim that needle alone tightens the stitch |
| Balanced tensions put the interlace inside the material | JUKI thread-tension section pp.43–49 | Conditional statement, not guaranteed for any settings |
| Bottom feed advances material after needle clears it; dog returns below plate; presser keeps material controlled | JUKI pp.35–42 and cycle chart | One bottom-feed example; no walking-foot or needle-feed claim |

## Provenance and simplification
All episode imagery is original SVG 2.5D art derived from the functional relationships, not copied source figures. The shell is removed, thickness and clearance are enlarged, and phase timing is slowed/nonlinear for teaching. Rear-side thread is dashed where hidden. The seam section is a topological explanation, not a dimensioned model. No RPM, exact angle, lift distance or tension adjustment is asserted. Existing research was reused; no unsupported factual expansion requires new search.
''')
hooks=[
('Jarumnya cuma naik turun. Tapi bagaimana dua benang bisa saling mengunci di dalam kain?','Familiar visible action leads directly to the hidden two-thread interaction; selected because its promise is answered by the entire chain.'),
('Ada benang kedua di bawah kain. Bagaimana benang ini bisa bertemu dengan benang di jarum?','Hidden-source mystery; begin below the fabric and trace toward the needle.'),
('Satu jahitan lahir dari satu loop kecil. Mari ikuti lintasannya di dalam mesin jahit.','Follow one orange thread loop through a continuous macro journey; a bolder thread-led film.')]
episode=(P/'EPISODE.md').read_text(encoding='utf-8-sig')
episode=episode.replace('- automation_after: hook','- automation_after: none').replace('- automation_state: pending','- automation_state: active').replace('- human_review: defaults through hook selection','- human_review: none').replace('- pre_render_authorization: pending activation',"- pre_render_authorization: delegated by the user's latest --automation instruction")
episode=episode.replace('- activation_evidence: none yet; accepting the topic does not select a hook', '- activation_evidence: latest user requested continuation with immediate --automation on 2026-10-24; supersedes pending after-hook policy')
episode=episode.replace('- script_status: not drafted; write only after the user selects a hook','- script_status: agent-verified v1 under delegated selection')
episode=episode.replace('- next_action: verify the mechanism, then present exactly three hooks and wait for the user\'s selection','- next_action: build and verify the required static storyboard, then audio and animation through local export')
episode+='\n## Continuation and delegated hook selection\n\nLatest scope retains until=export. Immediate --automation supersedes the prior delayed option. No human hook/script/layout/final-look approval is claimed.\n\n'
for i,(h,r) in enumerate(hooks,1):episode+=f'{i}. **{h}** {r}\n'
episode+='\nSelected: hook 1, by the agent under immediate automation. Research is complete within SOURCES.md. Sixteen explanatory shots will retain 90 seconds at 30 fps.\n'
write(P/'EPISODE.md',episode)
script='# Narration v1 — agent verified under automation\n\nLanguage: Indonesian. One continuous full-script narration request; no human approval claimed. Estimated 90-second composition; speech timing will be measured.\n\n'
for s in plan['scenes']:script+=f"## {s['id']} — {s['title']}\n\n{s['vo']}\n\nOn screen: {s['subtitle']}\n\n"
write(P/'SCRIPT.md',script);write(V/'SCRIPT.md',script)
write(V/'STORYLINES.md','''# Storyline selection

Five sketch devices considered: whole-machine cutaway tour; one thread as carrier; seam-result-first reverse chronology; a failed pickup comparison; one stitch as continuous slowed time. Failure comparison is omitted because the episode is about normal formation. Reverse chronology is weaker for a first-time spatial model.

## Selected — Under the fabric
The familiar sewing machine stitches in the first two seconds. Remove the front shell, keep the needle axis as a landmark, and tour the needle loop, rotating hook, stationary case, take-up and feed. Return to the same seam with its hidden two-thread interlace resolved. Form: causal tour with meaningful macro cuts and one continuous final cycle. Look: mineral bench, brushed steel, orange upper thread, teal lower thread. Sound: clear Indonesian voice; intentional absence of score and synthetic machine effects.

## Alternative — Follow the orange loop
A thread-led continuous dive follows the upper thread through the needle and around the case, revealing the teal lower thread only at the interlace. First two seconds: a near-tip eye carries the orange thread through cloth. Form: continuous tracking macro with context inserts. Same board materials; sparse voice with observation windows.

## Alternative — Open the finished stitch
A seam's internal crossing opens into an enlarged loop and the mechanism reconstructs around it. First two seconds: two layers of cloth separate around a clearly locked thread crossing. Form: result-first reverse reveal, then forward cycle. Same board; voice and intentional unscored holds.

Agent chose Under the fabric for the strongest recognisable opening and easiest causal/spatial continuity. Latest --automation delegates selection.
''')
write(V/'SPEC.md','''# Director specification
GOAL: Viewer can trace two threads through needle-loop formation, hook pickup, passage around the bobbin case, take-up and feed.
OUTPUT: HyperFrames 1080 x 1920, 30 fps.
TIME: 90 s x 30 = 2700 frames. Sixteen explanatory shots with 2–4 diagnostic phases at the three decisive events.
LOOK: #ECEEE9 ground, #F8F9F5 work surface, #172B3B ink, #536775 secondary. Orange #C94422 upper/input thread, blue #2459C4 active outer hook, teal #167580 lower/output thread. Steel shaded #A6B4BE with a 16–26px oblique rear face. Manrope 800 display 74px/1.10, tracking -3px; body 38px/1.3; notes 30px/1.35; captions 46px/1.38. Display origin x108,y164; action frame x70–1010,y430–1450; captions x118–962,y1510–1700. No texture or vignette. Simple contact shadow, no photographic media filters.
OBJECTS: recognisable sewing-machine arm, right column and base; needle eye near tip and right-side scarf; two fabric layers; presser foot with needle opening; tooth rows below plate; circular outer hook with a beak; stationary inner bobbin case with latch, visible bobbin thread exit; upper spool and take-up lever.
MOTION: rigid needle translation and outer-hook rotation; flexible thread paths. Mechanical motion is linear within each slowed phase, with observation holds on contact; camera reframes use power2.inOut over 18–30 frames. No decorative spring. One full cycle at the close rather than the same micro-loop across successive scenes.
SHOTS: scene-plan.json and STORYBOARD.md are the numeric shot map. Each shot names the new relationship, entrance/exit phase, framing, diagnostic poses and evidence.
BANNED: dark void, glow, particles, decorative HUD, KPI cards, generic UI, all-centred compositions, text drifting while read, spinning inner bobbin case, a floating hook tip, two threads turning into a drawn knot, feeding cloth while the needle is in it, unchanged loops across three consecutive shots.
QA: frame0 recognisable machine and stitch; s05 bottom/short rise/loop; s06 before/inside/retained pickup; s08 rear/front limbs; s11 contraction; s12 interlace inside layers; s13 feed while needle clear; s14 dog reset below plate; s15 full causal cycle; s16 resolved seam and exact 90s endpoint. Inspect phone sheet, cut strips and moving contact sequences. Audio measured, listening unavailable unless a listening tool is provided.
''')
story='''---
title: Satu jahitan mesin jahit
message: Two threads interlock in one synchronized stitch cycle
workflow: hyperframes
type: faceless-explainer
flow: automation
storyboard: no
mode: autonomous
format: portrait
width: 1080
height: 1920
fps: 30
duration: 90
music: none
captions: enabled
---

## Video direction
Di Balik Benda v3. Original 2.5D mechanical cutaway; the needle axis and stationary inner case are landmarks. Orange upper thread and teal bobbin thread remain distinct; blue highlights the rotating outer hook. Whole, section, needle macro, contact macro, depth reveal, take-up, seam section and side feed views have different explanatory jobs. Hide shell, enlarge gaps/thread thickness, and slow time explicitly. Static boards are mandatory before audio and animation under the production override; agent verification replaces the human checkpoint.
'''
for s in plan['scenes']:
    story+=f"\n## Frame {int(s['id'][1:])}: {s['title']}\n\n- id: {s['id']}\n- start: {s['start']}s\n- duration: {s['duration']}s\n- status: outline\n- purpose: {s['purpose']}\n- narration: {s['vo']}\n- on_screen: {s['subtitle']}\n- framing: {s['view']}; original 2.5D; needle axis and case latch retain orientation\n- continuity: cycle phase {s['p0']} to {s['p1']}; whole-cycle/reconstruction shots explicitly marked\n- diagnostic_poses: initial relation; approach or transfer at 40%; contact/loop geometry at 70%; resolved state before cut\n- motion: 0–0.5s orientation hold; 0.5s to duration-0.6s mechanical action; final 0.6s readable outcome. No moving title.\n- evidence: SOURCES.md, JUKI figures II-16–20 and six-elements sections; Coats loop/cast-off/stitch-setting\n"
story+='\n## Sound decisions\n\nNarration: use. BGM: none, an intentional unscored mechanical inspection under board v3. SFX: none, because bundled UI clicks/whooshes do not represent a sewing machine and no machine recording is supplied; slowed thread paths should not invent contact sounds. No sound cues are planned or silently omitted.\n'
write(V/'STORYBOARD.md',story)
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8-sig'))
row=next(x for x in tracker['productions'] if x['slug']==P.name);row.update(stage='storyboard',status='in_progress')
write(R/'TRACKER.json',json.dumps(tracker,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'scenes':len(scenes),'spoken_words':sum(len(s['vo'].split()) for s in plan['scenes']),'endpoint':'export'}))
