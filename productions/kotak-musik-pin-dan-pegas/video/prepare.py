"""Initialize the episode's durable brief and pre-audio shot plan."""
from pathlib import Path
import hashlib, importlib.util, json, shutil, requests, re

V=Path(__file__).resolve().parent
P=V.parent
R=P.parents[1]
def write(p,s):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(s,encoding='utf-8')
def dump(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

shots=[
('Nadanya disimpan di mana?','Kotak ini bisa memainkan lagu tanpa baterai. Siapa yang menyimpan nadanya?','whole',6),
('Satu jenis kotak musik','Kita buka kotak musik pegas, dengan silinder berpaku dan pengatur kecepatan jenis gesek.','explode',6),
('Putaran jadi simpanan','Saat kuncinya diputar, pegas di dalam rumahnya digulung untuk menyimpan energi.','spring',5.5),
('Pegas melepas tenaga','Ketika mekanisme berjalan, pegas mengendur dan menggerakkan roda gigi penggerak.','spring',5),
('Tenaga diteruskan','Gigi yang saling bertaut meneruskan putaran, menuju silinder dan rangkaian pengatur kecepatan.','gears',5.5),
('Silinder membawa pola','Silinder ini bukan pengeras suara. Di permukaannya, ada pin yang menonjol.','drum',5.5),
('Pola menjadi urutan','Letak pin menentukan gigi sisir mana yang dipetik, dan kapan petikan itu terjadi.','pattern',5.5),
('Pin mengangkat ujung','Perhatikan satu pin. Saat mendekat, pin mengangkat ujung gigi sisir logam.','pluck',5.5),
('Lepas, lalu bergetar','Setelah pin lewat, gigi itu terlepas dan bergetar. Getaran inilah yang menghasilkan nada.','release',6),
('Sisir yang bernada','Gigi-gigi sisir disetel untuk nada berbeda. Urutan petikannya membentuk lagu.','comb',5),
('Ada pengatur laju','Tapi putaran juga perlu dibatasi. Rangkaian roda gigi ikut memutar governor, pengatur kecepatannya.','governorlink',5.5),
('Sayap menyentuh dinding','Pada jenis ini, dua sayap lentur mengembang saat berputar, lalu menyentuh dinding cakram.','governor',6),
('Gesekan menahan putaran','Sentuhan itu menimbulkan gesekan, yang menahan laju mekanisme agar tidak melesat bebas.','brake',5.5),
('Tugasnya berbeda','Jadi, governor mengatur laju. Pola pin memilih urutan petikan; sisir menghasilkan nadanya.','roles',5.5),
('Bekerja bersamaan','Selama lagu berjalan, pegas, roda gigi, silinder, dan governor bekerja sebagai satu rangkaian.','cycle',6),
('Lagu sebagai pola fisik','Tenaganya tersimpan di pegas. Lagunya tersusun sebagai pola pin, yang dibaca lewat petikan logam.','answer',6),
]
plan=[];t=0
for n,(title,text,view,d) in enumerate(shots,1):
    plan.append(dict(id=f's{n:02}',title=title,text=text,view=view,start=t,end=t+d,duration=d));t+=d
assert t==90
dump(V/'scene-plan.json',plan)
account_path=R/'boards/di-balik-benda/ACCOUNTS.json'
target=dict(source='board',board_accounts_file=str(account_path.relative_to(R)).replace('\\','/'),board_accounts_sha256=sha(account_path),accounts=json.loads(account_path.read_text(encoding='utf-8'))['accounts'])
brief='''# Music box: pins and spring

board: di-balik-benda v4 (2026-10-25)
topic_selection: auto, delegated by --topic=auto
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
human_approval: false
pre_render_authorization: delegated by the user's --automation instruction
requested_endpoint: publishing
delivery: queue (next configured slot; no custom time)
format: 1080x1920, 30 fps, exactly 90 seconds
language: Indonesian
audience: curious general viewers

## Direction
Follow energy from a wound spring to gears, a pinned cylinder, comb vibration and a centrifugal friction governor. Scope: original explanatory model based on US5449856A; not every music box. Do not combine this friction governor with the air-brake variant. Exaggerated clearances, slowed motion, removed shell and enlarged pins are labelled. Pitch/tune and gear ratios are illustrative, never measurements of a particular product.

Inherited [editorial](../../../boards/di-balik-benda/EDITORIAL.md), [visual tokens](../../../boards/di-balik-benda/frame.md), and [choreography](../../../boards/di-balik-benda/SHOT-DIRECTION.md). Medium: layered 2.5D illustrated metal/polymer, upper-left light, dark blue contours, pale mineral bench. No flat infographic scenes. Sixteen explanatory shots, including pin/comb and governor contact macros.

Narration: ElevenLabs eleven_v4, root .env voice, one tagged full-script recording at native speed. SFX: existing library first, illustrative material contact and a distinct editorial inspection cue. No BGM: the subject is sound production, so keep the explanation and diagnostic plucking/release cues exposed without a competing tune. Reused sounds are illustrations, not an acoustic measurement or a reproduction of the pinned melody.

## Topic decision and overlap
Compared ten topics in conversation: music box, wing corkscrew, manual can opener, derailleur, seatbelt retractor, pawl hub, ratchet wrench, impact sprinkler, mechanical clock, crank pencil sharpener. Music box selected for five linked interactions, visual discovery and technical evidence. Not selected merely for implementation ease. Other candidates remain research leads, not verified scripts.
Checked TRACKER and all production folder names. No music-box episode exists. Existing sewing machine, differential (unregistered historical folder), lock, sprayer, toilet, stapler and simple fasteners have distinct central questions. Preserve all existing productions.

## Hook decision (before script)
1. “Kotak ini bisa memainkan lagu tanpa baterai. Siapa yang menyimpan nadanya?” Energy and note-pattern mystery; can be answered with spring, pins and comb.
2. “Tonjolan kecil ini menentukan kapan sebuah nada berbunyi.” Pin-contact-first macro story.
3. “Pegas ingin lepas cepat. Kenapa lagu kotak musik tetap teratur?” Governor-first story.
Recommended/selected: 1, agent choice under delegated automation, presented before script drafting. It covers both stored energy and stored note sequence. Human approval is not asserted.

## Publishing targets
```json
'''+json.dumps(target,ensure_ascii=False,indent=2)+'''
```
Live preflight: Trypost Admin's Workspace 01a171dd-5281-730d-af07-f2168d17add7; exact Instagram account connected; caller requires_approval=false, publishes_directly=true. instagram_reel supports 90 seconds and up to 300 MiB; caption limit 2200, five hashtags. Queue configured daily 10:00 Asia/Jakarta. Actual future slot comes from Trypost at creation.

## Current state
Research and hook selected; script agent-verified for claims and estimated timing. Next: static complete visual storyboard before audio and animation. No preview server created yet. Commit requested after the entire queue pipeline finishes.
'''
write(P/'EPISODE.md',brief);write(V/'BRIEF.md',brief)
script='# Narration and screen copy\n\nAgent-verified script v1; selected hook 1. Estimated timing; measured alignment supersedes estimates. All substantive claims map to C1–C6 in SOURCES.md.\n\n'
for s in plan:script+=f"## {s['id']} ({s['start']:g}–{s['end']:g}s)\n\nNarration: {s['text']}\n\nOn screen: {s['title']}\n\n"
write(P/'SCRIPT.md',script);write(V/'SCRIPT.md',script)
write(P/'SOURCES.md','''# Evidence ledger

Research date: 2026-10-27. Jina search followed by source-body reading. No creative image serves as mechanical evidence. Search snippets were leads only. Source text is paraphrased below.

## Sources
A. [US5449856A — Music box](https://patents.google.com/patent/US5449856A/en), detailed description, figures 1–4 and claims 1–2. Primary technical description of a spring-driven pinned-cylinder movement with comb, gear train and two flexible centrifugal friction wings. Basis of the selected variant and original diagrams; patent describes an implementation, not all products.
B. [US5543577A — Construction of music box](https://patents.google.com/patent/US5543577A/en), background and detailed structure. Independent technical corroboration of spring case, gear train, cylinder, comb-like vibrating member and a centrifugal damping friction disk. It has different support geometry; do not merge its assembly into A.
C. [Pinwheel Crafts — How Does a Music Box Work?](https://pinwheelcrafts.com/blogs/news/how-does-a-music-box-work), educational explanation read in full relevant passages. Corroborates stored spring energy, pin sequence, lifted/released vibrating comb teeth and tuned pitches. Its air-resistance governor is a different variant and is expressly excluded from the episode's governor claims.
D. [MBSI glossary](https://mbsi.org/glossary?cat_id=56), spring barrel, second wheel and speed regulator entries. Supports terminology and mechanical regulation, not the geometry of A's friction wings.
Reuge manufacturer's page returned empty/404 bodies; search snippets were not used as claim evidence.

## Claim map
| ID | Script/visual claim | Support and limits |
| --- | --- | --- |
| C1 | Winding stores spring energy; spring recoil drives gears | A description: spring leaf 20, axle 22, key 220 and driving gear 21; C winding section. No exact torque or winding count claimed. |
| C2 | Gear train couples cylinder and regulator | A gears 21/31/30/4/5 and regulator shaft 62; B corroborates architecture. Diagram spacing/tooth count reduced, arrows not a physical extra drive shaft. |
| C3 | Cylinder pins pluck comb teeth, selecting note and timing | A pins 300, comb 8 and vibrating teeth 80; C cylinder pattern. Simplified pin layout is an original illustration, not a known song. |
| C4 | A lifted and released comb tooth vibrates and produces a note; teeth are tuned differently | A sound mechanism; C comb section. Deflection and slowed vibration exaggerated for visibility; no claim of visual oscillation frequency matching audio. |
| C5 | Rotating flexible wings expand, touch disk wall, generate friction and regulate speed | A figures 4a–c, description and claims 1–2. B independently documents centrifugal damping disk. Two illustrated wings, not air blades; fixed enclosure does not rotate. Avoid perfect speed invariance and exact threshold claims. |
| C6 | Governor controls rate, pin pattern chooses sequence, comb generates sound | Functional synthesis of C2–C5, consistent with A and C; not a claim that governors select pitch. |

## Diagram and sound qualifications
Original layered 2.5D schematics, no product or source illustration copied into the film. Clearances, pin sizes, tooth bending and time enlarged. The pin approaches, lifts, releases and leaves the tooth; only the free end vibrates. Selected patent figures inspected as technical references. Governor is shown as an explanatory top section: wings rotate with shaft and flex outward toward a fixed friction wall. Full assembly layout simplified; macro views retain named/color landmarks. Sounds are reused licensed illustrations; they do not reproduce a specific instrument or melody.
''')
shutil.copy2(R/'boards/di-balik-benda/frame.md',V/'frame.md')
for f in ['manrope.ttf','ibm-plex-mono.ttf','Manrope-OFL.txt','IBM-Plex-Mono-OFL.txt']:
    (V/'assets/fonts').mkdir(parents=True,exist_ok=True);shutil.copy2(R/'boards/di-balik-benda/assets'/f,V/'assets/fonts'/f)
write(V/'STORYLINES.md','''# Storylines
Five seeds: follow stored energy; read a pin as a physical score; investigate a runaway tempo; follow one tooth from lift to sound; reassemble silent parts into an operating box.

1. Selected — A song stored in metal. A familiar wind-up box on a pale bench opens along assembly axes. The camera follows energy into a pinned score, then dives into plucking and friction regulation before returning to the box. First two seconds: recognizable box and exposed brass cylinder already visible, opening question on screen. Sound: narration plus licensed illustrative contact/release cues, no competing music.
2. Physical score. Begin inside one enlarged pin row, move through the sequence like reading a score, then reveal the spring machinery underneath. More abstract opening; not built.
3. The runaway investigation. Begin with a conceptual too-fast motion and solve why the governor constrains it, then reconstruct the whole sound chain. Risks implying an actual failure test; not built.
''')
write(V/'SPEC.md','''GOAL: Viewers can distinguish stored energy, physical note selection, sound generation and speed regulation.
OUTPUT: HyperFrames 1080 x 1920, 30 fps; 90 x 30 = 2700 frames.
LOOK: #ECEEE9 bench; #F8F9F5 surface; #172B3B ink; #C94422 input; #2459C4 inspected contact; #167580 output. Original 2.5D SVG with front/side faces, fixed upper-left shading, 4 px outlines, 10–20 px part thickness, no filters. Manrope 800 titles 76px, tracking -3px; body/captions 44px/1.25; IBM Plex Mono 30px annotations. Text and key object inside x108–930, y192–1330. Captions y1150–1305. Hero y480–1060.
OBJECTS: recognizable wooden wind-up music box, spring barrel/key, meshing drive gears, brass cylinder with pins, fixed-root metal comb, worm-linked friction governor with two flexible wings inside a stationary wall.
MOTION: coupled rotations linear; winding/reveal/attention power2.inOut; pin lift and release preserve contact and fixed tooth root; vibration damped analytic motion. Each scene uses finite time functions from a paused GSAP clock. Time/clearance enlarged and labelled. No camera-only action.
BANNED: navy void, glow, particles, decorative HUD, bouncing parts, floating loops, flat infographic-only scenes, moving read text, repeated unchanged operation, unsupported exact ratios, air-brake blades in this friction-governor episode. Board-required mineral field, functional mono annotations and 2.5D shading override generic defaults. No decorative logo/kicker.
QA: all 16 scene poses; pin approach/contact/release intermediate frames; governor expansion/wall contact; fixed enclosure and comb root; forward/reverse seeks; title/caption clearance; 90 sec export; cue timing and decoded audio.
SHOTS: scene-plan.json before audio, timing.json after measured alignment. STORYBOARD.md records each shot's causal handoff and diagnostic poses.
''')
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));assert not any(x['slug']==P.name for x in tracker['productions'])
tracker['productions'].append(dict(slug=P.name,topic='Spring-driven cylinder music box: winding, gear transmission, pin/comb plucking and two-wing centrifugal friction governor (US5449856A variant)',board='di-balik-benda',stage='storyboard',status='in_progress',path=f'productions/{P.name}'))
dump(R/'TRACKER.json',tracker)
# Technical reference images stay in a production-local research directory.
page=requests.get('https://patents.google.com/patent/US5449856A/en',timeout=40);page.raise_for_status()
urls=re.findall(r'<meta itemprop="full" content="([^"]+)',page.text)
(P/'research').mkdir(exist_ok=True)
dump(P/'research/figure-urls.json',urls)
for n,url in enumerate(urls[:5],1):
    r=requests.get(url,timeout=40);r.raise_for_status();(P/f'research/patent-figure-{n}.png').write_bytes(r.content)
print(json.dumps(dict(shots=len(plan),words=sum(len(s['text'].split()) for s in plan),reference_figures=len(urls))))
