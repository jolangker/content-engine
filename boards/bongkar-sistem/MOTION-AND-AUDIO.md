# Motion and audio - Bongkar Sistem v2

This revision replaces the v1 suggestion-only motion/sound guidance with explicit production requirements. The current package is static: authored poses and move plans, no new animation or synthesized audio. Apply and verify these rules during the next authorized audiovisual production.

## The unit is an event

Every important event joins actor, target, physical response, camera attention, and sound. Plan BEFORE -> APPROACH -> CONTACT/ACTION -> RESULT -> READABLE HOLD. Overlap entrances and secondary action where it helps pace, while preserving critical contact. A component should not simply appear already seated while the narrator says it was installed.

Keep physically linked components synchronized. If a handle affects a flow, derive both from the same operating state, with any real process delay preserved. Keep the achieved result across the next view. Stop repeating an operating loop after it has taught its relationship; advance to a new useful observation or operation.

At phone size the effect must remain noticeable without captions. Enlarge the view, show useful intermediate states, choose a better contrast/angle, or expose a section when it does not. Do not invent larger travel, force, or splash than the mechanism supports. A very brief justified result hold is part of a fast sequence.

## Camera choreography within shots

Write camera positions, target, focal length, intent, and proof times before implementation. Use a dominant move per shot with a clean settle/hold around contact. A clear majority of main shots should have noticeable intentional camera travel or motivated zoom as an initial review target; diagnostic holds are allowed. Avoid more than two fixed shots in sequence without a reason.

| Job | Move | What proves it |
| --- | --- | --- |
| Find the relevant part | Wide-to-detail dolly or motivated zoom-in | Subject grows clearly; a dolly also changes parallax/occlusion |
| Follow a transfer | Lateral/vertical tracking along the actual route | Subject/flow anchor stays readable as connected context passes |
| Expose depth | Short orbit, crane, or side approach | Previously hidden relation becomes visible without losing orientation |
| Read contact | Eye/low close-up, then brief settle | Contact and response can both be seen |
| Understand the layout | Overhead/section angle reached or cut to with state continuity | Input, operation, and output connections remain coherent |
| Reward the whole | Pull-back or useful zoom-out | Completed system and its consequence become visible |

Use both inward and outward scale changes when the explanation benefits. Lens change and camera travel are distinct tools, not interchangeable claims. Camera cuts can connect viewpoints but cannot satisfy the request for movement. No automatic ambient zoom on the entire film. Micro-drift alone is insufficient.

Preserve screen direction, coordinate system, part identity, connection geometry, and operating state. Keep velocities continuous within a move, and do not interpolate across a deliberate cut. Environment must cover the most extreme camera pose, not just the thumbnail. Keep captions anchored to the screen and off the contact.

For runtime implementation, use the registered seekable 3D camera/object state and the appropriate HyperFrames adapter. Avoid wall-clock or unregistered animation. Verify painted frames and actual moving playback. DOM bounds and a list of camera keyframes do not prove an internal WebGL camera moved visibly.

## A faster story with enough developments

Default 90 seconds, usually 75-95, strictly above 60. Around 20-26 meaningful visual steps at 90 seconds is the initial planning target, mostly 2.5-4.5 seconds. Build supported operations and consequences; do not just cut the existing six long views into smaller files. Let successive steps change scale, task, actor/target relation, or observed state. Detailed timing and quality gates are in PRODUCTION-STANDARDS.md.

## Comedy and human design

Keep the recurring builder sympathetic, competent enough to try, and a little too quick to celebrate. V2 shifts the human toward adult proportions and recognizable work clothing. The joke is behavioral: reaching for the chair too early, a prop revealing an unresolved condition, or a planted action returning at the end. It does not depend on giant eyes or a mascot body.

A middle comic development may use roughly 3-5 seconds; an ending callback is brief and optional. Plant the intent, let confidence register, interrupt it, then hold a readable reaction. Do not stack a dense technical line on the exact visual punchline. Resolve the useful explanation before the final comic reward. Exaggerated visitors remain overt fiction, not engineering evidence.

## Four distinct sound roles

1. Narration explains in conversational Indonesian with composed delivery.
2. Ambience establishes the location/weather quietly. Rain is ambience, not BGM and not interaction coverage.
3. Discrete SFX mark physically or theatrically meaningful movement, contact, and consequences.
4. Optional BGM supports pace only if it helps. It cannot replace the SFX event map.

Each important audible event receives a cue or an explicit reason for silence. A useful event can have movement, contact, and tail/result layers; use only the layers warranted. Examples are recorded in SFX-PLAN.md. Search/reuse/generate missing cues through the media workflow within authorized scope. A failed match is a reason to resolve/report the missing cue, not silently remove all accents.

Designed Foley can reinforce material/interaction without claiming to be the real recording. Do not add an irrelevant mechanical click to an otherwise silent process. Use restrained emphasis and localize it in time; avoid loud whooshes on every cut or a continuous effect bed that masks the very events it should support.

Trim leading silence and align contact to the visible trigger, initially within about two frames at 30 fps where physically appropriate. Let flow begin after its real cause. Keep focal cues audible over ambience and speech intelligible. Test short cue windows in the final export, not only the source asset or project timeline. A global loudness pass cannot certify cue coverage or perceived balance.

Review dry SFX with picture, then the narration mix and optional music. Report the listening status honestly. Waveform, ASR, and decode checks do not certify performance or subjective audibility. Without listening access, keep that result explicitly unresolved.

For narration follow the existing project policy: root .env default voice, explicit ElevenLabs provider and eleven_v4, delivery tags, voice validation, and fingerprinted reuse. This board revision neither regenerates the test's voice nor selects a new voice/model.
