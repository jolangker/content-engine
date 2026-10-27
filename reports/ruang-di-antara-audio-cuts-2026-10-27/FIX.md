# Ruang di Antara — corrected local exports v2

Completed 2026-10-28. Six local exports and their caption/content packages are complete. All 88 narration seams and 35 inherited sound cues pass checks on the actual encoded MP4s. Existing v1 videos, source voice caches and external delivery receipts are preserved.

| Corrected MP4 | Duration | Verified seams | Minimum quiet after new visual |
| --- | --- | --- | --- |
| [kabar-baik](../../productions/kabar-baik/exports/kabar-baik-v2.mp4) | 86.100s | 13 | 118.3ms |
| [cerita-belum-selesai](../../productions/cerita-belum-selesai/exports/cerita-belum-selesai-v2.mp4) | 86.000s | 15 | 180.0ms |
| [jeda-punya-waktu-kembali](../../productions/jeda-punya-waktu-kembali/exports/jeda-punya-waktu-kembali-v2.mp4) | 88.333s | 15 | 120.0ms |
| [gua-kira-udah-kelihatan](../../productions/gua-kira-udah-kelihatan/exports/gua-kira-udah-kelihatan-v2.mp4) | 85.200s | 15 | 253.3ms |
| [coba-hal-baru-berdua](../../productions/coba-hal-baru-berdua/exports/coba-hal-baru-berdua-v2.mp4) | 90.000s | 15 | 276.2ms |
| [terima-kasih-yang-melihat](../../productions/terima-kasih-yang-melihat/exports/terima-kasih-yang-melihat-v2.mp4) | 90.000s | 15 | 307.5ms |

Each production's exports folder contains matching `*-v2.srt`, `*-v2.vtt` and `export-proof-v2.png`. Its `CONTENT_PACKAGE.md` and `VERIFICATION-v2.md` identify the current local version, actual SHA-256, evidence and listening limits.

## Changes

- Pauses are placed inside measured quiet source audio, replacing midpoint-only timestamp cuts.
- Visual cuts use the integer 30fps clock and retain quiet margins on both sides. Captions, local choreography and SFX timing share the revised scene map.
- For recordings with old inserted pauses, the untouched source is spliced first, then normalized once to the inherited episode targets. This also removes the risk of rejoining an old limiter/gain edge inside a syllable. Individual word times remain estimates anchored to each acoustic utterance.
- Original layouts, source recordings and speech speed are retained. For the final audio-only normalization correction, verified H.264 video packets were preserved byte for byte.
- The shared [boundary helper](../../.agents/skills/shortform-production/scripts/audio_boundaries.py) and [audio contract](../../.agents/skills/shortform-production/references/audio-boundaries.md) prevent recurrence. Sound-design preflight rejects stale narration/timing, active narration at a cut or an inconsistent HTML scene map. Four historical audio preparation entry points now use the shared repair.

## Verification

All six pinned HyperFrames projects passed full checks and visual scene/seam review. Audio-only normalization refreshes reused the unchanged visual checks and reran acoustic preflight and actual encoded-mix checks, as recorded in each receipt. Full MP4 decode, source/export offset matching, exact frame counts, caption coverage and source-cache preservation passed. Eighteen regression tests pass: seven boundary tests and eleven existing narration/cache tests. All 104 current-package/verification local links resolve. Pipeline previews were stopped and their recorded PIDs no longer owned listening ports.

The [machine-readable results](revision-results.json) contain final export hashes and per-episode measurements. [Original diagnosis](REPORT.md) and source/export excerpts are retained separately.

Perceptual listening was not performed. These checks establish acoustic/encoded timing and preserved speech, not human approval of prosody or mix balance. External v1 drafts, scheduled posts and published posts were not replaced or reposted; the corrected v2 delivery is local.
