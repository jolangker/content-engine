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

All scene, caption and SFX clocks derive from measured timing.json. Exact duration90s. Board caption position y1500 explicitly overrides the generic vertical template; user-approved board v6 supplies this placement. Listening unavailable: objective audio verification retained.
