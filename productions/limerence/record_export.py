"""Mark export complete only after the encoded artifact and proof pass review."""
from pathlib import Path
import hashlib,json,re,shutil

prod=Path(__file__).resolve().parent
video=prod/'video'
summary=json.loads((prod/'exports/verification.json').read_text(encoding='utf-8'))['summary']
movie=prod/'exports/limerence.mp4'
assert movie.is_file() and movie.stat().st_size==summary['bytes']
assert summary['minimum_ssim']>.99 and abs(summary['duration_s']-85.366667)<.04
assert summary['decoded_proof_frames']==14
digest=hashlib.sha256(movie.read_bytes()).hexdigest()
(prod/'exports/limerence.mp4.sha256').write_text(digest+'  limerence.mp4\n',encoding='utf-8')
shutil.copy2(video/'verification/encoded/contact-sheet.jpg',prod/'exports/limerence-contact-sheet.jpg')

p=prod/'EPISODE.md'
s=p.read_text(encoding='utf-8')
s=re.sub(r'(?m)^- Stage: .*','- Stage: export; status: complete (approved final MP4 rendered and verified).',s,count=1)
s=s.replace('The authorized endpoint is a verified audiovisual preview; MP4 export awaits acceptance of that exact preview.',
    'The user approved preview v1 for MP4 export with “gas” on 2026-10-19; the final artifact is now verified.')
s=s.replace('## Final preview v1 — awaiting review','## Final preview v1 — historical review checkpoint (subsequently approved)')
s=s.replace('- No MP4 was exported. The original approved storyboard page, stills, and source poses remain preserved.',
    '- At this preview checkpoint no MP4 had been exported. The original approved storyboard page, stills, and source poses remain preserved.')
s=re.sub(r'## Next action\n[\s\S]*?(?=\n## Export authorization)',
    '## Next action\n\nDeliver the verified final MP4 and encoded contact sheet. No work remains within the approved export scope; external publication was not requested.\n',s)
s+='''
## Final delivery — 2026-10-19

- Artifact: [exports/limerence.mp4](exports/limerence.mp4), 6,433,118 bytes; H.264 High / yuv420p / BT.709, 1080×1920, 30 fps, 2,561 frames, exact container duration 85.366667 seconds. AAC stereo, 48 kHz, audio duration 85.366 seconds.
- Quality: HyperFrames delivery (high). The project pin moved from 0.8.173 to 0.8.174 after a freshness probe; the full check passed on 0.8.174 before rendering. No narration, layout, timing, or mix change was made for export.
- Render: drawElement capture with hardware GPU; 152.9 seconds wall time. All four built-in screenshot ground-truth comparisons passed. Render log: video/verification/render-delivery.log.
- Output verification: all 14 scene proof frames decoded from the actual MP4, inspected as a contact sheet; opening, charcoal, and closing frames also inspected full size. Preview comparison SSIM ranges 0.998466–0.999424, with sample timestamps rounded to the nearest 30 fps frame. This supports visual continuity across the CLI update and encoding, not byte-identical images.
- Audio: encoded stereo measures -15.53 LUFS / -1.88 dBTP. Its mono downmix measures -18.54 LUFS, matching the approved mono diagnostic mix (-18.49 LUFS) within 0.05 dB. The stereo integrated reading counts the duplicated channel energy; no audio gain revision was required.
- Proof: [encoded scene contact sheet](exports/limerence-contact-sheet.jpg), [metadata and comparison report](exports/verification.json), [SHA-256 checksum](exports/limerence.mp4.sha256).
- Local production is complete. No external publication was performed.
'''
p.write_text(s,encoding='utf-8')

p=video/'BRIEF.md';s=p.read_text(encoding='utf-8')
s=s.replace('Current authorized endpoint: verified audiovisual preview for review. MP4 export still requires acceptance of the final preview.',
    'The user accepted the final audiovisual preview with “gas” on 2026-10-19 and authorized MP4 export. The approved final MP4 is rendered and verified in ../exports/limerence.mp4.')
p.write_text(s,encoding='utf-8')
p=video/'STORYBOARD.md';s=p.read_text(encoding='utf-8')
s=s.replace('stage: preview\npreview_status: awaiting_review',
    'stage: export\npreview_status: approved\npreview_approved_date: 2026-10-19\nexport_status: complete')
p.write_text(s,encoding='utf-8')

p=video/'VERIFICATION.md';s=p.read_text(encoding='utf-8')
s+='''

## Approved final export — 2026-10-19

The user approved the exact presented preview v1 with “gas”. The CLI pin was upgraded from 0.8.173 to 0.8.174 as required by the freshness probe. Before rendering, the same full 28-time layout check and 300-sample / 31-assertion motion audit passed on 0.8.174 with zero errors/warnings; sampled contrast passed 35/35. The three previously reviewed informational connector heuristics are unchanged. Passing report: `.hyperframes/artifacts/checks/0e023850-ba63-4072-a53e-faf03501ef43.json`.

Render command: `npx hyperframes render --quality delivery --fps 30 --strict-all --output ../exports/limerence.mp4`. Result: exit 0, 6,433,118-byte MP4, 85.366667 seconds, 1080×1920, 30 fps / 2,561 frames, H.264 High / yuv420p / BT.709, AAC stereo / 48 kHz. DrawElement capture, hardware GPU, 152.9 seconds wall time. Four built-in drawElement-versus-screenshot self-verifications passed. An optional caption-overrides.json lookup returned a nonblocking 404; no authored resource failed and no override was needed.

`verify_export.py` decoded 14 proof frames from the actual MP4 and compared them with the approved preview stills at their nearest 30 fps timestamps. SSIM minimum 0.998466, maximum 0.999424. The encoded contact sheet and full-size frames 01/08/14 were visually inspected. Audio measures -15.53 LUFS integrated stereo / -1.88 dBTP. A unity-preserving mono downmix measures -18.54 LUFS versus the -18.49 LUFS mono diagnostic reference; the stereo difference is channel energy, not a gain change. No encoded audio clipping was measured.

Output metadata and comparisons: `../exports/verification.json`. Encoded proof: `verification/encoded/`, also copied to `../exports/limerence-contact-sheet.jpg`. The SHA-256 checksum accompanies the delivered file. No post-render HyperFrames lint/check/snapshot was run; verification examined the actual encoded artifact. Export is complete.
'''
p.write_text(s,encoding='utf-8')
tracker=prod.parents[1]/'TRACKER.json'
data=json.loads(tracker.read_text(encoding='utf-8-sig'))
row=next(x for x in data['productions'] if x['slug']=='limerence')
assert (tracker.parent/row['path']).is_dir()
row.update(stage='export',status='complete')
tracker.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'stage':'export','status':'complete','sha256':digest,'duration_s':summary['duration_s']}))
