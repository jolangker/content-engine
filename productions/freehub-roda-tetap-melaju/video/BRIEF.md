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
