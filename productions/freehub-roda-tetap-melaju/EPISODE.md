# Freehub: the wheel keeps rolling

board: di-balik-benda
board_revision: 6
topic_selection: auto
execution_policy: automation
automation_after: none
automation_state: active
human_review: none
human_approved: false
pre_render_authorization: delegated by the user's --automation instruction
requested_endpoint: publishing
delivery: queue
schedule: next configured free slot; no queue displacement
commit: after the requested pipeline endpoint is verified

## Brief
One new Indonesian mechanism explainer, 90 seconds / 2700 frames, 1080x1920 at 30fps. Curious general audience. Explain why a pawl-type bicycle freehub permits coasting while the pedals rest. Scope: two opposing spring-biased pawls on the input carrier and an internally toothed ring fixed to the hub shell. This is a topology-based schematic, not a dimensional reproduction or a claim about every bicycle. Bearings support the rotation; do not claim the clutch makes propulsion or suppress all friction. No repair tutorial or performance comparison.

Creative direction: [editorial](../../boards/di-balik-benda/EDITORIAL.md), [visual frame](../../boards/di-balik-benda/frame.md), and SHOT-DIRECTION.md, frozen v6. Original 2.5D illustration, shaded metal side faces, input orange, active pawls blue, output teal. Fixed lower speech captions: Manrope 600 46px, y1500, x108 width848, max two lines. Mechanism stage x80..1000/y430..1410; center visible geometry and full useful sweep. About 80–95% stage occupancy. Cropped inactive context is explicit in contact macros.

Narration: one continuous tagged ElevenLabs eleven_v4 request with the literal root-.env voice. Use the maintained narration helper. BGM: none, exposing speech and the dry contact contrast. SFX: existing media-use library first; reuse source-verified frozen metallic/travel cues for physical events, soft editorial click only for the cutaway. No new SFX generation. Measured acoustic gaps govern scene cuts and any inserted observation pauses. Words remain estimated inside each acoustic anchor. Listening limitations must be reported honestly.

## Topic decision and overlap
Shortlist presented in conversation before selection: freehub, derailleur, steam kettle, locking tape measure, toaster, mechanical pencil, umbrella, hydraulic door closer, kitchen timer, stapleless paper binding. All differ in audience question and takeaway from registered episodes. Inspected filesystem includes unregistered roda-beda-putaran (differential), which does not explain bicycle coasting. Pawl contact has an analogy with the seatbelt episode, but this episode explains sustained overrunning and renewed drive, not emergency acceleration sensing and load restraint. No repeat of the existing lock, pump, cistern, stapler, music box or stitch cycle.

Selected freehub under --topic=auto: recognition strong (stopped pedals while cycling); curiosity strong (why wheel and pedals separate); proof strong (steep face versus ramp); causal depth workable (chain/input, pawl/tooth torque transfer, ramp/pivot/spring release, renewed engagement); discovery strong (hidden coupling); motion diversity workable (translation of chain, coupled rotation, pivoting, spring deflection); evidence strong (primary patent topology and manufacturer explanation); production scope workable in 16 shots. Derailleur is comparably rich but needs chain transfer in another spatial plane; kettle needs electrical/thermal dependencies; timer overlaps music-box gearing. Pencil/payung/closer are viable but less immediate than the chosen coasting question. Candidate evidence leads are retained in SOURCES.md; unselected candidates were not fully claim-verified.

## Hook choice, before script
1. “Pedalnya berhenti. Kenapa rodanya masih berputar?” Familiar exterior behavior; promise: show input/output separation and why teeth behave differently by relative direction.
2. “Bunyi klik saat sepeda meluncur itu datang dari mana?” Sound-led inspection; promise: show cyclic pawl depression and reset.
3. “Satu arah mengunci, arah lain lewat. Bagaimana bisa?” State comparison; promise: show the two tooth faces.
Recommended and selected: 1, agent choice under immediate automation, not human approval. It establishes recognizable context before the cutaway. SCRIPT.md was created only after this selection and the evidence check.

## Story contract
Central mystery: pedal stopped, wheel rotating. First discovery planned 5–10s: separate orange input and teal output rotate differently. Question chain: what connects chain to wheel → what contact passes drive → why does coasting avoid that stop → what resets the pawl → how does drive reconnect? Signature: a pawl approaching the steep tooth face, making contact, then moving the ring with it. Give a stable enlarged contact view; label slowed motion and illustrative spacing. Ending: same wheel/pedal contrast, with cutaway overrun showing the ramp pressing the pawl inward. Show original bicycle frame, rear axle and wheel center landmarks across views.

## Publishing targets
Inherited the entire board ACCOUNTS.json list without override:

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

Trypost preflight: Admin's Workspace / 01a171dd-5281-730d-af07-f2168d17add7; exact @dibalikbenda.id ID 01a172c9-3761-700a-9798-00febaa9fa90, connected. Caller publishes directly; requires_approval false. Instagram reel: one video, max 900s/314572800 bytes; max 2200 caption characters and 5 hashtags. Queue configured daily 10:00 Asia/Jakarta. Use queue next and save observed UTC/offset schedule; do not invent its date. Local upload endpoint authorized by --delivery=queue. Optional feed sharing retained; no separate cover upload required, use supported cover offset if supplied.

## State
Brief/research/script agent-verified under delegated authorization. No human approval claimed. Next: complete and visually verify static storyboard before any synthesis/animation; then audio, animation, checks, preview, render, package, queue verification and commit.
Preview: none started yet. Usage start read: session 64% remaining, weekly 52%; this is only a snapshot. Context7 tools unavailable in this session; installed project-local CLI contract and CLI help/docs are the execution references.

## Static storyboard verification
Agent-verified before synthesis/animation: 16 real styled scene poses, ordered HTML board, saved PNG1920x4248 with16 valid loaded images. Visually inspected every tile and full contact frame. Repaired drive contact (pawl remains extended on the radial stop face), removed overlapping ring labels, enlarged bearing detail and removed cropped labels; axial shell uses a rotation witness rather than translating. Board identities, large centered mechanism and lower captions retained. Static board at video/boards/storyboard.html and video/boards/storyboard.png. Current stage: audio in progress.

## Audio placement
One ElevenLabs eleven_v4 synthesis, root-env voice, native89.520s, 201 words. Original cache preserved. Derived pitch-preserving tempo=1.07855422 chosen only if native recording leaves insufficient observation time. Source at native tempo is retained. Every derived-master sample preserved across verified quiet splices; one final normalization targets-16LUFS/-2dBTP.15 verified acoustic cuts, integer30fps map; final master90s. Individual word timings are estimates reanchored to utterances, not independent forced alignment. 59 short caption groups. Existing media-use manifest inspected before frozen material cue reuse. Music absent intentionally. Listening unavailable; no auditory or phone-speaker approval claimed.

## Publishing target snapshot
publishing_targets:
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

## Production verification in progress
Audio stage verified: native cache preserved,201 script words mapped,59 caption groups,15 measured quiet seams and22 source-verified SFX clips applied. Animation built in16 editable scene sub-compositions. HyperFrames full gate passed with0 errors/warnings and no browser skip; independent30fps motion inspection2684 samples passed. Reviewed32 beat frames,15 seam strips and2 phone sheets. A read-only fresh visual reviewer identified no additional P0/P1 beyond the already fixed approach/contact seam and leader-label overlaps. Final narrow changes are being rechecked before preview/render. First discovery now starts3.3s because the short opening question needs only3.3s; the early reveal is intentional and preserves familiar context. No human approval or listening claim.

## Final preview and render authorization
Agent-verified final composition under delegated --automation: verification-delivery-check.json passed0 errors/warnings. Repaired diagnostic contact/reset/label frames inspected.22 effects include pawl reset cues snapped to observed30fps return events, not merely guessed word times. Current storyboardv2 is reconstructed from the corrected final composition with measured labels; original pre-audio stills/HTML/PNG retained under .hyperframes/artifacts/pre-audio-board, with boards/pre-audio-archive.json hashes. Preview created by this run, project=C:\Users\muhth\Documents\projects\content-pipeline\productions\freehub-roda-tetap-melaju\video, PID=27464, port=3002, URL=http://127.0.0.1:3002/#project/video; HTTP200 verified. Hold: render and export verification only, then stop before packaging/delivery. Pre-render authorization delegated, no human approval claimed.

## Verified export and content package
Final MP4 verified90s/2700frames,1080x1920,30fps,H.264/AAC; full decode and all16 decoded proof frames inspected. Export SHA-256 df42cc9402c74bfb8bcab9899782a520ab8a7ea6753ab7a08bdf7b9018e72596, 20732764bytes. Caption package matches all201 spoken words. CONTENT_PACKAGE.md includes3 titles, exact Instagram copy,5 hashtags, editorial keywords, local cover and verified delivery links.22 actual-export SFX/15 acoustic seams measured separately; no listening claim. Next: authorized direct upload and queue next for the saved exact board account; then receipt verification and commit.

## Preview cleanup
Pipeline-owned preview PID27464 on port3002 stopped through managed preview --stop. Status reread reports not-running. Get-NetTCPConnection found no listener on3002 and Get-Process found no27464. No preview retained; review/render hold ended before package and external delivery.

## Publishing endpoint complete
Trypost Local direct upload HTTP201; public served copy HTTP200 and full SHA-256/byte match. Exact @dibalikbenda.id account and607-character copy/5hashtags/media readback verified. Post ID01a17f0c-0f6f-7113-9945-7d70a4463dda; media ID01a17f0b-de30-7222-8ae0-dd5b840ef614; observed status scheduled, schedule_mode queue. Actual due UTC2026-10-30 03:00:00, Asia/Jakarta2026-10-30T10:00:00+07:00. Endpoint means scheduling complete, not published. Receipt: PUBLISHING.json. No future monitor authorized or held open. All requested pipeline stages complete. Next: requested Git commit; retain media locally under existing binary-ignore policy. Preview cleanup verified.

## Run closed
All requested pipeline and queue endpoint work completed. Git commit requested after endpoint; consult repository history and the delivery reply for its resulting ID. No further pipeline work or future publication monitor pending. Preview closed and signed upload descriptor removed from the OS temporary directory. Render emitted the optional HyperFrames desktop app download link; include it in delivery notes. One anonymous rating10 feedback sent under the HyperFrames skill workflow; no project source or media published by that feedback. Local binary media remains outside Git under the existing ignore policy; verified hashes and source metadata are retained.
