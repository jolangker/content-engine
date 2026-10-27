"""Write a human-readable verification record from actual retained evidence."""
from pathlib import Path
import hashlib
import json
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification'
check=json.loads((Q/'hyperframes-check.json').read_text(encoding='utf-8'));preview=json.loads((Q/'preview-report.json').read_text(encoding='utf-8'));export=json.loads((Q/'export.json').read_text(encoding='utf-8'));sound=json.loads((Q/'sound-design-export.json').read_text(encoding='utf-8'));board=json.loads((V/'boards/verification.json').read_text(encoding='utf-8'))
assert check['ok'] and sound['status']=='passed' and preview['status']==200 and not preview['errors'];assert preview['playback_samples'][-1]['timelines']['main']==90
assert all(a['error'] is None for s in preview['playback_samples'] for a in s['audio']);assert board['count']==16
report=f'''# Verification — Coba hal baru berdua v1

## Editorial and evidence

One fictional couple tries cooking together to illustrate self-expansion. English concept and Indonesian meaning are spoken in Line 2. Approximately half the narration develops the explanation, the shared task and the research boundary; one mutual experiment follows. Hook 1 and the closing question connect the routine to trying something small. Research claims map to SOURCES.md; the original 2000 abstract was read via Europe PMC and theoretical context via the open review. Short-term ratings are not presented as durable benefit or treatment. No unsupported statistics, diagnostic labels or motive judgments.

## Static storyboard and creative review

Sixteen scene stills were captured from the actual assembled static composition before synthesis and animation. boards/storyboard.html loads all sixteen 1080×1920 images in order; full-page PNG is {board['width']}×{board['height']}. The saved PNG was opened and visually reviewed. Fonts, palette, short selective emphasis, caption band, fixed chrome and the two silhouettes match canonical board v1.2. Fourteen cream frames and two charcoal turns (8 discovery, 10 research limit) are present. The varied overhead table, large single participant, pair/path, repeated dinners, bowl close-up, countertop, viewpoint, bounded finding, separate issue, selection, invitation, alternatives, reflection, result and ending provide differing focal geometry and density. No generic card or text-only repetition.

## Motion and preview

Four actual seek poses per scene (64 total) were captured and all four motion sheets opened. Every scene develops an opening state plus three semantic changes; not just subtitle replacement. Storyboard geometry and stationary chrome persist. Caption phrases remain inside y1550–1740 with no text collisions. Complete Studio playback reached 90 seconds, eighteen five-second progression samples, no page errors or media errors. Narration loaded and progressed continuously; SFX presence is verified independently below.

The full HyperFrames 0.8.200 check passed: 309 layout sample states, zero errors; layout, runtime and explicit motion assertions passed; {check['contrast']['passed']}/{check['contrast']['checked']} text contrast checks passed. Nine static-analysis warnings conflate the same descendant-selector string in separate beat-local SVG groups; the groups and matched paths are disjoint, and actual four-phase poses verified their independent state. Sixteen type-floor warnings refer to approved fixed 26px series chrome, which is intentionally retained under the board contract. Studio's broad file scanner additionally treats the unassembled storyboard page and canonical HTML chrome fragment as compositions; the assembled render graph check has zero errors. These are reviewed tooling limits, not hidden composition failures.

## Audio and encoded file

One continuous ElevenLabs eleven_v4 request, root .env voice, 193 exact aligned spoken words; tags excluded from captions. Native recording 82.96s; 5.84s explicit editorial pauses; placed normalized voice 88.8s; 1.2s final visual hold. No time stretching. Six frozen licensed board cues follow the actual dinner, route, spoon, kneading, shared choice and plates; no BGM. Sound plan sources, timing and motion hashes match the placed tracks. Export cue waveform verification status: {sound['status']}.

Final file: {export['file']}. Actual duration {export['duration_s']}s, {export['width']}×{export['height']}, {export['fps']}fps, {export['frames']} frames, H.264 {export['pixel_format']} with AAC. Full decode passed. Encoded level: {export['loudness']['input_i']} LUFS / {export['loudness']['input_tp']} dBTP. Bytes {export['bytes']}; SHA-256 {export['sha256']}. All sixteen representative frames were decoded from the actual MP4 and inspected in exports/export-proof.png.

Direct perceptual listening was unavailable. Objective alignment, decoder, level, player progression and cue waveform evidence do not establish subjective performance or mix balance; no human listening approval is claimed. This limitation was disclosed during the run. Automated checks and visual final-look verification authorize export under the user's --automation, not fabricated human approval.

## Evidence paths

- video/boards/verification.json and storyboard.png
- video/verification/hyperframes-check.json
- video/verification/choreography.json, motion-sampling.json and motion-sheet-1…4.png
- video/verification/preview-report.json
- video/verification/export.json and sound-design-export.json
- video/timing.json, placement.json, sound_design.json
- exports/export-proof.png and coba-hal-baru-berdua.srt
- video/verification/preview-cleanup.json after release

Packaging and Trypost receipt must use the exact export hash above. Successful scheduling establishes a queued post, not a live publication.
'''
(P/'VERIFICATION.md').write_text(report,encoding='utf-8');print(json.dumps(dict(status='passed',export_sha256=export['sha256'],sound=sound['status'],duration=export['duration_s'])))
