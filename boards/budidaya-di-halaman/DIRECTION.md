# Budidaya di Halaman

Revision 10. Editorial v9 approved on 2026-11-24; see [Revision 9](#revision-9). Visual v5 approved on 2026-11-25, including the living-world motion preview and organic SFX library; see [Revision 10](#revision-10-visual-v5).

## Approved direction

On 2026-11-21, the user narrowed the concept to home-yard cultivation, ponds, and related activities, then replied “cocok” to the updated proposal and creation question. This authorized building the board for that niche. The complete visual and editorial package was approved by the user on 2026-11-22.

The audience is Indonesian-speaking general viewers curious about growing and raising things in a small yard. The viewer starts building on the first spoken beat, puts a simple version into use, and develops that same setup in response to what happens. The episode culminates in the working pond, rearing setup, or other backyard production system that the viewer has seen take shape. Then one scene shows what its first output is worth. Backyard aquaculture anchors the scope. Episodes are delivered at 1.25x. Every connected account gets one shared content package, and the thumbnail doubles as the film's end card.

## Reference and adaptations

The three local `jadiginisodara` reels establish the vertical illustrated cutaway, rapid setup, repeated problem and repair, progressive white-and-yellow captions, and final site-wide reveal. [Timestamped evidence and coverage](references/ANALYSIS.md) records the sources, selected frames, and limits of visual and acoustic analysis.

The studies use original locations, layouts, illustrations and sample wording. DM Sans is a selected typeface substitute, and the colors and dimensions are implementation choices informed by the visible roles in the clips. The overall mix direction uses the measured prominence of the separated vocal stem. Delivery, music and effects are creative specifications for future episodes.

## Package

- [Editorial framework v9](EDITORIAL.md) and [visual specification v5](frame.md).
- [Editable style board](style-board.html), [PNG preview](style-board.png), [Visual v5 study section](visual-v5-section.png), and [phone view](style-board-phone.png), rendered by [capture.py](capture.py). Three independent studies cover a pond and its outlet, aeration in a hatchery, and a live-feed harvest. A separate strip shows three static positions of a flow reveal. The revision 6 row adds the [income scene](income-study.png), the [thumbnail](thumbnail-study.png) with its crop check, the timeline position of both new beats and the shared-package rules ([assets/studies-r6.js](assets/studies-r6.js)). The Visual v5 row adds the 4-plane 2.5D depth parallax diagram, reactive weather/time-of-day study, event-driven camera grammar strip, and 16-asset organic SFX kit ([assets/world-v5.js](assets/world-v5.js), [assets/studies-v5.js](assets/studies-v5.js)).
- [Reusable organic SFX library](assets/sfx/manifest.json) and [credits](assets/sfx/CREDITS.md) — 16 loudness-normalized CC0/Pixabay effects (hybrid sourcing: CC0/Pixabay first, ElevenLabs Sound Effects reserved for authorized gaps).
- [Motion preview](motion-preview.mp4) and its [editable project](motion-preview/index.html); `motion-preview/build_draw.py` regenerates its copy of the study helpers, `world-v5.js`, and organic SFX assets.
- [Voice configuration](AUDIO.json) sets ElevenLabs **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh`) as the board default, as selected by the user. [Publishing accounts](ACCOUNTS.json) configures Instagram `@bikindihalaman.id` in Trypost (`Admin's Workspace`), selected and confirmed by the user on 2026-11-22. The YouTube channel **Bikin Di Halaman** (`@bikindihalaman_id`, same workspace) was added on 2026-11-22 at the user's request ("koneksian dahulu youtube Bikin Di Halaman"), matched by display name against the live Trypost account list. The Facebook page **Bangun Di Halaman** was added on 2026-11-22 at the user's request; Trypost returns no username for it, so `handle` records the page display name. The Instagram account stays first in the list; the closing-caption handle cue uses that first account.
- [Production contract](CONTRACT.json) restates the editorial v9 / visual v5 rules a finished episode can be checked against: 90–112.5 s at 1x with `delivery.speed` 1.25, first action within the first second, `motion.max_static_seconds` 3.0 s, the hook's first sentence within 10 s and its “tapi” by 12 s, caption region, narration with event-locked organic effects and no music, and twelve judged rules (including event-level `reframing`, 4-plane `living-world`, and `event-sfx`). A contract was first added on 2026-11-22, when the user approved gating productions against a board contract; each entry cites its source section.
- Motion evidence: the Visual v5 [motion preview](motion-preview.mp4), approved on 2026-11-25 (reusing the Pribs narration take).
- Revision 9 (editorial v9, visual v4, its contract and style board) is preserved in [revisions/9](revisions/9/). Editorial v8 and its contract are preserved in [revisions/8](revisions/8/). Editorial v7 and its contract are preserved in [revisions/7](revisions/7/). Editorial v6 and its contract are preserved in [revisions/6](revisions/6/). Revision 5 (editorial v5, visual v2, its contract and style board) is preserved in [revisions/5](revisions/5/).

## Revision 6

Requested by the user on 2026-11-23: add one income scene once the system works, deliver renders at 1.25x, make a thumbnail and check whether Trypost can upload one, and stop differentiating the content package per platform or account. On the same day the user chose: the duration window applies to the 1x composition at 90–112.5 s, so the 1.25x file runs 72–90 s and fits a Facebook Reel; the income scene shows a sourced rupiah estimate; the thumbnail is delivered as a PNG plus an in-video end card.

Prepared in `drafts/r6/` and promoted to the board root on approval; the v5 package moved to `revisions/5/`.

Trypost check (2026-11-23, `list-content-types-tool` and the post tools): Trypost has no custom thumbnail image upload. A video item's `meta.cover_offset_ms` chooses a cover frame on content types with `supports_video_cover`: `instagram_reel` and `instagram_feed` support it, while `youtube_short`, `facebook_reel` and `facebook_post` do not. This is why the thumbnail is also the film's end card. The workspace-wide tooling now supports this: the contract field `delivery.speed` makes the export gate measure a retimed file against its 1x composition, and the content-package and publishing references follow a board-level shared package and the cover-frame route.

Visual review of the draft (2026-11-23, 1440 px board, 1080 × 1920 studies, 390 px phone view): the first income render hid the keeper and basin behind the card, and its scale was too small to be the decisive interaction. The card was moved into the sky, and the scale, basin and keeper were enlarged so the weighing spans more than 40% of the width. Fish drawn behind the bowl and basin rims were redrawn on top. In the thumbnail, a band between the filled sky and the pond scrim was removed by matching their colour. Remaining limit: the income figures (10 kg, Rp25.000/kg, Nov 2026) are illustrative and have no source.

The user approved the static draft on 2026-11-23 ("approve"). This covers editorial v6, the visual spec v3 and the style board with its studies. Because the revision changes the motion direction, the board's approval still waits for the motion preview.

Motion preview: [motion-preview.mp4](motion-preview.mp4) (SHA-256 `c10e76c6…0781`) and its [editable project](motion-preview/index.html). It is a 24.83 s composition at 1x, rendered as a 24 fps master (`motion-preview/verification/master-24fps.mp4`, 596 frames) and restamped to 30 fps with the audio time-stretched 1.25x, pitch kept. The delivered clip is 19.88 s, 1080 × 1920.
- What it demonstrates:
  - The build hook: bare yard, digging from 0.25 s, liner, filling, fish.
  - A hard cut to the income beat: three fish onto the hanging scale, the needle settling, and the income card entering with the total chip arriving last and held 3.1 s at 1x.
  - A cut to the closing wide pull-out: congratulation and next-build question, "bikin di halaman" staying yellow, the handle fading in.
  - A hard cut to a 0.5 s end card identical to the thumbnail. Instagram's cover would point at about 19,620 ms.
- Sound: narration in the board voice and CC0/Pixabay effects; sources are in `motion-preview/assets/audio/CREDITS.md`.
- Measurements (`episode_qa.py --fingerprint`, caption region masked): first motion 0.2 s, longest static 0.2 s, held share 0.0, −13.64 LUFS, −1.86 dBTP.
- HyperFrames check: no errors. Remaining warnings follow approved board positions (cover at 240 px, captions at 1392 px, handle beneath them, outside some platform safe zones) and the intentionally short end card (0.6 s against a 2 s closing-line floor).
- Twelve decoded frames of the delivered clip were inspected.
- Limits at build time: the agent could not hear the mix (`listening: unavailable`); the figures and price month are illustrative.

The user watched the motion preview and approved it on 2026-11-23 ("approve"). Revision 6 is now the board's approved package: new productions selecting this board use editorial v6, visual v3 and its contract, while existing productions keep their snapshots. Remaining limits: the illustrative income figures, and the user's listening approval is the only listening record of the preview mix.

## Revision 7

Requested by the user on 2026-11-24: vary hooks within the pattern "Kalo kamu {aksi}.., {konjungsi temporal} kamu {aksi}.., kamu sudah punya... Tapi, {masalah}..."; give scripts the chain premature first system → problem → improvement → new problem → improvement again → problem–improvement loop → stable system → monetization → closing (closing unchanged); and make clear the board is not limited to dug pits.

Editorial v7 was prepared in `drafts/r7/` and reviewed with a comparison against v6 and a full sample script. The user approved it on 2026-11-24 ("approve dan pastikan contohnya masuk di editorial"). It is now the board's [editorial framework](EDITORIAL.md), including the [sample script](EDITORIAL.md#sample-script), with its [contract](CONTRACT.json): `build-first`, `shortfall-before-fix`, `final-job` and `income-scene` are reworded, `hook.first_sentence_max_seconds` is 10 s and a `tapi` turn is required by 12 s. Visual v4 is unchanged. New productions selecting this board use editorial v7 / visual v4; existing productions keep their snapshots.

- Choices made by the agent and accepted with the approval: at least two problem–improvement rounds with problems that differ in kind, a hook of roughly 8–12 s at 1x, and no repeat of the previous episode's first verb or connector.
- The user clarified that the dots in the original hook shorthand stand for words to complete. The current template names those slots explicitly and the worked hooks use ordinary punctuation.
- Open: the motion preview still speaks the v6 hook ("Kalau kamu gali lubang…, jadilah kolam lele sendiri"). Refreshing it needs new narration and a re-render; the user has not asked for it.

## Revision 8

Requested by the user on 2026-11-24: “tambahkan lebih banyak event problem-improvement loop. tiap loop dibuat lebih padat sehingga event lebih banyak”.

Editorial v8 was prepared in `drafts/r8/`. The user approved it on 2026-11-24 (“setuju”). It is now the board's [editorial framework](EDITORIAL.md) with its [contract](CONTRACT.json); v7 is preserved in [revisions/7](revisions/7/). Visual v4 is unchanged. New productions selecting this board use editorial v8 / visual v4; existing productions keep their snapshots.

- At least six problem–improvement rounds, counting the first two; seven or eight is typical (v7: at least two, three or four typical). Problems come from different triggers.
- A new [round density](EDITORIAL.md#round-density) budget: about 6–10 s per round at 1x (2–4 s problem, 4–6 s fix and test), roughly 15–25 spoken words, one cause per round, fix and test in one shot, no recap between rounds.
- The event map grows from eight to ten events to fifteen to nineteen, with each problem and each improvement counted as one. The 1x window stays 90–112.5 s, with a per-stage time budget.
- The worked catfish outline now runs seven rounds (17 events, 97 s at 1x). The bucket sample script runs seven rounds in 259 words; each round is 17–25 words.
- Contract: `shortfall-before-fix` requires six rounds of about 10 s or less, `event-map` names fifteen to nineteen events (it said seven to nine while the editorial said eight to ten), and `revision` is editorial v8 / visual v4.
- Open: the motion preview is unaffected, since it shows the hook, the income scene and the closing.

## Revision 9

Requested by the user on 2026-11-24: *"update board budidaya-di-halaman mengenai script yang 'Tapi'-nya berulang menjadi lebih bervariasi dan juga smooth"*.

Editorial v9 was prepared in `drafts/r9/` and approved for promotion by the user on 2026-11-24 (*"ya pr harus memuat promosi editorial v9"*). It is now the board's [editorial framework](EDITORIAL.md) with its [contract](CONTRACT.json) (SHA-256 `e7513a8dd9983e098c80bff61d1f7c59fb9b38be1535e8b2cf141322b5e1da55`); v8 is preserved in [revisions/8](revisions/8/). Visual v4 is unchanged. New productions selecting this board use editorial v9 / visual v4; existing productions (including `kolam-lele-di-halaman`) keep their recorded v8 snapshots.

- **Hook pattern preserved:** The four-slot opening hook keeps `"Tapi {masalah}."` (and `hook.turn` `["tapi"]` within `12.0 s`), preserving the board's signature opening turn.
- **Varied, smooth round transitions:** [Round density](EDITORIAL.md#round-density) replaces the v8 instruction to start every subsequent round with `"Tapi"` with varied natural Indonesian transitions matched to the trigger: elapsed time (`Besok paginya, …`, `Seminggu jalan, …`, `Lama-lama, …`, `Suatu pagi, …`, `Masuk bulan kedua, …`, `Nggak lama kemudian, …`), condition/weather (`Pas tengah hari, …`, `Begitu hujan deras turun, …`, `Tiap kali ganti air, …`), or direct side-effect (`Masalahnya, …`, `Giliran …`, `Cuma gara-gara itu, …`, `Ternyata, …`). `"Tapi"` stays reserved for the hook turn (and at most one later sharp reversal if truly earned).
- **Updated narration review & sample script:** [Review the narration](EDITORIAL.md#review-the-narration) adds an explicit non-repetition check for `"Tapi"`, and the full 7-round bucket [sample script](EDITORIAL.md#sample-script) is rewritten so `"Tapi"` appears only in the hook while Rounds 2–7 flow smoothly with varied transitions.
- **Contract update:** [CONTRACT.json](CONTRACT.json) updates `revision` to `editorial v9 / visual v4` and appends *"and transitions between rounds vary naturally rather than repeating 'Tapi' on every round"* to `shortfall-before-fix`.
- **Open:** The motion preview is unaffected, since it shows the hook, the income scene and the closing.

## Revision 10 (Visual v5)

Requested by the user on 2026-11-25 to upgrade the board's SFX richness, event-level camera movement, and full dynamic/living backyard background (non-minimalist), using a **Hybrid** SFX sourcing strategy (royalty-free CC0/CC BY via Openverse/Freesound & bundled Pixabay first; ElevenLabs Sound Effects reserved only for authorized gaps). Prepared in `drafts/r10/`, reviewed via the static style board and rendered motion preview, and **approved for promotion by the user on 2026-11-25** (*"approve, promosikan, commit dan push"*). Revision 9 (Editorial v9 / Visual v4) is archived in [revisions/9](revisions/9/). New productions selecting this board use editorial v9 / visual v5 and its contract; existing productions keep their recorded snapshots.

- **Spec & contract:** [frame.md](frame.md) (Visual v5) and [CONTRACT.json](CONTRACT.json) (`editorial v9 / visual v5`, SHA-256 `6681a52a9464efab8b2c846a0b08b731e06fde1e9a947e9772b333d54eac9626`, validated via `episode_qa.py --contract`). Sets `motion.max_static_seconds: 3.0`, upgrades `reframing` to event-level camera choreography, updates `income-scene` for a world-anchored price tag, and adds judged rules `living-world` and `event-sfx`.
- **Reusable organic SFX library (16 assets, 0 ElevenLabs credits used):** [assets/sfx/manifest.json](assets/sfx/manifest.json) and [assets/sfx/CREDITS.md](assets/sfx/CREDITS.md) (`dig-soil`, `wood-stake`, `tarp-rustle`, `fabric-net`, `pvc-snap`, `water-pour`, `water-splash`, `water-drain`, `water-bubbles`, `rain-shower`, `pellet-scatter`, `scale-chain`, `yard-ambience`, `cam-whoosh`, `tag-click`, `tag-pop`). Every asset was natively listened to; an initial `water-bubbles.mp3` take containing a spoken slate ("Aerator sound effect, take one") was caught by listening and replaced with a clean CC0 bubble recording (`locontrario23`, Freesound 395914).
- **Static style board:** [style-board.html](style-board.html), [style-board.png](style-board.png), [visual-v5-section.png](visual-v5-section.png), and [style-board-phone.png](style-board-phone.png) (`DM Sans` loaded, 0 overflow, 0 clipped text at 1440 px and 390 px). Visual review caught the `0.80× Yard` depth badge overlapping the keeper's torso in the first draft render; shifted right (`x=152`) and re-captured cleanly.
- **Playable motion preview:** [motion-preview.mp4](motion-preview.mp4) (`19.87 s` delivered at 1.25× / 30 fps, 1080 × 1920, SHA-256 `f55b6164f5a9f2ae…`) rendered from [motion-preview/index.html](motion-preview/index.html) (`24.83 s` @ 24 fps 1× master, reusing the existing Pribs narration take).
  - Demonstrates 4-plane 2.5D depth parallax (`0.18×` sky/clouds/sun, `0.45×` hills/gliding birds, `0.80×` swaying banana fronds/fence/shrubs/butterfly/dusk lit window + fireflies, `1.00×` hero cutaway/ripples/wet soil + `1.14×` wide edge-grass), event-driven camera punch-ins + route tracking + damped `2–4 px` micro-impact settles synced to 25 organic SFX cues + soft diegetic yard air beds (`bgm: none`), and a world-anchored price tag that stays pixel-locked to its beam nail during camera movement.
  - **Verification:** `hyperframes check --json` passed with 0 errors (`audio: 0/0`, `contrast: 25/25`, only expected board safe-zone and 0.625 s end-card warnings). `episode_qa.py --fingerprint` (caption region masked): `first_motion_seconds: 0.2`, `longest_static_seconds: 0.0`, `held_share: 0.0`, `integrated_lufs: -14.01`, `true_peak_dbtp: -1.97`. Inspected 10 decoded frames ([delivered-sheet.png](motion-preview/verification/delivered-sheet.png)) and listened natively to the delivered 1.25× audio mix: all speech intelligible, foley crisp and frame-locked, zero masking.

## Visual v4: price tag

On 2026-11-23 the user rejected the income card and its animation: "cardnya terlalu blocking dan animasinya lambat". They chose a tag hung on the scale. Visual v4 replaces the card with a 400 px paper tag hung by a string from a nail on an overhang of the scale beam (nail at 600, 594 px). It holds only the sum, the yellow total chip and a two-line `estimasi harga pengepul / Nov 2026` note at 28 px, the phone type floor.
- Timing: it drops in 0.2 s on "sepuluh" (10.8 s at 1x) and its swing settles within 0.5 s. Each figure pops in 0.15 s on its word (13.04 s and 14.72 s), and the tag grows downward. The total holds 3.1 s at 1x.
- Supporting changes: the slow drift zoom in the income scene was removed so the tag stays on its nail. The editorial wording and the `income-scene` contract rule now say "price tag", with the contract revision set to editorial v6 / visual v4. No production references visual v3, so v3 survives in Git history rather than under `revisions/`.
- Updated files: [frame.md](frame.md#price-tag), [income study](income-study.png), [style board](style-board.png), and the re-rendered [motion preview](motion-preview.mp4) (SHA-256 `c789edc1…bb11`, 19.88 s delivered).
- Measurements: first motion 0.2 s, longest static 0.2 s, −13.68 LUFS, −2.05 dBTP. HyperFrames craft now warns only about the intentional 0.5 s end card.

The user approved visual v4 on 2026-11-23 ("approve") after watching the re-rendered motion preview. New productions selecting this board use editorial v6 / visual v4 and its contract.

## Review

The first nila script followed a particle through a completed system. Editorial v2 made the keeper's goal, first attempt, visible shortfall, response, and retest part of angle selection. The maggot production then opened with a scoop from an established bin, so its build covered a collection improvement. On 2026-11-22 the user clarified that a board episode starts with the creation of the cultivation setup itself. The user also set a 90-second minimum, asked for more events, and specified a closing congratulation followed by a question about what to build next. Editorial v3 applies those requirements at topic selection and script review, with a 97-second illustrative catfish outline.

The user clarified that the build should be the subject of the episode, as in the reference pond and farm scripts. Editorial v4 compresses the initial build, then makes the system's development and first working result the story. It includes a 100-second illustrative outline. [Script evidence by reference](references/ANALYSIS.md#script-structure-across-the-references).

The user approved the editorial v5 / visual v2 package on 2026-11-22; revision 6 replaced it on 2026-11-23 and it is preserved in [revisions/5](revisions/5/). Earlier editorial revisions remain available as [v1](revisions/1/EDITORIAL.md), [v2](revisions/2/EDITORIAL.md), [v3](revisions/3/EDITORIAL.md), and [v4](revisions/4/EDITORIAL.md); visual v1 is preserved as [v1](revisions/1/frame.md). Visual v1 was exported at 1440 × 1328 and inspected together with all three portraits at a 390 px phone viewport; visual v2 keeps the same approved visual assets and adds only the closing caption signature cue.

The compositions and motion poses are static. The user set the board's audio direction to narration with scene-linked sound effects and no background music. [Current audio direction](frame.md#audio). On 2026-11-22, the user also approved embedding the consecutive signature phrase **bikin di halaman** into the spoken closing question (no opening intro or spoken follow CTA), paired with the yellow closing caption highlight and subtle handle cue in [frame.md](frame.md#framing-and-captions).
