"""Create the episode's local, recoverable production records."""
from pathlib import Path
import json, hashlib
P=Path(__file__).resolve().parent; R=P.parents[1]
def write(p,t): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def dump(p,x): write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
accounts=R/'boards/di-balik-benda/ACCOUNTS.json'
snapshot=dict(source='board',board_accounts_file=accounts.relative_to(R).as_posix(),board_accounts_sha256=hashlib.sha256(accounts.read_bytes()).hexdigest(),accounts=json.loads(accounts.read_text())['accounts'])
candidates=[
('Pembuka gabus bersayap','Why do the wings rise while turning and extract the cork when pressed? Investigate worm, annular rack, sector gears, pivots and bottle reaction.','strong','strong','strong','workable','workable','workable','strong','strong'),
('Pembuka kaleng manual','How does the can advance under the blade? Investigate traction wheel, crank, cutter and rim guide.','strong','strong','strong','workable','workable','strong','strong','strong'),
('Payung lipat manual','How does one slider spread many ribs? Investigate runner, stretchers, rib pivots and latch.','strong','strong','strong','workable','workable','strong','strong','strong'),
('Diferensial terbuka','How can driven wheels turn at different speeds in a corner? Investigate carrier, spider and side gears.','strong','strong','strong','workable','weak','strong','strong','workable'),
('Pelubang kertas dua mata','How does one handle lower two cutters and return them? Investigate leverage, guides and springs.','workable','workable','strong','workable','strong','strong','workable','strong'),
('Penggiling merica manual','How does rotation turn peppercorns into smaller pieces? Investigate feed, rotor, stator and adjustment.','strong','strong','strong','workable','workable','strong','strong','workable'),
('Dongkrak gunting','Why does turning a screw raise the saddle? Investigate screw, nuts, links and constrained lift.','strong','strong','strong','workable','workable','strong','strong','strong'),
('Pemutar salad tarik','How does a pull spin a basket without rewinding it? Investigate cord, clutch, gearing and brake.','strong','strong','strong','workable','workable','workable','strong','strong'),
('Pemantik piezo','How does pressing create a spark? Investigate loading, release, hammer and piezo stack.','strong','strong','strong','workable','workable','strong','strong','workable'),
('Dispenser pita perekat','Why can tape unwind yet be cut at a fixed edge? Investigate roll support, adhesive release and serrated cutter.','workable','workable','workable','workable','strong','strong','workable','strong')]
episode='''# Gabus: sayap dan gigi

board: di-balik-benda
board_revision: approved v6; EDITORIAL.md / frame.md / SHOT-DIRECTION.md frozen in this run
topic_selection: auto, explicitly delegated by --topic=auto
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
human_approval: false
pre_render_authorization: delegated by the user's --automation instruction
requested_endpoint: publishing
delivery: queue
schedule: next configured slot; no changes to the channel schedule
commit: requested after pipeline completion; include this episode and its tracker entry only

## Brief
One 90-second Indonesian educational reel, 1080x1920, 30fps (2700 frames). Curious general audience. Explain a pin-pivot, twin toothed-sector cork puller with a circumferentially grooved central shaft, as described in US4063473A Fig.1. Do not claim a named commercial model or reproduce patent manufacture improvements. Follow Di Balik Benda's shaded layered 2.5D illustration, mineral bench, orange input / blue active / teal output. Narration: ElevenLabs eleven_v4, voice resolved from board then root .env. SFX: required causal cues from existing library. Music: none, to leave small contacts audible.

## Topic comparison
All candidates are provisional editorial ideas, not researched explanations. Ratings: strong/workable/weak. Evidence rates source feasibility, not a completed fact check. Columns: causal depth, discovery, motion diversity, evidence feasibility, production scope, recognition, curiosity, visual proof.

| Candidate | Brief | Depth | Discovery | Motion | Evidence | Scope | Recognition | Curiosity | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
'''
episode+='\n'.join('| '+' | '.join(row)+' |' for row in candidates)
episode+='''

Selected: winged corkscrew. Its familiar opposing movements create a precise question; the worm, annular rack/sector transmission and fixed bottle support provide a linked chain rather than repeating one contact. Recognition is workable because the opening establishes the tool on a corked bottle. Can opener and umbrella are strong alternatives; corkscrew has the clearest matched input/output reversal to investigate.

Overlap: TRACKER.json and all production folder names inspected. Existing episodes cover sewing, cylinder lock, trigger sprayer, cistern, stapler, music box, belt retractor, freehub, oscillating fan, pencil, kettle and tape measure. Cork engagement plus paired sector leverage has a different question and takeaway from the freehub's one-way pawls. Existing video-nearby-copy and its uncommitted tracker change are unrelated and must be preserved.

## Story contract and researched hook choice
Central mystery: why do pressing wings down lift a cork up? Opening: both wings rotate down while the cork rises inside a sectioned bottle neck.
First discovery: by approximately 8–12s show toothed sectors engaged with annular shaft grooves; downward wing rotation drives the shaft upward.
Question chain: what connects wings to the shaft? → how did the shaft engage the cork? → why do wings rise during insertion? → what stays fixed when pressing? → why does the cork follow the shaft?
Signature: macro of both opposing toothed sectors rotating about fixed pins, with no slip pitch motion and upward rack travel; settled view, 3 diagnostic poses, material cue on drive onset.
Ending proof: return to the same neck and wings, now transparent enough to see the engaged worm carrying the cork upward while the base rests on the rim.

Exactly three hooks, prepared after research and before SCRIPT.md:
1. "Sayapnya ditekan turun. Kenapa gabusnya malah naik?" Opposite visible movements; fulfills with the sector/rack and bottle support. Recommended and selected by agent under delegation.
2. "Diputar di atas, dua lengannya ikut terangkat. Apa yang menyambungkan gerakannya?" Starts with insertion and traces shaft descent.
3. "Pembuka ini bertumpu pada bibir botol. Di situlah tarikan gabus bisa bekerja." Starts from the reaction path, then follows gearing.
Selection: hook 1 states a specific observable puzzle without unsupported strength claims. No human approval inferred.

Script verification: single guide speaking to the viewer, no fictional actors or ambiguous pronouns. Technical terms follow visible functions. No quantitative mechanical advantage, repair advice, spring explanation, or universal product claim. Visible geometry is original and not to scale; nonfunctional contours and cork texture are illustrative. Bottle content is absent.

## Tool and account preflight
Trypost live identity matched the board's sole account: Instagram dibalikbenda.id, account 01a172c9-3761-700a-9798-00febaa9fa90 in Admin's Workspace 01a171dd-5281-730d-af07-f2168d17add7. Connected; publishes_directly true, requires_approval false. instagram_reel accepts 900s and 300MiB, caption 2200 characters / 5 hashtags. Configured Asia/Jakarta schedule available. Final queue slot resolved at write time.
Jina research failed explicitly: quota exhausted. SearXNG and Context7 tools absent from current tool inventory. Fallback: web search and original patent HTML bodies; installed HyperFrames skills and pinned CLI help for syntax. Do not report unavailable plan usage as a known allowance.

## Publishing targets
'''
episode+='```json\n'+json.dumps(snapshot,indent=2)+'\n```\n'
write(P/'EPISODE.md',episode)
write(P/'SOURCES.md','''# Evidence and scope

Evidence is distinct from the board's creative references. Read 2026-11-04 using web tool after Jina quota failure. Primary technical sources only.

## S1 — US4063473A, description of prior construction in Fig.1
https://patents.google.com/patent/US4063473A/xx
Pin/eyelet pivot variant, not the improved rib mounting of later figures.

| Claim | Evidence location | Qualification |
| --- | --- | --- |
| C1: base rests on bottle rim; housing guides a sliding shaft | Description of Fig.1, body2/base3/struts4/housing9 | Body held in place, bottle stays fixed in illustration |
| C2: lower worm embeds into cork on turning | Shaft10/worm11 and operation paragraph | One intact engaged cork; omit failure and material strength claims |
| C3: middle shaft has parallel circumferential grooves | Portion12/grooves13 | Annular grooves, not a second helix; drawing must preserve this distinction |
| C4: sector teeth mesh through housing slots | Lever15/sector16/pivot17–18/slot19 | Teeth stay coupled to shaft travel; pins fixed to support ears |
| C5: shaft descends during insertion, wings rise; lowered wings drive shaft up and remove cork | Operation following Fig.1 description | Show slow illustrative timing; no pitch or force ratio claimed |

## S2 — EP3130558A1, winged corkscrew operating architecture
https://patents.google.com/patent/EP3130558A1/en
Background plus Fig.1 description cross-check shaft grooves, sector levers, pin pivots and rim-engaging base. Secondary utensils and handle attachments are outside this episode. Conflicting part-number usages within its text are avoided; S1 is canonical for geometry.

## Claim coverage
Script shots 1–3 and 10–16: C1,C4,C5. Shots4–7: C1,C2. Shots8–9: C3,C4,C5. All hidden contact and motion in visuals use the same claim map. The qualitative lever explanation is an inference from the depicted longer arm and short toothed sector, with no numerical gain. Do not state frictionless behavior or equal load sharing.

## Original illustration and simplifications
Original layered SVG parts, satin gradients and offset depth. Section removes the front of the housing and bottle; annular grooves shown frontally and in an isolated shaft detail. Helix rotation is represented by a phase-shifting projected curve, with insertion progress proportional to cumulative rotation. Gear pitch motion uses rack displacement = sector radius × angular rotation. Clearances, tooth counts, cork travel, dimensions and timing are illustrative, marked on screen. No patent drawing is used as audience-facing art; a local reference image is retained for engineering inspection only.
''')
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8-sig'))
assert not any(x['slug']==P.name for x in tracker['productions'])
tracker['productions'].append(dict(slug=P.name,topic='Winged corkscrew: worm engagement, annular shaft grooves, paired toothed sectors, fixed pivots and bottle-rim reaction (US4063473A Fig.1 variant)',board='di-balik-benda',stage='research',status='complete',path=P.relative_to(R).as_posix()))
dump(R/'TRACKER.json',tracker)
print(P.name)
