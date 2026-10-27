# Creative direction — Di Balik Benda v6

## Identity and experience

**Di Balik Benda** explains familiar objects and small systems to curious Indonesian-speaking general audiences. Its audience-facing promise is **“Yang tersembunyi, jadi terlihat.”** The viewer moves from curiosity to being able to describe the input, interaction, and output in their own words. Assume no engineering background while keeping the mechanism recognizable to technically informed viewers.

The organizing idea is an **illustrated inspection bench**. The object is the scene: its hidden spatial relationships supply the interest. Pale mineral fields make small gaps and silhouettes readable; shaded volume keeps separated parts recognizable. Precise annotations support inspection rather than turning the frame into a dashboard.

## Visual references

Inspect the [full style board](../assets/style-board.png) for the whole creative system. It is a 1700 × 5561-pixel static presentation, not an episode layout. Its board metadata, panel borders, study footers, and page grid are presentation furniture, not required episode overlays.

These independent 508 × 903-pixel studies demonstrate different decisions; their numbering does not establish a shot order:

| Reference | Learn from it |
| --- | --- |
| [Section study](../assets/study-01.png) | Exposed internal space, hatched solid material, anchored leader, shaded body, and separate input/active/output roles |
| [Macro study](../assets/study-02.png) | Large contact detail, translucent housing, preserved landmark, and annotation tied to a precise location |
| [Transfer study](../assets/study-03.png) | Shaded mechanical parts, emphasized contact, causal direction, material distinction, and centered occupied frame |

All three show the v6 lower caption treatment and enlarged framing. The depicted valve, zipper, and gears are original conceptual studies: their geometry and behavior must be independently established for a factual subject. All sample copy is illustrative.

## Invariants: medium and material

Use **2.5D illustration only** across whole-object, sectional, exploded, macro, comparison, and alternate views. Construct layered vector or raster parts with illustrated thickness or side faces, consistent shading, overlap, and coherent depth order. Restrained layer parallax may reinforce that depth. The original assets used vectors; vectors are not a tool requirement.

Keep clean silhouettes, consistent mechanical axes, satin polymer, brushed metal, and selectively transparent sectional housings. Contour, shading, highlights, and restrained grounding shadows make volume legible. Texture remains subordinate to contact and geometry; no grain or photographic finish is specified.

Flat labels, arrows, and captions may support the illustrated object. Standalone flat 2D scenes, true 3D scenes, mixed-medium sequences, and arbitrary camera orbits fall outside the accepted lock. A change of medium requires the user's explicit override. Another angle should be a coherent alternate 2.5D illustration with shared landmarks.

## Exact palette and meaning

| Token | Value | Role |
| --- | --- | --- |
| Canvas | `#ECEEE9` | Pale mineral field |
| Surface | `#F8F9F5` | Light inspection surface and caption block |
| Ink | `#172B3B` | Engineering ink, principal type and contours |
| Muted | `#536775` | Secondary text and supporting annotations |
| Line | `#CDD4D4` | Quiet separators and supporting rules |
| Input | `#C94422` | Applied force, initiating input or action |
| Active | `#2459C4` | Currently inspected component or contact |
| Output | `#167580` | Resulting motion or outgoing flow |
| Metal | `#A6B4BE` | Base mechanical material |

These are identity tokens. Shade materials while preserving semantic identity. Keep most parts in the base material vocabulary; use accents selectively. Color works with anchored labels, direction, and sequence rather than carrying meaning alone. A dark interior is permitted when it improves visibility, without introducing mandatory light/dark alternation.

## Typography and primitives

Use the bundled [Manrope variable font](../assets/manrope.ttf) and [IBM Plex Mono regular](../assets/ibm-plex-mono.ttf). Their licenses are [Manrope OFL](../assets/Manrope-OFL.txt) and [IBM Plex Mono OFL](../assets/IBM-Plex-Mono-OFL.txt). Make fonts available through the destination's own font mechanism. If that is impossible, choose a comparable sans/mono pair, disclose the substitution, and recheck width, weight, and line breaks; that is a fidelity exception, not an equivalent verified match.

| Role | Family and weight | Reference treatment |
| --- | --- | --- |
| Compact, confident display | Manrope 800 | Tracking `-0.055em` in the design specification |
| Short explanation | Manrope 500 | Line height 1.45 |
| Part name / inspection state | IBM Plex Mono 400 | Line height 1.5 |
| Narration caption | Manrope 600 | Exact treatment below |

The 508 × 903 studies use 42px titles; their rendered tracking is approximately `-0.05em`, a study-level variation from the display token. Keep the specified display token as the reusable default rather than copying the overview masthead's different typography. The technical character comes from objects and annotation precision, not pervasive all-caps interface text.

Use concise function or part labels. Reference callout stroke is 1.5px, with a dot terminating on the actual component. Exposed internal surfaces may hatch the cut solid material. Ghost housings have a reference opacity of 0.15 so the enclosure's location remains visible without obscuring the active part. Preserve opacity as a ratio; scale stroke and geometry to the destination.

## Composition and reference geometry

Keep one dominant object or mechanism per explanatory beat. Use coherent assembly axes, stable component identities, short anchored leaders, and space that reveals connections. Density follows complexity. A quiet frame with one part is appropriate when it teaches the relationship clearly; there is no decoration, focal-point, or ambient-motion quota.

The source film format is **1080 × 1920, 9:16**. Measurements below are in pixels on that canvas. Scale dimensional values by the output-size ratio for another 9:16 resolution. For a different aspect ratio, explicitly adapt the stage and safe areas rather than stretching the illustration; retain hierarchy, contact visibility, large framing, and caption separation. Check the destination's overlays on the actual output.

### Lower narration caption: accepted v6 treatment

| Property | Reference value |
| --- | --- |
| Region | Left x=108, top y=1500, width=848, minimum region height=150 |
| Alignment | Center phrase within that region; keep its lower anchor stable across shots |
| Type | Manrope 600, 46px, line height 1.3 |
| Foreground / background | Ink `#172B3B` / surface `#F8F9F5` |
| Block | Fit to text, maximum outer width 848 including padding |
| Padding / radius | 18px vertical, 26px horizontal / 14px |
| Copy | Short phrases aligned to measured speech, at most two lines |

The 150px height describes the caption region, not a requirement to inflate every text-fitted pale block. Keep the measured x=108 and width=848 reference even though it is not perfectly symmetric about x=540. Captions contain spoken words; annotations can add concise part names. Resegment long speech phrases before reducing the font. The studies use proportional 21.64px captions. Their captions establish appearance only, not speech synchronization.

### Large centered object: accepted preference with implementation targets

| Property | Reference value and status |
| --- | --- |
| Mechanism stage | x=80..1000, y=430..1410; board implementation target |
| Center | x=540, y=920; center the visible object or inspected subassembly |
| Occupancy | Target 80–95% of stage width or height, whichever fits first |
| Caption clearance | At least 60px above y=1500, including annotations and the full action sweep |
| Measurement | Actual visible geometry, excluding empty asset bounds, invisible shells, leaders, and shadows |

The user accepted larger, fitted, centered objects. Stage and occupancy numbers operationalize that preference; they are adaptable implementation targets, not measurements of every reference-production shot. Keep the 60px clearance in the source format unless a justified destination adaptation is recorded.

For a broad object, fit width; for a tall one, fit height. Contain the relevant silhouette and complete motion sweep. A purposeful macro may crop inactive context, preserving the decisive contact and a recognizable landmark. Reframe each explanatory job; an oversized invisible asset canvas does not make the mechanism itself large. Prefer fewer labels or a dedicated detail view over making the hero small to fit copy. The stage's nominal bottom leaves 90px to the caption, so the 60px minimum also accommodates carefully checked ancillary geometry.

Other source measurements are an 8px spacing unit, 64px presentation-board margin, and 32px sample-study safe inset. These belong to their original reference canvases, not universal episode margins. Typography and geometry must remain readable at phone size after scaling.

## Source-grounded illustrative application

Use the [transfer study](../assets/study-03.png) to explain a design choice: two large shaded components dominate, a localized ring identifies contact, and input/output cues show where attention should travel. In a new researched mechanism, first establish the whole, then frame the actual transfer large enough to inspect, retaining an axis or part landmark. Put a short spoken phrase in the lower text-fitted caption and anchor the useful part name near its component. Revisit the same opening input with the hidden connection exposed. This applies the concept without treating the schematic gear shape, sample sentence, or number of parts as factual or mandatory.

## Observable visual fidelity

- Does the actual illustrated volume remain coherent in whole, section, macro, and alternate views? Do rigid parts, enclosure location, and axes stay identifiable?
- Does the mechanism dominate through visible geometry rather than empty bounds? Are contact, useful clearance, relevant travel, and essential labels visible at phone size?
- Do the exact colors retain their semantic roles with supporting cues? Is material shading quiet enough for small gaps to read?
- Do Manrope/mono roles, short anchored annotations, and the lower two-line caption match the relevant bundled study? Are caption anchor, wrapping, and clearance preserved across frames?
- Does each composition expose a specific spatial or causal relation? Decorative grids, arbitrary interface numbers, unanchored lines, cards replacing the mechanism, or extra invented parts fail this direction.

For narrative, temporal, and sound fidelity, use [story, motion, and sound](story-motion.md). Static appearance does not establish those properties. Decision evidence and asset limitations are in [provenance](provenance.md).
