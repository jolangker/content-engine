# Stapler: siapa yang menekuk kakinya?

- Board: [Di Balik Benda v4](../../boards/di-balik-benda/DIRECTION.md), [editorial](../../boards/di-balik-benda/EDITORIAL.md), [visual specification](../../boards/di-balik-benda/frame.md).
- topic_selection: auto, explicitly delegated by --topic=auto.
- execution_policy: automation; automation_after: none; automation_state: active; human_review: none.
- pre_render_authorization: delegated by the user's --automation instruction.
- Requested endpoint: publishing; delivery: queue; schedule: next configured account slot, Asia/Jakarta (daily 10:00); no custom --at.
- Audience/language/output: curious general audience, Indonesian, 1080x1920, 30 fps, 90 seconds.
- Scope: one direct-action manual desk-stapler cycle, stationary inward-clinching anvil. Not a spring-powered release stapler, flat-clinch moving anvil, or staple gun.
- Audio: ElevenLabs eleven_v4, default voice resolved only from root .env; tagged full-script request. Event SFX required, no BGM to separate fine contact cues from speech.
- Medium: board-v4 2.5D only; original editable SVG with side faces, metal shading, consistent light, layer order; stationary base and anvil. Labels and force arrows are flat support.
- Storyboard override: pre-audio styled stills + HTML + full PNG required; agent verification, no human approval.
- Mechanical source limitations: schematic geometry, enlarged wire/clearance, compressed depth; not a measured product replica. Same variant throughout. Anvil groove angles and sheet capacities are not claimed.

## Topic decision
Candidates: stapler cycle; bicycle pawl freehub; reversible socket ratchet; automatic umbrella; mechanical kitchen timer; manual can opener; hydraulic door closer; inertial seatbelt reel; soap dispenser; crank pencil sharpener.
Chosen stapler balances feed/rotation/translation/penetration/plastic bending/return, primary patent support and a legible 90-second cycle. Freehub/ratchet concentrate on tooth contact; umbrella/timer need more variant geometry; door closer/seatbelt need tighter variant and domain boundaries; soap pump overlaps sprayer. Other candidates remain evidence leads, not verified scripts.
Overlap: tracker read, all production folders inspected including orphan roda-beda-putaran (no EPISODE.md). Prior board episodes cover lockstitch, cylinder lock, trigger sprayer and toilet cistern; none covers stapler. Historical v1 pen/zipper/clothespin/cable tie also differ. No related production overwritten.

## Hook selection
1. Kita menekan dari atas. Tapi siapa yang menekuk kaki staples di bawah kertas? — Hidden actor under a familiar action; chosen: direct payoff at the anvil.
2. Satu staples masuk. Staples berikutnya langsung siap. Apa yang mengaturnya? — Automatic feed, less direct to the strongest macro.
3. Kawat lurus ini berubah jadi pengunci kertas. Ikuti perjalanannya. — Material journey, clear but less curiosity.

Selected 1 under delegated automation, after source verification and before drafting SCRIPT.md.

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

Preflight: exact workspace/account connected; caller publishes directly; instagram_reel permits 900 s / 300 MiB, max 5 hashtags, 2200 characters. Queue schedule configured daily 10:00 Asia/Jakarta. Live tools read before synthesis.

## Intake state (historical)
Brief/research/script agent-verified. Storyboard in progress. No preview server started. Starting unrelated changes: TRACKER.json includes gua-kira-udah-kelihatan and that production directory is untracked; exclude from requested commit.

Storyboard agent-verified: 16/16 styled frames, boards/storyboard.html and boards/storyboard.png (1920x4248), all images loaded and ordered. Full PNG inspected before synthesis. Macro crop repaired to keep the force marker out of the heading. Static lint passed 0 errors/0 warnings. Physical chain and two detail views checked; s08-s10 progress one stroke, s11 is purposeful force-path replay. Human approval remains unset.

## Final look / preview ownership
Narration: ElevenLabs eleven_v4, voice 3mAVBNEqop5UbHtD8oxQ from root .env, native 88.64 seconds; 197 aligned spoken words. No resynthesis or tempo change. Measured timing in video/timing.json, 58 caption groups and 19 SFX cues. Motion verification passed 2723 local output-frame samples, fixed-anvil and wire-length checks, reverse seeking. See video/REVIEW.md for visual review and honest auditory limits.
Preview created by this pipeline at C:/Users/muhth/Documents/projects/content-pipeline/productions/stapler-kaki-menutup/video; PID 27404, port 3002, Studio http://127.0.0.1:3002/#project/video, HTTP 200. Retention reason: final look and render. Release condition: verified export, before packaging.
Agent-verified final look v1 under delegated --automation render authorization; human approval unset.

Audio timing correction: waveform matching found the streaming loudness filter shifted speech by about 0.407 s relative to planned captions. Replaced it with measured static gain and sample-indexed padding, retaining native narration. Five native/placed comparisons now correlate above 0.9999999 at the exact 450 ms offset. The first intermediate export is superseded; delivery is re-rendered from the corrected composition. No paid resynthesis.

## Verified export and package

v1 a647a767be0cc6ddb6f972877c29f42d2ba950b05981b009f16cde76d94f429a, 6360523 bytes; 90.000 s, 2700 frames, 1080x1920, 30 fps, H.264/AAC. Full decode and waveform checks passed, 19 SFX cues verified in export. CONTENT_PACKAGE.md, cover, SRT and VTT match. Agent-verified under automation; no human or perceptual listening approval. Next: queue delivery then scoped commit.

Preview released after export verification: managed stop succeeded; status not-running; port 3002 has no listener and PID 27404 no longer exists. No retained preview hold. Final mix is -16.92 LUFS / -1.83 dBTP; all 19 cues matched at 0.000s export offset. Picture stream remains identical after audio-only assembly. Final export frames visually inspected; package ready, queue delivery authorized.

## Queue delivery complete

Trypost post `01a174bf-6b0c-7375-a1f0-f1d2e4640cd2` read back as scheduled, queue mode, exact Instagram @dibalikbenda.id account, one 90-second video. Actual schedule: 2026-10-27T10:00:00+07:00 (Asia/Jakarta), 2026-10-27T03:00:00+00:00 UTC. Public served copy HTTP 200, SHA-256 and 6360523 bytes match final export. Caption differs only in LF→CRLF transport endings; both payload hashes retained. [Receipt](PUBLISHING.json). This is scheduled, not a claim of publication. No preview remains. Next: scoped commit requested by the user.
