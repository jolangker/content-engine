# Tape measure: spring and brake

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
schedule: next configured slot, Asia/Jakarta
commit: after pipeline completion; only changes from this run

## Production brief
Indonesian, 90 seconds, 1080x1920, 30fps, for curious general viewers. Original layered 2.5D sectional illustrations. Selected brake variant: US5806202A guided resilient tongue with follower pins, descending guide, detent and bearing ribs. A conventional spring-return reel is shown schematically, not claimed as an exact spring drawing from that brake patent. Axial separation is explicitly labelled. No universal claim about every tape measure. Spring geometry and timing are explanatory and not to scale. Hook calibration, blade curvature, bumper internals and manufacturing are outside scope.
Inherit [editorial](../../boards/di-balik-benda/EDITORIAL.md), [frame](../../boards/di-balik-benda/frame.md), and [shots](../../boards/di-balik-benda/SHOT-DIRECTION.md). Manrope 800 titles, Manrope 600 46px captions at y1500, IBM Plex Mono labels. Canvas #ECEEE9, ink #172B3B, orange input, blue active mechanism, teal output. Visible mechanism stage x80..1000, y430..1410. Captions retain the explicit board placement. Technical drawings become original shaded layered illustrations, not flat patent plates.
Narration: one continuous ElevenLabs eleven_v4 recording, delivery tags, board-aware root-env fallback. SFX: existing licensed library and frozen historical material cues. BGM intentionally absent to expose the small contacts and winding cues. No new SFX generation. Automated verification replaces human gates; listening limitations must be stated.

## Delegated topic selection
The following are provisional editorial proposals, not researched mechanism claims. All eight board criteria were evaluated. strong/workable/weak judge editorial feasibility, not retention.

| Candidate and short brief | Recognition | Question | Visual proof | Causal depth | Discovery | Motion | Evidence | Scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tape measure: why return yet stay locked? Investigate spring, reel and brake. Selected. | strong: household tool | strong: two opposing behaviours | strong: clamp versus recoil | strong: four handoffs | strong: spring separate from blade | strong: rotate/slide/flex | workable: patent leads | workable: single lock cycle |
| Toaster: what releases the carriage? Trace a selected latch cycle. | strong | strong | strong | strong | strong | strong | workable | workable: timer variant needed |
| Automatic umbrella: how does a button open it? Investigate runner and telescopic linkage. | strong | strong | strong | strong | strong | strong | workable | workable: dense geometry |
| Salad spinner: why does the basket keep spinning? Examine push drive and free motion. | workable | strong | strong | strong | strong | strong | workable | workable |
| Can opener: how do feed wheel and cutter cooperate? Follow one bite and advance. | strong | strong | strong | strong | strong | strong | workable | workable |
| Bicycle bell: how does a thumb movement ring repeatedly? Follow drive and striker. | strong | strong | strong | workable | strong | strong | workable | workable: music-box novelty lower |
| Ratchet screwdriver: why return without reversing the screw? Inspect pawl selection. | strong | strong | strong | workable | strong | workable | workable | workable: freehub overlap lower priority |
| Door closer: what slows the closing stroke? Investigate spring, piston and oil route. | strong | strong | strong | strong | strong | strong | workable | workable: valve variant needed |
| Correction tape: how do supply and take-up reels cooperate? Trace transfer onto paper. | strong | strong | strong | strong | strong | strong | workable | workable: friction drive needs source |
| Pump soap dispenser: how is it refilled after pressing? Investigate piston and valves. | strong | strong | strong | strong | strong | strong | workable | weak novelty: sprayer overlap |

Selection: tape measure has an immediately recognizable contradiction and a visible answer through distinct reel/spring/guide/clamp interactions. Tracker and all production folder names checked, including unregistered legacy folders. No tape-measure episode exists. Freehub and seatbelt share reels/locking but answer different questions through different mechanisms. No existing production was resumed or overwritten.

## Research outcome
Jina search failed with exhausted quota; SearXNG and Context7 tools are unavailable in this session. Used available web search and opened primary patent bodies and drawing pages. Evidence and qualifications in SOURCES.md. No claim is based only on a search snippet.

## Three hooks, before script drafting
1. “Pita meteran ditarik, lalu kembali sendiri. Tapi saat tombol dikunci, kenapa pitanya bisa diam?” Two familiar states, directly demonstrated. Selected under --automation.
2. “Tombol meteran ini tidak menggulung pitanya. Jadi, siapa yang menariknya masuk?” Contrast between actuator and energy source; supported but less immediate visually.
3. “Di dalam meteran, pegas dan pengunci bekerja berlawanan. Bagaimana keduanya mengatur satu pita?” Accurate system framing, but front-loads part names.
Recommendation and delegated choice: 1. Recognition first, then progressive discovery. Selection recorded before SCRIPT.md was created; no human approval claimed.

## Story contract
Central mystery: why does a self-returning blade stay extended when locked? First discovery: reveal separate spring/reel at approximately 8s. Question chain: what pulls it back? → where does energy come from? → how does the slider reach the blade? → what keeps the clamp engaged? → what changes when released? Signature interaction: guided pin crosses the detent while the tongue flexes and clamps the blade; settle camera, show approach/contact/flex/hold at large scale. Opening and ending use identical housing, blade and button landmarks. Ending exposes the spring and clamp while repeating pull/hold/unlock/return.

## Script verification
Read the complete spoken sequence against source scope: no unsupported universal lock claim, no claim that the visible blade itself provides all recoil, no invented ratchet, no motor, and no implication that the slider powers rewind. Exact brake example identified before internal detail. Technical names follow function. Narration and visual text are separate. All choices agent-verified under delegated authorization.

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
Live preflight: Admin's Workspace matches ID, @dibalikbenda.id connected, direct publishing permission, daily05:00 Asia/Jakarta schedule. Requested queue is explicit authorization.

## Storyboard verification
Agent-verified before audio/animation: 16 styled scene stills, boards/storyboard.html and complete 1920x4248 boards/storyboard.png. All images loaded, IDs/order match. Saved PNG opened and all16 inspected. Fixed blade/hook length, moving external pad, contact arrow anchoring and text encoding. Spring detail is a front chamber opened in section, not literal separated parts. Layered metal thickness and housing landmarks retained. No human approval claimed.

## Audio placement
One ElevenLabs eleven_v4 synthesis, root-env voice, native107.760s, 240 words. Original cache preserved. Derived pitch-preserving tempo=1.29831325 chosen only if native recording leaves insufficient observation time. Source at native tempo is retained. Every derived-master sample preserved across verified quiet splices; one final normalization targets-16LUFS/-2dBTP.15 verified acoustic cuts, integer30fps map; final master90s. Individual word timings are estimates reanchored to utterances, not independent forced alignment. 75 short caption groups. Bundled media-use manifest inspected; separate cue planning will copy frozen material assets. Music absent intentionally. Listening unavailable; no auditory or phone-speaker approval claimed.

## Preview ownership
Created by this pipeline: C:\Users\muhth\Documents\projects\content-pipeline\productions\meteran-pegas-dan-rem\video; PID 26420; port 3002; http://127.0.0.1:3002/#project/video. HTTP200 verified. Hold through final look and delivery render. Stop and verify PID/port released after encoded-export verification, before packaging/delivery. HyperFrames desktop app can edit the source project later.

## Final look and render authorization
Final check0errors/0warnings; mechanical2684frame/reverse-seek and10continuity checks pass. Corrected guide/touch/snap/clamp sequence is continuous, final arrow follows actual motion, restoring torque labelled. Final beat,phone and seam sheets inspected. See video/REVIEW.md. Agent-verified under --automation; human_approval:false. Delivery render authorized by user policy.

## Final storyboard refresh
After continuity/arrow repairs, rebuilt all16 stills, HTML and full PNG from measured final-composition midpoint frames. Initial pre-audio board preserved in video/boards/initial. Final saved1920x4248PNG opened and inspected:16ordered scenes, legible captions, macro contact states and matched whole-tool proof. No missing images.

## Preview cleanup
Managed preview stopped successfully after export verification. Final status:not-running. PID26420 and port3002 ownership checked separately before packaging. Export audio:-13.6LUFS-I,-1.4dBTP,0clipped samples; no auditory approval claimed.

## Verified export and package
v1 MP4, cover and caption sidecars verified. CONTENT_PACKAGE.md matches export SHA256 96d70134a86073d9b3e76be7b339ceb6f429d9cac9fc25d69b2e41bbe92319a6. Requested queue, one inherited Instagram target. Receipt prepared before upload/write; no duplicate post creation authorized.

## Delivery complete
Trypost Admin's Workspace; Instagram @dibalikbenda.id; post 01a19df1-1b07-7264-b2e9-78efedf4d3c5; provider status scheduled, schedule_mode queue. Returned UTC 2026-11-02 22:00:00 = 2026-11-03T05:00:00+07:00. Not yet published; no social URL returned. Public served media HTTP200, exact10095403bytes and SHA256 matches local export. Exact caption/account/type/media read-back passed. Receipt: PUBLISHING.json. Preview cleanup verified:not-running, PID26420 absent, port3002 has no listener. Pipeline endpoint queue is complete. Next action: none; future publication monitoring is outside this run. Commit only this production and its tracker row, preserving pre-existing workspace changes.
