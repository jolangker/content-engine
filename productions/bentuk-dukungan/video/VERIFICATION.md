# Verification — Bentuk Dukungan

HyperFrames 0.8.180; 1080×1920 / 30 fps; execution_policy: automation.
Render completed in 117.5 seconds, drawElement capture with hardware Intel Iris Xe GPU. All ground-truth comparisons passed.

## Check release

- Lint errors: 0, warnings: 0, info: 0.
- Runtime errors: 0, warnings: 0.
- Layout findings: 0 across 30 samples.
- Motion assertions: 62 assertions targeting headlines, actors, and chrome headers/footers across 300 motion samples: 0 findings (100% passed).
- Contrast checks: 33 checks across 5 sampled timestamps: 33/33 passed (100%).

## Visual and Composition Inspection

- All 14 representative scene frames decoded from the final MP4 and inspected in [exports/bentuk-dukungan-contact-sheet.jpg](../exports/bentuk-dukungan-contact-sheet.jpg).
- Visual variety: 14 distinct layouts following `frame.md` guidelines.
- Chrome identity: fixed header and footer present with correct metadata (`Ruang di Antara`, frame number, handle `@eliansatya`) and stationary positioning.
- Scene 5 utilizes the approved charcoal pressure treatment (`#302B28` background, `#F3EDE3` text, `#D8C8B5` actor) with fixed cream chrome metadata.

## Audiovisual Decode and Loudness

- Entire container decodes with FFmpeg `-xerror` without error or dropped packets.
- Container duration: exactly 89.400 seconds (2,682 frames at 30 fps).
- Narration: ElevenLabs Zephlyn (`3mAVBNEqop5UbHtD8oxQ`) with model `eleven_v4`. Unaccelerated speech, measured reading pauses.
- Encoded loudness:
  - Integrated Stereo: -16.73 LUFS
  - Stereo True Peak: -2.85 dBTP
  - Integrated Mono Downmix: -19.74 LUFS
- Captions: 44 subtitle phrases burned into video and exported to `exports/bentuk-dukungan.srt`.

## Pre-Render Authorization

Pre-render authorization was delegated by the user's `--automation` instruction. Agent verification completed with zero defects across all technical, visual, and audio dimensions.


## SFX correction — 2026-10-20

See [current export verification](../exports/verification-sfx.json) and [cue waveform evidence](verification/sound-design-export.json). The current local export is bentuk-dukungan-sfx-v2.mp4. Six cue matches pass, speech metadata is unchanged, full AV decode passes, fourteen scene comparisons retain the visual output (minimum SSIM 1.0). Integrated stereo loudness -16.73 LUFS; true peak -2.85 dBTP. Prior MP4s fail the new cue-plan verification (baseline evidence is in verification/sound-design-baseline.json), so an audio stream alone cannot satisfy the gate. Contact sheets were inspected. No human or agent realtime listening is claimed; objective evidence does not replace a perceptual balance review.
