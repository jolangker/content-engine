# Bikin Kandang Bebek Petelur Sistem Kering di Halaman

## Brief

- **Slug:** `kandang-bebek-petelur-kering`
- **Topic selection:** `topic_selection: user`. On 2026-11-24, after reviewing a 10-topic *Ternak Bebek* shortlist for `budidaya-di-halaman`, the user replied `"setuju"` accepting recommended candidate #1: building a backyard dry-litter (*sistem kering*) laying-duck coop from a bare yard corner through splash drainage, shade/ventilation, dry rice-husk litter, weather/runoff control, floor-level nesting, feed-spill control, and night predator protection to a stable coop and first weekly egg harvest.
- **Board:** `budidaya-di-halaman`, revision 9 (`editorial v9 / visual v4`, status `approved`). Inherit [direction](../../boards/budidaya-di-halaman/DIRECTION.md), [editorial framework v9](../../boards/budidaya-di-halaman/EDITORIAL.md), [visual specification v4](../../boards/budidaya-di-halaman/frame.md), and [production contract](CONTRACT.json).
- **Contract snapshot:** [CONTRACT.json](CONTRACT.json) copied verbatim from `boards/budidaya-di-halaman/CONTRACT.json` (`editorial v9 / visual v4`, SHA-256 `e7513a8dd9983e098c80bff61d1f7c59fb9b38be1535e8b2cf141322b5e1da55`), validated via `episode_qa.py --contract` (16 effective judged rules, 0 overrides).
- **Overlap check:** Inspected `TRACKER.json` and `productions/`. All 8 existing `budidaya-di-halaman` episodes cover fish, crustaceans, aquaponics, BSF maggots, or container crops (`akuaponik-lele-dan-kangkung`, `jejak-kotoran-kolam-nila`, `maggot-jalan-ke-wadah`, `pot-sumbu-selada`, `aquaponik-pasang-surut`, `kentang-dalam-pot`, `kolam-lobster-air-tawar`, `kolam-lele-di-halaman`). None covers ducks or backyard dry-litter poultry housing.
- **Audience & POV:** Indonesian-speaking general viewers curious about small-yard cultivation, addressed in casual Indonesian as `"kamu"` (the sole builder/keeper of one backyard corner throughout the film). Frame as a practical household-scale dry-litter coop without profit or income guarantees.
- **Format & duration target (inherited from board):** Vertical 9:16 (`1080 × 1920`) flat 2D illustrated cutaway in one consistent yard corner, authored at **90–112.5 s at 1x** and delivered at **1.25x** speed (`72–90 s` delivered, pitch kept), closing with an exact-match thumbnail end card (`0.625 s` 1x / `0.5 s` delivered).
- **Audio plan (inherited from board):**
  - Narration: `use` — board default ElevenLabs **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh`, `eleven_v4`) from [AUDIO.json](../../boards/budidaya-di-halaman/AUDIO.json).
  - BGM: `none` for the entire episode.
  - SFX: `use` — restrained, scene-linked construction, water splash/drain, husk rustle, rain, egg-placement, and latch cues subordinate to narration.
- **Word budget note:** `episode_qa.py --budget 255 --voice 5g0yKK2JwTRka0IG61Hh` reported no local cached narration audio for `5g0yKK2JwTRka0IG61Hh` in this clone. Plan initially at `2.4–2.6 words/s` (~235–265 spoken words for 90–112.5 s 1x, matching prior board episodes) and re-budget after the first narration take.
- **Execution & review policy:**
  - `execution_policy: human_review`
  - `endpoint: content_package`
  - `delivery: package` (local verified MP4 export, thumbnail PNG, SRT captions, and shared `CONTENT_PACKAGE.md`; no external upload or publishing authorized)
  - Retained human checkpoints: hook selection (current), script review, visual storyboard review, and final preview.

## Publishing targets

Inherited from `boards/budidaya-di-halaman/ACCOUNTS.json` for shared package destination planning and closing-signature handle (`@bikindihalaman.id` from the first listed account); no remote calls or publishing authorized:

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

## Candidate comparison (discovery summary)

Evaluated 10 distinct backyard duck-keeping builds for `budidaya-di-halaman` (dry-litter laying coop, slatted-floor meat-duck deck, DOD brooder box, semi-intensive mini-wading trough coop, DIY duck-egg incubator, integrated duck-over-fish *longyam*, wheeled *duck tractor*, narrow-alley colony bays with piped cup drinkers, paired *Azolla* + duck feed-saving setup, and quiet residential Muscovy/*entok* pen). No board performance analysis (`insights/*/ANALYSIS.md`) exists yet. Candidate #1 (dry-litter laying-duck coop) was recommended and accepted by the user because it directly overturns the most common backyard objection (*"bebek pasti becek dan bau"*), introduces a completely fresh poultry-house silhouette with 100% observable 2D cutaway causality across 7 rounds, and varies the income scene from fish weighing to counting clean egg trays.

## Researched story chain

Grounded in [SOURCES.md](SOURCES.md) (claims C1–C9). Exact ordering of the opening round adapts to the user's selected hook; all 7 problem–improvement rounds stay compact (~6–10 s / 15–25 words each at 1x) with varied, smooth Indonesian round transitions (`"Tapi"` reserved for the opening hook turn per Editorial v9):

1. **Premature first system (`00:00–00:11`, Hook):** On a bare yard corner (~2 × 2 m), erect a basic fence, set down drinking water, and release ~12 ready-to-lay local ducks (*bebek petelur / bayah* ~5 months, density ~3 ducks/m², C1) with no roof, drainage, dry litter, nests, or predator skirt. The first visible problem hits immediately.
2. **Round — Splash & mud (`C2`):** Ducks dabble and splash open water into muddy puddles, yet still need water deep enough (≥8 cm) to dip bills and nostrils for eye/nostril hygiene. *Fix & test:* Set a covered deep drinker with head cutouts atop a slatted platform over a dug gravel soak drain (*alas bilah + parit kerikil*) — ducks dunk heads cleanly while the main floor stays dry.
3. **Round — Midday heat stress (`C3`):** Ducks lack sweat glands and pant with open bills under hot sun. *Fix & test:* Add a slanted shade roof with upper cross-ventilation gaps — shade drops heat and ducks settle calmly.
4. **Round — Damp droppings & ammonia odor (`C4`):** Bare soil traps wet droppings, causing sharp ammonia odor and footpad irritation. *Fix & test:* Spread dry rice husks (*sekam padi kering*), scooping wet clumps and turning/topping up dry husks — floor stays dry and odor fades.
5. **Round — Wind-driven rain & yard runoff (`C5`):** Heavy side rain blows in and yard runoff seeps into the dry husks. *Fix & test:* Add roof eaves, a roll-down side tarp curtain (*tirai samping*), and an outer perimeter drain trench (*parit keliling*) — rainwater diverts outside while interior husks stay dry.
6. **Round — Scattered, soiled/cracked morning eggs (`C6`):** Ducks lay in the early morning (~03:00–08:00) on the open floor where eggs get trampled and dirty. *Fix & test:* Place floor-level wooden nest boxes (~30 × 30 cm, ~1 per 4–5 ducks, bedded with dry straw, no elevated perches) along the quiet back corner — morning eggs stay clean and intact.
7. **Round — Spilled feed & flies (`C7`):** Shallow open feed scatters into damp edges, wasting feed and drawing flies. *Fix & test:* Fit a deep lipped feed trough (*palung pakan berbibir*) set slightly apart from the water drain (still close enough to wash feed down) with measured portions — spills drop and flies clear.
8. **Round — Night predators & night panic (`C8`):** Rats and stray cats probe the lower bamboo gaps at night, raiding feed and startling ducks. *Fix & test:* Anchor a fine wire mesh skirt along the lower perimeter, latch the gate, and hang a soft dim warm night bulb — predators stay out and the flock rests calmly.
9. **Stable system check (`01:14–01:22`):** In one wide view during rain and morning feeding, water drains through the gravel slot, roof/curtain/trench keep rain out, husks stay dry, wire mesh holds, and clean eggs sit in the floor nest boxes.
10. **Monetization — First weekly egg harvest (`01:22–01:35`, `C9`):** Beside the finished coop, pack **60 clean fresh duck eggs (2 trays of 30)** gathered across one steady week (~8–9 eggs/day from 12 ducks at ~65–70% HDP). Hanging price tag drops on its nail: `60 butir × Rp3.500` → yellow chip `≈ Rp210.000` → note `estimasi harga pasar / Sep 2026` (Dindagkop UKM Demak, 5 traditional markets, Sep 2026). Spoken numbers rounded; no profit or payback claim.
11. **Closing wide view & end card (`01:35–01:46`):** Wide pull-out of the complete dry-litter duck coop and two egg trays. Congratulation naming the built coop + next-build question holding yellow `#FFD44D` on consecutive **`bikin di halaman`** with subtle `@bikindihalaman.id` fade-in, hard cutting to the `0.625 s` 1x (`0.5 s` delivered) exact-match thumbnail end card.

## Hook options (v1 — awaiting human selection)

All three options strictly follow Editorial v9's four-slot pattern (`Kalo kamu {aksi pertama}, {konjungsi temporal} kamu {aksi kedua}, kamu sudah punya {sistem}. Tapi {masalah}.`), avoid repeating the previous episode's (`kolam-lele-di-halaman`) first verb (`tancap`) and connector (`lalu`), keep Sentence 1 within `10.0 s` and `"Tapi"` within `12.0 s`, and stay within [SOURCES.md](SOURCES.md). *(No board performance analysis exists yet to weigh past hook mechanisms.)*

### Option 1 (Recommended) — Splash-to-mud surprise (water behavior failure)
- **Mechanism:** Immediate physical mess reversal — taps straight into viewers' top fear about backyard ducks (*becek dan bau*) and reveals that ordinary drinking water, not a swimming pond, triggers the mud problem. *(Board performance analysis: none yet.)*
- **First verb / connector:** `pasang` / `terus`
- **Spoken line (27 words; Sentence 1 = 20 words ≈ 7.7–8.3 s ≤ 10.0 s; `"Tapi"` at word 21 ≈ 8.1–8.7 s ≤ 12.0 s):**
  > “Kalo kamu pasang pagar bambu di halaman, terus kamu taruh ember air dan lepas bebek, kamu sudah punya kandang bebek. Tapi sorenya tanahnya langsung jadi lumpur bau.”
- **Frame 0 & `<1.0 s` motion:** Bare warm-clay yard corner beside the house with bundled bamboo slats ready; at `0.25 s` hands set up the low bamboo fence frame, drop an open water bucket, and release laying ducks, then an afternoon sky shift shows splashes turning the bare earth around the bucket into dark smelling mud.
- **On-screen line:** 46 px DM Sans ExtraBold progressive captions (max 2 lines): `Kalo kamu pasang pagar bambu di halaman,` / `terus kamu taruh ember air dan lepas bebek,` / `kamu sudah punya kandang bebek.` / `Tapi sorenya tanahnya langsung jadi lumpur bau.`
- **Promise:** Shows how to keep ducks clean and dry without taking away their head-dipping water, building through 7 physical upgrades to a dry backyard coop and two trays of clean eggs.

### Option 2 — Morning egg-loss frustration (output-first setback)
- **Mechanism:** Output-first pain point — hooks viewers who care about harvesting clean eggs by showing their very first morning eggs scattered, muddy, and cracked on the bare ground. *(Board performance analysis: none yet.)*
- **First verb / connector:** `susun` / `habis itu`
- **Spoken line (26 words; Sentence 1 = 19 words ≈ 7.3–7.9 s ≤ 10.0 s; `"Tapi"` at word 20 ≈ 7.7–8.3 s ≤ 12.0 s):**
  > “Kalo kamu susun pagar kayu di samping rumah, habis itu kamu lepas bebek petelur, kamu sudah punya kandang bebek. Tapi paginya telurnya berserakan kotor dan retak.”
- **Frame 0 & `<1.0 s` motion:** Bare side-yard strip with wooden fence panels ready; at `0.25 s` hands align the wooden fence enclosure and release ready-to-lay ducks, then a dusk-to-dawn sky shift reveals blue-green eggs scattered in dirt with one cracked shell.
- **On-screen line:** Progressive captions: `Kalo kamu susun pagar kayu di samping rumah,` / `habis itu kamu lepas bebek petelur,` / `kamu sudah punya kandang bebek.` / `Tapi paginya telurnya berserakan kotor dan retak.`
- **Promise:** Explains early-morning floor laying and builds through floor-level nest boxes, splash drainage, shade roof, dry rice husks, rain barrier, feed trough, and predator mesh to a clean weekly egg harvest.

### Option 3 — Midday thermal stress (biological/welfare surprise)
- **Mechanism:** Observable animal-behavior mystery — showing ducks panting with open bills under midday sun raises curiosity about how waterfowl stay cool and healthy in a dry yard coop without a pond. *(Board performance analysis: none yet.)*
- **First verb / connector:** `bentang` / `setelah itu`
- **Spoken line (26 words; Sentence 1 = 19 words ≈ 7.3–7.9 s ≤ 10.0 s; `"Tapi"` at word 20 ≈ 7.7–8.3 s ≤ 12.0 s):**
  > “Kalo kamu bentang jaring kawat di pojok halaman, setelah itu kamu masukkan bebek petelur, kamu sudah punya kandang bebek. Tapi pas siang bebeknya ngos-ngosan buka paruh.”
- **Frame 0 & `<1.0 s` motion:** Bare sunny backyard corner with rolled wire mesh; at `0.25 s` hands unroll and fasten the wire enclosure and let ducks walk in, then harsh overhead midday sun waves hit the pen and the ducks open their bills panting.
- **On-screen line:** Progressive captions: `Kalo kamu bentang jaring kawat di pojok halaman,` / `setelah itu kamu masukkan bebek petelur,` / `kamu sudah punya kandang bebek.` / `Tapi pas siang bebeknya ngos-ngosan buka paruh.`
- **Promise:** Explains why ducks overheat easily without sweat glands and develops an unshaded wire pen through roof/ventilation, head-dipping splash drain, dry husks, rain curtain, floor nests, feeder, and night security to a steady egg harvest.

**Recommendation:** **Option 1.** Mud and odor from splashed water is the single biggest objection Indonesian backyard viewers hold against raising ducks at home, reads unmistakably on mute in a flat 2D cutaway, and launches the most natural chronological build sequence (drain splash → shade roof → dry husks → rain curtain → floor nests → lipped feeder → predator wire skirt).

- **Hook selection:** `hook_selection: user`. On 2026-11-24 the user replied `"setuju"` accepting recommended **Option 1**. Its opening lines are preserved verbatim in [SCRIPT.md](SCRIPT.md) v1.

## Script review

[SCRIPT.md](SCRIPT.md) v1 is built around Hook Option 1 with 11 scenes (18 meaningful events: premature build hook, 7 distinct single-cause/single-fix problem–improvement rounds, stable check, weekly egg-harvest count with hanging price tag, and closing wide shot + 0.5 s delivered thumbnail end card). Note on Round 4 and Round 7 refinement during drafting: per Editorial v9's `"One cause per round"` rule, each round was tightened to a single visible cause and single physical fix (Round 4 focuses strictly on windblown side rain → roll-down side tarp curtain; Round 7 focuses strictly on rats slipping under bamboo gaps → fine lower wire mesh skirt).

### Script check (v1)

- **Spoken word count & budget output:** **251 spoken words** (`27 + 25 + 21 + 21 + 21 + 21 + 22 + 22 + 20 + 27 + 24`). `episode_qa.py --budget 255 --voice 5g0yKK2JwTRka0IG61Hh` reported no local cached narration audio for `5g0yKK2JwTRka0IG61Hh` in this clone (`budget again after its first take`). Evaluated at both the fallback pace (`2.40 wps`) and Pribs's recorded pace (`2.61 wps`): predicted narration is `96.2–104.6 s`, predicted 1x film duration (including `~3.8 s` boundary pauses/tag hold + `0.625 s` end card) is **`100.6–109.0 s`** (`~80.5–87.2 s` delivered at 1.25x), fitting comfortably inside the contract's `90.0–112.5 s` 1x window. Re-budget after the first narration take.
- **First sentence & `"Tapi"` turn:** Sentence 1 is **20 words** (`"Kalo kamu pasang pagar bambu di halaman, terus kamu taruh ember air dan lepas bebek, kamu sudah punya kandang bebek."`), predicted **`7.7–8.3 s`** (`<= 10.0 s`). `"Tapi"` arrives at word 21, predicted **`8.1–8.7 s`** (`<= 12.0 s`). Total `"tapi"` occurrences across the full script: **1** (hook only).
- **Selected hook three parts (Option 1):**
  - *Spoken line:* “Kalo kamu pasang pagar bambu di halaman, terus kamu taruh ember air dan lepas bebek, kamu sudah punya kandang bebek. Tapi sorenya tanahnya langsung jadi lumpur bau.”
  - *Frame 0 & `<1.0 s` motion:* Bare warm-clay yard corner with bundled bamboo slats ready; at `0.25 s` hands erect the low bamboo fence, set an open water bucket, and release laying ducks, followed by an afternoon sky shift revealing dark mud and odor lines around the bucket.
  - *On-screen line:* 46 px DM Sans ExtraBold max-2-line progressive captions matching the opening line.
- **Cold-read & POV continuity result:** Read all 251 spoken words sequentially without headings or visual cues. `"kamu"` resolves unambiguously to the single backyard builder/keeper throughout; every animal behavior, cause, upgrade, and visible result makes standalone sense without pictures. Three ear-clarity repairs were applied before finalizing v1: (1) Round 1 clarified `"ember bertutup dengan lubang paruh"` so listeners do not mistake it for a leaking bucket; (2) Round 5 used `"kotak sarang di lantai beralas jerami"` for natural Indonesian syntax; (3) Scene 10 opened with `"Seminggu berjalan, terkumpul kira-kira enam puluh butir dari dua belas bebek"` to ground flock scale naturally for the ear.
- **Contract judged rules (script scope):**
  - `[pass]` `hook-frame`: Frame 0 opens on the bare yard corner and bamboo slats (`0.25 s` first motion) with 46 px phone-readable progressive captions.
  - `[pass]` `pictures-alone`: All 11 scenes specify ordered visual sub-beats depicting cause, added physical upgrade, and on-screen retest without needing text.
  - `[pass]` `event-density`: Every scene introduces a distinct construction action, state change, or harvest check beyond captions (18 total events).
  - `[pass]` `motion-variety`: Shot plan alternates `wide` → `close` → `medium` → `close` → `medium-wide` → `close` → `medium` → `medium-close` → `wide` → `medium` → `wide` (max consecutive identical shot = `1 <= 2`).
  - `[pass]` `subject-scale` & `vessel-scale`: Coop cutaways, fittings, and two egg trays are planned at ≥40% frame width with persistent yard landmarks.
  - `[pass]` `ear-test`: Cold read passed after the three ear-clarity repairs above; single `"kamu"` POV throughout.
  - `[pass]` `build-first`: Hook Option 1 fills all four Editorial v9 slots verbatim with ordinary punctuation, starts on a bare corner, puts the coop in use, and ends on visible afternoon mud within time ceilings.
  - `[pass]` `shortfall-before-fix`: 7 problem–improvement rounds after the hook (21–25 words / `~8.0–10.0 s` each at 1x), one cause and one on-screen tested fix per round, across 7 distinct triggers (water splash, midday heat, wet droppings/ammonia, windblown side rain, morning scattered eggs, spilled feed/flies, night rats), with varied natural transitions (`Pas tengah hari`, `Beberapa hari jalan`, `Begitu hujan angin turun`, `Suatu pagi`, `Masalahnya`, `Malam harinya`) and `"Tapi"` only in the hook.
  - `[pass]` `same-system`: Every installed upgrade (gravel/slatted drain + covered head-hole bucket, slanted vented roof, dry rice-husk litter, roll-down side tarp curtain, floor-level straw nest boxes, lipped feed trough, lower fine wire mesh skirt) remains visible on the same coop through Scene 11.
  - `[pass]` `final-job`: Scene 9 shows the finished coop coping with sun/rain and feeding before calling it `"stabil"` (`"stabil"` never appears earlier).
  - `[pass]` `income-scene`: Scene 10 counts 60 eggs (2 trays) beside the finished coop with hanging price tag `60 butir × Rp3.500 ≈ Rp210.000` (`estimasi harga pasar / Sep 2026`, sourced from Dindagkop UKM Demak S12), rounded spoken numbers, ≥3 s 1x hold, no profit/payback/monthly claim.
  - `[pass]` `event-map`: 18 meaningful events (within 15–19); every component visibly enters the build via `"kamu"`.
  - `[pass]` `closing-lines`: Ends with congratulation naming the built dry-litter duck coop + next-build question containing consecutive `"bikin di halaman"`; no opening intro or follow prompt.
  - `[pass]` `closing-signature`: Holds yellow `#FFD44D` on `"bikin di halaman"`, fades in `@bikindihalaman.id`, hard cuts to `0.625 s` 1x (`0.5 s` delivered) exact-match thumbnail end card.
  - `[pass]` `reframing`: Uses close cutaways for splash drain, husk litter, and floor nests; medium-wide for side rain curtain; and wide pull-out for stable check and closing.

- **Script approval:** `script_approval: user`. On 2026-11-24 the user replied `"approve"` accepting [SCRIPT.md](SCRIPT.md) v1 (251 spoken words, 11 scenes, 18 events).

## Visual storyboard

Complete visual storyboard built from [approved SCRIPT.md v1](SCRIPT.md) and `boards/budidaya-di-halaman` (`Editorial v9 / Visual v4`) inside [video/](video/):

- **Artifacts:**
  - Scene plan: [video/STORYBOARD.md](video/STORYBOARD.md) (`11` frames, `105.625 s` planned at 1x = `84.5 s` delivered at 1.25x, max identical shot run = `1`, max push streak = `2`).
  - Stills (`11`): [video/boards/stills/](video/boards/stills/) (`frame-00-at-9.2s.png` through `frame-10-at-104.7s.png`).
  - Motion poses (`25`): [video/boards/poses/](video/boards/poses/) (`hook-0.0s.png`, `hook-0.8s.png`, `hook-3.0s.png`, plus `01-a-start.png`..`11-b-end.png` covering all 11 frames > 5.0 s).
  - Review board HTML: [video/boards/storyboard.html](video/boards/storyboard.html) (HyperFrames `.act`, `.frame`, `.title`, `.time`, `.words`, `.poses` classes, DM Sans on warm `#F6F1DD` paper).
  - Combined board PNG: [video/boards/storyboard.png](video/boards/storyboard.png) (`1600 × 7226` px, `1,437,897` bytes).
- **Visual inspection & craft repairs before lock:**
  1. Lowered front bamboo cutaway rail (`h = 14`, corner & bay pegs only) and refined lower wire-mesh skirt (`meshTop = floorBot - 22`, `9 px` grid, soft radial night glow) in [duck-world.js](video/assets/duck-world.js) so ducks, shallow/deep feeders, floor eggs, husks, and nest boxes read unobstructed across all 11 scenes.
  2. Repositioned `headDip` neck/bill angle and drinking ducks (`x = 176, y = 424`) across `s01`, `s02`, `s03`, `s10`, and `drawCompletedYard` so bills dip directly into the covered bucket's right head-access cutout above the slatted bamboo drain.
  3. Re-composed [s10.html](video/compositions/s10.html) with zero overlap among the 400 px hanging price tag (`600, 594` px nail), wooden bench & two 30-egg trays on the left, keeper & house on the right, and completed 7-upgrade dry-litter coop landmark cleanly below the tag and above captions.
  4. Tuned nighttime rat coordinates in [s08.html](video/compositions/s08.html) (`x = 106..212`) so both the initial fence breach and post-mesh blocked retreat remain unmistakably inside the zoomed frame.
  5. Updated Frame 11 poster to `104.7 s` (`frame-10-at-104.7s.png`) so the full yellow `#FFD44D` closing signature (`bikin di halaman?`) and `@bikindihalaman.id` appear cleanly on the storyboard card, while `11-b-end.png` shows the dusk-slate `Bikin kandang bebek kering` thumbnail end card.
- **Verification & quality gate:**
  - `npx hyperframes check --json`: **PASSED** (`0` errors, `18/18` contrast passed; only expected storyboard-stage warnings `film_silent` and `line_unread` on the `0.625 s` end card).
  - Browser verification ([video/verification/storyboard-browser.json](video/verification/storyboard-browser.json)): `36/36` images loaded with nonzero size (`0` broken), `DM Sans` loaded, `11/11` frames and `4` acts in exact order, `0` page errors, `0` failed requests, `0` horizontal overflow at `1600 px` desktop and `390 px` mobile; full `storyboard.png` visually inspected and confirmed crisp and readable.
  - `storyboard_lint.py --strict`: **PASSED** (`0` errors, `0` warnings).
  - `episode_qa.py --production productions/kandang-bebek-petelur-kering --stage storyboard`: **PASSED** (`disclose: []`; saved to [video/verification/quality-gate-storyboard.json](video/verification/quality-gate-storyboard.json)).

- **Storyboard approval:** `storyboard_approval: user`. On 2026-11-24 the user replied `"approve"` accepting the verified visual storyboard ([STORYBOARD.md](video/STORYBOARD.md), [storyboard.html](video/boards/storyboard.html), [storyboard.png](video/boards/storyboard.png)).

## Audio stage (resolved & verified)

- **Transport & voice resolution (2026-11-24):**
  - `elevenlabs_api`: `narration.py --check-api` OK (`tier: free`, `6,964` chars remaining before take). `elevenlabs_cli` not logged in; ElevenLabs MCP not connected.
  - Board default voice **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh`) returned HTTP 400 (`voice_not_found`) on the free-tier API key. On 2026-11-24 the user explicitly authorized ElevenLabs **Roger** (`CwhRBWXzGAHq8TQ4Fs17`) as an `episode_override` (`"Pakai override Roger (CwhRBWXzGAHq8TQ4Fs17)"`).
- **Narration synthesis (1 take, `elevenlabs_api`, `eleven_v4`):** [video/.media/audio/voice/narration-6aa40547f2ac90b3356c.mp3](video/.media/audio/voice/narration-6aa40547f2ac90b3356c.mp3) (`104.751 s`, exact `251` spoken words, `request_sha256: 6aa40547f2ac90b3356c9c5413b93424eae9d628db503b647f97687299284061`; recorded in [video/audio_request.json](video/audio_request.json) and [video/audio_meta.json](video/audio_meta.json)).
  - **Native listening (take 1, `listening: agent`):** Listened directly to the raw MP3 via `view_file`. Zero delivery tags read aloud, clean natural Indonesian pronunciation across all 251 words and numbers (`60 butir`, `12 bebek`, `3.500`, `210.000`), zero clipped syllables, well-paced curious-to-warm delivery.
- **Acoustic boundary placement & normalization:** Placed via `audio_boundaries.place()` (`0.16 s` editorial pauses after S01–S09, `3.60 s` after S10 yielding **`3.427 s >= 3.0 s`** 1x price-tag hold) and normalized once to `-14.0 LUFS / -1.5 dBTP` at [video/assets/audio/narration.wav](video/assets/audio/narration.wav) (`109.760 s`). Total 1x composition is **`111.000 s`** (`2664` frames @ 24 fps, `3330` frames @ 30 fps → **`88.800 s`** delivered at 1.25x, `end_card_start = 110.375 s`, `end_card_duration = 0.625 s`). Placed hook timings: Sentence 1 ends **`6.849 s <= 10.0 s`**, `"Tapi"` starts **`7.150 s <= 12.0 s`**. Receipt: [video/audio_boundaries.json](video/audio_boundaries.json); `audio_boundaries.py` preflight **passed** (`10/10` quiet boundaries).
- **Sound design (`bgm: none`, `sfx: use`):** Upgraded during revision pass 2 to **13 restrained cues across 6 unique non-duplicate bundled `media-use` assets** (`impact-bass-1.mp3`, `key-press.mp3`, `click.mp3`, `whoosh-short.mp3`, `pop.mp3`, `chime.mp3`; credits in [video/assets/audio/CREDITS.md](video/assets/audio/CREDITS.md)) planned in [video/sound_design.json](video/sound_design.json) and synced onto measured cues in [video/index.html](video/index.html) and [video/STORYBOARD.md](video/STORYBOARD.md).

## Verification & final preview

Draft 1x 24 fps proof film rendered at [video/verification/proof.mp4](video/verification/proof.mp4) (`1080 × 1920`, `24.0 fps`, `111.000 s` at 1x = `88.800 s` delivered at 1.25x, SHA-256 `8ea41cdc9ac4a21d1313617bc3df06b906a52e9945cd177432a3bb2c5a39fa53`) for composition SHA-256 `0b4e1ac1f24e5758d0c7d2218a1d2d495002a81d4d28a6909bfc59fe3973a78e`:

- **Automated technical & audio receipts (all passing):**
  - **Verification quality gate:** [video/verification/quality-gate-verification.json](video/verification/quality-gate-verification.json) — **`passed`** (21/21 checks, `disclose: []`, `hook-motion: 0.2 s <= 1.0 s`, `hook-first-sentence: 6.85 s <= 10.0 s`, `hook-turn: 7.15 s <= 12.0 s`, `empty-frames: 0`, `end-hold: 0.4 s`, all 11 scenes passing `motion-floor`).
  - **DOM anti-slop & read-time lint:** [video/verification/dom-lint.json](video/verification/dom-lint.json) — **`passed`** (`g5_fails: 0`, `readcheck_fails: 0`).
  - **HyperFrames check:** [video/verification/hyperframes-check.json](video/verification/hyperframes-check.json) — **`passed`** (`ok: true`, `0` errors, `0` layout/contrast/audio warnings, `19/19` contrast passed; only the expected contract-mandated `line_unread` notice on the `0.625 s` 1x / `0.500 s` delivered thumbnail end card).
  - **Storyboard lint (`--strict`):** **`passed`** (`0` errors, `0` warnings).
  - **Acoustic boundaries (`proof.mp4`):** [video/verification/audio-boundaries-export-v2.json](video/verification/audio-boundaries-export-v2.json) — **`passed`** (`10/10` quiet scene seams `-160.7` to `-200.0 dBFS`, `195–258 ms` quiet buffers).
  - **Sound design (`proof.mp4`):** [video/verification/sound-design-export-v2.json](video/verification/sound-design-export-v2.json) — **`passed`** (`13/13` cues at `0.000 s` offset, `6` unique asset hashes, `28.54 dB` median vocal-band SNR, `0.025 s` max masking).
  - **Native listening (`listening: agent`):** Heard both the raw ElevenLabs take (`narration-6aa40547f2ac90b3356c.mp3`, user-authorized Roger `episode_override`) and the revised 13-cue mix ([video/verification/proof-mix.mp3](video/verification/proof-mix.mp3)) natively via `view_file`.
- **Independent 7-dimension jury review ([video/REVIEW.md](video/REVIEW.md), subagent `48e3391d6fe6dd63bbba9c101118807a`):**
  - **Pass 1:** Returned `REVISE BEFORE RENDER` with 4 P0s (`s10` buried coop + narrow bench + keeper/tag collision, `s05`/`s09` underground rain streaks, `s07` occluded drinking duck + tiny feed crumbs/flies, `s04` floating unheld scoop) and 7 P1s (cross-period caption breaks, static `0.25 s` hook, egg-tray rim z-order, rigid `s01` mud trapezoid, `s11` keeper arm clip, duplicate SFX asset, stale receipts).
  - **Pass 2 (after fixing all 4 P0s & 7 P1s):** Returned **`APPROVE FOR DELIVERY RENDER (SHIP)`** — **16/16 judged rules passing**, **0 open P0s**, mean rubric **7.86/10**:
    - `style_fidelity: 8.2/10`, `concept_wow: 7.6/10`, `motion_craft: 7.7/10`, `design_typography: 8.0/10`, `finish_texture: 7.8/10`, `sound_sync: 7.5/10`, `technical: 8.2/10`.
  - **`weakest_shot`:** `s01` (`t=0.00–0.35 s`, `01-s01-start-0.25s.png`) — tied bamboo bundle and rising stakes satisfy `hook-frame`, but the initial `"Kalo"` sits over ~50% empty subterranean clay before ducks/water arrive (minor secondary note: far-left coop eave in `18-s10-tag-97.20s.png` touches `x=0`).
  - **Review contact sheets:** [review-sheet-1.jpg](video/verification/review-sheet-1.jpg), [review-sheet-2.jpg](video/verification/review-sheet-2.jpg), [review-sheet-3.jpg](video/verification/review-sheet-3.jpg).
- **Disclosure summary:** `disclose: []` in [quality-gate-verification.json](video/verification/quality-gate-verification.json). Transparent production note: narration uses the user-authorized `episode_override` voice **Roger** (`CwhRBWXzGAHq8TQ4Fs17`, approved 2026-11-24 because board default `Pribs` returned `voice_not_found` on the configured free-tier ElevenLabs API key).
- **Final preview approval:** `final_preview_approval: user`. On 2026-11-24, after reviewing `final_preview_review.md` and watching the playable proof video in chat, the user replied `"approve"` authorizing the final delivery render and local content package.

## Export & content package

- **1x 24 fps delivery master:** [video/out/master-24fps.mp4](video/out/master-24fps.mp4) (`1080 × 1920`, `24.0 fps`, `111.000 s`, `2664` frames, `35,128,554` bytes, SHA-256 `b2b861f880a663d119ef34531b06a07890a039ab145926643bdd35aa58ff2923`).
  - `audio_boundaries.py` on master: **`passed`** (`10/10` quiet seams; [audio-boundaries-master.json](video/verification/audio-boundaries-master.json)).
  - `sound_design.py` on master: **`passed`** (`13/13` cues at `0.000 s` / `-0.00002 s` offset, `6` unique asset hashes, `28.54 dB` median vocal-band SNR, `0.025 s` max masking; [sound-design-master.json](video/verification/sound-design-master.json)).
- **1.25x / 30 fps delivered export:** [exports/kandang-bebek-petelur-kering.mp4](exports/kandang-bebek-petelur-kering.mp4) (`1080 × 1920`, `30.0 fps`, `88.800 s`, `2664` frames kept verbatim via `setpts=0.8*PTS`, H.264 High `yuv420p` + AAC 48 kHz stereo `192 kbps`, `atempo=1.25` pitch-preserved + two-pass linear `loudnorm`, `22,346,228` bytes / `22.35 MB`, SHA-256 `5b77b7c5a6baac0b9ee30d32fb88a0eb0239c3398226220fc6736da8bc54222c`).
  - **Native listening (1.25x delivered audio, `listening: agent`):** Listened natively via `view_file` to [video/verification/export-1.25x-audio.mp3](video/verification/export-1.25x-audio.mp3) (`88.8 s`) — crisp, natural pitch-preserved Indonesian delivery at 1.25x, balanced non-masking SFX, clean price-tag hold and ending silence.
  - **Export quality gate:** [video/verification/quality-gate-export.json](video/verification/quality-gate-export.json) — **`passed`** (`22/22` checks, `disclose: []`, `integrated_lufs: -14.06 LUFS`, `true_peak_dbtp: -2.62 dBTP`, `hook-motion: 0.2 s`, `empty-frames: 0`, `end-hold: 0.2 s`, all 11 scenes passing `motion-floor`).
- **Companion delivery files:**
  - **Thumbnail PNG:** [exports/thumbnail.png](exports/thumbnail.png) (`1080 × 1920`, `444,331` bytes, SHA-256 `21e8dc0f838e92f34039021240ebbb72da81d95e061c5b45074a8a605458211e`), visually inspected via `view_file` — exact match to the final `0.500 s` end card (`Bikin kandang` / `bebek kering`).
  - **Sidecar SRT captions (1.25x):** [exports/kandang-bebek-petelur-kering.srt](exports/kandang-bebek-petelur-kering.srt) (`51` cues, `3,414` bytes, SHA-256 `4d2edf3ac5b37c9960ae7e7b2cd3c63c9332c25fa6ec017c267c1455c95347c6`).
  - **Shared content package:** [CONTENT_PACKAGE.md](CONTENT_PACKAGE.md) (shared copy for Instagram `@bikindihalaman.id`, YouTube `@bikindihalaman_id`, and Facebook `Bangun Di Halaman`).

## External delivery (Trypost drafts — completed)

- **User authorization (`draft` delivery, 2026-11-24):** User explicitly approved the final 1.25x export & content package and authorized draft upload (*"approve dan upload draft"*).
- **Transport:** `api` (`trypost.py`, `Admin's Workspace` `01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37`).
- **Receipt:** [PUBLISHING.json](PUBLISHING.json) (schema v2; export SHA-256 `5b77b7c5a6baac0b9ee30d32fb88a0eb0239c3398226220fc6736da8bc54222c`; no credentials or upload tokens persisted).
- **Per-channel verified results (all observed `status: draft` via `GET /posts/{id}`, exact caption match, `22,346,228` bytes, `88.8 s`):**
  1. **Instagram `@bikindihalaman.id`** (`01a2022d-bc57-71d8-9217-6e0319cb6c03`, `instagram_reel`): post ID `01a211a9-3f0a-7308-80ac-c46aa94302d0`, media ID `01a211a9-3d30-73b5-9780-a1baf085889f`, `cover_offset_ms: 88550` (`88800 − 250`), status **`draft`**.
  2. **YouTube `@bikindihalaman_id`** (`01a202dc-0e4a-72ae-bec8-589ab7f90045`, `youtube_short`): post ID `01a211a9-6cee-726a-8a3e-e1fbc2fc665a`, media ID `01a211a9-6a6a-70fb-ac62-cef44643e412`, `meta.title: "Bikin Kandang Bebek Petelur Sistem Kering di Halaman"`, status **`draft`**.
  3. **Facebook `Bangun Di Halaman`** (`01a2036c-5179-70c6-b908-25118446326d`, `facebook_reel`): post ID `01a211a9-959f-71c0-ac3a-b0789ca4d518`, media ID `01a211a9-93e0-7266-a97d-f846f33a4ee3`, status **`draft`**.

## Current state

- `stage: publishing`
- `status: complete`
- `next_action: all 3 Trypost drafts verified (not live); upload exports/thumbnail.png manually for YouTube Shorts and Facebook Reels when scheduling/publishing, and run a performance snapshot after publication`
