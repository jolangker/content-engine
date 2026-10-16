---
name: shortform-board
description: Explore, create, or revise reusable creative boards for short-form content, combining editorial framework, storytelling concept, visual direction, and a static style board. Use for vibe exploration or a fresh creative direction; episode scripts, storyboards, and finished videos belong to shortform-production.
---

# Shortform Board

Develop a creative system that can guide multiple productions. A board is the package of editorial and visual decisions plus its reference artifacts; the style-board image is one part of that package. Each board can have its own framework, tone, typography, palette, shapes, motion language, and audio direction.

## Establish context and the requested endpoint

Read project instructions and `TRACKER.json`, then the relevant existing board documents. Distinguish a new direction, continuation, revision, comparison, or discussion. An approved board is context, not a universal template. Reuse its decisions only when the user requests continuity.

If invoked without context, briefly show available boards and ask whether the user wants a new direction or to continue one. If the request already says to explore a new board, ask only the missing creative seed: what it should communicate or feel like, what they already picture, or which references to use. Use project context where available; avoid repeating intake already answered in the conversation.

Discuss before making artifacts when the user asks to discuss. A discussion or bare invocation does not create a board folder or tracker entry. Once a concrete direction is selected for development, or the user requests a visual artifact, read [board files and state](references/board-files.md), choose a stable slug, and save the work there. Preserve a provisional direction as draft when it has not been accepted.

For supplied URLs or references, inspect the actual material using the project's research tools. Identify observations separately from creative proposals. If access is incomplete, state that limit rather than claiming to have analyzed the entire account or reference.

## Explore distinct directions

For an open brief, first understand the audience experience, intended emotion, content purpose, and viewing surface. Ask only for missing information that materially changes the exploration. If the user has no picture in mind, offer a small number of clear starting choices instead of a long questionnaire.

Present roughly three to five genuinely different directions when breadth is useful. Vary narrative viewpoint, framing, composition, or format as well as visual treatment. Avoid a menu whose only difference is color. For each direction, make these tangible:

- What the audience should feel or understand.
- How the account speaks and how the content unfolds.
- What fills the frame and how motion would carry meaning.
- A short illustrative phrase or situation when it helps comparison.

Present the alternatives before recommending one, with a reason connected to the user's context. Treat mixing, rejecting, and redirecting as valid responses. A developed user idea can go directly to refinement; a fixed number of pitches is not required.

## Separate the layers of the concept

Make the following distinctions clear so the user can choose a combination:

| Layer | Decisions |
| --- | --- |
| Editorial framework | Audience promise, account stance, depth of explanation, and intended takeaway. |
| Storytelling concept | Repeatable way of revealing the subject: viewpoint, structure, metaphor, or format. |
| Visual direction | Palette, typography, composition, shapes/media, motion character, and audio mood. |

Recommend a coherent combination after showing the meaningful alternatives. Confirm the chosen direction through the user's response before developing its visual package in the normal collaborative flow. A user-delegated choice can be made and recorded with its reason; it is not user approval of later unseen work.

## Make the visual direction concrete

Load the installed `hyperframes-creative` skill and its relevant references before selecting a visual treatment. Follow its house-style and video-composition reads for substantive design. Use its design-spec guidance when writing `frame.md`; load typography or motion guidance when those decisions need detail.

Translate the chosen direction into specific proposed tokens and rules: color values with roles, font families with expressive and functional roles, visual primitives, composition principles, meaningful movement, and audio direction. Explain why those choices fit the content. Keep these proposals distinct from accepted decisions.

Motion and audio can be described without generating them. Use the HyperFrames entry skill and required domains if the user actually requests an animated demonstration. Named effects require the registry skill before hand-building them. A static board alone does not require initializing or rendering a HyperFrames video project.

## Build and review the static style board

When the user asks to see the direction, make a visual artifact, not just a written list. Use editable HTML/SVG or another suitable local source for typography and abstract geometry. Choose image-generation or design tools only when their capabilities fit the requested material.

Show the palette, actual typefaces, key primitives, and a few independent sample compositions that exercise different communicative needs. Include a compact motion vocabulary as static poses when relevant. The samples demonstrate a reusable identity; label them as independent studies rather than an episode sequence. Sample copy illustrates the style and does not establish psychological or scientific claims.

Render/export the board to a reviewable image, inspect the result, and fix clipping, missing fonts, illegible text, or mismatched tokens. Provide the source and preview links; offer or produce PDF when useful or requested. State which motion/audio properties remain conceptual. Preserve font files and licenses when needed for reliable viewing.

Present the board and wait for visual feedback in collaborative work. Apply revisions to the affected parts and update the corresponding spec and exports. A visual approval accepts that visual revision; it does not silently approve an editorial framework that has not been presented.

## Develop the reusable editorial framework

Use the chosen concept and accepted decisions to propose content pillars, narrative structures, explanation depth, voice, formats, and endings. Explain the purpose of each and include enough illustrative topics or phrasing to show how they work across episodes.

Tailor these to the board. The number of pillars, order of explanation, narrator voice, visual palette, and metaphor system may differ between boards. Existing account-level constraints still apply. An editorial-first request can develop this layer before visual design; preserve dependencies and approvals rather than forcing one sequence.

For psychology or other research-sensitive material, distinguish editorial examples from verified claims. A board can specify sourcing standards without researching or producing a complete episode. Real psychological explanations need suitable sources before being presented as facts.

Present the framework for review and record the user's response. When visual and editorial approvals cover the current versions and the requested board package exists, mark the board approved without requesting a redundant final confirmation. If the user delegates creation without intermediate review, deliver a completed draft for review; only mark approved when the user actually accepts it.

## Finish, resume, and hand off

- Keep the current phase, confirmed choices, pending questions, and next action in the board's `DIRECTION.md`. Keep root tracker entries small as defined in the storage reference.
- On continuation, inspect the actual files and current feedback, reuse accepted work, and continue from the unresolved layer. A brief "go" approves only the result or recommendation currently presented.
- Respect partial endpoints such as options only, visual direction only, or style board only. Report the actual completed scope and retain unfinished work as draft or awaiting review.
- For revisions of an approved board, follow the storage reference's version-preservation rule. Keep existing productions on their recorded direction until a change is requested.
- Deliver the board path, preview, and concise direction summary, with any remaining review clearly identified. Load `shortform-production` only when the user asks to turn material into an episode; board creation alone does not create a production folder or entry.
