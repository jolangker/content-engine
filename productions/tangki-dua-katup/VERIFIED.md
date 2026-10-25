# Verified export v1

- Board: Di Balik Benda v4; original layered 2.5D SVG, Indonesian, 16 explanatory shots.
- Export: [MP4](exports/tangki-dua-katup-v1.mp4), 90.0 seconds, 1080×1920,30fps,2700 frames,H.264/AAC,16,237,215 bytes.
- SHA-256: `5632b1f013288fb6fa2136d3e997791e5d1fa067e8b0b2089381a9b5b0560e6d`.
- Captions: burned in plus [SRT](exports/tangki-dua-katup.srt) and [VTT](exports/tangki-dua-katup.vtt);167 aligned spoken words, no delivery tags.
- Full file decoding passed; measured loudness -15.26 LUFS and true peak -1.82 dBTP. Six narration waveform windows passed.
- All31 placed SFX verified in actual MP4 with waveform matching, including expected onsets; sources and treatment in video/SFX_SOURCES.md.
- Framework check: zero errors and warnings in lint,runtime,layout,motion,contrast and craft. Informational cropped SVG bounds are intentional macro framing.
- Motion:1,616 samples across16 scenes, constant illustrative chain length and reverse-seek consistency passed. Representative final rendered frames inspected for every scene plus contact macros.
- Static storyboard: [HTML](video/boards/storyboard.html) and [PNG](video/boards/storyboard.png),16 ordered frames,1920×4035. Original pre-audio planning timing is retained; final measured timing is in video/timing.json and STORYBOARD.md. Repaired topology and moving-label anchors are included in both storyboard and film.
- Preview: pipeline-owned server PID28056,port3002,HTTP200 verified while held for render; stopped after export verification and listener release verified.
- Authorization: explicit --automation delegates agent verification and final render. Human approval is false. Endpoint --until=export reached; no content package,hosting or publication executed.

## Evidence and limits

Source map: [SOURCES.md](SOURCES.md). Functional generic lever/flapper/cup-float tank; internal fill-valve diaphragm and bowl siphon are outside scope. Refill/drain overlap preserved. Refill and fault overflow join below the closed outlet seal. Fixed-length chain is an illustrative quadratic,not a catenary simulation. Observation timing is slowed/compressed and labeled.

Direct perceptual listening and phone-speaker review were unavailable. Technical audio presence,alignment and levels passed; no subjective full-speed listening approval is claimed. Original full-script recording retained at native speed and pitch;10.48seconds of observation pauses added between phrases to support the90-second mechanism breakdown.
