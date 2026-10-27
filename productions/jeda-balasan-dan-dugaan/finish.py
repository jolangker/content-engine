"""Reconcile the actual queue endpoint, final files and preview cleanup."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[1];V=P/'video'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
file=P/'PUBLISHING.json';d=read(file);post=d['posts'][0];asset=d['assets'][0];export=read(V/'verification/export.json');remote=read(V/'verification/trypost-media.json')
assert post['status']=='scheduled' and asset['status']=='verified'
due=datetime.strptime(post['scheduled_at'],'%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc);assert due>datetime.now(timezone.utc)
local=due.astimezone(timezone(timedelta(hours=7)))
assert remote['status']=='passed' and remote['matches_local_export']
assert remote['sha256']==export['sha256']==post['export_sha256']==asset['sha256']
assert hashlib.sha256((P/asset['local_file']).read_bytes()).hexdigest()==export['sha256']
assert len(post['observed_media'])==1
media=post['observed_media'][0];assert media['original_filename']==f'{P.name}-v1.mp4';assert media['size']==export['bytes'];assert abs(media['meta']['duration']-export['duration_s'])<.05
assert read(V/'verification/preview-cleanup.json')['status']=='passed'
assert not any(k in json.dumps(d) for k in ('upload_token','upload_url','signature='))
post.update(scheduled_at_utc=due.isoformat(),scheduled_at_local=local.isoformat(),timezone='Asia/Jakarta')
post['verification'].update(schedule='future service-selected next configured queue slot verified against fresh UTC',media_bytes=media['size'],media_duration_s=media['meta']['duration'],media_filename=media['original_filename'],public_served_media='HTTP200 without credentials; full bytes and SHA-256 match local export')
asset.update(verification='Direct HTTP201 local upload; attached identity and server metadata readback; public full-file HTTP200 and SHA-256 match.',public_sha256=remote['sha256'])
file.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
end=f'''
## Final outcome — queue endpoint complete

V1 completed all dependencies through the requested queue endpoint. Verified MP4: 90s, 1080x1920, 30fps, 2700 frames, H.264/AAC. All 182 spoken words captioned; full decode, fifteen encoded acoustic seams and six cue waveform matches pass. Loudness {export['loudness']['input_i']} LUFS / {export['loudness']['input_tp']} dBTP. Measured sound, not perceptually heard; no human approval claimed.

Direct local upload and exact media readback verified. Trypost `{post['trypost_post_id']}`, Instagram @eliansatya, Admin's Workspace, status **scheduled**. Actual next configured queue slot: **{local:%Y-%m-%d %H:%M} WIB**, returned {post['scheduled_at']} UTC. Exact caption/account/content type/media match; public served file's full bytes and SHA-256 match the export. published_at remains null. This completes scheduling and does not claim live publication. No future monitoring requested.

[MP4](exports/{P.name}-v1.mp4), [SRT](exports/{P.name}.srt), [content package](CONTENT_PACKAGE.md), [queue receipt](PUBLISHING.json), [decoded proof](exports/export-proof.png), [storyboard](video/boards/storyboard.png).

Pipeline-owned preview PID20344/port3002 released after export verification; status and TCP ownership confirmed cleanup before packaging/upload. Sources, editable composition, audio provenance, alignment and receipts retained. Existing ignore rules keep generated video/audio binaries and proof sheets local. HyperFrames desktop app is available for continued editing: https://hyperframes.dev/studio/download?os=windows .

Next and final repository step: create the explicitly requested local commit for this production and its narrow tracker addition.
'''
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(end)
with (P/'CONTENT_PACKAGE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Queue receipt\n\nScheduled **{local:%Y-%m-%d %H:%M} WIB**, Instagram @eliansatya, Trypost `{post["trypost_post_id"]}`. Exact caption/media/account readback and public SHA-256 passed. Live publication not claimed. See PUBLISHING.json.\n')
with (V/'BRIEF.md').open('a',encoding='utf-8') as f:f.write(f'\n## Completed handoff\n\nAgent-verified v1 exported and queued for {local.isoformat()}. Receipt ../PUBLISHING.json. Owned preview released. No human approval or live publication claimed.\n')
with (V/'REVIEW.md').open('a',encoding='utf-8') as f:f.write('\n## Export confirmation\n\nActual delivery MP4 inspected across all 16 decoded scene samples; 90s, 2700 frames. Full decode, six SFX waveform matches, fifteen acoustic seam checks passed. Preview released. Exact file served publicly by Trypost and queued, as recorded in ../PUBLISHING.json.\n')
(P/'VERIFICATION.md').write_text(f'''# Final verification — Jeda balasan dan dugaan v1

Agent-verified under the user's immediate automation. No human approval claimed.

- Research: read original source body, narrowed to construct/measurement distinctions, explicit fictional application and limits in SOURCES.md.
- Static storyboard: sixteen real styled poses and full 1440x3229 PNG checked before audio/animation; HTML and PNG retained.
- Narration: one ElevenLabs eleven_v4 call, root voice, native 78.48s/182 words. Source samples preserved before measured quiet splices and final normalization; root 90s. Individual word timestamps remain estimates.
- Technical checks: HyperFrames 0.8.209 passes runtime/layout/contrast/motion/audio with no errors. Approved 26px chrome warnings retained. Scoped SVG-selector lint warnings verified by identical active-scene states after eighteen forward/reverse seeks.
- Creative checks: 64 phase samples, beat/phone sheets and all fifteen seam sheets; independent reviewer found no P0/P1. Two dark frames 08/14, fixed chrome and caption clearance verified. Frame 07 relies most on narration for its abstract distinction.
- Preview: HTTP200, full 90s playback, no page errors; narration media ready. Owned PID20344/3002 stopped and port ownership verified before external delivery.
- Export: H.264/AAC, 1080x1920, 30fps, 2700 frames, full decode passed. Actual decoded frame from each scene inspected. {export['bytes']} bytes, SHA-256 {export['sha256']}.
- Audio export: fifteen acoustic cuts and all six cue waveform matches pass; {export['loudness']['input_i']} LUFS / {export['loudness']['input_tp']} dBTP. Perceptual listening unavailable; objective presence/level measurements do not establish a listener's experience.
- Delivery: direct local HTTP201 upload, exact caption/account/media readback, public served HTTP200 full-file SHA-256 match. Status scheduled for {local.isoformat()}, post {post['trypost_post_id']}. Published status is not claimed.

Evidence: video/verification/*.json, video/REVIEW.md, PUBLISHING.json and CONTENT_PACKAGE.md. No required stage remains unfinished; requested local commit follows pipeline completion.
''',encoding='utf-8')
t=ROOT/'TRACKER.json';tracker=read(t);next(x for x in tracker['productions'] if x['slug']==P.name).update(stage='publishing',status='complete');t.write_text(json.dumps(tracker,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');assert all((ROOT/x['path']).is_dir() for x in tracker['boards']+tracker['productions'])
print(json.dumps(dict(status='complete',post_id=post['trypost_post_id'],scheduled_at_local=local.isoformat())))
