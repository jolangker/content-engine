# Board motion preview

Make one short clip that demonstrates how this board directs attention over time. Use the board's intended aspect ratio, visual tokens, and representative subject matter. Reuse a style-board sample when it can show the defining motion. Aim for roughly 5–10 seconds, long enough to see the setup, a meaningful change, and a readable hold. Demonstrate the relevant behavior, such as a reveal, object or camera movement, typography timing, a transition, or a cut. Default to a silent study and record any audio direction that remains conceptual.

## Build and render

Use the project-local [HyperFrames contract](../../hyperframes/SKILL.md), [motion guidance](../../hyperframes/references/motion.md), and [CLI skill](../../hyperframes-cli/SKILL.md). Follow registry discovery for named effects and the [3D integration](../../shortform-production/references/threejs.md#ownership-and-skill-selection) when building a 3D study. Keep editable source and required assets in the board's `motion-preview/` project and render `motion-preview.mp4` alongside it for direct playback from the board folder.

Authorization to build the board's visual package covers this preview render. Perform HyperFrames' checks and visual review, then render for the existing board review. Apply the [preview lifecycle](../../shortform-production/references/preview.md) to any server used for the study, recording ownership and cleanup in `DIRECTION.md`. A delivered MP4 releases the board review's need for a server unless the user requests a live preview.

## Verify and present

Play the exported MP4 at the intended viewing size, including phone size for vertical boards. Confirm the defining motion is visible, the reveal and hold give enough reading time, and the composition, type, and palette match `frame.md` and the static samples. Inspect representative decoded frames for clipping, missing assets, or unintended jumps. Correct defects and recheck the export.

Link the playable MP4 and editable source from `DIRECTION.md`. Record which behaviors were demonstrated, the inspected revision, and any limits. Present both the clip and the static board at the same review checkpoint. If rendering is blocked, record the blocker and the actual review scope so the visual package remains pending until the clip is available.
