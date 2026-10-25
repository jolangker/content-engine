# Bongkar Sistem - v2

A reusable Indonesian short-form identity: build a system through successive problems and solutions, with situational comedy from an overconfident builder. V2 responds to the user's generation test with full-screen environment, semi-realistic materials/proportions, clearer interactions, faster progression, in-shot camera motion and discrete SFX.

Default 90 seconds; typically 75-95; strictly above 60. Roughly 20-26 meaningful visual steps is the initial 90-second planning target. Status: v2 package under review, no human approval claimed.

## Start here

- [Visual board](style-board.png), [editable HTML](style-board.html), [PDF](style-board.pdf).
- [Direction and scope](DIRECTION.md), [feedback response](FEEDBACK-v2.md).
- [Editorial](EDITORIAL.md), [visual tokens](frame.md), [motion/audio](MOTION-AND-AUDIO.md).
- [Production standards](PRODUCTION-STANDARDS.md), [SFX event matrix](SFX-PLAN.md).
- [Interaction strip](interaction-direction.png), [verification](VERIFICATION.md).

The three 1080 x 1920 studies and 360 x 640 phone checks are independent identity samples. Action poses and camera plans are static, not moving/audible proof. Existing production hujan-bukan-sekadar-ember and its audio/export retain v1. The complete prior board is [archived here](revisions/v1-before-production-feedback/).

## Rebuild static assets

Use Blender 5.1.2 and the existing local Puppeteer/Chromium setup. No HTTP server or HyperFrames initialization is required.

```powershell
blender --background --factory-startup --python boards/bongkar-sistem/build-scenes-v2.py -- wide contact overhead before touch after
node boards/bongkar-sistem/export-board.cjs
```

To reuse the saved full setting instead of rebuilding its geometry:

```powershell
blender --background --factory-startup --python boards/bongkar-sistem/build-scenes-v2.py -- --reuse contact overhead before touch after
```

The script uses a fixed random seed and reuses the same world across camera poses. Its `.blend` assets and PNGs are under `assets/renders-v2/`. The legacy build-scenes.py and assets/renders/ refer to v1; they are not the v2 source. Follow the installed PDF skill's operation marker before authoring/exporting an optional PDF, then render/inspect its final pagination.
