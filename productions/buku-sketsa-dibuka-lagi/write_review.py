"""Record actual checks and the accepted final-look evidence."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification'
c=json.loads((Q/'hyperframes-check.json').read_text(encoding='utf-8'));assert c['ok']
seek=json.loads((Q/'seek-consistency.json').read_text(encoding='utf-8'));assert seek['same_state_after_reverse_seek']
preview=json.loads((Q/'preview-report.json').read_text(encoding='utf-8'));assert preview['status']==200 and not preview['errors']
text='''# Final-look review — v1, agent verification

The film follows one fictional reopened sketchbook from mismatched sales advice to asking about the partner's desired creative self and offering relevant practice time. The supporter remains the viewer, the brick participant remains the aspiring artist. The chosen sketchbook interaction provides stronger continuity than the rejected single overhead split-page film; a future gallery success opening was rejected because it implies an unsupported outcome. The board's cream/serif identity is explicitly inherited, not a new styling default.

## Evidence and repairs

The complete 16-scene static storyboard was captured and inspected before synthesis. All 16 full-size scene stills and the 1440x3183 combined PNG loaded and were ordered correctly. Four semantic phases for every scene were inspected in verification/motion-sheet-1.png through motion-sheet-4.png; review beat/phone/seam sheets are enumerated in verification/review-manifest.json. Final visual evidence includes all 64 phases and all 15 boundaries. No text clipping, caption collision, blank composition or unexpected palette change remained. Exactly 08/11 are charcoal; series chrome retains its geometry. Price-tag, paired curved book pages, plant sketch, pencil, clock and actor-owned speech outlines read at phone size.

Fresh-agent review, based only on storyboard and three sheets, found no P0 and one P1: round actors/table overlap and detached pencil left drawing/support overly dependent on narration. P1 at sampled 2.784/19.367/80.483/86.750s → added restrained brick reaching gestures in 01/04/06/14/15/16 and moved supporter left/outside the work area in shared-table views. Actor contours/colors, book, palette and narration remain unchanged. Pre-repair sources retained in verification/pre-gesture-source.json. Complete static board recaptured at measured timing; affected poses and final motion re-inspected after repair. Small speech-space glyphs intentionally draw in over 0.6–0.9s and are not clipped objects. No open P0/P1.

## Technical result and intentional warnings

Pinned HyperFrames 0.9.1 full check passes: runtime, layout, motion, contrast and audio have zero errors. Ten lint warnings are the analyzer's repeated selector string path,circle,line,rect within separately scoped SVG groups; actual paths are distinct, with no shared target. Forward/reverse seeking to 18 sampled moments gives identical active scene SVG transforms/opacity/path states, supporting the retained deterministic behavior. Sixteen craft warnings concern approved fixed chrome at 26px versus the generic 28px floor; keep board identity as required. Main emphasis is 76–82px and captions 46px. No broad ignore attributes hide actual content issues.

The internal editor preview returned HTTP200, no page errors, and progressed through the complete 90.03333s film with narration/SFX media ready and no media error. Project preview ownership is in verification/preview-owner.json; release after verified export. The HyperFrames desktop app can edit this local project if desired; the pipeline-owned temporary preview is not kept open after export.

Fifteen acoustic boundaries were measured inside decoded quiet intervals, with integer 30fps visual anchors. One ElevenLabs eleven_v4 recording, 187 spoken words, 76.8 native seconds; source speech is not sped up. Quiet-region pause insertion and final normalization yield 88.50008s placed narration and a 90.03333s composition. Individual word timestamps remain estimates; all 187 words are in 49 caption groups. POV check includes audible Lo bisa tanya / Misalnya dia menjawab / Setelah dengar jawabannya, lo bisa cues.

Six sparse material SFX are planned, provenance/hash checked and placed against actual motion. No BGM: avoid prescribing an emotional response to the partner's aspirations. Dramatic 08/11 and final hold have no SFX. Acoustic levels and export cue presence are objective measurements; perceptual listening was unavailable and is not claimed. Encoded MP4 verification is required separately after render.

## Weakest shot and limits

Scene 11's unfinished plant is a restrained illustration of an ongoing step, and is visually less specific than the full sketchbook scenes. More authored practice marks could enrich it, but no success meter or guaranteed outcome is warranted. Organic faceless actors are inherited board vocabulary. This review checks composition/semantic states and numerical motion/audio evidence; it does not establish how a human listener experiences pronunciation, pacing or the mix.

## Authorization

Agent accepts this final look under the user's immediate --automation instruction, including delegated pre-render authorization and queue delivery. No human approval claimed. Render exactly the verified current source; content package and scheduling follow actual export checks.
'''
(V/'REVIEW.md').write_text(text,encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('\n## Final-look acceptance\n\nAgent repaired the fresh reviewer P1 with partner reaching gestures and supporter spacing; static board and affected motion re-inspected. Full check, phone/motion/seam sheets, complete preview playback and forward/reverse seek pass. Final look accepted under delegated automation; human_approval=false. video/REVIEW.md records retained warnings, weakest shot and the unavailable perceptual listening. Next: render and inspect encoded export.\n')
print(json.dumps(dict(agent_verified=True,human_approved=False,composition_sha256=hashlib.sha256((V/'index.html').read_bytes()).hexdigest())))
