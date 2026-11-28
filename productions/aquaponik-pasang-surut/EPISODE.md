# Akuaponik Pasang Surut di Halaman

## Brief and selection

- `topic_selection: user`. On 2026-11-22 the user explicitly confirmed “aquaponik” for production after resolving the input validation on `--topic=aquaponik`.
- Board: `budidaya-di-halaman`, editorial revision 4 (approved), visual revision 1. Inherit [direction](../../boards/budidaya-di-halaman/DIRECTION.md), [editorial framework](../../boards/budidaya-di-halaman/EDITORIAL.md), and [visual specification](../../boards/budidaya-di-halaman/frame.md).
- Purpose: Show an Indonesian backyard keeper building an integrated flood-and-drain aquaponic system from scratch, discovering operational constraints (overflow, stagnant water/root rot, solid waste clogging), and resolving them with an automatic bell siphon and mechanical solids settling.
- Organisms & setup: Small fish pond (nila/lele) at the bottom, elevated gravel grow bed (sayur selada/kangkung) on top, submersible pump, bell siphon, and settling filter.
- Audience: Indonesian-speaking general viewers curious about backyard fish and vegetable cultivation. The viewer is addressed as “kamu”; the narration follows hands-on construction, observable shortfalls, physical repairs, and the earned dual harvest.
- Format: Vertical 9:16 (1080 × 1920), illustrated cutaway animation. Planned duration: ~105–110 seconds, strictly adhering to the Editorial v4 minimum requirement of at least 90 seconds.
- Audio plan: Warm conversational Indonesian narration (board voice: ElevenLabs Pribs `5g0yKK2JwTRka0IG61Hh`), no background music (BGM `none` per board specification), and scene-linked sound effects (splashing, pipe clicks, gravel filling, siphon trigger/drain).
- `execution_policy: human_review`. Retain human checkpoints at hook selection, script approval, visual-storyboard approval, and final-preview review.
- `endpoint: content_package`; `delivery: package`.

## Editorial comparison and overlap

Checked `TRACKER.json` and existing production directories:
- `jejak-kotoran-kolam-nila`: Focuses on recirculating tilapia pond waste treatment through a settling chamber.
- `maggot-jalan-ke-wadah`: Focuses on BSF larvae rearing bin and self-harvesting prepupal migration.
- `pot-sumbu-selada`: Focuses on wick-reservoir self-watering planters.

This new production, `aquaponik-pasang-surut`, builds a full integrated multi-tier aquaponic system combining aquaculture and hydroponics with flood-and-drain mechanics (bell siphon). It does not duplicate existing productions.

## Researched story chain (Editorial v4)

1. **00:00–00:11: Start building on the first spoken beat.**
   The keeper places a fish pond container in the yard corner and erects a sturdy tiered frame with an elevated plant grow bed directly above it, filled with gravel media. A submersible pump is placed in the pond.
2. **00:11–00:23: First visible shortfall (Meluap).**
   The keeper turns on the pump. Water rises steadily into the gravel bed, but with no drainage outlet, it spills over the container rim and threatens to drain the fish tank dry.
3. **00:23–00:35: First intervention (Pipa tegak sederhana).**
   The keeper installs a vertical overflow standpipe through the bottom of the grow bed. Water no longer spills over the rim, draining back into the fish pond.
4. **00:35–00:48: Second constraint (Akar terendam & kekurangan oksigen).**
   With a simple overflow pipe, the water level remains permanently constant. Plant roots submerged constantly in stagnant water show stunted growth and risk root rot due to lack of aeration.
5. **00:48–01:03: Second intervention (Pasang Bell Siphon).**
   The keeper places a bell siphon cap over the standpipe. When the water crests, the siphon effect triggers, rapidly draining the bed down to the bottom snore cuts, sucking fresh atmospheric air into the root zone before breaking and refilling.
6. **01:03–01:18: Third constraint (Kotoran padat menyumbat kerikil).**
   Fish are introduced and fed. Solid fish feces and uneaten feed particles get sucked up by the pump, forming dark sludge pockets in the gravel that restrict water flow.
7. **01:18–01:32: Third intervention (Tabung pengendap kotoran / settling chamber).**
   The keeper splices a vertical settling chamber into the supply pipe between the pump and grow bed. Heavy solid waste settles at the bottom of the chamber, while only dissolved, nutrient-rich water reaches the gravel.
8. **01:32–01:46: Final test and payoff (Siklus biologi & panen ganda).**
   Nitrifying bacteria in the clean gravel convert ammonia into nitrate. Leafy greens thrive above, clean oxygenated water cascades back into the pond below, and fish swim actively.
9. **01:46–01:56: Wide reveal & closing sign-off.**
   Pull back to wide view of the working backyard setup.
   Narration closes with: *“Selamat, kamu sudah punya sistem akuaponik pasang surut sendiri di halaman, panen ikan dan sayur dari satu putaran air. Habis ini, kamu mau bikin apa lagi di halaman?”*

## Writing context

Applied [script-writer](../../.agents/skills/script-writer/SKILL.md) and [research and script](file:///C:/Users/muhth/Documents/projects/content-engine/.agents/skills/shortform-production/references/research.md). Tone is casual, friendly, hands-on educational Indonesian. Avoid hype, greetings, or generic CTAs. Focus on concrete physical actions and observable results.

## Hook review v1

1. **Dual harvest / Action-first (Recommended & Selected)**
   *Opening*: “Kalau kamu mau panen ikan sekaligus petik sayur segar di halaman sempit, kamu pasang wadah baki tanaman tepat di atas kolam ikan.”
   *Angle & Appeal*: Action-first hook opening on the primary aspiration of backyard hobbyists (space-efficient dual harvest) and the immediate hands-on first step.
   *Promise*: Shows how an elevated planter above a fish pond becomes a self-regulating, flood-and-drain aquaponic system that solves overflow, root rot, and sludge build-up.

2. **The Overflow Dilemma / Problem-first**
   *Opening*: “Kalau kamu pompa air kolam ikan langsung naik ke baki sayuran, bakinya bakal meluap atau malah bikin akar tanamanmu busuk terendam.”
   *Angle & Appeal*: Problem-based hook addressing the common beginner failure mode of simply pumping pond water to plants without a proper siphon cycle.
   *Promise*: Reveals why continuous pumping fails and demonstrates how installing an automatic bell siphon creates healthy flood-and-drain cycles for both fish and plants.

3. **Self-watering & Fertilizing / Curiosity & Benefit**
   *Opening*: “Gimana caranya kotoran ikan di dasar kolam bisa otomatis jadi pupuk sayur tanpa kamu perlu ganti air kolam tiap minggu?”
   *Angle & Appeal*: Benefit-driven hook targeting fish keepers tired of frequent dirty water changes, offering a biological and mechanical solution.
   *Promise*: Follows the complete water journey from fish waste to plant fertilizer, explaining the physical build and biological balance of backyard aquaponics.

`hook_selection: user`. On 2026-11-22 the user selected option 1 ("1"). Its wording is preserved verbatim in [SCRIPT.md](SCRIPT.md).

## Script review v1

[SCRIPT.md](SCRIPT.md) contains nine distinct scenes with an estimated ~115–125 second runtime, fulfilling the Editorial v4 requirement of at least 90 seconds.

- **Continuity and role check**: Read without metadata, “kamu” consistently refers to the backyard keeper who builds the setup, observes the shortfalls (overflow, stagnant root saturation, sludge accumulation), executes physical repairs (standpipe, bell siphon, settling chamber), and harvests the crops. The narrator guides and explains causal mechanisms at the exact decision points. Closing lines follow the mandatory two-part sign-off: congratulations naming the built system, followed by the spoken question asking what to build next.
- **Factual claim mapping**:
  - C1 (stacked setup & gravity return) -> Scene 1
  - C2 (continuous pump overflow & root hypoxia) -> Scene 2 & Scene 4
  - C3 (bell siphon flood-and-drain cycle) -> Scene 5
  - C4 (dual aeration of roots and fish) -> Scene 6
  - C5 (nitrification in gravel media) -> Scene 8
  - C6 (mechanical solids settling chamber) -> Scene 7 & Scene 8
- No unsubstantiated harvest quantities or instant cycling timelines are claimed.
- Script timings remain estimates; no narration has been synthesized yet.

## Publishing targets

```yaml
publishing_targets:
  source: board
  board_accounts_file: boards/budidaya-di-halaman/ACCOUNTS.json
  board_accounts_sha256: a755eaf48dcdc490d71b1043e905bc0ac2cd14ef37164f98d6f97d16ac2a5461
  accounts: []
```

## Visual storyboard review v1

- Plan: [video/STORYBOARD.md](video/STORYBOARD.md), 9 scenes matching the approved narration, spanning approximately 126 seconds (exceeding the 90-second minimum duration floor).
- Styled stills: [video/boards/stills/](video/boards/stills/), nine 1080 × 1920 frames captured at 6, 18, 31, 45, 60, 75, 89, 104, and 119 seconds.
- Review artifacts: [HTML board](video/boards/storyboard.html) and [complete PNG board](video/boards/storyboard.png), 1600 × 3622 px (806,871 bytes). Corrected font loading by embedding DM Sans 800 base64 with strict font-readiness verification across all still captures. The saved PNG was opened and inspected: all 9 scene cards, titles, timing labels, and voiceover text are in order with verified DM Sans glyphs.
- [Verification record](video/VERIFICATION.md): `npx hyperframes check --json` passed with `ok: true`, zero lint, runtime, layout, or contrast errors. Browser QA (`video/verification/storyboard-browser.json`) confirmed zero clipped text, all 9 images loaded, and DM Sans ready. Phone viewport captured at `video/verification/storyboard-phone.png` (390 px).
- Presentation: Human review of the complete visual storyboard is required before audio synthesis and animation, under the active `human_review` execution policy.

## Audio and speech synthesis

- **Narration Provider**: ElevenLabs MCP tool `creative_generate_speech`, model `eleven_v4`.
- **Voice**: Pribs (`5g0yKK2JwTRka0IG61Hh`, "Friendly Casual Narration") matching board `AUDIO.json`.
- **Generation ID**: `0taIpokfxCvNdcpZxj85` in session `piQ4Nnac86aCsnInl9s5`, flow `sEa9HznIsFtX1ad6RMcT`.
- **Raw Master Audio**: 127.2 seconds duration (`narration-mcp.mp3`, SHA-256: `e01a17e2d65c2e41fbf36e029a93b0183475c650a7d51db8a203cfdb0c904bbd`).
- **Word-Level Alignment**: Measured with local `faster-whisper` (`large-v3`, CPU int8). Transcribed 336 spoken tokens across 127.2 seconds (`audio_mcp_timings.json`).
- **Narration Import**: Registered via `narration.py --import-mcp` into `.media/audio/voice/narration-34885f29151f75952fdb.mp3` with verified `audio_meta.json`.

## Assembly, clock, and sound design

- **Timebase & Clock**: 30 fps shared clock. Total video duration is **132.87 seconds** (3,986 frames), exceeding the 90-second minimum duration floor.
- **Measured Scene Boundaries**:
  - `s01`: 0.00s – 16.40s (16.40s) — Setup bertingkat wadah & baki kerikil
  - `s02`: 16.40s – 30.30s (13.90s) — Pompa menyala, air meluap dari baki
  - `s03`: 30.30s – 41.73s (11.43s) — Pipa tegak standpipe terpasang
  - `s04`: 41.73s – 54.90s (13.17s) — Akar bibit sayur tergenang statis & membusuk
  - `s05`: 54.90s – 71.93s (17.03s) — Bell siphon otomatis menguras baki (vakum aktif)
  - `s06`: 71.93s – 84.60s (12.67s) — Udara segar masuk akar & aerasi oksigen kolam
  - `s07`: 84.60s – 98.77s (14.17s) — Pakan rutin & kotoran padat ikan mulai menyumbat
  - `s08`: 98.77s – 113.07s (14.30s) — Tabung pengendap memisahkan kotoran & bakteri nitrifikasi
  - `s09`: 113.07s – 132.87s (19.80s) — Ekosistem matang: sayur lebat, ikan nila sehat, air jernih
- **Captions Track**: 96 timed phrase groups in `compositions/captions.html` and companion `captions.srt`. Styled in DM Sans 800 at 46px/1.12 with progressive active word highlights (`#FFD44D` active, `#FFF9E8` spoken, 4px `#281D18` outline).
- **Sound Design (`sound_design.json`)**:
  - `narration`: `use` (continuous eleven_v4 take in Pribs, normalized to -16 LUFS target at `assets/audio/narration.wav`).
  - `bgm`: `none` (strictly adhering to board editorial & visual direction).
  - `sfx`: `use` (5 scene-linked physical cues from verified local media library):
    1. `sfx-standpipe-click`: 31.80s (Scene 3, standpipe seating click, 0.35s, gain 0.20)
    2. `sfx-siphon-whoosh`: 61.10s (Scene 5, bell siphon suction whoosh, 0.60s, gain 0.22)
    3. `sfx-siphon-pop`: 68.70s (Scene 5, air ingress siphon break pop, 0.35s, gain 0.18)
    4. `sfx-chamber-click`: 100.87s (Scene 8, settling chamber fitting snap, 0.35s, gain 0.20)
    5. `sfx-bio-sparkle`: 108.27s (Scene 8, bacterial nitrification biological payoff, 0.80s, gain 0.25)
- **Acoustic Boundaries**: `audio_boundaries.py` verified all 8 scene seams with quiet RMS levels <= -54 dBFS (`{"status": "passed", "boundaries": 8}`).

## Final preview verification

- **Preview Server Lifecycle**:
  - Studio URL: `http://localhost:3002/#project/video`
  - Server URL: `http://localhost:3002`
  - Port: 3002
  - Lifecycle: Server started for human visual review, inspected, and stopped cleanly after human preview approval on 2026-11-22 ("ya").
- **Proof Artifacts**:
  - Combined review sheet: [contact-sheet.jpg](video/verification/preview-final/contact-sheet.jpg) (467 KB, 9-frame sequence).
  - Individual 1080 × 1920 proof stills: [frame-00-at-8s.png](video/verification/preview-final/frame-00-at-8s.png) to [frame-08-at-123s.png](video/verification/preview-final/frame-08-at-123s.png).
- **Technical Validation (`npx hyperframes check --json`)**:
  - `ok: true`, 0 lint errors, 0 runtime errors, 0 layout errors, 0 contrast errors, 0 craft errors, 0 audio errors.

## Delivery export and content package

- **Render Command**: `npx hyperframes render --quality delivery --output ../exports/aquaponik-pasang-surut.mp4`
- **Render Output**:
  - File: [aquaponik-pasang-surut.mp4](exports/aquaponik-pasang-surut.mp4)
  - Size: 6,708,572 bytes (~6.4 MB)
  - SHA-256: `cea4a853c543fcd07ffece4091e18642614420b83948cdd21b3b5c5a3834f9d8`
  - Duration: 132.866667 seconds (2m 12.9s, 3,986 frames at 30 fps)
  - Streams: Video H.264 (High Profile, 1080 × 1920, yuv420p), Audio AAC (48 kHz mono)
  - Integrated Loudness: `-13.25` LUFS, True Peak: `-0.98` dBFS
- **Export Verification**:
  - Stream inspection and decoding pass without errors (`video/verification/export.json`).
  - Audio boundaries verified on rendered export (`audio_boundaries.py --export`: `status: passed, boundaries: 8`).
  - Sound design cues matched in export audio (`sound_design.py --export`: `status: passed, cues: 5`).
- **Companion Deliverables**:
  - Sidecar Subtitles: [aquaponik-pasang-surut.srt](exports/aquaponik-pasang-surut.srt) (5,771 bytes, 96 caption groups)
  - Cover Image: [aquaponik-pasang-surut-cover.png](exports/aquaponik-pasang-surut-cover.png) (236,619 bytes, captured at t = 123.0s)
  - Content Package: [CONTENT_PACKAGE.md](CONTENT_PACKAGE.md)

## Current state

- `stage`: content_package
- `status`: complete
- `next_action`: none (production package ready for distribution)
- Verification: Full production workflow completed. Hook, script, visual storyboard, and final preview approved by user. Audio generated via ElevenLabs MCP and aligned via Whisper. MP4 render verified across streams, loudness, acoustic seams, and SFX matching. Content package written and verified.
