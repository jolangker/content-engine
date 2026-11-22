# Board motion preview

Make one pilot scene that proves the board in motion before any episode depends on it; a board is approved only with a reviewed motion preview. Use the board's intended aspect ratio, visual tokens, caption treatment, and representative subject matter with illustrative copy. Reuse a style-board sample when it can carry the pilot.

## What the pilot shows

Roughly 12–20 seconds, in this order:

1. **The hook.** Frame 0 and the first three seconds as the board's episodes will open: the subject already on screen, the first change inside the first second, the on-screen line.
2. **One explanation beat.** A complete beat of the board's format with its internal changes: the reveal, the object or camera movement, typography timing, and a readable hold.
3. **One transition** into a second composition at a different shot scale.
4. **Sound.** A narration sample in the board's voice with captions timed to it, plus the effects or music the board's audio direction calls for. Resolve the voice under [narration voice](board-files.md#narration-voice) and synthesize under the production [audio contract](../../shortform-production/references/audio.md). When the voice is undecided or synthesis is unavailable, time the captions to a read-aloud estimate, record the audio direction as unverified in `DIRECTION.md`, and name that limit at the review.

## Build and render

Use the project-local [HyperFrames contract](../../hyperframes/SKILL.md), [motion guidance](../../hyperframes/references/motion.md), and [CLI skill](../../hyperframes-cli/SKILL.md). Follow registry discovery for named effects and the [3D integration](../../shortform-production/references/threejs.md#ownership-and-skill-selection) when building a 3D study. Keep editable source and required assets in the board's `motion-preview/` project and render `motion-preview.mp4` alongside it for direct playback from the board folder.

Authorization to build the board's visual package covers this preview render and its narration sample. Perform HyperFrames' checks and visual review, then render for the existing board review. Apply the [preview lifecycle](../../shortform-production/references/preview.md) to any server used for the study, recording ownership and cleanup in `DIRECTION.md`. A delivered MP4 releases the board review's need for a server unless the user requests a live preview.

## Verify and present

Measure the clip the way episodes are gated, giving the caption region so caption changes stay out of the motion numbers:

```bash
python .agents/skills/shortform-production/scripts/episode_qa.py --fingerprint boards/<slug>/motion-preview.mp4 --caption-region <x,y,width,height>
```

`first_motion_seconds` and `longest_static_seconds` fall inside the board's [production contract](board-files.md#production-contract) limits, and `held_share` matches the pace the board intends; for a board built from reference videos, compare all three with the reference fingerprints. Record the output in `DIRECTION.md`.

Play the exported MP4 at the intended viewing size, including phone size for vertical boards. Confirm the hook lands in its first second, the reveal and hold give enough reading time, and the composition, type, and palette match `frame.md` and the static samples. Inspect representative decoded frames for clipping, missing assets, or unintended jumps. Correct defects and recheck the export.

Link the playable MP4 and editable source from `DIRECTION.md`. Record which behaviors were demonstrated, the inspected revision, the measurement, and any limits. Present both the clip and the static board at the same review checkpoint. If rendering is blocked, record the blocker and the actual review scope; the board stays `draft` until the clip is reviewed.
