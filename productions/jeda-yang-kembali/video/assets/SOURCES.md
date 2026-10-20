# Asset provenance

- Newsreader regular variable and italic fonts, copied from the approved Ruang di Antara board assets. Original family: https://github.com/google/fonts/tree/main/ofl/newsreader . OFL license included locally.
- DM Sans variable font, copied from the same board. Original family: https://github.com/google/fonts/tree/main/ofl/dmsans . OFL license included locally.
- GSAP 3.14.2 runtime frozen locally from https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js . Used for deterministic timeline motion.
- Narration v2: original single-request ElevenLabs Zephlyn (`3mAVBNEqop5UbHtD8oxQ`), eleven_v4, resolved from project .env; exact tagged input in ../audio_request.json. Native alignment, original MP3 and request/hash receipt are in ../.media/audio/voice/. Reading pauses are derived in a PCM WAV without changing speech samples; source timing and transform are in ../narration_source_meta.json and ../audio_meta.json. The prior Brian source and its metadata remain preserved under ../../revisions/v1/. No human voice recording supplied and no provider switch.
- Abstract actors, paths, layout and graphics are original deterministic CSS/SVG for this episode using the approved board palette. No stock footage, B-roll, external photographs, music, or sound effects used.

- Series chrome: frozen copy of ../../../../boards/ruang-di-antara/components/; canonical tokens in board frame.md, implementation correction 2026-10-20.
- Path reveals: measured SVG stroke tracing adapted from the installed svg-stroke-trace registry component in ../compositions/components/. Local episode geometry, palette and finite timing replace its demonstration appearance; no decorative drift/glow is used.
