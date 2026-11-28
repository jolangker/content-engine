# Bikin Petak Minapadi Nila di Halaman

## Brief

- **Slug:** `minapadi-nila-di-halaman`
- **Topic selection:** `topic_selection: auto` (delegated via `--topic=auto` with user scope `"pilihkan topik seputar hybrid yang relevan dengan indonesia dan familiar"`). Evaluated a 10-topic Indonesian backyard hybrid/integrated cultivation shortlist below and selected Candidate #1: building a backyard tarp-lined **Minapadi** plot (*ikan nila* + *padi sawah* in one framed yard bed with a deeper perimeter *caren* trench) from a bare yard corner through 7 single-cause problem–improvement rounds to a stable dual-crop system and first weighed harvest.
- **Board:** `budidaya-di-halaman`, revision 10 (`editorial v9 / visual v5`, status `approved`), explicitly selected via `--board=budidaya-di-halaman`. Inherit [direction](../../boards/budidaya-di-halaman/DIRECTION.md), [editorial framework v9](../../boards/budidaya-di-halaman/EDITORIAL.md), [visual specification v5](../../boards/budidaya-di-halaman/frame.md), [organic SFX kit](../../boards/budidaya-di-halaman/assets/sfx/manifest.json), and [production contract](CONTRACT.json).
- **Contract snapshot:** [CONTRACT.json](CONTRACT.json) copied verbatim from `boards/budidaya-di-halaman/CONTRACT.json` (`editorial v9 / visual v5`, SHA-256 `6681a52a9464efab8b2c846a0b08b731e06fde1e9a947e9772b333d54eac9626`), validated via `episode_qa.py --contract`.
- **Overlap check:** Inspected `TRACKER.json` and `productions/` (all 13 existing `budidaya-di-halaman` productions). Existing episodes cover lined pond + gravel-bed aquaponics (`akuaponik-lele-dan-kangkung`, `aquaponik-pasang-surut`), Nile tilapia settling chamber (`jejak-kotoran-kolam-nila`), BSF maggot ramp (`maggot-jalan-ke-wadah`), leaf-lettuce wick planter (`pot-sumbu-selada`), container potatoes (`kentang-dalam-pot`), redclaw crayfish pond (`kolam-lobster-air-tawar`), standalone catfish tarp pond (`kolam-lele-di-halaman`), dry-litter laying duck coop (`kandang-bebek-petelur-kering`), horizontal drum swamp eel (`kolam-belut-dalam-drum`), betta mini-farm (`ternak-ikan-cupang`), circular wiremesh giant gourami pond (`kolam-gurame-di-halaman`), and elevated stilt kampung chicken coop (`kandang-panggung-ayam-kampung`). None covers **Minapadi** (integrated paddy rice + Nile tilapia in one yard-scale framed tarp plot), the perimeter *caren* trench cutaway, chemical-free *keong mas* stake traps, arched *burung pipit* bird netting, or controlled *pelataran*-to-*caren* harvest draining.
- **Audience & POV:** Indonesian-speaking general viewers curious about backyard cultivation, addressed in warm conversational Indonesian as `"kamu"` (the sole builder/keeper at one consistent yard corner). Gross market-reference estimate only; no profit or payback promise.
- **Format & duration target (inherited from board):** Vertical 9:16 (`1080 × 1920`), 4-plane 2.5D illustrated living backyard cutaway, authored at **90–112.5 s at 1x** (24 fps master restamped to 30 fps at **1.25x** = **72–90 s delivered**, pitch kept), closing with an exact-match thumbnail end card (`0.625 s` 1x / `0.5 s` delivered).
- **Audio plan:**
  - Narration: `use` — `eleven_v4` via `elevenlabs_api` (`tier: starter`, `31,189` chars remaining verified 2026-11-28). Because board default **Pribs** (`5g0yKK2JwTRka0IG61Hh`) returns HTTP 400 (`voice_not_found`) on the active Starter API key, this automated run uses premade **Roger – Laid-Back, Casual, Resonant** (`CwhRBWXzGAHq8TQ4Fs17`) as `episode_override`, matching `ELEVENLABS_VOICE_ID` in Doppler/root `.env` and the established series fallback across recent `budidaya-di-halaman` episodes (`kandang-bebek-petelur-kering`, `ternak-ikan-cupang`, `kolam-gurame-di-halaman`, `kandang-panggung-ayam-kampung`).
  - BGM: `none` for the entire episode.
  - SFX: `use` — board Visual v5 organic SFX library (`boards/budidaya-di-halaman/assets/sfx/manifest.json`) with event-locked foley and low-gain diegetic condition beds.

## Execution, review & delivery policy

```text
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
pre_render_authorization: delegated by the user's --automation instruction
endpoint: publishing
delivery: queue
schedule: account queue slots (Trypost)
trypost_transport: api
```

## Publishing targets

Inherited full default account list from `boards/budidaya-di-halaman/ACCOUNTS.json` (preflight verified live via Trypost REST API `trypost.py check` and `trypost.py accounts --all` on 2026-11-28: `Admin's Workspace` `01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37`, `publishes_directly: true`, all 3 accounts `connected` with `has_posting_schedule: true`, `timezone: Asia/Jakarta`):

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

## Topic discovery shortlist (10 candidates — `topic_selection: auto`)

*Scope:* `"pilihkan topik seputar hybrid yang relevan dengan indonesia dan familiar"` for `budidaya-di-halaman` (`editorial v9 / visual v5`). No board performance analysis (`insights/*/ANALYSIS.md`) exists yet.

1. **Minapadi Nila & Padi dalam Petak Terpal Bercaren di Halaman (RECOMMENDED & SELECTED):** Rakit petak sawah mini berlapis terpal untuk memadukan padi sawah dan ikan nila sekaligus di sudut halaman; berevolusi dari bibit padi tercabut ikan menuju parit *caren* keliling, peneduh parsial *paranet* di atas *caren*, pelimpah berkasa, ajir jebakan keong mas tanpa kimia, aerasi halus, jaring melengkung anti-pipit, hingga pengeringan terkontrol ke *caren* untuk panen ganda nila + beras.
2. **Longyam Halaman (Kandang Ayam + Kolam Ikan Terpisah Penampung):** Sistem hybrid legendaris Indonesia (ayam di atas, ikan di bawah), dilengkapi saringan/penampung kotoran agar amonia tidak meledak di kolam kecil. *(Dilewati: tumpang tindih siluet dengan `kandang-panggung-ayam-kampung` yang baru dibuat dan `kolam-lele-di-halaman`.)*
3. **Budikdamber (Lele + Kangkung dalam Ember 80 L):** Sistem hybrid paling populer di rumah tangga perkotaan Indonesia untuk ikan lele dan kangkung sekaligus. *(Dilewati: tumpang tindih dengan `akuaponik-lele-dan-kangkung` dan merupakan naskah contoh langsung di `EDITORIAL.md`.)*
4. **Vertiminaponik (Menara Pipa Sayur Pakcoy + Kolam Ikan Nila):** Sistem hybrid urban racikan Kementan yang menyatukan talang sayur vertikal dan kolam ikan di bawahnya. *(Dilewati: mekanisme resirkulasi akuaponik tumpang tindih dengan `akuaponik-lele-dan-kangkung` dan `aquaponik-pasang-surut`.)*
5. **Kolam Ikan Nila + Baki Pakan Hidup Azolla Microphylla:** Memadukan kolam nila dengan baki dangkal biakan *Azolla* di sampingnya sebagai sumber pakan hijau berprotein tinggi yang terus tumbuh sendiri.
6. **Polikultur Kolam Terpal Udang Galah + Ikan Nila:** Budidaya hybrid dua lapisan air (udang galah di dasar + nila di kolom tengah) dengan shelter pipa, pemisahan zona pakan, dan aerasi.
7. **Kandang Kelinci Panggung + Boks Cacing Tanah (Vermikompos Kolong):** Memadukan kandang kelinci di atas dengan bak cacing *Lumbricus/ANC* di kolong untuk mengubah kotoran langsung menjadi pupuk kascing dan cacing pakan.
8. **Tabulampot Sambung Pucuk Multi-Varietas (Mangga/Jambu Hibrida di Drum):** Merakit satu batang bawah tahan banting dengan dua sambungan pucuk varietas buah unggulan dalam drum halaman hingga berbuah ganda.
9. **Bedengan Tumpangsari Cabai, Tomat & Kemangi (Companion Hybrid):** Membangun bedengan angkat terpadu untuk tiga tanaman dapur akrab Indonesia yang saling mengusir hama dan panen bergantian.
10. **Longbek / Mina-Itik (Kolam Ikan + Bebek Hibrida Pedaging di Pinggirnya):** Sistem terpadu bebek pedaging dan kolam ikan di halaman. *(Dilewati: tumpang tindih dekat dengan `kandang-bebek-petelur-kering`.)*

**Selection rationale:** Candidate #1 (`minapadi-nila-di-halaman`) is the single most recognizable, culturally iconic Indonesian hybrid cultivation system (*minapadi* = ikan + padi), anchors cleanly in the board's backyard aquaculture pillar with zero overlap across all 13 prior episodes, offers a dramatically fresh cutaway silhouette (golden-green rice stalks above a deep perimeter *caren* swimming channel), and supports 7 genuinely distinct, KKP/Kementan-verified engineering rounds culminating in a dual harvest backed by live 28 Nov 2026 FishInfo Jatim pricing.

## Research and hook selection (agent-selected under active automation)

Research verified all 9 claims (`C1–C9`) against Pustaka BPPSDMP Kementan, BRMP DIY Kementan, KKP technical guidelines, live FishInfo Jatim (`2026-11-28`: Nila consumer average **Rp33.783/kg**), and live SISKAPERBAPO Jatim (`2026-11-27`: Beras Medium Rp13.034/kg / Premium Rp15.091/kg) in [SOURCES.md](SOURCES.md).

Hook options v1 follow Editorial v9's four-slot pattern (`Kalo kamu {aksi pertama}, {konjungsi temporal} kamu {aksi kedua}, kamu sudah punya {sistem}. Tapi {masalah}.`), avoid repeating recent episodes' opening verbs and connectors (`kolam-gurame-di-halaman`: `lingkarkan`/`lalu`; `kandang-panggung-ayam-kampung`: `dirikan`/`begitu`), and stay comfortably inside `10.0 s` (Sentence 1) and `12.0 s` (`"Tapi"`):

1. **Option 1 (Selected — agent choice under active automation) — Biological/root-disturbance surprise (uprooted rice seedlings):**
   - *Mechanism:* Immediate hybrid conflict — viewers assume you can plant rice and drop tilapia into the same muddy plot on day one, so watching seedlings float uprooted the next morning sparks instant curiosity about how fish and rice actually coexist.
   - *First verb / connector:* `hamparkan` / `kemudian`
   - *Spoken line (25 words; Sentence 1 = 19 words ≈ `7.6 s ≤ 10.0 s`; `"Tapi"` at word 20 ≈ `8.0 s ≤ 12.0 s`):*
     > “Kalo kamu hamparkan terpal isi lumpur di halaman, kemudian kamu tanam padi dan lepas nila, kamu sudah punya minapadi. Tapi besoknya bibit padinya mengambang tercabut.”
   - *Frame 0 & `<1.0 s` motion:* Bare warm-clay yard corner with folded teal tarp, timber/bamboo border slats, and rice seedling tray; at `0.25 s`, hands spread the tarp over the low frame, fill dark paddy mud and water, plant tidy rows of bright green rice shoots, and release tilapia fingerlings, then morning light reveals uprooted rice shoots floating as fish stir the shallow floor.
   - *On-screen line:* 46 px DM Sans 800 progressive captions (max 2 lines); thumbnail/cover promise **Bikin minapadi / di sudut halaman** (yellow on **minapadi**).
   - *Promise:* Shows why flat simultaneous stocking fails and develops the exact same framed tarp plot through 7 real minapadi upgrades (*caren*, partial *paranet*, screened overflow, chemical-free *keong mas* stake trap, fine aeration, arched bird net, controlled harvest drain) to a stable dual harvest.
2. **Option 2 — Midday thermal shock puzzle (environmental trigger):**
   - *First verb / connector:* `susun` / `setelah itu`
   - *Spoken line (25 words):* “Kalo kamu susun petak terpal isi lumpur di halaman, setelah itu kamu tanam padi dan tebar nila, kamu sudah punya minapadi. Tapi pas siang nilanya megap-megap kepanasan.” *(Frame 0: bare yard corner, flat tarp paddy built and stocked, midday sun beats down on shallow water; skips the signature rice-root vs fish-refuge *caren* motivation up front.)*
3. **Option 3 — Rain overflow escape surprise (weather trigger):**
   - *First verb / connector:* `rakit` / `habis itu`
   - *Spoken line (25 words):* “Kalo kamu rakit bingkai terpal sawah di halaman, habis itu kamu tanam padi dan isi nila, kamu sudah punya minapadi. Tapi sekali hujan deras, nilanya hanyut meluap.” *(Frame 0: bare yard corner, plot filled and planted, storm pours over rim; less unique to the rice+fish hybrid dynamic than Option 1.)*

- `hook_selection: auto` (delegated under active `--automation`). Selected **Option 1** because uprooted rice seedlings visually dramatize the *exact* core conflict of a hybrid fish-plus-rice system, immediately motivate the signature *caren* (deep perimeter trench) cutaway upgrade in Round 1, use a fresh verb/connector (`hamparkan` / `kemudian`), and chain cleanly into all 7 rounds.

## Script check (v1 — agent-verified under active automation)

[SCRIPT.md](SCRIPT.md) v1 is built around Hook Option 1 across 11 scenes (18 meaningful events).

- **Spoken word count & budget:** **235 spoken words** (`25 + 22 + 20 + 19 + 22 + 19 + 19 + 21 + 18 + 26 + 24`). Budgeted via `episode_qa.py --budget 235 --voice CwhRBWXzGAHq8TQ4Fs17` (Roger measured `2.49 wps`, `words_for_range: [210, 263]`, predicted raw narration `~94.4 s`, predicted 1x film `~100.9 s` inside `90.0–112.5 s`, delivered 1.25x `~80.7 s`). Reconcile after synthesis.
- **First sentence & `"Tapi"` turn:** Sentence 1 = **19 words** (predicted `~7.6 s ≤ 10.0 s`); `"Tapi"` at word 20 (predicted `~8.0 s ≤ 12.0 s`). Total `"tapi"` occurrences in full script: **1** (hook only).
- **Selected hook three parts:** Option 1 spoken line, Frame 0 bare corner + `<0.25 s` tarp spread / planting / stocking + uprooted seedlings, and 46 px DM Sans 800 progressive captions recorded above and in [SCRIPT.md](SCRIPT.md).
- **Cold-read & POV check:** Read all 235 spoken words standalone without headings or visual cues. `"kamu"` refers consistently to the single backyard builder/keeper throughout; every problem, physical fix, and result is clear on audio alone. Repairs applied before locking v1: (1) removed stacked cat+bird mention in Round 6 so Round 6 focuses strictly on a single cause (*burung pipit* attacking ripening grain); (2) changed Round 1 verb from `"gali"` to `"bentuk parit caren dalam"` so it remains physically coherent inside a tarp-lined yard frame; (3) varied construction verbs (`hamparkan`, `bentuk`, `tarik`, `pasang`, `tancap`, `buka`) across scenes and verified zero mechanical `"Tapi"` repetition.
- **Contract judged rules (script scope):**
  - `hook-frame`: **pass** — Frame 0 shows bare yard corner with folded tarp/frame slats and motion at `0.25 s` under 46 px captions.
  - `pictures-alone`: **pass** — All 11 scenes define concrete sequential visual sub-beats showing cause, added part, and tested effect.
  - `event-density`: **pass** — 11 scenes / 18 distinct physical events beyond captions.
  - `motion-variety`: **pass** — Shot scales alternate (`wide` → `close cutaway` → `medium` → `medium-wide` → `close cutaway` → `medium` → `medium-wide` → `close cutaway` → `wide` → `medium` → `wide`; max consecutive same shot = 1).
  - `subject-scale` & `vessel-scale`: **pass** — Framed minapadi plot, *caren* cutaway, hanging weigh-scale, and harvest rice basket planned at ≥40% frame width with consistent yard landmarks.
  - `ear-test`: **pass** — Standalone cold read passed after the 3 repairs above; single `"kamu"` POV throughout.
  - `build-first`: **pass** — Hook Option 1 completes all four Editorial v9 slots with ordinary punctuation and fresh verb/connector (`hamparkan` / `kemudian`).
  - `shortfall-before-fix`: **pass** — 7 single-cause rounds (19–22 words / `~7.6–8.8 s` each at 1x), each tested on screen, distinct triggers (`bibit tercabut`, `panas siang`, `luapan hujan`, `hama keong mas`, `air keruh/oksigen`, `burung pipit`, `panen ikan di sela padi`), varied transitions (`Pas tengah hari`, `Begitu hujan deras turun`, `Seminggu jalan`, `Masuk bulan kedua`, `Giliran bulir padi menguning`, `Masalahnya`), `"Tapi"` only in hook.
  - `same-system`: **pass** — Every installed feature (deep perimeter *caren*, partial *paranet* over *caren*, screened overflow pipe, bamboo *ajir* stakes, *caren* air stone, arched bird net, controlled drain plug) remains legible on the exact same plot through Scene 11.
  - `final-job`: **pass** — Scene 9 shows the completed minapadi plot thriving through sun/rain with clear aerated *caren*, lush golden rice, and healthy tilapia before calling it stable.
  - `income-scene`: **pass** — Scene 10 weighs `15 kg` tilapia beside the finished minapadi plot (`15 kg × Rp34.000 ≈ Rp510.000`, `estimasi harga pasar / Nov 2026`, sourced from FishInfo Jatim 28 Nov 2026) with harvested rice beside it for home kitchen use, rounded spoken numbers, ≥3 s 1x hold, zero profit/payback claim.
  - `event-map`: **pass** — 18 events (`15–19`); every finished component enters visibly.
  - `closing-lines` & `closing-signature`: **pass** — Ends with congratulation naming the built minapadi plot + next-build question containing consecutive `"bikin di halaman"`, yellow hold + `@bikindihalaman.id`, hard cut to `0.625 s` 1x (`0.5 s` delivered) exact-match thumbnail end card.
  - `reframing`, `living-world`, `event-sfx`: **pass** — Plans beat-level push-ins/pans/micro-impacts, 4-plane 2.5D parallax & reactive weather, and frame-locked organic SFX from board Visual v5 library (`bgm: none`).

## Storyboard verification (agent-verified under active automation)

- **Plan:** [video/STORYBOARD.md](video/STORYBOARD.md) — 11 frames (`105.250 s` measured 1x = `84.200 s` at 1.25x), 18 events, shot variety max run 1 (`wide` / `close cutaway` / `medium` / `medium-wide` alternating), `storyboard_lint.py --strict` passed (`0` errors, `0` warnings).
- **Styled stills & poses:**
  - [video/boards/stills/](video/boards/stills/) — 11 styled `1080 × 1920` stills (`frame-00-at-8.6s.png` .. `frame-10-at-103.7s.png`), visually inspected and refreshed after Pass 2 upgrades.
  - [video/boards/poses/](video/boards/poses/) — 25 progression poses (`hook-0.0s.png`, `hook-0.8s.png`, `hook-3.0s.png`, plus `01-a-start.png`..`11-b-end.png`).
  - [video/boards/storyboard.html](video/boards/storyboard.html) & [video/boards/storyboard.png](video/boards/storyboard.png) (`36/36` images loaded, `DM Sans` loaded, `0` broken images, `0` desktop/mobile overflow). Inspected saved PNG directly.
- **Gate verdict:** `episode_qa.py --stage storyboard` **passed** (`video/verification/quality-gate-storyboard.json`, `disclose: []`).

## Current state

- `stage`: publishing
- `status`: complete
- `next_action`: optionally upload `exports/thumbnail.png` manually as the Shorts/Reel cover in YouTube Studio and Meta Business Suite (`supports_video_cover: false` via Trypost; Instagram already uses `cover_offset_ms: 83950`), then run a performance review snapshot 48–72 hours after scheduled publications go live on `2026-11-29`.

## Delivery summary & verification record (2026-11-28)

- **Audio (`eleven_v4` + quiet boundaries + 37 SFX):** Generated single 242-word continuous take in **Roger** (`CwhRBWXzGAHq8TQ4Fs17`, `episode_override`, `elevenlabs_api` Starter tier) via `narration.py --auto-align` (`100.0 s`), placed clean pauses via `audio_boundaries.py` (`10/10` boundaries passed), applied 37 frame-locked organic SFX cues from the board Visual v5 library (`bgm: none`) via `sound_design.py`, natively listened to raw take, 1× proof mix, and 1.25× export (`listening: agent`), and passed `sound_design.py --export` (`37/37` cues, `28.81 dB` median vocal-band SNR, `0.025 s` max severe masking, `<= 0.02 ms` offset).
- **Verification & independent audit:** Rendered `video/verification/proof.mp4` (`1080×1920`, `24 fps`, `105.250 s`), passed `hyperframes check --json` (`ok: true`, 0 errors) and `dom_lint.py` (`11/11` scenes, `0` G5 / `0` readcheck fails). Fresh-context subagent reviewer (`15f5a892-7c11-4dd4-8557-2b5539ecb4ce`) audited Pass 1 (`NEEDS REVISION BEFORE RENDER`, 4 P0 + 5 P1), all P0s and P1s were fixed (`sfx-s05-bucket-drop` re-anchored to `"Batang"` occ=2 at `45.174 s`, `s10` gantry/price tag lifted into open sky at `world y=211.3`, high-contrast split-bamboo `ajir` stakes with red bands persistent `s05–s11`, `s08` overhead diagonal scoop handle, grounded `s05` bucket & `s11` dual harvest baskets, falling `s09` pellets, partial sickle-harvested `s10` rice stubble), and Pass 2 returned **`APPROVE FOR DELIVERY RENDER`** (`18/18` judged rules passed, `0` open P0s, 6/7 rubric dimensions `8.0/10` and `finish_texture 7.0/10`, recorded in [`video/REVIEW.md`](video/REVIEW.md)). Passed `episode_qa.py --stage verification --dom-lint` (`video/verification/quality-gate-verification.json`, `disclose: []`).
- **Export (`1.25×` pitch-kept, 30 fps):** Rendered 24 fps delivery master (`video/out/master-24fps.mp4`, `67,238,149` bytes, `105.250 s`) and retimed to [`exports/minapadi-nila-di-halaman.mp4`](exports/minapadi-nila-di-halaman.mp4) (`33,732,623` bytes, SHA-256 `07318c436a631f29134a51157a36c260594bb9a4a685d5304219be4befb1abfb`, `84.200 s`, `1080×1920`, `30.0 fps`, `2,526` frames, **`-14.05 LUFS`**, **`-2.76 dBTP`**), plus [`exports/thumbnail.png`](exports/thumbnail.png) (`303,410` bytes, SHA-256 `fcf34f0d0c4220a47a506f56f9bc54bd814442eee041c3ace0b39fbf430ff662`) and [`exports/minapadi-nila-di-halaman.srt`](exports/minapadi-nila-di-halaman.srt) (`49` cues, `3,417` bytes). Listened natively to 1.25× mix, inspected `thumbnail.png`, and passed `episode_qa.py --stage export` (`video/verification/quality-gate-export.json`, `disclose: []`).
- **Content package & Trypost queue delivery (`transport: api`):** Shared Indonesian copy documented in [`CONTENT_PACKAGE.md`](CONTENT_PACKAGE.md). Uploaded MP4 once in `Admin's Workspace` (`01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37`), scheduled all 3 inherited accounts via `queue: next`, verified `scheduled` status & future slots via `GET /posts/{id}`, and saved schema v2 receipt in [`PUBLISHING.json`](PUBLISHING.json):
  - **Instagram (`@bikindihalaman.id`, `instagram_reel`):** post `01a21fee-0dcb-7118-9d43-d7f784fba3f3` — `scheduled` (`schedule_mode: queue`) for `2026-11-29 02:48:00` UTC (`09:48 WIB`, `cover_offset_ms: 83950`).
  - **YouTube (`@bikindihalaman_id`, `youtube_short`):** post `01a21fee-3a1f-7119-bf53-6288df76a7ee` — `scheduled` (`schedule_mode: queue`) for `2026-11-29 05:40:00` UTC (`12:40 WIB`, `meta.title: "Bikin Petak Minapadi Nila di Halaman"`).
  - **Facebook (`Bangun Di Halaman`, `facebook_reel`):** post `01a21fee-5be8-70c7-89ec-744178cfd229` — `scheduled` (`schedule_mode: queue`) for `2026-11-29 02:21:00` UTC (`09:21 WIB`).

## Google Drive archive (synced)

- **Folder:** [`budidaya-di-halaman/minapadi-nila-di-halaman`](https://drive.google.com/drive/folders/1uxUgPwRxNvtvz7xELmzZedq-H9A6PPIk) (`folder_id: 1uxUgPwRxNvtvz7xELmzZedq-H9A6PPIk`, `remote_path: budidaya-di-halaman/minapadi-nila-di-halaman`, synced `2026-11-27T20:13:49Z` via `gdrive.py` using Doppler, `env_source: doppler+dotenv`):
  - `minapadi-nila-di-halaman.mp4` (`33,732,623` bytes, MD5 `51f8a00e9651226d3656750922670256`, `uploaded`, file `1bEG7d1fOjEXAObVr8gJq3i2hwLOyYi9Y`)
  - `minapadi-nila-di-halaman.srt` (`3,417` bytes, MD5 `00c09cca2c4259a32a3671e698646a0e`, `uploaded`, file `1yv6WA3lWK0ICz8SJjXzfvn55dWo2GEqv`)
  - `thumbnail.png` (`303,410` bytes, MD5 `6cede29235dbd41a8a25bf90c161bcf0`, `uploaded`, file `1hNSkrpmKM4OvqIqdYf2kd_JDZfvZWqXY`)
  - `CONTENT_PACKAGE.md` (`6,217` bytes, MD5 `7c03bd69f026dd112f2b861baf155d10`, `uploaded`, file `12JTFhI01kFDQ14HnK5hqWNxheVI-4B9G`)
