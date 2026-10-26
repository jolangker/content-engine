# webpage — category module (search-driven)

Apply the [scene-specialist contract](../../SKILL.md) and [scene build contract](../../references/builder-contract.md). This module supplies a visual recipe within the assigned episode window; inherit project style, paths, audio, and review policy before using its examples.

**Animate a webpage / link.** Capture a supplied URL or use the user's supplied page screenshot, then animate a scroll, UI reveal, cursor demo, or region callout within the assigned scene. Inherit the production's narration and scene duration. Existing-video captioning follows [captions](../../../hyperframes/references/captions.md); an entire product film follows [launch guidance](../../../hyperframes/references/types/launch.md) under its production owner.

## Source (Step 2)

Fetch the page via `hyperframes capture --json` (DOM + screenshots) or a provided screenshot → frozen project-local image(s)/DOM. `asset_needs`: `{ kind: web, source: <url>, treatment: none }`.

Inspect the capture result before building. If `BLOCKED.md` exists, JSON reports `ok: false`, or the
command exits non-zero, stop the URL-capture path and report the reason. Continue with a provided
screenshot only when it was an explicit source from the user (or the user explicitly chooses it
after the failure). Do not animate a blocked partial capture, invent missing DOM, or eyeball element
coordinates from protection/challenge pages.

This web need cannot use the generic asset-free fallback: it requires a usable captured screenshot
or DOM, or a provided screenshot explicitly selected by the user. If none is available, stop.

## Vocabulary / leans on

- Use current [motion](../../../hyperframes/references/motion.md) and [runtime guidance](../../../hyperframes/references/runtimes.md); search the registry before building a named effect.
- Primitives: scroll pan · spotlight/dim · cursor move + click-ripple · zoom-to-region · callout pin + label.

## Build (reuse-first)

Place the captured page as the base layer; animate a **scroll-through** (translateY over the page height), **spotlight** key regions (dim + highlight), a **cursor** that moves and clicks (ripple), **zoom** to a coordinate, and **callout** pins/labels anchored to page regions. Honor `builder-contract.md`.

**Two rules that match the news article-highlight (see `../news/module.md`):**

- **Highlights are swept/animated ON, never pre-applied** — a spotlight box wipes in (`scaleX 0→1`), a marker sweeps a region, a callout pops _after_ the zoom lands; the page never starts pre-annotated.
- **Anchor to REAL element positions** — `hyperframes capture` gives the page HTML/DOM, so measure the target element (`getBoundingClientRect` → stage-local) and zoom/highlight it exactly, step-by-step (the "highlight a real element" technique). Don't eyeball coords.
