---
name: Dua Dunia
version: 1
status: approved
colors:
  navyHud: "#1C3A4A"
  navyStroke: "#142A36"
  creamText: "#FFFDF5"
  accentYellow: "#FAD668"
  worldCleanGreen: "#78A55E"
  worldCompareAmber: "#E8A838"
  skyTop: "#3B88C3"
  skyLow: "#78AFD8"
  asphalt: "#56595B"
  sidewalk: "#B8BDC0"
  warmFacade: "#CAA584"
  capsuleOrange: "#E67E35"
  capsuleTeal: "#3A9D8F"
  capsulePlum: "#7A5BA8"
typography:
  headline: { fontFamily: Fredoka, fontWeight: 700, fontSize: 84px }
  panelLabel: { fontFamily: Fredoka, fontWeight: 700, fontSize: 48px }
  hudTitle: { fontFamily: Fredoka, fontWeight: 600, fontSize: 38px }
  caption: { fontFamily: Fredoka, fontWeight: 700, fontSize: 56px }
  disclaimer: { fontFamily: Fredoka, fontWeight: 600, fontSize: 26px }
spacing:
  frame: 1080x1920
  splitDividerY: 960px
  disclaimerY: 78px
  captionCenterY: 1475px
  captionRegion: [54, 1380, 972, 200]
  textStroke: 10px
---

# Dua Dunia — visual specification v1

Reusable 3D diorama kit and sample scenes live in [assets/kit-3d.js](assets/kit-3d.js) and [studies/studies.html](studies/studies.html).

## 3D treatment

### Form
- **Hybrid diorama:** Urban environments, buildings, vehicles, street furniture, and trees use **Polyfork** free low-poly GLB assets (`nyc-city-kit-fbca88` or topic-matched Polyfork kits, real-metre scale `size_m`, placed at `y = 0`, never rescaled arbitrarily).
- **Per-episode Polyfork sourcing (anti-bias rule):** The 6 models bundled in `boards/dua-dunia/assets/models/` are only a baseline street starter kit, **not** the full asset pool. Before building scenes for any new production, the agent must map every topic-specific hero location or prop (e.g., factory, hospital, school, office, market, construction site, farm, train, port) and **query the Polyfork MCP (`list_kits` / `search_assets`)** to download topic-matched `.glb` assets locally into `productions/<slug>/video/assets/models/` (or promote broadly reusable models into `boards/dua-dunia/assets/models/`). Do not recycle only the 6 starter street models when a beat depicts a non-street location or mechanism.
- **Procedural capsule characters:** Citizens, workers, and officials are built procedurally in Three.js as clean toy-capsule figures (~1.75 m tall: spherical head, dot eyes, readable curved smile/frown, cap hair, capsule torso/limbs, optional signature prop like sunglasses, tie, or hardhat) so facial emotion and group mood read instantaneously at phone scale. Standing characters keep feet planted on the ground with subtle breathing/head/arm idle motion (no artificial vertical bouncing); walking sidewalk NPCs use alternating leg/arm stride cycles.
- **Diegetic plaques:** Key institutions (`HALTE BUS`, `LOKET`, `PABRIK`, `SEKOLAH`) are labeled inside the 3D scene using crisp navy or green double-bordered rectangular plaques with cream Fredoka lettering.

### Materials
- Matte, low-sheen surfaces (`roughness: 0.78–0.92`, `metalness: 0.0–0.08`) so Polyfork architecture and procedural capsule characters share one unified tabletop-miniature feel.
- Keep neutral architectural midtones (`#56595B` asphalt, `#B8BDC0` concrete, `#CAA584` warm brick/plaster) so colored vehicles, capsule outfits, and HUD data accents (`#78A55E` World A, `#E8A838` World B, `#FAD668` active highlight) pop cleanly.

### Light and depth
- Clean daytime sky (`#3B88C3` → `#78AFD8`) with soft directional sun key (`intensity: 1.55`), warm-cool hemisphere fill (`#D9EEFF` sky / `#7E7B74` ground, `intensity: 1.1`), and soft contact/cast shadows.
- **Tone mapping rule (Polyfork compatibility):** Use `THREE.NoToneMapping` (or `THREE.LinearToneMapping`) with `SRGBColorSpace` output; **never use ACESFilmicToneMapping at exposure 1.0**, which darkens Polyfork palettes by ~30%.

### Camera and movement
- **Single-world street level:** Perspective camera (`fov: 38°–42°`) at human or slightly elevated miniature eye level (`y = 2.2–4.5 m`) with gentle continuous drift, slow dolly, or moving vehicles/figures so the frame stays alive (`first_motion <= 0.5s`, `max_static <= 1.5s`, `held_share <= 10%`).
- **Aerial twin-world split-screen:** Elevated 40°–50° isometric-like perspective (`fov: 34°`) looking down over matching city grids in top and bottom 960 px viewports.
- **Deterministic clock:** All camera paths, vehicle loops, character bobbing/walking, and HUD reveals derive strictly from explicit HyperFrames time `t` (no `requestAnimationFrame` drift).

### Finishing and annotations
- No heavy bloom, lens flares, or motion blur. Clarity at phone width (`390 px` CSS) takes priority.
- **Split-screen spotlight:** When narration focuses on one world in a 50/50 split, apply a subtle dark scrim (`rgba(15, 28, 38, 0.42)`) over the inactive half so focus locks immediately.

## Composition and split-screen

- Canvas: `1080 x 1920`, `30 fps` (delivery standard; reference was `24 fps`).
- **Persistent epistemic chrome:** Top-center subtle disclaimer (`Eksperimen pikiran. Angka dari model.`) at `y = 78px` in `26px` Fredoka SemiBold white with navy outline.
- **50/50 horizontal split:** Divider line (`6px` solid `#142A36`) at `y = 960px`. World A label (`top-left`, `y = 140px`) and World B label (`bottom-half top-left`, `y = 1005px`).
- **Center control pill:** When locking shared starting conditions or timestamps (`10.000 warga`, `Bulan 12`, `Tahun 10`), place a dark-navy rounded pill (`#1C3A4A`, cream text, thin cream/slate border) straddling the `y = 960px` divider.

## HUD and data cards

- Dark slate-navy rounded cards (`background: rgba(28, 58, 74, 0.94)`, `border: 3px solid rgba(255, 253, 245, 0.16)`, `border-radius: 28px`) composited over a dimmed/blurred 3D city backdrop.
- **Crossover line chart:** World A in `#78A55E` (clean green), World B in `#E8A838` (compare amber), crisp white node + dashed vertical marker at the inflection point, bold floating callout (`Nyalip!`) above the card.
- **100-world robustness grid:** 10×10 rounded square tiles inside a dark-navy frame; highlighted majority tiles carry `#FAD668` yellow borders against muted slate-teal minority tiles, with a summary line directly beneath.

## Typography and captions

- Single family across all chrome: **Fredoka** (variable weight `400–700`, SIL OFL 1.1, bundled at `assets/fonts/Fredoka-Variable.ttf`).
- All floating titles, scenario labels, and captions use `#FFFDF5` fill with a thick `#142A36` outer stroke (`paint-order: stroke fill`, `8–12px`) and subtle drop shadow for legibility over bright sky or busy streets.
- **Caption band:** Fixed lower-third zone `[54, 1380, 972, 200]` (centered at `y = 1475px`, ~77% height). Short 1-line clauses (3–6 words) with active spoken word highlighted in `#FAD668`. Keep critical 3D faces, plaques, and chart axes outside this band.

## Motion

- **First motion:** `<= 0.5 s` (reference: `0.20 s`). Vehicles glide, characters bob/gesture, or camera drifts from frame 0.
- **Max static hold:** `<= 1.5 s` (reference: `1.00 s`, `held_share: 1.0%`).
- **Cuts:** Clause-aligned hard cuts (avg `2.8–4.5 s` per shot); reserve brief smooth fades/wipes (`0.2–0.4 s`) for time-skip transitions or HUD card entrances.
- **HUD entrances:** Crisp `0.25–0.35 s` scale-pop (`back.out(1.4)`) for headlines, control pills, and chart nodes; progressive path draw for crossover curves.

## Audio

- **Voice-led:** Conversational, expressive Indonesian male narrator (~2.1–2.7 words/sec; reference: `2.39 wps`), mixed around `-14 LUFS` (`true_peak <= -0.5 dBTP`).
- **BGM:** Continuous lighthearted acoustic-guitar + mallet/xylophone instrumental bed (~110–116 BPM) sitting `24–30 dB` below voice (reference: `-28.96 dB` margin, ~2 dB gentle ducking under speech).
- **SFX:** Optional and very sparse; the format relies on vocal inflection and visual contrast rather than constant pop/whoosh hits.

## Assets & Provenance

- **Font:** `assets/fonts/Fredoka-Variable.ttf` (Google Fonts, SIL OFL 1.1, `assets/fonts/OFL.txt`).
- **3D Models (Polyfork `nyc-city-kit-fbca88`, CC BY 4.0):**
  - `assets/models/city-bus-49fd97.glb` — City Bus by Polyfork (https://polyfork.dev/asset/city-bus-49fd97), CC BY 4.0
  - `assets/models/compact-hatchback-386417.glb` — Compact Hatchback by Polyfork (https://polyfork.dev/asset/compact-hatchback-386417), CC BY 4.0
  - `assets/models/town-car-56eeb6.glb` — Town Car by Polyfork (https://polyfork.dev/asset/town-car-56eeb6), CC BY 4.0
  - `assets/models/one-storey-shop-row-83c958.glb` — One-Storey Shop Row by Polyfork (https://polyfork.dev/asset/one-storey-shop-row-83c958), CC BY 4.0
  - `assets/models/brick-tenement-7d2014.glb` — Brick Tenement by Polyfork (https://polyfork.dev/asset/brick-tenement-7d2014), CC BY 4.0
  - `assets/models/street-tree-0d33f3.glb` — Street Tree by Polyfork (https://polyfork.dev/asset/street-tree-0d33f3), CC BY 4.0
- **Runtime:** Three.js r170 ESM (`assets/vendor/three.module.min.js`, `GLTFLoader.js`, `BufferGeometryUtils.js`, MIT License).
