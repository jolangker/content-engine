# charts — category module

Apply the [scene-specialist contract](../../SKILL.md) and [scene build contract](../../references/builder-contract.md). This module supplies a visual recipe within the assigned episode window; inherit project style, paths, audio, and review policy before using its examples.

Animated **data-viz** from data. Asset-free (the "input" is the data). "One chart, one message" for short durations.

Read [data guidance](../../../hyperframes/references/types/data.md) before planning or building. Apply its guidance to default chart choices; preserve a chart type explicitly requested by the user.

## Plan (Director)

`content`: `{ type: bar|line|pie|race|pct, data[], labels[], headline, axes: bool }`. For `race`, data must be cumulative/time-staged.

## Vocabulary / leans on

- Block: **`data-chart`** (animated **bar + line**, staggered reveal, value labels — proven: borrowed + customized + rendered to MP4 in the prototype `charts-demo`).
- Also in the registry: **`bar-chart-race`** — install it rather than hand-authoring a race.
- For **pie / donut, ring/%**, search the live registry first; hand-author SVG/CSS geometry with seek-safe animation only when no result fits.
- Signature animations: bar stagger-grow · line `stroke-dashoffset` draw-on · pie radial sweep · ring fill · KPI count-up · race reorder.

## Build (reuse-first)

Reuse `data-chart`: `npx hyperframes add data-chart` → edit the data arrays + scales + headline/labels + palette in place (its data is baked in the script, not a `--variables` flag). Axes hidden by default; show muted only when magnitude is the message. Determinism: drive any animation from the seek clock, never wall-clock.

## Dashboard-skeleton variant

Use a dashboard layout only for an explicitly requested product-dashboard scene. Inherit the accepted UI/brand assets and board layout; any logo is a verified frozen project asset. Coordinate the requested stat and chart modules within that scene instead of adding a dashboard to an unrelated data beat.
