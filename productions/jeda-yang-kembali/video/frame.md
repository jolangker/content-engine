---
name: ruang-di-antara-v1.1
implementation_revision: 2026-10-20
canvas: { width: 1080, height: 1920, fps: 30 }
colors:
  canvas: "#F3EDE3"
  ink: "#302B28"
  accent: "#A34F3F"
  sand: "#D8C8B5"
typography:
  display: { fontFamily: "Newsreader", weight: 400, lineHeight: 1.06 }
  body: { fontFamily: "DM Sans", weight: 400, size: 42, lineHeight: 1.3 }
  label: { fontFamily: "DM Sans", weight: 500, size: 30, lineHeight: 1.3 }
  captions: { fontFamily: "DM Sans", weight: 500, size: 46, lineHeight: 1.25 }
spacing:
  safeLeft: 88
  safeRight: 144
  contentTop: 230
  keyContentBottom: 1480
  captionTop: 1550
  captionBottom: 1740
components:
  header: { left: 88, right: 144, top: 101, height: 34, fontSize: 26, lineHeight: 1.3, tracking: ".095em", rule: none }
  footer: { left: 88, right: 144, bottom: 82, height: 34, fontSize: 26, lineHeight: 1.3 }
  series: "Ruang di Antara"
  handle: "@eliansatya"
  chrome_css: "components/chrome.css"
  chrome_html: "components/chrome.html"
---

# Ruang di Antara — implementation contract

The approved v1.1 editorial and visual direction remains in DIRECTION.md and EDITORIAL.md. The user authorized these implementation corrections on 2026-10-20 after investigating repetitive compositions and drifting series metadata. The prior package is preserved in revisions/v1.1. This correction fixes reusable identity; it does not claim a new human review of generated frames.

## Fixed series identity

Use the shared chrome source in every production, copied into its project for self-contained rendering. Header and footer have the same position, dimensions, typography, wording and visibility in every scene and production at 1080×1920. The right header contains the current frame number and total; the footer contains the handle. No episode tagline or header rule is added implicitly. On charcoal scenes, change metadata ink from charcoal to cream; geometry stays fixed. Chrome stays visible through cuts and does not join scene entrance/exit motion. Other aspect ratios need an explicit adaptation rather than a new inferred position.

Keep scene content in x88–936 / y230–1480 and captions in y1550–1740. Metadata is nonessential and outside those content bands. The original style-board's three independent studies remain creative references; their illustrative section labels and footer phrases are not the production chrome specification.

## Variable scene content

Preserve the cream/charcoal/brick/sand palette, Newsreader/DM Sans pairing, faceless organic forms and meaningful distance, connection, boundaries and traces. A charcoal pressure beat is allowed. B-roll, decoration without meaning, and gender/diagnostic color coding remain outside this direction.

Choose composition from the beat: an intimate quote, a large interaction diagram, an asymmetric response, a comparison, a time agreement, or a spare reflection can carry different ideas. Change focal scale, text/diagram relationship, alignment, actor presence, whitespace and choreography where the explanation warrants it. The two actors are a vocabulary, not a requirement to place two equal-size forms below a headline in every frame. A semantic change in a label or path alone is insufficient evidence of compositional variety. Repeated layouts are appropriate when a deliberate before/after comparison needs a stable reference.

Before animation, record each frame's focal element, composition and visual change from its neighbor. Review the full contact sheet for repeated silhouettes and repeated entrance rhythms. After animation, inspect the landed pose of every scene and fixed chrome at scene boundaries. Record creative review separately from technical checks; automation retains both.


## Episode adaptation ? revision v2

Use one charcoal pressure scene (04). Scene layout and timing are recorded in STORYBOARD.md. Shared chrome is inherited unchanged; content changes scale and placement according to the beat. No B-roll or decorative motion.
