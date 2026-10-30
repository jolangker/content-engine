# Kettle: steam disconnects the circuit

board: di-balik-benda
board_revision: v6 (2026-10-27)
topic_selection: auto
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
human_approval: false
pre_render_authorization: delegated by the user's --automation instruction
requested_endpoint: publishing
delivery: queue
schedule: next configured slot, Asia/Jakarta, no custom time
commit: after the pipeline completes; include only this run's changes

## Brief and frozen direction
An Indonesian 90-second 1080x1920, 30fps illustrated 2.5D explanation for curious general viewers. Exact scope: steam-actuated snap-disc and over-centre mechanical switch; selected geometry is an original, simplified sectional interpretation of US4357520A, not a production drawing or universal kettle design. Keep the steam actuator distinct from the separate dry-boil protector, which is outside the explanation. Do not imply steam enters electrical contacts. Mechanism deliberately enlarged and operation slowed; heating time compressed. No repair directions.

Inherit [editorial](../../boards/di-balik-benda/EDITORIAL.md), [visual tokens](../../boards/di-balik-benda/frame.md), and [shot direction](../../boards/di-balik-benda/SHOT-DIRECTION.md). Caption treatment Manrope60046px at y1500, max2lines. Large fitted mechanism stage x80..1000/y430..1410. Narration ElevenLabs eleven_v4, root-env voice; separate existing SFX. BGM intentionally absent to expose small interaction sounds.

## Delegated topic decision
Shortlist presented in conversation: kettle, toaster, hydraulic door closer (replaces the differential overlap), salad spinner, automatic umbrella, tape measure, can opener, bicycle bell, wiper, pendulum clock. Existing tracker and production folder names inspected: selected question, actuation and takeaway do not duplicate sewing, lock, sprayer, cistern, stapler, music box, seatbelt, freehub, oscillating fan or mechanical pencil episodes. Wiper is related to the fan's rotary/oscillating linkage and therefore ranks lower for novelty. Kettle is selected for everyday recognition, a concrete shutoff question, and supported visible proof, not for ease of animation.

| Candidate | Recognition | Question | Visual proof | Causal depth | Discovery | Motion diversity | Evidence | Scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kettle | strong: daily boiling | strong: why off? | strong: duct/disc/contact | strong: four handoffs | strong: hidden dry sensor | strong: flow/flex/rotate/slide | strong: patent+engineering body | workable: one shutoff cycle |
| Toaster | strong | strong: why pop? | strong: latch/release | strong | strong | strong | workable: circuit variant needs lock | workable |
| Hydraulic door closer | strong: self-closing door | strong: why slow then latch? | workable: selected piston/valve section | workable: spring and damping stages | strong | strong: rotation/translation/flow | workable: manufacturer control guide | workable: exact variant must be researched |
| Salad spinner | workable | strong: press→spin | strong | strong | strong | strong | workable: US7621213B2 | workable |
| Umbrella | strong | strong: small button→opening | strong | strong | strong | strong | workable: US20090293925A1 | workable: telescoping variant |
| Tape measure | strong | strong: rewind | strong | workable | workable | strong | workable: US5210956A | workable |
| Can opener | strong | strong: cut+advance | strong | strong | strong | strong | workable: US1617142A | workable |
| Bicycle bell | strong | strong: repeated hits | strong | workable | strong | strong | workable: CN206466078U | workable |
| Wiper | strong | strong: turn→sweep | strong | strong | workable | strong | workable: EP0683076A1 | workable, related fan angle |
| Pendulum | strong | strong: paced gear motion | strong | strong | strong | strong | workable: authoritative educational lead | workable: select escapement |

All assessments are editorial, not retention predictions. Evidence leads for alternatives are discovery only, not completed claim verification.

## Hook checkpoint, before script drafting
1. “Airnya mendidih. Kok ketelnya tahu kapan harus mati?” — observable mystery and full causal promise. Recommended and selected under delegated automation.
2. “Uap ini punya jalur lain: menuju sakelar.” — hidden route opener.
3. “Dua lapis logam kecil ini ikut mematikan ketelmu.” — component-first opener.

Central mystery: why does a boiling kettle switch off? First discovery: uap menuju unit pemutus through the revealed duct, approximately8s. Chain: what carries the signal? → where does it arrive? → why does the disc change? → how does that separate contacts? Signature: steam-heated snap disc trips the over-centre lever, then link separates contacts. Opening and ending share kettle/lid/handle landmarks; final condensed replay exposes the cause. s03 explicitly rewinds after opening discovery. s16 explicitly replays, not an extra unexplained automatic cycle.

## Publishing targets
```json
{
  "source": "board",
  "board_accounts_file": "boards/di-balik-benda/ACCOUNTS.json",
  "board_accounts_sha256": "b975f156df5c9c6bb0ac33f940b2cef5191793fd2c659a027a4e75291dcc25f3",
  "accounts": [
    {
      "provider": "trypost",
      "workspace_id": "01a171dd-5281-730d-af07-f2168d17add7",
      "workspace_name": "Admin's Workspace",
      "social_account_id": "01a172c9-3761-700a-9798-00febaa9fa90",
      "service": "instagram",
      "handle": "dibalikbenda.id"
    }
  ]
}
```
Preflight: Trypost Local, Admin's Workspace, exact board account connected, caller publishes directly; Instagram Reel supports90s. Queue configured10:00 daily Asia/Jakarta. No remote post created yet.

## State
Research and script agent-verified; storyboard is next. No human approvals asserted. Native narration and delivery files will be preserved. Listening capability unavailable unless a suitable tool becomes available.

## Storyboard verification
Complete pre-audio board inspected:16 styled scene stills in correct order, no missing images; HTML and full PNG1920x4274. Agent visual check of all16poses passed after correcting the early contact-state continuity and moving bottom annotations to1395px. Files: video/boards/storyboard.html and video/boards/storyboard.png; individual stills video/boards/stills/. Static board verifies layout, not final motion/audio. Accepted under delegated automation; no human approval.

## Audio placement
One ElevenLabs eleven_v4 synthesis, root-env voice, native94.240s, 213 words. Original cache preserved. Derived pitch-preserving tempo=1.13542169 chosen only if native recording leaves insufficient observation time. Source at native tempo is retained. Every derived-master sample preserved across verified quiet splices; one final normalization targets-16LUFS/-2dBTP.15 verified acoustic cuts, integer30fps map; final master90s. Individual word timings are estimates reanchored to utterances, not independent forced alignment. 64 short caption groups. Bundled media-use manifest inspected; separate cue planning will copy frozen material assets. Music absent intentionally. Listening unavailable; no auditory or phone-speaker approval claimed.

## Preview ownership
Pipeline-owned preview created for final-look review: project=C:\Users\muhth\Documents\projects\content-pipeline\productions\ketel-uap-memutus-arus\video, PID=12872, port=3002, URL=http://127.0.0.1:3002/#project/video. HTTP200 verified. Retention only until delivery render and export verification; release before external delivery. No human-review hold, automation authorizes render after agent verification.

## Filesystem overlap audit correction
An unregistered legacy folder productions/roda-beda-putaran retains differential video/output artifacts, although no EPISODE.md remains. Differential is therefore excluded from the final shortlist. Replacement candidate: hydraulic door closer ? familiar self-closing door, question why closing slows then latches; strong recognition/question/discovery/motion, workable causal depth/proof/evidence/scope pending exact hydraulic variant selection. Manufacturer evidence lead: https://www.assaabloy.com/uk/en/knowledge-centre/door-controls/backcheck-latching-speed-closing-delay-what-does-it-all-mean (body read with Jina). This correction affects only the unused candidate; the selected kettle has no overlap. No legacy folder modified.

## Final-look acceptance under automation
Current measured board inspected:16scenes,1920x4274PNG, all resources loaded, updated macro contact/spring replays and grounded fixed pillar visible.15seams reviewed via overview plus fresh strips at revised cuts;8signature poses show approach/snap/reaction. First causal duct discovery occurs within s02 at approximately5s after timing placement (earlier than initial8sestimate). Check passed;12intentional macro context-crop warnings retained as documented in REVIEW.md. Delivery render started for exactly2700frames. No continuous perceptual playback or audio listening claimed.

Final-note revision: preview restarted after prior cleanup, PID=9588, port=3002, URL=http://127.0.0.1:3002/#project/video; HTTP200 confirmed. Same pipeline ownership and release-after-export condition. Final board and note geometry verified:16notes, one line each,62pxcaption clearance. Corrected delivery render authorized by active automation.

## Verified package
CONTENT_PACKAGE.md matches export v1 and actual metadata. All delivery links exist; Instagram caption length=822, five relevant hashtags. Next: reconcile duplicate search, upload exact verified bytes, schedule queue next and save observed receipt. No second draft-review gate under active automation.

## Queue endpoint complete
Trypost Local re-read confirmed scheduled/queue for @dibalikbenda.id, post ID=01a18e88-104c-7349-956f-1bd042abd3ec, media ID=01a18e87-afa9-7198-9220-a35ea6453f3d. Assigned UTC=2026-11-01T03:00:00+00:00; local=2026-11-01T10:00:00+07:00. Anonymous HTTPS media download returned200 with exact export SHA256 and bytes. [Receipt](PUBLISHING.json). Scheduled endpoint complete; publication is future and not claimed live. No future polling authorized/needed. Next: commit this production and its tracker entry; preserve unrelated workspace changes.

## Final state
stage: publishing
status: complete
Queue receipt is verified for all inherited targets (one Instagram account). Final export SHA256=6d26100d0555869aac7462d5bcdf549cb3c1d3f1602b3168e4d6cbd8096fdf7b, bytes=9566743,90.000s/2700frames. Full decode,16decoded scene proofs,15encoded quiet seams and18encoded SFX cues passed. Final loudness=-13.7LUFS; true peak=-1.4dBTP; clipping=0. Subjective listening unavailable. Pipeline preview PID9588 stopped, status not-running, no listener on3002 and PID absent. No review hold/server retained. Provider did not retain optional cover offset0; remote cover setting remains unset, local first-frame cover is only a recommendation. No publication-live claim or future polling. No remaining production or delivery work. The completed production and its own tracker entry are committed together; Git history supplies the commit identity.
