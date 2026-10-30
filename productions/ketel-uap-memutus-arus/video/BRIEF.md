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
Shortlist presented in conversation: kettle, toaster, differential, salad spinner, automatic umbrella, tape measure, can opener, bicycle bell, wiper, pendulum clock. Existing tracker and production folder names inspected: selected question, actuation and takeaway do not duplicate sewing, lock, sprayer, cistern, stapler, music box, seatbelt, freehub, oscillating fan or mechanical pencil episodes. Wiper is related to the fan's rotary/oscillating linkage and therefore ranks lower for novelty. Kettle is selected for everyday recognition, a concrete shutoff question, and supported visible proof, not for ease of animation.

| Candidate | Recognition | Question | Visual proof | Causal depth | Discovery | Motion diversity | Evidence | Scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kettle | strong: daily boiling | strong: why off? | strong: duct/disc/contact | strong: four handoffs | strong: hidden dry sensor | strong: flow/flex/rotate/slide | strong: patent+engineering body | workable: one shutoff cycle |
| Toaster | strong | strong: why pop? | strong: latch/release | strong | strong | strong | workable: circuit variant needs lock | workable |
| Differential | strong encounter, hidden part | strong: unequal wheel speeds | workable: bevel mesh | strong | strong | workable: mainly rotation | workable | workable: complex tooth geometry |
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
