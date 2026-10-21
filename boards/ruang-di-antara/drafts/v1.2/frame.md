---
name: ruang-di-antara-v1.2-draft
implementation_revision: 2026-10-21
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
sequence:
  frameCount: 16
  dramaticFrameCount: 2
  lightFrameCount: 14
  targetDurationSeconds: 90
  planningDurationRangeSeconds: [85, 95]
  planningBeatsPerFrame: [3, 5]
paletteModes:
  light: { background: "#F3EDE3", text: "#302B28", metadata: "#302B28", captions: "#302B28" }
  dramatic: { background: "#302B28", text: "#F3EDE3", metadata: "#F3EDE3", captions: "#F3EDE3" }
contentDirection:
  primary: visual-action
  planningEmphasisWords: [0, 5]
  supportingParagraphs: false
  captions: full-spoken-words
---

# Ruang di Antara — frame contract v1.2

Draft implementation of user requirements dated 2026-10-21; awaiting visual review. See DIRECTION.md. The active approved package is retained at the board root.

## Identity and safe areas

Use local Newsreader regular/italic and DM Sans assets. Shared chrome is frozen in components/: header x88–936 / top101 / height34, footer x88–936 / bottom82 / height34. Copy these sources into each production. Header shows the series and current frame / 16; footer shows @eliansatya. Geometry and visibility persist across shots and palette changes. Chrome does not join content choreography.

Keep key content in x88–936 / y230–1480 and captions in y1550–1740. Captions contain spoken words only. One reading priority is visible at a time. Use Newsreader for selective short emphasis; DM Sans for essential labels and captions. Display scale is chosen for the composition and verified at phone size.

## Less text, richer visual storytelling — user revision

Let the visual action occupy most of the content field. Start with 0–5 emphasis words as an implementation guideline, allowing frames without emphasis text. A necessary definition or communication example can be longer, staged over time. Remove supporting paragraphs and labels that only restate narration. The relatable question remains in the spoken hook and full captions; the emphasis layer may show a short question or appear as successive phrases. Caption coverage is not reduced by reducing emphasis copy.

Enrich scenes through context-bearing illustrated objects, voice ribbons, speech spaces, unresolved time, shared event markers, meaningful occlusion and changes in spatial relationships. Keep faceless organic participants, the four-color palette and consistent illustration language. Large interaction scenes and close details should carry meaning when emphasis text is hidden. Use a phone only when attention to a phone is part of the fictional scene; objects do not establish psychological explanations by themselves. Composition should make the action legible before extra labels are considered.

## Sixteen frames and two dramatic palette switches

Exactly sixteen meaningful compositions per standard episode. Fourteen have cream background and charcoal text. Exactly two dramatic frames use charcoal background and cream text. Invert main copy, explanatory labels, captions and metadata together; keep their geometry fixed. Use cream/sand for fine lines and readable text on charcoal. Brick remains a graphic accent, not small text on charcoal.

Select the two dramatic script lines before storyboarding and justify both switches. Their positions follow the story; 04 and 12 in the rhythm strip are illustrative. Separate dramatic frames with cream where the story permits. At the beginning of a dramatic frame, land the inversion together on the dramatic phrase or at its cut; maintain the dark mode for that frame and return to cream for the next light frame. Avoid repeated flashes within a shot. These two frames are not an instruction to alternate background every beat.

Preserve participant identity across palette changes: silhouette, position and trajectory remain locatable. A charcoal participant may invert to cream on charcoal while its established silhouette/continuity identifies it. Distinguish actors through shape as well as color. Color, size and diagram arrows must not imply gender, blame, diagnosis, worth or stronger evidence than the narration provides.

## Multiple internal beats

Every frame develops through meaningful visual changes. Start with 3–5 internal beats as a planning guideline, adapting to reading time and measured speech. Specify starting state → action → response → visible consequence. A beat may redirect attention, change distance, extend a path, expose a boundary, reframe an established element or reveal a decisive phrase. Subtitle changes alone do not count.

Avoid leaving the complete landed composition unchanged through most of a shot. Distribute semantic developments across its duration; a final still hold is purposeful after movement has resolved. A five-second frame can carry four distinct actions without four separate title animations. Some shapes or paths may persist into the next frame to preserve continuity.

Vary timing, scale, direction, focal placement and the relation between typography and diagram. Do not repeat a fixed entrance–diagram–support sequence in every frame. Richness comes from a sequence of readable actions; unnecessary floating, continuous zooms and movement unrelated to meaning do not fulfill the requirement. Use brief stillness to punctuate a dramatic phrase or final reflection.

## Visual vocabulary

Faceless organic forms, illustrated everyday objects, meaningful distance, connections, boundaries, position traces and introduced event markers form one visual vocabulary. B-roll is excluded. Intentional flat color fields keep the explanatory action clear. Build depth through foreground overlaps, large actions and context-bearing objects. Added elements must make the scene or its evolution more legible; general creative recipes do not override this board's relational concept.

## Handoff and review

For every frame, record its focal composition, narration range, timed internal beats, visual consequence, palette mode and sound events. Review all sixteen landed compositions and actual intermediate poses, not just titles or label changes. Exactly two palette entries must be dramatic. Inspect inversion contrast, actor continuity, caption bands and stationary chrome at boundaries. Technical checks do not replace creative review.

The style-board samples are independent fictional studies, not an episode storyboard. The four-pose motion strip describes one frame's evolution; it is not four additional frames. Motion and audio remain conceptual until a production or explicit demonstration is made. Audio direction is in AUDIO.md; editorial and sourcing standards are in EDITORIAL.md.
