# Kolam Ikan Gurame di Halaman

## Brief

- **Slug:** `kolam-gurame-di-halaman`
- **Topic selection:** `topic_selection: user`. On 2026-11-27, after reviewing a 10-topic Indonesia-familiar shortlist under `--board=budidaya-di-halaman --automation=after-topic --delivery=queue`, the user replied `"setuju"`, accepting recommended Candidate #1: building a backyard giant gourami (*Osphronemus goramy*) circular wiremesh tarp pond from a bare yard corner through problem–improvement rounds to a stable pond and first weighed harvest.
- **Board:** `budidaya-di-halaman`, revision 10 (`editorial v9 / visual v5`, status `approved`), explicitly selected via `--board=budidaya-di-halaman`. Inherit its [direction](../../boards/budidaya-di-halaman/DIRECTION.md), [editorial framework v9](../../boards/budidaya-di-halaman/EDITORIAL.md), [visual specification v5](../../boards/budidaya-di-halaman/frame.md), [organic SFX kit](../../boards/budidaya-di-halaman/assets/sfx/manifest.json), and [production contract](CONTRACT.json).
- **Contract snapshot:** [CONTRACT.json](CONTRACT.json) copied verbatim from `boards/budidaya-di-halaman/CONTRACT.json` (`editorial v9 / visual v5`, SHA-256 `28cb1f61279ad4254be43cabebf6967412d9e3f964e0eb4d4e3af48127c24e77`), validated via `episode_qa.py --contract`.
- **Overlap check:** Checked `TRACKER.json` and `productions/`. Existing `budidaya-di-halaman` episodes cover backyard aquaponics (`akuaponik-lele-dan-kangkung`, `aquaponik-pasang-surut`), Nile tilapia settling chamber (`jejak-kotoran-kolam-nila`), BSF maggot exit ramp (`maggot-jalan-ke-wadah`), leaf-lettuce wick planter (`pot-sumbu-selada`), container potatoes (`kentang-dalam-pot`), redclaw crayfish lined pond (`kolam-lobster-air-tawar`), standalone catfish rectangular wood-stake tarp pond (`kolam-lele-di-halaman`), dry-litter laying duck coop (`kandang-bebek-petelur-kering`), horizontal 200 L drum swamp eel pond (`kolam-belut-dalam-drum`), and betta breeding/grow-out/soliter rack (`ternak-ikan-cupang`). None covers giant gourami (*Osphronemus goramy* / *ikan gurame*), circular wiremesh pond assembly, leaf-feeding frames, or gourami fungal/temperature/calm-water rounds.
- **Candidate comparison:** Candidate #1 was recommended over 9 distinct Indonesia-familiar alternatives (quail cage, planter-bag bird's eye chili, backyard free-range chicken coop, shaded oyster-mushroom rack, snakehead tarp pond, cricket box, sack/bag shallot bed, patin tarp pond, and stingless *Trigona* bee box) because backyard aquaculture anchors `budidaya-di-halaman`, gourami is a flagship Indonesian family consumption fish with high market value, and its circular wiremesh silhouette + leaf-eating behavior + rain/fungus sensitivity deliver a genuinely distinct 7-round build arc under Editorial v9 and Visual v5. *(No board performance analysis `insights/*/ANALYSIS.md` exists yet.)*
- **Provisional angle & research questions (awaiting verified source research):**
  - Start at a bare yard corner with a rolled wiremesh ring, tarp liner, water, and juvenile *Osphronemus goramy* (*bibit gurame*), then evolve the exact same circular pond through ~7 compact single-cause rounds (6–10 s each at 1x, varied natural Indonesian transitions; `"Tapi"` reserved for the opening hook turn) covering provisional hypotheses to verify in `SOURCES.md`:
    1. Tarp/liner or unaged water/shock issue or rapid initial build vulnerability (e.g., sharp wiremesh edge / unbuffered sun or clear water stress)
    2. Floating leaf feed (*daun talas/kangkung*) scattering & rotting at edges → floating PVC/bamboo feeding ring (*bingkai pakan daun*) + clearing leftovers
    3. Midday heat / harsh light or sudden cold rain temperature drop triggering fungal stress (*jamur putih*) → shade net (*paranet*) / partial rain shelter & water buffering
    4. Heavy rain raising water to the rim → screened overflow pipe (*pipa pelimpah berkasa*)
    5. Stagnant low-oxygen water / gentle circulation needs for gurame (calm aeration without turbulent current) → fine-bubble air stone / shaded corner + partial drain flush
    6. Yard predators (cats, herons/birds) → overhead net cover
    7. Size disparity / territorial nipping or density management as gourami grow → sorting / split or thinning harvest check
  - Follow with a stable-system check, a weighed first-harvest monetization scene beside the completed pond (verified household circular-pond yield × dated Indonesian market/collector price in `SOURCES.md`, labelled `estimasi`), and closing wide view + congratulation + consecutive `"bikin di halaman"` question + `@bikindihalaman.id` + `0.5 s` delivered (`0.625 s` at 1x) thumbnail end card.
- **Format & audio defaults (inherited from board):** Vertical 9:16 (`1080 × 1920`), authored at **90–112.5 s at 1x** (24 fps master restamped to 30 fps at **1.25x** = **72–90 s delivered**, pitch kept). Language: casual second-person Indonesian (`"kamu"` referring singly to the backyard keeper). Board default voice: ElevenLabs **Pribs – Friendly Casual Narration** (`5g0yKK2JwTRka0IG61Hh` from `boards/budidaya-di-halaman/AUDIO.json`, `eleven_v4`), BGM `none`, SFX `use` (board Visual v5 organic SFX library + documented hybrid additions).

## Execution, review & delivery policy

```text
execution_policy: automation
automation_after: topic
automation_state: active
activating_decision: user acceptance ("setuju") of Candidate #1 from 10-topic Indonesia-familiar shortlist (2026-11-27)
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

## Preflight & active blockers (2026-11-27)

1. **Trypost preflight (`api`):** Passed (`Admin's Workspace`, all 3 inherited accounts `connected` with active schedules).
2. **Web research (resolved 2026-11-27):** User authorized built-in `search_web` and updated global `C:\Users\muhth\.gemini\AGENTS.md` to remove the SearXNG MCP dependency. Deep research completed and verified against primary Indonesian government, academic, and market-price pages in [SOURCES.md](SOURCES.md) (claims C1–C8, including FishInfo Jatim 27 Nov 2026 **Rp45.250/kg**).
3. **Audio preflight & remaining quota blocker:** User replied `"2. confirm"` for fallback voice **Roger** (`CwhRBWXzGAHq8TQ4Fs17`, `eleven_v4`) on free tier. However, character quota checks still show `8,720 / 10,000` used (**`1,280` chars remaining**) on `ELEVENLABS_API_KEY` / CLI and `39,745 / 40,000` used (**`255` chars remaining**) on ElevenLabs MCP, whereas a full 240-word `budidaya-di-halaman` narration is ~1,600–1,800 characters. Storyboard work proceeds first under active automation; audio synthesis waits for quota replenishment or a fresh key.

## Research and hook selection (agent-selected under active automation)

Research verified circular wiremesh tarp pond setup and liner wall protection (`karpet talang`), *Osphronemus goramy* temperature (`24–30 °C`), cool-rain *Saprolegnia* white fungus prevention (`atap plastik bening` + `paranet`), wilting and floating-ring feeding of *daun talas*, screened overflow (`pipa pelimpah berkasa`), calm-water central bottom drain & fine-bubble aeration, predator top mesh (`jaring penutup`), periodic size grading, conservative 2 m circular pond yield (`~40 kg` from ~100 fingerlings at 450–500 g), and dated Indonesian pricing (FishInfo Jatim 27 Nov 2026: **Rp45.250/kg**; DKP Bantul 2026: **Rp43.000/kg**). Mapped in [SOURCES.md](SOURCES.md).

Hook options v1 follow Editorial v9's four-slot pattern (`Kalo kamu {aksi pertama}, {konjungsi temporal} kamu {aksi kedua}, kamu sudah punya {sistem}. Tapi {masalah}.`), avoid repeating the previous episode's (`ternak-ikan-cupang`) opening verb (`taruh`) and connector (`terus`), vary mechanism and opening problem, and stay within the contract's `10.0 s` first-sentence and `12.0 s` `"Tapi"` ceilings *(no board performance analysis exists yet)*:

1. **Option 1 (Selected — agent choice under active automation) — Weather/biological surprise (`jamur putih` after rain):**
   - *Mechanism:* Counter-intuitive environmental vulnerability — viewers assume an outdoor circular pond is safe once filled, so sudden white fungus after rain sparks immediate curiosity about temperature/pH buffering.
   - *First verb / connector:* `lingkarkan` / `lalu`
   - *Spoken line (26 words; Sentence 1 = 18 words ≈ 7.5 s ≤ 10.0 s; `"Tapi"` at word 19 ≈ 7.9 s ≤ 12.0 s):*
     > “Kalo kamu lingkarkan besi wiremesh di halaman, lalu kamu lapis terpal dan tebar bibit gurame, kamu sudah punya kolam gurame. Tapi baru beberapa hari kehujanan, sirip ikannya berjamur putih.”
   - *Frame 0 & `<1 s` motion:* Bare warm-clay yard corner with rolled wiremesh and folded teal tarp; within `0.25 s`, hands roll the wiremesh into a ring, drape the tarp, fill water and release juvenile gurame, then cool rain arrives and white cottony patches appear on fins.
   - *On-screen line:* 46 px DM Sans 800 progressive captions matching the opening line; thumbnail/cover promise **Kolam gurame / di sudut halaman** (yellow on **gurame**).
   - *Promise:* Explains why unbuffered tarp ponds lose thermal stability in rain and builds through 7 visible circular-pond upgrades to a stable system and weighed first harvest.
2. **Option 2 — Structural puncture surprise (wiremesh weld tear):**
   - *Mechanism:* Immediate physical failure — water pressure pushes the new tarp against bare wiremesh weld ends, dropping the waterline overnight (`“Kalo kamu tegakkan rangka wiremesh di sudut rumah, setelah itu kamu pasang terpal dan isi air, kamu sudah punya kolam gurame. Tapi besok paginya airnya surut sejengkal.”`).
3. **Option 3 — Dietary/water fouling surprise (fresh taro-leaf sap):**
   - *Mechanism:* Feeding trap — tossing raw *daun talas* straight in clouds and foams the water (`“Kalo kamu bentangkan rangka bundar di halaman, begitu kamu isi air dan lepas gurame, kamu sudah punya kolam gurame. Tapi dikasih daun talas, airnya malah keruh.”`).

**Selection rationale:** Option 1 leads with a distinctly *gurame* biological hazard (`jamur putih` from cool rain on an unbuffered tarp pond) rather than repeating a leak hook, uses a fresh verb/connector (`lingkarkan` / `lalu`), and sets up all 7 chronological upgrades cleanly on the same circular wiremesh pond.

## Script check (v1 — agent-verified under active automation)

- **Spoken word count & budget (`episode_qa.py --budget 236`):** **236 spoken words** (`1,553` chars without tags; ~`1,650` tagged chars); Roger measured pace `2.39 wps` (`words_for_range: [202, 252]`); predicted raw narration `98.7 s`, predicted 1x film `105.4 s` (fits `90.0–112.5 s` 1x; `~84.3 s` delivered at 1.25x). Reconcile after synthesis.
- **First sentence & `"Tapi"` turn:** Sentence 1 = **19 words** (predicted `7.9 s ≤ 10.0 s`); `"Tapi"` at word 20 (predicted `8.4 s ≤ 12.0 s`).
- **Selected hook three parts:** Option 1 spoken line, Frame 0 bare corner + `<0.25 s` wiremesh roll action, and 46 px progressive captions recorded above and in [SCRIPT.md](SCRIPT.md).
- **Cold-read result & repairs:** Read all 235 words standalone without headings or visual cues. `"kamu"` resolves consistently to the single backyard keeper; tightened pacing across Scenes 1–11 so total spoken count (`235`) fits comfortably inside `words_for_range [202, 252]`.
- **Contract judged rules (script scope):**
  - `hook-frame`: **pass** — Frame 0 shows bare corner + wiremesh roll at `0.25 s` with 46 px captions.
  - `pictures-alone`: **pass** — Every scene specifies sequential visual sub-beats showing cause, added part, and tested outcome.
  - `event-density`: **pass** — 11 scenes / 18 events each add a distinct construction change, check, or result.
  - `motion-variety`: **pass** — Planned shots alternate `wide` → `medium` → `close cutaway` → `medium` → `medium-wide` → `close cutaway` → `medium` → `close cutaway` → `wide` → `medium` → `wide` (max consecutive same shot = 1).
  - `subject-scale` & `vessel-scale`: **pass** — Circular wiremesh pond and hanging scale planned at `>=40%` frame width with constant yard landmarks.
  - `ear-test`: **pass** — Cold read passed after Round 7 clarity repair; single `"kamu"` POV throughout.
  - `build-first`: **pass** — Hook fills all four Editorial v9 slots with ordinary punctuation, bare starting point, active premature pond, and observable white fungus within timing ceilings.
  - `shortfall-before-fix`: **pass** — 7 single-cause rounds (20–24 words / `8.4–10.0 s` each at 1x), each tested on screen, distinct triggers (`hujan dingin/jamur`, `tepi wiremesh`, `getah/sisa daun talas`, `luapan hujan`, `endapan dasar & oksigen tenang`, `predator`, `persaingan ukuran`), `"Tapi"` used only in Scene 1.
  - `same-system`: **pass** — Every added upgrade remains visible on the same circular wiremesh pond through Scene 11.
  - `final-job`: **pass** — Scene 9 shows the completed pond handling rain and heat with calm bubbles and feeding before calling it stable.
  - `income-scene`: **pass** — Scene 10 weighs `40 kg` beside the finished pond (`40 kg × Rp45.000 ≈ Rp1.800.000`, `estimasi harga pasar / Nov 2026` from FishInfo Jatim 27 Nov 2026), rounded spoken figures, `>=3 s` 1x hold, no profit promise.
  - `event-map`: **pass** — 18 events (`15–19`), every component enters on screen.
  - `closing-lines`: **pass** — Ends with congratulation naming the built pond + next-build question containing consecutive `"bikin di halaman"`, zero intro or follow CTA.
  - `closing-signature`: **pass** — Holds yellow on `"bikin di halaman"`, fades in `@bikindihalaman.id`, hard cuts to `0.625 s` 1x (`0.5 s` delivered) thumbnail end card.
  - `reframing`: **pass** — Beat-level push-ins, lateral pans, and wide pull-outs planned across all 11 scenes.

## Storyboard verification (agent-verified under active automation)

- **Plan:** [video/STORYBOARD.md](video/STORYBOARD.md) — 11 frames (`107.10 s` planned 1x), 18 events, shot variety max run 1 (`wide` / `medium` / `close cutaway` alternating), `storyboard_lint.py --strict` passed (0 errors, 0 warnings).
- **Styled stills & poses:**
  - [video/boards/stills/](video/boards/stills/) — 11 styled `1080 × 1920` stills (`frame-00-at-8.5s.png` .. `frame-10-at-105.6s.png`), visually inspected; repaired `gourami-world.js` color mixing and `s10` price-tag framing/chip single-line wrap (`≈ Rp1.800.000`).
  - [video/boards/poses/](video/boards/poses/) — 25 progression poses (`hook-0.0s.png`, `hook-0.8s.png`, `hook-3.0s.png`, plus `01-a-start.png`..`11-b-end.png`).
  - [video/boards/storyboard.html](video/boards/storyboard.html) & [video/boards/storyboard.png](video/boards/storyboard.png) (`1600 × 7449` px, 36/36 images loaded, `DM Sans` loaded, 0 broken images). Inspected saved PNG directly.
- **Gate verdict:** `episode_qa.py --stage storyboard` **passed** (`video/verification/quality-gate-storyboard.json`, `disclose: []`).

## Current state

- `stage`: publishing
- `status`: complete
- `next_action`: optionally upload `exports/thumbnail.png` manually as the Shorts/Reel cover in YouTube Studio and Meta Business Suite (`supports_video_cover: false` via Trypost; Instagram already uses `cover_offset_ms: 84350`), then review performance in 48–72 hours after scheduled publications go live on `2026-11-28`.

## Delivery summary & verification record (2026-11-27)

- **Audio (`eleven_v4` + quiet boundaries + 41 SFX):** User authorized voice override to premade voice **Roger** (`CwhRBWXzGAHq8TQ4Fs17`) and updated `.env` `ELEVENLABS_API_KEY`. Generated single 236-word continuous take via `narration.py --auto-align` (`100.56 s`), placed clean pauses via `audio_boundaries.py` (`10/10` boundaries passed), applied 41 frame-locked organic SFX cues from the board Visual v5 library (`bgm: none`) via `sound_design.py`, natively listened (`listening: agent`), and passed `sound_design.py --export` (`27.12 dB` median vocal-band SNR, `0.0 s` severe masking, `<= 0.5 ms` offset).
- **Verification & independent audit:** Rendered `video/verification/proof.mp4` (`1080x1920`, `24 fps`, `105.750 s`) and passed Pass 2 fresh-context subagent review (`21ad1006-a1b3-4c10-a757-83c9cbf6c1aa`: **`APPROVE FOR DELIVERY RENDER`**, `18/18` judged rules passing, `0` P0/P1, rubric `8.5–9.3/10`, recorded in [`video/REVIEW.md`](video/REVIEW.md)). Passed `episode_qa.py --stage verification --dom-lint` (`disclose: []`).
- **Export (`1.25x` pitch-kept, 30 fps):** Rendered 24 fps delivery master (`video/verification/master-24fps.mp4`) and retimed to [`exports/kolam-gurame-di-halaman.mp4`](exports/kolam-gurame-di-halaman.mp4) (`28,704,162` bytes, SHA-256 `1a1f1c3b7364dca876c8569098935cec63d289c46dcec8e09a2507caeddfc49e`, `84.602 s`, `1080x1920`, `30.0 fps`, `-14.04 LUFS`, `-2.42 dBTP`), plus [`exports/thumbnail.png`](exports/thumbnail.png) (`477,217` bytes) and [`exports/kolam-gurame-di-halaman.srt`](exports/kolam-gurame-di-halaman.srt) (`51` cues, `3,500` bytes). Listened natively to `1.25x` mix, inspected decoded frames, and passed `episode_qa.py --stage export`.
- **Content package & Trypost queue delivery (`transport: api`):** Shared Indonesian copy documented in [`CONTENT_PACKAGE.md`](CONTENT_PACKAGE.md). Uploaded MP4 once in `Admin's Workspace` (`01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37`), scheduled all 3 inherited accounts via `queue: next`, verified `scheduled` status & future times via `get-post`, and saved receipt in [`PUBLISHING.json`](PUBLISHING.json):
  - **Instagram (`@bikindihalaman.id`, `instagram_reel`):** post `01a21c66-5c4d-7071-bacc-6c937b8a7730` — `scheduled` (`schedule_mode: queue`) for `2026-11-28 06:44:00` UTC (`cover_offset_ms: 84350`).
  - **YouTube (`@bikindihalaman_id`, `youtube_short`):** post `01a21c66-8768-73f6-bd23-fee578fc6089` — `scheduled` (`schedule_mode: queue`) for `2026-11-28 10:07:00` UTC (`meta.title: "Bikin Kolam Ikan Gurame di Sudut Halaman"`).
  - **Facebook (`Bangun Di Halaman`, `facebook_reel`):** post `01a21c66-a5ad-71e8-9a0c-33e287e91822` — `scheduled` (`schedule_mode: queue`) for `2026-11-28 06:36:00` UTC.

## Google Drive archive (synced)

- **Folder:** [`budidaya-di-halaman/kolam-gurame-di-halaman`](https://drive.google.com/drive/folders/1IbxWKZDtWlOtcjVbX4nu0cSnuOlbTidw) (`folder_id: 1IbxWKZDtWlOtcjVbX4nu0cSnuOlbTidw`, `remote_path: budidaya-di-halaman/kolam-gurame-di-halaman`, synced `2026-11-27T09:59:15Z` via `gdrive.py` using Doppler, `env_source: doppler+dotenv`):
  - `kolam-gurame-di-halaman.mp4` (`28,704,162` bytes, MD5 `19e5a20935b1f81f2afcf81b36c445aa`, `uploaded`, file `1iQQKBz7aeDtFVvbMHM4ZBs6aje4AS-fS`)
  - `kolam-gurame-di-halaman.srt` (`3,500` bytes, MD5 `fcbebe016ddbb5ac4a7aaceed2dd69f1`, `uploaded`, file `1CgNQjEgj4QsUyEMfhc7K0kctBjOcjQ2d`)
  - `thumbnail.png` (`477,217` bytes, MD5 `28fe8499c1822c7b2606724f46383ffb`, `uploaded`, file `18pONxCPpClx_M-S__FbB89SBYB8nzrHo`)
  - `CONTENT_PACKAGE.md` (`5,972` bytes, MD5 `7722a6ce7386f3e7fd811130ded461f6`, `uploaded`, file `1g9AxNW6tjE1sGC3aqLp6XLhShymAn8Li`)
