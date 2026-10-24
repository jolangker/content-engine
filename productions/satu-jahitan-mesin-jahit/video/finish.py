from pathlib import Path
import json,re,hashlib
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
e=json.loads((V/'verification/export.json').read_text(encoding='utf-8'))
assert e['status']=='passed'
video=P/'exports/satu-jahitan-mesin-jahit.mp4'
assert hashlib.sha256(video.read_bytes()).hexdigest()==e['sha256']
cleanup=json.loads((V/'verification/preview-cleanup.json').read_text(encoding='utf-8'))
assert cleanup['status']=='verified_stopped' and cleanup['recorded_pid']==15340
assert (V/'boards/storyboard.png').exists() and len(list((V/'boards/stills').glob('frame-*.png')))==16
assert (P/'exports/satu-jahitan-mesin-jahit.srt').exists() and (P/'exports/proof-sheet.jpg').exists()
ep=P/'EPISODE.md';text=ep.read_text(encoding='utf-8')
text=text.replace('- topic: how a single-needle, two-thread lockstitch is formed; define the hook variant from technical evidence before locking the explanation','- topic: single-needle two-thread type-301 lockstitch, using JUKI\'s documented horizontal full-rotary-hook variant')
text=text.replace('- human_approved_hook: false','- human_approved_hook: true; the user replied "setuju" after hook 1 and its selected direction were presented on continuation')
text=text.replace('- workflow_initialization: deferred until the production needs a HyperFrames video project; video/ must be empty before init','- workflow_initialization: initialized once inside video/ with HyperFrames 0.8.188; the maintained consolidated HyperFrames explainer workflow replaces the retired faceless-explainer skill')
text=text.replace('- preview: no server started or inherited for this production','- preview: pipeline preview PID 15340 / port 3002 was opened for final look and render, then verified stopped after export')
text=re.sub(r'## Audio planning\n.*?(?=\n## Current state)', '## Audio planning\n\nCompleted with one ElevenLabs eleven_v4 request and the project-root .env voice. Original audio and alignment are preserved. See Audio v1 and video/audio_meta.json for pitch-preserving tempo processing and measured placement. Narration only is intentional; BGM and SFX decisions are recorded in video/sound_design.json.\n',text,flags=re.S)
text=re.sub(r'## Current state\n.*?(?=\n## Continuation)', '## Current state\n\n- current_stage: export\n- current_status: complete\n- requested_endpoint: export; preserved from the original request\n- next_action: none within the requested scope\n- completed: researched explanation, script, 16-shot verified static board, continuous narration, captions, animated composition, agent final-look verification and verified MP4\n- review_policy: immediate automation from the latest instruction; no human final-video approval claimed\n',text,flags=re.S)
text+=f'''\n## Verified delivery v1

- MP4: exports/satu-jahitan-mesin-jahit.mp4
- Captions: exports/satu-jahitan-mesin-jahit.srt
- Decoded export proof: exports/proof-sheet.jpg
- Static planning board: video/boards/storyboard.html and video/boards/storyboard.png
- Duration: {e['duration_s']} seconds; 1080 x 1920; 30 fps; {e['frames']} frames; H.264 video and AAC audio.
- Export SHA-256: {e['sha256']}
- Full decode: no errors. Audio: {e['integrated_lufs']} LUFS integrated; {e['true_peak_dbtp']} dBTP; sample peak below clipping.
- Technical final check: passed without errors or warnings. Diagnostic and exported proof frames inspected. Audio measurement does not establish perceptual listening; uninterrupted audiovisual watching was unavailable.
- Export authorization: delegated by latest --automation, after agent verification; human final approval false.
- Preview cleanup: managed stop, not-running status, and listener/process checks verified. PID 15340 no longer owns port 3002. No preview hold remains.
- Scope fulfilled: export only. No content-package or external delivery action was executed.

Detailed evidence: video/verification/export.json, video/verification/final-check.json, video/verification/preview-cleanup.json and video/REVIEW.md.
'''
ep.write_text(text,encoding='utf-8')
verification=f'''# Delivery verification — v1

The delivered MP4 is {e['duration_s']} seconds at 1080 x 1920, 30 fps, {e['frames']} frames. H.264/AAC. SHA-256: `{e['sha256']}`. Size: {e['bytes']} bytes.

The final HyperFrames check has no lint, runtime, layout, contrast or craft findings. Static storyboard verification covers 16 scenes and a full 1920 x 4268 board. Phone, beat, cut, targeted mechanical poses and decoded MP4 proof frames were visually inspected. These are bounded pose/continuity checks; they do not claim a numerical physics simulation or uninterrupted audiovisual viewing.

Full file decode returned no errors. Decoded sample peak: {e['sample_peak']:.6f}. Integrated loudness: {e['integrated_lufs']} LUFS. True peak: {e['true_peak_dbtp']} dBTP. All 211 words are included in 53 caption groups; tags are excluded. Caption and narration timings use the documented 1.05 pitch-preserving tempo transform. Native synthesis source, alignment, request fingerprint and hashes are preserved. BGM and SFX are intentionally absent, with no planned cues omitted. Perceptual listening was unavailable.

The final look was exposed in Studio before render under active immediate automation. The pipeline-owned preview was released and its stop verified after export; no review hold remains. The export-only endpoint is complete. See REVIEW.md for creative choices and the schematic rear-thread-view limitation.
'''
(V/'VERIFICATION.md').write_text(verification,encoding='utf-8')
tracker=R/'TRACKER.json';d=json.loads(tracker.read_text(encoding='utf-8-sig'));row=next(x for x in d['productions'] if x['slug']==P.name);row.update(stage='export',status='complete');tracker.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
verified=json.loads(tracker.read_text(encoding='utf-8'));assert (R/row['path']).is_dir()
print(json.dumps({'stage':'export','status':'complete','mp4':str(video),'duration_s':e['duration_s'],'sha256':e['sha256'],'preview_cleanup':cleanup['status']}))
