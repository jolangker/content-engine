# Fan: continuous rotation becomes a head swing

board: di-balik-benda
board_revision: 6
topic_selection: auto
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
human_approved: false
pre_render_authorization: delegated by the user's --automation
requested_endpoint: publishing
delivery: queue
schedule: next configured slot, no displacement
commit: after pipeline completion

## Scope and direction
One new Indonesian 90-second explainer, 1080x1920, 30fps, 2700 frames, 16 shots. Curious general audience. Explain mechanical fan oscillation using the conventional motor/worm/clutch/carrier-disc/connecting-arm topology described in US7811059B2. Fixed illustrative crank radius: do not explain the patent's additional variable-angle control. Exact gearing ratios, speeds and dimensions are not product measurements. No repair or disassembly instructions. Not all fans use this mechanism.

Selected board [editorial](../../../boards/di-balik-benda/EDITORIAL.md), [frame](../../../boards/di-balik-benda/frame.md), SHOT-DIRECTION.md and DIRECTION.md v6. Illustrated 2.5D inspection bench, shaded thickness, fixed pale mineral ground #ECEEE9, ink #172B3B. Orange input, blue inspected linkage, teal output head. Large centered mechanism within x80..1000/y430..1410. Lower captions inherit actual stapler style: Manrope600 46px/1.3 at x108/y1500/width848, fitted pale blocks, at most two lines. This explicit board preference governs lower placement; leave room around platform controls, avoid right action rail, retain sidecars.

Narration uses one tagged ElevenLabs eleven_v4 request, voice resolved from root .env by maintained narration.py. BGM intentionally absent to expose speech and movement cues. SFX existing media-use assets and source-verified frozen material cues only, no new generation. Continuous gearing shares low-level representative cues; no claim of literal fan recording. Verify acoustic scene cuts and source-preserving observation pauses. Listening limits recorded honestly.

## Delegated topic selection
Ten candidates were presented in conversation before selection: mechanical oscillating fan, steam kettle, tape measure, hydraulic closer, iris aperture, pendulum escapement, reversible screwdriver, umbrella, mechanical pencil, toaster. Selected fan under --topic=auto. All eight rubric criteria: recognition strong (household fan); curiosity strong (continuous input versus reversing output); visual proof strong (fixed anchor and constant-length rod); causal depth strong (shared motor, gearing, eccentric, constraint, clutch); discovery strong (stationary anchor hidden under moving housing); motion diversity strong (rotation, yaw, pivoting, clutch travel); evidence strong (primary patent); scope workable (16 shots with fixed radius). Kettle/closer offer flow/thermal explanations but need more invisible-state encoding; iris/clock have stronger geometry demands; tape/pencil/screwdriver offer a narrower chain. No trends claimed.

Overlap checked TRACKER plus all production folder names, including unregistered roda-beda-putaran: this is a new question and mechanism, distinct from freehub coasting, music-box governor, seatbelt restraint, stapler, pump, cistern, lock and sewing. No recurring run: this invocation creates one episode.

## Hook selection before script
1. “Baling-balingnya terus searah. Kenapa kepala kipas bisa bergerak bolak-balik?” Behavior contrast; promises the crank-linkage answer.
2. “Satu motor, dua gerakan. Bagaimana kipas melakukannya?” Power-path angle; promises two branches.
3. “Kenop ditarik, kepala berhenti. Kenapa baling-baling tetap jalan?” State comparison; promises clutch isolation.
Recommended and selected 1 under delegated automation; not human approval. Research supports each. Script written after this selection.

## Story contract
First discovery at5–10s: shared shaft powers both front blades and rear mechanism. Linked questions: how power reaches rear disc → why pin orbits → why a rod cannot simply orbit freely → how fixed anchor forces head yaw → why clutch stops only this branch. Signature at35–48s: rigid rod holds its length between fixed anchor and orbiting pin while the head pivots. Show 4 diagnostic poses and emphasize two distinct fixed pivots. Opening and ending pair a running fan with now-visible hidden linkage. Head, gearbox and carrier-center positions move as one rigid assembly; stationary base never follows the head. Physical closure solved analytically at every seek. Stable landmarks: blue anchor A, dark neck pivot O, orange eccentric pin P.

## Publishing targets
Full inherited list from board ACCOUNTS.json:

```json
[
  {
    "provider": "trypost",
    "workspace_id": "01a171dd-5281-730d-af07-f2168d17add7",
    "workspace_name": "Admin's Workspace",
    "social_account_id": "01a172c9-3761-700a-9798-00febaa9fa90",
    "service": "instagram",
    "handle": "dibalikbenda.id"
  }
]
```

Preflight verified Admin's Workspace /01a171dd-5281-730d-af07-f2168d17add7; connected Instagram @dibalikbenda.id /01a172c9-3761-700a-9798-00febaa9fa90. Caller publishes directly, requires_approval false. Current content rules: instagram_reel, one video max900s/314572800bytes, caption2200 chars/5 hashtags. Configured queue in Asia/Jakarta; observed next slot2026-10-30T03:00Z (10:00WIB), recheck at delivery. Use queue next, no top insertion. Package and local upload authorized by user's queue endpoint.

Usage at start: session94%, weekly73% remaining. Context7 tools unavailable; pinned installed CLI documentation and command help used for execution. No skill upgrades performed. Existing untracked creative-direction skill is unrelated user work and excluded from this commit.

## Current state
Brief, research and script agent-verified. Next: visually verify full static storyboard before synthesis or animation. No preview started.
