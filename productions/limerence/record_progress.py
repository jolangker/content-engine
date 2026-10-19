"""Reconcile durable production notes with the accepted layout and measured audio."""
from pathlib import Path
import json
prod=Path(__file__).resolve().parent
p=prod/'EPISODE.md'
s=p.read_text(encoding='utf-8')
s=s.replace('- Stage: storyboard; status: awaiting_review (styled static storyboard v1 is ready).',
    '- Stage: production; status: in_progress (approved layouts are animated against measured narration).')
s=s.replace('Estimated duration remains 90 seconds, not a measured result.',
    'The original planning estimate was 90 seconds; measured voice is now 83.76 seconds, yielding an 85.367-second composition.')
s=s.replace('The canonical [STORYBOARD.md](video/STORYBOARD.md) records `built` frames with `layout_approved: false`.',
    'The user approved this exact styled static version with “cocok” on 2026-10-19. [STORYBOARD.md](video/STORYBOARD.md) records `layout_approved: true`; animated frames retain those approved poses.')
s=s.replace('- No animation, audio synthesis, final video preview, or MP4 export has been generated. Styled layouts await review; plan approval does not imply layout approval.',
    '- Audio synthesis succeeded with the required ElevenLabs/Brian/eleven_v4 configuration. Motion and captions are in production. The authorized endpoint is a verified audiovisual preview; MP4 export awaits acceptance of that exact preview.')
s=s.replace('- Music and selective SFX remain proposals from the board; resolve only during the relevant stage.',
    '- Audio direction resolved: no music bed, preserving the quiet spoken reflection; two soft bundled ticks support observed-action examples. No suitable cached BGM candidate was found and no alternate music provider was silently selected.')
s=s.replace('The styled-static pass is complete and awaiting review: all 14 frames use the approved local fonts and palette. Inspected snapshots come from the mounted HyperFrames index. The project requires visual-board acceptance before animation and the later audio stage; generic permission to run audio in parallel does not remove that checkpoint.',
    'The styled-static pass was completed and then accepted by the user with “cocok” on 2026-10-19. All 14 frames use the approved local fonts and palette. The original review page and stills remain historical evidence; approved-static/ retains the source poses. Animation was authorized by that acceptance.')
s=s.split('## Next action')[0]+'''## Audio and animation execution — 2026-10-19

One continuous narration request used ElevenLabs Brian (`nPczCjzI2devNBz1zQrb`) and `eleven_v4`, with delivery tags. The shared audio wrapper failed internally without returning voices; documented direct SDK `convert_with_timestamps` with MP3 output succeeded using the same key, provider, voice, and model. Original speech is preserved. The native alignment contains all 180 approved words in exact order after punctuation normalization. Captions contain spoken text only.

The original MP3 is 83.76 seconds. A 48 kHz PCM mix copy normalizes loudness without time stretching; measured -18.48 LUFS integrated, -1.99 dBTP, LRA 2.0. Voice starts at 0.4 seconds. Scene boundaries are mechanically derived from native alignment and snapped to 30 fps. The composition ends at 85.366667 seconds, within the board's 85–95 second range.

The assembly has 14 scene sub-compositions, one continuous narration track, one caption sub-composition containing 41 groups, and two quiet SFX cues. All 180 words are represented once in captions. Motion uses staged phrase reveals and measured SVG traces; dashed imagined connections retain their dashed appearance. No camera move or B-roll is introduced.

## Next action

Verify all animated frames, inspect representative stills and caption/scene boundaries, then open the full audiovisual Studio preview. Record preview awaiting_review and ask for changes or MP4 rendering. Preserve the exact approved narration and layouts. Final preview approval remains required before MP4 export.
'''
p.write_text(s,encoding='utf-8')
video=prod/'video'
verification=video/'VERIFICATION.md'
v=verification.read_text(encoding='utf-8')
v=v.replace('# Styled static storyboard — verification','# Verification record\n\n## Historical styled static storyboard verification')
v=v.replace('Scope: 14 styled static compositions and the review page. No animation, synthesized audio, or MP4 has been produced.',
    'Historical scope: 14 styled static compositions and the review page. At this checkpoint no animation, synthesized audio, or MP4 had been produced.')
v=v.replace('The styled layouts presented here await user review. `built` in STORYBOARD.md means a posed composition and inspected still exist; `layout_approved: false` preserves the unapproved state.',
    'The styled layouts were subsequently accepted by the user with “cocok” on 2026-10-19. The current STORYBOARD.md records `layout_approved: true`. At the original static checkpoint, `built` meant a posed composition and inspected still existed.')
verification.write_text(v,encoding='utf-8')
print('Production and approval history reconciled.')
