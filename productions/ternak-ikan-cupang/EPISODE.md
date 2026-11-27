# Ternak Ikan Cupang di Halaman

## Brief

- **Slug:** `ternak-ikan-cupang`
- **Topic selection:** `topic_selection: user`. On 2026-11-27, after requesting `"carikan topik seputar ikan cupang"` with `--board=budidaya-di-halaman --automation=after-topic --delivery=queue`, the user replied `"setuju"`, accepting recommended Candidate #1: building a backyard *Betta splendens* breeding, fry-rearing, and jarred soliter-rack setup from an empty breeding box in a yard corner through 7 problem–improvement rounds to a stable system and first counted harvest.
- **Board:** `budidaya-di-halaman`, revision 10 (`editorial v9 / visual v5`, status `approved`), explicitly selected via `--board=budidaya-di-halaman`. Inherit its [direction](../../boards/budidaya-di-halaman/DIRECTION.md), [editorial framework v9](../../boards/budidaya-di-halaman/EDITORIAL.md), [visual specification v5](../../boards/budidaya-di-halaman/frame.md), [organic SFX kit](../../boards/budidaya-di-halaman/assets/sfx/manifest.json), and [production contract](CONTRACT.json).
- **Contract snapshot:** [CONTRACT.json](CONTRACT.json) copied from `boards/budidaya-di-halaman/CONTRACT.json` (`editorial v9 / visual v5`, normalized SHA-256 `6681a52a9464efab8b2c846a0b08b731e06fde1e9a947e9772b333d54eac9626`), validated via `episode_qa.py --contract`.
- **Overlap check:** Checked `TRACKER.json` and `productions/`. Existing `budidaya-di-halaman` episodes cover backyard aquaponics (`akuaponik-lele-dan-kangkung`, `aquaponik-pasang-surut`), Nile tilapia waste settling (`jejak-kotoran-kolam-nila`), BSF prepupal exit ramp (`maggot-jalan-ke-wadah`), leaf-lettuce wick planter (`pot-sumbu-selada`), container potatoes (`kentang-dalam-pot`), redclaw crayfish shelter pond (`kolam-lobster-air-tawar`), standalone catfish tarp pond (`kolam-lele-di-halaman`), dry-litter laying duck coop (`kandang-bebek-petelur-kering`), and horizontal 200 L plastic drum swamp eel pond (`kolam-belut-dalam-drum`). None covers *Betta splendens* (*ikan cupang*), bubble-nest spawning, fry micro-feeding, or jarred soliter racks.
- **Candidate comparison:** Candidate #1 was recommended over 9 distinct betta alternatives (PVC central-drain soliter rack, shallow tarp *lubukan* grow-out pond, recycled styrofoam hatchery box, *Moina/Daphnia* live-feed tub, outdoor UV mini-greenhouse rack, gallon-jar *grooming* rack, aerator-free planted betta tub, trickle-tray *Tubifex* rack, and shaded *Wild Betta* blackwater biotope) because it delivers the full beginner-friendly *"bikin ternak ikan cupang di halaman sendiri"* arc, brings a fresh visual evolution (breeding box → fry grow-out tub → tiered soliter jar rack), and naturally yields 7 distinct single-cause biological/structural rounds under Editorial v9 and Visual v5. *(No board performance analysis exists yet.)*
- **Provisional angle & research questions (awaiting source verification):**
  - Start on a bare yard corner with an empty breeding box/container, water, and a pair of *Betta splendens*, then evolve the exact same yard corner through ~7 compact single-cause rounds (pending verification in `SOURCES.md`):
    1. Male & female placed directly together fight/nip fins → transparent conditioning divider (*perjodohan*) + floating bubble-nest support & dried *ketapang* leaf (*Terminalia catappa*).
    2. Rain/wind destroys bubble nest & overflows shallow outdoor box → overhead rain/shade cover (*paranet*/plastik bening) + screened overflow/freeboard.
    3. Newly hatched fry ignore standard pellets & starve → remove male after free-swimming, feed infusoria / *Artemia* / *Moina* micro-feed.
    4. Crowded fry tank fouls quickly & standard scoop/hose sucks up fry → move to larger grow-out tub + mesh-tipped airline siphon (*sipon selang berkasa*) for gentle bottom cleaning.
    5. Entering month 2, growing males nip each other's fins → build tiered soliter jar rack (*rak toples soliter*) and sort males individually.
    6. Neighboring jarred males constantly flare and exhaust themselves → slip opaque cardboard/paper dividers (*sekat*) between jars.
    7. Males jump out of open jars overnight (or mosquito larvae/predators enter) → keep safe water freeboard + breathable mesh cover.
  - Follow with a stable-system check, a counted harvest monetization scene beside the finished rack (verified conservative per-spawn count × dated Indonesian wholesale/collector/ornamental-market price in `SOURCES.md`, labelled `estimasi`), and closing wide view + congratulation + consecutive `"bikin di halaman"` question + `@bikindihalaman.id` + `0.5 s` delivered (`0.625 s` at 1x) thumbnail end card.
- **Format & audio defaults (inherited from board):** Vertical 9:16 (`1080 × 1920`), authored at **90–112.5 s at 1x** (24 fps master restamped to 30 fps at **1.25x** = **72–90 s delivered**, pitch kept). Language: conversational second-person Indonesian (`"kamu"` referring singly to the backyard keeper). Board default voice: ElevenLabs **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh` from `boards/budidaya-di-halaman/AUDIO.json`, `eleven_v4`), BGM `none`, SFX `use` (board Visual v5 organic SFX library).

## Execution, review & delivery policy

```text
execution_policy: automation
automation_after: topic
automation_state: active
activating_decision: user acceptance ("setuju") of Candidate #1 from 10-topic shortlist (2026-11-27)
human_review: none for subsequent work
pre_render_authorization: delegated by the user's --automation=after-topic instruction after topic acceptance
endpoint: publishing
delivery: queue
schedule: account queue slots (Trypost)
trypost_transport: api
```

## Publishing targets

Inherited full default account list from `boards/budidaya-di-halaman/ACCOUNTS.json` (preflight verified live via Trypost REST API `trypost.py check` and `trypost.py accounts --all` on 2026-11-27: `Admin's Workspace` `01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37`, `publishes_directly: true`, all 3 accounts `connected` with `has_posting_schedule: true`, `timezone: Asia/Jakarta`):

```yaml
publishing_targets:
  source: board
  board_accounts_file: boards/budidaya-di-halaman/ACCOUNTS.json
  board_accounts_sha256: 1a909556b9081ab0a43a037baba6888e03306d539bd13e8b891a32ea336b7f30
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

## Preflight & resolved blockers (2026-11-27)

1. **Web research authorization (resolved):** On 2026-11-27 the user explicitly authorized `"1. pakai default search tool"` (`search_web`) because SearXNG MCP tools were disabled in this session. Deep research completed and verified against primary Indonesian fisheries/government and dated supplier pages in [SOURCES.md](SOURCES.md).
2. **ElevenLabs voice override (resolved):** On 2026-11-27 the user explicitly authorized `"2. pakai premade sound Roger"` — **Roger – Laid-Back, Casual, Resonant** (`CwhRBWXzGAHq8TQ4Fs17`, `eleven_v4`) as an `episode_override` on `elevenlabs_api` (`.env` free tier, `3,067` chars remaining; board default `Pribs` `5g0yKK2JwTRka0IG61Hh` returned HTTP 400 `voice_not_found`, and starter MCP had only `255` chars left).
3. **Trypost preflight:** Passed (`transport: api`, all 3 inherited accounts `connected` with active posting schedules).

## Research and hook selection (agent-selected under active automation)

Research verified pair conditioning with a transparent divider, dried *Terminalia catappa* (*daun ketapang*), bubble-nest care (~36 h hatch), outdoor rain/sun protection (*plastik bening* + *paranet*), day-4 micro-feed (infusoria/*Artemia*/*Moina*), week-5 grow-out transfer & gentle bottom siphoning (~30% change), month-2 male sorting into soliter jars, opaque dividers against chronic flaring, breathable jump lids, conservative 50-fish first-harvest count at ~3 months (10–12 weeks), and dated Indonesian wholesale pricing from Super Koi Nusantara (4 Sep 2026: Grade C *Halfmoon* Rp10.000–Rp20.000/ekor, using conservative lower bound **Rp10.000/ekor** → `50 ekor × Rp10.000 ≈ Rp500.000`, `estimasi grosir / Sep 2026`). Mapped in [SOURCES.md](SOURCES.md).

Hook options v1 follow Editorial v9's four-slot pattern, avoid repeating `kolam-belut-dalam-drum`'s opening verb (`rebahkan`) and connector (`habis itu`), and stay under the `10.0 s` first-sentence and `12.0 s` `"Tapi"` ceilings *(no board performance analysis exists yet)*:

1. **Option 1 (Selected — agent choice under active automation) — Territorial aggression surprise:**
   - *Mechanism:* Counter-intuitive behavioral clash — viewers expect putting a male and female together starts breeding immediately, so immediate fin-tearing fighting sparks instant curiosity.
   - *Spoken line (26 words; S1 = 18 words ≈ `7.6 s ≤ 10.0 s`; `"Tapi"` at word 19 ≈ `8.0 s ≤ 12.0 s`):* `"Kalo kamu taruh boks di halaman, terus kamu isi air dan sepasang cupang, kamu sudah punya ternak cupang. Tapi baru sebentar, siripnya langsung robek saling serang."`
   - *Frame 0 & `<1.0 s` motion:* Bare clay yard corner; within `0.25 s` hands set down an empty plastic breeding box on wooden blocks, water and a red/blue betta pair go in, then the male lunges tearing a fin fragment.
   - *On-screen line:* Progressive 46 px DM Sans ExtraBold captions matching the spoken line; thumbnail promise **Bikin ternak cupang / di sudut halaman** (yellow on **ternak cupang**).
   - *Promise:* Walks chronologically through all 7 betta-specific upgrades (transparent divider + ketapang, rain canopy + paranet, micro-feed, grow-out tub + mesh siphon, tiered soliter rack, cardboard dividers, mesh jump lids) to a counted first harvest.
2. **Option 2 — Weather crisis (bubble nest destroyed by rain):** `"Kalo kamu susun boks di halaman, lalu kamu isi air dan sepasang cupang, kamu sudah punya ternak cupang. Tapi pas hujan turun, sarang busanya hancur berantakan."` (Frame 0: bare yard corner, box stacked and filled, rain breaks bubble nest; skips conditioning step chronologically.)
3. **Option 3 — Fry feeding puzzle:** `"Kalo kamu siapkan boks di halaman, setelah itu kamu pijahkan sepasang cupang, kamu sudah punya ternak cupang. Tapi pas menetas, burayaknya lemas nggak mau makan."` (Frame 0: bare yard corner, box set up and hatched fry ignore oversized pellets; jumps past spawning & weather early.)

- `hook_selection: auto` (delegated under active `--automation=after-topic`). Selected **Option 1** because immediate territorial fin-tearing is uniquely iconic to *Betta splendens*, reads clearly on mute in a flat cutaway, and lets all 7 rounds progress in natural chronological lifecycle order (Day 0 → Day 4 → Month 1 → Month 2 → Month 3).

## Script check (v1 — agent-verified under active automation)

[SCRIPT.md](SCRIPT.md) v1 is built around Hook Option 1 across 11 scenes (18 events).

- **Spoken word count & budget:** **242 spoken words**. At Roger's measured pace (`2.37 wps` from `kolam-belut-dalam-drum`; fallback `2.40 wps`), predicted raw narration is `100.8–102.1 s`, predicted 1x film duration (including ~1.98 s quiet boundaries + ~2.2 s post-S10 tag hold + `0.625 s` end card) is **`105.6–106.9 s`**, fitting `90.0–112.5 s` 1x (`84.5–85.5 s` delivered at 1.25x). Re-check with `episode_qa.py --budget` after synthesis.
- **First sentence & `"Tapi"` turn:** Sentence 1 is **18 words** (predicted `7.5–7.6 s ≤ 10.0 s`). `"Tapi"` is word 19 (predicted `~7.9–8.0 s ≤ 12.0 s`). `"Tapi"` appears **once** in the entire script (hook only); Rounds 2–7 vary transitions (`Begitu hujan deras turun`, `Empat hari jalan`, `Sebulan kemudian`, `Masuk bulan kedua`, `Masalahnya`, `Suatu pagi`).
- **Cold-read & POV check:** Read all 242 spoken words standalone without headings or visual cues. `"kamu"` resolves cleanly to the single backyard keeper throughout; every actor (`sepasang cupang`, `betina`, `jantan`, `burayak`, `cupang jantan`) resolves from speech alone. Repairs applied before finalizing v1: (1) added explicit `"Setelah bertelur, kamu angkat betina, jantan jaga sarang busa"` in S02 so removing the male in S04 makes complete causal sense on audio alone; (2) removed a second `"tapi"` in S04; (3) tightened S07 `"Mentalnya kembali tenang"` → `"Mereka kembali tenang"` and S10 `"Di pengepul"` → `"Di grosir"` to match the verified wholesale price source.
- **Contract judged rules (script scope):**
  - `hook-frame`: **pass** — Bare yard corner at Frame 0 with box placement at `0.25 s` and 46 px captions.
  - `pictures-alone`: **pass** — Every scene specifies ordered visual sub-beats showing cause, fix, and test.
  - `event-density`: **pass** — 11 scenes / 18 distinct events beyond captions.
  - `motion-variety`: **pass** — Shot scales alternate (`wide` → `close cutaway` → `medium-wide` → `close cutaway` → `medium` → `medium-wide` → `close` → `medium` → `wide` → `medium` → `wide`; max same-shot run 1).
  - `subject-scale` & `vessel-scale`: **pass** — Breeding box, grow-out tub, soliter rack, jars, and harvest tray planned at ≥40% frame width with consistent yard landmarks.
  - `ear-test`: **pass** — Standalone cold-read passed with zero ambiguous pronouns or passive actor gaps.
  - `build-first`: **pass** — Hook Option 1 fills all four Editorial v9 slots verbatim with ordinary punctuation and fresh verb/connector (`taruh` / `terus`).
  - `shortfall-before-fix`: **pass** — 7 single-cause problem–improvement rounds (19–22 words / ~8.0–9.3 s each at 1x), distinct triggers, varied transitions (`"Tapi"` only once in S01).
  - `same-system`: **pass** — All installed components (breeding box + ketapang, clear rain roof + paranet, grow-out tub + mesh siphon, tiered soliter rack + cardboard dividers + mesh jump lids) remain visible together through S11.
  - `final-job`: **pass** — S09 shows the finished multi-container setup coping with afternoon rain and feeding before calling it stable.
  - `income-scene`: **pass** — S10 counts and packs conservative `50 ekor` beside the finished rack with world-anchored tag `50 ekor × Rp10.000 ≈ Rp500.000` (`estimasi grosir / Sep 2026`, sourced from Super Koi Nusantara 4 Sep 2026), rounded spoken figures, ≥3 s 1x hold, no profit/payback claim.
  - `event-map`: **pass** — 18 events (within 15–19); every component enters on screen.
  - `closing-lines` & `closing-signature`: **pass** — Congratulation naming the built betta setup + next-build question with consecutive `"bikin di halaman"`, yellow hold + `@bikindihalaman.id`, hard cut to `0.625 s` 1x end card.
  - `reframing`, `living-world`, `event-sfx`: **pass** — Plans beat-level push-ins/pans/micro-impacts, 4-plane 2.5D parallax & reactive weather, and frame-locked organic SFX from board Visual v5 library (`bgm: none`).

## Visual storyboard (passed — agent-verified under active automation)

- Initialized HyperFrames 0.9.77 inside [`video/`](video/) (`--skip-skills`) with board Visual v5 runtime (`video/assets/world-v5.js`), custom betta world (`video/assets/betta-world.js`), generator (`video/build_project.py`), and storyboard builder (`video/build_storyboard.py`).
- Produced [`video/STORYBOARD.md`](video/STORYBOARD.md), 11 scene stills (`video/boards/stills/`), 25 sub-beat poses (`video/boards/poses/`), [`video/boards/storyboard.html`](video/boards/storyboard.html), and [`video/boards/storyboard.png`](video/boards/storyboard.png) (`1600 × 7361`, 36/36 images loaded, visually inspected and refined for fin containment, 2-line end-card headline `Ternak cupang / di sudut halaman`, clean S10 tray/tag layout, Frame 0 empty box, and ketapang leaf scale).
- Passed `storyboard_lint.py --strict` (`0` errors, `0` warnings) and `episode_qa.py --stage storyboard` (`disclose: []`, [`video/verification/quality-gate-storyboard.json`](video/verification/quality-gate-storyboard.json)).

## Audio & sound design (verified & natively listened)

- **Narration (`episode_override`):** Single ElevenLabs `eleven_v4` take with user-authorized premade voice **Roger** (`CwhRBWXzGAHq8TQ4Fs17`, `elevenlabs_api`, `request_sha256: aeb8290f7b4f6e51daf686a5f161a3f4559d1a78bd475fb677b70961fcaaf7c5`): `video/.media/audio/voice/narration-aeb8290f7b4f6e51daf6.mp3` (`101.36 s`, exact `242` words). Natively listened via `read_file`: natural Indonesian delivery, zero tags read aloud, zero clipped syllables.
- **Boundary placement & timing:** Placed via `video/place_and_sync.py` (`audio_boundaries.place()`): `video/assets/audio/narration.wav` (`107.18 s`, normalized once to `-14.0 LUFS / -1.5 dBTP`). Exact 1x composition: **`108.000 s`** (`2592` frames @ 24 fps), `first_sentence_end_s = 6.57 s <= 10.0 s`, `tapi_turn_start_s = 6.89 s <= 12.0 s`, `s10_tag_hold_1x_s = 3.296 s >= 3.0 s`, end card `107.375–108.000 s` (`0.625 s` at 1x). Passed `audio_boundaries.py` (`10/10`).
- **SFX & BGM:** `bgm: none`; 43 word-anchored organic backyard SFX cues from the board Visual v5 CC0/Pixabay kit in `video/sound_design.json`. Passed `sound_design.py --apply` and `--check`.

## Independent review & verification (passed)

- Fresh-context `research` subagent (`7e3554bf-6076-4954-b7f4-f24df1f41b4e`) audited the proof render:
  - **Pass 1 (`HOLD`):** Found 6 P0 and 6 P1 defects (clipped S11 keeper, S10 roof-stacked table/floating tag beam, S09 keeper placement & missing feeding surge, S04–S08 premature fix visuals/SFX, flat S07 flaring/droop, S11 tray overlap, storm sun, stray canopy bar, cut-off S07 rack legs, doc drift).
  - **Pass 2 (`APPROVE FOR DELIVERY RENDER`):** After fixing all 6 P0s and all 6 P1s (`composition_sha256: 94bb678bc275048a1af35f16b27f991f1f1cb16afcb2c1d8bd1af027271a35ea`), passed **18/18 judged rules**, **0 open P0s**, and **7/7 rubric dimensions at 8–9/10** (`style_fidelity: 8`, `concept_wow: 8`, `motion_craft: 8`, `design_typography: 8`, `finish_texture: 8`, `sound_sync: 9`, `technical: 9`), with 2 minor open P1s recorded in [`video/REVIEW.md`](video/REVIEW.md).
- Natively listened to revised `video/verification/proof-mix.mp3` (`listening: agent`).
- Passed `episode_qa.py --stage verification --dom-lint` (`disclose: []`, [`video/verification/quality-gate-verification.json`](video/verification/quality-gate-verification.json)).

## Export & content package (passed)

- **1x master:** `video/verification/master-24fps.mp4` (`43,934,459` bytes, SHA-256 `55bbd5d1ee482eb336807d6641a66f6059d19a2d82b7f54c0516139c502c7b77`); passed `audio_boundaries.py --export` (`10/10`) and `sound_design.py --export` (`43/43` cues within `±0.5 ms`, median vocal-band SNR `27.71 dB`, longest severe masking `0.025 s`).
- **Delivered 1.25x video:** [`exports/ternak-ikan-cupang.mp4`](exports/ternak-ikan-cupang.mp4) (`21,142,701` bytes / `21.14 MB`, SHA-256 `102e77d4d6fb1bea0612a8fd4b41e539f6488a65bcf80ab2d458cef03f1247c3`, `1080 × 1920 @ 30 fps`, exact **`86.400 s` / `86400 ms`**, `cover_offset_ms: 86150`, two-pass loudnorm **`-14.04 LUFS` / `-2.79 dBTP`**, full decode clean). Natively listened to 1.25x delivery mix (`video/verification/delivery-mix-1.25x.mp3`) and visually checked delivered frames.
- **Delivered thumbnail:** [`exports/thumbnail.png`](exports/thumbnail.png) (`439,242` bytes, SHA-256 `726bf946327fd4e996e6888c50c0370ce4ec575768a21c03508d885c9575aa49`).
- **Delivered sidecar SRT:** [`exports/ternak-ikan-cupang.srt`](exports/ternak-ikan-cupang.srt) (`35` cues, 1.25x scaled, SHA-256 `7010f276553c1c64bcad5277d0aa4a73a99515a8726423999c79df63ad89daf4`).
- **Export gate:** Passed `episode_qa.py --stage export --film exports/ternak-ikan-cupang.mp4` (`disclose: []`, [`video/verification/quality-gate-export.json`](video/verification/quality-gate-export.json)).
- **Shared content package:** [`CONTENT_PACKAGE.md`](CONTENT_PACKAGE.md) (recommended title `Bikin Tempat Ternak Ikan Cupang di Halaman dari Boks sampai Rak Soliter`, shared caption with schematic & wholesale-estimate disclosure, 5 hashtags including `#bikindihalaman`, editorial keywords, and verified delivery metadata).

## Google Drive archive (synced)

- **Folder:** [`budidaya-di-halaman/ternak-ikan-cupang`](https://drive.google.com/drive/folders/1o7lE1q7Vp_prHtwjsvZABZVHQ7TedeA7) (`folder_id: 1o7lE1q7Vp_prHtwjsvZABZVHQ7TedeA7`, synced `2026-11-27T08:06:37Z` via `gdrive.py` using Doppler):
  - `ternak-ikan-cupang.mp4` (`21,142,701` bytes, MD5 `f7f9379297e8d0d61b7fb3d9fda97629`, `uploaded`)
  - `thumbnail.png` (`439,242` bytes, MD5 `fb56f38cd37aa24af85aeb0b10de320a`, `uploaded`)
  - `ternak-ikan-cupang.srt` (`2,935` bytes, MD5 `a4806915882d01b00d8a4e6ebe391eab`, `uploaded`)
  - `CONTENT_PACKAGE.md` (`6,300` bytes, MD5 `ed35884b1cfcd704bab987a29c365212`, `uploaded`)

## Publishing — Trypost queue scheduling (complete)

- **Transport & workspace:** Trypost REST API (`trypost.py`, `transport: api`) on `Admin's Workspace` (`01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37`, `publishes_directly: true`).
- **Receipt:** [`PUBLISHING.json`](PUBLISHING.json) (schema v2; `exports/ternak-ikan-cupang.mp4` uploaded once and reused via workspace media ID within the same workspace; all 3 posts verified via `GET /posts/{id}`).
- **Per-channel observed status (queued/scheduled — NOT live-published yet):**
  - **Instagram `@bikindihalaman.id`** (`01a2022d-bc57-71d8-9217-6e0319cb6c03`, `instagram_reel`): post `01a21953-3b0a-7239-af9e-8054d5b45c07`, media `01a21953-3739-70a4-9e4b-0e262db4a732` (`cover_offset_ms: 86150`), status **`scheduled`** (`queue`), scheduled **`2026-11-28 02:43:00` UTC** (`2026-11-28 09:43:00 WIB`).
  - **YouTube `@bikindihalaman_id`** (`01a202dc-0e4a-72ae-bec8-589ab7f90045`, `youtube_short`): post `01a21953-3f81-73b7-b16f-c60599cc6426`, media `01a21953-4d92-7002-9aba-0caa70bd8451` (`meta.title` set), status **`scheduled`** (`queue`), scheduled **`2026-11-28 05:19:00` UTC** (`2026-11-28 12:19:00 WIB`).
  - **Facebook `Bangun Di Halaman`** (`01a2036c-5179-70c6-b908-25118446326d`, `facebook_reel`): post `01a21953-51f0-7365-97d1-471f4a93c594`, media `01a21953-65f3-728f-9af4-bdd526a96552`, status **`scheduled`** (`queue`), scheduled **`2026-11-28 04:33:00` UTC** (`2026-11-28 11:33:00 WIB`).

## User approval (2026-11-27)

- On 2026-11-27 (`07:48+07:00`), the user explicitly approved the completed episode, delivered export, shared content package, and Trypost queue schedule (`"approve, commit, dan buatkan pr ke main"`), authorizing git commit and pull request creation to `main`.

## Current state

- `stage: publishing`
- `status: complete`
- `approval: user_approved (2026-11-27)`
- `next_action: optional manual upload of exports/thumbnail.png as custom cover in YouTube Studio (@bikindihalaman_id) and Meta Business Suite (Bangun Di Halaman), then run a post-publication performance review snapshot after 2026-11-28 queue slots publish.`
