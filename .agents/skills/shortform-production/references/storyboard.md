# Visual storyboard

Read before creating or revising a storyboard, or handing a production to HyperFrames with an endpoint at storyboard or later. This reference owns the pipeline's artifact and completion requirements. Use HyperFrames' [storyboard format](../../hyperframes/references/storyboard-format.md) and [storyboard recipe](../../hyperframes/references/storyboard.md) for scene poses and board structure.

## Scope and execution policy

Every new production reaching `storyboard` creates the complete visual storyboard before audio synthesis and animation, including `--automation` runs continuing to preview, export, content package, or publishing. Endpoints at brief, research, or script stop before this work.

Active automation delegates layout review to the agent while retaining every artifact below. Carry the resolved execution policy and storyboard requirement into `EPISODE.md` and `video/BRIEF.md` when present. Pending `--automation=after-storyboard` retains human review of the complete verified board, including its PNG; acceptance activates automation under [the invocation contract](invocation.md#activation). Reuse legacy `flow`, `storyboard`, and `mode` metadata when resuming, while the resolved pipeline policy determines the current review gate.

## Required artifacts

Paths below are relative to the production's HyperFrames project, normally `video/`:

| Artifact | Requirement |
| --- | --- |
| `STORYBOARD.md` | Canonical scene plan with scene identifiers, purpose, copy, visual idea, order, and timing estimates. |
| `boards/stills/` | One real styled static frame per planned scene, posed in the composition with the selected board's fonts, colors, copy, and layout. Follow the owning recipe's snapshot process and file naming. |
| `boards/storyboard.html` | Styled review board with every still in scene order, scene identifiers/titles, and timing labels, using the recipe's frame classes. |
| `boards/storyboard.png` | PNG capture of the complete HTML board, including every scene and its labels. This combined board image is separate from individual scene stills and final-video proof sheets. |

## Build and verify

For 3D scenes, read [Three.js integration](threejs.md) before posing them. Its renderer-based stills and craft checks feed the same storyboard artifacts and review policy below.

1. Resolve the scene plan from the selected script and creative direction. Pose and capture each scene using HyperFrames' storyboard recipe. Inspect every still for legibility, intended hierarchy, fixed board identity, and visual rhythm across scenes. Repair affected poses before assembly.
2. Assemble the HTML board from those stills. Load the local page in a browser, wait for fonts and all scene images to finish loading, and check that every image has nonzero dimensions and every planned scene is present in the correct order. Fix missing resources and clipped content before capture.
3. Capture the entire board as `boards/storyboard.png`, including content below the first viewport. Choose a board width and grid that keep frames and labels legible. Open the saved PNG itself and check that all scenes are visible, ordered, and readable; a first-viewport screenshot or an HTML path alone does not complete this step.
4. Record artifact paths, scene coverage/count, PNG dimensions, and visual inspection outcome in `EPISODE.md` or the existing verification document. Present links to both the HTML board and PNG for a human storyboard checkpoint, a storyboard endpoint, or an explicit inspection request. For an automated run continuing beyond storyboard, retain the verified board internally and use a concise progress update under [presentation and durable records](invocation.md#presentation-and-durable-records). Apply the run's human review or agent verification policy, then enforce the selected endpoint.

The storyboard stage is complete only when all required artifacts exist, their scene counts/order agree, and the saved PNG has passed visual inspection. An internal outline, a final-video contact sheet, or existing HTML/stills without the combined PNG is insufficient. Repair a failed capture within scope; record a concrete blocker if it cannot be completed, rather than claiming storyboard completion or advancing a fresh production into audio/animation.

## Resume and revise

Reuse valid artifacts and prior approval for the same layouts. On a continuation that includes storyboard or video work, repair missing storyboard artifacts from the existing valid scene layouts without regenerating narration or rebuilding the video merely to fill the gap. For an already animated project, scene snapshots may supply the missing board; identify them as a reconstruction from the current composition rather than an earlier human-approved sketch. Preserve the actual later tracker stage and record the repair in the episode.

A package-only, publishing-only, or unrelated narrow revision reuses its existing inputs under the invocation contract; it does not initiate historical storyboard reconstruction. When storyboard layouts or scene order change, update the affected stills, HTML, and PNG together and repeat the affected checks. For completed historical work, distinguish the storyboard planning version from later video proof sheets; an earlier layout approval never implies approval of a changed final video.
