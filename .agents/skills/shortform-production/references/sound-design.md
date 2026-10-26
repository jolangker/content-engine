# Sound design: plan, assemble, verify

Read when placing or revising SFX/BGM, then again for the affected export checks. The [audio contract](audio.md) owns provider choices, media-use-first sourcing, and stage completion.

Keep the production's sound decisions in `video/sound_design.json`, independently of narration requests and caches. Record each role's mode (`use` or `none`) and reason. For each SFX cue record its ID, scene, narrative purpose, exact visual/word trigger, local asset and provenance, composition start, duration, and initial gain. Add a readable cue table and intentional silence to `STORYBOARD.md`. Select cue density from the board and message, rather than adding an effect to every transition.

Resolve estimated cue times against measured narration and actual motion before assembly. Store the timing-file and placed-narration hashes in the plan; changed speech, pacing, or motion requires rechecking affected cues. Narration synthesis owns voice metadata only: preserve supplemental media records and mark existing sound design for timing revalidation. Its completion does not complete the whole audio stage.

Use `scripts/sound_design.py` from this skill for plans using local assets and top-level audio clips:

```bash
python .agents/skills/shortform-production/scripts/sound_design.py --video productions/<slug>/video --apply
python .agents/skills/shortform-production/scripts/sound_design.py --video productions/<slug>/video --check
python .agents/skills/shortform-production/scripts/sound_design.py --video productions/<slug>/video --export productions/<slug>/exports/<version>.mp4
```

`--apply` validates inputs, writes managed SFX clips, supplemental metadata and the storyboard cue table, and preserves narration and unrelated clips. Call it after a builder rewrites the composition. Include the audio `--check` preflight in project check/render wrappers when using this plan. `--check` fails on stale timing/narration, missing or altered assets, cue/track mismatches, hidden clips, or out-of-range timing. `--export` additionally uses cue waveform matching with a fitted narration residual on decoded MP4 audio; it writes evidence under `verification/`. This helper requires NumPy and FFmpeg and covers explicit local top-level SFX without per-cue FX or automation. Nested/processed cues need equivalent verification through their owning HyperFrames timeline and processed reference, not an unsupported success claim. The JSON plan carries `version`, `decisions`, `timing_sha256`, `narration_sha256`, `motion_sources` (scene path to `motion_digest` hash, ignoring editor identity stamps), `assets` (ID, path, SHA-256, source), and `cues` (ID, asset, scene, purpose, trigger, start, duration, volume, track).

Before rendering, reconcile every planned cue with its actual track and verify source hashes and audible source content. After rendering, verify the effects in the MP4 at their expected times, not just that an AAC stream exists. Check full-file decode, clipping/loudness and speech intelligibility alongside cue presence. Inspect the audiovisual result when playback is available; objective presence and level measurements do not prove perceptual balance. Record unavailable listening explicitly and present the file for listening without claiming human approval. Keep evidence tied to plan, composition, asset and export hashes so later edits invalidate it.
