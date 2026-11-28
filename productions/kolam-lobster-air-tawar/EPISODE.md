# Bikin Kolam Lobster Air Tawar di Halaman

## Brief

- **Slug:** `kolam-lobster-air-tawar`
- **Topic selection:** `topic_selection: user`. On 2026-11-22, after requesting `"carikan topik"`, the user replied `"setuju"` to the recommended candidate #1 from the 10-topic shortlist: building a backyard lined pond/tank for freshwater redclaw crayfish (*Cherax quadricarinatus*) from an empty yard corner through escape prevention, molting shelters, bottom-water management, and a first household harvest.
- **Board:** `budidaya-di-halaman`, revision 5 (`editorial v5 / visual v2`, status `approved`), explicitly selected via `--board=budidaya-di-halaman`. Inherit [direction](../../boards/budidaya-di-halaman/DIRECTION.md), [editorial framework v5](../../boards/budidaya-di-halaman/EDITORIAL.md), [visual specification v2](../../boards/budidaya-di-halaman/frame.md), and [contract](../../boards/budidaya-di-halaman/CONTRACT.json).
- **Contract snapshot:** [CONTRACT.json](CONTRACT.json), copied from `boards/budidaya-di-halaman/CONTRACT.json` (`sha256: 3da249adc998ea7ee3f9553177324a113543f8022294314ed756f1822e98bc52`) and validated with `episode_qa.py --contract`.
- **Audience and POV:** Indonesian-speaking general viewers curious about small-yard cultivation, addressed as `"kamu"` in casual second-person Indonesian. The viewer is the sole builder/keeper across the episode. Frame as a household hobby setup, not a commercial farm profit claim.
- **Format and runtime target:** Vertical 9:16 (`1080 × 1920`, 30 fps) flat 2D cutaway illustration in one consistent shaded backyard corner. Minimum finished duration `90 seconds` (target `~98–108 seconds`, budgeted at `>= 221` spoken words—targeting `~235–255` words—for Pribs's measured `2.61 words/s` pace across 4 recorded episodes).
- **Audio plan (inferred from board contract):**
  - Narration: `use` — board default ElevenLabs voice **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh`) from [AUDIO.json](../../boards/budidaya-di-halaman/AUDIO.json) with `eleven_v4`.
  - BGM: `none` for the entire episode per board contract.
  - SFX: `use` — restrained, scene-linked physical contact, water fill/drain, PVC pipe placement, and aerator bubble cues subordinate to speech.
- **Execution and delivery policy:**
  - Intake policy: `execution_policy: human_review` through hook selection and script review. Superseded on 2026-11-22 by the active automation policy recorded under [Execution policy](#execution-policy-2026-11-22).
  - `endpoint: content_package` (default full production endpoint; no `--until` cap requested).
  - `delivery: package` (local verified MP4 export + companion files + `CONTENT_PACKAGE.md`; no external upload/draft/publish authorized).

## Publishing targets

Inherited from `boards/budidaya-di-halaman/ACCOUNTS.json` for local package destination planning and the closing-caption handle cue (`@bikindihalaman.id` from the first listed account); no remote calls or publishing authorized:

```yaml
publishing_targets:
  source: board
  board_accounts_file: boards/budidaya-di-halaman/ACCOUNTS.json
  board_accounts_sha256: 768706ecdff76690c669c9d12edeca43fc5f48a508e0dbf817363ce19a7ea8ad
  accounts:
    - provider: trypost
      workspace_id: 01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37
      workspace_name: "Admin's Workspace"
      social_account_id: 01a2022d-bc57-71d8-9217-6e0319cb6c03
      service: instagram
      handle: bikindihalaman.id
    - provider: trypost
      workspace_id: 01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37
      workspace_name: "Admin's Workspace"
      social_account_id: 01a202dc-0e4a-72ae-bec8-589ab7f90045
      service: youtube
      handle: bikindihalaman_id
```

## Candidate comparison and overlap check

- **Editorial comparison:** Ten non-duplicate backyard builds were evaluated (freshwater crayfish shelter pond, catfish spawning with *kakaban*, *Daphnia/Moina* live-feed tub, two-tier vermicompost bin, anti-washout *Azolla* bed, mini oyster-mushroom rack, *gurame* leaf-feeding pond, *hapa* fry nursery, Kratky raft kangkung box, and mud-free clean-water eel tub). Candidate #1 was recommended and accepted by the user because aquaculture anchors `budidaya-di-halaman`, crustaceans/benthic stock are new to the board, and every husbandry constraint happens visibly at the tank walls and floor in a 2D cutaway. No published board performance snapshot exists yet to weight historical metrics.
- **Overlap check:** Verified against `TRACKER.json` and `productions/` directories. Existing board episodes cover aquaponics (`akuaponik-lele-dan-kangkung`, `aquaponik-pasang-surut`), recirculating tilapia solids settling (`jejak-kotoran-kolam-nila`), BSF prepupal ramp harvesting (`maggot-jalan-ke-wadah`), a lettuce wick planter (`pot-sumbu-selada`), and container potatoes (`kentang-dalam-pot`). None covers crustacean containment, molting refuges, or benthic shelter-pond construction.

## Researched story chain

Grounded in [SOURCES.md](SOURCES.md) (claims C1–C5):

1. **Build and stock the first basin (`00:00–00:12`):** At a bare, shaded corner of the yard, the keeper frames a low rectangular box, lines it with tarpaulin, fills conditioned shallow water, and acclimates/releases uniform juvenile redclaw crayfish (*Cherax quadricarinatus*). Early milestone: the first simple lobster pond is running.
2. **Shortfall 1 — Overnight climbing escape (`00:12–00:23`):** After a dusk-to-morning sky shift, a crayfish is seen climbing a corner fold / dangling hose up to the top rim. High water near the rim and wall-hugging lines give climbing crayfish an exit path (C2).
3. **Fix 1 — Freeboard, inward rim lip, and overhead line (`00:23–00:35`):** The keeper lowers the waterline slightly, fits a smooth inward-projecting lip around the top edge, and keeps hoses off the wall. Retest: a climbing crayfish meets the inward lip and drops back into the water (C2).
4. **Shortfall 2 — Molting vulnerability on the bare floor (`00:35–00:48`):** In cutaway section on the flat bare liner, one growing crayfish sheds its old shell (*ganti kulit* / *molting*) and sits pale and soft-shelled beside its empty exoskeleton while harder-shelled tankmates close in with raised claws (C3).
5. **Fix 2 — Tiered PVC pipe / roster shelters and shade (`00:48–01:02`):** The keeper places stacks of open-ended PVC pipe tunnels and slotted roster blocks across the floor (more holes than crayfish, aligned so water can pass through) plus partial overhead shade. Retest: a newly molted crayfish backs safely into its own pipe tunnel until its shell hardens (C3, C1).
6. **Shortfall 3 — Sunken leftover feed fouls the bottom layer (`01:02–01:15`):** Excess sinking pellets settle between the floor shelters; uneaten residue darkens at the bottom interface where bottom-dwelling crayfish breathe, pushing sluggish crayfish toward the edges (C4, C2).
7. **Fix 3 — Overhead-suspended aeration, measured dusk feeding, and bottom drain flush (`01:15–01:30`):** The keeper hangs an air stone from above (not touching the walls) to circulate oxygen down to the floor, feeds measured evening portions on a check tray, and opens a screened bottom drain valve to flush settled sludge before topping up clean water (C4).
8. **Final job and wide sign-off (`01:30–01:44`):** After time-compressed growth (months compressed visually, C5), the keeper lowers the water through the bottom drain valve, lifts a drained PVC shelter stack cleanly, and collects grown blue-green redclaw crayfish into a harvest basin. Return to the wide yard view showing the inward rim lip, shade, suspended aerator, shelter stacks, and bottom drain together, closing with the congratulation and consecutive `"bikin di halaman"` question plus `@bikindihalaman.id` handle cue.

## Hook options (v1)

No board performance analysis exists yet; options are evaluated against `CONTRACT.json` (`build-first`, `hook-frame`, `first_sentence_max_seconds <= 5.0` at Pribs's `2.61 words/s` pace, `first_motion_max_seconds <= 1.0`) and [script-craft.md](../../.agents/skills/shortform-production/references/script-craft.md).

1. **Build-and-floor contrast (Recommended)**
   - **Mechanism:** Immediate build action paired with a spatial insight—unlike fish swimming mid-water, everything critical for crayfish happens on the tank floor and walls.
   - **Spoken opening:** `"Kalau kamu mau bikin kolam lobster, rakit dulu bak di halaman. Bentangkan terpal dan isi air dangkal, soalnya hidup lobster semuanya di dasar bak."` *(First sentence: 11 words, ~4.21 s at 2.61 wps.)*
   - **Frame 0 and first-second motion:** Frame 0 shows the bare, shaded clay corner of the backyard beside the house with corner stakes ready; within `< 1.0 s`, the keeper's hands set the first wooden/bamboo pond frame onto the bare ground.
   - **On-screen line:** Phone-readable progressive caption (`46 px` DM Sans ExtraBold, active word `#FFD44D`): `"Kalau kamu mau bikin kolam lobster,"` / `"rakit dulu bak di halaman."` Cover copy (over the completed cutaway): **BIKIN KOLAM LOBSTER DI HALAMAN** (yellow accent on **KOLAM LOBSTER**).
   - **Appeal and promise:** Puts the viewer straight to work while planting one visual lens—watch the floor and walls—that unifies all three build upgrades (rim barrier, floor shelter pipes, and bottom aeration/drain) through harvest.

2. **Overnight escape tension**
   - **Mechanism:** Rapid starter build contrasted with the beginner surprise of crayfish climbing out overnight.
   - **Spoken opening:** `"Kalau kamu rakit bak terpal kosong, kamu bisa pelihara lobster sendiri. Tapi kalau tepinya polos tanpa penghalang, besok pagi lobsternya bisa memanjat keluar."` *(First sentence: 11 words, ~4.21 s at 2.61 wps.)*
   - **Frame 0 and first-second motion:** Frame 0 shows the empty yard corner with a low frame and folded dark-teal liner at its edge; within `< 1.0 s`, the keeper pulls the liner taut across the bare frame floor.
   - **On-screen line:** Progressive caption: `"Kalau kamu rakit bak terpal kosong,"` / `"kamu bisa pelihara lobster sendiri."` Cover copy: **LOBSTER KABUR DARI BAK HALAMAN?** (yellow accent on **KABUR DARI BAK**).
   - **Appeal and promise:** Hooks curiosity with a concrete, unexpected crustacean behavior (climbing walls/hoses at night), then pays it off first at `00:12–00:35` before uncovering the deeper molting and bottom-oxygen upgrades needed to reach harvest.

3. **Shaded narrow-yard transformation**
   - **Mechanism:** Space-opportunity framing turning an unused shaded side-yard corner into a self-contained crustacean harvest setup.
   - **Spoken opening:** `"Kalau kamu punya sudut halaman teduh, mulai aja pasang bak terpal kosong. Dari satu bak dangkal ini, gimana caranya lobster tumbuh aman sampai panen?"` *(First sentence: 11 words, ~4.21 s at 2.61 wps.)*
   - **Frame 0 and first-second motion:** Frame 0 shows an empty shaded strip beside the house wall; within `< 1.0 s`, the rectangular pond frame drops into place on the bare ground and water begins pouring in.
   - **On-screen line:** Progressive caption: `"Kalau kamu punya sudut halaman teduh,"` / `"mulai aja pasang bak terpal kosong."` Cover copy: **PANEN LOBSTER DARI SUDUT HALAMAN** (yellow accent on **PANEN LOBSTER**).
   - **Appeal and promise:** Speaks directly to viewers with limited shaded yard space and promises a step-by-step physical build that answers how to keep molting, bottom-dwelling crayfish safe until harvest.

**Recommendation:** Option 1. It opens cleanly on `"Kalau kamu mau bikin kolam lobster..."` (matching the board's `"bikin … di halaman"` identity), hits the hands-on build action in 11 words (`~4.2 s`), and gives the viewer a single spatial rule (*semua kejadiannya di dasar dan dinding bak*) that connects climbing prevention, PVC molting shelters, and bottom-waste flushing into one coherent engineering story rather than only teasing the first obstacle.

- **Hook selection:** `hook_selection: user`. On 2026-11-22 the user replied `"2"`, selecting **Option 2 (Overnight escape tension)**. Its two opening sentences are preserved verbatim at the start of [SCRIPT.md](SCRIPT.md).

## Script check (v1)

Drafted [SCRIPT.md](SCRIPT.md) across 9 scenes around Hook Option 2 and verified against [CONTRACT.json](CONTRACT.json) and [script-craft.md](../../.agents/skills/shortform-production/references/script-craft.md):

- **Word count & budget (`episode_qa.py --budget 275 --voice 5g0yKK2JwTRka0IG61Hh`):** `275` spoken words; measured Pribs pace `2.61 words/s` across 4 recorded episodes -> predicted narration `105.4 s`, predicted film `112.2 s`, `fits: true` against `duration_seconds.min: 90` (`words_for_range: [221, null]`).
- **First sentence timing:** `"Kalau kamu rakit bak terpal kosong, kamu bisa pelihara lobster sendiri."` — `11 words`, predicted `4.21 s` (`<= 5.0 s` limit).
- **Selected hook's three parts:**
  - *Spoken line:* `"Kalau kamu rakit bak terpal kosong, kamu bisa pelihara lobster sendiri. Tapi kalau tepinya polos tanpa penghalang, besok pagi lobsternya bisa memanjat keluar."`
  - *Frame 0 & `< 1.0 s` motion:* Bare shaded backyard corner with low pond frame and folded dark-teal tarpaulin ready; within `< 1.0 s`, the keeper pulls and fastens the liner across the empty frame floor.
  - *On-screen line:* Progressive 46 px caption (`"Kalau kamu rakit bak terpal kosong,"` / `"kamu bisa pelihara lobster sendiri."`) and dedicated cover copy **LOBSTER KABUR DARI BAK HALAMAN?** (yellow `#FFD44D` on **KABUR DARI BAK**).
- **Cold-read & POV continuity result:** Read all 275 spoken words continuously without headings or visual cues. `"kamu"` resolves unambiguously to the single backyard builder/keeper throughout; `"mereka"` and `"-nya"` resolve cleanly to the stocked crayfish or immediately preceding tank part. During cold-read, repaired three passive clauses in Scene 7 (`dikuras, ditambah, ditakar`) to active `"kamu"` actions (`kamu kuras`, `isi lagi`, `taruh pakan sore di nampan kecil`) so the feed tray's introduction is explicitly acted by the keeper, and refined Scene 8's `"bercapit kebiruan"` to `"bercangkang biru kehijauan"` to match both sexes of *Cherax quadricarinatus* in S1/S2/S4.
- **Contract judged rules concerning the script:**
  - `[pass]` `hook-frame`: Frame 0 shows the bare yard corner, frame, and folded liner (`< 1.0 s` liner stretch) with 46 px phone-readable progressive captions and cover headline **LOBSTER KABUR DARI BAK HALAMAN?**.
  - `[pass]` `pictures-alone`: Ordered sub-beats across Scenes 1–9 visually depict every step from bare-ground assembly through three shortfalls/repairs to drain-and-pipe harvest without relying on text.
  - `[pass]` `event-density`: All 9 scenes depict concrete state changes or assembly actions, with 2–3 timed visual sub-beats marked inside every >19-word scene.
  - `[pass]` `motion-variety`: Adjacent scenes alternate shot scales (`wide -> close -> medium -> close -> medium-wide -> close -> medium -> medium-close -> wide`).
  - `[pass]` `ear-test`: Cold-read confirmed every actor, pronoun, causal turn, and action resolves from speech alone.
  - `[pass]` `build-first`: Scene 1 opens on `"Kalau kamu rakit bak terpal kosong..."` with hands stretching the liner on a visibly bare yard corner.
  - `[pass]` `first-turn`: The initial basin is stocked and hits its first visible shortfall (overnight climbing over the bare rim) in Scene 1–2 (`00:04–00:22`).
  - `[pass]` `shortfall-before-fix`: Climbing escape (Scenes 1–2), soft-shell molting attack (Scene 4), and murky bottom / sluggish edge crowding (Scene 6) are each shown before their cause is named and before Fixes 1, 2, and 3 are installed.
  - `[pass]` `same-system`: Every upgrade stays anchored in the same backyard corner and framed tarpaulin basin through Scene 9.
  - `[pass]` `final-job`: Scene 8 harvests by opening the built bottom drain valve and lifting the flow-through PVC pipe stack installed in Scene 5.
  - `[pass]` `event-map`: Nine construction, test, and consequence events carry ~112.2 predicted seconds, with every finished feature actively installed by `"kamu"`.
  - `[pass]` `closing-lines`: Scene 9 ends with `"Selamat, kamu sudah punya kolam lobster air tawar sendiri, lengkap dengan bibir penahan, rumah pipa, dan kuras dasar."` followed by `"Habis ini, apa lagi yang mau kamu bikin di halaman?"` (consecutive `"bikin di halaman"`, no intro, no follow prompt).
  - `[pass]` `closing-signature`: Scene 9 holds `"bikin di halaman"` in `#FFD44D` to the end of the line and fades in `@bikindihalaman.id` beneath the caption.

## Script approval

On 2026-11-22 the user replied `"cocok --automation"` to the full script v1 and the question about proceeding to the visual storyboard. This is human approval of [SCRIPT.md](SCRIPT.md) v1 (275 spoken words, nine scenes). It does not approve the storyboard, the final look or the render; those are delegated below.

## Execution policy (2026-11-22)

The same reply carried bare `--automation`, which is active immediately.

```text
execution_policy: automation
automation_after: none
automation_state: active
human_review: none for subsequent work
pre_render_authorization: delegated by the user's --automation instruction
endpoint: content_package
delivery: package
```

- Human decisions retained as evidence: topic (`"setuju"`), hook 2 (`"2"`), script v1 (`"cocok"`).
- Delegated to the agent from here: visual storyboard acceptance, audio decisions, final look, the delivery render and packaging. The complete visual storyboard, including `video/boards/storyboard.png`, stays required before audio synthesis and animation.
- Retained under automation: technical and factual verification, the quality gate at storyboard, verification and export, and an independent review of the film before the delivery render. A gate verdict of `needs_human_review` keeps the human final-preview checkpoint.
- No external delivery is authorized. The publishing targets above are package destinations only.

## Storyboard verification (2026-11-22)

Agent-verified and accepted under the delegated automation policy. No human reviewed the board.

- HyperFrames 0.9.77 was initialized once in the empty `video/` folder with `--skip-skills`. [Brief](video/BRIEF.md) · [spec](video/SPEC.md) · inherited [frame](video/frame.md) (board visual v2, same hash as the board file).
- Plan: [video/STORYBOARD.md](video/STORYBOARD.md), nine frames, 112 s estimated, each with `shot`, timed `reads` and `sound`. Shots run wide, close cutaway, medium cutaway, close cutaway, medium-wide, close cutaway, medium cutaway, medium-close, wide.
- Stills: nine 1080 × 1920 frames in [video/boards/stills/](video/boards/stills/), captured from the composition at 9.3, 19.9, 31.6, 42.1, 55.6, 69.8, 79.6, 94.9 and 111.6 s. Poses: 30 files in [video/boards/poses/](video/boards/poses/) (hook at 0, 1 and 3 s, then start, middle and end of every scene).
- Board: [HTML](video/boards/storyboard.html) and [PNG](video/boards/storyboard.png), 1760 × 2519, SHA-256 `f143b583217eed2e6617e0f90b03d123f0ff838e691bd9d635d1760221e5e1ed`. Chromium loaded all 39 images with nonzero size, in order s01 to s09, DM Sans ready, no clipped text, no page errors, no horizontal overflow at 1760 or 390 px. [Browser evidence](video/verification/storyboard-browser.json)
- Gate: `passed` at `--stage storyboard`, nothing to disclose. [Verdict](video/verification/quality-gate-storyboard.json)
- HyperFrames `check`: 0 errors. Three warnings kept on purpose: `film_silent` (no narration yet), `outside_safe_zone` on the caption (the board places captions at y=1392), `timeline_track_too_dense` (60 caption groups share the one captions track).
- Looked at: the saved PNG and all nine stills at full size, plus contact sheets across every scene. Repaired while posing: the keeper's arm now enters from an upper corner instead of dropping as a vertical bar; the gutter is drawn as cement after it read as a log; a moon replaced a dark disc; the glare bands stay inside the tank; the young crayfish leave the bucket instead of appearing above the yard; the harvest tub sits clear of the gutter.
- Weak points carried into assembly: the crayfish are small in both wide shots (scenes 1 and 9); in scene 7 the second animal perched on the brick reads awkwardly; scene 6 relies on the brown wash and the tilted animal to say "cloudy and sluggish".
- Scenes already hold draft timelines on the estimated timing, so the stills are frames of the real compositions. Frame status stays `built`; they become `animated` once retimed to the measured narration.
- Routine choices: caption groups were re-broken to about five words (60 groups) from the longer lines in `SCRIPT.md`, wording unchanged; the first caption word is on screen at frame 0; the closing handle uses `@bikindihalaman.id`.
- No preview server was started; `preview --status` reports not-running for this project.

## Audio preparation and blocker (2026-11-22)

- Decisions: narration `use` (Pribs, `eleven_v4`), BGM `none` (board contract), SFX `use` (contact, pour, drain and bubbling cues on visible actions). `sound_design.json` waits for measured timing.
- [video/audio_request.json](video/audio_request.json) holds the full narration as one `narration` line in nine paragraphs with delivery tags. The voice resolves from the board (`boards/budidaya-di-halaman/AUDIO.json`, `5g0yKK2JwTRka0IG61Hh`). With tags removed the text equals the approved narration, 275 words; the POV check recorded under Script check covers this wording.
- `narration.py --check` returns `awaiting_mcp`, request `03181ba707f6a7ac7a0df5aba5b0e8a8a4a16f7c65f63961ede18c22cbee43a4`, no cache hit. The prepared call is `creative_generate_speech` with `model_id: eleven_v4`, the board voice, the tagged prompt and `generations_count: 1`.
- **Blocked at that point (resolved below):** this session has no ElevenLabs MCP connection. Connected servers are trypost, context7, markitdown, playwright, blender, jina and Roblox_Studio; an `elevenlabs` server is configured for Codex only. No speech was requested and no other provider was used, as the audio contract requires MCP synthesis.
- The bundled media-use effects are interface sounds (clicks, pops, whooshes); pour, drain and bubbling cues need the board's earlier production assets or media-use retrieval once timing is known.

## Narration through the ElevenLabs CLI (2026-11-22)

- The user replied "gunakan elevenlabs cli". This is an explicit episode-level override of the MCP-only synthesis route; provider, model and voice are unchanged (ElevenLabs, `eleven_v4`, Pribs `5g0yKK2JwTRka0IG61Hh` from the board).
- One take, no retry: `@elevenlabs/cli` 1.12.2, `text-to-speech convert_with_timestamps`, `mp3_44100_128`, `language_code: id`, the tagged text from `audio_request.json`. [Run receipt](video/audio_cli_run.json). The account had 4,321 characters left before the call and 2,325 after.
- Take: 102.88 s, SHA-256 `d7d91ab9a9bf1e674da6927d72c7cada179a2cc8ce1dc08c28e17641be5386d5`, cached under `video/.media/audio/voice/` with the provider's native character alignment. `narration.py` returns `ready` with 275 words, identical to the approved script. The cache receipt records `transport: elevenlabs_cli`; it carries no MCP flow IDs.
- Listening: unavailable. Stand-in check: a local Whisper large-v3 transcript returns the 275 script words with spelling variants only and no delivery tag read aloud. [Transcript check](video/verification/narration-transcript-check.json). Word starts differ from the native alignment by a median 0.2 s, at most 0.7 s.

## Assembly (2026-11-22)

- [place_audio.py](video/place_audio.py) keeps every speech sample, inserts 0.35 to 0.9 s of silence inside eight measured quiet gaps, and puts each scene cut on an integer frame with at least 320 ms of quiet either side. Film length 109.066667 s, 3,272 frames. First sentence ends at 4.08 s. [Timing](video/timing.json) · [boundaries](video/audio_boundaries.json) · [captions](video/captions.srt)
- Scene beats hang on anchor words; all nine scenes play their reads as motion and frame status is `animated`. 60 caption groups follow the native word times.
- Sound: narration `use`, BGM `none`, SFX `use` with ten contact and pull cues from the bundled media-use library. Pouring, draining, bubbling and the splash are silent on purpose: the library has no water sounds and generating effects was not requested. [Plan](video/sound_design.json)

## Verification and final preview (2026-11-22)

- HyperFrames `check`: 0 errors; kept warnings are the caption below the platform safe line and the dense captions track.
- Draft proof: [video/verification/proof.mp4](video/verification/proof.mp4), SHA-256 `7c8b3baac561cf545b8735f46b7fda9da9e518254b93fe94724b4b08a4cbcf28`, 109.07 s, 1080 × 1920, 30 fps, H.264 + AAC, −13.4 LUFS, −1.6 dBTP. Scene cuts are silent in the proof; ten cues match their placed times.
- Gate at `--stage verification`: **`needs_human_review`**. Disclosed: `independent_review: unavailable` and `listening: unavailable`. Every measured check passes. [Verdict](video/verification/quality-gate-verification.json) · [review](video/REVIEW.md)
- Independent review: a fresh-context sub-agent was started but could not open images, so no reviewer other than the author has judged the picture. Its three document-based notes are folded into the open P1 list in the review.
- Weakest shot: s07. Open P1 notes: s07 perched animal, s04 overlapping cluster, s09 pipes returning after the harvest, small animals in both wides, s06 thin read of "oxygen thins". No P0.
- Under the automation policy this is the one retained human pause. No delivery render has been made; `exports/` does not exist.

## Managed preview

Pipeline-owned preview for `productions/kolam-lobster-air-tawar/video`, started by this run after `preview --status` reported not-running: PID 32296, port 3002, http://127.0.0.1:3002/#project/video (HTTP 200, PID confirmed as the listener). Was held for the human final-preview review. Release was done with `npx --yes hyperframes@0.9.77 preview --stop --json` from `video/` after the review and the delivery render, then confirm status and that the port is free.

## Final review, export and package (2026-11-22)

- The user reviewed the final preview and replied "cocok", then "cocok dan render di speed 1.25x". `video/REVIEW.md` records `independent_review: human`, `listening: human`; the verification gate reran as `passed`. The five P1 notes stay open by that acceptance.
- Delivery render: `video/verification/master-24fps.mp4` at delivery quality and 24 fps (2,618 frames, every frame an exact composition frame). Scene-cut silence and all ten effect cues verified on this 1x master. Its frames were restamped to 30 fps without re-encoding and the audio time-stretched 1.25x (pitch kept): [exports/kolam-lobster-air-tawar-1.25x.mp4](exports/kolam-lobster-air-tawar-1.25x.mp4), 87.27 s, 1080 × 1920, 30 fps, −13.5 LUFS, −1.4 dBTP, full decode clean, SHA-256 `3def57575da24bbeaf3d663854c1a02ac81a7e4321a97f4ee80bbc59efcf4006`. Ten frames across the file were inspected.
- **Export gate: `failed` on the 1.25x file.** `film-format`: 87.27 s against the 109.07 s composition and the board's 90 s minimum. `motion-floor`: the gate reads scene windows from the 1x timing, so its late-scene result is an artifact of the speed change. This follows from the requested speed; no 1x delivery file was requested or made.
- Sidecar captions rescaled to 1.25x and a cover were written to `exports/`. [CONTENT_PACKAGE.md](CONTENT_PACKAGE.md) is written and states the deviation.
- Preview PID 32296 on port 3002 stopped with `preview --stop`; status is not-running and the port is free.

## Delivery decision (2026-11-22)

The user replied "tetap 1.25x": the 87.27 s file is the accepted delivery. This is a user-directed deviation from the board's 90 s minimum; the export gate verdict stays `failed` on `film-format` and is not overridden or rerun. All other export evidence above stands.

## Drafts on Trypost (2026-11-22)

- The user asked: "lanjut upload draft ke akun yang tertaut di board". Read as an explicit target selection of the board's current account list, which now has three accounts; the Facebook page `Bangun Di Halaman` (`01a2036c-5179-70c6-b908-25118446326d`) was added to the board after this production's two-account snapshot. Targets for this delivery: Instagram, YouTube, Facebook.
- Preflight: workspace `Admin's Workspace` matches, the caller publishes directly, all three accounts are `connected` with matching IDs and handles, no earlier post for this episode exists. The export (SHA-256 `3def5757…f4006`) was uploaded once and reused by media ID.
- Three drafts, one per account, each observed as `draft` with the video attached (87.28 s on the server): Instagram reel `01a20419-f9c9-70cb-b653-43cd6afff584`, YouTube Short `01a2041a-2c3d-71a1-a25c-eb6b285d44cf` (title set), Facebook reel `01a2041a-42d8-7208-93eb-a6a371fe6d7d` (Instagram caption reused; the package has no Facebook copy). Receipt: [PUBLISHING.json](PUBLISHING.json).
- Left unset: schedule, YouTube privacy and category (provider defaults: public, People & Blogs), AI-content disclosure flags, custom cover. Nothing is scheduled or published.

## Current state

- `stage: publishing`
- `status: complete` (requested delivery: draft)
- `next_action: none until the user asks to schedule or publish the drafts.`
