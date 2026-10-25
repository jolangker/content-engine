# Interaction sound matrix — v2

Reusable design examples, not assets, a measured mix, or the existing episode's revised cue sheet. Select only events present in the researched system and actual action. Ambient rain remains a separate track. No audio has been generated in this board revision.

| Event type | Movement/preparation | Contact emphasis | Consequence/tail | Visible trigger |
| --- | --- | --- | --- | --- |
| Fit a rigid connector | Short material scrape/friction | Compact material tap/seat | Small settling sound if visible | Surfaces meet and component reaches its seated state |
| Turn a handle | Grip/shaft friction where warranted | Stop/click only if the mechanism has it | Matching flow/motion onset | Actual handle travel and operating threshold |
| Water reaches a surface | Stream begins after valid cause | Local splash at real impact | Short trickle/drip | Stream endpoint meets receiving surface |
| Close a cover | Motion/friction | Rim contact | Latch/settle if present | Lid reaches rim, then latch engages |
| Catch debris | Flow carries visible debris | Small material impact if audible at chosen scale | Water continues along valid path | Debris meets screen and stays there |
| Use a hand tool | Tool movement | Each important visible contact | Material response, if present | Tool touches the working surface |
| Open a chair | Hinge/fabric movement | Frame reaches stop | Weight/creak when someone sits | Separate unfold and weight-contact moments |
| Comic visitor/prop | Appropriate approach sound | Brief prop contact | Pause or small response | Reveal, prop arrival, then character reaction |

## Episode ledger fields

For each event record: `event_id`, `shot`, `actor`, `target`, `trigger_time`, `before/action/result`, `sound_role`, `asset_path`, `source_and_license`, `sha256`, `trim`, `onset/end`, `gain/envelope`, `track`, `intentional_silence_reason`, `export_window`, `presence_and_sync_evidence`, `listening_status`.

An asset found is not a cue placed. A cue placed is not proof that it is audible in the export. Rain/room tone/BGM cannot be counted as discrete event coverage. Keep unresolved assets visible in the ledger until resolved or an explicit scoped limitation is reported.
