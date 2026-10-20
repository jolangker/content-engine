# Verification ? corrective revision v2

Verified 2026-10-20 under the production's existing delegated automation policy. The user authorized the investigated pipeline and visual corrections with ?gas perbaiki?. Human visual/audio approval of this revision is not claimed.

## Configuration and narration

- Default voice now resolves from the root .env through the maintained project narration entry point. ElevenLabs voice metadata verified `3mAVBNEqop5UbHtD8oxQ` as Zephlyn. Provider and model remain ElevenLabs / eleven_v4.
- One full-script synthesis returned the native 76.72s MP3 and alignment. All 187 spoken words match the unchanged script in order. Caption words exclude delivery tags. The new verified cache is keyed by audible request inputs and validates audio/alignment hashes; the old Brian MP3 is not reused or relabeled.
- A derived PCM track inserts 8.60s of reading pauses between ideas. `verification/pacing-v2.json` verifies every original decoded speech sample is preserved and the inserted intervals contain silence. There is no speech-rate change. Source audio/timing remains available separately.
- Seven regression tests pass for project-file precedence over inherited shell settings, stale/missing voice rejection, intentional overrides, request identity, cache/file integrity, and delivery-tag exclusion. The skill validator and changed Python compilation pass.

## Visual and identity review

All 14 scene proofs were inspected in contact sheets; the first 30 seconds were inspected at full resolution. A path/label collision in scene 03 was repaired. Scene 04 uses an issue marker plus two people, avoiding an unintended third character. Layouts vary quotation scale, diagram placement, actor count/size, direction, and typographic sequence. Named layout counts alone are not the creative evidence: the rendered contact sheet was reviewed.

Board chrome is copied from the canonical board component sources, implementation correction 2026-10-20. All 14 sources contain the same CSS and one header/footer pair. `verification/chrome-v2.json` checks 28 rendered samples at every scene's beginning/end, including charcoal scene 04. Series label and handle have stationary pixel bounds; the maximum glyph-edge difference is one pixel from inverted-color antialiasing. Frame numbering changes as intended. No entrance/exit motion targets the chrome.

Final HyperFrames 0.8.176 check (`verification/check-v2-release.json`): no lint, runtime, layout, motion or contrast errors/warnings. It covers 508 layout samples, including 494 transition samples; 300 motion samples with 63 root assertions; 26/26 sampled text contrast checks pass. Browser capture uses hardware Intel Iris Xe / drawElement; the render completed in 125.8s.

## Delivered encode

[Video](../exports/jeda-yang-kembali-v2.mp4): 86.933333s, 1080?1920, 30 fps, 2608 frames, H.264/yuv420p, AAC stereo 48 kHz, 6,808,445 bytes. The entire audiovisual file decodes with FFmpeg -xerror. Fourteen decoded scene proofs match their preview frames with minimum SSIM 0.998217. Encoded loudness: -16.73 LUFS stereo / -19.75 LUFS mono downmix; true peak -2.74 dBTP.

SHA-256: `888eee56e5acb09a609344b4fb2e1e94cdb04b33c6d77c258262ec0e11f10d7d`. [Export evidence](../exports/verification-v2.json), [contact sheet](../exports/jeda-yang-kembali-v2-contact-sheet.jpg), [subtitles](../exports/jeda-yang-kembali-v2.srt).

Studio remains exposed at http://localhost:3002/#project/video; HTTP 200 was verified. No human realtime listen is claimed; voice identity, exact alignment, preserved speech samples, measured mix and full decode are the audio verification basis.

## Version boundaries and rebuild

The v1 sources/audio/export/evidence are preserved under ../revisions/v1. The original Buffer draft and Cloudinary receipt still identify v1; no external replacement, scheduling or publication was performed in this corrective pass. The local v2 export and content package are complete.

For an explicitly authorized rebuild: run ../prepare.py, validate/synthesize via ../synthesize_narration.py, apply ../pace_narration.py, then ../build_video.py. Re-run the affected browser/pixel checks before rendering. ../verify_export.py routes to the current v2 export verifier. A source narration invocation resets timing to its native recording; apply the episode pacing transform before rebuilding the composition.
