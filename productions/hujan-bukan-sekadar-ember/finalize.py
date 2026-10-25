from pathlib import Path
import json,re,hashlib
P=Path(__file__).resolve().parent;V=P/'video';R=P.parents[1]
report=json.loads((V/'verification/export/report.json').read_text(encoding='utf-8'))
receipt=json.loads((V/'verification/audio-correction/receipt.json').read_text(encoding='utf-8'))
assert receipt['video_unchanged']
assert hashlib.sha256((P/'exports/hujan-bukan-sekadar-ember.mp4').read_bytes()).hexdigest()==report['sha256']==receipt['output_sha256']
assert (P/'exports/hujan-bukan-sekadar-ember.srt').exists()
assert (V/'boards/storyboard.png').exists() and (V/'boards/storyboard-planning-v1.png').exists()
sound=json.loads((V/'sound_design.json').read_text(encoding='utf-8'))
sound['export_verification']={'path':'verification/export/report.json','correlation':report['mix']['expected_mix_correlation'],'cue_presence':'passed','audio_correction':'verification/audio-correction/receipt.json','static_rain_gain':1,'lane_peak_gain':.09,'reason':'Pinned engine multiplies static gain and volume lane. Unity baseline preserves the planned lane. Final audio was processed and muxed by the same pinned HyperFrames engine; encoded video hash is unchanged.'}
(V/'sound_design.json').write_text(json.dumps(sound,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
story=(V/'STORYBOARD.md').read_text(encoding='utf-8');plan=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'))
for i,t in enumerate([12.8,18.5,33,44,63,71.4]):
    pattern=rf'(## Frame {i+1} — .*?)(?=\n## Frame |\Z)';m=re.search(pattern,story,re.S);b=re.sub(r'- poster: [^\n]+',f"- poster: {t-plan[i]['start']:.4f}s",m.group(1));story=story[:m.start()]+b+story[m.end():]
story+='\n## Final artifact version\n\nFinal aligned board uses six stills extracted from the verified 84.7s export. The pre-audio planning board remains at boards/storyboard-planning-v1.html and boards/storyboard-planning-v1.png, with its original six poses in boards/stills/. The latest boards/storyboard.html and boards/storyboard.png show final scene coverage and measured timings. Agent verification applies; no human approval is claimed.\n'
(V/'STORYBOARD.md').write_text(story,encoding='utf-8')
review=V/'verification/REVIEW.md';text=review.read_text(encoding='utf-8')
text=text.replace('Pending replacement render. The verification script will decode the actual export, inspect metadata and black frames, measure audio loudness, reconstruct narration and the rain envelope from their source tracks, compare the exported mix, and extract final-video proof frames. Completion remains pending until those files and checks succeed.',f'''Verified final export: 84.7s, 1080x1920, 30fps, 2541 H.264 yuv420p frames, AAC 48kHz stereo, {report['bytes']} bytes. Full decode passes, zero black segments. Measured integrated loudness {report['audio']['loudness']['input_i']} LUFS and true peak {report['audio']['loudness']['input_tp']} dBTP. Native speech offset is recovered with zero sample lag; the narration/rain model correlates {report['mix']['expected_mix_correlation']:.6f} with the exported audio. Mono voice duplication into stereo accounts for the different fitted source coefficients; this is an objective cue-presence check, not subjective listening.

The first export check caught double attenuation of rain: the pinned engine multiplies static gain by the volume lane. The rain static gain was corrected from 0.09 to 1, retaining the intended 0–0.09 envelope. The exact pinned HyperFrames engine's processCompositionAudio and muxVideoWithAudio functions regenerated the audio and copied the encoded video stream without any re-encoding. Stream hashes before and after match. The original render and correction receipt remain in verification/audio-correction/. The current index and reproducible assembler carry the corrected gain. No voice synthesis or frame rendering was repeated for this correction.

Twelve proof frames extracted from the final MP4 and the final six-frame 1560x2237 board were opened and visually inspected. All scene images load; names/order agree. Frame captions, first-flush fill/bypass/reset, open/closed tank, comic visitor, overflow route and watering-can contact remain visible. The initial pre-audio board is retained separately. All verification is agent work under delegated authorization; the audio-listening limitation above remains.

Final SHA-256: {report['sha256']}. Full report: verification/export/report.json.

Preview cleanup: pinned preview --stop returned stopped; status returned not-running. A direct TCP listener query for port 3002 returned no listener, so recorded PID 28552 no longer owns that port. Capture-board helper browsers close in finally; no pipeline preview is retained.''')
review.write_text(text,encoding='utf-8')
episode=P/'EPISODE.md';text=episode.read_text(encoding='utf-8')
text+='''
## Current state — export complete

- Requested endpoint `export` is complete under active automation. No content package, hosting or publication was performed.
- Final file: [exports/hujan-bukan-sekadar-ember.mp4](exports/hujan-bukan-sekadar-ember.mp4), 84.7s, 1080x1920, 30fps, H.264/AAC, 26,047,542 bytes.
- Captions: [exports/hujan-bukan-sekadar-ember.srt](exports/hujan-bukan-sekadar-ember.srt), 66 groups covering all 183 spoken words; captions are also burned into the MP4.
- SHA-256: f0f4605d261edd47354686641dbddfe2d31b09502a61ec1d8d1770246efcb0d1.
- Verified full decode, zero black segments, source-aligned speech and rain cue presence. Final frame and full-board visual inspection passed. See [review](video/verification/REVIEW.md), [export report](video/verification/export/report.json) and [audio correction receipt](video/verification/audio-correction/receipt.json).
- Final storyboard: [HTML](video/boards/storyboard.html), [PNG](video/boards/storyboard.png). Six ordered final-video stills, 1560x2237 board, all images valid and saved PNG visually inspected. The earlier planning version remains at `video/boards/storyboard-planning-v1.*`; it was verified before audio/animation. Final refinements are represented in the latest board.
- Final authorization: agent-verified under the user's --automation instruction. Human approval remains false. Subjective audio listening was unavailable; objective alignment, ASR, decoding, loudness and mix-comparison checks do not certify pronunciation, prosody or subjective balance.
- Preview released after export verification: PID 28552, port 3002; managed stop succeeded, status not-running, direct port query found no listener. No retention hold remains.
- Next action: none within the requested endpoint. Preserve this production and its selected topic on any continuation.
'''
episode.write_text(text,encoding='utf-8')
tracker=R/'TRACKER.json';data=json.loads(tracker.read_text(encoding='utf-8-sig'));entry=next(x for x in data['productions'] if x['slug']==P.name);entry['stage']='export';entry['status']='complete';tracker.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert json.loads(tracker.read_text())['productions'][-1]['path']==f'productions/{P.name}'
assert (R/entry['path']).is_dir()
print(json.dumps({'stage':entry['stage'],'status':entry['status'],'duration':report['duration'],'sha256':report['sha256'],'preview':'stopped and port released'}))
