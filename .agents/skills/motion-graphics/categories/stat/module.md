# stat — category module

Apply the [scene-specialist contract](../../SKILL.md) and [scene build contract](../../references/builder-contract.md). This module supplies a visual recipe within the assigned episode window; inherit project style, paths, audio, and review policy before using its examples.

A single **hero number** reveal. Asset-free (the "input" is the number). ~4–6s.

Read [data guidance](../../../hyperframes/references/types/data.md) before planning or building the number reveal.

## Plan (Director)

`content`: `{ value, prefix ($), suffix (% / x / K-M-B), label, ring: bool }`. Envelope: bold display font, restrained palette + one accent.

## Vocabulary / leans on

- Block: **`apple-money-count`** (finance-flavoured: $ counter + green flash + money burst + SFX) when it fits; otherwise hand-author.
- Follow the current data/motion contract; preserve the episode's approved palette, imagery, and audio when adapting a finance-specific block.
- Primitives: `count_up` (odometer) · `scale_pop` · `ring_fill` (arc) · `label_stagger` (after value) · `hold`.

## Build (reuse-first)

Reuse `apple-money-count` + set target / prefix / suffix / label / palette; **or** hand-author per the proven prototype `v0-stat-motion-demo`:

- **count-up is timeline-driven** — tween a proxy `{v:0}→target` with `onUpdate` writing the formatted number (seek-safe; never setInterval/wall-clock).
- `font-variant-numeric: tabular-nums`; decelerating ease; ~1.2–1.6s then **hold** the final value.
- ring/arc via `stroke-dashoffset`, finishing in sync with the count-up; label fades in **after** the number lands (value → meaning).
