# Bikin Kandang Panggung Ayam Kampung di Halaman

## Brief

- **Slug:** `kandang-panggung-ayam-kampung`
- **Topic selection:** `topic_selection: auto` (delegated via `--topic=auto` with user scope `"pilihkan topik seputar ternak ayam"`). Evaluated a 10-topic backyard chicken-keeping shortlist below and selected Candidate #1: building an elevated bamboo stilt coop (*kandang panggung*) for 20 backyard *ayam kampung / KUB* from a bare yard corner through 7 single-cause problem–improvement rounds to a stable system and first counted market-reference harvest.
- **Board:** `budidaya-di-halaman`, revision 10 (`editorial v9 / visual v5`, status `approved`), explicitly selected via `--board=budidaya-di-halaman`. Inherit [direction](../../boards/budidaya-di-halaman/DIRECTION.md), [editorial framework v9](../../boards/budidaya-di-halaman/EDITORIAL.md), [visual specification v5](../../boards/budidaya-di-halaman/frame.md), [organic SFX kit](../../boards/budidaya-di-halaman/assets/sfx/manifest.json), and [production contract](CONTRACT.json).
- **Contract snapshot:** [CONTRACT.json](CONTRACT.json) copied verbatim from `boards/budidaya-di-halaman/CONTRACT.json` (`editorial v9 / visual v5`, SHA-256 `6681a52a9464efab8b2c846a0b08b731e06fde1e9a947e9772b333d54eac9626`), validated via `episode_qa.py --contract`.
- **Overlap check:** Inspected `TRACKER.json` and `productions/`. Existing `budidaya-di-halaman` episodes cover fish, crayfish, aquaponics, BSF maggots, container vegetables, and one ground-level dry-litter laying duck coop (`kandang-bebek-petelur-kering`). Zero episodes cover chickens (*ternak ayam*), elevated stilt coops (*kandang panggung*), under-coop manure pits with lime/husks, hanging back-height feeders, nipple drinker lines, or wooden roosting perches. Choosing meat-type backyard *ayam kampung / KUB* in an elevated stilt coop also creates a clear visual and payoff distinction from the ground-level laying duck coop (no ground-level husk floor or egg-tray counting repeat).
- **Audience & POV:** Indonesian-speaking general viewers curious about backyard cultivation, addressed in natural conversational Indonesian as `"kamu"` (the sole builder/keeper in one consistent yard corner throughout). Practical household-scale build without profit or income guarantees.
- **Format & duration target (inherited from board):** Vertical 9:16 (`1080 × 1920`), 4-plane 2.5D illustrated living backyard cutaway, authored at **90–112.5 s at 1x** (24 fps master restamped to 30 fps at **1.25x** = **72–90 s delivered**, pitch kept), closing with an exact-match thumbnail end card (`0.625 s` 1x / `0.5 s` delivered).
- **Audio plan:**
  - Narration: `use` — `eleven_v4` on `elevenlabs_api` (`rem: 2,661` chars on configured free-tier key). Because board default **Pribs** (`5g0yKK2JwTRka0IG61Hh`) returns HTTP 400 (`voice_not_found`) on the configured free-tier API key, this automated run uses premade **Roger – Laid-Back, Casual, Resonant** (`CwhRBWXzGAHq8TQ4Fs17`) as `episode_override`, matching `ELEVENLABS_VOICE_ID` in Doppler/root `.env` and the user-established free-tier fallback across recent `budidaya-di-halaman` episodes (`kandang-bebek-petelur-kering`, `ternak-ikan-cupang`, `kolam-gurame-di-halaman`).
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

*Scope:* `"pilihkan topik seputar ternak ayam"` for `budidaya-di-halaman` (`editorial v9 / visual v5`). No board performance analysis (`insights/*/ANALYSIS.md`) exists yet.

1. **Kandang Panggung Ayam Kampung (KUB) di Halaman (RECOMMENDED & SELECTED):** Bangun kandang panggung bambu berkolong di sudut halaman untuk 20 ekor ayam kampung/KUB pembesaran; berevolusi dari nampan pakan dicakar tumpah, bau amonia kolong, air minum kotor, panas siang, tampias hujan/angin malam, kaki terselip tanpa tenggeran, hingga tikus malam, sampai panen 20 ekor siap potong.
2. **Kandang Baterai Mini Ayam Petelur Roll-Out di Lorong Samping:** Rakit kandang miring bertingkat untuk 10–12 ayam petelur agar telur menggelinding bersih ke luar, melalui kalibrasi kemiringan, bocor pipa minum, panas, kotoran nampan, hingga panen krat telur mingguan. *(Dilewati: payoff hitung krat telur terlalu dekat dengan `kandang-bebek-petelur-kering`.)*
3. **Kandang Umbaran Semi-Intensif Ayam Kampung Berpagar Jaring:** Buat area umbaran berpagar dan rumah tidur kecil di halaman, menghadapi ayam terbang melompati pagar, kutu tanpa bak mandi debu, hujan, sarang bertelur, dan predator malam.
4. **Boks Brooder Pemanas DOC Ayam Kampung (Fase 0–4 Minggu):** Rakit boks kayu penghangat anak ayam baru menetas dengan lampu pijar, berevolusi mengatasi kedinginan/kepanasan, lantai kawat, tirai angin, minum anti-basah, hingga panen anakan sehat umur sebulan.
5. **Kandang Ayam Kate / Ayam Hias Vertikal di Sudut Teras:** Susun aviary mungil bertingkat untuk sepasang ayam hias dengan tenggeran, alas pasir, pintu ganda anti-kabur, dan kotak eram sampai menetaskan anakan.
6. **Kandang Ayam Kampung Sistem Deep Litter Fermentasi (Tanpa Bau):** Bangun kandang lantai tanah beralas sekam fermentasi untuk menekan bau di lingkungan padat penduduk, melalui penyeimbangan kelembapan, pengadukan, dan sirkulasi udara. *(Dilewati: siluet lantai tanah + sekam terlalu mirip `kandang-bebek-petelur-kering`.)*
7. **Kandang Traktor Ayam (Chicken Tractor) Roda Dorong di Rumput:** Rakit kandang segitiga ringan beroda yang digeser tiap beberapa hari di rumput halaman untuk ayam kampung, lengkap dengan apron anti-gali, peneduh, dan minum gantung anti-tumpah.
8. **Kandang Pembesaran & Boks Jemur Ayam Pelung / Kampung Jago:** Bangun kandang pembesaran bersekat dengan kurungan jemur pagi, tempat pakan anti-tumpah, dan atap teduh untuk membesarkan ayam kampung jantan.
9. **Integrasi Kandang Ayam Kampung + Boks Maggot BSF Hemat Pakan:** Padukan kandang ayam kecil dengan boks biokonversi maggot BSF dari sisa dapur sebagai tambahan protein pakan untuk menekan biaya pakan harian. *(Dilewati: tumpang tindih sebagian dengan `maggot-jalan-ke-wadah`.)*
10. **Inkubator / Mesin Tetas Telur Ayam Kampung DIY Boks Kayu:** Rakit boks penetas bertermostat dengan rak putar dan baki air kelembapan, melalui kalibrasi titik dingin, kipas sirkulasi, pemutaran rutin, dan teropong telur hingga menetas.

**Selection rationale:** Candidate #1 (`kandang-panggung-ayam-kampung`) is the clearest, most universally relatable Indonesian backyard chicken build after *"bikin kandang panggung ayam kampung di halaman sendiri"*, introduces a brand-new elevated two-level cutaway silhouette (*lantai panggung* + *kolong kotoran*) that looks totally distinct from both fish ponds and the ground-level duck pen, and delivers 7 concrete, independently verified poultry-husbandry rounds leading to a 20-bird harvest payoff backed by live SISKAPERBAPO East Java data (27 Nov 2026).

## Research and hook selection (agent-selected under active automation)

Research verified all 9 claims (`C1–C9`) against Kementerian Pertanian (BBPP Kupang, BRMP Jatim, Ditjen PKH), PT Medion veterinary/husbandry articles, and live SISKAPERBAPO Jawa Timur (`2026-11-27`: `Daging Ayam Kampung / ekor` = **Rp70.029/ekor**) in [SOURCES.md](SOURCES.md).

Hook options v1 follow Editorial v9's four-slot pattern (`Kalo kamu {aksi pertama}, {konjungsi temporal} kamu {aksi kedua}, kamu sudah punya {sistem}. Tapi {masalah}.`), avoid repeating the previous episode's (`kolam-gurame-di-halaman`) first verb (`lingkarkan`) and connector (`lalu`), and stay inside `10.0 s` (Sentence 1) and `12.0 s` (`"Tapi"`):

1. **Option 1 (Selected — agent choice under active automation) — Scratch-and-spill surprise (behavioral failure):**
   - *Mechanism:* Counter-intuitive poultry behavior clash — viewers assume a slatted bamboo floor solves cleanliness immediately, so watching chickens scratch half their feed straight through the slats into the under-coop pit sparks instant curiosity.
   - *First verb / connector:* `dirikan` / `begitu`
   - *Spoken line (26 words; S1 = 19 words ≈ `7.9 s ≤ 10.0 s`; `"Tapi"` at word 20 ≈ `8.3 s ≤ 12.0 s`):*
     > “Kalo kamu dirikan panggung bambu di halaman, begitu kamu masukkan ayam dan nampan pakan, kamu sudah punya kandang ayam. Tapi sorenya separuh pakannya jatuh ke kolong.”
   - *Frame 0 & `<1.0 s` motion:* Bare warm-clay yard corner with stacked bamboo stilts/slats ready; at `0.25 s` hands plant the stilt posts, lay the bamboo slatted deck, set down an open feed tray, and release young chickens, then afternoon light arrives as chickens scratch feed raining down through the floor gaps into the pit.
   - *On-screen line:* 46 px DM Sans 800 progressive captions (max 2 lines); thumbnail promise **Kandang panggung / ayam kampung** (yellow on **ayam kampung**).
   - *Promise:* Explains why open trays waste feed on slatted floors and develops the exact same stilt coop through 7 physical upgrades to a healthy 20-bird harvest.
2. **Option 2 — Ammonia pit odor shock (environmental trigger):**
   - *First verb / connector:* `rakit` / `setelah itu`
   - *Spoken line (26 words):* “Kalo kamu rakit kandang panggung dari bambu di halaman, setelah itu kamu lepas dua puluh ayam kampung, kamu sudah punya ternak ayam. Tapi tiga hari jalan, kolongnya bau amonia.” *(Frame 0: bare yard corner, bamboo stilt coop assembled and stocked, dark odor lines rise from damp pit; slightly closer to duck-coop odor hook.)*
3. **Option 3 — Night crowding & slipped toes puzzle (welfare trigger):**
   - *First verb / connector:* `bangun` / `habis itu`
   - *Spoken line (26 words):* “Kalo kamu bangun lantai bambu panggung di sudut halaman, habis itu kamu masukkan ayam kampung muda, kamu sudah punya kandang ayam. Tapi malamnya ayamnya berdesakan dan kakinya terselip.” *(Frame 0: bare yard corner, stilt floor built and stocked, night falls and birds huddle on bare slats; starts in night lighting rather than bright yard action.)*

- `hook_selection: auto` (delegated under active `--automation`). Selected **Option 1** because chickens scratching feed straight down through bamboo floor slats is uniquely iconic to an elevated *kandang panggung*, reads unmistakably on mute in a 2.5D vertical cutaway, avoids repeating an odor/mud opening from `kandang-bebek-petelur-kering`, and sets up all 7 upgrades in clean chronological order.

## Script check (v1 — agent-verified under active automation)

[SCRIPT.md](SCRIPT.md) v1 is built around Hook Option 1 across 11 scenes (18 meaningful events).

- **Spoken word count & budget:** **236 spoken words** (`26 + 20 + 21 + 20 + 20 + 21 + 20 + 20 + 19 + 25 + 24`). Budgeted with `episode_qa.py --budget 236 --voice CwhRBWXzGAHq8TQ4Fs17` (verified below; at Roger's ~2.39 wps, raw narration ≈ `98.7 s`, 1x film ≈ `105–107 s` inside `90.0–112.5 s`, delivered 1.25x ≈ `84–86 s`). Reconciled after narration synthesis.
- **First sentence & `"Tapi"` turn:** Sentence 1 = **19 words** (predicted `~7.9 s <= 10.0 s`); `"Tapi"` at word 20 (predicted `~8.3 s <= 12.0 s`). Total `"tapi"` occurrences in full script: **1** (hook only).
- **Selected hook three parts:** Spoken line, Frame 0 bare yard corner + `0.25 s` bamboo stilt assembly + feed-scratch spill, and 46 px DM Sans 800 captions recorded above and in [SCRIPT.md](SCRIPT.md).
- **Cold-read & POV check:** Read all 236 spoken words standalone without headings or visual cues. `"kamu"` refers consistently to the single backyard builder/keeper throughout; every problem, upgrade, and result makes standalone sense on audio alone. Repairs applied before locking v1: (1) replaced second night-time cue in Round 7 (`Suatu malam` → `Seminggu kemudian`) so Rounds 6 and 7 do not repeat night openers back-to-back; (2) spelled `nipel` naturally in Indonesian (`pipa minum nipel gantung`) to avoid English loanword TTS glitches; (3) shortened S01 Sentence 1 from 21 to 19 words for ample margin under 10.0 s.
- **Contract judged rules (script scope):**
  - `hook-frame`: **pass** — Frame 0 shows bare clay yard corner with stacked bamboo poles and motion at `0.25 s` under 46 px captions.
  - `pictures-alone`: **pass** — All 11 scenes specify concrete sequential sub-beats showing cause, added component, and tested outcome.
  - `event-density`: **pass** — 11 scenes / 18 distinct physical events beyond captions.
  - `motion-variety`: **pass** — Shot scales alternate (`wide` → `close cutaway` → `medium` → `close cutaway` → `medium-wide` → `medium` → `close cutaway` → `medium-wide` → `wide` → `medium` → `wide`; max consecutive same shot = 1).
  - `subject-scale` & `vessel-scale`: **pass** — Elevated stilt coop, under-coop pit, hanging feeder/nipple line, perch bar, and harvest crates planned at ≥40% frame width with consistent yard landmarks.
  - `ear-test`: **pass** — Standalone cold read passed after the 3 repairs above; single `"kamu"` POV throughout.
  - `build-first`: **pass** — Hook Option 1 completes all four Editorial v9 slots verbatim with ordinary punctuation and fresh verb/connector (`dirikan` / `begitu`).
  - `shortfall-before-fix`: **pass** — 7 single-cause problem–improvement rounds (20–21 words / ~8.4–9.2 s each at 1x), each tested on screen, distinct triggers (`ceker pakan tumpah`, `amonia kolong`, `air minum kotor`, `stres panas siang`, `hujan angin dingin`, `tidur tanpa tenggeran`, `tikus malam`), varied transitions (`Tiga hari jalan`, `Masalahnya`, `Pas tengah hari`, `Begitu hujan angin turun`, `Malam harinya`, `Seminggu kemudian`), `"Tapi"` only in hook.
  - `same-system`: **pass** — Every installed upgrade (hanging feeder, husk+lime pit, nipple drinker line, vented slanted roof, roll-down tarp curtain, round wooden roosts, fine wire mesh) remains visible on the same stilt coop through Scene 11.
  - `final-job`: **pass** — Scene 9 shows the completed stilt coop coping with sun/rain, dry pit, intact feed, and healthy chickens before calling it `"stabil"`.
  - `income-scene`: **pass** — Scene 10 counts 20 market-ready chickens beside the finished coop with world-anchored hanging price tag `20 ekor × Rp70.000 ≈ Rp1.400.000` (`estimasi harga pasar / Nov 2026`, sourced from SISKAPERBAPO Jatim 27 Nov 2026), rounded spoken figures, ≥3 s 1x hold, zero profit/payback claim.
  - `event-map`: **pass** — 18 events (within 15–19); every component visibly enters the build.
  - `closing-lines` & `closing-signature`: **pass** — Ends with congratulation naming the built stilt coop + next-build question containing consecutive `"bikin di halaman"`, yellow hold + `@bikindihalaman.id`, hard cut to `0.625 s` 1x (`0.5 s` delivered) exact-match thumbnail end card.
  - `reframing`, `living-world`, `event-sfx`: **pass** — Plans beat-level push-ins/pans/micro-impacts, 4-plane 2.5D parallax & reactive weather, and frame-locked organic SFX from board Visual v5 library (`bgm: none`).

## Storyboard verification (agent-verified under active automation)

- **Plan:** [video/STORYBOARD.md](video/STORYBOARD.md) — 11 frames (`100.250 s` measured 1x = `80.200 s` delivered at 1.25x), 18 events, alternating shot scales (`max consecutive same shot = 1`), `storyboard_lint.py --strict` passed (`0` errors, `0` warnings).
- **Styled stills & poses:** [video/boards/stills/](video/boards/stills/) (`11` stills) and [video/boards/poses/](video/boards/poses/) (`25` poses), rendered into [video/boards/storyboard.html](video/boards/storyboard.html) and [video/boards/storyboard.png](video/boards/storyboard.png) (`36/36` images loaded, `0` broken, `0` overflow, refreshed from Pass 2 final compositions).
- **Gate verdict:** `episode_qa.py --stage storyboard` **passed** ([video/verification/quality-gate-storyboard.json](video/verification/quality-gate-storyboard.json), `disclose: []`).

## Audio, verification & independent jury audit

- **Narration (`eleven_v4`, `elevenlabs_api`):** Synthesized single continuous 234-word take using `Roger` (`CwhRBWXzGAHq8TQ4Fs17`, `episode_override` matching prior board episodes because board default `Pribs` `5g0yKK2JwTRka0IG61Hh` returns HTTP 400 on the free-tier key) at `video/.media/audio/voice/narration-0032d0d6cdf1224bc9a9.mp3` (`93.84 s`, `request_sha256: 0032d0d6cdf1224bc9a9631a871d8ef2960abcf9872cfda354e51f5d56d9a4fd`). Natively listened (`listening: agent`): clean Indonesian pronunciation, zero tags read aloud.
- **Acoustic boundaries & organic SFX (`bgm: none`, `sfx: use`):** Placed 10 quiet boundaries via `audio_boundaries.py` (`0.18 s` after S01–S09, `3.60 s` after S10 giving `3.679 s` 1x price-tag hold), normalized once to `-14.0 LUFS / -1.5 dBTP` at `video/assets/audio/narration.wav` (`100.250 s` total 1x; `end_card_start: 99.625 s`, `end_card_duration: 0.625 s`). Mixed **36 frame-locked organic SFX cues** (`14` unique board Visual v5 CC0/Pixabay assets) via `sound_design.py`.
- **Independent 7-dimension jury audit ([video/REVIEW.md](video/REVIEW.md), fresh-context subagent `1979e78c-cf70-47c2-a377-3acb1d09406a`):**
  - Pass 1 returned `REVISE BEFORE RENDER` (4 P0s, 5 P1s, `s07` weakest-shot overhaul, `s04` 2.25× `wow_upgrade`).
  - After applying all Pass 1 fixes (`composition_sha256: 0d6b47ace4c223e069211a2984a059098995e88459c98bb3ceed4bd2894372d3`), Pass 2 returned **`APPROVE FOR DELIVERY RENDER`** — **18/18 judged rules passing**, `0` open P0s, rubric `style_fidelity: 8.0`, `concept_wow: 7.5`, `motion_craft: 7.5`, `design_typography: 8.0`, `finish_texture: 7.5`, `sound_sync: 7.5`, `technical: 8.0`; `weakest_shot: s10`.
- **Automated verification receipts (all passing):** `dom_lint.py` (`0` G5 / `0` readcheck), `hyperframes check --json` (`ok: true`, `0` errors), `audio_boundaries.py --export` (`10/10`), `sound_design.py --export` (`36/36` cues passed, `28.78 dB` median vocal-band SNR, `0.0 s` severe masking), and `episode_qa.py --stage verification --dom-lint` (`status: passed`, `disclose: []`).

## Export & content package

- **1x 24 fps master:** [video/out/master-24fps.mp4](video/out/master-24fps.mp4) (`49,823,403` bytes, SHA-256 `cea4ec70a6ef8db71887df57c08d0bdb515ce29590c6230ae9dcffa896075a2f`), verified with `audio_boundaries.py` (`10/10`) and `sound_design.py` (`36/36`).
- **Delivered 1.25x / 30 fps MP4:** [exports/kandang-panggung-ayam-kampung.mp4](exports/kandang-panggung-ayam-kampung.mp4) (`26,106,217` bytes, SHA-256 `619b83a146cc9e0092307af715afa15e00a6d4411539c3c672edfae9ddcf3858`, `80.200 s`, `1080 × 1920`, `30.0 fps`, `2,406` frames, H.264 High `yuv420p` + AAC 48 kHz stereo `192 kbps`, `-14.05 LUFS`, `-2.81 dBTP`). Natively listened at 1.25x (`listening: agent`).
- **Companion files:** [exports/thumbnail.png](exports/thumbnail.png) (`217,649` bytes, SHA-256 `0ddd89188f6cb0870a01d13f4cc2520e00eb40691410b188b2a12683a15e804d`), [exports/kandang-panggung-ayam-kampung.srt](exports/kandang-panggung-ayam-kampung.srt) (`44` cues, `3,208` bytes, SHA-256 `cde1ffb921c6b7de3b947eba8c44f786f68ab5ba3699af47a17a2565a170c702`), and [CONTENT_PACKAGE.md](CONTENT_PACKAGE.md).
- **Export quality gate:** [video/verification/quality-gate-export.json](video/verification/quality-gate-export.json) — **`passed`** (`disclose: []`, `hook-motion: 0.2 s`, `empty-frames: 0`, `end-hold: 0.2 s`, `longest_static_seconds: 0.0` across all 11 scenes).

## Google Drive archive (synced)

- **Folder:** [`budidaya-di-halaman/kandang-panggung-ayam-kampung`](https://drive.google.com/drive/folders/1LwDwJM_EAoIEWNF5tvHwh6rc52u0WowP) (`folder_id: 1LwDwJM_EAoIEWNF5tvHwh6rc52u0WowP`, `remote_path: budidaya-di-halaman/kandang-panggung-ayam-kampung`, synced `2026-11-27T19:30:51Z` via `gdrive.py`, `env_source: doppler+dotenv`):
  - `kandang-panggung-ayam-kampung.mp4` (`26,106,217` bytes, MD5 `95e9177ffb72dac8c9ae9280964693e3`, `uploaded`, file `1W6PI8_n6_y750Wsmk88WCxvdBVb8VQtx`)
  - `kandang-panggung-ayam-kampung.srt` (`3,208` bytes, MD5 `6a7519137b7868003acff99852b8cb9e`, `uploaded`, file `1K4v9mH31m8JB__1X_Akawc9T7yeFgWdB`)
  - `thumbnail.png` (`217,649` bytes, MD5 `e0faf712fa876f1b0da685b6f48ea587`, `uploaded`, file `1j7K9fIvhh6NCHhhM9sq7TwGiJug9gBGc`)
  - `CONTENT_PACKAGE.md` (`4,992` bytes, MD5 `83d6f699b8b5a296a202dd835aa7f24f`, `uploaded`, file `18eKn-T6ocVGdzlqw3PVoB4Lc3zJOPJML`)

## External delivery (Trypost queue — completed)

- **Transport:** `api` (`trypost.py`, `Admin's Workspace` `01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37`).
- **Receipt:** [PUBLISHING.json](PUBLISHING.json) (schema v2; export SHA-256 `619b83a146cc9e0092307af715afa15e00a6d4411539c3c672edfae9ddcf3858`; zero credentials or upload tokens stored).
- **Per-channel verified queue results (all observed `status: scheduled`, `schedule_mode: queue` via `GET /posts/{id}`, exact shared caption match, `80.2 s`, not yet live):**
  1. **Instagram `@bikindihalaman.id`** (`01a2022d-bc57-71d8-9217-6e0319cb6c03`, `instagram_reel`): post `01a21e81-474c-718a-9455-34390db2d773`, media `01a21e81-44d5-70df-a2ed-7a610923b898` (`cover_offset_ms: 79950`), scheduled **`2026-11-28 12:31:00` UTC (`2026-11-28 19:31:00 WIB`)**.
  2. **YouTube `@bikindihalaman_id`** (`01a202dc-0e4a-72ae-bec8-589ab7f90045`, `youtube_short`): post `01a21e81-968b-7328-a8d6-07d0730d8dc8`, media `01a21e81-9428-72b3-a5d5-a3d9b48d352c`, `meta.title: "Bikin Kandang Panggung Ayam Kampung di Halaman"`, scheduled **`2026-11-28 12:27:00` UTC (`2026-11-28 19:27:00 WIB`)**.
  3. **Facebook `Bangun Di Halaman`** (`01a2036c-5179-70c6-b908-25118446326d`, `facebook_reel`): post `01a21e81-b205-7167-8f8e-5caf33b10968`, media `01a21e81-b1c1-701e-b763-c8d0102099bc`, scheduled **`2026-11-28 08:20:00` UTC (`2026-11-28 15:20:00 WIB`)**.

## Current state

- `stage`: publishing
- `status`: complete
- `next_action`: optionally upload `exports/thumbnail.png` manually as custom cover in YouTube Studio and Meta Business Suite (`supports_video_cover: false` via Trypost; Instagram already uses `cover_offset_ms: 79950`), then run a performance snapshot 48–72 hours after scheduled go-live on `2026-11-28`.
