# Verification — Cerita belum selesai v1

Status: complete at the requested **export** endpoint. Agent-verified under the user's `--automation` instruction. No human editorial or perceptual audio approval is claimed.

## Delivered files

- [MP4](exports/cerita-belum-selesai-v1.mp4): 86.000s, 1080 × 1920, 30 fps, H.264/AAC, 5.31 MB.
- [Spoken captions](exports/cerita-belum-selesai.srt): 38 phrases, all 194 spoken words, no delivery tags.
- [Decoded export proof sheet](exports/proof-sheet.jpg).
- [Visual storyboard](video/boards/storyboard.html) and [full PNG](video/boards/storyboard.png): all 16 styled planning poses, 1640 × 3531px review image. Later timing labels use measured narration.

## Evidence

Render uses pinned HyperFrames 0.8.197, local GSAP/fonts and seekable scene timelines. The CLI full check passed runtime, layout and contrast without errors. Reviewed exceptions: approved canonical 26px chrome versus generic 28px craft threshold; 38 caption segments intentionally share one dedicated caption track. Studio also scans the required storyboard HTML and inherited chrome fragment as standalone compositions; its two missing-root-ID findings concern those documents, not renderable video scenes.

Creative review covered exactly 16 meaningful compositions, 14 cream and two charcoal frames (04 and 12), silhouette continuity, restrained selective copy and complete caption coverage. Four illustrated states per scene were inspected, and pixel-change checks excluded caption/chrome areas. The full Studio player reached 86s with no page errors; the narration reached 84.8s at native speed. The final quiet visual tail is 1.2s. No B-roll or music bed.

The final MP4 fully decodes. Sixteen decoded frames agree with matching seeked preview states (mean absolute RGB errors recorded in [export.json](video/verification/export.json)). Five planned material cues passed independent waveform matching in the AAC export, including timing/gain checks; see [sound-design-export.json](video/verification/sound-design-export.json). Measured final integrated loudness: -15.23 LUFS, true peak -1.00 dBTP. The original TTS cache is preserved; the mix uses a duration-preserving loudness derivative.

Perceptual listening was unavailable. Native alignment, playback progression, full decode, levels and cue waveform matches provide technical evidence, not a claim about human-perceived naturalness or mix balance. Research and authored-example limits are in [SOURCES.md](SOURCES.md).

## Resource lifecycle and scope

Pipeline preview PID 21360 / port 3002 stopped through the project CLI after export verification. Managed status is not-running and the recorded PID no longer owns the listening port. [Cleanup evidence](video/verification/preview-cleanup.json).

No content package, upload or external delivery was requested under the export cap. Further work requires a new continuation request. Board and generation metadata remain frozen with this production.

MP4 SHA-256: `e21613f5827845a201e50f4ef5921bf2c6897392c45746778912110a9401efca`.

## Subsequent publishing continuation
The user explicitly extended the earlier export-only scope with “publish sekarang via trypost”. The existing video was reused without regeneration. Public served media matched the full export SHA-256 and byte range; exact package caption was checked before publication. Trypost confirmed published at 2026-10-25T19:58:07+07:00; [live Reel](https://www.instagram.com/reel/De6wmnVErFS/). See PUBLISHING.json for the preserved receipt and transient retry observation.
