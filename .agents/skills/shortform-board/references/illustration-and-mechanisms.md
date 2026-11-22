# Procedural Mark-Making & Mechanism Cutaways

Read when developing an illustrative 2D/2.5D board in `shortform-board` or building organic illustrations and mechanical cutaways in `shortform-production`. Pair with [`assets/procedural-kit/mark-making.js`](../assets/procedural-kit/mark-making.js) (`window.MarkKit`) for frame-seek deterministic rendering in Canvas 2D or inline SVG.

## 1. A style is a way of making marks, not a palette swap

Before writing drawing code for a new board, define its **physical hand** across four axes so the artwork never collapses into generic flat SVG rectangles and ellipses:

| Hand | Edge & nib character | Tone & surface logic | Order of marks (for self-drawing reveals) |
| --- | --- | --- | --- |
| **Pencil & Watercolour** | Tapered graphite line (`wobble: 1.2`, `pressure: 0.25`) over soft edges | Translucent washes (`buildWatercolorWash`, `shrink: 1.5`) that miss the line slightly; pigment rim | 1. Light construction line -> 2. Light-to-dark washes -> 3. Crisp accent graphite |
| **Ink & Line-Wash** | Flexible nib (`pressure: 0.45`, thick on shade side, open where light hits) | Wet wash laid first, pooling along bottom edges | 1. Broad wet wash -> 2. Tapered contour ink -> 3. Callout labels |
| **Ballpoint / Technical Sketch** | Near-constant fine line (`taper: 0.08`, `width: 2.2`) | Tone strictly from directional hatching (`buildAnchoredHatchLines`: single, cross, 3rd pass) | 1. Axis/datum rules -> 2. Outer silhouette -> 3. Shade hatching |
| **Chalkboard / Slate** | Dry broken stroke over dark ground (`#1B2420`) with dust flecks | Lit faces worked twice; ghost erasures of prior states | 1. Faint chalk diagram -> 2. Heavy lit strokes -> 3. Accent chalk |
| **Cut-Paper Collage** | Zero drawn outlines; crisp scissor polygons or fibrous torn edges | Soft drop shadow per layer (`dy: 4..10px`) establishing physical stack order | Layer-by-layer placement from ground sky/table up to focal token |
| **Risograph Print** | Halftone dot screens at distinct angles per ink drum; slight `1.5–3px` registration offset | Multiply/overprint blending where two drums overlap; bare cream paper = white | 1. Base drum -> 2. Secondary drum -> 3. Key/accent ink drum |
| **2.5D Shaded Cutaway** (*Di Balik Benda*) | Clean silhouette contour + internal crease hairlines; split housings | 4-value directional planes (lit top, mid face, shadow wall, recessed cavity) + metal/fluid specular | 1. Stationary housing back -> 2. Moving subassembly -> 3. Front cutaway rim & callout |

## 2. Self-drawing reveals beat opacity fades

- **Grow strokes along their centreline:** Use `MarkKit.svgTaperedPath(pts, { progress })` or `MarkKit.drawTaperedStroke(ctx, pts, { progress })` instead of `opacity: 0 -> 1` when introducing paths, routes, siphon tubes, or callout leaders.
- **Anchor texture to the part, never to the viewport:** Pass the part's local coordinates (or `anchorX`, `anchorY`) into `buildAnchoredHatchLines` and `fbm2D` with a stable per-part integer `seed`. A still part never shimmers unless intentional line-boil on twos (`boilStep: Math.floor(t * 12)`) is part of the board's identity, and a moving lever carries its shading with it.
- **Closed-form springs for seek safety:** Drive physical overshoot (detent snaps, valve seating, lid drops) with `MarkKit.springAtTime(localT, { zeta: 0.8, omega: 16, from, to })` so arbitrary forward/backward HyperFrames frame seeks produce bit-identical poses.

## 3. Building honest machines & cutaways (`machines` workflow)

When staging mechanisms, backyard builds, or physical systems:

1. **Inventory from the ground up before geometry:** List (a) the ground/bench/vessel it rests on, (b) the stationary frame/housing that carries load, (c) the input actuator a hand touches, (d) the internal transmission/flow path, and (e) the **one hero part** that carries the story (it alone receives the active accent color). Nothing floats in mid-air without a mount, shaft, boss, or fluid surface.
2. **Split wrapping parts into three depth layers:** Any cylinder, tank, or casing that encloses an inner mechanism must be drawn in three explicit layers: `housing-back` (darkest interior cavity) -> `active-mechanism` (spring, pawl, piston, roots, water column) -> `housing-front-cutaway` (cut rim and foreground lip). Never paste an internal gear flat on top of an uncut exterior box.
3. **One kinematic state function drives everything:** Compute coupled part transforms from one shared state variable `state(t)` (e.g., `drumAngle(t)` drives blade extension, spring coil tension, and tooth deflection together; `waterLevel(t)` drives float height, valve angle, and outlet stream together) so teeth never interpenetrate and readouts never drift from geometry.
4. **Exploded views follow assembly order:** Use `MarkKit.explodeShareAt(index, count, progress, mode)` along true axial vectors—outer covers and fasteners travel farthest and leave first, then return home last (*last-out, first-home*).
5. **Crop-check every contact joint at phone width:** Inspect shaft bosses, pawl-ratchet teeth, valve seats, and pipe outlets at `360–384 px` width to confirm zero z-order inversions, zero floating gaps at contact moments, and `>= 60 px` clearance above the caption band.
