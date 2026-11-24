# Gabus: sayap dan gigi

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
| Pembuka gabus bersayap | Why do the wings rise while turning and extract the cork when pressed? Investigate worm, annular rack, sector gears, pivots and bottle reaction. | strong | strong | strong | workable | workable | workable | strong | strong |
| Pembuka kaleng manual | How does the can advance under the blade? Investigate traction wheel, crank, cutter and rim guide. | strong | strong | strong | workable | workable | strong | strong | strong |
| Payung lipat manual | How does one slider spread many ribs? Investigate runner, stretchers, rib pivots and latch. | strong | strong | strong | workable | workable | strong | strong | strong |
| Diferensial terbuka | How can driven wheels turn at different speeds in a corner? Investigate carrier, spider and side gears. | strong | strong | strong | workable | weak | strong | strong | workable |
| Pelubang kertas dua mata | How does one handle lower two cutters and return them? Investigate leverage, guides and springs. | workable | workable | strong | workable | strong | strong | workable | strong |
| Penggiling merica manual | How does rotation turn peppercorns into smaller pieces? Investigate feed, rotor, stator and adjustment. | strong | strong | strong | workable | workable | strong | strong | workable |
| Dongkrak gunting | Why does turning a screw raise the saddle? Investigate screw, nuts, links and constrained lift. | strong | strong | strong | workable | workable | strong | strong | strong |
| Pemutar salad tarik | How does a pull spin a basket without rewinding it? Investigate cord, clutch, gearing and brake. | strong | strong | strong | workable | workable | workable | strong | strong |
| Pemantik piezo | How does pressing create a spark? Investigate loading, release, hammer and piezo stack. | strong | strong | strong | workable | workable | strong | strong | workable |
| Dispenser pita perekat | Why can tape unwind yet be cut at a fixed edge? Investigate roll support, adhesive release and serrated cutter. | workable | workable | workable | workable | strong | strong | workable | strong |

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
```json
{
  "source": "board",
  "board_accounts_file": "boards/di-balik-benda/ACCOUNTS.json",
  "board_accounts_sha256": "b975f156df5c9c6bb0ac33f940b2cef5191793fd2c659a027a4e75291dcc25f3",
  "accounts": [
    {
      "provider": "trypost",
      "workspace_id": "01a171dd-5281-730d-af07-f2168d17add7",
      "workspace_name": "Admin's Workspace",
      "social_account_id": "01a172c9-3761-700a-9798-00febaa9fa90",
      "service": "instagram",
      "handle": "dibalikbenda.id"
    }
  ]
}
```

## Visual storyboard verification
Agent inspected boards/storyboard.png (1920x4221), all16 styled stills in correct order, no missing images. HTML board and plan agree. Fixed disconnected handle (zero-width gradient stroke), duplicate cork gradient/part ID, and extraction continuity. Stage framing uses functional crops for macro; original shaded2.5D and board caption retained. Artifacts: video/STORYBOARD.md, video/boards/storyboard.html, video/boards/storyboard.png, video/boards/stills/. Agent-verified before synthesis; no human approval claimed.

## Audio placement
One ElevenLabs eleven_v4 synthesis, root-env voice, native95.440s, 222 words. Original cache preserved. Derived pitch-preserving tempo=1.14987952 chosen only if native recording leaves insufficient observation time. Source at native tempo is retained. Every derived-master sample preserved across verified quiet splices; one final normalization targets-16LUFS/-2dBTP.15 verified acoustic cuts, integer30fps map; final master90s. Individual word timings are estimates reanchored to utterances, not independent forced alignment. 69 short caption groups. Bundled media-use manifest inspected; separate cue planning will copy frozen material assets. Music absent intentionally. Listening unavailable; no auditory or phone-speaker approval claimed.

## Preview and pre-render verification
HyperFrames check passed: lint/runtime/layout/contrast/audio/craft zero errors and zero warnings, browser executed. Dedicated frame-state proof passed2684 interior frames plus reverse seeks across16 scenes, including fixed insertion cork, rigid extraction, pin/rack coupling and10 continuity seams. All69 caption groups fit at46px with one line. All15 acoustic seams passed. Agent inspected beat, phone and signature seam sheets. Pipeline-owned preview: video project, PID8896, port3002, http://127.0.0.1:3002/#project/video, created by this run; retain through render verification then stop. HTTP readiness passed. No human approval or listening claimed. Final storyboards updated to measured timing; initial pre-audio board archived.

## Visual review repair
Fresh-eyes review under HyperFrames review.md found P1 at78.4–81s: cork clearance not evident. Extended extraction beyond insertion-start shaft position while preserving fixed pins, rack pitch and rigid worm/cork travel. Final cork bottom568.64 against rim590 provides21.36 illustrative units clearance; s15 settles by82s and holds. Reverse-seek and continuity proof passed again. Initial storyboard is historical; measured final board and repaired proof frames represent delivered version. Signature8-frame transfer strip inspected. Full-speed perceptual playback/listening not available; state checks and rendered sampled motion do not claim such a review.

## Verified export and package
v1 MP4, cover and caption sidecars verified. Package matches SHA256 489377503e52d746ee55ef8599026443f2eb374520e5b760bb795c772e239c52. Queue endpoint, sole inherited Instagram account. Intent/fingerprint persisted before upload and creation.

## Queue delivery complete
Trypost Admin's Workspace, Instagram @dibalikbenda.id. Post 01a1a316-db00-70b0-8834-6dc07edf9813, observed scheduled / queue, UTC 2026-11-03 22:00:00, local 2026-11-04T05:00:00+07:00. Exact copy/type/account/media read back; public HTTP200 copy has identical15741582bytes and SHA256489377503e52d746ee55ef8599026443f2eb374520e5b760bb795c772e239c52. Receipt: PUBLISHING.json. Scheduling complete; publication is future and not monitored. No live publication claimed.

Export verification:90.000s,2700frames,1080x1920,30fps,H.264/yuv420p,AAC48kHz; full decode passed. Agent inspected all16 decoded proof frames. All16 encoded SFX matches within0.334ms;15 encoded acoustic boundaries passed. Mix-13.7LUFS,-1.7dBTP,zero clipping. Listening unavailable. Pipeline preview stopped; final status not-running, PID8896 gone and port3002 no listener.

Pipeline and scheduling complete. Requested Git handoff includes this production and its tracker entry, excluding pre-existing work on video-nearby-copy and unrelated tracker text. Video remains editable through HyperFrames; renderer suggested hyperframes open . for desktop editing.
