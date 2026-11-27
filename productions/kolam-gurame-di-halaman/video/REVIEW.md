# Film Verification & Independent Review Note — `kolam-gurame-di-halaman`

- **Reviewed film:** `verification/proof.mp4` (`1080x1920`, `24 fps`, `105.750 s` at `1.0x`; delivery target `1.25x` pitch-kept = `84.600 s` at `30 fps`)
- **Pass 1 audit (subagent `8552a4bd-7126-41a8-8221-538f146bb217`):** `FIX BEFORE DELIVERY RENDER` — identified 6 P0s and 4 P1s (`s10` `same-system`, cross-cut caption bleed on seams, `s06` initial drain pre-existing, static `hold` cameras on `s04`/`s07`/`s10`, undersized frame-0 props / `s10` basket & clipped price tag, unverified `s11` closing frames, bare wrist ends, early wide framing on `s03`, and missing `s03` water-seep SFX). All fixed and re-verified.
- **Pass 2 audit (fresh `research` subagent `21ad1006-a1b3-4c10-a757-83c9cbf6c1aa`):** **`APPROVE FOR DELIVERY RENDER`** — 0 P0, 0 P1, 2 minor P2 observations.
- **Audio listening (`listening: agent`):** Listened natively to both ElevenLabs `eleven_v4` single narration take (`Roger` `CwhRBWXzGAHq8TQ4Fs17`, `100.56 s`, 236 words) and final `verification/proof-mix.mp3` (`105.75 s`). Indonesian pronunciation is clean and natural, delivery tags were not read aloud, no words clip, quiet boundaries match `audio_boundaries.py --export` (`10/10` boundaries passed), and 41 organic SFX cues (`bgm: none`) stay audible yet clearly subordinate to speech (`median_vocal_band_snr_db: 27.12`, `longest_severe_masking_s: 0.0`, all 41 cues verified `<= 0.5 ms` offset).

## Gate record

composition_sha256: 1914a8e85e7edfcc15137329c8176e641da5db99733314c494b4333f6eef664e
independent_review: subagent
listening: agent
weakest_shot: s03 (beat-06-at-25.284s.png, 20.67-29.90s), macro push-in and karpet talang insertion read well, but the rounded helper sleeve ends inside the frame and the pre-push clay seep patch is subtle at phone scale
wow_upgrade: s03/s08, extend helper arm sleeves off the viewport edge and enlarge the darkening wet clay seep puddle at the outer wiremesh base during s03 0.00-2.31s for instant mobile read

- rubric.style_fidelity: 9.0/10 — Faithful budidaya-di-halaman 2.5D vector backyard look, 4-plane parallax, warm-clay foreground, consistent dual-pond landmarks, and matching end card (frame-04-at-105.45s.png)
- rubric.concept_wow: 9.0/10 — Authentic 7-round gourami problem-fix arc (cold-rain fungus -> wiremesh seep -> taro sap -> overflow -> sludge/O2 -> predators -> grading) leading into a clear 40 kg x Rp45.000 ~ Rp1.800.000 harvest payoff
- rubric.motion_craft: 8.8/10 — Immediate 0.3s entry motion (beat-01), event-driven push/pan/pull across all 11 scenes, tight s03 macro push (beat-06), smooth s10 basket push + >3s tag hold, and crisp 0.5s delivered end-card cut
- rubric.design_typography: 9.2/10 — Clean two-line captions in calm lower soil (0 readcheck fails, zero bleed on review-seam-01/05/10), unobstructed right-mounted s10 price tag (beat-20, review-seam-10), yellow "bikin di halaman?" + @bikindihalaman.id (frame-02), safe-zone end card (frame-04)
- rubric.finish_texture: 8.5/10 — Crisp vector detailing across water clarity shifts, bubbles, woven basket, and dusk fireflies; minor P2 deduction for floating rounded sleeve cap in s03 (beat-06-at-25.284s.png) and s08
- rubric.sound_sync: 9.0/10 — Single eleven_v4 narration take, bgm: none, 41 frame-locked organic SFX cues (<= 0.5 ms offset) including sfx-s03-leak-seep, 27.12 dB vocal-band SNR, 0.0 s severe masking, 10/10 quiet boundaries
- rubric.technical: 9.3/10 — 1080x1920, 105.75 s at 1x (84.60 s at 1.25x), dom_lint.py (11 scenes, 0 fails), audio_boundaries.py --export (10 boundaries), sound_design.py --export (41 cues) all verified passing

- [pass] hook-frame: Frame 0 and beat-01-at-0.3s.png show bare yard soil with unrolled wiremesh cylinder, folded teal tarp, active forearm entry, and phone-legible "Kalo kamu" caption
- [pass] pictures-alone: review-beats-1.jpg and review-beats-2.jpg trace bare wiremesh build -> cold rain fungus -> salt bath + canopy/paranet -> karpet talang pad -> floating feeding ring -> overflow pipe -> bottom drain + aerator -> predator mesh -> second graded pond -> weighed 40 kg harvest -> dusk wide view without relying on text
- [pass] event-density: Every scene s01-s11 renders explicit on-screen construction changes, problem states (fungus, drop-seep, cloudy foam, storm rim-fill, bottom sludge, predator claw marks, crowding), fixes, and harvest weigh-in
- [pass] motion-variety: Neighbouring scenes vary continuously across framing and camera move (s01 wide push -> s02 medium pan -> s03 close macro push -> s04 medium pull -> s05 medium-wide pan -> s06 close push -> s07 medium pan -> s08 close pan -> s09 wide pull -> s10 medium push -> s11 wide pull)
- [pass] subject-scale: Active vessel/prop cluster fills >=40% frame width across views while retaining yard landmarks (beat-01 ~55% cluster, beat-06/beat-12 >70% cutaway width, s10 beat-19/beat-20 ~44-48% basket width)
- [pass] ear-test: Verified via native audio listen on proof-mix.mp3: conversational Indonesian ("kamu"), unambiguous component progression, zero contradictory pronouns
- [pass] build-first: Spoken run in s01 ("Kalo kamu lingkarkan besi wiremesh di halaman, lalu kamu lapis terpal dan tebar bibit gurame, kamu sudah punya kolam gurame. Tapi setelah kehujanan, sirip ikannya berjamur putih.") completes on bare wiremesh/tarp before fungal spot close-in (8.04s turn)
- [pass] shortfall-before-fix: Seven distinct gourami-specific rounds in s02-s08 (8.23s-9.90s each at 1x) each show the problem before applying and verifying its upgrade using varied transitions
- [pass] same-system: Backyard landmarks (banana tree, fence, house, garden bed) and cumulative pond upgrades (canopies, karpet talang, rings, overflows, bottom drains, red valves, aerators, predator mesh, second pond) stay visible together through s10 (beat-19, beat-20, review-seam-10) and s11
- [pass] final-job: s09 (75.07-83.87s) shows heavy rain shedding off the canopy and out both screened overflows, clearing to sunny shaded water with fine bubbles and active feeding across both ponds
- [pass] income-scene: s10 (83.87-95.43s) weighs plump harvested gourami in an oversized basket beside both intact ponds on a 40 kg hanging scale, dropping an unobstructed right-mounted world tag reading "40 kg x Rp45.000 / ~ Rp1.800.000 / estimasi harga pasar Nov 2026" (>3.3s hold, no profit claim)
- [pass] event-map: 18 planned/rendered events across STORYBOARD.md (1 premature build + 14 round events + 1 stability storm/feed check + 1 weighed harvest + 1 closing wide & end card), every component shown entering the yard
- [pass] closing-lines: s11 congratulates "kolam gurame di halaman" and closes on "Habis ini, apa lagi yang mau kamu bikin di halaman?" with zero channel intro or follow ask
- [pass] closing-signature: closing-check/contact-sheet.jpg, frame-02-at-104.9s.png, and frame-04-at-105.45s.png confirm yellow "bikin di halaman?", fading @bikindihalaman.id handle, clean caption clear, and 0.625s (0.5s delivered) thumbnail-matched end card at 105.125s
- [pass] reframing: Every scene s01-s11 carries event-driven camera motion (push/pan/pull) with zero dead holds >3.0s and tactile impulse settles on physical hits
- [pass] living-world: 4-plane 2.5D depth parallax, drifting clouds/birds, butterflies, dusk fireflies & lit house window (s11), weather lighting shifts, water ripples/caustics/bubbles, and calm lower soil behind captions
- [pass] event-sfx: sound_design.json + sound_design.py --export verify 41 word-anchored organic SFX cues (including sfx-s03-leak-seep at 22.919s) with bgm: none and 27.12 dB vocal-band SNR
- [pass] vessel-scale: Oversized frame-0 build props, tight >70% s03/s06 cutaways, and >=40% s10 harvest basket preserve yard landmarks and clear readability at 360px phone preview

### Pass 1 Findings Disposition (All Resolved)
- P0 · s10 same-system regression -> restored dual completed circular ponds & side bed behind s10 gantry & basket · fixed
- P0 · cross-cut caption bleed on review-seam-01/05/10 -> gated captions against owning sceneEnd - 0.03s · fixed
- P0 · t=48.83s · s06 bottom drain pre-existing before install -> s06 starts bare-floor and drops drain at 3.6s · fixed
- P0 · s04/s07/s10 static hold cameras -> replaced with pull (s04), pan (s07), and push+tag-drift (s10) + synced STORYBOARD.md · fixed
- P0 · Frame 0/s01-03/s10 undersized vessels & s10 tag edge clip -> enlarged props >=40% width, added s03 macro push 1.72x, repositioned s10 beam nail to {406, 228} · fixed
- P0 · closing-check frames uncaptured -> captured & inspected 102.5, 104.5, 104.9, 105.15, 105.45s · fixed
- P1 · severed floating hand stumps -> added dark-green long sleeve forearms in drawHand · fixed
- P1 · s03 wide early cutaway -> tightened camera push to 1.72x over left seam · fixed
- P1 · s10 overhang nail clipped right edge -> moved nail world coordinate to {406, 228} with wider beam · fixed
- P1 · s03 missing leak water drip SFX -> added sfx-s03-leak-seep (water-drain, gain 0.14) · fixed
- P2 · s03/s08 helper arm sleeve cap ends inside viewport & initial clay seep subtle at phone size -> deferred cosmetic polish (`wow_upgrade`) · open
