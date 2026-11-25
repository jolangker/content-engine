# Kolam Lele di Halaman

## Brief

- `topic_selection: user`. On 2026-11-24, after reviewing a 10-topic shortlist for `budidaya-di-halaman`, the user explicitly chose **ternak lele** as the topic for a new production.
- **Board:** `budidaya-di-halaman`, revision 8 (Editorial v8 / Visual v4). Inherit its [direction](../../boards/budidaya-di-halaman/DIRECTION.md), [editorial framework v8](../../boards/budidaya-di-halaman/EDITORIAL.md), [visual specification v4](../../boards/budidaya-di-halaman/frame.md), and [production contract](CONTRACT.json).
- **Contract snapshot:** [CONTRACT.json](CONTRACT.json) copied from `boards/budidaya-di-halaman/CONTRACT.json` (`editorial v8 / visual v4`, SHA-256 `8def1552948e1124b373e301f36388fd33f5ad1f2bae72b13b2575592ac0d0ca`), validated via `episode_qa.py --contract`.
- **Overlap check:** Checked `TRACKER.json` and `productions/`. Existing `akuaponik-lele-dan-kangkung` covers backyard aquaponics (gravel media bed of kangkung, biofilter cycling, bell siphon, and first kangkung cut). Existing `jejak-kotoran-kolam-nila` covers a Nile tilapia settling chamber. Existing `kolam-lobster-air-tawar` covers redclaw crayfish (escape rim, molting shelters, hanging aerator). This episode is a distinct standalone backyard catfish farming build (*ternak lele* in an above-ground tarp pond) following 7 distinct problem–improvement rounds through to a stable pond and first catfish harvest/weighing under Editorial v8.
- **Angle & planned event chain (pending hook confirmation):** Start on a bare yard corner, put up a simple above-ground tarp pond (~2 × 1 × 0.8 m, ~150–200 *Clarias gariepinus* fingerlings) without safeguards, then evolve the exact same pond through 7 compact problem–improvement rounds (6–10 s each at 1x) with varied triggers: (1) liner puncture/water drop → pad frame & base; (2) midday heat stress/surfacing → shade net (*paranet*); (3) heavy rain overflow → screened overflow pipe; (4) muddy footpath runoff → route pipe to adjacent garden bed; (5) leftover feed/bottom sludge clouding water → bottom drain valve + measured feeding; (6) night predator tracks/missing fish → top mesh cover; (7) size disparity/cannibalism → grading with scoop into netted divider/second zone. Follow with a stable-system check, a hanging-scale monetization scene (`15 kg × Rp23.000 = Rp345.000`, `estimasi harga pasar / Nov 2026` from FishInfo Jatim), and the closing wide view + signature question + 0.5 s thumbnail end card. See [SOURCES.md](SOURCES.md).
- **Format & audio defaults (inherited from board):** 9:16 vertical illustrated cutaway (1080 × 1920), authored at **90–112.5 s at 1x** and delivered at **1.25x** speed (72–90 s delivered) with pitch kept. Language: conversational Indonesian (`"kamu"` referring singly to the backyard keeper). Voice: ElevenLabs **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh`, `eleven_v4`), BGM `none`, SFX `use` (scene-linked contact/water/rain/net cues).
- **Word budget note:** Local workspace clone has no measured narration audio files cached for `5g0yKK2JwTRka0IG61Hh` (`episode_qa.py --budget` requires a fresh take to measure pace); plan initially at 2.4–2.6 words/second (~230–265 words for 90–112.5 s 1x, consistent with prior Pribs episode `kolam-lobster-air-tawar` at 2.61 wps) and re-budget after the first take.
- **Execution & review policy:**
  - `execution_policy: human_review`
  - `endpoint: content_package`
  - `delivery: package`
  - Retained human checkpoints: hook selection, script review, visual storyboard review, and final preview.

## Publishing targets

```yaml
publishing_targets:
  source: board
  board_accounts_file: boards/budidaya-di-halaman/ACCOUNTS.json
  board_accounts_sha256: 098943ff65eaf188fd7ea3a1b4e769e0729f78269e896a789af8e13c624e1d94
  accounts:
    - provider: trypost
      workspace_id: 01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37
      workspace_name: Admin's Workspace
      social_account_id: 01a2022d-bc57-71d8-9217-6e0319cb6c03
      service: instagram
      handle: bikindihalaman.id
    - provider: trypost
      workspace_id: 01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37
      workspace_name: Admin's Workspace
      social_account_id: 01a202dc-0e4a-72ae-bec8-589ab7f90045
      service: youtube
      handle: bikindihalaman_id
    - provider: trypost
      workspace_id: 01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37
      workspace_name: Admin's Workspace
      social_account_id: 01a2036c-5179-70c6-b908-25118446326d
      service: facebook
      handle: Bangun Di Halaman
```

## Research and hook review

Research verified practical tarp-pond construction, optimal *Clarias gariepinus* temperature (25–30 °C), rain overflow and effluent routing, bottom sludge/ammonia management, predator netting, periodic grading against cannibalism, backyard harvest yield (~15 kg from ~150 fingerlings in 2.5–3 months at 7–9 fish/kg), and dated Indonesian market pricing (FishInfo Jatim 24 Nov 2026: Rp23.163/kg; Bantul April 2026: Rp25.000/kg). All claims and qualifications are mapped in [SOURCES.md](SOURCES.md).

Hook options v1 follow Editorial v8's four-slot pattern (`Kalo kamu {aksi pertama}, {konjungsi temporal} kamu {aksi kedua}, kamu sudah punya {sistem}. Tapi {masalah}.`), avoid repeating the previous published episode's opening verb (`rakit`), and fit within the contract's `10.0 s` first-sentence and `12.0 s` `"Tapi"` turn ceilings. *(No board performance analysis exists yet to weigh historical hook mechanisms.)*

### Option 1 (Recommended) — Construction surprise: overnight waterline drop (bamboo frame)
- **Mechanism:** Immediate physical construction failure (visible waterline drop by morning) that sets up a natural chronological escalation across 7 rounds.
- **Spoken line (25 words; sentence 1 = 17 words ≈ 6.5–7.1 s; `"Tapi"` ≈ 7.2 s):**
  > “Kalo kamu ikat rangka bambu di sudut halaman, terus kamu bentang terpal dan isi air, kamu sudah punya kolam lele. Tapi besok paginya airnya surut sejengkal.”
- **Frame 0:** Bare warm-clay yard corner with bamboo poles ready; within 0.25 s hands tie the frame upright, drape the dark liner, fill clear water and catfish fingerlings, then a quick night-to-morning sky shift reveals the waterline dropped a handspan.
- **On-screen line:** Captions (46 px, 2 lines max) revealing word-by-word: `Kalo kamu ikat rangka bambu di sudut halaman,` / `terus kamu bentang terpal dan isi air,` / `kamu sudah punya kolam lele.` / `Tapi besok paginya airnya surut sejengkal.`
- **Promise:** Shows why the hasty pond loses water and tracks 7 visible upgrades through to a steady pond and weighed first catfish harvest.

### Option 2 — Biological mystery: midday heat stress at the surface (wood-stake frame)
- **Mechanism:** Observable fish distress behavior (catfish hanging/gasping at midday) triggering curiosity about shallow exposed backyard ponds.
- **Spoken line (26 words; sentence 1 = 18 words ≈ 6.9–7.5 s; `"Tapi"` ≈ 7.6 s):**
  > “Kalo kamu tancap patok kayu di pojok rumah, lalu kamu pasang terpal dan tebar benih, kamu sudah punya kolam lele. Tapi pas tengah hari lelenya megap-megap di atas.”
- **Frame 0:** Bare sunny yard corner; within 0.25 s wooden stakes are driven in, liner and water go in with fingerlings, then harsh overhead midday light drives catfish vertically up to the surface.
- **On-screen line:** Captions: `Kalo kamu tancap patok kayu di pojok rumah,` / `lalu kamu pasang terpal dan tebar benih,` / `kamu sudah punya kolam lele.` / `Tapi pas tengah hari lelenya megap-megap di atas.`
- **Promise:** Explains overheating in an unshaded yard pond and builds through shading, rain control, drainage, predator netting, and grading to the first harvest.

### Option 3 — Weather crisis: heavy night rain overflowing a round wiremesh pond
- **Mechanism:** Sudden external weather crisis (rain overflow threatening fish escape) using a circular wiremesh pond silhouette.
- **Spoken line (26 words; sentence 1 = 18 words ≈ 6.9–7.5 s; `"Tapi"` ≈ 7.6 s):**
  > “Kalo kamu bentuk pagar kawat melingkar di halaman, habis itu kamu lapis terpal dan isi bibit, kamu sudah punya kolam lele. Tapi pas hujan deras malamnya airnya meluap keluar.”
- **Frame 0:** Bare flat yard with rolled wiremesh; within 0.25 s the wire ring locks into a circle, circular tarp and water with fingerlings fill in, then a dark rainstorm lifts water over the rim.
- **On-screen line:** Captions: `Kalo kamu bentuk pagar kawat melingkar di halaman,` / `habis itu kamu lapis terpal dan isi bibit,` / `kamu sudah punya kolam lele.` / `Tapi pas hujan deras malamnya airnya meluap keluar.`
- **Promise:** Shows how a circular yard tarp pond gains overflow control, runoff routing, shading, bottom flushing, predator netting, and sorting through to the first weighed harvest.

**Recommendation:** Option 1. The sudden waterline drop is unmistakable even on mute in a flat side cutaway, uses a classic low-cost bamboo frame familiar to Indonesian viewers, and allows all 7 problem–improvement rounds to unfold in natural chronological order (leak → midday heat → rain overflow → footpath runoff → bottom sludge → night predator → cannibalism grading).

`hook_selection: user`. On 2026-11-24 the user selected **Option 2** (“opsi 2”). Its wording and wooden-stake tarp pond setup are carried verbatim into [SCRIPT.md](SCRIPT.md) v1.

## Script review

[SCRIPT.md](SCRIPT.md) v1 is built around Option 2 with 11 scenes (18 meaningful events: premature build hook, 7 distinct problem–improvement rounds, stable check, hanging-scale income scene, and closing wide shot + 0.5 s delivered thumbnail end card).

### Script check (v1)

- **Spoken word count & budget output:** **255 spoken words**. Local workspace has no cached audio for Pribs (`5g0yKK2JwTRka0IG61Hh`), so `episode_qa.py --budget` requires a first take to measure pace locally. Using both the fallback rate (`2.40 wps`) and Pribs's recorded pace in `kolam-lobster-air-tawar` (`2.61 wps`): predicted narration is `97.7–106.3 s`, predicted 1x film duration (including ~3.5 s visual holds/tag hold + `0.625 s` end card) is **`101.8–110.4 s`**, fitting the contract's `90.0–112.5 s` 1x window (`~81.5–88.3 s` delivered at 1.25x). Re-budget after the first narration take.
- **First sentence & `"Tapi"` turn:** Sentence 1 is **20 words** (predicted `7.7–8.3 s` ≤ `10.0 s` contract ceiling). `"Tapi"` begins at word 21 (predicted `~8.0–8.6 s` ≤ `12.0 s` contract ceiling).
- **Selected hook three parts (Option 2):**
  - *Spoken line:* “Kalo kamu tancap patok kayu di pojok rumah, lalu kamu pasang terpal dan tebar benih, kamu sudah punya kolam lele. Tapi pas tengah hari lelenya megap-megap di atas.”
  - *Frame 0:* Bare sunny yard corner with wooden stakes and folded tarp ready; stakes driven in at `0.25 s`, liner/water/fingerlings added, then harsh midday light brings catfish gasping to the surface.
  - *On-screen line:* 46 px max-2-line progressive captions matching the opening line.
- **Cold-read result & repairs:** Read all 255 spoken words standalone without headings or visual cues. `"kamu"` resolves cleanly to the single backyard keeper throughout; each paragraph states cause, action, and visible result independently of captions. Two ear-clarity repairs applied during drafting: (1) Round 2 clarified where the sacking goes (`alasi sekam dan lapisi rangkanya pakai karung`) and (2) Round 5 explicitly named flushing bottom sludge (`buang endapannya`) while avoiding the word `"stabil"` before Scene 9.
- **Contract judged rules (script scope):**
  - `hook-frame`: **pass** — Frame 0 opens on the bare yard corner and wooden stakes with action starting at `0.25 s` and 46 px phone-legible captions.
  - `pictures-alone`: **pass** — Every scene specifies visual sub-beats showing cause, added part, and tested outcome in sequence.
  - `event-density`: **pass** — All 11 scenes / 18 events introduce a distinct construction change, check, or result beyond captions.
  - `motion-variety`: **pass** — Shot plan alternates `wide` → `medium` → `close` → `medium` → `medium-wide` → `close` → `medium` → `close` → `wide` → `medium` → `wide` (no >2 identical consecutive shots).
  - `subject-scale` & `vessel-scale`: **pass** — Pond cutaway, fittings, and hanging scale are planned at ≥40% frame width with consistent yard landmarks.
  - `ear-test`: **pass** — Cold read passed after Round 2 and Round 5 ear-clarity edits; single `"kamu"` POV throughout.
  - `build-first`: **pass** — Hook fills all four Editorial v8 slots verbatim with ordinary punctuation, starts on a bare corner, puts the pond in use, and ends on observable gasping within time limits.
  - `shortfall-before-fix`: **pass** — 7 problem–improvement rounds after the hook (20–24 words / `7.7–10.0 s` each at 1x), one cause and one on-screen tested fix per round, across 7 different triggers (midday heat, liner puncture, heavy rain overflow, footpath runoff, bottom sludge, cat predator, cannibalism).
  - `same-system`: **pass** — Every added upgrade (paranet, sacking/husk padding, screened overflow, bed extension pipe, bottom drain valve, top net, interior net divider) stays visible on the same pond through Scene 11.
  - `final-job`: **pass** — Scene 9 shows the completed pond handling rain and feeding simultaneously before calling it stable.
  - `income-scene`: **pass** — Scene 10 weighs `15 kg` beside the finished pond with hanging price tag `15 kg × Rp23.000 ≈ Rp345.000` (`estimasi harga pasar / Nov 2026`, sourced from FishInfo DKP Jatim 24 Nov 2026), rounded spoken figures, ≥3 s 1x hold, no profit/payback claim.
  - `event-map`: **pass** — 18 events (within 15–19); every component enters on screen.
  - `closing-lines`: **pass** — Ends with congratulation naming the built pond + next-build question containing consecutive `"bikin di halaman"`; no intro or follow prompt.
  - `closing-signature`: **pass** — Holds yellow on `"bikin di halaman"`, fades in `@bikindihalaman.id`, hard cuts to `0.625 s` 1x (`0.5 s` delivered) thumbnail end card.
  - `reframing`: **pass** — Uses push-in cutaways for liner corner/sludge/grading, lateral move for bed pipe, and pull-out to wide for stable check and closing.

- **Revision v2 (2026-11-24):** User feedback on v1: *"kata tapi sangat berulang. coba variasikan agar lebih natural dan smooth"*. Kept `"Tapi"` only in the hook (Scene 1, preserving the Editorial v8 four-slot hook and `hook.turn` contract rule), and varied transitions across Rounds 2–7 and Scene 10 (`Besok paginya, airnya malah…`, `Begitu hujan deras turun,…`, `Masalahnya,…`, `Lama-lama,…`, `Suatu pagi, muncul…`, `Masuk bulan kedua, giliran…`, `Tiga bulan berjalan,…`). Word count is **254 words** (`tapi` count: 1; predicted 1x `101.4–110.0 s`, all contract checks and cold read pass cleanly).
- `script_approval: user` (2026-11-24: *"approve dan otomasi sampai upload draft"*).

## Active automation & delivery policy (activated 2026-11-24)

```text
execution_policy: automation
automation_after: script
automation_state: active
activating_decision: user approval of SCRIPT.md v2 (2026-11-24)
human_review: none for subsequent work
pre_render_authorization: delegated by the user's automation instruction ("approve dan otomasi sampai upload draft")
endpoint: publishing
delivery: draft
```

- **Preflight (2026-11-24):**
  - ElevenLabs transport: `elevenlabs_api` (`narration.py --check-api` OK, tier `free`, 0/10,000 chars used; `elevenlabs` CLI not logged in).
  - Trypost transport: `api` (`trypost.py check` OK on `Admin's Workspace` `01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37`; all 3 inherited accounts verified `connected`: `instagram:bikindihalaman.id`, `youtube:bikindihalaman_id`, `facebook:Bangun Di Halaman`).

## Storyboard verification (agent-verified under active automation)

- **Artifacts:**
  - [video/STORYBOARD.md](video/STORYBOARD.md) — 11 frames (`105.625 s` estimated 1x), 18 events, shot variety max run 1, `storyboard_lint.py --strict` passed (0 errors).
  - [video/boards/stills/](video/boards/stills/) — 11 styled scene stills rendered from HyperFrames (`compositions/s01.html`..`s11.html` + `assets/catfish-world.js`).
  - [video/boards/poses/](video/boards/poses/) — 25 poses (`hook-0.0s.png`, `hook-0.8s.png`, `hook-3.0s.png` plus start/end poses for Frames 01–11).
  - [video/boards/storyboard.html](video/boards/storyboard.html) & [video/boards/storyboard.png](video/boards/storyboard.png) (`1600×6869`, 36/36 images loaded, 0 broken).
- **Visual inspection:** Inspected contact sheets, `frame-04-at-44.4s.png`, `11-b-end.png`, and full `storyboard.png`. Fixed 3 framing/craft items before gating: (1) adjusted `s03` and `s05` zoom anchors so the left stake corner and right vegetable bed sit cleanly in frame, (2) corrected `s05` overflow pipe downward gravity elbow into the bed, (3) moved harvest basin below the pipes in `s11` and matched thumbnail top sky fill `#CFD9B6`.
- **Gate verdict:** `episode_qa.py --stage storyboard` **passed** (`video/verification/quality-gate-storyboard.json`, `disclose: []`).

## Audio stage (resolved & verified)

- **Blocker resolved (2026-11-24):** Board default voice **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh`) returned HTTP 400 (`voice_not_found`, `free_users_allowed: False`) on the configured free-tier `ELEVENLABS_API_KEY`. The user explicitly authorized ElevenLabs **Roger** (`CwhRBWXzGAHq8TQ4Fs17`) as an `episode_override` (`"Roger"`).
- **Narration synthesis (1 take, `elevenlabs_api`, `eleven_v4`):** [video/.media/audio/voice/narration-aa05fa17fa4d8ebcb954.mp3](video/.media/audio/voice/narration-aa05fa17fa4d8ebcb954.mp3) (`103.889 s`, exact `254` words; sentence 1 ends `6.921 s <= 10.0 s`; `"Tapi"` turn at `7.194 s <= 12.0 s`; recorded in [video/audio_request.json](video/audio_request.json) and [video/audio_meta.json](video/audio_meta.json)).
- **Quiet boundary placement & normalization:** Placed via `audio_boundaries.place()` (0.22 s pauses on S01–S09, 2.40 s post-S10 pause giving `3.148 s >= 3.0 s` 1x price-tag hold) and normalized once to `-14.0 LUFS / -1.5 dBTP` at [video/assets/audio/narration.wav](video/assets/audio/narration.wav) (`108.270 s`, total 1x composition `109.458333 s` = 2627 frames @ 24 fps, `end_card_start = 108.833333 s`, `end_card_duration = 0.625 s`). Verified via `audio_boundaries.py` (`10/10` boundaries quiet).
- **Sound design & listening:** `bgm: none`; `12` subtle scene-linked bundled `media-use` SFX cues in [video/sound_design.json](video/sound_design.json) (credits in [video/assets/audio/CREDITS.md](video/assets/audio/CREDITS.md)). `listening: agent` — natively listened via `view_file` to the raw narration take, the 1x proof mix (`proof-mix.mp3`), and the 1.25x delivered audio stream (`delivery-mix-1.25x.mp3`).

## Verification & independent review (agent-verified under active automation)

- **Independent jury audit pass 1 (`research` subagent `3f04e9ba2965ceb2d18401d968507d92`):** Identified 6 P0 visual continuity/reframing/typography blockers (`s10` bare-pond regression, `s07/s09/s11` closed U-loop pipe, `s05` missing lateral pan & vegetable bed, `s03` missing close-up push, `s11` unverified closing-signature yellow hold & low-contrast handle, `s11` end-card word spacing & bright sky/sun collision) and P1 polish items.
- **Fixes applied & re-audit pass 2 (`3f04e9ba2965ceb2d18401d968507d92`):** Fixed all 6 P0s and high-impact P1s (`assets/catfish-world.js`, `compositions/s11.html`, `compositions/captions.html`, `sound_design.json`, `SCRIPT.md` metadata, `STORYBOARD.md`) — unified open-ended spouts, 2.0–2.15× cutaway pushes (`s03/s06/s08`), lateral pan (`s05`), full completed 7-upgrade pond in `s10`, balanced 2-line captions with verified yellow `"bikin di halaman?"` + high-contrast `@bikindihalaman.id` (`108.45s`), and seamless dusk-slate end card (`109.1s`). Re-audit issued **APPROVE FOR DELIVERY RENDER (SHIP)**: **16/16 judged rules pass**, **0 open P0s**, all **7 rubric dimensions 7–8/10** (`style_fidelity: 8`, `concept_wow: 7`, `motion_craft: 7`, `design_typography: 8`, `finish_texture: 7`, `sound_sync: 7`, `technical: 8`). Recorded in [video/REVIEW.md](video/REVIEW.md) (`composition_sha256: 7e8412863b402056c5c867a4d03212593345cdf8af9efdfd538516f59389d527`).
- **Verification gate:** `episode_qa.py --stage verification --dom-lint` **passed** (`disclose: []`) — [video/verification/quality-gate-verification.json](video/verification/quality-gate-verification.json) (`proof.mp4` 25.2 MB, 10/10 quiet boundaries, 12/12 SFX matched at `offset_s: 0.0`, median vocal-band SNR `29.78 dB`, `dom_lint` 0 G5/readcheck fails).

## Export & packaging

- **1x Delivery master:** [video/verification/master-24fps.mp4](video/verification/master-24fps.mp4) (`33.9 MB`, `109.458 s`, 2627 frames @ 24 fps, `--quality delivery`); verified `audio_boundaries.py` (`10/10` passed) and `sound_design.py` (`12/12` passed, median vocal-band SNR `29.78 dB`).
- **Delivered 1.25x video:** [exports/kolam-lele-di-halaman.mp4](exports/kolam-lele-di-halaman.mp4) (`18,701,174` bytes / `18.70 MB`, `87.567 s` = `87567 ms`, `1080 × 1920 @ 30 fps`, pitch-kept `atempo=1.25`, two-pass `loudnorm`, `−14.05 LUFS` integrated / `−2.8 dBTP` true peak, SHA-256 `2701a63156487fbedb7cdf24bc7724725c2c1e08a17eb9546d0f1be413f64410`). Listened natively to the 1.25x audio stream (`delivery-mix-1.25x.mp3`): speech remains natural and easy to follow; inspected decoded frames (`delivered-s10.png`, `delivered-endcard.png`).
- **Delivered thumbnail & captions:** [exports/thumbnail.png](exports/thumbnail.png) (`159,986` bytes, SHA-256 `f30ce9388a5e27ef0995a6365fd9e0a0781bb8d8620e9f4776e2c67e34d0a28f`), [exports/kolam-lele-di-halaman.srt](exports/kolam-lele-di-halaman.srt) (`54` cues, SHA-256 `57d58fa29d986545a5bb4a7ec4dd2c02789c34520effb7295921efdcc2bb51b7`).
- **Export gate:** `episode_qa.py --stage export` **passed** (`21/21` checks passed, `disclose: []`) — [video/verification/quality-gate-export.json](video/verification/quality-gate-export.json).
- **Content package:** Shared Editorial v8 package written to [CONTENT_PACKAGE.md](CONTENT_PACKAGE.md) (`Bikin Kolam Lele di Halaman dari Patok Kayu dan Terpal`, shared copy/hashtags/keywords across all 3 accounts).

## External delivery (Trypost drafts — completed)

- **Transport:** `api` (`trypost.py`, `Admin's Workspace` `01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37`).
- **Receipt:** [PUBLISHING.json](PUBLISHING.json) (schema v2; export SHA-256 `2701a63156487fbedb7cdf24bc7724725c2c1e08a17eb9546d0f1be413f64410`; no credentials or upload tokens persisted).
- **Per-channel verified results (all observed `status: draft` via `GET /posts/{id}`):**
  1. **Instagram `@bikindihalaman.id`** (`01a2022d-bc57-71d8-9217-6e0319cb6c03`, `instagram_reel`): post ID `01a21040-a8d1-7315-bf63-bd462e9286af`, media ID `01a21042-4979-70f5-86a9-b5c9c352f985`, `cover_offset_ms: 87317` (`87567 − 250`), status **`draft`**.
  2. **YouTube `@bikindihalaman_id`** (`01a202dc-0e4a-72ae-bec8-589ab7f90045`, `youtube_short`): post ID `01a21042-727f-70ff-bd9f-1dd5713aed70`, media ID `01a21042-70c5-7057-abd2-1ae56aecaf76`, `meta.title: "Bikin Kolam Lele di Halaman dari Patok Kayu dan Terpal"`, status **`draft`**.
  3. **Facebook `Bangun Di Halaman`** (`01a2036c-5179-70c6-b908-25118446326d`, `facebook_reel`): post ID `01a21042-9b0a-719e-af98-a69133972e51`, media ID `01a21042-98c2-725d-8e57-abf669e0b711`, status **`draft`**.
- **Stage status & next action:** `stage: publishing`, `status: complete` (requested `draft` endpoint satisfied across all 3 inherited accounts; posts remain in `draft` and are NOT live).
- **User acceptance (`final_delivery_approval: user`, 2026-11-24):** User explicitly approved the delivered video, package, and 3 Trypost drafts (*"approve. lu boleh update statusnya"*). Status confirmed at `stage: publishing`, `status: complete` in [TRACKER.json](../../TRACKER.json); Trypost posts remain `draft` as requested. **Next action:** upload [exports/thumbnail.png](exports/thumbnail.png) manually for YouTube Shorts and Facebook Reels when scheduling/publishing, and run a performance snapshot after publication.


