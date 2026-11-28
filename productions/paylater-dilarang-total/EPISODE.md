# Cicilan & Paylater Dilarang Total

## Brief and execution

- **slug:** `paylater-dilarang-total`
- **topic:** Twin-world 10-year thought experiment comparing two identical cities where World A bans all consumer installments and paylater (cash-only retail) while World B keeps consumer installments and paylater legal.
- **topic_selection:** `auto` (delegated via `--topic=auto`; initial housing/rent-control pick was caught by user as already published on Trypost `2026-11-27`, verified via live Trypost post audit, and pivoted cleanly before any file creation to verified non-duplicate Candidate #3 *"Cicilan & Paylater Dilarang Total"*).
- **board:** `dua-dunia` (`approved`, revision `editorial v3 / visual v1`)
- **direction:** [DIRECTION.md](../../boards/dua-dunia/DIRECTION.md)
- **editorial:** [EDITORIAL.md](../../boards/dua-dunia/EDITORIAL.md)
- **visual:** [frame.md](../../boards/dua-dunia/frame.md)
- **contract_snapshot:** [CONTRACT.json](CONTRACT.json) (copied from `boards/dua-dunia/CONTRACT.json`, `editorial v3 / visual v1`, SHA-256 `a5e26a4fdac7aa6c3ecc209a9084cfc46b91d4737c8f5e176aded9022b636b73`).
- **purpose:** Vivid, provocative 3D miniature-world simulation testing the widespread gut intuition that banning all paylater and consumer installments immediately frees households from debt — showing the genuine Month 1–3 relief, the Month 9–Year 2 retail/courier slowdown and essential-goods cash wall, the back-alley pawn/informal-lender spillover, and an Archetype B (*Honeymoon → Backfire*) 10-year reversal where World B wins 68/100 model runs unless affordable emergency credit replaces banned paylater.
- **audience:** General Indonesian short-form viewers (young workers, shoppers, small-business owners, couriers, students).
- **format:** `1080x1920`, `30 fps`, hybrid 3D low-poly diorama (topic-specific Polyfork GLB retail/appliance/parcel/living-room/alley props + procedural capsule citizens), Fredoka bold outlined captions in `[54, 1380, 972, 200]`, persistent top-center disclaimer `Eksperimen pikiran. Angka dari model.`.
- **language:** Indonesian (natural spoken conversational storytelling, *aku/kamu* register; zero policy-report prose).
- **duration_target:** `75–115 s` (sweet spot `85–105 s`; `238` spoken words budgeted at `2.4 wps` baseline → `~99.2 s`; re-budget after first measured take).
- **audio:** Narration (`eleven_v4`, board default voice `AfkBqzsATOuueGnLAvJi` — *Samsul — Warm & Clear Narrator*, confirmed Starter tier via `narration.py --check-api`) + lighthearted acoustic-guitar/mallet BGM (`-15.5..-12.5 LUFS`, `<= -0.5 dBTP`); SFX optional/sparse per board contract.
- **outcome_archetype:** **Archetype B — *Enak di awal, bumerang di akhir* (Honeymoon → Backfire)**, intentionally contrasting with `transportasi-umum-gratis` (Archetype A) and `slip-gaji-terbuka` (Archetype C).
- **requested_endpoint:** `publishing` (`--delivery=queue` across all 3 inherited `Dua Dunia Lab` Trypost accounts)
- **delivery:** `queue`
- **execution_policy:** `automation`
- **automation_after:** `none`
- **automation_state:** `active`
- **human_review:** `none`
- **pre_render_authorization:** `delegated by the user's --automation instruction`
- **publishing_transport:** `api` (Trypost REST API via `trypost.py`, workspace `01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37` / `Admin's Workspace`, preflight verified `status: ok`)

## Publishing targets

*Inherited from `boards/dua-dunia/ACCOUNTS.json` under target inheritance; external `--delivery=queue` authorized by the user's invocation.*

```yaml
publishing_targets:
  source: board
  board_accounts_file: boards/dua-dunia/ACCOUNTS.json
  board_accounts_sha256: fbcd4220d560424982f842c33e8fba86e9cb1dd93db03230ba3899285769ce72
  accounts:
    - provider: trypost
      workspace_id: 01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37
      workspace_name: "Admin's Workspace"
      social_account_id: 01a208db-b614-7326-9f1b-e5e9ab8100c1
      service: instagram
      handle: duadunia.lab
    - provider: trypost
      workspace_id: 01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37
      workspace_name: "Admin's Workspace"
      social_account_id: 01a20931-862c-7024-a294-6a715c13a929
      service: youtube
      handle: duadunia_lab
    - provider: trypost
      workspace_id: 01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37
      workspace_name: "Admin's Workspace"
      social_account_id: 01a2093d-8956-701b-9933-7f2e6776b752
      service: facebook
      handle: "Dua Dunia Lab"
```

## Topic discovery shortlist & overlap check (`--topic=auto`)

- **Overlap audit (`TRACKER.json`, `productions/`, and live Trypost `Dua Dunia Lab` posts):**
  - Already published on `Dua Dunia Lab`: (1) Bungkus rokok polos (`2026-11-24`), (2) Transportasi umum gratis (`2026-11-25`, Archetype A), (3) Slip gaji dibuka publik (`2026-11-26`, Archetype C), (4) Harga sewa rumah & kos dikunci (`2026-11-27`).
  - Zero overlap across all other boards (`di-balik-benda`, `ruang-di-antara`, `budidaya-di-halaman`) or remaining folders.
- **10-topic lightweight editorial shortlist (evaluated against `EDITORIAL.md` 4-check litmus test):**
  1. **Cicilan & Paylater Dilarang Total** *(Money / Lifestyle — **SELECTED**)*: World A bans all consumer installments & paylater; tests whether debt-free calm lasts or triggers retail collapse and back-alley informal lending (Archetype B).
  2. **UMR Naik 2x Lipat Besok Pagi** *(Public / Economic)*: World A doubles minimum wage overnight; tests purchasing-power boom vs. UMKM price hikes, shift cuts, and informalization.
  3. **Beli Mobil Baru Wajib Punya Garasi Pribadi** *(Urban / Lifestyle)*: World A mandates verified private garage proof for new car purchases; tests clear alleys vs. parking-rent spikes and paper loopholes.
  4. **Sekolah Tanpa PR dan Tanpa Ujian** *(Public / Everyday)*: World A removes all homework and exams; tests lower student stress vs. hidden inequality via private tutoring (`bimbel`).
  5. **Medsos Mati Total Tiap Jam 9 Malam** *(Social / Lifestyle)*: World A shuts down social media nightly 21:00–06:00; tests better sleep vs. nighttime UMKM/creator revenue drops and daytime doomscrolling.
  6. **Kerja 4 Hari Seminggu (Gaji Tetap 100%)** *(Public / Work)*: World A cuts the workweek to 4 days at full pay; tests office productivity vs. shift-cost spikes in hospitals/restaurants/factories.
  7. **Subsidi BBM Dihapus Total Besok Pagi** *(Public / Economic)*: World A removes all fuel subsidies immediately; tests initial logistics/food shock vs. long-term efficiency if funds are reinvested.
  8. **Setiap Produk Wajib Cantumkan Biaya Produksi & Margin** *(Money / Retail)*: World A mandates cost-and-margin stickers on every product; tests fair pricing vs. small-shop squeeze from invisible rent/overhead.
  9. **Rumah Kosong Kena Pajak 10x Lipat** *(Public / Housing)*: World A taxes vacant homes 10×; tests instant rental release vs. sham leases and lower new builds *(deprioritized due to proximity to 2026-11-27 rent-freeze episode)*.
  10. **Semua Parkir Pinggir Jalan Dilarang Total** *(Urban / Transit)*: World A bans all curbside street parking; tests faster traffic vs. small street-side warung revenue drop *(deprioritized due to proximity to 2026-11-25 transit episode)*.
- **Selection rationale:** Candidate #1 (*Cicilan & Paylater Dilarang Total*) offers immediate visceral Indonesian relatability, 100% distinct 3D settings (electronics/appliance store, living room, parcel depot, checkout cutaway, back-alley pawnshop) from all 4 published episodes, rock-solid peer-reviewed empirical evidence (Di Maggio et al. 2022, Bian et al. 2023/2024, CFPB 2023/2025, Zinman 2010, Bhutta et al. 2016), and a crisp Archetype B (*Honeymoon → Backfire*) reversal.

## Research status

- **Status:** Complete ([SOURCES.md](SOURCES.md)).
- **Key resolved findings:**
  1. **Impulsive spending & retail demand (Di Maggio et al. 2022 NBER w30508; Bian et al. 2023/2024 NBER w31202/w33178):** BNPL creates a strong "liquidity flypaper effect" raising retail spending and merchant sales while expanding access to liquidity-constrained buyers — so banning it cuts impulsive spending immediately *and* contracts retail/courier volume.
  2. **Debt-stacking pain in World B (CFPB 2023/2025):** ~63% of BNPL users hold multiple simultaneous loans (~33% across multiple lenders) alongside higher traditional credit stress, grounding World A's real Month 1–3 honeymoon relief.
  3. **Informal/worse credit spillover under bans (Zinman 2010 JBF; Bhutta, Goldin, & Homonoff 2016 JLE):** Restricting or banning formal short-term credit does not eliminate cash shocks; liquidity-constrained households migrate to worse substitutes (pawnshops, late bills, informal high-cost lending).

## Hook options (delegated under `--automation`)

*No board performance analysis exists yet. All 3 hooks satisfy `dua-dunia` `editorial v3` (`EDITORIAL.md#hook-craft`, `sharp-premise-hook`, Sentence 1 `<= 4.5 s`, Frame 0 motion `<= 0.5 s`, zero format announcement).*

1. **Option 1 (Selected under `--automation`) — Counter-intuitive gut punch:**
   - **Spoken line (`11` words; Sentence 1 = `5` words `~2.08 s` at `2.4 wps`):** `"Cicilan dan paylater dilarang besok. Awalnya tenang, tahun kedua toko tutup."`
   - **Frame 0:** Eye-level 3D commercial street outside `TOKO ELEKTRONIK`; bold `TUNAI SAJA` banner flips down (`t = 0.0–0.5 s`) while nearby small shop rolls down a `TUTUP` shutter as shoppers pause.
   - **On-screen line:** Headline `PAYLATER DILARANG TOTAL?` + persistent disclaimer `Eksperimen pikiran. Angka dari model.` + lower-band captions.
   - **Reason selected:** Sharpest mid-scroll cognitive collision ("why would banning paylater shut shops?"), names both *cicilan* and *paylater* in breath one (`~2.1 s`), and promises the exact Archetype B reversal paid off by the 3D checkout-wall cutaway.
2. **Option 2 — Provocative daily-life "what if":**
   - **Spoken line (`10` words, `~4.17 s`):** `"Kalau besok semua cicilan dan paylater dilarang, dompet langsung aman?"`
   - **Frame 0:** Shopping strip outside gadget shop & parcel bay as `NO PAYLATER` stamp drops over checkout (`t = 0.0–0.5 s`).
   - **On-screen line:** Headline `TANPA PAYLATER = DOMPET AMAN?` + disclaimer + captions.
3. **Option 3 — Stakes-first scene drop:**
   - **Spoken line (`10` words; Sentence 1 = `5` words `~2.08 s`):** `"Bayangin besok paylater dihapus total. Beli kulkas wajib tunai penuh."`
   - **Frame 0:** Appliance/gadget store interior as `RP 4 JT TUNAI` tag pops above a fridge/phone display (`t = 0.0–0.5 s`) and a worker checks a thin wallet.
   - **On-screen line:** Headline `SEMUA BELANJA WAJIB TUNAI` + disclaimer + captions.

- **Selection provenance:** `agent` choice under delegated authorization (`--automation`; not human-approved).

## Script check (v1 — agent-verified under `--automation`)

- **Script artifact:** [SCRIPT.md](SCRIPT.md) (`v1`, `19` scenes across all 6 `dua-dunia` `editorial v3` causal phases; Archetype B reversal).
- **Word budget:** `238` spoken words (`CONTRACT.json` range: `180–290`). `episode_qa.py --budget` reported no prior measured production for board voice `AfkBqzsATOuueGnLAvJi`, so planned at `2.4 wps` baseline (`script-craft.md`) → predicted speech `99.17 s` (range `88.1–113.3 s` across `2.1–2.7 wps`), safely inside `75–115 s` (`85–105 s` sweet spot). Will re-budget immediately after measured narration take.
- **First sentence timing:** `"Cicilan dan paylater dilarang besok."` — `5` words → `2.08 s` predicted at `2.4 wps` (`<= 4.5 s` contract limit).
- **Cold-read check:** **Pass.** Read all 238 spoken words standalone without headings, visuals, or metadata:
  - Repairs made before locking v1: (1) added explicit `"toko Dunia A sepi"` anchor in S08 after S07's `Dunia B` beat so the world switch is crystal clear to the ear; (2) changed `"Cicilan resmi tutup"` → `"Begitu cicilan resmi hilang, banyak warga lari ke gadai dan pinjaman gelap"` in S11 for smooth spoken flow; (3) changed `"potongan kecil"` → `"potongan ringan"` in S13; (4) clarified S17 flip trigger to `"Dunia A cuma unggul kalau ada kredit darurat"`; (5) spelled all numbers in Indonesian words (`tiga`, `empat`, `sepuluh`, `seratus`, `enam puluh delapan`).
  - Every pronoun, world (`Dunia A`/`Dunia B`), and cause-effect turn resolves strictly from speech.
- **Script-relevant contract judged rules (`CONTRACT.json`, `editorial v3 / visual v1`):**
  - `hook-frame`: **pass** — S01 Frame 0 opens on active 3D commercial storefront with `TUNAI SAJA` banner dropping (`0.0–0.5 s`), neighboring shutter lowering, and phone-legible headline `PAYLATER DILARANG TOTAL?`.
  - `ear-test`: **pass** — standalone cold-read resolves every actor, world, and causal link without on-screen copy.
  - `epistemic-disclaimer`: **pass** — persistent `Eksperimen pikiran. Angka dari model.` across all 19 scenes; simulation figures framed explicitly as model outcomes (`Di model sepuluh tahun ini`, `Dari seratus percobaan`).
  - `provocative-relatable-topic`: **pass** — tests one crisp daily-money rule (total ban on consumer installments & paylater) directly hitting shopping, bills, small shops, and emergency cash flow; 100% distinct from all 4 prior episodes and the corruption reference.
  - `sharp-premise-hook`: **pass** — S01 drops straight into a 5-word first sentence (`~2.08 s <= 4.5 s`) and counter-intuitive 11-word punch with zero format announcement.
  - `controlled-twin-worlds`: **pass** — S02 establishes a concise 50/50 horizontal split baseline (`Awal persis sama`) before S03–S04 isolate the single installment rule.
  - `causal-twist-and-outcome`: **pass** — delivers Archetype B (*Honeymoon → Backfire*): Month 1–3 debt relief (S05–S07) reverses into Month 9 retail slowdown, Year 2 cash wall, back-alley informal lending (S08–S11), and Year 3 reversal (`Berbalik!`) with Dunia B winning `68/100`.
  - `physical-mechanism`: **pass** — S12–S14 present a dual 3D retail-checkout cutaway contrasting Dunia B's stepped price-slice ramp & rolling parcel conveyor against Dunia A's solid `TEMBOK TUNAI` blocking both impulsive buyers and urgent workers toward a glowing `PINJAMAN GELAP` side-alley detour.
  - `spoken-storytelling-voice`: **pass** — crisp conversational Indonesian alternating short punches (`Padahal belum.`, `Roda toko berputar.`) with concrete everyday moments; zero policy-report prose.
  - `data-proof-cards`: **pass** — S15 dark-navy 10-year reversal line chart (`Berbalik!` at Year 3) + S17 dark-navy randomized 10×10 Monte Carlo robustness grid (`68 / 100 DUNIA B MENANG`).
  - `soft-closing-cta`: **pass** — S19 ends with `"Dari dua dunia ini, kamu pilih hidup di Dunia A, atau tetap di Dunia B?"` (consecutive `dua dunia`, zero follow/subscribe/like prompts).

## Visual storyboard (complete — `passed`)

- **HyperFrames workspace:** `productions/paylater-dilarang-total/video/` (initialized via `--skip-skills --non-interactive --skill=hyperframes`).
- **3D asset library:** 21 topic-specific Polyfork CC BY 4.0 GLB models (`2.41 MB`) + 6 board starter GLB models (`27` GLBs total in `video/assets/models/`).
- **Artifacts:** [BRIEF.md](video/BRIEF.md), [STORYBOARD.md](video/STORYBOARD.md) (`storyboard_lint.py --strict`: `passed`, 0 errors / 0 warnings, `status: animated`), [storyboard.html](video/boards/storyboard.html) (`60/60` stills & poses loaded), [storyboard.png](video/boards/storyboard.png) (visually inspected).
- **Quality gate (`--stage storyboard`):** `passed` (`disclose: []`).

## Audio & sound design (complete — natively auditioned)

- **Narration:** Single-take `eleven_v4` synthesis via `narration.py` (`elevenlabs_api`, Starter tier, official board voice `AfkBqzsATOuueGnLAvJi` — *Samsul — Warm & Clear Narrator*) → `video/.media/audio/voice/narration-56226411bf3c96fbbcbb.mp3` (`88.56 s`, `238` words, Sentence 1 ends at `2.24 s <= 4.5 s`). Natively auditioned (`listening: agent`).
- **BGM & Master Mix:** Deterministic F-major `112 BPM` acoustic-guitar + wooden-mallet BGM (`video/audio/bgm-acoustic-mallet.wav`) with dramatic silence drop on *"Padahal belum."* (`33.5–34.8 s`), sparser half-time D-minor tension shift across `s08–s11`, audible accents on `s13`/`s14`/`s15`, and warm F-major cadence at `89.20 s`. Mixed via 2-pass EBU R128 loudnorm into `video/audio/master-mix.wav` (`89.20 s`, `2,676` frames @ 30 fps, `-14.26 LUFS`, `-1.50 dBTP`), synced into [timing.json](video/timing.json) (`words` + 80 safe-margin caption clauses) and [sound_design.json](video/sound_design.json).

## Production & independent verification (v2 — `passed`)

- **Independent review v1 (`research` subagent `8ba1dbcf-5642-4b6e-82e6-eb49ca27b8f5`):** `FAIL` (2 P0s: `s12` cutaway too small, `s04`/`s14` long caption margins; 6 P1s).
- **v2 polish:** Rebuilt `s12` as full-bleed 50/50 vertical cutaway split; capped captions to `900px` centered width (`<= 24` chars); dressed living-room & checkout interiors + glowing laptop; added dynamic BGM pause + D-minor tension shift; upgraded `s09`/`s16`/`s18`/`s19`, dark-navy `.top-banner` pills, and `data-board-chrome` on disclaimer.
- **Technical gates:** `dom_lint.py` `passed` (`g5_fails: 0`, `readcheck_fails: 0`, `composition_sha256: 1c5a367875bddf1d77993c75c215b381f66aae1233e652e60f6b48b345d1c9aa`); seek determinism `deterministic: true`, `errors: []` ([seek-determinism.json](video/verification/seek-determinism.json)); native audio audition of decoded proof MP3 passed.
- **Independent jury review v2 ([REVIEW.md](video/REVIEW.md)):** **`PASS`** (`19/19` judged rules `[pass]`, `0` open P0/P1, 7-dimension mean **`8.17/10`**: `style_fidelity 8.4`, `concept_wow 8.3`, `motion_craft 7.8`, `design_typography 8.1`, `finish_texture 7.9`, `sound_sync 8.2`, `technical 8.5`; `weakest_shot`: `s09` mid-pan plaque crop at `40.60 s`).
- **Quality gate (`--stage verification --dom-lint`):** `passed` (`disclose: []`) — [quality-gate-verification.json](video/verification/quality-gate-verification.json).

## Final delivery export & content package (complete — `passed`)

- **Delivered film:** [exports/paylater-dilarang-total.mp4](exports/paylater-dilarang-total.mp4) (`57,616,251 bytes` / `54.9 MB`, SHA-256 `b94ce6239eeee690b3b645a4e8d7741d85145523e4ca3725e132462789065099`, `1080×1920`, `30 fps`, `2,676` frames, `89.20 s`, H.264 High `yuv420p` + AAC LC 48 kHz stereo 192 kbps).
- **Thumbnail:** [exports/thumbnail.png](exports/thumbnail.png) (`t = 3.38 s`, `537,117 bytes`, visually verified).
- **Quality gate (`--stage export`):** `passed` (`disclose: []`, `21/21` checks passed: `-14.30 LUFS`, `-1.39 dBTP`, `hook-first-sentence: 2.24 s`, `hook-motion: 0.2 s`, `longest_static_seconds: 0.0 s`, `empty-frames: 0`, `end-hold: 0.0 s`) — [quality-gate-export.json](video/verification/quality-gate-export.json).
- **Content package:** [CONTENT_PACKAGE.md](CONTENT_PACKAGE.md) (shared Indonesian caption within IG `2,200`-char / `5`-hashtag limit, title + alternatives, cover offset `3380 ms`).

## Google Drive archive (synced)

- **Status:** `ok` (`env_source: doppler`, `synced_at: 2026-11-28T02:18:37Z`)
- **Remote path:** `dua-dunia/paylater-dilarang-total`
- **Folder ID / URL:** `18E61kuEY-RjuJUnlhEoktUHCxldHY_Xt` · [Google Drive folder](https://drive.google.com/drive/folders/18E61kuEY-RjuJUnlhEoktUHCxldHY_Xt)
- **Archived deliverables (`uploaded: 3`):**
  - `paylater-dilarang-total.mp4` (`57,616,251` bytes, MD5 `bf2f385e28836476b8523db3747c4fd8`, file ID `1bgURnf8YNw4Gt1Tootv61LRicyj2s-FO`)
  - `thumbnail.png` (`537,117` bytes, MD5 `0e876ba59d3c52e77fcd1ef5d93e4112`, file ID `1WindrzoAGs5P5W8RPs0x4-QWIoicGa4J`)
  - `CONTENT_PACKAGE.md` (`6,079` bytes, MD5 `127e40426da1300722e7b0f30e71b0f1`, file ID `1tRV3lei9YlocU9w475p8QcaDr8ZsKMgP`)

## External delivery — Trypost queue (`publishing` complete)

- **Transport:** Trypost REST API (`trypost.py`, `api`, workspace `01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37` / `Admin's Workspace`).
- **Receipt:** [PUBLISHING.json](PUBLISHING.json) (`schema_version: 2`, all 3 channels verified via authoritative `GET /posts/{id}` readback).
- **Per-channel verified status (scheduled into each account's next free `Asia/Jakarta` queue slot):**

| Channel | Handle / Account | Content Type | Trypost Post ID | Media ID | Observed Status | Scheduled At (UTC / WIB) | Settings Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Instagram | `@duadunia.lab` (`01a208db-b614-7326-9f1b-e5e9ab8100c1`) | `instagram_reel` | `01a21ff6-5306-7214-8a70-8fd5b8e7b9fb` | `01a21ff6-50a5-70d5-b354-804dfa76f371` | `scheduled` | `2026-11-28 12:44:00` UTC (`19:44 WIB`) | `cover_offset_ms: 3380`, `57,616,251` bytes, `89.2 s` |
| YouTube | `@duadunia_lab` (`01a20931-862c-7024-a294-6a715c13a929`) | `youtube_short` | `01a21ff6-adbb-733c-be31-9b1739c12706` | `01a21ff6-a9e6-737b-bcba-c8a55ea11622` | `scheduled` | `2026-11-28 10:39:00` UTC (`17:39 WIB`) | `meta.title` set, `57,616,251` bytes, `89.2 s` |
| Facebook | `Dua Dunia Lab` (`01a2093d-8956-701b-9933-7f2e6776b752`) | `facebook_reel` | `01a21ff7-12e5-7084-99a3-3b7bd74f030c` | `01a21ff7-109a-72c1-be15-6b764994a50b` | `scheduled` | `2026-11-28 06:05:00` UTC (`13:05 WIB`) | `57,616,251` bytes, `89.2 s <= 90 s` |

## Review & next action

- **Current stage:** `publishing`
- **Status:** `complete` (requested endpoint `--delivery=queue` satisfied across all 3 `Dua Dunia Lab` channels; all posts are `scheduled` for future slots, not yet live).
- **Next action:**
  1. *(Optional)* Upload or select custom cover frame [exports/thumbnail.png](exports/thumbnail.png) (`t = 3.38 s`) manually in YouTube Studio (`@duadunia_lab`) and Meta Business Suite (`Dua Dunia Lab` FB) since Trypost `supports_video_cover` is `false` for `youtube_short` and `facebook_reel` (Instagram Reels already has `cover_offset_ms: 3380`).
  2. After the three posts publish on `2026-11-28`, run a post-publication performance review snapshot (`performance.md#use-it`) once 24–72 hours of views/retention accumulate.
