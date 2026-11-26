# Kolam Belut dalam Drum Bekas

## Brief

- **Slug:** `kolam-belut-dalam-drum`
- **Topic selection:** `topic_selection: user`. On 2026-11-25, after requesting `"carikan topik"`, the user replied `"setuju"` to the recommended candidate #1 from the 10-topic shortlist: building a backyard Asian swamp eel (*Monopterus albus*) rearing drum from an unused 200 L plastic drum in a bare yard corner through seven problem–improvement rounds to a stable system and first weighed harvest.
- **Board:** `budidaya-di-halaman`, revision 10 (`editorial v9 / visual v5`, status `approved`), explicitly selected via `--board=budidaya-di-halaman`. Inherit its [direction](../../boards/budidaya-di-halaman/DIRECTION.md), [editorial framework v9](../../boards/budidaya-di-halaman/EDITORIAL.md), [visual specification v5](../../boards/budidaya-di-halaman/frame.md), [organic SFX kit](../../boards/budidaya-di-halaman/assets/sfx/manifest.json), and [production contract](CONTRACT.json).
- **Contract snapshot:** [CONTRACT.json](CONTRACT.json) copied from `boards/budidaya-di-halaman/CONTRACT.json` (`editorial v9 / visual v5`, SHA-256 `6681a52a9464efab8b2c846a0b08b731e06fde1e9a947e9772b333d54eac9626`), validated via `episode_qa.py --contract`.
- **Overlap check:** Checked `TRACKER.json` and `productions/`. Existing `budidaya-di-halaman` episodes cover backyard aquaponics (`akuaponik-lele-dan-kangkung`, `aquaponik-pasang-surut`), Nile tilapia waste settling (`jejak-kotoran-kolam-nila`), BSF prepupal exit ramp (`maggot-jalan-ke-wadah`), leaf-lettuce wick planter (`pot-sumbu-selada`), container potatoes (`kentang-dalam-pot`), redclaw crayfish shelter pond (`kolam-lobster-air-tawar`), and standalone catfish tarp pond (`kolam-lele-di-halaman`). None covers Asian swamp eel (*Monopterus albus*), mud-substrate fermentation, or horizontal cut plastic drum builds.
- **Candidate comparison:** Candidate #1 was recommended over nine non-overlapping alternatives (Tubifex trickle tray rack, tiered quail cage, shaded oyster-mushroom rack, Moina/Daphnia live-feed tub, gourami leaf-feeding pond, betta breeding/grow-out rack, covered snakehead tank, vertical PVC strawberry tower, and stingless Trigona bee box) because aquaculture anchors the board while a horizontal 200 L plastic drum breaks the rectangular tarp-pond silhouette of the prior two episodes, supports seven diverse single-cause rounds for Editorial v9, and exploits Visual v5's 4-plane 2.5D cutaway and weather/SFX system. *(No board performance analysis exists yet to weigh historical metrics.)*
- **Angle & researched event chain (pending hook confirmation):** Start at a bare backyard corner with an empty 200 L plastic drum. Cut open the top lengthwise, brace it horizontally on chocks, scoop in mud/straw + water, and stock ~2 kg (~160–200) uniform 10–12 cm *Monopterus albus* juveniles right away, then evolve the exact same drum through **7 compact single-cause rounds** (6–10 s each at 1x, varied natural Indonesian transitions; `"Tapi"` reserved for the opening hook turn):
  1. **Unfermented mud fermentation heat/gas** → hold eels briefly, ferment mud + chopped straw + EM4 for ~2 weeks until cool and dark, flush surface water, restock → eels burrow comfortably.
  2. **Midday sun overheating & bright light stress** → add floating water hyacinth (*eceng gondok*, ~3/4 surface) and stretch overhead shade net (*paranet*) → water cools and eels stay sheltered.
  3. **Heavy night rain raising water to the wet rim & eels slipping out** → cut a screened overflow pipe (*pipa pelimpah berkasa halus*) below the rim leaving freeboard → excess rain drains while eels stay inside.
  4. **Daytime feed left untouched and rotting (nocturnal species)** → shift feeding to measured late-afternoon/evening portions (after 17:00) beneath the plants → eels strike immediately.
  5. **Stagnant surface water turning murky brown & foul (ammonia)** → install a screened low drain pipe and gentle PVC trickle-water inlet → water stays fresh and odor clears.
  6. **Backyard predators (cat/birds) eyeing the open drum** → fit a removable wire-mesh frame lid (*tutup rangka kawat kasa*) over the top opening → drum stays protected day and night.
  7. **Size disparity & larger eels biting smaller ones (~month 2)** → scoop and sort by size, moving smaller eels to a matching second drum beside the first → even growth without losses.
  Follow with a **stable-system check** (rain + evening feed handled smoothly by all installed features), a **monetization scene** beside the drum (drain water via bottom pipe, lift plants, scoop harvest into basin and hang on scale with tag `6 kg × Rp72.500 ≈ Rp435.000`, `estimasi pasar Jatim · Nov 2026` from FishInfo DKP Jatim, rounded spoken figures, no profit/payback claim), and the **closing wide view** + congratulation + consecutive `"bikin di halaman"` question + `@bikindihalaman.id` + `0.5 s` delivered (`0.625 s` at 1x) thumbnail end card. See [SOURCES.md](SOURCES.md).
- **Format & audio defaults (inherited from board):** Vertical 9:16 (`1080 × 1920`), authored as a 1x composition of **90–112.5 seconds** (24 fps master restamped to 30 fps at **1.25x** delivery speed = **72–90 s delivered**, pitch kept). Language: casual second-person Indonesian (`"kamu"` referring singly to the backyard keeper). Voice: ElevenLabs **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh` from `boards/budidaya-di-halaman/AUDIO.json`, `eleven_v4`), BGM `none`, SFX `use` (board Visual v5 organic SFX library + documented hybrid additions).
- **Word budget note:** `episode_qa.py --budget 250 --voice 5g0yKK2JwTRka0IG61Hh --production productions/kolam-belut-dalam-drum` reported no locally cached measured audio for Pribs in this clone. Plan at `2.40–2.61 wps` (fallback `2.40 wps` and Pribs's archived `2.61 wps`, ~235–260 spoken words for `90–112.5 s` 1x) and re-budget after the first take.
- **Execution, review & delivery policy:**

```text
execution_policy: automation
automation_after: script
automation_state: pending
human_review: defaults through script approval
pre_render_authorization: pending activation
endpoint: publishing
delivery: queue
schedule: account queue slots (Trypost)
trypost_transport: api
```

## Publishing targets

Inherited full default account list from `boards/budidaya-di-halaman/ACCOUNTS.json` (preflight verified live via Trypost REST API `trypost.py check` and `trypost.py accounts --all` on 2026-11-25: all 3 accounts `connected`, `has_posting_schedule: true`, `timezone: Asia/Jakarta`, workspace `publishes_directly: true`):

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

Research verified drum-based *Monopterus albus* preparation, substrate fermentation heat/gas, temperature/light sensitivity, rain-overflow escapes, nocturnal feeding, ammonia/drainage, predators, size-disparity grading, conservative 1-drum yield (~6 kg from 2 kg / 160–200 juveniles over 3–4 months), and dated provincial market pricing (FishInfo DKP Jatim, 20–26 Nov 2026: **Rp72.500/kg**). All claims and boundaries are documented in [SOURCES.md](SOURCES.md).

Hook options v1 follow Editorial v9's four-slot pattern (`Kalo kamu {aksi pertama}, {konjungsi temporal} kamu {aksi kedua}, kamu sudah punya {sistem}. Tapi {masalah}.`), avoid repeating the previous episode's opening verb (`tancap`) and connector (`lalu`), vary mechanism and opening problem, and fit comfortably within the contract's `10.0 s` first-sentence and `12.0 s` `"Tapi"` ceilings. *(No board performance analysis exists yet to weigh historical hook mechanisms.)*

### Option 1 (Recommended) — Biological/chemical surprise: raw unfermented mud drives eels up listlessly
- **Mechanism:** Counter-intuitive biological mismatch — viewers assume mud + water is immediately ideal for eels, so seeing eels rise weakly out of fresh mud sparks instant curiosity.
- **Spoken line (27 words; sentence 1 = 18 words ≈ 6.9–7.5 s; `"Tapi"` at word 19 ≈ 7.3–7.9 s):**
  > “Kalo kamu belah bagian atas drum bekas, terus kamu isi lumpur sawah dan lepas bibit belut, kamu sudah punya kolam belut. Tapi besok paginya belutnya malah naik lemas ke permukaan.”
- **Frame 0 & `<1 s` motion:** Bare warm-clay backyard corner with a weathered blue 200 L plastic drum ready; within `0.3 s` the keeper cuts open the top horizontal window, braces the drum on chocks, scoops in fresh mud/straw, pours water and releases juvenile eels, then a quick night-to-morning light shift shows warm gas bubbles rising from the mud as pale, sluggish eels poke up at the surface.
- **On-screen line:** Progressive 46 px DM Sans ExtraBold captions (`Kalo kamu belah bagian atas drum bekas,` / `terus kamu isi lumpur sawah dan lepas bibit belut,` / `kamu sudah punya kolam belut.` / `Tapi besok paginya belutnya malah naik lemas ke permukaan.`). Thumbnail/cover promise: **BIKIN KOLAM BELUT DI DRUM BEKAS** (yellow on **KOLAM BELUT**).
- **Promise:** Explains why fresh unfermented mud traps heat and fermentation gas, then walks chronologically through all 7 drum upgrades (fermentation, shade & water hyacinth, screened rain overflow, evening feeding, bottom drain & trickle, predator mesh lid, and size grading) to a weighed first harvest.

### Option 2 — Physical escape crisis: slippery eels crawl over the wet rim during night rain
- **Mechanism:** High-stakes escape drama — opens on the vivid fear of slippery eels crawling out of a yard drum when rain fills it to the lip.
- **Spoken line (28 words; sentence 1 = 20 words ≈ 7.7–8.3 s; `"Tapi"` at word 21 ≈ 8.0–8.7 s):**
  > “Kalo kamu rebahkan drum plastik di sudut halaman, habis itu kamu isi lumpur dan lepas bibit belut, kamu sudah punya kolam belut. Tapi pas hujan malamnya belutnya merayap keluar.”
- **Frame 0 & `<1 s` motion:** Bare yard corner with an upright empty plastic drum; within `0.3 s` the drum tips onto its side on chocks with its top cut open, mud/water and eels go in, then sudden dark night rain lifts water to the lip and a slick eel slithers over the wet edge.
- **On-screen line:** Progressive 46 px captions (`Kalo kamu rebahkan drum plastik di sudut halaman,` / `habis itu kamu isi lumpur dan lepas bibit belut,` / `kamu sudah punya kolam belut.` / `Tapi pas hujan malamnya belutnya merayap keluar.`). Cover promise: **BELUT KABUR DARI DRUM HALAMAN?** (yellow on **KABUR DARI DRUM**).
- **Promise:** Shows how freeboard and a screened overflow pipe stop rain-night escapes first, then solves mud fermentation, midday heat, nocturnal feeding, ammonia drainage, predators, and grading through to first harvest.

### Option 3 — Behavioral puzzle: daytime feed sits untouched and rots in bright sun
- **Mechanism:** Everyday husbandry puzzle — viewers used to catfish expect an instant feeding frenzy, so untouched rotting food in bright daylight creates immediate intrigue.
- **Spoken line (28 words; sentence 1 = 19 words ≈ 7.3–7.9 s; `"Tapi"` at word 20 ≈ 7.7–8.3 s):**
  > “Kalo kamu potong sisi atas drum plastik, setelah itu kamu isi lumpur dan tebar bibit belut, kamu sudah punya kolam belut. Tapi tiap dikasih makan siang, pakannya malah membusuk.”
- **Frame 0 & `<1 s` motion:** Bare yard corner with an empty drum and hand saw; within `0.3 s` the top cutout lifts off, mud/water and eels go in, then daytime worms/pellets drop into sunlit water while zero eels emerge and a murky brown cloud forms around the untouched feed.
- **On-screen line:** Progressive 46 px captions (`Kalo kamu potong sisi atas drum plastik,` / `setelah itu kamu isi lumpur dan tebar bibit belut,` / `kamu sudah punya kolam belut.` / `Tapi tiap dikasih makan siang, pakannya malah membusuk.`). Cover promise: **BIKIN KOLAM BELUT TANPA GALI TANAH** (yellow on **KOLAM BELUT**).
- **Promise:** Reveals why nocturnal, light-shy eels refuse daytime meals in an open drum, then solves shade/water hyacinth, mud fermentation, rain overflow, bottom water renewal, predator mesh, and grading through to first weighed harvest.

**Recommendation:** Option 1. Skipping the 14-day mud fermentation is the #1 beginner pitfall specific to mud-based eel drums, delivers an immediate counter-intuitive surprise ("lumpur mentah justru bikin belut lemas"), and unlocks the cleanest chronological progression through all 7 rounds without reordering setup steps.

`hook_selection: user`. On 2026-11-25 the user replied `"opsi 2"`, selecting **Option 2 (Physical escape crisis: rain-night rim escape)**. Its opening wording is preserved verbatim in [SCRIPT.md](SCRIPT.md) v1.

## Script review

[SCRIPT.md](SCRIPT.md) v1 is built around Hook Option 2 with 11 scenes (18 meaningful events: premature horizontal drum build + rain-escape hook, 7 distinct single-cause problem–improvement rounds, stable-system check, hanging-scale income scene, and closing wide shot + 0.5 s delivered thumbnail end card).

### Script check (v1)

- **Spoken word count & budget output:** **250 spoken words**. Local workspace clone has no cached audio for Pribs (`5g0yKK2JwTRka0IG61Hh`), so `episode_qa.py --budget` reported no measured pace and will be re-run after the first take. Using both the fallback rate (`2.40 wps`) and Pribs's archived pace (`2.61 wps`): predicted narration is `95.8–104.2 s`, predicted 1x composition duration (including `~3.5 s` pauses/tag hold + `0.625 s` end card) is **`99.9–108.3 s`** (`79.9–86.6 s` delivered at 1.25x), fitting the contract's `90.0–112.5 s` 1x window with margin on both sides.
- **First sentence & `"Tapi"` turn:** Sentence 1 (`"Kalo kamu rebahkan drum plastik di sudut halaman, habis itu kamu isi lumpur dan lepas bibit belut, kamu sudah punya kolam belut."`) is **22 words** (predicted `8.43–9.17 s` ≤ `10.0 s` contract ceiling). `"Tapi"` begins at word 23 (predicted `~8.6–9.4 s` ≤ `12.0 s` contract ceiling). `"Tapi"` appears **once** across the entire script (hook only); Rounds 2–7 use varied natural Indonesian transitions (`Besok paginya`, `Pas tengah hari`, `Giliran kamu tebar pakan siang`, `Beberapa minggu jalan`, `Suatu pagi`, `Masuk bulan kedua`).
- **Selected hook three parts (Option 2):**
  - *Spoken line:* “Kalo kamu rebahkan drum plastik di sudut halaman, habis itu kamu isi lumpur dan lepas bibit belut, kamu sudah punya kolam belut. Tapi pas hujan malamnya belutnya merayap keluar.”
  - *Frame 0 & `< 1.0 s` motion:* Bare clay yard corner with upright empty blue 200 L plastic drum; within `0.25 s` the drum tips horizontally onto chocks with top cut open, mud/water and eels go in, then dark night rain lifts water to the wet rim as an eel slithers over.
  - *On-screen line:* Progressive 46 px DM Sans ExtraBold captions matching the spoken line; thumbnail/end-card promise **BIKIN KOLAM BELUT / DI DRUM BEKAS** (yellow `#FFD44D` on **KOLAM BELUT**).
- **Cold-read result & repairs:** Read all 250 spoken words continuously without headings or visual cues. `"kamu"` resolves unambiguously to the single backyard keeper throughout; every problem, fix, and result follows from speech alone. Four ear-clarity repairs applied before presenting v1: (1) S2 replaced `"bibirnya"` with `"bibir drum"`; (2) S3 replaced `"amankan dulu"` with `"pindahkan belutnya"` so the moved subject is explicit; (3) S4 separated water hyacinth placement from overhead paranet (`"isi eceng gondok lalu pasang paranet di atasnya"`); (4) S7 changed `"Besoknya utuh lagi"` to `"Besoknya jumlahnya utuh"`.
- **Contract judged rules (script scope):**
  - `hook-frame`: **pass** — Frame 0 opens on the bare yard corner and empty blue drum with tipping motion at `0.25 s` and 46 px phone-readable captions.
  - `pictures-alone`: **pass** — Every scene specifies ordered visual sub-beats depicting cause, installation, and visible retest without relying on text.
  - `event-density`: **pass** — All 11 scenes / 18 events introduce a distinct construction change, operating check, or consequence beyond captions.
  - `motion-variety`: **pass** — Shot scales alternate cleanly (`wide` → `close` → `medium` → `medium-wide` → `close` → `medium` → `medium-wide` → `close` → `wide` → `medium` → `wide`, zero adjacent repeats).
  - `subject-scale` & `vessel-scale`: **pass** — Horizontal drum cutaway, fittings, and hanging scale are planned at ≥40% frame width with persistent yard landmarks.
  - `ear-test`: **pass** — Standalone cold-read passed after the 4 ear-clarity repairs above; single `"kamu"` POV throughout.
  - `build-first`: **pass** — Hook Option 2 fills all 4 Editorial v9 slots verbatim with ordinary punctuation, starts on an unused drum in a bare corner, puts the drum into use, and turns on observable rain-night escape within time limits.
  - `shortfall-before-fix`: **pass** — 7 single-cause problem–improvement rounds after the hook (20–22 words / ~7.7–9.2 s each at 1x), each fix tested on screen across 7 distinct triggers (rain escape, unfermented mud gas/heat, midday heat/light, nocturnal feeding, ammonia fouling, cat predator, cannibalism/size gap), with varied transitions and `"Tapi"` only in the hook.
  - `same-system`: **pass** — Every upgrade (chocks, screened overflow, fermented dark mud, water hyacinth, paranet, bottom drain valve, trickle pipe, wire-mesh lid, second grading drum) stays visible on the same site through Scene 11.
  - `final-job`: **pass** — Scene 9 shows the completed drums coping with rain and evening feeding before calling the setup stable.
  - `income-scene`: **pass** — Scene 10 weighs conservative `6 kg` harvest beside the finished drum with world-anchored price tag `6 kg × Rp72.500 ≈ Rp435.000` (`estimasi pasar Jatim · Nov 2026`, sourced from FishInfo DKP Jatim 20–26 Nov 2026), rounded spoken figures, ≥3 s 1x hold, no profit/payback/guarantee claim.
  - `event-map`: **pass** — 18 events (within 15–19); every component (including the second drum in S8) enters visibly on screen.
  - `closing-lines`: **pass** — Ends with congratulation naming the drum eel pond + next-build question containing consecutive `"bikin di halaman"`; no intro or follow prompt.
  - `closing-signature`: **pass** — Holds yellow on `"bikin di halaman"`, fades in `@bikindihalaman.id`, hard cuts to `0.625 s` 1x (`0.5 s` delivered) thumbnail end card.
  - `reframing`: **pass** — Plans beat-level event push-ins (wet rim escape, bottom drain install, size-gap bite), lateral tracking (paranet pull, scoop to drum 2), micro-impact settles, and gentle living drift (no dead-freeze > 3 s).
  - `living-world`: **pass** — Plans 4-plane 2.5D parallax, reactive weather/time-of-day shifts (sunny → night storm → morning → harsh midday → dusk → rainy evening → golden harvest), and calm soil behind the caption band.
  - `event-sfx`: **pass** — Every scene maps frame-accurate organic SFX from the board Visual v5 library with `bgm: none`.

- `script_approval: user` (2026-11-25: `"approce"`, approving [SCRIPT.md](SCRIPT.md) v1, 250 spoken words, 11 scenes).

## Active automation & delivery policy (activated 2026-11-25)

```text
execution_policy: automation
automation_after: script
automation_state: active
activating_decision: user approval of SCRIPT.md v1 (2026-11-25)
human_review: none for subsequent work
pre_render_authorization: delegated by the user's --automation=after-script instruction after script approval
endpoint: publishing
delivery: queue
schedule: account queue slots (Trypost)
trypost_transport: api
```

- **Preflight (2026-11-25):**
  - Trypost transport: `api` (`trypost.py check` OK on `Admin's Workspace` `01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37`; all 3 inherited accounts verified `connected` with active posting schedules).
  - ElevenLabs transport: `elevenlabs_api` (`narration.py --check-api` OK, `tier: free`, `0 / 10,000` chars used; `elevenlabs` CLI `logged_in: false`). **Voice preflight note:** board default voice `Pribs` (`5g0yKK2JwTRka0IG61Hh`) returned HTTP 400 `voice_not_found` on this free-tier API key; will finish the full independent visual storyboard first, then resolve voice authorization before synthesis.

## Visual storyboard (agent-verified under active automation)

- **Storyboard verification:** `storyboard_verification: agent (active automation)` (2026-11-25).
- **Artifacts:** [video/BRIEF.md](video/BRIEF.md), [video/STORYBOARD.md](video/STORYBOARD.md) (`11` frames, `103.625 s` estimated 1x, all non-final read gaps `<= 3.0 s`, alternating shot scales with max run `1`, max push streak `1`), [video/boards/storyboard.html](video/boards/storyboard.html), [video/boards/storyboard.png](video/boards/storyboard.png) (`1600 × 8718`, `36/36` images loaded, `0` broken), 11 scene stills in `video/boards/stills/`, and 25 hook/motion poses in `video/boards/poses/`.
- **Visual inspection & polish:** Inspected `contact-sheet-1.jpg`, `contact-sheet-2.jpg`, `hook-0.0s.png`, `hook-3.0s.png`, `frame-00-at-9.2s.png`, `frame-07-at-71.9s.png`, `frame-09-at-91.6s.png`, `frame-10-at-101.5s.png`, and `11-b-end.png`. Applied and verified 7 visual polish fixes: (1) centered upright drum pivot in `hook-0.0s`, (2) foreground wooden chocks clearly visible beneath the cut drum, (3) unmistakable wet-rim escape eel arch in `s01`, (4) clean Drum 1 / Drum 2 spacing in `s08`/`s09`/`s11` with zero pipe collision, (5) closed Drum 1 mesh lid and lifted lower landmark drums above the `s10` caption band, (6) keeper positioned clear of the left paranet post in `s11` plus dimmed thumbnail clouds behind the dark `#281D18E6` end-card panel, and (7) `data-layout-allow-overflow` on `<canvas>`.
- **Checks & gates:**
  - `npx hyperframes check --json`: `0` lint/runtime/layout/contrast errors (`24/24` contrast passed; only expected pre-audio `film_silent` warning and `#captions` bottom-band safe-zone hint).
  - `storyboard_lint.py --production productions/kolam-belut-dalam-drum --strict`: **passed** (`frame_count: 11`, `max_push_streak: 1`, `text_dominated_share: 0.0`, `errors: []`, `warnings: []`).
  - `episode_qa.py --production productions/kolam-belut-dalam-drum --stage storyboard`: **passed** (`disclose: []`) — [video/verification/quality-gate-storyboard.json](video/verification/quality-gate-storyboard.json).

## Audio stage (resolved & verified)

- **Blocker resolved (2026-11-25):** Board default voice **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh` from `boards/budidaya-di-halaman/AUDIO.json`) returned HTTP 400 `voice_not_found` on the configured free-tier `ELEVENLABS_API_KEY`. The user explicitly authorized ElevenLabs **Roger** (`CwhRBWXzGAHq8TQ4Fs17`) as an `episode_override` and instructed active automation to proceed through Trypost queue scheduling.
- **Narration synthesis (1 take, `elevenlabs_api`, `eleven_v4`):** [video/.media/audio/voice/narration-719ccc96e5f2718885a8.mp3](video/.media/audio/voice/narration-719ccc96e5f2718885a8.mp3) (`105.482 s`, exact `250` spoken words matching approved [SCRIPT.md](SCRIPT.md) v1; measured pace `2.37 wps`, `episode_qa.py --budget` `fits: true`; recorded in [video/audio_request.json](video/audio_request.json) and [video/audio_meta.json](video/audio_meta.json)).
- **Raw take listening (`listening: agent`):** Natively listened via `view_file` to `narration-719ccc96e5f2718885a8.mp3` — zero delivery tags read aloud, clear Indonesian pronunciation across all aquaculture/pricing terms, zero clipped syllables, natural conversational tone shifts.
- **Quiet boundary placement & normalization:** Placed via [video/place_and_sync.py](video/place_and_sync.py) calling `audio_boundaries.place()` (`0.22 s` pauses on S01–S09, `2.05 s` post-S10 pause giving **`3.063 s >= 3.0 s`** 1x full price-tag hold) and normalized once to `−14.0 LUFS / −1.5 dBTP` at [video/assets/audio/narration.wav](video/assets/audio/narration.wav) (`109.470 s`; total 1x composition **`110.375 s`** = `2649` exact frames @ 24 fps -> **`88.300 s`** delivered at 1.25x / 30 fps; `end_card_start = 109.750 s`, `end_card_duration = 0.625 s`; first sentence ends `7.333 s <= 10.0 s`; `"Tapi"` turn at `7.827 s <= 12.0 s`). Verified via `audio_boundaries.py` (`10/10` boundaries quiet at `-200.0 dBFS`) and recorded in [video/timing.json](video/timing.json) and [video/audio_boundaries.json](video/audio_boundaries.json).
- **Sound design (Visual v5 organic SFX):** `bgm: none` per board contract; `41` non-overlapping frame-locked organic SFX cues across `15` assets from the board Visual v5 library ([boards/budidaya-di-halaman/assets/sfx/manifest.json](../../boards/budidaya-di-halaman/assets/sfx/manifest.json), credits in [video/assets/audio/CREDITS.md](video/assets/audio/CREDITS.md)), all `>= 140 ms` clear of all 10 quiet scene boundaries and silent across the end card. Built via [video/build_sound_design.py](video/build_sound_design.py) into [video/sound_design.json](video/sound_design.json), applied and verified via `sound_design.py --apply` and `--check` (`passed`, `41` cues).
- **Preflight checks:** `storyboard_lint.py --strict` **passed** (`0` errors, `0` warnings, `status: animated`), `dom_lint.py` **passed** (`g5_fails: 0`, `readcheck_fails: 0`, `composition_sha256: 94529b0f790d8cf19c561441181cb463d6612dda267073cee1eb131b665f0bfa`), `npx hyperframes check --json` **passed** with **`0` errors, `0` warnings, `0` info** across all 6 checks (`lint`, `runtime`, `layout`, `contrast`, `craft`, `audio`).

## Verification & independent review (agent-verified under active automation)

- **Independent jury audit pass 1 (`research` subagent `d805c7eef095d3886a6fbc0d2c9a811b`):** Flagged 3 P0 blockers (`same-system` paranet omission in `s10` + unintroduced Drum 2 paranet between `s08`/`s09`, floating mid-air wooden chocks at `0.8 s` in `s01`, stale `dom-lint.json` hash verification) and 6 high-impact P1 items (left-skewed hidden-word captions & mid-clause breaks, `s09` premature lid opening during `"tutup kasa aman,"`, `2.85 s` `s10→s11` pause, Drum 2 right-edge clipping + keeper/house/basin clearances, mid-film camera variety + `s08` bite drama, and plastic `pvc-snap` on `s10` unit price).
- **Revisions & Independent re-audit pass 2 (`d805c7eef095d3886a6fbc0d2c9a811b`):** Fixed all 3 P0 blockers and all 6 P1 items (`eel-world.js`, `build_project.py`, `place_and_sync.py`, `build_sound_design.py`, `STORYBOARD.md`, `SCRIPT.md`), re-rendered `verification/proof.mp4` (`36.8 MB`, `110.375 s`, `2649` frames @ 24 fps), re-listened natively to `proof-mix.mp3`, and re-audited 24 decoded proof frames + fresh receipts. Re-audit issued **`APPROVE FOR DELIVERY RENDER`**: **18/18 judged rules pass**, **0 open P0s**, all **7 rubric dimensions 7–8/10** (`style_fidelity: 8`, `concept_wow: 8`, `motion_craft: 7`, `design_typography: 8`, `finish_texture: 8`, `sound_sync: 8`, `technical: 8`). Recorded in [video/REVIEW.md](video/REVIEW.md) (`composition_sha256: 94529b0f790d8cf19c561441181cb463d6612dda267073cee1eb131b665f0bfa`, `independent_review: subagent`, `listening: agent`).
- **Verification gate:** `episode_qa.py --stage verification --dom-lint` **passed** (`disclose: []`) — [video/verification/quality-gate-verification.json](video/verification/quality-gate-verification.json).

## Export & packaging

- **1x Delivery master:** [video/verification/master-24fps.mp4](video/verification/master-24fps.mp4) (`54 MB`, `110.375 s`, `2649` frames @ 24 fps, `--quality delivery`); verified full decode clean, `audio_boundaries.py` (`10/10` boundaries `-200.0 dBFS`), and `sound_design.py` (`41/41` cues matched, median vocal-band SNR `27.8 dB`, `0.0 s` severe masking).
- **Delivered 1.25x video:** [exports/kolam-belut-dalam-drum.mp4](exports/kolam-belut-dalam-drum.mp4) (`26,817,959` bytes / `26.82 MB`, `88.300 s` = `88300 ms`, `1080 × 1920 @ 30 fps`, pitch-kept `atempo=1.25`, two-pass `loudnorm`, `−13.99 LUFS` integrated / `−2.85 dBTP` true peak, full decode clean, SHA-256 `1ede5ca2ae9d59779b9cca3317ff763182e2c78e36d245ca4bfd31cee1d8a752`). Listened natively via `view_file` to the 1.25x audio stream (`delivery-mix-1.25x.mp3`): speech and all 41 SFX cues remain natural, crisp, and easy to follow; visually inspected decoded frames (`exports/thumbnail.png`, `delivered-s10.png`, `delivered-s11-sig.png`).
- **Delivered thumbnail & sidecar captions:** [exports/thumbnail.png](exports/thumbnail.png) (`516,654` bytes, SHA-256 `1a4e8e448b964df6824d8c1e2edc4cae1e58a8d29d11a02b49eeecf75355e123`), [exports/kolam-belut-dalam-drum.srt](exports/kolam-belut-dalam-drum.srt) (`36` cues, SHA-256 `48d811c614c6933a7ee762f622ec98c2963644653dff7f097266098ea3075edd`).
- **Export gate:** `episode_qa.py --stage export` **passed** (`disclose: []`) — [video/verification/quality-gate-export.json](video/verification/quality-gate-export.json).
- **Content package:** Shared Editorial v9 package written to [CONTENT_PACKAGE.md](CONTENT_PACKAGE.md) (`Bikin Kolam Belut di Halaman dari Drum Bekas`, shared copy/hashtags/keywords across all 3 accounts).

## External delivery (Trypost queue scheduling — completed)

- **Transport:** `api` (`trypost.py`, `Admin's Workspace` `01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37`). Duplicate check confirmed zero prior posts for this episode.
- **Receipt:** [PUBLISHING.json](PUBLISHING.json) (schema v2; export SHA-256 `1ede5ca2ae9d59779b9cca3317ff763182e2c78e36d245ca4bfd31cee1d8a752`; no credentials or upload tokens persisted).
- **Per-channel verified results (all observed `status: scheduled` via `GET /posts/{id}` in each account's configured next free queue slot; NOT live-published yet):**
  1. **Instagram `@bikindihalaman.id`** (`01a2022d-bc57-71d8-9217-6e0319cb6c03`, `instagram_reel`): post ID `01a21651-35bf-735e-b65b-ebf08d463d62`, media ID `01a21653-6357-70b4-af2a-2c2f99b81e0b`, `cover_offset_ms: 88050` (`88300 − 250`), status **`scheduled`**, scheduled at **`2026-11-27 04:30:00` UTC** (`2026-11-27T11:30:00+07:00`, `Asia/Jakarta`).
  2. **YouTube `@bikindihalaman_id`** (`01a202dc-0e4a-72ae-bec8-589ab7f90045`, `youtube_short`): post ID `01a21655-b1e3-73fe-a319-48620f784eb0`, media ID `01a21655-dc62-733e-9f03-9d7a0535902d`, `meta.title: "Bikin Kolam Belut di Halaman dari Drum Bekas"`, status **`scheduled`**, scheduled at **`2026-11-27 08:30:00` UTC** (`2026-11-27T15:30:00+07:00`, `Asia/Jakarta`).
  3. **Facebook `Bangun Di Halaman`** (`01a2036c-5179-70c6-b908-25118446326d`, `facebook_reel`): post ID `01a21655-e4e6-711a-9fe4-bdd675d29714`, media ID `01a21656-08fa-7378-90c9-632df0b8da1a`, status **`scheduled`**, scheduled at **`2026-11-27 10:30:00` UTC** (`2026-11-27T17:30:00+07:00`, `Asia/Jakarta`).
- **Preview lifecycle:** No preview server was started during this run.

## Current state

- `stage: publishing`
- `status: complete` (requested delivery: `queue`, all 3 inherited accounts verified `scheduled` in configured queue slots; posts are scheduled, not yet live-published)
- **User acceptance (`final_delivery_approval: user`, 2026-11-25):** User explicitly approved the delivered video, content package, and 3 scheduled Trypost queue slots (*"approve dan buatkan pr"*).
- `next_action: upload exports/thumbnail.png manually in YouTube Studio and Meta Business Suite / Facebook before or after publication (Instagram cover_offset_ms=88050 is already set), and run a performance review snapshot after the queued posts publish`
