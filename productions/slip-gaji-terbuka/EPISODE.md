# Semua Slip Gaji Wajib Dibuka ke Publik

## Brief and execution

- **slug:** `slip-gaji-terbuka`
- **topic:** Twin-world 10-year thought experiment comparing two identical cities where World A mandates that every worker's salary slip is publicly visible while World B keeps individual salaries confidential.
- **topic_selection:** `user` (user accepted recommended Candidate #1 *"Semua Slip Gaji Wajib Dibuka ke Publik"* from the 10-topic `dua-dunia` discovery shortlist with `"setuju"` on 2026-11-24).
- **board:** `dua-dunia` (`approved`, revision `editorial v3 / visual v1`)
- **direction:** [DIRECTION.md](../../boards/dua-dunia/DIRECTION.md)
- **editorial:** [EDITORIAL.md](../../boards/dua-dunia/EDITORIAL.md)
- **visual:** [frame.md](../../boards/dua-dunia/frame.md)
- **contract_snapshot:** [CONTRACT.json](CONTRACT.json) (copied from `boards/dua-dunia/CONTRACT.json`, `editorial v3 / visual v1`, SHA-256 `46ecd764943ca5ab0e2059d560bd199f04c0487a6b8237bba0d86b309d63f38d`, validated via `episode_qa.py --contract`).
- **purpose:** Provocative, vivid miniature-world simulation testing the gut intuition that forcing all salaries into the open instantly creates workplace fairness and higher pay — exposing the asymmetric morale shock, the employer bargaining-power trap ("domino raise ceiling") in a 3D office cutaway, flattened merit rewards, and a split trade-off verdict (Archetype C) where cross-firm job mobility decides who wins.
- **audience:** General Indonesian short-form viewers (office workers, fresh graduates, freelancers, students, managers).
- **format:** `1080x1920`, `30 fps`, hybrid 3D low-poly diorama (topic-specific Polyfork GLB office/commercial interiors & street props + procedural capsule citizens), Fredoka bold outlined captions in `[54, 1380, 972, 200]`, persistent top-center disclaimer `Eksperimen pikiran. Angka dari model.`.
- **language:** Indonesian (natural spoken conversational storytelling, consistent *aku/kamu* or *kita* register; zero stiff policy-report prose).
- **duration_target:** `75–115 s` (sweet spot `85–105 s`, `180–290` spoken words planned at `2.4 wps` baseline since board voice `AfkBqzsATOuueGnLAvJi` has no prior measured production in `episode_qa.py --budget`; re-budget after first measured take).
- **audio:** Narration (`eleven_v4`, board default voice `AfkBqzsATOuueGnLAvJi` — *Samsul — Warm & Clear Narrator*, subject to API tier availability at audio stage) + lighthearted acoustic-guitar/mallet BGM (`-15.5..-12.5 LUFS`, `<= -0.5 dBTP`); SFX optional/sparse per board contract.
- **outcome_archetype:** **Archetype C — *Sama-sama ada harga mahal* (Bitter Trade-Off / Split Verdict)**, intentionally rotating away from Episode 1's Archetype A (*Delayed Crossover*) so channel outcomes stay unpredictable.
- **requested_endpoint:** `publishing` (upgraded from `content_package` by user's explicit `"upload ke queue"` approval at the final preview checkpoint on 2026-11-25).
- **delivery:** `queue` (authorized across all 3 inherited `Dua Dunia Lab` Trypost accounts via `"upload ke queue"`).
- **execution_policy:** `human_review` (all human checkpoints completed: topic selection, hook selection, script approval, visual storyboard v1.1 approval, and final preview approval + queue delivery authorization).

## Publishing targets

*Inherited from `boards/dua-dunia/ACCOUNTS.json` as default package destinations. Target inheritance authorizes no external upload, draft, queue, or publish action (`delivery: package`).*

```yaml
publishing_targets:
  source: board
  board_accounts_file: boards/dua-dunia/ACCOUNTS.json
  board_accounts_sha256: a029e7b9199fa4e4b9a9d6bb711dd26dc56a23ad4373c7c6daa3b7021ef6865b
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

## Candidate comparison & overlap check

- **Overlap check:** Inspected `TRACKER.json` and `productions/` folders. The only existing `dua-dunia` episode is `transportasi-umum-gratis` (fare-free public transit, street/station setting, Archetype A delayed crossover). No other board covers mandatory public salary disclosure, and the topic is completely distinct from the board's reference video (corruption).
- **Why Candidate #1 beat alternatives:** Out of 10 shortlisted `dua-dunia` candidates across public/economic rules (UMR 2×, 4-day workweek, no homework/exams, removing fuel subsidy, empty-home tax) and social/lifestyle experiments (open salary slips, banning paylater/installments, garage mandate for cars, 9 PM social-media curfew, mandatory cost/margin price tags), public salary disclosure provides the sharpest visual contrast after Episode 1 (moving into offices, salary boards, and HR rooms), immediate comment-debate polarization for Indonesian workers/students, and strong empirical grounding for an Archetype C split verdict.

## Research status

- **Status:** Complete ([SOURCES.md](SOURCES.md)).
- **Key resolved findings:**
  1. **Pay gaps genuinely shrink:** Denmark's 2006 law cut gender pay gaps ~13% (Bennedsen et al. 2022), Canada's Sunshine Lists cut them ~30% (Baker et al. 2023), and US public academic disclosure cut within-department inequality up to 20% and drove up to 50% of gender-gap narrowing (Obloj & Zenger 2022).
  2. **Immediate morale & quit shock is asymmetric:** Below-median earners lose job satisfaction and look for new jobs while above-median earners feel no boost (Card et al. 2012); discovering a peer earns 10% more cuts effort by 9.4% in a Southeast Asian bank experiment (Cullen & Perez-Truglia 2022); online public tax records in Norway widened the rich–poor happiness gap by 29% (Perez-Truglia 2020).
  3. **Core 3D mechanism — the employer bargaining-power trap:** Under open pay, granting one worker a raise pressures the firm to raise every peer, letting employers credibly lock a lower, flatter ceiling (average wages −2% overall and −4% for college-educated workers across 13 US states in Cullen & Pakzad-Hurson 2023; −1–3% in Canada; −7% pay and +75% quit rate among top California city managers in Mas 2017) and weakening pay-for-performance (Obloj & Zenger 2022).
  4. **Split-verdict flip condition:** Cross-firm transparency paired with easy job switching pushes employers to compete upward (+1.3–3.6% in Arnold et al. 2025 working paper; Cullen & Pakzad-Hurson 2023), whereas low job mobility traps workers under flat internal ceilings.

## Hook options (awaiting human selection)

*Board performance analysis: none available yet (`transportasi-umum-gratis` is still in Trypost draft status). All 3 hooks strictly obey `dua-dunia` `editorial v3` (`EDITORIAL.md#hook-craft` & `CONTRACT.json` `sharp-premise-hook`): zero format announcement (`"Kita simulasikan..."`), Sentence 1 `<= 4.5 s` at `2.4 wps`, active 3D Frame 0 motion within `<= 0.5 s`, and every implication grounded in `SOURCES.md`.*

### Option 1 (Recommended) — Counter-intuitive gut punch
- **Mechanism:** *Counter-intuitive gut punch* — immediately collides with the popular intuition ("open salaries make raises easier") in the first breath to trigger an instant curiosity gap.
- **Spoken line (10 words total; Sentence 1 = 5 words, `~2.08 s`; full hook `~4.17 s` at `2.4 wps`):**
  > "Semua slip gaji dibuka publik. Anehnya, naik gaji malah seret."
- **Frame 0:** Street-to-glass-office cutaway diorama at morning arrival: a glowing dark-navy `PAPAN SLIP GAJI` board hangs in front of a bustling office lobby (`RP 6 JT`, `RP 9 JT`, `RP 14 JT`) as capsule coworkers step up and point (`t = 0.0–0.5s`) while a subtle red ceiling bar lowers across the top pay band.
- **On-screen line:** Bold Fredoka headline `SLIP GAJI DIBUKA PUBLIK?` + persistent top-center disclaimer `Eksperimen pikiran. Angka dari model.` + lower-band word-synced captions.
- **Angle & promise:** Strongest mid-scroll stop for Reels/Shorts because it immediately challenges what viewers expect, then pays off the promise directly through the 3D HR domino-raise ceiling mechanism (Cullen & Pakzad-Hurson 2023), pay-for-performance flattening (Obloj & Zenger 2022), and the cross-firm mobility split verdict in the 100-world grid.

### Option 2 — Provocative daily-life "what if"
- **Mechanism:** *Provocative daily-life "what if"* — poses a crisp, relatable thought-experiment question directly to the viewer without revealing the twist upfront.
- **Spoken line (9 words total; Sentence 1 = 9 words, `~3.75 s` at `2.4 wps`):**
  > "Kalau besok semua slip gaji dipajang terbuka, langsung adil?"
- **Frame 0:** Eye-level 3D office entrance plaza: morning commuters stride toward the glass lobby (`t = 0.0–0.5s`) and pause before a public `SLIP GAJI PUBLIK` board mounted beside the entrance — one worker smiles in relief while two identical-role coworkers side-by-side frown at contrasting figures.
- **On-screen line:** Bold Fredoka headline `GAJI TERBUKA = LANGSUNG ADIL?` + persistent top-center disclaimer `Eksperimen pikiran. Angka dari model.` + lower-band word-synced captions.
- **Angle & promise:** Cleanest, widest debate framing that invites viewers to form their own gut answer ("yes, finally fair!" vs. "no, total office drama!") before testing both halves in the twin-world simulation and revealing why fairness improves while average pay and merit raises tighten.

### Option 3 — Stakes-first scene drop
- **Mechanism:** *Stakes-first scene drop* — drops the viewer straight into the visceral day-one emotional collision of learning the coworker at the next desk earns more.
- **Spoken line (10 words total; Sentence 1 = 5 words, `~2.08 s`; full hook `~4.17 s` at `2.4 wps`):**
  > "Bayangin besok slip gaji dibuka. Ternyata sebelahmu gajinya lebih gede."
- **Frame 0:** Close 3/4 cutaway inside an open-plan office row: two capsule coworkers typing side by side at identical desks glance up as glowing public salary tags (`RP 7 JT` vs `RP 9 JT`) pop above their monitors (`t = 0.0–0.5s`), one shrinking back awkwardly while the other freezes with a sharp frown.
- **On-screen line:** Bold Fredoka headline `SEBELAHMU GAJINYA LEBIH GEDE` + persistent top-center disclaimer `Eksperimen pikiran. Angka dari model.` + lower-band word-synced captions.
- **Angle & promise:** Highest immediate personal-drama hook grounded in Card et al. (2012) and Cullen & Perez-Truglia (2022)'s Southeast Asia bank findings, pulling viewers in through relatable office tension before zooming out to the twin-world HR trap and long-term trade-off.

- **Recommendation:** **Option 1** — delivers the sharpest scroll-stopping contrast with viewers' default intuition, cleanly embodies `dua-dunia` `editorial v3`'s punchy counter-intuitive voice, and sets up the exact HR wage-compression twist that makes the 3D mechanism unforgettable.
- **Selected hook:** **Option 1** (`user` approved recommended Option 1 with `"setuju"` on 2026-11-25).
  - **Spoken line:** `"Semua slip gaji dibuka publik. Anehnya, naik gaji malah seret."` (`10` words total; Sentence 1 = `5` words `~2.08 s`, full hook `~4.17 s` at `2.4 wps`).
  - **Frame 0:** Street-to-glass-office cutaway diorama at morning arrival; glowing dark-navy `PAPAN SLIP GAJI` board (`RP 6 JT`, `RP 9 JT`, `RP 14 JT`) hangs outside the busy lobby as capsule coworkers walk up and point (`t = 0.0–0.5 s`) while a red ceiling bar lowers across the top row.
  - **On-screen line:** Bold Fredoka headline `SLIP GAJI DIBUKA PUBLIK?` + persistent top-center `Eksperimen pikiran. Angka dari model.` + lower-band word-synced captions.

## Script check (v1 — approved)

- **Approval:** Approved by user (`"approve"`) on 2026-11-25.
- **Script artifact:** [SCRIPT.md](SCRIPT.md) (`v1`, `19` scenes across all 6 `dua-dunia` `editorial v3` causal phases; Archetype C split verdict).
- **Word budget:** `239` spoken words (`CONTRACT.json` range: `180–290`). `episode_qa.py --budget` reported no prior measured narration for board voice `AfkBqzsATOuueGnLAvJi`, so budgeted at `2.4 wps` baseline (`script-craft.md`) → predicted speech `99.58 s` (range `88.5–113.8 s` across `2.1–2.7 wps`), fitting `CONTRACT.json` `75–115 s` (`85–105 s` sweet spot). Re-budget immediately after first measured narration take.
- **First sentence timing:** `"Semua slip gaji dibuka publik."` — `5` words → `2.08 s` predicted at `2.4 wps` (full 10-word hook `~4.17 s`, safely `<= 4.5 s` contract limit).
- **Cold-read check:** **Pass.** Read the complete 239-word narration standalone without headings, visuals, or metadata:
  - Repairs made before finalizing v1: (1) added explicit `"di Dunia A"` anchor in S05 so the week-1 reaction clearly belongs to World A without visual labels; (2) added `"Bos setuju karena pintu tertutup."` in S11 so the closed-door vs. open-board contrast lands fully to the ear before S12; (3) dropped unverified "title inflation" loophole from S14 so every claim maps strictly to verified findings in `SOURCES.md`; (4) replaced formal/literary wording (`tak lagi`, `kesenjangan`, `orang-orang`, `pelan-pelan`) and `"HR"` (TTS pronunciation hazard) with crisp spoken Indonesian (`nggak`, `selisih gaji`, `perlahan`, `bos`/`kantor`); (5) explicitly framed model outputs (`Di model sepuluh tahun ini`, `Dari seratus percobaan`) and spelled out all numbers in Indonesian words (`seratus`, `lima puluh empat`, `sepuluh`).
  - Every pronoun (`keduanya`/`kedua dunia`, `Yang gajinya`, `Mereka`), world (`Dunia A`/`Dunia B`), and causal link resolves strictly from speech.
- **Script-relevant contract judged rules (`CONTRACT.json`, `editorial v3 / visual v1`):**
  - `hook-frame`: **pass** — S01 Frame 0 opens on active 3D glass-office lobby with glowing `PAPAN SLIP GAJI` board, moving arriving workers (`0.0–0.5 s`), and phone-legible headline `SLIP GAJI DIBUKA PUBLIK?`.
  - `ear-test`: **pass** — standalone cold-read resolves every actor, world, and cause-effect beat without on-screen text.
  - `epistemic-disclaimer`: **pass** — persistent `Eksperimen pikiran. Angka dari model.` carried across all 19 scenes, and simulation metrics explicitly framed as model runs (`Di model sepuluh tahun ini`, `Dari seratus percobaan`).
  - `provocative-relatable-topic`: **pass** — tests one clean workplace/social rule (mandatory public salary disclosure) directly hitting everyday wages, peer tension, and raise negotiations; completely distinct from Episode 1 and the corruption reference.
  - `sharp-premise-hook`: **pass** — S01 drops straight into a counter-intuitive 10-word gut punch (`~4.17 s`, Sentence 1 `~2.08 s <= 4.5 s`) with zero format announcement (`"Kita simulasikan..."`).
  - `controlled-twin-worlds`: **pass** — S02 establishes a concise, non-robotic shared baseline in 50/50 split-screen (`DUA KOTA KEMBAR · AWAL SAMA` — synced from `100.000 pekerja` during storyboard number-sync lint without altering spoken narration) before S03–S04 isolate the single salary-disclosure rule.
  - `causal-twist-and-outcome`: **pass** — moves through asymmetric morale shock (S05–S07), genuine pay-gap narrowing (S08), unexpected Year 2 raise freeze (S09), and Archetype C bitter trade-off / 54–46 split verdict (S15–S17) rather than repeating Episode 1's Archetype A winner formula.
  - `physical-mechanism`: **pass** — S10–S13 use a concrete 3D architectural office cutaway contrasting `Dunia B`'s closed wooden door (1 raise = 1 person) against `Dunia A`'s glass wall + corridor `PAPAN GAJI` domino wave (1 raise → 10 coworkers knocking → heavy flat ceiling beam locking pay down).
  - `spoken-storytelling-voice`: **pass** — conversational Indonesian storytelling alternating short 3–6 word punches (`Kelihatannya beres. Padahal belum.`) with vivid concrete workplace moments; zero policy-report prose or bullet lists.
  - `data-proof-cards`: **pass** — S15 dark-navy 10-year divergence HUD chart (`Selisih vs Gaji Rata-Rata`) + S17 dark-navy 10×10 Monte Carlo robustness grid (`54 / 100 Dunia A unggul`).
  - `soft-closing-cta`: **pass** — S19 closes with `"Dari dua dunia ini, kamu pilih kerja di Dunia A, atau tetap di Dunia B?"` (consecutive `dua dunia`, zero follow/subscribe/like prompts).

## Visual storyboard (v1.1 — approved)

- **Approval:** Approved by user (`"approve"`) on 2026-11-25 after v1.1 randomized Frame 17 100-world grid revision.

- **HyperFrames project:** [video/](video/) (initialized via `npx hyperframes init` on CLI `0.9.93`, carrying board `Fredoka-Variable.ttf`, `OFL.txt`, Three.js r170 ESM vendor files, [video/frame.md](video/frame.md), and [video/BRIEF.md](video/BRIEF.md); posed composition preserved at [video/boards/.posed.html](video/boards/.posed.html) with starter composition restored to [video/index.html](video/index.html) per storyboard recipe).
- **Canonical storyboard plan:** [video/STORYBOARD.md](video/STORYBOARD.md) (`19` frames, all `status: built`, planned duration `99.58 s` across 6 acts/phases, max same-shot run `2`, read cadence `<= 1.5 s`).
  - `storyboard_lint.py --strict`: **passed** (`0` errors, `0` warnings, `max_push_streak: 1`, `text_dominated_share: 0.0`). Synced Frame 2 on-screen pill to `DUA KOTA KEMBAR · AWAL SAMA` (and matched the visual note in `SCRIPT.md` without changing spoken narration) to satisfy strict number-sync.
- **3D assets & staging:**
  - `video/assets/kit-3d.js` + `video/assets/episode-3d.js` (deterministic `renderAt(t)` across 6 bespoke 3D environments: glass office lobby plaza + sunset lobby, twin corporate districts, open-plan office bay, office pantry/breakout lounge, interior split rooms, and the hero dual-room 3D cutaway featuring the closed wooden door vs. glass wall, corridor `PAPAN GAJI`, 10-worker domino wave, and lowering mechanical ceiling beam, plus S15 10-year divergence HUD & S17 100-world Monte Carlo grid HUD).
  - Sourced **21 topic-specific Polyfork GLBs** (`office-794453` + `nyc-city-kit-fbca88`, CC BY 4.0, total `1.86 MB`) into `video/assets/models/` alongside 6 board starter GLBs (`27` GLBs verified present, `THREE.NoToneMapping` + `THREE.SRGBColorSpace`, `PCFShadowMap` with `normalBias: 0.08`).
- **Required visual storyboard artifacts:**
  - **Scene stills:** `video/boards/stills/` — `19` posed static stills (`frame-00-at-2.71s.png` .. `frame-18-at-97.39s.png`).
  - **Change-over-time poses:** `video/boards/poses/` — `41` stills (`hook-0.0s.png`, `hook-0.4s.png`, `hook-3.0s.png`, plus `19` start/end pairs `01-a-start.png`/`01-b-end.png` .. `19-a-start.png`/`19-b-end.png`).
  - **HTML review board:** [video/boards/storyboard.html](video/boards/storyboard.html) — verified in headless Chromium (`60/60` images loaded with `naturalWidth > 0`, `0` broken resources, proper `act` / `frame` / `title` / `time` / `words` / `poses` structure).
  - **Combined board PNG:** [video/boards/storyboard.png](video/boards/storyboard.png) — `1680×8403 px` (`3.93 MB`), full-page capture visually inspected end-to-end along with individual hero stills and contact sheets.
- **Visual inspection & craft repairs completed before board freeze:**
  1. Fixed WebGL half-viewport clipping after `renderSplitScreen()` by resetting `scissorTest(false)` and full viewport `1080×1920` on exit and at `renderAt()` entry.
  2. Raised all S15/S17 HUD text sizes to `>= 28 px` to satisfy `npx hyperframes check`'s portrait legibility floor and boosted `.mob-tower.rival` contrast (`#9ED182`).
  3. Pulled S01 lobby camera back and tuned `PAPAN SLIP GAJI` height so `SLIP GAJI DIBUKA PUBLIK?` never collides with the lowering `PLAFON KETAT` tag.
  4. Replaced oversized bus in S02/S03/S19 corporate plazas with a compact `hatchback` so tower entrances stay clear.
  5. Re-framed S06 desk close (workers rotated front-3/4, clean `RP 6 JT` + `LOKER BARU` + briefcase vs. `RP 8 JT`), S07 pantry (`100%` uncropped cluster margins), S09/S16 interior splits (front-3/4 poses + inset plaques), S10–S13 cutaways (clean wing plaques on S10 wide, hidden on S11–S13 close-ups so DOM top banners never collide), S14 exiting workers (all 3 carrying briefcases visible across frame), and S15 chart legend (`Dunia B (Rahasia)` clear of amber line + `Tertahan!` badge opaque by mid-beat).
  6. **User revision (`v1.1`, 2026-11-25):** Per user feedback (`"panel uji coba 100 jangan dibuat sorted gitu yang ijo dan bukan. bikin random aja fill-nya"`), replaced Frame 17's contiguous top-54/bottom-46 grid with a deterministic seeded Fisher-Yates scatter (`seed 54107`, exact `54` green-gold / `46` slate) and randomized reveal sequence (`seed 54209`) from neutral pending sockets; re-captured `17-a-start.png`, `frame-16-at-86.25s.png`, `17-b-end.png`, rebuilt `storyboard.html` (`60/60` images loaded) and `storyboard.png` (`1680×8403 px`), visually inspected updated stills and full PNG, and re-passed `storyboard_lint.py --strict` and `episode_qa.py --stage storyboard`.
- **Quality gate (`--stage storyboard`):** **PASSED** (`disclose: []`, all 7 checks passed: `scene-count: 19`, `duration: 99.58 s`, `shot-variety: max_run 2`, `reads-cadence <= 1.5 s`, `poses: 3 hook + 19 start/end pairs`, `storyboard-artifacts: 19 stills + HTML + PNG`, `storyboard-craft: 0 errors / 0 warnings`). Saved to [video/verification/quality-gate-storyboard.json](video/verification/quality-gate-storyboard.json).
- **Preview server:** None started (remote VM environment; storyboard verified and delivered via static HTML board and combined PNG artifact).

## Audio & sound design (completed)

- **Transport & voice resolution:** `elevenlabs_api` (REST API via `.env`, Free tier; `elevenlabs` CLI not logged in). Board default voice `AfkBqzsATOuueGnLAvJi` (*Samsul*, `category: professional`) returned `HTTP 402` on the Free-tier key (0 credits spent). User explicitly authorized episode override to premade `eleven_v4` voice `TX3LPaxmHKxFdv7VOQHJ` (*Liam — Energetic, Social Media Creator*) for consistency with `dua-dunia` Episode 1 (`transportasi-umum-gratis`).
- **Single-take narration:** Synthesized via `narration.py` into `video/.media/audio/voice/narration-cf8d1518ce8f331e7cd5.mp3` (`96.758 s`, `239` spoken words, `2.47 wps`, native word timestamps, Sentence 1 ends at **`2.120 s` `<= 4.5 s`**, full hook ends at `4.720 s`). Natively auditioned end-to-end by agent (`listening: agent`) — crisp natural Indonesian storytelling, zero read-aloud delivery tags, zero clipped edge syllables.
- **BGM & master mix:** Deterministic `112 BPM` F-major acoustic-guitar (Karplus-Strong) + wooden-mallet + warm bass bed (`video/audio/bgm-acoustic-mallet.wav`, `97.400 s`, `48 kHz stereo`, SHA-256 `1ea0a4901db5a4c3...`) matching `dua-dunia` board direction, shifting into minor suspense across `S06–S07` and `S09–S14`, with subtle harmonic mallet accents on `S03`, `S08`, `S11` (quiet deal chime), `S12` (ascending wooden-mallet domino pulse), `S13` (damped low-end ceiling-lock thud), `S15`, and `S17`, and resolving cleanly on an F-major cadence at `97.40 s`. Mixed with `-25 dB` vocal-pocket EQ (`highpass 90 Hz`, `-3.5 dB @ 1.8 kHz`), gentle sidechain ducking, and 2-pass EBU R128 `loudnorm` into `video/audio/master-mix.wav` (`-14.51 LUFS`, `-2.49 dBTP`, SHA-256 `06d440fe07ad7a61...`) and natively auditioned end-to-end (`listening: agent`).
- **Timing & sound plan:** Exact 30-fps-snapped scene timings (`97.400 s`, `19` scenes, `239` words, `60` hand-curated semantic Indonesian caption clauses) saved in [video/timing.json](video/timing.json); explicit `narration: use`, `bgm: use`, `sfx: none` decisions and asset hashes recorded in [video/sound_design.json](video/sound_design.json). [video/STORYBOARD.md](video/STORYBOARD.md) updated to measured scene windows (`status: animated`; `storyboard_lint.py --strict`: `passed`, `0` errors / `0` warnings).

## Production & verification (passed)

- **Composition & deterministic checks:** Wired [video/index.html](video/index.html) (`97.40 s`, `1080×1920 @ 30 fps`, `<audio id="master" src="audio/master-mix.wav">`, `composition_sha256: 1905b58fd5a531f02ae92594aad682bc2c4ddbb52f4068dd332846733bb7bbaf`), [video/assets/kit-3d.js](video/assets/kit-3d.js), and [video/assets/episode-3d.js](video/assets/episode-3d.js). Verified:
  - `npx hyperframes check --json`: `contrast` `36/36` WCAG AA passed, `craft` `0` errors / `0` warnings, `audio` `0` errors, `runtime` `0` errors.
  - `dom_lint.py`: `status: passed`, `g5_fails: 0`, `readcheck_fails: 0` ([video/verification/dom-lint.json](video/verification/dom-lint.json)).
  - Bit-for-bit seek determinism (`45s → 90s → 10s → 45s` and `86s → 81.5s → 86s`): `deterministic: true`, `errors: []`.
- **Draft proof film:** Rendered via HyperFrames (`--quality draft` in 6 sequential chunks muxed losslessly with unbroken `audio/master-mix.wav`) to [video/verification/proof.mp4](video/verification/proof.mp4) (`SHA-256: 3381799f4703ae8d201e2da2812120f769ce5f40cb0c91a6370c215e59f67421`, `1080×1920 @ 30.0 fps`, `97.40 s`, `first_motion_seconds: 0.2`, `longest_static_seconds: 0.0`, `held_share: 0.0`, `integrated_lufs: -14.56`, `true_peak_dbtp: -2.00`). Decoded contact sheets ([review-sheet-1.png](video/verification/review-sheet-1.png), [review-sheet-2.png](video/verification/review-sheet-2.png)) and decoded audio ([proof-audio.wav](video/verification/proof-audio.wav)) inspected directly.
- **Independent review loop (`subagent`, fresh-context jury):**
  - **v1 (`FAIL`):** Caught 9 P0s (S11 ajar door/transom, S06 chair impalement + occluded `LOKER BARU`, S05/S09/S10/S12/S16 plaque clipping, S15 curve/legend overlap, S13 flat slab beam). All 9 fixed in v2.
  - **v2 (`FAIL`):** Caught 4 P0s (detached floating `monitor-arm-609448.glb` across office interiors, levitating S06 `LOKER BARU` + overhanging briefcase, S09/S16 Dunia B faces inside caption band + heavy 550px `.caption-scrim` + misaligned `+15% NAIK`, S05/S08 tag occlusions) + S11 cutaway `wow_upgrade`. All 4 P0s, S11 `wow_upgrade` (`1.86m` opaque cutaway wall revealing smiling Boss B & Star B + green `ANGGARAN` over shut walnut `TERTUTUP` door), S14 gripped banker box & hand-parented briefcases, S07 coffee cups, and S11–S13 BGM marimba accents resolved in v3.
  - **v3 (`PASS`):** `0` open P0s, **`19 / 19` judged rules `[pass]`**, **`7 / 7` jury rubric dimensions `>= 7.0`** (`style_fidelity 8.3`, `concept_wow 8.4`, `motion_craft 7.5`, `design_typography 8.2`, `finish_texture 7.4`, `sound_sync 7.8`, `technical 8.1`; mean `7.96/10`). Full review & gate record saved in [video/REVIEW.md](video/REVIEW.md).
- **Quality gate (`--stage verification --dom-lint`):** **PASSED** (`status: "passed"`, `disclose: []`, all 20 checks passed). Receipt saved at [video/verification/quality-gate-verification.json](video/verification/quality-gate-verification.json).
- **Preview server:** None started (remote VM environment; preview delivered via decoded contact sheets, `proof.mp4`, and `proof-audio.wav`).

## Export & content package (completed)

- **User final-preview approval:** Approved by user (`"upload ke queue"`) on 2026-11-25, authorizing the final delivery render and Trypost queue scheduling across all 3 inherited `Dua Dunia Lab` channels.
- **Delivery render:** [exports/slip-gaji-terbuka.mp4](exports/slip-gaji-terbuka.mp4) (`1080×1920`, `30 fps` exact `2,922` frames, `start_time: 0.000 s`, `H.264 High yuv420p bt709` + `AAC LC 48 kHz stereo 192 kbps`, `faststart`, `97.40 s`, `55,253,826 bytes` / `52.7 MB`, SHA-256 `d3b4974799c771335319efc1087097f1f0b91d4a55e0332f36774134a4e3d3fa`). Decoded spot-check frames (`0.05 s`, `3.06 s`, `57.38 s`, `95.51 s`) visually inspected under `video/verification/export-check/`.
- **Quality gate (`export`):** `passed` (`disclose: []`, `21/21` checks passed: `-14.56 LUFS`, `-2.00 dBTP`, `longest_static_seconds: 0.0` across all 19 scenes, `hook-motion: 0.2 s`, `empty-frames: 0`, `end-hold: 0.0 s`) — saved at [video/verification/quality-gate-export.json](video/verification/quality-gate-export.json).
- **Content package:** [CONTENT_PACKAGE.md](CONTENT_PACKAGE.md) — recommended title *"Semua Slip Gaji Wajib Dibuka Publik: Naik Gaji Malah Seret?"*, 2 alternatives, shared Indonesian caption (`1,583` chars, `5` hashtags within Instagram's `2,200`-char / `5`-hashtag cap, `SOURCES.md` attribution & model disclaimer), keywords, in-video cover offset `3060 ms`, and verified delivery metadata.

## External delivery — Trypost queue (completed)

- **Transport:** Trypost REST API (`trypost.py`, `api`, workspace `01a1a6aa-c99c-70fb-b7ba-0cdeeb629c37`, `Admin's Workspace`).
- **Requested delivery:** `queue` (scheduled into each connected account's configured `Asia/Jakarta` queue; future publication is NOT claimed as already live).
- **Receipt:** [PUBLISHING.json](PUBLISHING.json) (schema v2, verified export SHA-256 `d3b4974799c771335319efc1087097f1f0b91d4a55e0332f36774134a4e3d3fa`; HTTP 200 exact byte & SHA-256 match verified on all 3 served copies; zero credentials or upload tokens persisted).
- **Verified per-channel results (authoritative `GET /posts/{id}` readback):**
  1. **Instagram (`@duadunia.lab`, `01a208db-b614-7326-9f1b-e5e9ab8100c1`, `instagram_reel`):** Post ID `01a215c2-e928-711f-bdee-d7410bdd2ed3` — **`scheduled`** (`schedule_mode: queue`), scheduled for **`2026-11-26 05:00:00` UTC** (**`2026-11-26 12:00 WIB`**), media ID `01a215c4-2ead-7276-a01d-1cd8de106087` (`55,253,826 bytes`, `97.4 s`, **`cover_offset_ms: 3060`**).
  2. **YouTube (`@duadunia_lab`, `01a20931-862c-7024-a294-6a715c13a929`, `youtube_short`):** Post ID `01a215c5-6121-71e1-bf88-f3a3e7b0a425` — **`scheduled`** (`schedule_mode: queue`), scheduled for **`2026-11-26 09:00:00` UTC** (**`2026-11-26 16:00 WIB`**), media ID `01a215c5-60bb-7079-9b80-b06f9bff6367` (`55,253,826 bytes`, `97.4 s`, `meta.title: "Semua Slip Gaji Wajib Dibuka Publik: Naik Gaji Malah Seret?"`).
  3. **Facebook (`Dua Dunia Lab`, `01a2093d-8956-701b-9933-7f2e6776b752`, `facebook_post`):** Post ID `01a215c5-9780-724f-b84e-3bdb0367ce0e` — **`scheduled`** (`schedule_mode: queue`), scheduled for **`2026-11-26 11:00:00` UTC** (**`2026-11-26 18:00 WIB`**), media ID `01a215c5-9735-719a-b6cf-26f6b473d8b3` (`55,253,826 bytes`, `97.4 s`; `facebook_post` chosen because `97.40 s` exceeds `facebook_reel`'s 90 s limit).

## Review & next action

- **Current stage:** `publishing`
- **Status:** `complete` (for requested `--delivery=queue` across all 3 inherited `Dua Dunia Lab` channels)
- **User acceptance (`final_delivery_approval: user`, 2026-11-25):** User explicitly approved the delivered export, `CONTENT_PACKAGE.md`, and 3 verified Trypost queued posts (`"approve dan buatkan pr"`).
- **Next action:**
  1. *(Optional manual cover)* Trypost sets `cover_offset_ms: 3060` automatically on Instagram Reels only (`supports_video_cover: true`); if you want a custom thumbnail/cover frame on YouTube Shorts or Facebook Post (`supports_video_cover: false`), set it manually in YouTube Studio / Meta Business Suite using the `t = 3.06 s` `PAPAN SLIP GAJI` frame ([f01-3.06s.png](video/verification/export-check/f01-3.06s.png)).
  2. *(Post-publication follow-up)* After the queued posts publish on `2026-11-26` (`12:00 / 16:00 / 18:00 WIB`), run a performance review snapshot under [performance review](../../.agents/skills/shortform-production/references/performance.md) once metrics accumulate.



