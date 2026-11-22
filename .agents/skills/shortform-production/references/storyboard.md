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
| `boards/poses/` | Stills that show change over time: `hook-<seconds>s.png` at frame 0, the first change and three seconds, and for every frame longer than the contract's `motion.max_static_seconds`, `NN-a-<label>.png`, `NN-b-<label>.png` onward in beat order from its start pose to its end pose. |

## Plan change over time

A still shows a layout. These entries make the plan say what changes and when, and the film is held to them later. In `STORYBOARD.md` every frame carries:

- `shot`: its scale and view in one or two words (`wide`, `close cutaway`, `top-down`, `macro`). Frames that share a label share a framing; a run of one label stays within the contract's `storyboard.max_same_shot_run` (2 by default).
- `scene`: concrete physical objects and observable actions (never abstract layout placeholders like `"title card"` or `"bullet list"`). Choose staging from [explainer grammars and motion devices](motion-and-grammars.md), and split wrapping housings/cutaways under [procedural mark-making and cutaways](../../shortform-board/references/illustration-and-mechanisms.md).
- `camera` & `on_screen_text` (when applicable): camera punctuation (`hold`, `push`, `pull`, `pan`, `snap-zoom` — never 3 consecutive push-ins; accents `<= 1/3` of shots) and non-caption on-screen copy (`<= 8` words, numbers matching `SCRIPT.md`). Lint `STORYBOARD.md` before posing stills with `python .agents/skills/shortform-production/scripts/storyboard_lint.py --production productions/<slug> --strict`.
- `reads`: each visible change with its window in seconds from the frame's start, in HyperFrames' format: `water climbs the bed wall (0-4s); it spills over the rim (4-8.5s)`. A new read starts at least every `motion.max_static_seconds`; the film's final frame may hold three seconds longer. Take the reads from the beats marked in the script.
- `status`: `built` once its still is posed, and `animated` only when the scene's timeline plays its reads.

Capture `boards/poses/` in their own snapshot runs and move the files into place, since each run clears its output folder. Show the hook poses as a strip before the first frame of `storyboard.html` and each long frame's poses beneath its box, in elements with `class="poses"`, so the combined PNG carries them.

## Build and verify

For 3D scenes, read [Three.js integration](threejs.md) before posing them. Its renderer-based stills and craft checks feed the same storyboard artifacts and review policy below.

1. Resolve the scene plan from the selected script and creative direction. Pose and capture each scene using HyperFrames' storyboard recipe. Inspect every still for legibility, intended hierarchy, fixed board identity, and visual rhythm across scenes. Repair affected poses before assembly.
2. Assemble the HTML board from those stills. Load the local page in a browser, wait for fonts and all scene images to finish loading, and check that every image has nonzero dimensions and every planned scene is present in the correct order. Fix missing resources and clipped content before capture.
3. Capture the entire board as `boards/storyboard.png`, including content below the first viewport. Choose a board width and grid that keep frames and labels legible. Open the saved PNG itself and check that all scenes are visible, ordered, and readable; a first-viewport screenshot or an HTML path alone does not complete this step.
4. Record artifact paths, scene coverage/count, PNG dimensions, and visual inspection outcome in `EPISODE.md` or the existing verification document. Present links to both the HTML board and PNG for a human storyboard checkpoint, a storyboard endpoint, or an explicit inspection request. For an automated run continuing beyond storyboard, retain the verified board internally and use a concise progress update under [presentation and durable records](invocation.md#presentation-and-durable-records). Apply the run's human review or agent verification policy, then enforce the selected endpoint.
5. Run the gate from the project root with `python .agents/skills/shortform-production/scripts/episode_qa.py --production productions/<slug> --stage storyboard`. It holds the planned duration and frame count to the contract, checks shot variety and the read cadence, confirms the hook and long-frame poses exist and differ outside the caption region, and confirms the stills, HTML board and PNG are present. Fix what fails and run it again; the verdict is saved as `video/verification/quality-gate-storyboard.json`.

The storyboard stage is complete only when all required artifacts exist, their scene counts/order agree, the saved PNG has passed visual inspection, and the gate passes at `--stage storyboard`. An internal outline, a final-video contact sheet, or existing HTML/stills without the combined PNG is insufficient. Repair a failed capture within scope; record a concrete blocker if it cannot be completed, rather than claiming storyboard completion or advancing a fresh production into audio/animation.

## Resume and revise

Reuse valid artifacts and prior approval for the same layouts. On a continuation that includes storyboard or video work, repair missing storyboard artifacts from the existing valid scene layouts without regenerating narration or rebuilding the video merely to fill the gap. For an already animated project, scene snapshots may supply the missing board; identify them as a reconstruction from the current composition rather than an earlier human-approved sketch. Preserve the actual later tracker stage and record the repair in the episode.

A package-only, publishing-only, or unrelated narrow revision reuses its existing inputs under the invocation contract; it does not initiate historical storyboard reconstruction. When storyboard layouts or scene order change, update the affected stills, HTML, and PNG together and repeat the affected checks. For completed historical work, distinguish the storyboard planning version from later video proof sheets; an earlier layout approval never implies approval of a changed final video.
