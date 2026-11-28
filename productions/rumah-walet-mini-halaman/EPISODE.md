# Bikin Rumah Burung Walet Mini di Halaman

## Brief

- **Slug:** `rumah-walet-mini-halaman`
- **Topic selection:** `topic_selection: user`. On 2026-11-28, after reviewing a 10-topic *sarang burung walet* shortlist for `budidaya-di-halaman`, the user replied `"setuju"` accepting recommended Candidate #1: building a backyard mini swiftlet house (*Rumah Burung Walet / RBW mini*) from a bare yard corner through 7 single-cause problem–improvement rounds (light baffle, elbow vent pipes, floor water basin, grooved wood nesting planks, calm indoor nesting audio, smooth zinc anti-gecko frame, fledgling-safe midday harvest) to a stable colony and first weighed raw-nest harvest.
- **Board:** `budidaya-di-halaman`, revision 10 (`editorial v9 / visual v5`, status `approved`), explicitly selected via `--board=budidaya-di-halaman`. Inherit [direction](../../boards/budidaya-di-halaman/DIRECTION.md), [editorial framework v9](../../boards/budidaya-di-halaman/EDITORIAL.md), [visual specification v5](../../boards/budidaya-di-halaman/frame.md), [organic SFX kit](../../boards/budidaya-di-halaman/assets/sfx/manifest.json), and [production contract](CONTRACT.json).
- **Contract snapshot:** [CONTRACT.json](CONTRACT.json) copied verbatim from `boards/budidaya-di-halaman/CONTRACT.json` (`editorial v9 / visual v5`, SHA-256 `6681a52a9464efab8b2c846a0b08b731e06fde1e9a947e9772b333d54eac9626`), validated via `episode_qa.py --contract` (18 effective judged rules, 0 overrides).
- **Overlap check:** Inspected `TRACKER.json` and `productions/` (all 14 existing `budidaya-di-halaman` productions). Existing episodes cover fish ponds, crayfish, swamp eels, aquaponics, minapadi, betta mini-farm, BSF maggots, container crops, laying duck coop, and elevated kampung chicken coop. Zero episodes cover edible-nest swiftlets (*Aerodramus fuciphagus*), swiftlet houses, light-baffle *void/lar* architecture, grooved nesting planks, or raw bird's nest harvesting.
- **Audience & POV:** Indonesian-speaking general viewers curious about backyard cultivation, addressed in natural conversational Indonesian as `"kamu"` (the sole builder/keeper at one consistent yard corner). Honest about wild colonization (location/flight-path dependent, months to a year+ before first harvest); gross collector estimate only with zero profit or payback promise.
- **Format & duration target (inherited from board):** Vertical 9:16 (`1080 × 1920`), 4-plane 2.5D illustrated living backyard cutaway, authored at **90–112.5 s at 1x** (24 fps master restamped to 30 fps at **1.25x** = **72–90 s delivered**, pitch kept), closing with an exact-match thumbnail end card (`0.625 s` 1x / `0.5 s` delivered).
- **Audio plan:**
  - Narration: `use` — `eleven_v4` on `elevenlabs_api` (Starter tier verified via `narration.py --check-api`, `28,709` chars remaining). Board default **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh`) from `boards/budidaya-di-halaman/AUDIO.json` confirmed present in `my voices` on this Starter API key; resolved via `resolve_voice(root, board="budidaya-di-halaman")`.
  - BGM: `none` for the entire episode.
  - SFX: `use` — board Visual v5 organic SFX library (`boards/budidaya-di-halaman/assets/sfx/manifest.json`) with event-locked foley and low-gain diegetic condition beds.

## Execution, review & delivery policy

```text
execution_policy: automation
automation_after: topic
automation_state: active
activating_decision: user accepted Candidate #1 ("setuju" on 2026-11-28)
human_review: none for subsequent work
pre_render_authorization: delegated by the user's --automation=after-topic instruction after topic acceptance
endpoint: content_package
delivery: package
```

## Publishing targets

Inherited full default account list from `boards/budidaya-di-halaman/ACCOUNTS.json` (local snapshot for shared `CONTENT_PACKAGE.md` destinations and `@bikindihalaman.id` closing-signature handle; no external upload or publishing authorized under default `delivery: package`):

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

## Topic discovery summary (`topic_selection: user`)

Presented 10 distinct backyard *sarang burung walet* candidates (no board performance analysis exists yet): (1) Rumah Burung Walet mini mandiri di sudut halaman *(recommended)*, (2) RBW mini dinding GRC & baja ringan, (3) sulap loteng/dak rumah jadi kamar walet, (4) RBW mini papan kayu kampung, (5) RBW mini tenaga surya, (6) menara void sempit lahan 2×3 m, (7) RBW sistem kolam bawah & kabut, (8) hybrid RBW di atas kolam ikan, (9) RBW + pojok serangga alami, (10) RBW + meja cuci sarang tanpa pemutih. On 2026-11-28, the user replied `"setuju"` accepting Candidate #1, locking the topic and activating `--automation=after-topic`.

## Research and hook selection (agent-selected under active automation)

Research verified all 9 claims (`C1–C9`) against PUSTAKA BPPSDMP Kementerian Pertanian RI (2023 & 2024), Markas Walet technical & price updates (Nov–Dec 2024 & 03 Aug 2026 national collector benchmark `Rp 8.310.000/kg`), Dunia Walet (2023), PT Rumah Burung Indonesia Jaya (Dec 2025), Jurnal Teknik Sipil UAJY (2013), Jurnal Peternakan Lingkungan Tropis UNMUL (2021), and JSSM Universiti Malaysia Terengganu (2021) in [SOURCES.md](SOURCES.md).

Hook options v1 follow Editorial v9's four-slot pattern (`Kalo kamu {aksi pertama}, {konjungsi temporal} kamu {aksi kedua}, kamu sudah punya {sistem}. Tapi {masalah}.`), avoid repeating recent episodes' first verbs and connectors (`minapadi`: `hamparkan`/`kemudian`; `ayam-kampung`: `dirikan`/`begitu`; `gurame`: `lingkarkan`/`lalu`), keep Sentence 1 under `10.0 s` and `"Tapi"` under `12.0 s`, and stay within `SOURCES.md`. *(No board performance analysis exists yet.)*

1. **Option 1 (Selected — agent choice under active automation) — Instant drop-in-and-flee mystery (light-glare behavioral rejection):**
   - *Mechanism:* Counter-intuitive habitat clash — viewers assume a brick box with an entry hole and bird calls will attract swiftlets to nest immediately, so seeing birds swoop in and bolt straight back out sparks instant curiosity about cave darkness (`< 1 lux`) and triggers the signature *sekat gelap* cutaway fix in Round 1.
   - *First verb / connector:* `susun` / `setelah itu`
   - *Spoken line (25 words; Sentence 1 = 19 words ≈ `7.4–7.9 s ≤ 10.0 s`; `"Tapi"` at word 20 ≈ `7.8–8.3 s ≤ 12.0 s`):*
     > “Kalo kamu susun dinding bata berlubang di halaman, setelah itu kamu putar suara panggil, kamu sudah punya rumah walet. Tapi burungnya cuma mampir lalu kabur.”
   - *Frame 0 & `<1.0 s` motion:* Bare warm-clay yard corner with stacked concrete bricks, roof planks, and a calling tweeter ready; at `0.25 s` hands lay the compact two-level brick tower with an upper entry hole, mount the calling sound, and watch swiftlets swoop in, encounter bright sunlight flooding the empty room, circle once, and bolt back out.
   - *On-screen line:* 46 px DM Sans 800 progressive captions (max 2 lines); thumbnail/cover promise **Bikin rumah** / **walet mini** (yellow on **walet mini**).
   - *Promise:* Reveals why an open brick room fails for cave-dwelling swiftlets and builds the exact same yard tower through 7 real microclimate, perch, acoustic, pest, and harvest upgrades to a stable colony and first `100 g` harvest.
2. **Option 2 — Midday oven shock (thermal failure):**
   - *Mechanism:* Thermal discomfort contrast — shows birds abandoning a closed brick house as afternoon sun heats it past `30 °C`.
   - *First verb / connector:* `bangun` / `habis itu`
   - *Spoken line (25 words):* “Kalo kamu bangun ruang bata tertutup di halaman, habis itu kamu buka lubang masuk dan putar suara, kamu sudah punya rumah walet. Tapi siangnya ruangnya panas sekali.” *(Skips the signature cave-darkness light-baffle architecture in Round 1.)*
3. **Option 3 — Slippery-claw setback (biological morphology puzzle):**
   - *Mechanism:* Unexpected avian anatomy reveal — shows entering swiftlets unable to cling to smooth ceiling planks because of their four forward-curved claws.
   - *First verb / connector:* `rakit` / `terus`
   - *Spoken line (25 words):* “Kalo kamu rakit rumah bata berplafon kayu di halaman, terus kamu putar suara panggil, kamu sudah punya rumah walet. Tapi burungnya terpeleset terus saat mau hinggap.” *(Less iconic as a first visual shock than sunlight blasting straight through the open hole.)*

- `hook_selection: auto` (delegated under active `--automation=after-topic`). Selected **Option 1** because bright sunlight flooding an unbaffled swiftlet room explains the #1 defining feature of a swiftlet house (*sekat cahaya / void gelap*), reads unmistakably on mute in a 2.5D vertical cutaway, and launches the cleanest logical sequence across all 7 rounds.

## Script check (v1 — agent-verified under active automation)

[SCRIPT.md](SCRIPT.md) v1 is built around Hook Option 1 across 11 scenes (18 meaningful events).

- **Spoken word count & budget:** **240 spoken words** (`25 + 21 + 21 + 21 + 22 + 20 + 21 + 22 + 18 + 26 + 23`). `episode_qa.py --budget 235 --voice 5g0yKK2JwTRka0IG61Hh` reported no local cached narration for Pribs in this clone; evaluated against Pribs's recorded board motion-preview pace (`2.57 wps`, `60 words / 23.36 s`) and the `2.40 wps` fallback pace: predicted raw narration is `93.4–100.0 s`, predicted 1x film duration (including `~5.8 s` boundary pauses/tag hold + `0.625 s` end card) is **`99.5–106.2 s`** (`79.6–85.0 s` delivered at 1.25x), centered squarely inside `90.0–112.5 s` at 1x. Will reconcile after synthesis.
- **First sentence & `"Tapi"` turn:** Sentence 1 = **19 words** (predicted `7.4–7.9 s <= 10.0 s`); `"Tapi"` at word 20 (predicted `7.8–8.3 s <= 12.0 s`). Total `"tapi"` occurrences across full script: **1** (hook only).
- **Selected hook three parts:** Option 1 spoken line, Frame 0 bare yard corner + `<0.25 s` masonry build / calling audio / swiftlets swooping in and bolting from glare, and 46 px DM Sans 800 progressive captions recorded above and in [SCRIPT.md](SCRIPT.md).
- **Cold-read & POV check:** Read all 240 spoken words standalone without headings or visual cues. `"kamu"` resolves unambiguously to the single backyard builder/keeper throughout; every problem, physical fix, and biological result makes standalone sense on audio alone. Repairs applied before locking v1: (1) Round 2 changed `"ruangnya pengap di atas tiga puluh derajat"` → `"suhunya naik di atas tiga puluh derajat"` for clearer ear comprehension; (2) Round 3 clarified `"olesan liur"` → `"sarang liurnya"` so general viewers immediately understand what peels off; (3) Round 5 simplified `"pemutar suara inap pelan dekat papan sirip"` → `"suara inap pelan di papan sirip"` and Round 7 tightened `"ambil sarang bertelur bikin koloni kabur"` for crisp spoken rhythm; (4) kept strictly zero English loanwords (`tweeter`, `speaker`, `void`) in spoken Indonesian narration to ensure crisp TTS pronunciation.
- **Contract judged rules (script scope):**
  - `[pass]` `hook-frame`: Frame 0 opens on bare warm-clay yard corner with stacked bricks and motion at `0.25 s` under 46 px captions.
  - `[pass]` `pictures-alone`: All 11 scenes specify ordered visual sub-beats depicting cause, added upgrade, and on-screen retest.
  - `[pass]` `event-density`: 11 scenes / 18 distinct physical events beyond captions.
  - `[pass]` `motion-variety`: Shot plan alternates `wide` → `close cutaway` → `medium-wide` → `medium` → `close cutaway` → `medium` → `medium-wide` → `close cutaway` → `wide` → `medium` → `wide` (max consecutive identical shot = `1`).
  - `[pass]` `subject-scale` & `vessel-scale`: Mini swiftlet tower cutaway, baffle, vent pipes, floor water basin, grooved planks, zinc LMB frame, and hanging harvest scale planned at ≥ 40% frame width with persistent yard landmarks.
  - `[pass]` `ear-test`: Standalone cold read passed after the 4 repairs above; single `"kamu"` POV throughout.
  - `[pass]` `build-first`: Hook Option 1 completes all four Editorial v9 slots verbatim with ordinary punctuation and fresh verb/connector (`susun` / `setelah itu`).
  - `[pass]` `shortfall-before-fix`: 7 single-cause problem–improvement rounds (20–22 words / `~7.8–9.2 s` each at 1x), each tested on screen, distinct triggers (`cahaya silau`, `panas siang >30°C`, `udara kering/sarang rapuh`, `plafon licin`, `suara panggil keras`, `hama tokek malam`, `panen saat bertelur`), varied natural transitions (`Cahaya matahari...`, `Pas tengah hari`, `Seminggu jalan`, `Giliran walet hinggap`, `Masalahnya`, `Masuk bulan ketiga`, `Begitu sarang jadi`), `"Tapi"` only in hook.
  - `[pass]` `same-system`: Every installed upgrade (dark baffle wall, downward elbow PVC vent pipes, floor water basin, grooved meranti planks, quiet indoor nesting tweeters, smooth zinc LMB frame, fledgling-safe harvest rhythm) remains visibly legible on the same backyard tower through Scene 11.
  - `[pass]` `final-job`: Scene 9 shows the completed house coping with bright midday heat and dusk return before calling the colony `"stabil"`.
  - `[pass]` `income-scene`: Scene 10 weighs `100 g` (~13 dry raw white mangkok nests) on a hanging scale beside the finished house with world-anchored price tag `100 g × Rp8.310 ≈ Rp831.000` (`estimasi harga pengepul / Agu 2026`, sourced from Markas Walet 03 Aug 2026 national benchmark), rounded spoken numbers, `>= 3 s` 1x hold, zero profit/payback/promise claim.
  - `[pass]` `event-map`: 18 meaningful events (`15–19`); every finished component visibly enters the build.
  - `[pass]` `closing-lines` & `closing-signature`: Congratulation naming built mini swiftlet house + next-build question containing consecutive `"bikin di halaman"`, yellow `#FFD44D` hold + `@bikindihalaman.id`, hard cut to `0.625 s` 1x (`0.5 s` delivered) exact-match thumbnail end card.
  - `[pass]` `reframing`, `living-world`, `event-sfx`: Plans beat-level push-ins/tracking/micro-impacts, 4-plane 2.5D parallax & reactive lighting, and frame-locked organic SFX from board Visual v5 library (`bgm: none`).

## Visual storyboard (v1 — agent-verified under active automation)

- **HyperFrames project:** Initialized cleanly in [video/](video/) (`npx hyperframes init --skip-skills --skill=hyperframes`), inheriting board DM Sans variable font, Visual v5 4-plane 2.5D engine (`assets/world-v5.js`), domain cutaway world (`assets/walet-world.js`), local GSAP (`assets/gsap.min.js`), and all 16 Visual v5 CC0/Pixabay organic SFX assets (`assets/sfx/`).
- **Storyboard artifacts:** [video/BRIEF.md](video/BRIEF.md), [video/STORYBOARD.md](video/STORYBOARD.md) (`storyboard_lint.py --strict`: `passed`, 0 errors, 0 warnings, `frame_count: 11`, `max_push_streak: 1`), 11 standalone HyperFrames scene compositions (`compositions/s01.html`–`s11.html`), progressive captions composition (`compositions/captions.html`), 36 captured high-resolution stills/poses (`boards/stills/`, `boards/poses/`), [video/boards/storyboard.html](video/boards/storyboard.html), and [video/boards/storyboard.png](video/boards/storyboard.png) (`1600 × 9993`, `36/36` images loaded, `0` broken, `0` console/network errors, `0` desktop/mobile overflow).
- **Gate receipt:** `episode_qa.py --stage storyboard` → `{"status": "passed", "stage": "storyboard", "disclose": []}` (`video/verification/gate-storyboard.json`).
- **Visual inspection & polish applied before audio:** Inspected `storyboard.png` and individual frame stills/poses (`hook-0.0s`, `frame-00`–`frame-08`, `01-b-end`, `07-b-end`, `08-a-start`, `10-b-end`, `11-b-end`); fixed: (1) chained color-mix helper (`wMixColor`) in `walet-world.js` so `s03` interior stays deep cave slate; (2) forearm-to-sleeve overlap in `drawWorkingHand`; (3) elevated `cam.y` (`452–464`) across zoomed cutaways `s02`, `s04`, `s05`, `s06`, `s07` so plinths/basins clear the caption zone cleanly; (4) baffle `+1 px` overlap removing hairline seam; (5) `s01` exiting swiftlet trajectory clearing the roof tile; (6) `s04` full-scale smooth-alpha swiftlets; (7) `s11` keeper-held nest proportion (`0.46`); and (8) `s08` seamless full-depth interior plaster + right-side Beat 1 hand entry completely above the caption band.

## Audio (v1 — single take verified & listened natively)

- **Transport & synthesis:** `elevenlabs_api` (Starter tier verified via `narration.py --check-api`, single continuous take via `narration.py --auto-align`, zero retries).
- **Voice & model:** `provider: elevenlabs`, `tts_model: eleven_v4`, board default **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh`, `voice_resolution.source: board_config`, `boards/budidaya-di-halaman/AUDIO.json`).
- **Raw take:** `video/.media/audio/voice/narration-cbba372a1ff2767f8fd3.mp3` (`request_sha256: cbba372a1ff2767f8fd367d213c5bede31aab9b8736ca694656ead7c55039261`, `98.769 s`, exact `240` natively aligned words).
- **Native listening (`listening: agent`):** Listened natively to the full raw MP3 take before placement. Zero spoken delivery tags, zero clipped syllables, clean natural Indonesian delivery and accurate numeric pronunciation (`tiga puluh derajat`, `seratus gram`, `delapan ribu tiga ratus per gram`, `delapan ratus tiga puluh ribu`).
- **Acoustic boundaries & placed narration:** Placed via `audio_boundaries.place(..., pre_roll=0.15, fps=30)` with `0.22 s` editorial pauses after S01–S09 and `2.80 s` after S10 (giving `3.229 s` 1x yellow total-chip hold + `1.53 s` S11 wide pull-out intro), padded cleanly to `104.625 s` at 1x (`2,511` exact frames @ 24 fps = `83.700 s` delivered @ 30 fps at `1.25x`; end card `104.000–104.625 s` = `0.625 s` 1x / `0.500 s` delivered), normalized once via `normalize_after_placement(..., integrated=-14.5, true_peak=-1.5, lra=7)` to `video/assets/audio/narration.wav`.
  - Measured Hook S1 end (`walet.`): **`7.084 s` <= `10.0 s`**
  - Measured Hook turn (`Tapi`): **`7.423 s` <= `12.0 s`**
  - Every scene boundary (all 10 cuts): `201.7–1530.0 ms` verified quiet margins (`audio_boundaries.py --video`: `passed`, 10/10 boundaries).
- **BGM:** `none` (board contract).
- **SFX:** `use` — `44` frame-locked organic foley hits and low-gain diegetic backyard beds from the board Visual v5 CC0/Pixabay kit (`video/sound_design.json`), strictly inside scene interiors (`>= 120 ms` away from all 10 quiet cuts and silent during `0.625 s` end card). Verified via `sound_design.py --apply` & `--check` (`passed`, 44 cues).
- **Composition sync:** Reconciled `video/index.html`, `compositions/s01.html`–`s11.html`, exact word-by-word progressive `compositions/captions.html`, and `video/STORYBOARD.md` (`status: animated`; `storyboard_lint.py --strict`: `passed`, 0 errors/warnings; `dom_lint.py`: `passed`, 0 G5/readcheck failures).

## Delivery summary & verification record (2026-11-28)

- **Verification & independent 7-dimension jury audit:** Rendered `video/verification/proof.mp4` (`1080 × 1920`, `24 fps`, `104.625 s`), passed `hyperframes check --json --no-cache` (`ok: true`, `0` lint, `0` runtime, `0` layout errors/warnings/info, `31/31` contrast), `dom_lint.py` (`11/11` scenes, `0` G5 anti-slop / `0` readcheck fails), `storyboard_lint.py --strict` (`0` errors, `0` warnings), and `proof-fingerprint.json` (`first_motion_seconds: 0.2`, `longest_static_seconds: 0.0`, `held_share: 0.0`). Fresh-context subagent reviewer (`0718e434b46abec3201bb994c29931be`) audited Pass 1 (`NEEDS REVISION BEFORE RENDER`, 6 P0 + 4 P1); all P0s and P1s were fixed (`sfx-09-mist` separated non-overlapping at `77.267 s` gain `0.14` bringing `sound_design.py --export` to `44/44` cues passing; `wow_upgrade` rebuilding S05 as `2.4×` ceiling-plank claw-skid/groove-grip macro and S07 as `2.2×` moonlit LMB tokek/zinc-collar corner cutaway plus tightened S02/S04/S06 cutaways; centered Frame 0 opening caption at `0.00 s` and full-chunk active-yellow karaoke with `data-layout-allow-safe-zone`; persistent S01 calling tweeter cleanly above zinc collar across S01–S11; warmed Visual v5 cream-sage sky, staggered brick masonry, gradient mist ribbons, wooden thermometer plaque, exterior downward PVC elbows with mesh caps, foreground cutaway hose). Pass 2 returned **`APPROVE FOR DELIVERY RENDER`** (`18/18` judged rules passed, `0` open P0s, all `7/7` rubric dimensions `8.0/10`, `weakest_shot: 05-s02-prob (11.40s)`, recorded in [`video/REVIEW.md`](video/REVIEW.md), `composition_sha256: 99fbd46b292fbdc8ca4a95867255f0622a6873b375c1491e9d154c4ed7544f7a`). Passed `episode_qa.py --stage verification --dom-lint` ([`video/verification/quality-gate-verification.json`](video/verification/quality-gate-verification.json), `disclose: []`).
- **Delivery master & 1.25× export (`30 fps`, pitch-kept):** Rendered 24 fps delivery master (`video/out/master-24fps.mp4`, `35,064,357` bytes, SHA-256 `23f117da2bb61023ca0a396cca4deba899189746480f20d941d72a51d7bf3055`, `104.625 s`, `2,511` frames), verified `audio_boundaries.py --export` (`passed`, `10/10` boundaries) and `sound_design.py --export` (`passed`, `44/44` cues, `34.69 dB` median vocal-band SNR, `0.025 s` max severe masking). Retimed via `setpts=PTS/1.25,fps=30`, pitch-kept `atempo=1.25`, and two-pass linear `loudnorm` (`I=-14.0:TP=-1.5:LRA=11`) to:
  - [`exports/rumah-walet-mini-halaman.mp4`](exports/rumah-walet-mini-halaman.mp4) (`19,080,060` bytes / `18.20 MB`, SHA-256 `8801d5999d8a4538945ccfa366afd1e66dd30a1e291e446a793206df9e448ace`, `1080 × 1920`, H.264 High `yuv420p` / AAC 48 kHz `187 kbps`, `30.0 fps`, `2,511` frames, exact duration **`83.700 s`**, integrated **`-14.03 LUFS`**, true peak **`-2.44 dBTP`**).
  - [`exports/thumbnail.png`](exports/thumbnail.png) (`1080 × 1920`, `408,436` bytes, SHA-256 `c86e8eed25abfb148ce8fee879843d6a1c07d2fa141723d27ca1e54e6d30d52c`, exact match to the `0.500 s` delivered end card `83.200–83.700 s`, `cover_offset_ms: 83450`).
  - [`exports/rumah-walet-mini-halaman.srt`](exports/rumah-walet-mini-halaman.srt) (`42` cues, `1.25×` scaled, `3,000` bytes, SHA-256 `b582d481f3733f6f01b633fe28d458109cb081c4b5b59cdb4ec23c62223d0484`, cleared cleanly at `83.200 s`).
- **Delivered audio/visual verification & export gate:** Listened natively to 1.25× delivered mix (`video/verification/delivered-mix.mp3`, `listening: agent` — crisp pitch-kept Indonesian speech, balanced SFX, silent end card), visually inspected `exports/thumbnail.png` and decoded export frames (`video/verification/export-contact-sheet.jpg`), and passed `episode_qa.py --stage export` ([`video/verification/quality-gate-export.json`](video/verification/quality-gate-export.json), `status: passed`, `disclose: []`).
- **Content package (`delivery: package`):** Authored single shared Indonesian copy unchanged for all three inherited board accounts (`@bikindihalaman.id`, `@bikindihalaman_id`, `Bangun Di Halaman`) in [`CONTENT_PACKAGE.md`](CONTENT_PACKAGE.md). No external Trypost upload or publishing performed under default `delivery: package`.

## Google Drive archive (synced)

- **Folder:** [`budidaya-di-halaman/rumah-walet-mini-halaman`](https://drive.google.com/drive/folders/1q8G_TogBt_9sMwptt2W-tbU5rIaTaVlE) (`folder_id: 1q8G_TogBt_9sMwptt2W-tbU5rIaTaVlE`, `remote_path: budidaya-di-halaman/rumah-walet-mini-halaman`, synced `2026-11-28T16:26:27Z` via `gdrive.py`, `env_source: dotenv`):
  - `rumah-walet-mini-halaman.mp4` (`19,080,060` bytes, MD5 `162242154541fc98fa1979f18d33ef90`, `uploaded`, file `1Bigv0-Hv_NFvMvTCSSFA16MXHnz9GYcb`)
  - `rumah-walet-mini-halaman.srt` (`3,000` bytes, MD5 `053c4a0c594034165aef86460e1eb56e`, `uploaded`, file `1HEFCepd7XO5q4asW69rP0pbeDvIY2a7T`)
  - `thumbnail.png` (`408,436` bytes, MD5 `c9f0fe9c0b18802ff144a6d4ed547217`, `uploaded`, file `1gPaGMa1MQdHWthXUBa0u3x-CecWOajqq`)
  - `CONTENT_PACKAGE.md` (`6,756` bytes, MD5 `3cff36de648632ce68b57a4f529b3b97`, `uploaded`, file `1Jm4G5c2muD-f6ISosDehDw_cR3t2Iu3Z`)

## Current state

- `stage`: content_package
- `status`: complete
- `user_approval`: approved on 2026-11-28 (`"approve dan buatkan pr"`)
- `next_action`: pull request opened against `main`; ready for merge or optional Trypost draft/queue/publish command if external publishing is requested later.

