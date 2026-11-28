---
format: 1080x1920
duration: 90s
mode: autonomous
flow: automation
storyboard: no
music: none
message: Two valves coordinate one tank cycle
---

# Video direction

Board Di Balik Benda v4. Shaded 2.5D SVG throughout. Orange input, blue active part, teal flow. Camera crops preserve shared landmarks. Timings measured against full narration. Caption keep-out y1600–1800; all meaningful scene content stays above y1580. Agent verification replaces human layout approval. Static storyboard artifacts are mandatory.

Normal chronology includes overlapping drainage and refill. Shots 2–3 are an anatomy reset after opening teaser; shot13 is a labeled alternate inspection of refill, shot14 a labeled fault example, shot15 an explicitly announced replay. Time slowed for inspection and compressed for refill; not a dimensional simulation.

## Frame 1 — Siapa yang menghentikan air? (0.000–5.681s)

- status: animated
- src: compositions/frames/s01.html
- duration: 5.68088s
- transition_in: cut
- scene: Satu siklus otomatis
- voiceover: Sekali tekan, air keluar. Tapi siapa yang tahu kapan tangkinya sudah penuh?
- poster: 3.522s
- blueprint: compose
- focal: shaded 2.5D whole view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Siapa yang menghentikan air?. New information: Satu siklus otomatis.

Scene 1 (0–1.14s): Orient to whole; preserve state and cue the active part. Scene 2 (1.14–4.26s): Input → contact or flow transfer → dependent response, action `tank`. Scene 3 (4.26–5.68s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {"exterior": 1, "lidY": 0}], [0.35, {"exterior": 0.08, "lidY": -58}], [0.7, {"leverAngle": -14, "flapAngle": 48, "flush": 1, "water": 0.8}], [1, {"leverAngle": 0, "flapAngle": 48, "water": 0.65, "flush": 1}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 2 — Buka tangkinya (5.681–11.128s)

- status: animated
- src: compositions/frames/s02.html
- duration: 5.44725s
- transition_in: cut
- scene: Tipe tuas + flapper
- voiceover: Kita buka tangki tipe tuas dan flapper. Ada dua katup dengan tugas berbeda.
- poster: 3.377s
- blueprint: compose
- focal: shaded 2.5D tank view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Buka tangkinya. New information: Tipe tuas + flapper.

Scene 1 (0–1.09s): Orient to tank; preserve state and cue the active part. Scene 2 (1.09–4.09s): Input → contact or flow transfer → dependent response, action `reveal`. Scene 3 (4.09–5.45s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {"exterior": 0.8, "lidY": 0}], [0.45, {"exterior": 0.035, "lidY": -70}], [1, {"exterior": 0.035, "lidY": -70}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 3 — Dua tugas terpisah (11.128–15.652s)

- status: animated
- src: compositions/frames/s03.html
- duration: 4.52396s
- transition_in: cut
- scene: Buang / isi
- voiceover: Yang di bawah membuang air. Yang di samping mengatur air masuk.
- poster: 2.805s
- blueprint: compose
- focal: shaded 2.5D tank view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Dua tugas terpisah. New information: Buang / isi.

Scene 1 (0–0.90s): Orient to tank; preserve state and cue the active part. Scene 2 (0.90–3.39s): Input → contact or flow transfer → dependent response, action `identify`. Scene 3 (3.39–4.52s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {}], [0.45, {}], [1, {}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 4 — Putaran menjadi tarikan (15.652–19.958s)

- status: animated
- src: compositions/frames/s04.html
- duration: 4.30577s
- transition_in: cut
- scene: Putar → tarik
- voiceover: Tekan gagang. Tuas berputar, menarik rantai ke atas.
- poster: 2.670s
- blueprint: compose
- focal: shaded 2.5D lever view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Putaran menjadi tarikan. New information: Putar → tarik.

Scene 1 (0–0.86s): Orient to lever; preserve state and cue the active part. Scene 2 (0.86–3.23s): Input → contact or flow transfer → dependent response, action `lever`. Scene 3 (3.23–4.31s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {}], [0.2, {}], [0.65, {"leverAngle": -5, "flapAngle": 13}], [1, {"leverAngle": -5, "flapAngle": 13}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 5 — Jalur buang terbuka (19.958–25.455s)

- status: animated
- src: compositions/frames/s05.html
- duration: 5.49694s
- transition_in: cut
- scene: Flapper terangkat
- voiceover: Rantai mengangkat flapper dari dudukannya. Jalur menuju mangkuk terbuka.
- poster: 3.408s
- blueprint: compose
- focal: shaded 2.5D flapper view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Jalur buang terbuka. New information: Flapper terangkat.

Scene 1 (0–1.10s): Orient to flapper; preserve state and cue the active part. Scene 2 (1.10–4.12s): Input → contact or flow transfer → dependent response, action `open`. Scene 3 (4.12–5.50s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {"leverAngle": -5, "flapAngle": 13}], [0.2, {"leverAngle": -5, "flapAngle": 13}], [0.66, {"leverAngle": -14, "flapAngle": 48, "flush": 1}], [1, {"leverAngle": -14, "flapAngle": 48, "flush": 1, "water": 0.97}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 6 — Gravitasi bekerja (25.455–30.508s)

- status: animated
- src: compositions/frames/s06.html
- duration: 5.05369s
- transition_in: cut
- scene: Air mengalir turun
- voiceover: Air tangki turun karena gravitasi. Gagangnya tidak memompa air.
- poster: 3.133s
- blueprint: compose
- focal: shaded 2.5D tank view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Gravitasi bekerja. New information: Air mengalir turun.

Scene 1 (0–1.01s): Orient to tank; preserve state and cue the active part. Scene 2 (1.01–3.79s): Input → contact or flow transfer → dependent response, action `drain`. Scene 3 (3.79–5.05s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {"leverAngle": -14, "flapAngle": 48, "flush": 1, "water": 0.97}], [0.85, {"leverAngle": -14, "flapAngle": 48, "flush": 1, "water": 0.7}], [1, {"leverAngle": -14, "flapAngle": 48, "flush": 1, "water": 0.7}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 7 — Tetap terbuka sesaat (30.508–35.733s)

- status: animated
- src: compositions/frames/s07.html
- duration: 5.22402s
- transition_in: cut
- scene: Dibantu daya apung
- voiceover: Gagang dilepas. Daya apung membantu flapper tetap terbuka sesaat.
- poster: 3.239s
- blueprint: compose
- focal: shaded 2.5D flapper view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Tetap terbuka sesaat. New information: Dibantu daya apung.

Scene 1 (0–1.04s): Orient to flapper; preserve state and cue the active part. Scene 2 (1.04–3.92s): Input → contact or flow transfer → dependent response, action `buoyancy`. Scene 3 (3.92–5.22s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {"leverAngle": -14, "flapAngle": 48, "flush": 1, "water": 0.7}], [0.3, {"leverAngle": 0, "flapAngle": 48, "flush": 1, "water": 0.67}], [1, {"flapAngle": 48, "flush": 1, "water": 0.5}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 8 — Pelampung ikut turun (35.733–41.002s)

- status: animated
- src: compositions/frames/s08.html
- duration: 5.26960s
- transition_in: cut
- scene: Turun → mulai isi
- voiceover: Air turun, pelampung ikut merosot. Katup pengisi mulai membuka.
- poster: 3.267s
- blueprint: compose
- focal: shaded 2.5D float view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Pelampung ikut turun. New information: Turun → mulai isi.

Scene 1 (0–1.05s): Orient to float; preserve state and cue the active part. Scene 2 (1.05–3.95s): Input → contact or flow transfer → dependent response, action `floatdown`. Scene 3 (3.95–5.27s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {"flapAngle": 48, "flush": 1, "water": 0.5}], [0.65, {"flapAngle": 48, "flush": 1, "fill": 1, "refill": 1, "water": 0.28}], [1, {"flapAngle": 48, "flush": 1, "fill": 1, "refill": 1, "water": 0.22}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 9 — Buang dan isi bertumpang tindih (41.002–44.980s)

- status: animated
- src: compositions/frames/s09.html
- duration: 3.97767s
- transition_in: cut
- scene: Dua aliran bersamaan
- voiceover: Jadi, pengisian bisa dimulai saat air lama masih keluar.
- poster: 2.466s
- blueprint: compose
- focal: shaded 2.5D tank view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Buang dan isi bertumpang tindih. New information: Dua aliran bersamaan.

Scene 1 (0–0.80s): Orient to tank; preserve state and cue the active part. Scene 2 (0.80–2.98s): Input → contact or flow transfer → dependent response, action `overlap`. Scene 3 (2.98–3.98s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {"flapAngle": 48, "flush": 1, "fill": 1, "refill": 1, "water": 0.22}], [0.85, {"flapAngle": 35, "flush": 1, "fill": 1, "refill": 1, "water": 0.08}], [1, {"flapAngle": 35, "flush": 1, "fill": 1, "refill": 1, "water": 0.08}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 10 — Karet kembali menutup (44.980–51.678s)

- status: animated
- src: compositions/frames/s10.html
- duration: 6.69856s
- transition_in: cut
- scene: Kembali ke dudukan
- voiceover: Saat tangki terkuras, flapper turun. Karet bertemu dudukan, menutup jalur buang.
- poster: 4.153s
- blueprint: compose
- focal: shaded 2.5D flapper view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Karet kembali menutup. New information: Kembali ke dudukan.

Scene 1 (0–1.34s): Orient to flapper; preserve state and cue the active part. Scene 2 (1.34–5.02s): Input → contact or flow transfer → dependent response, action `close`. Scene 3 (5.02–6.70s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {"flapAngle": 35, "flush": 1, "fill": 1, "refill": 1, "water": 0.08}], [0.58, {"flapAngle": 0, "flush": 0, "fill": 1, "refill": 1, "water": 0.08}], [1, {"fill": 1, "refill": 1, "water": 0.16}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 11 — Tangki mulai penuh lagi (51.678–56.759s)

- status: animated
- src: compositions/frames/s11.html
- duration: 5.08090s
- transition_in: cut
- scene: Air naik → pelampung naik
- voiceover: Kini air masuk tertampung. Permukaannya naik, membawa pelampung.
- poster: 3.150s
- blueprint: compose
- focal: shaded 2.5D fill view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Tangki mulai penuh lagi. New information: Air naik → pelampung naik.

Scene 1 (0–1.02s): Orient to fill; preserve state and cue the active part. Scene 2 (1.02–3.81s): Input → contact or flow transfer → dependent response, action `rise`. Scene 3 (3.81–5.08s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {"fill": 1, "refill": 1, "water": 0.16}], [0.88, {"fill": 1, "refill": 1, "water": 0.8}], [1, {"fill": 1, "refill": 1, "water": 0.8}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 12 — Batas tercapai, aliran berhenti (56.759–63.045s)

- status: animated
- src: compositions/frames/s12.html
- duration: 6.28544s
- transition_in: cut
- scene: Naik → berhenti isi
- voiceover: Pelampung mengendalikan katup pengisi. Saat batasnya tercapai, air masuk berhenti.
- poster: 3.897s
- blueprint: compose
- focal: shaded 2.5D float view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Batas tercapai, aliran berhenti. New information: Naik → berhenti isi.

Scene 1 (0–1.26s): Orient to float; preserve state and cue the active part. Scene 2 (1.26–4.71s): Input → contact or flow transfer → dependent response, action `stop`. Scene 3 (4.71–6.29s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {"fill": 1, "refill": 1, "water": 0.8}], [0.65, {"fill": 1, "refill": 1, "water": 1}], [0.75, {"water": 1}], [1, {"water": 1}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 13 — Selang kecil punya jalur sendiri (63.045–68.768s)

- status: animated
- src: compositions/frames/s13.html
- duration: 5.72356s
- transition_in: cut
- scene: Selang pengisi mangkuk
- voiceover: Sebagian air pengisi melewati selang kecil menuju pipa limpasan, mengisi kembali mangkuk.
- poster: 3.549s
- blueprint: compose
- focal: shaded 2.5D refill view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Selang kecil punya jalur sendiri. New information: Selang pengisi mangkuk.

Scene 1 (0–1.14s): Orient to refill; preserve state and cue the active part. Scene 2 (1.14–4.29s): Input → contact or flow transfer → dependent response, action `refill`. Scene 3 (4.29–5.72s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {"fill": 1, "refill": 1, "water": 0.6}], [0.15, {"fill": 1, "refill": 1, "water": 0.62}], [0.85, {"fill": 1, "refill": 1, "water": 0.83}], [1, {"fill": 1, "refill": 1, "water": 0.86}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 14 — Jalur untuk kelebihan air (68.768–74.588s)

- status: animated
- src: compositions/frames/s14.html
- duration: 5.81937s
- transition_in: cut
- scene: Jika air terlalu tinggi
- voiceover: Kalau air tangki terlalu tinggi, kelebihannya masuk pipa limpasan. Ini jalur cadangan.
- poster: 3.608s
- blueprint: compose
- focal: shaded 2.5D overflow view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Jalur untuk kelebihan air. New information: Jika air terlalu tinggi.

Scene 1 (0–1.16s): Orient to overflow; preserve state and cue the active part. Scene 2 (1.16–4.36s): Input → contact or flow transfer → dependent response, action `overflow`. Scene 3 (4.36–5.82s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {"fill": 1, "water": 1}], [0.45, {"fill": 1, "water": 1.18}], [0.55, {"fill": 1, "overflow": 1, "water": 1.18}], [1, {"fill": 1, "overflow": 1, "water": 1.18}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 15 — Ikuti satu siklus (74.588–82.509s)

- status: animated
- src: compositions/frames/s15.html
- duration: 7.92171s
- transition_in: cut
- scene: Tekan → buang → isi
- voiceover: Perhatikan siklusnya: tuas menarik, flapper membuka, pelampung turun, lalu tangki mengisi lagi.
- poster: 4.911s
- blueprint: compose
- focal: shaded 2.5D tank view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Ikuti satu siklus. New information: Tekan → buang → isi.

Scene 1 (0–1.58s): Orient to tank; preserve state and cue the active part. Scene 2 (1.58–5.94s): Input → contact or flow transfer → dependent response, action `cycle`. Scene 3 (5.94–7.92s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {}], [0.14, {"leverAngle": -14, "flapAngle": 48, "flush": 1, "water": 0.95}], [0.4, {"flapAngle": 48, "flush": 1, "fill": 1, "refill": 1, "water": 0.1}], [0.54, {"fill": 1, "refill": 1, "water": 0.1}], [0.88, {"fill": 1, "refill": 1, "water": 1}], [0.96, {}], [1, {}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

## Frame 16 — Siap dipakai lagi (82.509–90.000s)

- status: animated
- src: compositions/frames/s16.html
- duration: 7.49069s
- transition_in: cut
- scene: Dua tugas. Satu siklus.
- voiceover: Flapper menahan air. Pelampung mengatur pengisian. Dua tugas, satu tangki siap dipakai lagi.
- poster: 4.644s
- blueprint: compose
- focal: shaded 2.5D whole view of the same cistern
- rules: causal state interpolation, anchored emphasis, svg-path-draw

Purpose: Siap dipakai lagi. New information: Dua tugas. Satu siklus..

Scene 1 (0–1.50s): Orient to whole; preserve state and cue the active part. Scene 2 (1.50–5.62s): Input → contact or flow transfer → dependent response, action `ready`. Scene 3 (5.62–7.49s): Hold and confirm the resulting state; labels follow the mechanical event rather than replacing it.

Diagnostic poses (normalized shot time): `[[0, {}], [0.45, {}], [0.8, {"exterior": 0.55, "lidY": 0}], [1, {"exterior": 0.55, "lidY": 0}]]`. The main cycle preserves state across shots 4–12. Shot 3 intentionally holds a full-tank anatomy view while the two functional parts are emphasized separately; no invented mechanical stage. SFX: map onsets to these same key poses; sustained water cues cover coupled flow, dry editorial cues identify inspection/reveal.

<!-- sound-cues:start -->
## Current sound cues

Authority: [sound_design.json](sound_design.json). BGM: none — Unscored inspection; foreground narration and material/water cues.

| Cue | Scene | Main time (s) | Asset | Gain | Purpose / trigger |
| --- | --- | --- | --- | --- | --- |
| sfx-s01-01 | s01 | 0.000 | section-reveal | 0.7 | Start of selective section reveal |
| sfx-s01-02 | s01 | 2.000 | water-flow | 0.5 | Same shot key-pose flow onset/continuation |
| sfx-s02-03 | s02 | 5.667 | section-reveal | 0.7 | Lid separation and section transparency begin |
| sfx-s03-04 | s03 | 12.033 | chain-contact | 0.26 | First valve emphasis begins |
| sfx-s03-05 | s03 | 13.833 | chain-contact | 0.26 | Second valve emphasis begins |
| sfx-s04-06 | s04 | 16.500 | handle-contact | 0.45 | Press and lever motion begin |
| sfx-s04-07 | s04 | 16.500 | chain-contact | 0.38 | Chain endpoint begins rising |
| sfx-s05-08 | s05 | 21.067 | chain-contact | 0.35 | Further lever/flapper lift begins |
| sfx-s05-09 | s05 | 21.067 | water-flow | 0.45 | Same shot key-pose flow onset/continuation |
| sfx-s06-10 | s06 | 25.467 | water-flow | 0.45 | Same shot key-pose flow onset/continuation |
| sfx-s07-11 | s07 | 30.500 | handle-contact | 0.3 | Lever return begins |
| sfx-s07-12 | s07 | 30.500 | water-flow | 0.45 | Same shot key-pose flow onset/continuation |
| sfx-s08-13 | s08 | 35.733 | water-flow | 0.3 | Same shot key-pose flow onset/continuation |
| sfx-s08-14 | s08 | 35.733 | water-refill | 0.36 | Same shot key-pose flow onset/continuation |
| sfx-s09-15 | s09 | 41.000 | water-flow | 0.4 | Same shot key-pose flow onset/continuation |
| sfx-s09-16 | s09 | 41.000 | water-refill | 0.36 | Same shot key-pose flow onset/continuation |
| sfx-s10-17 | s10 | 44.967 | water-flow | 0.35 | Same shot key-pose flow onset/continuation |
| sfx-s10-18 | s10 | 48.867 | rubber-seat | 0.55 | Flapper reaches zero angle; main flush flow stops |
| sfx-s10-19 | s10 | 44.967 | water-refill | 0.38 | Same shot key-pose flow onset/continuation |
| sfx-s11-20 | s11 | 51.667 | water-refill | 0.44 | Same shot key-pose flow onset/continuation |
| sfx-s12-21 | s12 | 56.767 | water-refill | 0.4 | Same shot key-pose flow onset/continuation |
| sfx-s12-22 | s12 | 61.467 | rubber-seat | 0.3 | Fill/refill opacity reaches zero |
| sfx-s13-23 | s13 | 63.033 | water-refill | 0.45 | Same shot key-pose flow onset/continuation |
| sfx-s14-24 | s14 | 68.767 | water-refill | 0.35 | Same shot key-pose flow onset/continuation |
| sfx-s14-25 | s14 | 71.400 | water-flow | 0.42 | Same shot key-pose flow onset/continuation |
| sfx-s15-26 | s15 | 74.600 | handle-contact | 0.4 | Lever/flapper begin actuating |
| sfx-s15-27 | s15 | 74.600 | water-flow | 0.42 | Same shot key-pose flow onset/continuation |
| sfx-s15-28 | s15 | 75.700 | water-refill | 0.42 | Same shot key-pose flow onset/continuation |
| sfx-s15-29 | s15 | 78.867 | rubber-seat | 0.45 | Flapper reaches its seat |
| sfx-s15-30 | s15 | 82.200 | rubber-seat | 0.28 | Full water level; fill switches off |
| sfx-s16-31 | s16 | 85.867 | section-reveal | 0.65 | Lid/front illustration close |

Intentional silence: Every designed interaction mapped to material accents or sustained water; editorial inspection cues differentiated from literal physical acoustics.
<!-- sound-cues:end -->
