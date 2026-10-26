# Scene build contract

Use inside the existing HyperFrames project and assigned scene. The [format contract](../../hyperframes/references/format.md) owns markup, timing, variables, and media; [motion](../../hyperframes/references/motion.md) and [runtimes](../../hyperframes/references/runtimes.md) own animation. Project style, canvas, scene duration, and audio decisions take precedence over module examples.

## Composition and timing

- Author only the assigned file. A sub-composition is a bare `<template>` containing its styles, markup, and scripts; style its root as `#root` with `width/height: 100%`. Canvas dimensions come from the owning composition.
- Match the host, inner `data-composition-id`, and registered timeline ID. Keep element IDs unique in the assembled project.
- Keep the scene's local clock and its mounted start distinct. Translate narration anchors to local scene times; keep every reveal and final hold inside the assigned duration.
- Build one paused timeline and register it after its tweens are complete. The framework owns clip visibility and media playback; animate inner visual wrappers.
- Preserve entering/ending object identity and the agreed transition handoff. A scene's final readable state is part of its deliverable.

## Layout before animation

Pose the scene at its most informative state using real copy/data, inherited fonts, palette roles, and visual medium. Check hierarchy, caption clearance, phone readability, and intentional overlap before animating. Keep fixed board chrome consistent. A registry example's glow, color, type, card layout, or sound is a customization choice under the accepted direction.

Kinetic display type is a graphics element; the owner's full spoken captions remain on their established caption track.

Choose one primary explanatory action, with coordinated supporting motion where useful. Develop the visual across the assigned window rather than revealing everything immediately or extending a decorative loop.

## Seek-safe implementation

Use explicit start/end states for delayed entrances on inner elements. Preserve deterministic transforms and avoid CSS/GSAP ownership conflicts. Timed DOM elements remain editable with stable IDs; freeze asset files locally.

Counters and charts derive their displayed values and geometry from the timeline. Keep one data source and consistent rounding, clamp held values, and verify start/intermediate/final values under forward and reverse seeking. A counter using `onUpdate` needs events-enabled host seeking; prove that its value updates in the assembled render. A sourced value remains within the episode's claim boundaries.

## Verification and handoff

Inspect the assembled project, not only the isolated scene. Proof frames cover the reveal, meaningful intermediate action, readable hold, final state, and affected seams. Check captions, hierarchy, overflow, and data correctness at phone scale. Use the owning workflow's check/snapshot commands and review policy.

Return file path, scene window, required assets/registry items, proof frames, and unresolved findings to the owner. Additional export, audio generation, project setup, and human gates belong to that owner's requested scope.
