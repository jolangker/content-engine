# Mechanical and static visual review

Reviewed 2026-10-25 against `SOURCES.md`, `scene-plan.json`, `build.py`, `mechanism.py`, the saved complete `boards/storyboard.png`, and individual stills 04, 05, 08, 09, 10, 12 and 14 at full output size. This is a source/pose/static-layout review, not temporal playback or audio approval.

## Findings and disposition

1. **Moving labels missed their parts — root correction required.** The original `pelampung` leader in shots 08/12 terminated at fixed `(315,495)` while the float moved; at low water it pointed to the falling fill stream, and at high water to empty space below the float. The original open-flapper leader in shots 05/07 terminated on the valve seat. Use an anchor on the actual float at `(315,430+floatY)`, and a flapper anchor obtained by rotating `(568,789)` about `(650,795)`. Generate static leaders from the selected pose and update animated leaders from the same state. Root owns this builder correction and recapture.

2. **Overflow/refill branch visually crossed a closed seal — corrected in illustration source.** Original flow paths crossed the flapper face in shots 10/14. The corrected fixed overflow branch joins the common outlet at `(570,852)`, below the seat's `y805..828` sealing region. Both refill and overflow flow paths now follow `L645785 Q645815610834 L570852 L570906`. The solid branch's lowest extent is `y860`, within the existing ceramic floor's `y863` boundary: no new protruding external pipe was added. Root must rebuild scenes and inspect the recaptured result.

3. **Lever-chain connection could leave the macro — corrected crop.** The original lever crop started at `y225`, while the raised lever tip at -14 degrees reached approximately `y208`. The lever viewBox is now `85 165 650 710`, retaining the tip/chain connection and pivot.

4. **Initial coupled pose stretched the chain — source helper corrected; builder correction required.** The initial shot-04 combination lever -14 degrees / flapper 13 degrees separated the endpoints by approximately 542 units versus a resting chord near 478. Root's agreed correction uses lever -5 / flapper 13 for shot 04's result and shot 05's entry, then progresses to -14 / 48. `mechanism.chain_path()` now preserves a schematic 490-unit chain length with a perpendicular quadratic bow solved by 20 sampled segments and 18 binary iterations. This is a visible slack abstraction, not a catenary/force simulation. The root's animated JavaScript must mirror this helper rather than retaining the previous 30-unit bow.

Verification of the agreed revised poses sampled 101 interpolants per pose segment across all 16 shots. Maximum endpoint chord was **485.817306 units**, at lever -14 / flapper 48, below the 490-unit available length. SVG XML parsed successfully after the source corrections. These numerical checks verify pose feasibility and syntax, not rendered animation.

## State and topology checks

- Shots 04 through 12 preserve their outgoing/next incoming operating state once the agreed shot-04/05 lever correction is applied: lift, drain, handle release with flap still open, float descent and fill onset, overlapping inflow/outflow, reseat, rise, and shutoff. The sequence does not reset to a full tank between these shots.
- Main flush flow, fill-to-tank, refill-hose route and fault overflow remain distinguishable. The closed flapper blocks the main tank outlet while the corrected refill branch bypasses it downstream.
- The normal full surface is `y410`, below overflow lip `y350`; lower SVG y is higher physically. The refill hose ends at `y323`, leaving a 27-unit gap above the overflow lip. It is not drawn submerged.
- Float upper lip is approximately 10 units above the normal surface, with its body immersed. Automatic travel follows `365*(1-water)` with limits -45..332. At near-empty poses the float reaches its lower travel while retaining water contact. A failed overfill scenario may submerge the float after its upper travel limit; the scenario is explicitly abnormal.
- The flap's hinge remains at `(650,795)` next to the fixed overflow assembly. The chain stays attached to the lever-tip and flapper lifting eye. Housing, riser and overflow tube remain stationary during the cycle.
- Shot 13's different fill state is explicitly tagged `INSPEKSI JALUR ISI`; shot 14 is tagged `CONTOH KONDISI ABNORMAL` and its subtitle is conditional; shot 15 announces the compressed replay. Those state changes are not presented as continuous normal chronology.
- The episode remains scoped to the gravity tank. It does not invent a fill-valve diaphragm cutaway or explain unsupported bowl-siphon geometry.

## Static clarity

All 16 scenes are present in the saved board. Board colors and shaded illustrated thickness remain consistent in whole, cutaway and macro views. The sheet alternates assembly context, lever, flap, float and flow-path inspection. The repeated flapper macros answer different supported questions: opening, buoyant hold and reseating. The two adjacent anatomy views are a short deliberate orientation sequence, not a repeated operating loop. Titles and scene subtitles are readable at output size; the moving leader fixes above are necessary to prevent misidentification.

## Remaining verification

Root must rebuild and recapture the storyboard after the source/builder fixes, then inspect the corrected stills. This report does not establish full-speed mechanical continuity, deterministic seeking, sound onset synchronization, listening quality or final export correctness. Those belong to the subsequent production verification.
