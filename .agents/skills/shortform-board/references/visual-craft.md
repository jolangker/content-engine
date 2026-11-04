# Visual craft for new and revised boards

Use this branch for visual exploration, new style boards, and visual revisions or revamps. `shortform-board` retains ownership of the package, state, review, and handoff. Apply these supporting skills within the requested visual scope.

## Load the supporting skills

- Read [frontend-design](../../frontend-design/SKILL.md) before planning visual direction or revising compositions. Use its subject-grounded choices, plan critique, typography, hierarchy, and restraint for the board and its editable HTML/SVG source.
- Also read [canvas-design](../../canvas-design/SKILL.md) when developing static composition studies or a style board. Use its design philosophy, spatial communication, and refinement pass to explore and render the treatment. Resolve its bundled `canvas-fonts/` relative to that skill's directory.
- For a chosen 3D direction, follow [reusable 3D treatment](#define-a-reusable-3d-treatment) below. It uses the installed Three.js craft skills within this board's static exploration and review scope.

The current user brief and the board's accepted constraints govern these supporting skills. On a revision, inspect the current visual source, rendered samples, `frame.md`, and latest feedback first; record which aspects are being preserved or reworked. Broader visual replacement follows the user's requested scope. Preserve the approved version as required by [board files](board-files.md#revising-an-approved-board).

Treat upstream style suggestions and lists of common defaults as prompts for judgment. Typography, palette, illustration, and medium must serve this board's audience and subject. A chosen cream palette, serif, geometric treatment, or cartoon language can be appropriate. Prefer measured readability over a generic thin-type treatment; explanatory labels identify real relationships. Actual user feedback and approval come from the conversation, including when an upstream example assumes a client reaction.

## Develop a visual argument

Ground the treatment in supplied references, the subject's materials or visual culture, and the intended audience experience. If an open brief needs outside visual input, inspect a small relevant reference set before settling the direction. Record source links and observed features separately from proposed adaptations in `DIRECTION.md`; reference-video analysis stays with `video-to-board`.

Make the visual idea testable: describe what gives this board its character and how composition, form, type, and color express it. Compare this plan with the brief before implementation. Rework choices that could be transferred unchanged to an unrelated subject without losing meaning. When alternatives are useful, vary their visual structure or storytelling as well as surface styling.

For canvas studies, retain the design philosophy in board-local Markdown, either in `DIRECTION.md` or a linked study file. The study's outputs are Markdown plus PNG/PDF. Integrate the selected treatment into the editable board source and canonical `frame.md`; the study does not replace the reusable package. Keep only references and assets actually useful to the direction, with their provenance and applicable licenses.

Build independent samples that exercise different communication needs appropriate to the board, such as a focal image, an interaction, or a detailed explanation. Carry a recognizable identity across them while varying composition. Static motion poses demonstrate proposed movement; animated verification still belongs to an explicitly requested demonstration or production.

## Define a reusable 3D treatment

Use this branch when a selected direction includes 3D or the user requests a 3D revision. Preserve the accepted medium on other board work. Read [Three.js craft integration](../../shortform-production/references/threejs.md#ownership-and-skill-selection) for skill routing, source provenance, and compatibility. Load geometry, materials, or lighting for the actual study; load post-processing when finishing changes the look, and animation when planning poses or reusable movement principles requires it. Technical examples support the board's chosen style rather than prescribing photorealism.

Record the following decisions where they apply in the body of the board's canonical `frame.md`, using the existing visual-guidance format. Keep recognized visual tokens in their existing frontmatter fields; these decisions do not introduce new HyperFrames YAML keys.

| Decision | Reusable direction to capture |
| --- | --- |
| Form | Realism or abstraction, silhouette/detail level, edge treatment, and rules for cutaways or exploded assemblies. |
| Materials | Surface families, color roles, roughness/reflection character, and how transparency preserves important relationships. |
| Light and depth | Key/fill/rim intent, environment/background, contact shadows, contrast, and subject separation. |
| Camera and movement | Framing, perspective, distance, camera versus object movement, pacing/easing character, and readable holds. |
| Finishing and annotations | Depth-of-field/bloom restraint, image clarity, label anchors, caption clearance, and fixed board chrome. |

Use concrete values or ranges when they materially determine the intended look; tie dimensions to a stated scene scale. Distinguish identity rules from per-episode choices so the board supports varied compositions. The episode owns its objects, exact camera path, timings, runtime version, and performance budget.

Develop independent static studies that exercise this treatment, including the detail or spatial relationship most likely to become unclear. Retain editable scene source and required local assets under the board folder, with provenance/licenses, and use actual rendered poses in the style-board source/export. Reuse the board's current source layout when it can host the studies; a 3D study needs no production folder or HyperFrames video initialization. Reference imagery can guide the look but does not establish that the implemented materials and lights match it.

At the existing visual review, inspect silhouette, material separation, shadows/reflections, important contact points, finishing, and annotation clearance at phone scale. Use static start/hold/end poses when movement direction needs explanation; label motion properties as conceptual until animated verification exists. Record inspected studies and unresolved limits in `DIRECTION.md` alongside the normal review notes.

Before handoff, reconcile the selected treatment in `frame.md`, rendered studies, and recorded visual revision. Link the reusable scene source/assets from that guidance where needed. Productions inherit this accepted treatment under [Three.js production integration](../../shortform-production/references/threejs.md#plan-and-pose-the-scene), then build and verify their own timeline. A draft study stays a proposal until accepted under shortform-board's existing review policy.

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
