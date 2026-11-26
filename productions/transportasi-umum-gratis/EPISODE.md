# Semua Transportasi Umum Gratis

## Brief and execution

- **slug:** `transportasi-umum-gratis`
- **topic:** Twin-world 10-year thought experiment comparing two identical cities where World A makes all public transportation (buses, trains/MRT, trams) fare-free while World B keeps standard paid fares.
- **topic_selection:** `user` (user supplied topic `"semua transportasi unum gratis"` after reviewing the 10-topic discovery shortlist on 2026-11-24).
- **board:** `dua-dunia` (`approved`, revision `editorial v2 / visual v1`)
- **editorial:** [EDITORIAL.md](../../boards/dua-dunia/EDITORIAL.md)
- **visual:** [frame.md](../../boards/dua-dunia/frame.md)
- **contract_snapshot:** [CONTRACT.json](CONTRACT.json) (copied from `boards/dua-dunia/CONTRACT.json`, `editorial v2 / visual v1`, SHA-256 `a6972f2b198696b45d6fe5036f06e7a9ad3093b1092eb4bf027f06dbfb599ba1`, validated via `episode_qa.py --contract`).
- **purpose:** Playful, rigorous miniature-world simulation that tests the popular intuition ("if all public transport becomes free tomorrow, does the city instantly improve?"), exposes realistic short-term crowding/budget/car-shift friction, demonstrates the physical boarding + fleet-capacity mechanism in 3D, and leaves viewers with a clear trade-off and choice question.
- **audience:** General Indonesian short-form viewers (commuters, young workers, students, urban residents).
- **format:** `1080x1920`, `30 fps`, hybrid 3D low-poly diorama (topic-specific Polyfork GLB models + procedural capsule citizens), Fredoka bold outlined captions in `[54, 1380, 972, 200]`, persistent top-center disclaimer `Eksperimen pikiran. Angka dari model.`.
- **language:** Indonesian (`aku/kamu` conversational curious narrator).
- **duration_target:** `75–115 s` (sweet spot `90–105 s`, ~`215–250` spoken words planned at `2.4 wps` baseline since voice `AfkBqzsATOuueGnLAvJi` has no prior measured production in `episode_qa.py --budget`; re-budget after first take).
- **audio:** Narration (`eleven_v4`, board voice `AfkBqzsATOuueGnLAvJi` — Samsul, Warm & Clear Narrator) + lighthearted acoustic-guitar/mallet BGM (`-15.5..-12.5 LUFS`, `<= -0.5 dBTP`); SFX optional/sparse per board contract.
- **requested_endpoint:** `publishing` (`--delivery=draft`, authorized by user `"otomasikan sampai upload draft"` on 2026-11-24 after storyboard v1 approval).
- **execution_policy:** `automation`
- **automation_after:** `storyboard`
- **automation_state:** `active` (activated by user approval of visual storyboard v1 on 2026-11-24)
- **human_review:** `none for subsequent work` (hook Option 1, script v1, and storyboard v1 were human-approved; subsequent production, verification, export, packaging, and Trypost draft upload proceed under active automation with independent subagent review)
- **pre_render_authorization:** `delegated by the user's "otomasikan sampai upload draft" instruction after storyboard v1 approval`
- **audio_transport:** `elevenlabs_api`
- **publishing_transport:** `api` (Trypost REST API via `trypost.py`, workspace `01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37` / `Admin's Workspace`)
- **publishing_targets:**
  - `source`: `board` (confirmed by user and saved to `boards/dua-dunia/ACCOUNTS.json` on 2026-11-24)
  - `board_accounts_file`: `boards/dua-dunia/ACCOUNTS.json`
  - `board_accounts_sha256`: `a029e7b9199fa4e4b9a9d6bb711dd26dc56a23ad4373c7c6daa3b7021ef6865b`
  - `accounts`:
    1. `instagram` `@duadunia.lab` (`01a208db-b614-7326-9f1b-e5e9ab8100c1`)
    2. `youtube` `@duadunia_lab` (`01a20931-862c-7024-a294-6a715c13a929`)
    3. `facebook` `Dua Dunia Lab` (`01a2093d-8956-701b-9933-7f2e6776b752`)

## Overlap & differentiation check

- **TRACKER.json productions:** Zero existing episodes under `dua-dunia` and zero public-transit policy episodes across other boards.
- **Board internal motion preview (`boards/dua-dunia/motion-preview.mp4`):** The board's 15-second internal motion preview used *"Angkutan Umum Gratis? Simulasi 10 Tahun"* strictly as a static-study/preview visual benchmark, never as a tracked production episode. This full 90–105 s episode covers **all public transportation modes** (buses, trains/stations, trams) with original empirical research (`SOURCES.md`), original script/numbers/arc, and topic-specific Polyfork 3D environments (transit station/depot, train/tram, commercial street, office/school destinations) beyond the board's 6 starter street models.

## Research status

- **Status:** Complete ([SOURCES.md](SOURCES.md)).
- **Key resolved questions:**
  1. Does fare-free transit immediately clear car traffic? No—empirical evidence from Luxembourg (LISER 2026: −4.6 pp daily car use, only 1.2% full car-to-PT switch), Tallinn (−5% car, walking shift), and NYC pilot (11% from cars) shows limited congestion relief alone.
  2. What causes the Year 1–2 dip? Surging ridership (+30–85%) without immediate extra fleet packs vehicles (+7% bus stop time in NYC pilot, lower comfort/cleanliness in Luxembourg) and exposes the farebox budget gap (8–33% of operating costs; Hasselt 4× cost rise).
  3. What physical mechanism flips the outcome? Removing fareboxes/turnstiles enables all-door boarding (−37–51% dwell time per passenger, NACTO) and eliminates ticketing/enforcement overhead; reinvesting those savings plus dedicated mobility funding into fleet expansion and bus lanes (Dunkirk 100→135 buses) creates frequency and speed that finally win commuters and unlock major social/accessibility gains (+23% low-income PT in Tallinn, 47.9% more work/edu trips in Luxembourg).

## Hook options (awaiting human selection)

*Board performance analysis: none available yet (first episode on `dua-dunia`). All 3 hooks satisfy `EDITORIAL.md#hook-pattern` (identical twin worlds + single named difference + comparison question within 4.5s) and stay strictly within `SOURCES.md`.*

### Option 1 (Recommended) — Direct policy contrast at the station & curb
- **Mechanism:** Immediate rule contrast & visible barrier removal (open zero-fare boarding vs. paid ticket queue).
- **Spoken line (12 words; Sentence 1 = 9 words, ~3.75 s at 2.4 wps; full run ~4.3–4.5 s):**
  > "Kita simulasikan dua dunia sama, tapi satu transportasinya gratis. Mana yang menang?"
- **Frame 0:** Street-level 3D diorama outside a bustling transit station & bus stop; a crisp `RP 0` archway stands wide open with capsule commuters walking straight into all doors of an arriving bus/train from frame 0 (`t = 0.0–0.5s`) while pedestrians stride along the sidewalk.
- **On-screen line:** Bold Fredoka headline `TRANSPORTASI UMUM GRATIS?` above the station + persistent `Eksperimen pikiran. Angka dari model.` top-center + lower-band word-synced captions.
- **Angle & promise:** Cleanest, widest framing for `dua-dunia`'s debut episode—declares the exact single variable immediately without narrowing the question solely to traffic or budgets, then pays it off across crowding friction, physical boarding/fleet mechanics, a Year 4 crossover, and the 100-world sensitivity check.

### Option 2 — Traffic congestion paradox (intuition trap)
- **Mechanism:** Counterintuitive traffic promise that sets up the early congestion surprise.
- **Spoken line (12 words; Sentence 1 = 9 words, ~3.75 s at 2.4 wps; full run ~4.3–4.5 s):**
  > "Aku bikin dua dunia kembar, cuma beda ongkos transportasi. Mana lebih baik?"
- **Frame 0:** Elevated 3/4 street diorama showing bumper-to-bumper private cars idling beside a gliding bus and commuter rail line with a `RP 0` badge rotating overhead from `t = 0.0s`.
- **On-screen line:** Bold Fredoka headline `GRATIS = BEBAS MACET?` + lower-band captions.
- **Angle & promise:** Directly hooks commuters' strongest gut assumption ("free transit empties the roads"), making the Year 1–2 reveal that cars barely disappear hit even harder before showing how fleet capacity and all-door speed change the game.

### Option 3 — Fiscal skepticism & durability tension
- **Mechanism:** Economic trade-off & sustainability doubt raised right on Frame 0.
- **Spoken line (12 words; Sentence 1 = 9 words, ~3.75 s at 2.4 wps; full run ~4.3–4.5 s):**
  > "Dua dunia ini sama, kecuali semua transportasi umumnya gratis. Dunia mana menang?"
- **Frame 0:** Immediate horizontal 50/50 split diorama: top half shows smiling commuters breezing past a `TARIF RP 0` station gate as a bus rolls in (`t = 0.0–0.5s`); bottom half shows a `BAYAR` ticket gate queue beside a steady municipal budget meter.
- **On-screen line:** Bold Fredoka headline `GRATIS SELAMANYA, KUAT NGGAK?` + lower-band captions.
- **Angle & promise:** Meets skeptical viewers where they already are ("can a city actually afford this?"), promising a fair 10-year and 100-world stress test showing when free transit thrives and the 29/100 worlds where underfunding makes it fail.

- **Recommendation:** **Option 1** — strongest debut clarity for `dua-dunia`, follows the canonical street-level hook shot from `frame.md` (saving the 50/50 split reveal for Beat 2 so visual rhythm escalates cleanly), and sets up both the crowding/traffic surprise and fiscal trade-off without locking the whole episode into only one sub-question.
- **Selected hook:** **Option 1** (`user` approved recommended Option 1 with `"setuju"` on 2026-11-24).
  - **Spoken line:** `"Kita simulasikan dua dunia sama, tapi satu transportasinya gratis. Mana yang menang?"`
  - **Frame 0:** Street-level 3D diorama outside a bustling transit station & bus stop; wide-open `RP 0` archway with capsule commuters walking straight into all doors of an arriving bus & commuter train (`t = 0.0–0.5s`) while pedestrians stride along the sidewalk.
  - **On-screen line:** Headline `TRANSPORTASI UMUM GRATIS?` + persistent disclaimer `Eksperimen pikiran. Angka dari model.` + lower-band word-synced captions.

## Script check (v1 — awaiting human review)

- **Script artifact:** [SCRIPT.md](SCRIPT.md) (`v1`, 19 scenes across all 12 `dua-dunia` beats)
- **Word budget:** `239` spoken words (`CONTRACT.json` range: `180–290`). `episode_qa.py --budget` reported no prior measured narration for voice `AfkBqzsATOuueGnLAvJi`, so budgeted at `2.4 wps` baseline (`script-craft.md`) → predicted speech `99.58 s` (range `88.5–113.8 s` across `2.1–2.7 wps`), fitting `75–115 s` (`90–105 s` sweet spot). Will re-budget immediately after first measured narration take.
- **First sentence timing:** `"Kita simulasikan dua dunia sama, tapi satu transportasinya gratis."` — `9` words → `3.75 s` predicted at `2.4 wps` (`<= 4.5 s` contract limit; full 12-word hook ~`4.3–5.0 s`).
- **Cold-read check:** **Pass.** Read the 239-word narration standalone without visuals/headings:
  - Repairs made during draft: tightened `"sopir juga lebih tenang"` → `"cekcok ongkos hilang"` (self-explanatory to the ear and directly grounded in Vital City/Kansas City −40% driver assault data); clarified `"kota"` → `"Dunia A"` in S05; replaced abstract `"skor mobilitas"` → `"kecepatan dan kenyamanan"` in S10; corrected S13 so fleet expansion is funded by `"anggaran kota"` rather than overclaiming ticket-machine savings alone; replaced visual-dependent `"Di papan skor akhir"` → `"Di akhir simulasi"` in S16; spelled out all numbers in Indonesian words (`seratus ribu`, `sepertiga`, `tujuh puluh satu`, `delapan puluh empat`) for clean TTS reading.
  - All pronouns (`Keduanya`, `ongkosnya`, `begitu`) resolve directly from spoken context; every paragraph conveys what happened and why without on-screen copy.
- **Script-relevant contract judged rules:**
  - `hook-frame`: **pass** — S01 Frame 0 opens on active 3D transit hub with `RP 0` archway, moving bus/train (`0.0–0.5s`), and phone-legible headline `TRANSPORTASI UMUM GRATIS?`.
  - `ear-test`: **pass** — full cold-read above resolves every actor, world (`Dunia A`/`Dunia B`), and causal link without visuals.
  - `epistemic-disclaimer`: **pass** — persistent `Eksperimen pikiran. Angka dari model.` specified across all 19 scenes; simulation numbers framed explicitly as model outcomes (`Dari seratus simulasi...`).
  - `simulation-hook`: **pass** — S01 declares identical twin worlds, names the single differing variable (`satu transportasinya gratis`), ends on comparison question (`Mana yang menang?`), Sentence 1 = `3.75 s` (`<= 4.5 s`).
  - `controlled-twin-worlds`: **pass** — S02 establishes 50/50 split-screen locking 3 shared baselines (100,000 residents, equal income, equal traffic) before S03–S04 isolate the single fare rule.
  - `short-term-dip`: **pass** — S07–S10 (`est. 27.1–46.7 s`, ~27–47% of runtime) show unchanged car traffic, walking substitution, bus crowding, budget squeeze, and Year 2 dip where World A trails World B.
  - `physical-mechanism`: **pass** — S11–S13 demonstrate the concrete 3D cutaway mechanism: World B front-door fare bottleneck (up to 1/3 travel time in dwell) vs. World A turnstile removal, all-door boarding, and fleet expansion.
  - `data-proof-cards`: **pass** — S14 dark-navy crossover line chart (`Nyalip!` at Year 4) + S18 dark-navy 10×10 Monte Carlo robustness grid (`71/100` win, `84` early dip).
  - `soft-closing-cta`: **pass** — S19 ends with `"Jadi di dua dunia ini, kamu pilih tinggal di mana?"` (consecutive `dua dunia`, zero follow/subscribe/like prompts).
  - `original-topic`: **pass** — original all-mode free public transit scenario, empirical research (`SOURCES.md`), model numbers, and dialogue (distinct from the reference corruption episode and internal 15 s board preview).

- **Script approval:** Approved by user (`"approve"`) on 2026-11-24 (`SCRIPT.md` v1, 239 words, 19 scenes).

## Visual storyboard (v1 — awaiting human review)

- **HyperFrames project:** [video/](video/) (initialized empty with `--skip-skills --skill=hyperframes`)
- **Brief & visual spec:** [video/BRIEF.md](video/BRIEF.md), [video/frame.md](video/frame.md)
- **Scene plan:** [video/STORYBOARD.md](video/STORYBOARD.md) (`19` frames, `status: built`, planned duration `99.6 s`, `storyboard_lint.py --strict`: `passed`, `0` errors, `0` warnings)
- **HTML board:** [video/boards/storyboard.html](video/boards/storyboard.html) (`60/60` images verified loaded with `naturalWidth > 0`)
- **Combined PNG:** [video/boards/storyboard.png](video/boards/storyboard.png) (`1680×9504 px`, full-page capture verified visually: all 19 frames ordered across 4 acts, 3-frame hook strip + 38 start/end change-over-time poses legible)
- **Stills & poses:** `video/boards/stills/` (`19` hero stills `frame-00..18`) and `video/boards/poses/` (`hook-0.0s.png`, `hook-0.4s.png`, `hook-3.0s.png` + `01-a-start.png`/`01-b-end.png` through `19-a-start.png`/`19-b-end.png`)
- **3D Polyfork sourcing:** Inherited 6 board baseline street models + sourced **15 topic-specific Polyfork GLBs** (CC BY 4.0) into `video/assets/models/`: `city-tram`, `tram-track-tile`, `bus-shelter`, `subway-entrance`, `turnstile-bank`, `ticket-booth`, `service-bay-garage`, `office-tower`, `cafe-storefront-unit`, `cafe-table-set`, `public-school`, `city-taxi`, `traffic-light`, `bicycle-parking-rack`, `city-bicycle`. Rendered via Three.js r170 (`THREE.NoToneMapping`, `SRGBColorSpace`) with deterministic `hf-seek` clock.
- **Visual inspection repairs applied before handoff:**
  1. Moved F01/F06 foreground hero commuters onto the far transit plaza so lower captions never cross faces.
  2. Hid World B's `LOKET` plaque in F02 so twin starting worlds read visually identical before F03 isolates the rule.
  3. Re-framed F09 so both the 12 frowning commuters at the stalled bus and the red dropping `DEPOT · KAS MENIPIS` budget bar sit cleanly in frame.
  4. Added auto-fit horizontal padding in `createDiegeticPlaque` so `STASIUN & SEKOLAH` and `PAJAK → ARMADA` never touch inner borders.
  5. Separated F13 depot dispatch buses onto a parallel transit lane (`z = -9.8`) behind `cutBusA` (`z = -5.4`) to eliminate bus intersection, hid `cutPlaqueA` during F12 macro, centered F12 `1/3 waktu berhenti` dwell ring, and added queue step-forward progression in F12.
  6. Repositioned F14 `Dunia A (Gratis)` legend to top-left (zero curve crossing), populated F15 cafe tables with smiling students/workers, and raised F18 10×10 Monte Carlo grid card ~160 px clear of the caption band.
- **Quality gate (`storyboard`):** `passed` (`disclose: []`) — saved at [video/verification/quality-gate-storyboard.json](video/verification/quality-gate-storyboard.json). `hyperframes check --json` also returned `ok: true` (`0` lint/runtime/layout errors).
- **Preview server:** None started (remote VM environment; full storyboard delivered via verified HTML & combined PNG).

## Audio & sound design (completed)

- **Storyboard approval & automation:** User approved storyboard v1 and authorized active automation through Trypost draft upload (`"otomasikan sampai upload draft"`, 2026-11-24). Confirmed all 3 Dua Dunia Lab accounts and saved them to `boards/dua-dunia/ACCOUNTS.json` (SHA-256 `a029e7b9199fa4e4b9a9d6bb711dd26dc56a23ad4373c7c6daa3b7021ef6865b`).
- **Authorized voice override:** Because the `.env` ElevenLabs key is Free-tier and blocks library voice `AfkBqzsATOuueGnLAvJi` (*Samsul*) with HTTP 402, the user authorized an episode override to premade `eleven_v4` voice `TX3LPaxmHKxFdv7VOQHJ` (*Liam — Energetic, Social Media Creator*).
- **Narration take:** Single-take synthesis saved at `video/.media/audio/voice/narration-07364012a18ff79e6209.mp3` (`239` spoken words, natively auditioned via `view_file` — clean Indonesian pronunciation, zero read-aloud tags). Leading silence trimmed (`150 ms`) and opening S01 tightened by pitch-preserving `atempo=1.18` so Sentence 1 ends at `3.703 s` and full hook (`"Mana yang menang?"`) ends at `4.449 s` (`<= 4.5 s`); total film duration `96.63 s` ([video/timing.json](video/timing.json)).
- **BGM & master mix:** Deterministic F-major 112 BPM acoustic-guitar + wooden-mallet bed (`video/audio/bgm-acoustic-mallet.wav`) with tension dip on `s07–s10` and harmonic accents on `s03`, `s12`, `s14`, `s18`, and `s19` resolution; sidechain-ducked under voice and 2-pass EBU R128 loudnorm mixed into `video/audio/master-mix.wav` (`-14.15 LUFS`, `-1.48 dBTP`, natively auditioned via `view_file`). Asset hashes and explicit `narration: use`, `bgm: use`, `sfx: none` decisions saved in [video/sound_design.json](video/sound_design.json).

## Production, independent review & verification (passed)

- **Composition & determinism:** 19-scene deterministic Three.js r170 + Polyfork diorama (`video/index.html`, `video/assets/kit-3d.js`, `video/assets/episode-3d.js`, `composition_sha256: a1a49d583945f49450cf8f1c5fd55a0a5449276efffcb6dade1956075f474ddb`). Seek test `45.0s → 90.0s → 10.0s → 45.0s` verified bit-for-bit identical (`a2b75d0c2fdc`), zero console/page errors.
- **Polish from independent review v1:** Resolved all 5 P0 findings (unoccluded `TARIF Rp 0` at `t=0.00s`, `PCFShadowMap` + `normalBias: 0.08` eliminating shadow acne, tightened S01 hook to `4.449 s`, 16 brake-lit bumper-to-bumper cars + elevated tracking in `s07`/`s08`, 14 visibly frowning riders + centered `DEPOT · KAS MENIPIS` in `s09`, uncropped cutaway plaques in `s12`/`s13`, Year 2 frowning shelter crowd in `s10`, Year 10 fleet/car differentiation in `s16`/`s19`, natural cafe clusters in `s15`).
- **Independent review v2 (`subagent`, fresh context):** **`PASS`** — all `18/18` contract judged rules `[pass]`, `0` open P0 findings, 7-dimension jury rubric scores all `>= 7.5/10` (`style_fidelity: 8.5`, `concept_wow: 8.0`, `motion_craft: 7.5`, `design_typography: 7.5`, `finish_texture: 7.5`, `sound_sync: 8.0`, `technical: 8.5`). Weakest shot: `s11` (lower caption brushes top edge of 3D `DUNIA B` plaque). Recorded in [video/REVIEW.md](video/REVIEW.md).
- **DOM lint (`dom_lint.py`):** `passed` (`g5_fails: 0`, `readcheck_fails: 0`).
- **Quality gate (`verification --dom-lint`):** `passed` (`disclose: []`) — saved at [video/verification/quality-gate-verification.json](video/verification/quality-gate-verification.json).

## Export & content package (completed)

- **Delivery render:** [exports/transportasi-umum-gratis.mp4](exports/transportasi-umum-gratis.mp4) (`1080×1920`, `30 fps`, `H.264 yuv420p` + `AAC 48 kHz stereo`, `96.63 s`, `74,050,903 bytes` / `70.6 MB`, SHA-256 `e153efb0c1cec94af16d5d918d811b961bb455292edf8d8bd7834a4f4a01e308`). Decoded frames at `0.05 s`, `55.0 s`, `95.0 s` visually inspected.
- **Quality gate (`export`):** `passed` (`disclose: []`, `-14.19 LUFS`, `-1.08 dBTP`, `longest_static_seconds: 0.0` across all 19 scenes, `hook-motion: 0.2 s`, `empty-frames: 0`, `end-hold: 0.0 s`) — saved at [video/verification/quality-gate-export.json](video/verification/quality-gate-export.json).
- **Content package:** [CONTENT_PACKAGE.md](CONTENT_PACKAGE.md) — recommended title *"Gimana Kalau Semua Transportasi Umum Gratis? (Simulasi Dua Dunia)"*, 2 alternatives, shared Indonesian caption with model transparency & `SOURCES.md` credit, hashtags, keywords, cover offset `2500 ms`, and verified delivery metadata.

## External delivery — Trypost drafts (completed)

- **Transport:** Trypost REST API (`trypost.py`, workspace `01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37`, `Admin's Workspace`).
- **Requested delivery:** `draft` only (no scheduling or live publication).
- **Receipt:** [PUBLISHING.json](PUBLISHING.json) (schema v2, verified export SHA-256 `e153efb0c1cec94af16d5d918d811b961bb455292edf8d8bd7834a4f4a01e308`).
- **Verified per-channel results:**
  1. **Instagram (`@duadunia.lab`, `instagram_reel`):** Draft ID `01a21073-5bfd-7072-b4b6-0c39ec3635c0` — `status: draft`, media attached (`01a21075-35b3-72f2-a653-6761976b5704`, `96.63 s`, `cover_offset_ms: 2500`).
  2. **YouTube (`@duadunia_lab`, `youtube_short`):** Draft ID `01a21075-87d6-71ed-9365-d52c1027a8d9` — `status: draft`, media attached (`01a21075-8794-71b2-b853-d706a6e5d3f0`, `96.63 s`, `meta.title` set).
  3. **Facebook (`Dua Dunia Lab`, `facebook_post`):** Draft ID `01a21075-c016-71ec-b375-185a4812cdc3` — `status: draft`, media attached (`01a21075-bfd3-717d-ab9d-f6e68019e778`, `96.63 s`; `facebook_post` selected because `96.63 s` exceeds `facebook_reel`'s 90 s cap).

## Review & next action

- **Current stage:** `publishing` (`complete` for `--delivery=draft`)
- **User approval:** Final delivery (verified export, `CONTENT_PACKAGE.md`, and 3 Trypost drafts) accepted by user (`"approve"`) on 2026-11-24.
- **Next action:** Drafts remain safely in `draft` status in Trypost (`Admin's Workspace`) until the user explicitly requests scheduling (`queue` / `--at`), live publication (`publish`), or a follow-up performance review after publication.
