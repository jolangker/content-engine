---
workflow: faceless-explainer
flow: automation
storyboard: no
mode: autonomous
message: "Dua katup mengatur satu siklus: flapper membuang, pelampung mengendalikan pengisian."
angle: how-to
length: 90s
destination: vertical short-form master
aspect: 9:16
language: id
audience: curious Indonesian general audience
board: di-balik-benda
board_revision: v4
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
until: export
delivery: package
pre_render_authorization: delegated by the user's --automation instruction
---

# Intent

Explain one gravity cistern cycle with a lever, chain, buoyant hinged flapper, cup float and fill valve. Scope the illustration to the tank: water exits toward the bowl, whose siphon is outside this episode. Explain visible functional control of the fill valve without inventing an internal diaphragm design. Illustrations are schematic, not dimensional assembly drawings. Operation is slowed and refill time compressed for explanation.

# Confirmed choices

User invocation: `$shortform-production --board=di-balik-benda --topic=auto --until=export --automation`.
The user delegates topic, hook, layout and final-render decisions. Board v4 supplies 90 seconds, 2.5D only, linked interactions and synchronized SFX. No external delivery is requested. Stop after verified MP4 and captions, without packaging or publishing.

# Inferred production decisions

1080x1920, 30fps, 16 explanatory shots; neutral platform master with conservative inset for captions. Natural Indonesian narration. Original shaded SVG mechanism throughout, board Manrope and IBM Plex Mono. No music: leave space for water and material cues under speech. Resolve voice from root .env using maintained narration entry point, ElevenLabs eleven_v4. Personal prefs agree with automation/no human storyboard; no recipe exists.

# Storyboard override

Create every required static pose, all scene stills, `boards/storyboard.html` and full `boards/storyboard.png` before synthesis and animation. Agent verification replaces human layout review. Retain `storyboard: no` as execution mode; it does not remove these artifacts.

# Visual and motion direction

Inherit ../../../../boards/di-balik-benda/frame.md, EDITORIAL.md and SHOT-DIRECTION.md, v4. One persistent tank assembly with explicit exterior/section and local macro landmarks. Orange input, blue inspected parts, teal flow/output. Show lever rotation, chain take-up, hinged flapper opening, tank draining, float descent and fill opening, reseat, water rising and float shutoff. The fill valve begins opening during drain, not only after reseating. Distinguish the normal refill tube route from a separately labeled overflow fault demonstration. All physical views remain shaded 2.5D.

# Review and limits

Human approval: false. Agent verifies claims, static rhythm, mechanical continuity, cue coverage, seeking, runtime and export. Record unavailable perceptual listening honestly. Preview resources follow production skill ownership and verified cleanup.
