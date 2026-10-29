# Delivery verification — v1

## Export

- `exports/momen-kecil-dinikmati-lagi-v1.mp4`: 90.0 seconds, 2700 frames, 1080x1920, 30fps, H.264/yuv420p with stereo AAC, 4,278,479 bytes.
- SHA-256: `e00e0ef575c311d3d8a6e38ab387cf03cdca3f5bb9c4755ce682b1b7d48e609c`.
- Full video/audio decode passed. Actual input measurement: -13.73 LUFS, -1.59 dBTP, LRA 3.10. Values in loudnorm's output fields are hypothetical processing results; this export was measured, not modified again.
- Six actual SFX matches passed at their authored triggers (maximum detected offset 0.000334 seconds). All fifteen encoded acoustic boundaries passed with quiet margins. These are independent of loudness and stream-presence checks.
- All sixteen representative decoded frames and forty-five encoded seam frames were inspected. No blank cuts, wrong palette/chrome, clipped captions, outgoing caption leaks or unintended scene-host overlap. The corrected thought boundary is present in scene 15. Full captions contain 204 spoken words in 55 groups plus a matching SRT.

## Creative and technical review

See video/REVIEW.md for pre-render review, intentional warnings, fresh reviewer feedback and its resolved P1. Final HyperFrames 0.8.209 check passed lint/runtime/layout/motion/contrast/audio with zero errors. The fixed 26px chrome and selector-group baseline warnings are retained with reasons and seek evidence. Eighteen forward/reverse seeks match; all fifteen exact cuts activate the intended host. Preview HTTP200, no page errors and playback progression to 01:30 were checked.

Static storyboard exists with sixteen loaded scene images, HTML board and complete PNG. The initial board passed before audio synthesis. Its final updated capture is 1440x3206, with measured scene labels and the scene15 revision. Initial other stills preserve the planning captions rather than pretending to be captured final video. The separate export proof is decoded from the MP4.

One ElevenLabs eleven_v4 synthesis at the project .env voice produced 81.44 native seconds and 204 aligned words. Native-speed samples were preserved before quiet-region insertion and final source normalization; placed narration is 88.499958 seconds followed by a 1.5-second tail. Word-level estimates are not claimed as precise acoustic alignment.

## Limits and lifecycle

Perceptual listening was unavailable; pronunciation, naturalness and subjective mix balance are not claimed as heard. Visual inspection, browser playback progression, waveform checks, loudness, full decode and cue matching are separate evidence. No human approval is recorded; the user delegated review and render under --automation.

The pipeline-owned preview PID22640/port3002 was released after export verification. Status is not-running and the port has no remaining listener. See video/verification/preview-cleanup.json. No unrelated process was terminated.

## Evidence

Machine receipts under video/verification/: hyperframes-check.json, seek-consistency.json, preview-report.json, exact-seams.json, export.json, encoded-cuts.json, audio-boundaries-export-v2.json, sound-design-export-v2.json and preview-cleanup.json. Content package verifies actual hash/paths and 1047 caption characters/three hashtags. Publishing outcome belongs in PUBLISHING.json after readback; scheduling is not proof of future live publication.
