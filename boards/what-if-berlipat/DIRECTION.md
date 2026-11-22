# What If It Doubled

Working name: What If Berlipat. Revision 1. Editorial v1 and visual v1 approved by the user on 2026-11-22, after seeing the style board and the combined motion preview.

## Brief

Given by the user on 2026-11-22. One everyday object doubles in number every day, visualised until it is absurd. English first for a global and US audience, Indonesian as an optional second upload. Monetised on YouTube Shorts and Facebook Reels, TikTok for reach. 20 to 40 seconds, never under 10. The viewer should want to share it ("look at this") rather than comment.

Fixed by the brief: on-screen question in the first two seconds; Day 1 with one object and a counter; slow pull-back while the count accelerates through room, house and city; one globally known comparator per scale jump; a one-line deadpan payoff; last frame loops into the first; low-poly 3D, flat colour, one main object, no faces; large text readable without sound; no narration or a single flat payoff voice, a sound effect per scale jump, thin music; a new premise, real arithmetic with saved sources, and different scenes and comparators every episode; no "part 2".

## Approved direction

A toy diorama on a seamless single-hue sweep. The object carries the only other colour. Exact counts in condensed white numerals; a paper day chip; comparator tags with real measures; one unbroken pull-back through every scale a single scene can hold; a hero-colour iris that hides the cut only at a big jump (city, country, planet); a fast rewind that closes the loop.

- [Editorial framework v1](EDITORIAL.md)
- [Visual specification v1](frame.md)
- [Style board source](style-board.html) and [PNG](style-board.png)
- [Motion preview MP4](motion-preview.mp4) and its [editable project](motion-preview/index.html)
- [Study source](studies/studies.html) with four rendered stills in `studies/`
- [Scene kit](assets/scene/diorama.js), [counter helpers](assets/scene/counter.js), [type styles](assets/scene/type.css)
- [Voice configuration](AUDIO.json): no voice selected. [Publishing accounts](ACCOUNTS.json): none configured.

## Decisions

Accepted by the user on 2026-11-22:

- The look: flat single-hue worlds, hero-coloured object, Archivo with condensed numerals.
- No narration. Sound effects are dense and carry the film ("tanpa narasi namun kaya sfx").
- The Indonesian version is made only on request.
- Publishing accounts: the user will supply them later. `ACCOUNTS.json` stays empty until then.

- Scale changes: the camera pulls back without a cover for as long as it can, and the screen is covered by the object's colour only for big jumps such as a city or the planet. The user first asked to see the uncovered version ("kamera mundur terus tanpa ditutup, saya mau lihat versi itu dulu"), was shown it beside the iris version with the note that it was only proven from plate to bedroom, and then chose the combination ("mundur terus selama masih bisa, ditutup hanya untuk lompatan besar (kota, bumi)").
- Loop: left to the agent ("terserah Devin"). The fast rewind is kept: it runs the same camera path backwards, so the loop adds no cut.

The seven-rung scale ladder was not commented on.

## Provenance

No reference video was supplied; the direction comes from the written brief. Geometry, studies and motion are original and built in code. Archivo variable font: The Archivo Project Authors, SIL OFL 1.1 (`assets/fonts/`). Three.js r187, MIT (`assets/vendor/`). Globe land mask rasterised from Natural Earth 1:110m land polygons, public domain (`assets/scene/landmask.js`).

Sample figures are illustrative and unverified. They were derived from rough per-object sizes to keep the samples plausible: about 2.75e-8 m3 of loose rice per grain, a 4 x 4 x 2.5 m bedroom, a 16 mm die, a 93 m Statue of Liberty. A production must source and recompute its own.

## Rendered review

Inspected on 2026-11-22.

- **Style board**, 1440 x 3697. Checked at board scale and in zoomed crops: Archivo loads in both widths, no overflow, palette values match `frame.md`.
- **Studies**, 1080 x 1920 each: hook (cobalt, one grain), house (plum, tennis balls), landmark (pine, dice beside the statue), payoff (cobalt, globe). Silhouettes, value separation and contact shadows read at phone size. Tags were moved so they do not collide and stay in the safe area.
- **Motion preview**, 14.3 s, 1080 x 1920, 30 fps, silent. Hook hold; day ticks with exact counts; one unbroken pull-back in which grains become a heap on the plate, the heap spills off the table around Day 23, the floor fills and rice heaps over the bedroom walls by Day 32 (camera distance 0.2 m to 30 m on one eased path, one scene); the bedroom tag; a hero iris under which the days race from 32 to 69 and the scene cuts to the planet; the Earth tag; the payoff; the rewind. Decoded frames were inspected across the full clip. First and last frames match (PSNR 51.6 dB).
- `hyperframes check` passes with no errors. Remaining warnings are intended: the returning question is on screen briefly because it is the loop point; the canvas sits inside the root frame; the software renderer lacks one WebGL extension.
- Two earlier previews were shown to the user and are superseded by this one: a 10 s version with an iris between plate and bedroom, and a 12 s pull-back-only version.

Known limits:

- The preview is a 14 s study of the grammar. It shows three scales and two comparators, and jumps from a bedroom straight to the planet; an episode runs 20 to 40 s over four or five scales.
- On Day 1 a single grain of rice is small in frame and the plate reads weakly until the camera pulls back. A larger first object will not have this problem; for small objects the opening may need a tighter macro or a lighter plate.
- The unbroken pull-back is proven from plate to bedroom, a 150x change in camera distance inside one scene. Carrying it on through a building or a landmark needs the larger scene to contain the smaller one; that is not built or tested. Where it cannot be done, the iris is the fallback.
- City, country and partial-coverage planet scales have scene primitives (`buildBlockCube`, `buildGlobe`) but no city or country study yet.
- Audio is written direction only. No sound has been produced or tested, and the motion preview is silent.
- The Indonesian text variant has not been laid out; it is made on request only.

The HyperFrames renderer does not follow a symlink out of the project folder, so `motion-preview/assets/` is a copy of `assets/`. `export-board.cjs` refreshes that copy; run it before rendering the preview. No preview server is left running.

## Open items

- Publishing accounts: the user will supply them. `ACCOUNTS.json` is empty.
- Audio is direction only; no sound has been produced or heard.
- The scale ladder and the sample copy were not commented on individually; they were approved as part of the package.

## Next action

None for the board. Add accounts to `ACCOUNTS.json` when the user supplies them. A specific episode is a separate request handled by `shortform-production`.
