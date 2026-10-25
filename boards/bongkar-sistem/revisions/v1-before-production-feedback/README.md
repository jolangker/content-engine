# Bongkar Sistem

A reusable Indonesian short-form identity: build a system through successive problems and solutions, with a recurring overconfident builder and situational visual comedy. Nominal duration is 90 seconds; simpler topics may finish in 60–75 seconds.

Start with [style-board.png](style-board.png), [DIRECTION.md](DIRECTION.md), and [EDITORIAL.md](EDITORIAL.md). Status: awaiting review of the new v1 package. The earlier concept selection is not approval of these new images.

## Package

- [Editable style board](style-board.html), [PDF](style-board.pdf).
- [World study](study-01.png), [section study](study-02.png), [comedy study](study-03.png).
- [Character direction](character-direction.png).
- [Visual specification](frame.md), [motion/audio direction](MOTION-AND-AUDIO.md).
- [Reference study](REFERENCE-STUDY.md), [provenance](assets/SOURCES.md), [verification](VERIFICATION.md).

## Rebuild the static board

The local environment used Blender 5.1.2 and existing Puppeteer/Chromium. No preview server is needed. Commands below assume the repository root and Blender on PATH; the script can also be passed to the installed Blender executable by absolute path.

```powershell
blender --background --factory-startup --python boards/bongkar-sistem/build-scenes.py -- rail section comedy cast
node boards/bongkar-sistem/export-board.cjs
```

Scene selection is optional; omit arguments to render all four, or supply `rail`, `section`, `comedy`, or `cast`. Random geometry uses a fixed seed at process start; changing the selected render sequence can change decorative pebble placement. The delivered final section/cast were refined with the `section cast` selection after rendering all scenes. The scene script, editable `.blend` files, and final PNGs remain available for future work. Still rendering does not validate future animation.

The exporter creates the board PNG/PDF, native frame PNGs, phone checks, character strip, and JSON layout report. It uses local files and always closes its helper browser. When authoring or changing the optional PDF, follow the installed PDF skill's operation marker and visual verification workflow. Re-render the PDF for inspection after layout changes; do not infer PDF pagination from the HTML image.
