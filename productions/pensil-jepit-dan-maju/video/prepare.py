"""Freeze this episode's delegated decisions and pre-audio scene plan."""
from pathlib import Path
import hashlib,json,shutil,sys
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'))
from narration import resolve_voice
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def dump(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
rows=[
('mystery',6,'Maju, kok tidak mundur?','Sekali klik, isi pensil maju. Kenapa saat tombol kembali, isinya tidak ikut mundur?','whole',0,1),
('grip',5,'Yang membawa isi: penjepit','Pada mekanisme tekan ini, isi dibawa oleh penjepit kecil di dekat ujung pensil.','section',0,.12),
('ring',5,'Cincin membuatnya menggenggam','Kepala penjepit bercelah dan melebar. Cincin di luarnya merapatkan rahang, sehingga isi tergenggam.','jaw',0,.1),
('input',6,'Tombol mendorong rangkaian','Saat tombol ditekan, tabung isi dan penjepit bergerak ke depan. Pegas di dalam ikut tertekan.','spring',0,.26),
('carry',6,'Isi ikut maju','Selama masih menjepit, rahang, cincin, dan isi bergerak bersama. Isi melewati penahan ringan di ujung.','section',.26,.55),
('stop',6,'Cincin sampai ke pembatas','Lalu cincin menyentuh pembatas di rumah mekanisme. Cincin berhenti, tetapi penjepit masih bisa maju sedikit.','stop',.55,.65),
('release',7,'Maju lagi, rahang terbuka','Perhatikan celah ini. Kepala penjepit keluar dari cincin, rahangnya membuka, dan genggamannya pada isi terlepas.','jaw',.65,.78),
('retainer',5,'Siapa yang menahan isi?','Isi tidak langsung meluncur bebas. Penahan di dekat ujung memegangnya dengan gesekan ringan.','retainer',.78,.8),
('springback',6,'Pegas mengembalikan rangkaian','Ketika tombol dilepas, pegas mengembalikan tabung dan penjepit. Isi tetap di posisi yang sudah maju.','spring',.8,.9),
('slideback',5,'Penjepit kembali, isi tinggal','Selagi rahang belum menggenggam lagi, penjepit bergeser kembali melewati isi yang ditahan di ujung.','return',.9,.96),
('regrip',6,'Cincin merapatkan rahang lagi','Saat kepala penjepit masuk kembali ke cincin, rahangnya merapat dan menggenggam isi lagi.','jaw',.96,1),
('ready',5,'Siap untuk menulis','Sekarang isi tertahan oleh penjepit utama. Penahan ringan di ujung tadi membantu selama perpindahan genggaman.','section',1,1),
('step',5,'Satu siklus, satu langkah','Jadi, gerak maju dan gerak kembali tidak membawa isi dengan cara yang sama.','compare',0,1),
('repeat',5,'Klik berikutnya mengulang proses','Klik berikutnya mengulangi urutan itu: jepit, bawa maju, lepas, lalu jepit kembali.','section',0,1),
('scope',5,'Gerak kecil, dibuat terlihat','Ini contoh mekanisme rahang dan cincin. Jarak geraknya diperbesar agar perpindahan genggaman terlihat jelas.','jaw',0,1),
('answer',7,'Kembali tanpa menarik isi','Tombolnya kembali, tetapi isi sudah berpindah pegangan. Itulah sebabnya setiap klik meninggalkan sedikit isi di luar.','proof',0,1),
]
plan=[];t=0
for n,(key,d,title,text,view,a,b) in enumerate(rows,1):
 plan.append(dict(id=f's{n:02}-{key}',key=key,start=t,end=t+d,duration=d,title=title,text=text,view=view,phase_start=a,phase_end=b));t+=d
assert t==90
dump(V/'scene-plan.json',plan)
accounts=R/'boards/di-balik-benda/ACCOUNTS.json'
targets=dict(source='board',board_accounts_file=accounts.relative_to(R).as_posix(),board_accounts_sha256=hashlib.sha256(accounts.read_bytes()).hexdigest(),accounts=json.loads(accounts.read_text())['accounts'])
brief='''# Mechanical pencil: grip transfer leaves the lead advanced

board: di-balik-benda
board_revision: 6
topic_selection: auto
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
human_approved: false
pre_render_authorization: delegated by the user's --automation instruction
requested_endpoint: publishing
delivery: queue
schedule: next configured slot; no displacement
commit: after pipeline completion

## Brief and inherited direction
One Indonesian 90-second, 1080x1920, 30fps, 16-shot explanation for curious general audiences. Explain the partial-press lead-feed subsystem in the working state documented in US4106874A, corroborated by EP0168122A1's chuck/ring construction and US4205924A's sliding ring/shoulder and friction-holder sequence. Do not depict the patents' additional retractable nose, shake weight, extra cushioning springs or assembly inventions. One illustrative split chuck; no universal claim about every mechanical pencil. No dimensions or speed presented as product measurements.

Inherit [editorial](../../../boards/di-balik-benda/EDITORIAL.md), [frame](../../../boards/di-balik-benda/frame.md), and [shot direction](../../../boards/di-balik-benda/SHOT-DIRECTION.md) v6. Pale inspection bench #ECEEE9, ink #172B3B; orange applied input, blue inspected ring/jaws, teal advanced lead/retainer emphasis. All objects use layered 2.5D illustrated thickness, sectional walls, material gradients and fixed light from upper left. Local Manrope/IBM Plex Mono. Large centered active subassembly in x80..1000/y430..1410; relevant silhouette and complete travel fit. Captions inherit Manrope600 46px/1.3 at x108/y1500/width848, pale fitted blocks, <=2 lines and >=60px object clearance. Board's explicit lower-caption preference governs over generic vertical defaults; check right rail and retain SRT/VTT.

Narration: one tagged ElevenLabs eleven_v4 request, root .env voice via maintained narration.py. BGM intentionally absent: dry mechanism cues and speech carry the inspection. SFX use existing bundled editorial cues plus frozen material Foley when bundled electronic clicks do not fit metal/axial travel. No new SFX generation. Physical cues are stylized explanations, not recordings of this pencil. Keep complete synthesis, alignment, acoustic splices and sound/export receipts. Listening limitations must be stated honestly.

## Delegated topic decision and overlap
Ten candidates were visibly presented before selection: mechanical pencil, tape measure, correction tape, can opener, adjustable wrench, automatic umbrella, ratchet screwdriver, piezo lighter, utility knife, hydraulic door closer. Pencil selected under --topic=auto, not human approval. Recognition strong (ordinary writing tool); curiosity strong (forward lead despite returning button); visual proof strong (ring stop and transfer to tip retainer). Causal richness: button/tube, spring, ring stop, jaw opening, friction retention, regrip. Discovery by 6-11s; mixed axial, sectional and tip detail views; verified primary evidence. Scope fits 16 shots. Tape reel overlaps the seatbelt's winding imagery; ratchet overlaps freehub; correction tape needs more clutch qualification; opener/closer need wider mechanism budgets. No trends or retention predictions claimed.

Checked every tracker topic and production folder, including unregistered roda-beda-putaran. Distinct from lock, sprayer, cistern, stapler, freehub, fan, music box, seatbelt and lockstitch. Board historical pen/zipper/clothespin examples are overlap references, not extant new targets. This request creates one episode.

## Hook checkpoint, resolved before script
1. “Sekali klik, isi pensil maju. Kenapa saat tombol kembali, isinya tidak ikut mundur?” Observable forward/return mystery; promises grip-transfer proof.
2. “Di dalam pensil ini, ada penjepit yang bergantian menggenggam dan melepas.” Hidden-component approach; promises jaw/ring explanation.
3. “Tombolnya cuma bergerak sebentar. Bagaimana isi pensil bisa keluar sedikit demi sedikit?” Incremental feed approach; promises the cycle.
Recommended and selected 1 under delegated automation. Options presented in conversation after primary research. No human hook or script approval fabricated.

## Story contract
Central mystery: why the lead stays advanced when the button returns. Opening shows one external click; first discovery at 6-11s reveals a near-tip chuck carrying the lead. Questions link: what grips -> what squeezes the jaws -> how input moves them -> why the ring stops -> why jaws release -> who holds lead during return -> how grip is restored. Signature 28-47s: ring shoulder contact, chuck overtravel and jaw opening, shown as four diagnostic states, then the distinct tip retainer. Ending matches opening's pencil silhouette, axial input and length landmark, now showing the transfer within a cutaway. Main lead never retreats during free chuck return. Ring and jaw travel are explicitly schematic and enlarged; do not confuse the lightly frictional tip retainer with the writing-load chuck.

## Publishing targets
'''
brief+='```json\n'+json.dumps(targets,indent=2)+'\n```\n'
brief+='''
Live preflight: Admin's Workspace /01a171dd-5281-730d-af07-f2168d17add7, me.requires_approval false and publishes_directly true; inherited Instagram @dibalikbenda.id /01a172c9-3761-700a-9798-00febaa9fa90 connected. Content type instagram_reel, <=900s and314572800bytes; caption<=2200 characters/5 hashtags. Queue daily10:00 Asia/Jakarta; actual next slot is resolved by Trypost at scheduling, not guessed. User authorizes direct upload and queue next.

## Execution and preservation
HyperFrames0.8.216 freshly initialized in empty video/. Context7 tools unavailable in session; installed project-local skills, pinned CLI docs and help are execution fallback. Usage at start: session96%, weekly62% remaining. No skill updates. Existing initial changes in TRACKER (gali-jadi/tong-hujan) and their folders are unrelated and excluded from this commit; preserve their working bytes.

## Stage record
Brief, primary research and script agent-verified under automation. Next: complete and inspect static storyboard before narration synthesis and animated assembly. No preview server started.
'''
write(P/'EPISODE.md',brief);write(V/'BRIEF.md',brief)
write(P/'SOURCES.md','''# Evidence and claim map

Primary source bodies read with Jina MCP on2026-10-30. Search snippets were used only for discovery. Original diagrams are new illustrations; no patent image is copied into the film.

A. [US4106874A — Mechanical pencil](https://patents.google.com/patent/US4106874A/en). Detailed-description passage on slight/partial push-cap depression while already in writing position: lead case and chuck/sleeve advance, sleeve meets shoulder5a, chuck releases; on release lead remains advanced while chuck and sleeve retract and grip a new position. Claim5 identifies a resilient friction bushing. Episode isolates that feed subsystem; its extra full-press nose-retraction cam, movable tip sleeve and multiple springs are outside scope. Keep the illustrated outer nose stationary during this selected feed cycle.

B. [EP0168122A1 — Mechanical pencil and method of assembling the same](https://data.epo.org/publication-server/rest/v1.1/patents/EP0168122NWA1/document.html). Lead pipe3, split chuck5, axially slidable clamp ring6 and sleeve7; confirms ring clamps the chuck. Its special assembly stopper and cushioning implementation are not depicted as part of our simplified cycle.

C. [US4205924A — Mechanical pencil with lead-feeding device](https://patents.google.com/patent/US4205924A/en). Detailed operation: chuck15/ring14 carry lead against light holder4 friction; ring stops at shoulder2E; chuck overtravels, expands and releases lead; front spring13 returns the mechanism and the wedge/ring regrips. Both shake and button operation are described. This film does not add its shake weight or claim an exact geometry copy. C corroborates the sliding-ring physics; A supplies the manually pressed scope.

| Spoken/visual claim | Evidence | Boundary |
| --- | --- | --- |
| A click can advance lead without withdrawing it on release | A partial-press operation | Selected jaw/ring feed type; not all pencils |
| Split jaws are squeezed by an outer ring | B chuck5/ring6; C wedge15B/ring14 | Two visible jaws are a sectional view, not a claim of universal jaw count |
| Button/tube/chuck move axially, loading a return spring | A cap2/case8/S2 | Omit full-press/retract mechanisms |
| Lead, ring and gripping chuck initially travel together | A sleeve6/chuck7; C ring14 operation | Exaggerated schematic travel, no mm claims |
| Ring reaches housing shoulder, chuck moves beyond and opens | A shoulder5a; C shoulder2E | Signature shown with separated timing for observation |
| Tip retainer applies light friction and holds lead during open return | A claim5 plus partial-press sequence; C holder4 | Retainer is not the primary writing-load lock |
| Spring return and ring reseating restore the grip | A S2 return/regrip; C front spring13 | Ring returns with loose chuck before final rearward seating; lead remains advanced |
| Repeated clicks create stepwise projection | A repeated pumping passage | Increment size illustrative |

Rejected engineering basis: US2528328A uses a different point-clutch/guide-tube topology; inspected but not combined with this mechanism. These patents document embodiments, not the prevalence of any commercial model. Stylization: removed front half-shell, enlarged clearances/travel, slowed cycle, thickness and material shading. Lead is visually thickened for phone legibility; no scale or friction coefficient claimed. Colored force arrows and lead fiducials are editorial guides.

## Candidate leads
Correction tape US8746316B2; meter lock US4927092A; can opener US7437825B2; adjustable wrench US5644957A; umbrella US6170497B1; ratchet US8109181B2; piezo US6856074B2; cutter US6513246B2; hydraulic closer EP0469697A1. Candidate leads are discovery context, not verified claims imported into this script.
''')
script='# Script v1 — selected hook1\n\nAgent-verified under delegated automation; timing below is estimated until measured.\n\n'
script+='\n'.join(f'## {n:02} — {s["title"]} ({s["start"]}-{s["end"]}s)\n\nNarration: {s["text"]}\n\nOn-screen: {s["title"]}\n' for n,s in enumerate(plan,1))
script+='\nNo CTA. Narration captions contain the spoken words; short headings add inspection context.\n'
write(P/'SCRIPT.md',script);write(V/'SCRIPT.md',script)
story='---\nformat: 1080x1920\nduration: 90s\nmessage: Grip transfer leaves lead advanced while the button returns\narc: Mystery -> grip -> stop -> release -> retention -> regrip -> proof\naudience: Curious Indonesian-speaking general audiences\nmode: autonomous\n---\n\n# Static storyboard before audio/animation\n\n'
for n,s in enumerate(plan,1):
 story+=f'## Frame {n} — {s["title"]} ({s["start"]}-{s["end"]}s)\n\n- act: '+('Mystery' if n<3 else 'Inspection' if n<13 else 'Proof')+f'\n- status: built\n- src: compositions/{s["id"]}.html\n- duration: {s["duration"]}s\n- poster: {s["start"]+s["duration"]*.65}\n- scene: {s["view"]} 2.5D sectional illustration\n- voiceover: {s["text"]}\n- reads: Heading holds entire shot; active component then contact/response; spoken captions after measured audio\n- sound: Material contact/travel at physical event; softer editorial cutaway cue; no music\n- phase: {s["phase_start"]} to {s["phase_end"]} of enlarged feed cycle\n\nOne causal question: {s["title"]}. Fixed landmark: dark lead axis and nose. Front is down; no rotation swaps the direction. Orange input acts before blue contact and teal retained output. Camera is settled before decisive contact. Housing remains fixed. Poses show approach, shoulder contact, open jaws and retained lead; return ends in regrip. Cutaway has shaded wall thickness and consistent upper-left lighting. Full motion remains inside stage and above captions.\n\n'
story+='## Intelligibility and silence\n\nNo BGM by design. Observation holds retain quiet after short Foley tails. Sustained axial moves use a restrained dry friction cue, not a transient on every frame. Tip friction and radial release use quiet representative material cues; not claimed literally audible. Final event cue sheet is generated from actual frame-clock motion after measured narration.\n'
write(V/'STORYBOARD.md',story)
write(V/'SPEC.md','''# Quantified visual and motion specification

1080x1920,30fps,2700frames,90s. Boardv6. Background#ECEEE9, ink#172B3B, orange#C94422, blue#2459C4, teal#167580. Manrope800 headings70px/1.1 x108/y205 max800wide; fixed after entrance. Captions Manrope60046px/1.3 x108/y1500 width848 max2lines, padding18x26 radius14. Annotations>=30px output. Mechanism stage x80..1000/y430..1410, active silhouette80–95% of fitted dimension, visible sweep included. Vector extrusions10–18px, dark side faces and soft contact shadows; no flat diagram-only shot.

Fixed axis front=down. Illustrative chuck forward44units, ring travel24units; remaining20units open jaws. Ring shoulder stays at front-limit position; ring returns loosely with chuck before rearward reseating. Lead displacement24units each cycle, never returns with open jaws. Tip retainer stays fixed; grip transfer is not a second synchronized moving clamp. Native recording preserved, silence inserted at measured quiet boundaries, exactly2700outputframes. Mechanical moves smooth cubic; decisive contacts settle without elastic overshoot; no unseeded randomness. One paused timeline per scene; analytic renderAt(time), reversible seeking. Camera per view is a purposeful fixed section/macro/reframe, no decorative orbit. Slowed/enlarged explanatory timing marked.

SHOTS: scene-plan.json owns the16estimated windows; timing.json supersedes measured frame ranges. s01 external click; s02 carrying chuck; s03 clamp ring; s04 spring/input; s05 coupled forward travel; s06 ring/shoulder stop; s07 signature release; s08 friction retainer; s09 spring return; s10 loose chuck return; s11 regrip; s12 two holding roles; s13 forward-versus-return fiducial; s14 next cycle; s15 exaggerated scale qualification; s16 matched opening cutaway proof. Meaningful observation pauses, not repeated unchanged loops.

BANNED: dark void, neon/glow, decorative grids/HUD, cards replacing mechanism, numbered corner labels, logo, unrelated CTA, floating contacts, rigid jaw translation that breaks the chuck stem, lead retreat during released return, ring passing its stop, decorative camera drift, three consecutive identical framing/operation shots. Centered large objects and pale mono labels are explicit board choices. Do not add serif typography or pill UI.

QA: all16stills; four signature poses; fixed ring-stop geometry; axial/radial coupling; every integer30fps seek; nonsequential seeking; all scene starts/mids, cut strips and phone sheet; captions<=2lines/no overlap; full MP4 decode and duration, acoustic seams, SFX residual matching and loudness. Sound measured, subjective listening unavailable unless an audio playback tool becomes available.
''')
write(V/'STORYLINES.md','''# Storyline choice
1. Why lead stays advanced when the button comes back: selected, direct observable mystery and grip-transfer proof.
2. Tour the components: rejected as an opening inventory before a discovery.
3. Lead slipping as a repair diagnosis: rejected; would need model-specific failure evidence and a different purpose.
''')
for src,dst in [('manrope.ttf','manrope.ttf'),('ibm-plex-mono.ttf','ibm-plex-mono.ttf')]:
 write(V/'assets/fonts/.keep','')
 shutil.copy2(R/'boards/di-balik-benda/assets'/src,V/'assets/fonts'/dst)
for f in (R/'boards/di-balik-benda/assets').glob('*OFL.txt'):shutil.copy2(f,V/'assets/fonts'/f.name)
write(V/'frame.md',(R/'boards/di-balik-benda/frame.md').read_text(encoding='utf-8'))
voice,provenance=resolve_voice(R)
tagged='[curious, clear conversational Indonesian] '+plan[0]['text']+'\n\n'+' '.join(s['text'] for s in plan[1:6])+'\n\n[focused, patient explanation] '+' '.join(s['text'] for s in plan[6:12])+'\n\n[warm, conclusive] '+' '.join(s['text'] for s in plan[12:])
dump(V/'audio_request.json',dict(provider='elevenlabs',lang='id',voice=voice,voice_resolution=provenance,tts_model='eleven_v4',lines=[dict(id='narration',text=tagged)]))
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'))
assert not any(x['slug']==P.name for x in tracker['productions'])
tracker['productions'].append(dict(slug=P.name,topic='Button-operated mechanical pencil feed: split chuck, sliding clamp ring and shoulder, spring return, tip friction retention and regrip',board='di-balik-benda',stage='storyboard',status='in_progress',path=P.relative_to(R).as_posix()))
dump(R/'TRACKER.json',tracker)
print(json.dumps(dict(shots=len(plan),seconds=t,words=sum(len(s['text'].split()) for s in plan))))
