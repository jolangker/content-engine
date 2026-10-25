# Asset provenance

## Original visual assets

`renders/world-rail.png`, `renders/section-house.png`, `renders/comedy-visitor.png`, and `renders/character-poses.png` are original static procedural 3D renders created for this board. Their editable geometry is preserved in the matching `.blend` files and rebuilt by `../build-scenes.py`. No external photo, texture image, character model, logo, or generated bitmap was used. Soil uses a procedural shader; all geometry is authored in the script.

The files are design studies. Rail geometry, the house air route, thermal-color markers, the builder, and oversized mosquito travellers are illustrative; they are not engineering or biological evidence. Contact sheets under `reference-studies/` are analysis derivatives of the user's supplied videos, not reusable stock or public-facing production assets.

## Fonts

Barlow Regular 400, Bold 700, and Black 900 were downloaded from the Google Fonts source repository on 2026-10-25. Original license: `Barlow-OFL.txt`.

- https://raw.githubusercontent.com/google/fonts/main/ofl/barlow/Barlow-Regular.ttf
- https://raw.githubusercontent.com/google/fonts/main/ofl/barlow/Barlow-Bold.ttf
- https://raw.githubusercontent.com/google/fonts/main/ofl/barlow/Barlow-Black.ttf
- https://raw.githubusercontent.com/google/fonts/main/ofl/barlow/OFL.txt

IBM Plex Mono Regular 400 and its original license were reused from the existing `boards/di-balik-benda/assets/` package. Original source recorded there:

- https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/IBMPlexMono-Regular.ttf
- https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/OFL.txt

Exact asset hashes and retrieval/reuse paths are in [font-manifest.json](font-manifest.json). All fonts load locally; the style board requires no network request.

## Tools and documentation

Static scenes: Blender 5.1.2, Cycles, 24 samples with denoising. Board layout: editable HTML/CSS. Exports: local Chromium through Puppeteer. Neither a HyperFrames project nor an animation render was initialized.

The current Blender Python API was consulted via Context7 (`/websites/blender_api_current`) for background rendering and scene/image settings. Primary documentation: https://docs.blender.org/api/current/bpy.types.Scene.html and https://docs.blender.org/api/current/bpy.types.ImageFormatSettings.html . The installed application's runtime verified the actual scene and render APIs used here. `use_nodes` raises a future-removal deprecation notice on this Blender version; it does not fail rendering.
