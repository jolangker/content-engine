# Bentuk Dukungan

Created: 2026-10-20. Board: `ruang-di-antara`, approved v1.1 (visual v1 restored on 2026-10-18, implementation revision 2026-10-20).
Direction: [editorial](../../boards/ruang-di-antara/EDITORIAL.md), [visual](../../boards/ruang-di-antara/DIRECTION.md), [implementation contract](../../boards/ruang-di-antara/frame.md).

## Resolved brief

- topic_selection: auto
- Topic: Support matching: distinguishing emotional presence from practical solutions.
- Angle: When sharing vulnerability, an immediate leap to problem-solving can feel like dismissal; matching the support type (listening vs solving) builds genuine safety.
- Audience: Indonesian adults navigating communication gaps and recurrent misunderstandings in romantic relationships.
- Message: Distinguish what you actually need—space to be heard (emotional support) or help with next steps (instrumental support). State it clearly, and ask before offering advice.
- Format: Instagram Reel, 1080×1920 portrait, 30 fps, Indonesian lo–gua narration, target ~90 seconds (85–95s range), 14 scenes.
- Visual: approved cream/charcoal/brick/sand palette (`#F3EDE3`, `#302B28`, `#A34F3F`, `#D8C8B5`), Newsreader + DM Sans, two faceless abstract forms, meaningful distance, boundaries, and interactive trajectories; no B-roll.
- Audio: ElevenLabs voice Zephlyn `3mAVBNEqop5UbHtD8oxQ` from project root `.env`, model `eleven_v4`, delivery tags; native reading speed and unaccelerated speech. Quiet, reflective atmosphere.
- Requested endpoint: verified export, content package, Cloudinary original upload, and Buffer Instagram draft.
- execution_policy: automation
- human_review: none
- pre_render_authorization: delegated by the user's --automation instruction
- Human approval: none for this episode; agent verification replaces human checkpoints under delegated authorization.
- Target: My Organization (`691274923530437a1a02ed9f`), Instagram @eliansatya (`6ad6400e778b240e2f5a8060`), Asia/Jakarta; confirmed against board `frame.md` handle `@eliansatya` and live Buffer channel discovery.
- Settings: Reel (`metadata.instagram.type: reel`), `shouldShareToFeed: true`, `isAiGenerated: true`, `saveToDraft: true`, `mode: addToQueue`, `schedulingType: automatic`; no due time.

## Selection provenance

- Internal shortlist comparison:
  1. **Bentuk dukungan: didengar atau dicarikan solusi?** (Selected: Optimal matching model / Cutrona & Russell 1990; addresses everyday vulnerability vs unsolicited advice; strong behavioral contrast and immediate relational utility; diversifies the board's themes into positive co-regulation).
  2. **Ekspektasi yang tak terucap** (Mind reading / unspoken expectations; strong theme, but risks narrative overlap with `limerence`'s theme of guessing vs knowing).
  3. **Permintaan maaf tanpa perubahan pola** (Post-conflict repair; viable, but follows another conflict-heavy episode immediately after `jeda-yang-kembali`).
- Overlap check: `TRACKER.json` and existing productions `limerence` (infatuation and projecting compatibility before a relationship) and `jeda-yang-kembali` (taking a break during conflict with a return agreement) cover distinct situations and takeaways. This episode focuses on supportive communication when one partner shares stress.

## Production and Verification — 2026-10-20

- Spoken script: 183 words, 14 scenes, Indonesian lo–gua in [SCRIPT.md](SCRIPT.md).
- Audio synthesis: ElevenLabs Zephlyn (`3mAVBNEqop5UbHtD8oxQ`), model `eleven_v4`, duration 79.52s native speech. Paced with measured reading pauses to 87.77s (total composition duration 89.400s at 30 fps, 2,682 frames).
- Visual composition: 14 scene sub-compositions in `video/compositions/frames/`, following board v1.1 implementation contract with fixed chrome header/footer and varied scene layouts. Scene 5 features the approved charcoal tension beat.
- Pre-render check: HyperFrames check passed with 0 lint errors/warnings, 0 runtime errors, 0 layout findings, 62/62 motion assertions passed, and 33/33 contrast checks passed.
- Render: `npx hyperframes render . -o ../exports/bentuk-dukungan.mp4 -q delivery` completed in 117.5s (drawElement capture, hardware GPU).
- Output verification: Container decoded with FFmpeg `-xerror`; 14 scene proof frames decoded and compiled into contact sheet [exports/bentuk-dukungan-contact-sheet.jpg](exports/bentuk-dukungan-contact-sheet.jpg).
- Loudness: -16.73 LUFS stereo, -19.74 LUFS mono downmix, -2.85 dBTP.
- Content package: [CONTENT_PACKAGE.md](CONTENT_PACKAGE.md) delivered with copyable Instagram caption, recommended titles, hashtags, and delivery metadata.

## Publishing Status

- Requested endpoint: `--delivery=draft` to Instagram `@eliansatya` via Cloudinary hosting and Buffer MCP.
- Export file: [exports/bentuk-dukungan.mp4](exports/bentuk-dukungan.mp4), 7,038,386 bytes, SHA-256 `fb4512cf67dee93f08c1f7820cc7d4ee9ac2703f3998fe5b1bfdc7e57f8fb4af`.
- Blocker: The Cloudinary MCP connector (`sign_upload`) and Buffer MCP connector (`create_post`) are not currently connected in the execution environment. Local export, checksums, and content package remain fully verified and preserved.
- Receipt: [PUBLISHING.json](PUBLISHING.json).
