"""Freeze the editorial plan and inherited identity before producing media."""
from pathlib import Path
import json, hashlib, shutil, sys
P=Path(__file__).resolve().parent; R=P.parents[1]; V=P/'video'
sys.path.insert(0,str(R/'.agents/skills/shortform-production/scripts'))
from narration import resolve_voice
def write(p,t):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def dump(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
rows=[
('mystery','Ditarik, kok kembali?',5,'whole','Pita meteran ditarik, lalu kembali sendiri. Tapi saat tombol dikunci, kenapa pitanya bisa diam?','Recognizable pull and short return, then lock; matched ending.'),
('reveal','Ada pegas terpisah',6,'section','Di dalamnya ada gulungan pita dan pegas pengembali. Keduanya terhubung, tetapi bukan bagian yang sama.','First discovery at 8 seconds: shell removal exposes separate reel and spring.'),
('pull','Tarikan memutar gulungan',5,'section','Kita mulai saat pita ditarik. Pita terurai, sehingga gulungannya ikut berputar pada poros.','Visible blade translation and coupled reel rotation.'),
('anchor','Satu sisi ditahan',6,'spring','Pegas pipih terhubung ke bagian berputar dan tumpuan tetap. Jadi, tarikan pita mengubah bentuk pegas.','Separate axial spring chamber; inner anchor fixed, outer connection follows reel.'),
('energy','Tarikan menyimpan energi',5,'spring','Pegas menyimpan energi dari tarikan tadi. Energi inilah yang nantinya memutar gulungan ke arah sebaliknya.','Spring bends under extraction; reverse torque arrow, no independent spring motor.'),
('return','Gulungan menarik pita',5,'section','Saat tarikan dilepas, pegas menggerakkan gulungan kembali. Pita pun tergulung masuk ke dalam rumahnya.','Release input, reel reverses and blade retracts together.'),
('question','Bagaimana menahannya?',5,'whole','Lalu bagaimana tombol menahannya? Kita lihat contoh meteran dengan pengunci geser dan lidah lentur ini.','Explicit selected variant US5806202A; blade extended for brake inspection.'),
('slider','Tombol membawa lidah',5,'lock','Tombol luar terhubung ke pengunci di dalam. Saat digeser, bagian bawah pengunci turun mendekati pita.','Follow finger pad through rib to internal curved slide member.'),
('guide','Pin mengikuti jalur',6,'guide','Dua pin kecil mengikuti jalur di rumah meteran. Jalur ini mengarahkan ujung lidah menuju permukaan pita.','One near-side follower pin shown; opposite symmetric pin identified, no detached parts.'),
('touch','Ujung menyentuh pita',6,'contact','Mula-mula, ujung lidah menyentuh pita. Di bawah pita ada penopang yang menjadi lawan tekanannya.','Signature pose A to B: tip approaches and contacts blade above fixed support.'),
('snap','Lewati tonjolan kecil',7,'guide','Dorongan dilanjutkan. Pin melewati tonjolan kecil, lalu masuk ke permukaan penahan. Gerakan ini membuat lidah makin melentur.','Signature pose B to C: follower crosses detent; tongue tip slides inward, flex increases.'),
('clamp','Pita terjepit',6,'contact','Lidah yang melentur menekan pita ke penopangnya. Jepitan ini menahan pita agar tidak ditarik kembali oleh pegas.','Signature pose D: settled clamp, reel stays still, reverse torque remains.'),
('held','Pegas masih menarik',5,'section','Jadi, pegasnya tetap memberi tarikan. Penguncilah yang menahan gerakan, selama jepitannya masih bekerja.','Show spring bias and opposing clamp simultaneously; no detached energy symbol.'),
('unlock','Jepitan dilepas',6,'lock','Saat tombol digeser kembali, pin keluar dari posisi penahan. Lidah terangkat, dan jepitan pada pita terlepas.','Follower climbs back over detent; elastic tongue relaxes and tip clears blade.'),
('rewind','Pegas mengambil alih',5,'section','Sekarang pegas bisa memutar gulungan lagi. Pita bergerak masuk, sementara pengunci tetap menjauh dari jalurnya.','Coupled return with stationary disengaged brake; return slowed for inspection.'),
('proof','Dua tugas berbeda',7,'proof','Jadi, yang mengembalikan pita adalah pegas. Yang membuatnya diam adalah jepitan pengunci. Tombolnya mengatur jepitan itu.','Matched opening proof: pull, lock and hold, release lock, rewind; causes visible.'),
]
plan=[];t=0
for i,(key,title,d,view,text,action) in enumerate(rows):
 plan.append(dict(id=f's{i+1:02}-{key}',key=key,title=title,start=t,end=t+d,duration=d,view=view,text=text,action=action));t+=d
assert t==90
dump(V/'scene-plan.json',plan)
accounts=R/'boards/di-balik-benda/ACCOUNTS.json'
targets=dict(source='board',board_accounts_file=accounts.relative_to(R).as_posix(),board_accounts_sha256=hashlib.sha256(accounts.read_bytes()).hexdigest(),accounts=json.loads(accounts.read_text())['accounts'])
brief='''board: di-balik-benda
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
schedule: next configured slot, Asia/Jakarta
commit: after pipeline completion; only changes from this run

## Production brief
Indonesian, 90 seconds, 1080x1920, 30fps, for curious general viewers. Original layered 2.5D sectional illustrations. Selected brake variant: US5806202A guided resilient tongue with follower pins, descending guide, detent and bearing ribs. A conventional spring-return reel is shown schematically, not claimed as an exact spring drawing from that brake patent. Axial separation is explicitly labelled. No universal claim about every tape measure. Spring geometry and timing are explanatory and not to scale. Hook calibration, blade curvature, bumper internals and manufacturing are outside scope.
Inherit [editorial](../../boards/di-balik-benda/EDITORIAL.md), [frame](../../boards/di-balik-benda/frame.md), and [shots](../../boards/di-balik-benda/SHOT-DIRECTION.md). Manrope 800 titles, Manrope 600 46px captions at y1500, IBM Plex Mono labels. Canvas #ECEEE9, ink #172B3B, orange input, blue active mechanism, teal output. Visible mechanism stage x80..1000, y430..1410. Captions retain the explicit board placement. Technical drawings become original shaded layered illustrations, not flat patent plates.
Narration: one continuous ElevenLabs eleven_v4 recording, delivery tags, board-aware root-env fallback. SFX: existing licensed library and frozen historical material cues. BGM intentionally absent to expose the small contacts and winding cues. No new SFX generation. Automated verification replaces human gates; listening limitations must be stated.

## Delegated topic selection
The following are provisional editorial proposals, not researched mechanism claims. All eight board criteria were evaluated. strong/workable/weak judge editorial feasibility, not retention.

| Candidate and short brief | Recognition | Question | Visual proof | Causal depth | Discovery | Motion | Evidence | Scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tape measure: why return yet stay locked? Investigate spring, reel and brake. Selected. | strong: household tool | strong: two opposing behaviours | strong: clamp versus recoil | strong: four handoffs | strong: spring separate from blade | strong: rotate/slide/flex | workable: patent leads | workable: single lock cycle |
| Toaster: what releases the carriage? Trace a selected latch cycle. | strong | strong | strong | strong | strong | strong | workable | workable: timer variant needed |
| Automatic umbrella: how does a button open it? Investigate runner and telescopic linkage. | strong | strong | strong | strong | strong | strong | workable | workable: dense geometry |
| Salad spinner: why does the basket keep spinning? Examine push drive and free motion. | workable | strong | strong | strong | strong | strong | workable | workable |
| Can opener: how do feed wheel and cutter cooperate? Follow one bite and advance. | strong | strong | strong | strong | strong | strong | workable | workable |
| Bicycle bell: how does a thumb movement ring repeatedly? Follow drive and striker. | strong | strong | strong | workable | strong | strong | workable | workable: music-box novelty lower |
| Ratchet screwdriver: why return without reversing the screw? Inspect pawl selection. | strong | strong | strong | workable | strong | workable | workable | workable: freehub overlap lower priority |
| Door closer: what slows the closing stroke? Investigate spring, piston and oil route. | strong | strong | strong | strong | strong | strong | workable | workable: valve variant needed |
| Correction tape: how do supply and take-up reels cooperate? Trace transfer onto paper. | strong | strong | strong | strong | strong | strong | workable | workable: friction drive needs source |
| Pump soap dispenser: how is it refilled after pressing? Investigate piston and valves. | strong | strong | strong | strong | strong | strong | workable | weak novelty: sprayer overlap |

Selection: tape measure has an immediately recognizable contradiction and a visible answer through distinct reel/spring/guide/clamp interactions. Tracker and all production folder names checked, including unregistered legacy folders. No tape-measure episode exists. Freehub and seatbelt share reels/locking but answer different questions through different mechanisms. No existing production was resumed or overwritten.

## Research outcome
Jina search failed with exhausted quota; SearXNG and Context7 tools are unavailable in this session. Used available web search and opened primary patent bodies and drawing pages. Evidence and qualifications in SOURCES.md. No claim is based only on a search snippet.

## Three hooks, before script drafting
1. “Pita meteran ditarik, lalu kembali sendiri. Tapi saat tombol dikunci, kenapa pitanya bisa diam?” Two familiar states, directly demonstrated. Selected under --automation.
2. “Tombol meteran ini tidak menggulung pitanya. Jadi, siapa yang menariknya masuk?” Contrast between actuator and energy source; supported but less immediate visually.
3. “Di dalam meteran, pegas dan pengunci bekerja berlawanan. Bagaimana keduanya mengatur satu pita?” Accurate system framing, but front-loads part names.
Recommendation and delegated choice: 1. Recognition first, then progressive discovery. Selection recorded before SCRIPT.md was created; no human approval claimed.

## Story contract
Central mystery: why does a self-returning blade stay extended when locked? First discovery: reveal separate spring/reel at approximately 8s. Question chain: what pulls it back? → where does energy come from? → how does the slider reach the blade? → what keeps the clamp engaged? → what changes when released? Signature interaction: guided pin crosses the detent while the tongue flexes and clamps the blade; settle camera, show approach/contact/flex/hold at large scale. Opening and ending use identical housing, blade and button landmarks. Ending exposes the spring and clamp while repeating pull/hold/unlock/return.

## Script verification
Read the complete spoken sequence against source scope: no unsupported universal lock claim, no claim that the visible blade itself provides all recoil, no invented ratchet, no motor, and no implication that the slider powers rewind. Exact brake example identified before internal detail. Technical names follow function. Narration and visual text are separate. All choices agent-verified under delegated authorization.
'''
write(P/'EPISODE.md','# Tape measure: spring and brake\n\n'+brief+'\n## Publishing targets\n```json\n'+json.dumps(targets,indent=2)+'\n```\nLive preflight: Admin\'s Workspace matches ID, @dibalikbenda.id connected, direct publishing permission, daily05:00 Asia/Jakarta schedule. Requested queue is explicit authorization.\n')
write(V/'BRIEF.md','# Production brief\n\n'+brief)
write(P/'SOURCES.md','''# Evidence and claim boundaries

Research date: 2026-11-03. Jina unavailable (quota); fallback web search and full source-body reads. Sources are evidence, not creative directions.

| ID | Primary record | Supported use and qualification |
| --- | --- | --- |
| S1 | [US5806202A](https://patents.google.com/patent/US5806202A/en), detailed description and figures2–5 | Selected slide-lock variant: external pad and rib carry curved body; two follower pins run in descending housing guides. Tongue first contacts blade; followers pass protrusion onto lock surface, flexing tongue against blade and supporting ribs. Reverse movement releases it. Original artwork preserves the contact sequence; cross-section shows one of the symmetric guides. |
| S2 | [US5210956A](https://patents.google.com/patent/US5210956A/en), background | Spring-biased coiled tape rewinds into housing; lock can hold extension against the spring. Used only for the conventional recoil principle, not this patent's alternative brake or special bumper. |
| S3 | [EP3318834B1](https://patents.google.com/patent/EP3318834B1/en), background paragraph on motor assembly and fixed hub | Tape connects to spring-containing rotating assembly and is tensioned against fixed hub. Supports simplified anchor/reel/spring explanation; its separate patented slide geometry is not imported. |

Script map: shots1–3 and6: S2; shots4–5 and15: S3 plus energy interpretation of spring loading; shots7–14: S1; shot16: S1/S2 synthesis. Energy storage/release is the physical interpretation of the documented spring bias. No quantitative spring law, material dimensions or torque curve is asserted.
Drawings inspected: S1 pages2–5 (figures1–5). Near-side pin, inclined guide, detent lock surface, blade and bearing ribs retain their functional relationships. Schematic return spring is labelled in an axially separated chamber: exact spring winding count, dimensions and manufacturing attachment are not claimed. Blade length, part spacing, flex displacement and action speed are illustrative. No named commercial product is represented. No hook accuracy or bumper design claim is made.
''')
script='# Narration — v1\n\nLanguage: Indonesian. Estimated scene windows before measurement. Spoken words only in the quoted sequence; headings and visual annotations are not narrated.\n\n'
script+='\n\n'.join(f'## {i+1:02} · {s["title"]} ({s["start"]}–{s["end"]}s estimated)\n\n{s["text"]}\n\nVisual: {s["action"]}' for i,s in enumerate(plan))+'\n'
write(P/'SCRIPT.md',script);write(V/'SCRIPT.md',script)
voice,resolution=resolve_voice(R,board='di-balik-benda')
tagged='[curious, clear conversational Indonesian] '+plan[0]['text']+'\n\n[explaining, measured pace] '+'\n\n'.join(s['text'] for s in plan[1:9])+'\n\n[focused, slightly slower] '+'\n\n'.join(s['text'] for s in plan[9:12])+'\n\n[clear, confident] '+'\n\n'.join(s['text'] for s in plan[12:])
dump(V/'audio_request.json',dict(provider='elevenlabs',board='di-balik-benda',lang='id',voice=voice,voice_resolution=resolution,tts_model='eleven_v4',lines=[dict(id='narration',text=tagged)]))
shutil.copy2(R/'boards/di-balik-benda/frame.md',V/'frame.md')
write(V/'STORYLINES.md','# Considered storylines\n\n1. Follow a blade from pull to lock to release (selected, strong visible cause).\n2. Start at detent macro then reveal entire tool (weaker recognition).\n3. Compare three brake designs (too broad for90s).\n')
write(V/'SPEC.md','''GOAL: explain how spring return and a sliding clamp control the same measuring blade.
OUTPUT: HyperFrames1080x1920,30fps;90s=2700frames.
LOOK: #ECEEE9 bench; #F8F9F5 surfaces; #172B3B ink; #C94422 input; #2459C4 active; #167580 output. Manrope800 titles70px/-3px, Manrope600 captions46px/1.3, IBM Plex Mono400 labels28px. Layered illustrated sidewalls offset14px, upper-left highlights, restrained contact shadows opacity.12. Mechanical contours and actual support faces carry the scene. No decorative HUD.
OBJECTS: recognizable D-profile tape housing with ribbed external button; reflective ruled blade with L-hook; cylindrical reel with distinct axial spring chamber; fixed shaft; flat spiral spring; curved slider and spring tongue; paired follower pins; guide ridge, detent and fixed blade support.
MOTION: pull/rewind linear coupled blade and reel; slider follows inclined guide; tongue flexes on contact; spring inner end stays fixed while outer end follows reel. Camera reframes then holds through signature contact. No rigid-body deformation except resilient tongue/spring. Changed timing explicitly labelled.
SHOTS: sixteen scenes in scene-plan.json and STORYBOARD.md; estimate first discovery8s, signature53–67s; exact windows replaced by measured acoustic anchors.
BANNED: flat patent-plate scenes, fake3D orbit, generic cards, glowing energy orb, arbitrary tooth ratchet, decorative looping movement, repeated identical cycle across three consecutive shots, small hero, unanchored labels, caption font reduction, unsourced parts.
QA: all16 scene stills; contact poses approach/touch/detent/clamp/release; full contact sheet; all caption groups; integer30fps scene map; final90s output and audio cue presence.
''')
tracker=R/'TRACKER.json';data=json.loads(tracker.read_text(encoding='utf-8-sig'));assert not any(x['slug']==P.name for x in data['productions'])
data['productions'].append(dict(slug=P.name,topic='Spring-return tape measure: reel, fixed-hub spring loading, guided slide lock, detent-driven resilient tongue clamping and release (US5806202A variant)',board='di-balik-benda',stage='script',status='complete',path='productions/'+P.name));dump(tracker,data)
print(json.dumps(dict(scenes=len(plan),seconds=t,words=sum(len(s['text'].split()) for s in plan))))
