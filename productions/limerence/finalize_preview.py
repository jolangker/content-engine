"""Record the verified preview checkpoint; do not encode or approve an export."""
from pathlib import Path
import json,re
prod=Path(__file__).resolve().parent
video=prod/'video'
report=video/'.hyperframes/artifacts/checks/5fa604a2-85d7-4a9b-8519-19e50bd5f957.json'
check=json.loads(report.read_text(encoding='utf-8'))
assert check['ok'] and check['motion']['enabled'] and check['motion']['ok']
live=json.loads((video/'verification/playback-check.json').read_text(encoding='utf-8'))['summary']
assert live['maxTime']>=85.3 and len(live['observedScenes'])==14 and len(live['observedCaptions'])==41
assert not live['pageErrors'] and not live['mediaErrors']

p=prod/'EPISODE.md'
s=p.read_text(encoding='utf-8')
s=re.sub(r'(?m)^- Stage: .*','- Stage: preview; status: awaiting_review (verified audiovisual preview v1 is ready).',s,count=1)
s=s.replace('Motion and captions are in production.', 'All 14 animated frames and 41 caption groups are verified.')
s=s.replace('- Future narration:', '- Resolved narration:')
s=s.replace('Narration is approved; defer synthesis until the visual storyboard checkpoint is accepted under the project\'s stage ordering.',
    'The approved narration was synthesized after the exact visual storyboard was accepted.')
s=s.split('## Next action')[0]+'''## Final preview v1 — awaiting review

- Studio review URL: http://localhost:3002/#project/video — persistent server, HTTP 200; the user can play and edit here.
- Exact composition: 85.366667 seconds, 1080×1920, 14 animated scenes, continuous Brian narration, 41 caption groups, two quiet SFX, no music bed.
- Full check passed: 16 HTML files, zero errors/warnings; runtime clear; 28 layout samples; 300 motion samples / 31 assertions; 35/35 sampled contrast checks. Three informational open-connector heuristics were visually reviewed.
- Full live 1× Studio playback reached 85.3406 seconds and the narration reached its complete 83.76 seconds. All 14 scene IDs and all 41 caption groups were observed across 274 samples, with no page or media errors. This is playback/timing evidence, not a human listening judgment of pronunciation.
- Proof: [frames 01–09](video/verification/animated-stills/contact-sheet-1.jpg), [frames 10–14](video/verification/animated-stills/contact-sheet-2.jpg), [playing Studio](video/verification/studio-playing.png), and [verification record](video/VERIFICATION.md).
- Studio's broader all-HTML lint scan also discovers the historical plain review page boards/storyboard.html and reports its absent composition ID. The mounted video passes the full CLI check. Preserve that approved review page; it is not a scene in the video.
- No MP4 was exported. The original approved storyboard page, stills, and source poses remain preserved.

## Next action

Present this exact audiovisual preview and ask for revisions or MP4 rendering, following the project's final-preview checkpoint. A new “cocok” approving this preview authorizes export of this version; do not ask again for the approved script, static layouts, or voice choice. For targeted revisions, change only affected dependencies and reverify. Preserve existing narration unless the narration itself is revised.
'''
p.write_text(s,encoding='utf-8')

p=video/'BRIEF.md'
s=p.read_text(encoding='utf-8').replace('Duration is estimated, not measured.',
    'The initial estimate was 90 seconds. Measured continuous narration is 83.76 seconds; the verified composition is 85.366667 seconds.')
p.write_text(s,encoding='utf-8')
p=video/'STORYBOARD.md'
s=p.read_text(encoding='utf-8').replace('stage: audio-and-animation','stage: preview\npreview_status: awaiting_review')
p.write_text(s,encoding='utf-8')
p=video/'VERIFICATION.md'
s=p.read_text(encoding='utf-8')+'''

## Live Studio playback

Studio opened the actual root composition with all 14 scenes and the caption composition registered. HTTP 200, no page errors; narration decoded at 83.76 seconds. A full 1× playback sampled 274 states through 85.3406 seconds, observed all 14 scene IDs and all 41 caption groups, and reached the end of the narration without page or media errors. Evidence: `verification/studio-ready.json`, `verification/playback-check.json`, and `verification/studio-playing.png`. This is a live playback/decoding test, not an auditory judgment of pronunciation or prosody.

Studio's all-HTML lint scan separately discovers the historical plain `boards/storyboard.html` review page and reports `root_missing_composition_id` there. That document is deliberately a review page, is not mounted by index.html, and remains preserved at its approved location. The full mounted-video check above passes with zero errors and warnings. No composition was changed to hide the review-page diagnostic.

Preview v1 is awaiting user review. The persistent server remains alive. MP4 export has not been authorized for this preview yet.
'''
p.write_text(s,encoding='utf-8')

tracker=prod.parents[1]/'TRACKER.json'
data=json.loads(tracker.read_text(encoding='utf-8-sig'))
row=next(p for p in data['productions'] if p['slug']=='limerence')
row.update(stage='preview',status='awaiting_review')
assert (tracker.parent/row['path']).is_dir()
tracker.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
json.loads(tracker.read_text(encoding='utf-8'))
print('Preview v1 recorded as awaiting_review. No MP4 export.')
