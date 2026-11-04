# Three.js craft for HyperFrames productions

Read before planning, building, or revising a 3D scene, including storyboard poses, materials, lighting, geometry, animation, and post-processing. Apply this reference when using the project-local Three.js skills for a production. Static board studies use the skill routing below with shortform-board's [reusable 3D treatment](../../shortform-board/references/visual-craft.md#define-a-reusable-3d-treatment) for artifacts and review; the timeline, storyboard, and export requirements here apply to production work.

## Ownership and skill selection

shortform-production owns the brief, board inheritance, scene plan, stages, audio, review, and delivery. The installed [HyperFrames contract](../../hyperframes/SKILL.md), [3D direction](../../hyperframes/references/types/3d.md), and [runtime protocol](../../hyperframes/references/runtimes.md) own composition structure and frame rendering. Read them for 3D authoring, then load only the supporting skills needed by the scene:

| Scene task | Supporting skill | Apply to the production |
| --- | --- | --- |
| Lighting and shadows | [threejs-lighting](../../threejs-lighting/SKILL.md) | Key/fill/rim balance, environment lighting, contact and cast shadows, subject separation. |
| Surface appearance | [threejs-materials](../../threejs-materials/SKILL.md) | Board-appropriate PBR or stylized materials, roughness, transmission, texture color spaces. |
| Object construction | [threejs-geometry](../../threejs-geometry/SKILL.md) | Recognizable silhouettes, custom parts, profiles, bevels, normals, and efficient repeated geometry. |
| Object and model motion | [threejs-animation](../../threejs-animation/SKILL.md) | Keyframes, skeletal/morph animation, clip blending, and procedural motion sampled at explicit times. |
| Image finishing | [threejs-postprocessing](../../threejs-postprocessing/SKILL.md) | Depth cues, restrained bloom, ambient occlusion, anti-aliasing, and output conversion. |

These skills supply implementation knowledge, not a new intake, visual direction, rendering framework, or approval flow. Their real-time examples need the adaptation below. Search the HyperFrames registry before hand-building a named visual, as usual. Use current library documentation for APIs that depend on the production's actual Three.js version; the installed examples target r186 and do not establish that version as a project requirement.

## Plan and pose the scene

Use 3D when form, depth, assembly, or movement explains the scene's idea and fits the selected board. Preserve an accepted 2D or stylized treatment unless the requested revision changes it. A narrow revision reuses unaffected geometry, audio, and timing.

For a board with an accepted 3D treatment, inherit its canonical visual guidance and recorded revision, using its rendered studies and linked scene assets as implementation references. Resolve episode-specific subjects, paths, timing, and runtime settings in the production spec; feed a requested change to the reusable identity back through shortform-board's revision policy.

In the existing scene plan/spec, record the object or mechanism, explanatory action, camera framing and path, material/light treatment, and caption/label space. Record asset provenance and applicable licenses alongside the production's other assets. For factual mechanisms, keep source-backed construction and motion distinct from illustrative simplifications; shading or a convincing mesh is not evidence of physical accuracy.

Build the readable hero pose using the intended renderer, geometry, materials, lighting, and output treatment. Capture it into the owner's required storyboard stills and combined board. An unrelated generated image is a reference, not proof of the executable 3D treatment. Static board exploration remains static; it does not start narration, animation, or export.

Evaluate the pose at the actual delivery size: silhouette, depth, material separation, important contact points, and label/caption clearance must survive phone viewing. Let the board determine realism, palette, and texture density. Fix geometry, light placement, or framing before adding an effect to hide an unclear subject.

## Adapt real-time examples to frame seeking

Follow HyperFrames' current runtime protocol as the authority for readiness, timeline registration, and seek events. Carry these constraints into the scene build context:

- **One clock:** derive camera, transforms, lights, material parameters, shader time, and animation poses from the explicit HyperFrames time. Replace sample `requestAnimationFrame`, `setAnimationLoop`, wall-clock timers, and accumulated per-frame motion with a seekable render-at-time path. If GSAP drives a property, keep that timeline paused under HyperFrames and give the property one owner.
- **Time scope:** resolve incoming seek time against the composition's actual time basis. Verify a scene that starts later in the film at its own start and middle; avoid subtracting the scene offset twice or applying global time to a local animation.
- **Deterministic state:** the same timestamp must produce the same pose and pixels after forward, backward, repeated, or out-of-order seeks. Sample animation clips at the requested time rather than advancing from the preceding frame. Reset blend/transition state when it would otherwise depend on playback history. Seed random data once; precompute stateful physics/particles and sample their recorded state.
- **Ready before capture:** load pinned runtime files, models, textures, and environment assets from the video project before capture. Keep scene markup and canvas identity stable. Register heavy setup through the current build-readiness protocol, including shader preparation where needed. Seek-time asynchronous work uses the protocol's completion hook; file existence alone does not prove readiness.
- **Fixed output:** use the production's canvas dimensions and a deliberate render resolution/pixel ratio rather than the preview device's pixel ratio. Keep the renderer, camera, and post-processing buffers in agreement. Preserve DOM labels, captions, and fixed board chrome in the composition hierarchy around the canvas.
- **Seekable effects:** time-dependent post-processing must also sample explicit time. Feedback, temporal accumulation, random glitch, and grain need deterministic reset/replay or a baked result; skip an effect that cannot reproduce an arbitrary frame reliably. Apply tone mapping and output color conversion once in the chosen render pipeline.

Use post-processing for generated 3D within its scene. Existing footage grades, grain, blur, and vignettes retain HyperFrames' media-treatment workflow. Pin a production's runtime dependencies and retain its valid assets; installing these knowledge skills does not authorize upgrading every existing video project or replacing its renderer.

## Verify within the existing checkpoints

Use the owner's HyperFrames check/snapshot/review loop and saved review policy. Add 3D evidence to the existing verification record rather than introducing another approval gate:

1. Inspect the reveal, readable hold, most demanding camera/object pose, final state, and relevant scene seams in the assembled composition. Check silhouette, model intersections, normals, shadow artifacts, reflection clipping, transmission, depth of field, and caption clearance where applicable. Effects should preserve the explanatory detail.
2. Capture a representative timestamp, seek forward and backward, then return and capture it again. Compare the actual images. Also inspect a later scene at its start and middle, and check the approved storyboard pose against the finished scene. Repair changed poses, blank frames, or temporal drift before rendering delivery media.
3. Measure the heaviest frame at the intended output settings. Reduce draw calls, excessive subdivisions, shadow resolution, transparent layers, or effect passes where necessary while retaining the accepted look. Reinspect the affected result; preview smoothness alone does not establish export readiness.
4. Record inspected timestamps, image locations, seek comparison results, render settings/runtime version, performance findings, and remaining limits. For delivery, verify representative frames in the actual exported video under the existing final verification workflow.

A technical check passing does not establish visual quality. Preserve storyboard and final-preview checkpoints, automation behavior, audio verification, and endpoint boundaries from shortform-production.

## Dependency provenance and maintenance

The five project-local `threejs-*` skill folders are unmodified copies of `skills/threejs-lighting`, `skills/threejs-materials`, `skills/threejs-geometry`, `skills/threejs-animation`, and `skills/threejs-postprocessing` from [cloudai-x/threejs-skills](https://github.com/cloudai-x/threejs-skills/tree/0e181866f095b5f06d005133876e926515390d95/skills), commit `0e181866f095b5f06d005133876e926515390d95`. The repository's MIT `LICENSE` is bundled in each folder. They are knowledge dependencies; Three.js itself is installed or vendored per video project when needed.

Keep adaptations in this reference and routing in project-owned skills/AGENTS.md. Leave installed HyperFrames and CloudAI-X skill contents unchanged. When updating either dependency, review the current runtime protocol, version-sensitive examples, relative links, and seek behavior, then update the recorded dependency revision for changed copies. A HyperFrames refresh should not require restoring project-specific edits inside its installed folders.
