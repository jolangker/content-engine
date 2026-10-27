"""Freeze this episode's decisions, claims and pre-audio shot plan."""
from pathlib import Path
import json, shutil
V=Path(__file__).resolve().parent; P=V.parent; R=V.parents[2]
def write(p,s): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8')
def dump(p,x): write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
rows=[
('mystery',5,'Pedal berhenti. Roda tetap jalan.','Pedalnya berhenti. Kenapa rodanya masih berputar?','bike','Opening proof: stationary crank, moving rear wheel.'),
('independent',5,'Dua bagian, bisa beda putaran','Di roda belakang, penggerak dari rantai dan rumah roda bisa berputar berbeda.','ring','First discovery: input stops while output rotates; introduce separation at functional use.'),
('input',5,'Rantai memutar penggerak','Saat mengayuh, rantai menarik sproket. Sproket memutar badan penggerak di dalam freehub.','axial','Chain travel drives sprocket and splined input body.'),
('inside',5,'Pengait bertemu cincin bergigi','Di sinilah pengait kecil bertemu cincin bergigi yang terhubung ke rumah roda.','ring','Cut shell at the shared axle; ring belongs to output, pawls to input.'),
('spring',5,'Pegas menyiapkan pengait','Pegas mendorong ujung pengait ke arah gigi. Bagian ini disebut pawl.','macro','First use of spring and pivot; pawl is biased outward.'),
('approach',6,'Menuju sisi yang menahan','Ketika penggerak berputar untuk mengayuh, ujung pengait mendekati sisi gigi yang tegak.','macro','Approach: a small angular clearance closes at a steep tooth face.'),
('contact',6,'Kontak ini meneruskan putaran','Lihat titik sentuhnya. Pengait tertahan di sisi itu, lalu mendorong cincin ikut berputar.','macro','Signature: approach, metal contact, coupled input/output and result hold.'),
('drive',5,'Sekarang keduanya ikut berputar','Putaran diteruskan ke rumah roda dan jari-jari. Roda pun didorong oleh kayuhan.','ring','Coordinated rotation, output spokes share ring motion.'),
('stop',5,'Lalu kayuhan berhenti','Sekarang kayuhan berhenti. Penggerak dari rantai melambat, tetapi roda masih melaju.','axial','Input stops; output continues, without claiming a powered wheel.'),
('overtake',6,'Roda melewati penggeraknya','Cincin pada rumah roda kini bergerak melewati pengait. Kontaknya datang dari sisi sebaliknya.','ring','Relative motion reverses; wheel overtakes the stopped input.'),
('ramp',6,'Sisi miring menekan pengait','Sisi miring gigi menekan pengait masuk. Pengait berputar pada dudukannya, melawan dorongan pegas.','macro','Macro: ramp contact depresses the pivoted pawl; no disconnect in midair.'),
('reset',5,'Lewat satu gigi, siap lagi','Setelah puncak gigi lewat, pegas mengangkat ujung pengait lagi menuju celah berikutnya.','macro','Release and spring reset after passage of the tooth.'),
('clicks',6,'Tekan, lepas, berulang','Tekan, lepas, lalu berulang. Kontak pengait dan gigi inilah sumber klik pada freehub tipe ini.','ring','Several genuine tooth passages; material contact cues on reset.'),
('bearing',6,'Bantalan memberi jalan putar','Bantalan menopang bagian yang berputar. Pengait mengatur sambungan satu arahnya, sehingga roda tidak harus menyeret pedal.','bearing','Bearing supports rotation; it is distinct from the pawl clutch.'),
('resume',7,'Kayuh lagi, pengait bertemu','Saat mengayuh lagi, penggerak menyusul. Setelah ujung pengait bertemu sisi penahan berikutnya, putaran tersambung kembali.','macro','Take-up closes a gap; no universal engagement angle or tooth count.'),
('answer',7,'Mengayuh terhubung. Meluncur lewat.','Jadi, saat meluncur, gigi melewati pengait. Saat mengayuh, pengait menahannya. Roda bisa melaju sementara pedal beristirahat.','proof','Matched opening with a large cutaway showing the hidden reason.'),
]
plan=[];t=0
for n,(key,d,title,text,view,job) in enumerate(rows,1):
 plan.append(dict(id=f's{n:02}-{key}',key=key,start=t,end=t+d,duration=d,title=title,text=text,view=view,job=job));t+=d
assert t==90
dump(V/'scene-plan.json',plan)
accounts=json.loads((R/'boards/di-balik-benda/ACCOUNTS.json').read_text(encoding='utf-8'))['accounts']
brief='''# Freehub: the wheel keeps rolling

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
schedule: next configured free slot; no queue displacement
commit: after the requested pipeline endpoint is verified

## Brief
One new Indonesian mechanism explainer, 90 seconds / 2700 frames, 1080x1920 at 30fps. Curious general audience. Explain why a pawl-type bicycle freehub permits coasting while the pedals rest. Scope: two opposing spring-biased pawls on the input carrier and an internally toothed ring fixed to the hub shell. This is a topology-based schematic, not a dimensional reproduction or a claim about every bicycle. Bearings support the rotation; do not claim the clutch makes propulsion or suppress all friction. No repair tutorial or performance comparison.

Creative direction: [editorial](../../boards/di-balik-benda/EDITORIAL.md), [visual frame](../../boards/di-balik-benda/frame.md), and SHOT-DIRECTION.md, frozen v6. Original 2.5D illustration, shaded metal side faces, input orange, active pawls blue, output teal. Fixed lower speech captions: Manrope 600 46px, y1500, x108 width848, max two lines. Mechanism stage x80..1000/y430..1410; center visible geometry and full useful sweep. About 80–95% stage occupancy. Cropped inactive context is explicit in contact macros.

Narration: one continuous tagged ElevenLabs eleven_v4 request with the literal root-.env voice. Use the maintained narration helper. BGM: none, exposing speech and the dry contact contrast. SFX: existing media-use library first; reuse source-verified frozen metallic/travel cues for physical events, soft editorial click only for the cutaway. No new SFX generation. Measured acoustic gaps govern scene cuts and any inserted observation pauses. Words remain estimated inside each acoustic anchor. Listening limitations must be reported honestly.

## Topic decision and overlap
Shortlist presented in conversation before selection: freehub, derailleur, steam kettle, locking tape measure, toaster, mechanical pencil, umbrella, hydraulic door closer, kitchen timer, stapleless paper binding. All differ in audience question and takeaway from registered episodes. Inspected filesystem includes unregistered roda-beda-putaran (differential), which does not explain bicycle coasting. Pawl contact has an analogy with the seatbelt episode, but this episode explains sustained overrunning and renewed drive, not emergency acceleration sensing and load restraint. No repeat of the existing lock, pump, cistern, stapler, music box or stitch cycle.

Selected freehub under --topic=auto: recognition strong (stopped pedals while cycling); curiosity strong (why wheel and pedals separate); proof strong (steep face versus ramp); causal depth workable (chain/input, pawl/tooth torque transfer, ramp/pivot/spring release, renewed engagement); discovery strong (hidden coupling); motion diversity workable (translation of chain, coupled rotation, pivoting, spring deflection); evidence strong (primary patent topology and manufacturer explanation); production scope workable in 16 shots. Derailleur is comparably rich but needs chain transfer in another spatial plane; kettle needs electrical/thermal dependencies; timer overlaps music-box gearing. Pencil/payung/closer are viable but less immediate than the chosen coasting question. Candidate evidence leads are retained in SOURCES.md; unselected candidates were not fully claim-verified.

## Hook choice, before script
1. “Pedalnya berhenti. Kenapa rodanya masih berputar?” Familiar exterior behavior; promise: show input/output separation and why teeth behave differently by relative direction.
2. “Bunyi klik saat sepeda meluncur itu datang dari mana?” Sound-led inspection; promise: show cyclic pawl depression and reset.
3. “Satu arah mengunci, arah lain lewat. Bagaimana bisa?” State comparison; promise: show the two tooth faces.
Recommended and selected: 1, agent choice under immediate automation, not human approval. It establishes recognizable context before the cutaway. SCRIPT.md was created only after this selection and the evidence check.

## Story contract
Central mystery: pedal stopped, wheel rotating. First discovery planned 5–10s: separate orange input and teal output rotate differently. Question chain: what connects chain to wheel → what contact passes drive → why does coasting avoid that stop → what resets the pawl → how does drive reconnect? Signature: a pawl approaching the steep tooth face, making contact, then moving the ring with it. Give a stable enlarged contact view; label slowed motion and illustrative spacing. Ending: same wheel/pedal contrast, with cutaway overrun showing the ramp pressing the pawl inward. Show original bicycle frame, rear axle and wheel center landmarks across views.

## Publishing targets
Inherited the entire board ACCOUNTS.json list without override:
'''
brief+='\n```json\n'+json.dumps(accounts,indent=2)+'\n```\n'
brief+='''
Trypost preflight: Admin's Workspace / 01a171dd-5281-730d-af07-f2168d17add7; exact @dibalikbenda.id ID 01a172c9-3761-700a-9798-00febaa9fa90, connected. Caller publishes directly; requires_approval false. Instagram reel: one video, max 900s/314572800 bytes; max 2200 caption characters and 5 hashtags. Queue configured daily 10:00 Asia/Jakarta. Use queue next and save observed UTC/offset schedule; do not invent its date. Local upload endpoint authorized by --delivery=queue. Optional feed sharing retained; no separate cover upload required, use supported cover offset if supplied.

## State
Brief/research/script agent-verified under delegated authorization. No human approval claimed. Next: complete and visually verify static storyboard before any synthesis/animation; then audio, animation, checks, preview, render, package, queue verification and commit.
Preview: none started yet. Usage start read: session 64% remaining, weekly 52%; this is only a snapshot. Context7 tools unavailable in this session; installed project-local CLI contract and CLI help/docs are the execution references.
'''
write(P/'EPISODE.md',brief);write(V/'BRIEF.md',brief)
write(P/'SOURCES.md','''# Evidence and visual boundaries

Bodies read through Jina MCP on 2026-10-28. Search snippets used only for discovery. No PDF text extraction used.

A. [US5460254A, Freehub](https://patents.google.com/patent/US5460254A/en). Primary topology: hub body 10 receives ratchet ring 20 with internal teeth 21; splined sprocket coupling 40 carries pawl driver 41, pawls 43 and spring 44. Pawls engage teeth to drive in one direction and allow driveless relative rotation in the other. Coaxial bearing support described. Do not inherit the patent's untested claims about eliminating damaging forces or superiority. Diagram uses two opposed pawls and a schematic common bias spring, not exact dimensions.

B. [Elitewheels: Understanding Bicycle Wheel Freehub Mechanisms](https://www.elite-wheels.com/technology/understanding-bicycle-wheel-freehub-mechanisms). Manufacturer explanation read in body: spring-loaded pawls engage ratchet teeth during pedaling and allow coasting. Describes click sound arising from engagement and notes different freehub architectures. Terminology around body/ring placement is general; A governs this schematic's exact carrier/ring topology. Do not use B's claimed sound/price correlations, point counts, performance advice or brands as universal facts.

C. [DT Swiss Ratchet Technologies Overview](https://www.dtswiss.com/en/wheels/ratchet-overview). Body read to distinguish face-ratchet designs from pawl hubs. No face-ratchet mechanics are substituted into the selected pawl illustration.

## Claim map
| ID | Script and visual claim | Evidence and scope |
| --- | --- | --- |
| C1 | Chain/sprocket turns splined input; wheel hub can overrun input | A introduction, coupling 40 and splines42; B pedaling/coasting. Stationary input is an explanatory coasting example, not a claim that pedals are always motionless. |
| C2 | Pawls on input act against internal ring attached to output hub | A 10/11/20/21/41/43. Axle fixed in the bicycle, spokes share hub-shell rotation. |
| C3 | Spring biases pawl toward engagement | A spring44 retaining pawls and B spring-loaded pawl operation. Spring shape/contact enlarged schematically; no spring constant or exact deformation claimed. |
| C4 | Steep face accepts drive; opposite ramp depresses pawl during overrun | A one-way hinged-pawl topology and B one-direction engagement/coasting. Asymmetric tooth geometry is the functional schematic interpretation of the ratchet, not patent dimensions. The animation solves tip clearance against the displayed tooth profile. |
| C5 | Repeated pawl/tooth encounters produce clicking in this design | B sound section; scope explicitly pawl-type, not all wheels or face ratchets. Foley is illustrative, not a recording of this product. |
| C6 | Bearings support rotation separately from the clutch | A bearing sets and coaxial assembly; no frictionless-motion claim. |
| C7 | Renewed drive closes a clearance then re-engages | A one-way drive and B engagement positions. No quantitative delay, threshold, speed, tooth count or simultaneous-load claim. |

## Creative interpretation
Original layered vector illustrations with shaded 12–18px side faces, shared axle landmark, cut shells and axial spacing. Tooth count18, drawn angles, exaggerated clearance, simplified spring path and slowed event timings are illustrative. Macro crop removes inactive ring/driver portions but retains pivot, tooth face and neighboring teeth. No engineering dimensions, maintenance advice or diagnostic promises.

## Unselected candidate evidence leads
These are discovery leads only, not verified script claims: [derailleur manufacturer/service explanation](https://www.parktool.com/en-us/blog/repair-help/how-a-rear-derailleur-works) (body read); [kettle steam-switch description](https://www.qianxunele.com/news/industry-news/comparing-steam-switch-and-bimetal-thermostat-functions.html); [tape locking pad](https://patents.google.com/patent/US4927092A/en); [toaster timing](https://wiki.restarters.net/index.php?title=Toasters&printable=yes); [pencil clutch](https://patents.google.com/patent/US2528328A/en); [umbrella linkage](https://patents.google.com/patent/US6170497B1/en); [hydraulic closer](https://patents.google.com/patent/EP0469697A1/en); [kitchen timer](https://patents.google.com/patent/US3555809A/en); [stapleless binding](https://patents.google.com/patent/US5024643A/en).
''')
script='# Narration v1 — selected hook 1\n\nLanguage: Indonesian. One continuous performance; 16 paragraph boundaries follow the explanatory shots. Estimated 90-second composition, to be reconciled with measured speech. Human approval: false; agent-verified under --automation.\n\n'+'\n\n'.join(x['text'] for x in plan)
script+='\n\n## On-screen copy\nSpeech captions reproduce only spoken words in short phrases. Titles are separate visual guidance:\n\n'+'\n'.join(f'{n+1:02}. {s["title"]}' for n,s in enumerate(plan))+'\n'
write(P/'SCRIPT.md',script);write(V/'SCRIPT.md',script)
write(V/'STORYLINES.md','''# Storyline selection
Five sketches: stopped pedal/coasting wheel; source of the click; follow chain torque; two synchronized opposing-direction specimens; one pawl's contact diary.

1. Selected: The resting pedal. Start with a recognizable bicycle, rear wheel moving while the crank rests. Open its rear hub, trace drive, inspect overrun and return to the same behavior with a visible cutaway. First two seconds: wheel spokes move, orange crank holds. Pale bench, v6 typography, original shaded metal, dry contact cues and foreground narration. Selected for recognition and a demonstrated causal ending.
2. Sound detective. Start on the coast clicking, progressively expose its source with a macro contact diary, return to a quiet coupled drive. First two seconds: spinning wheel and clicks, then hub location. Same medium; sound supplies the question. Not built because source of a sound is less direct than the wheel/pedal behavior.
3. Bold: two nested worlds. A split comparison keeps input still in one specimen and output still in the other, resolving relative motion before merging into one tooth contact. First two seconds: two visibly different rotating bodies. More analytical and denser at phone size; not built.
''')
write(V/'SPEC.md','''GOAL: Explain why a pawl freehub connects forward drive yet lets the wheel overrun the chain input.
OUTPUT: 1080x1920, 30fps, exactly90s/2700frames, H.264 MP4 plus AAC, SRT/VTT and cover.
LOOK: frozen board v6; #ECEEE9 bench, #F8F9F5 surface, #172B3B ink; input #C94422, active #2459C4, output #167580. Manrope800 titles72px/-3px tracking, Manrope600 captions46px/1.3; annotation IBM Plex Mono28px. Metal gradients with upper-left light, 12–18px side thickness, occlusion, fixed axle.
FRAMING: visible geometry fits x80..1000/y430..1410, center540/920; at least80% of one stage dimension for normal shots. Macro intentionally crops inactive context. Titles x108/y205/w800, notes y1380, captions x108/y1500/w848/max2lines. Caption top stays60px below all active geometry/annotation.
OBJECTS: recognizable bicycle wheels, frame, chain and crank; spline input body, output hub/spokes, internal asymmetric ratchet ring, two opposite pawls on input pivots, spring bias, fixed axle and ball bearing support. Stable topology and material identity in every view.
MOTION: deterministic state from paused GSAP scalar clock. Physical rotation linear; drive transition closes clearance then constrains input/output equal angular velocity. Coast output advances while input stops; geometric clearance solver depresses pawl at the displayed ramp and returns it to engagement. No gear reversal to fake coasting. Stable contact camera with diagnostic poses. Explanatory timing slowed and labeled.
SHOTS: scene-plan.json owns16 initial layouts; STORYBOARD.md owns questions, first uses, attention, diagnostic states and sound. Exactly90s, measured speech anchors replace estimates without shrinking composition.
SOUND: one continuous tagged ElevenLabs eleven_v4 using root-env voice; preserve native cache. Pauses inserted only inside measured quiet gaps; one final normalization. Frozen material contact/travel effects, bundled soft editorial click; no BGM, no generated SFX.
BANNED: small object in empty SVG; true3D; flat standalone diagram; decorative HUD, glows, particles, logo bumper; generic transition whooshes; repeated cycle with labels changed; rotating axle; pawl penetrating ring; pawl floating off its pivot; input carrying wheel during coast; teeth count/angle as engineering specification; unverified listening claims. Centered hero and pale ground are the explicit board identity.
QA: full pre-audio board, every scene midpoint, frame0, contact/ramp/reset diagnostic strips, phone sheet, shared axle and relative-motion checks; full HyperFrames gate; exact2700 frames and90s; acoustic quiet seams, source preservation, all captions, SFX waveform matches, full decode/loudness and preview lifecycle cleanup.
''')
shutil.copy2(R/'boards/di-balik-benda/frame.md',V/'frame.md')
for name in ['manrope.ttf','ibm-plex-mono.ttf','Manrope-OFL.txt','IBM-Plex-Mono-OFL.txt']:
 dst=V/'assets/fonts'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/'boards/di-balik-benda/assets'/name,dst)
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'))
assert not any(x['slug']==P.name for x in tracker['productions'])
tracker['productions'].append(dict(slug=P.name,topic='Pawl-type bicycle freehub: chain input, steep-face drive, ramp-induced pawl depression, spring reset, bearing support and renewed engagement',board='di-balik-benda',stage='script',status='complete',path='productions/'+P.name));dump(R/'TRACKER.json',tracker)
print(json.dumps(dict(scenes=len(plan),seconds=t,words=sum(len(s['text'].split()) for s in plan))))
