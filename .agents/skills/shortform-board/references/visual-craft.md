# Visual craft for new and revised boards

Use this branch for visual exploration, new style boards, and visual revisions or revamps. `shortform-board` retains ownership of the package, state, review, and handoff. Apply these supporting skills within the requested visual scope.

## Load the supporting skills

- Read [frontend-design](../../frontend-design/SKILL.md) before planning visual direction or revising compositions. Use its subject-grounded choices, plan critique, typography, hierarchy, and restraint for the board and its editable HTML/SVG source.
- Also read [canvas-design](../../canvas-design/SKILL.md) when developing static composition studies or a style board. Use its design philosophy, spatial communication, and refinement pass to explore and render the treatment. Resolve its bundled `canvas-fonts/` relative to that skill's directory.

The current user brief and the board's accepted constraints govern both skills. On a revision, inspect the current visual source, rendered samples, `frame.md`, and latest feedback first; record which aspects are being preserved or reworked. Broader visual replacement follows the user's requested scope. Preserve the approved version as required by [board files](board-files.md#revising-an-approved-board).

Treat upstream style suggestions and lists of common defaults as prompts for judgment. Typography, palette, illustration, and medium must serve this board's audience and subject. A chosen cream palette, serif, geometric treatment, or cartoon language can be appropriate. Prefer measured readability over a generic thin-type treatment; explanatory labels identify real relationships. Actual user feedback and approval come from the conversation, including when an upstream example assumes a client reaction.

## Develop a visual argument

Ground the treatment in supplied references, the subject's materials or visual culture, and the intended audience experience. If an open brief needs outside visual input, inspect a small relevant reference set before settling the direction. Record source links and observed features separately from proposed adaptations in `DIRECTION.md`; reference-video analysis stays with `video-to-board`.

Make the visual idea testable: describe what gives this board its character and how composition, form, type, and color express it. Compare this plan with the brief before implementation. Rework choices that could be transferred unchanged to an unrelated subject without losing meaning. When alternatives are useful, vary their visual structure or storytelling as well as surface styling.

For canvas studies, retain the design philosophy in board-local Markdown, either in `DIRECTION.md` or a linked study file. The study's outputs are Markdown plus PNG/PDF. Integrate the selected treatment into the editable board source and canonical `frame.md`; the study does not replace the reusable package. Keep only references and assets actually useful to the direction, with their provenance and applicable licenses.

Build independent samples that exercise different communication needs appropriate to the board, such as a focal image, an interaction, or a detailed explanation. Carry a recognizable identity across them while varying composition. Static motion poses demonstrate proposed movement; animated verification still belongs to an explicitly requested demonstration or production.

## Review the rendered work

Inspect the actual exports at board scale and the sample compositions at phone viewing size. Assess:

- **Specificity:** identify the visible decisions that connect the design to this subject and audience. Rework interchangeable motifs or layout habits where the brief leaves room.
- **Communication:** the focal image, spatial relationship, or action carries the intended idea. Where visual storytelling is intended, briefly hide emphasis copy to check what the image communicates on its own.
- **Range:** samples address distinct needs while sharing the same illustration, type, and material language. Similarity follows identity rather than duplication of one layout.
- **Craft:** hierarchy, spacing, contrast, font rendering, annotation anchors, and intended overlaps remain readable at the viewing size. Refine the existing composition before adding elements to solve a weak focal point.
- **Fidelity:** source, exports, and `frame.md` agree, and the result respects the accepted constraints and requested revision scope.

Fix observed weaknesses and inspect the affected export again. In the existing visual review notes in `DIRECTION.md`, record the inspected revision, specific findings, corrections, and any remaining limits. Present the result at `shortform-board`'s existing visual checkpoint; this review adds no separate approval gate. Colors, font names, or a checklist score alone do not establish visual quality.

## Dependency provenance

The project-local `frontend-design` and `canvas-design` folders are unmodified copies of `skills/frontend-design` and `skills/canvas-design` from [anthropics/skills](https://github.com/anthropics/skills/tree/ca45fc496a3436251f191354091d557da31c15b5/skills), commit `ca45fc496a3436251f191354091d557da31c15b5`. Their licenses and canvas font assets are bundled. Keep project adaptations in this reference; when updating the dependency copies, review compatibility and update the recorded source revision.
