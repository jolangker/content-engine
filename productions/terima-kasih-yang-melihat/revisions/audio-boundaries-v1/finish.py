"""Reconcile the queue endpoint using actual provider evidence and fresh time."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[1];V=P/'video'
file=P/'PUBLISHING.json';d=json.loads(file.read_text(encoding='utf-8'));post=d['posts'][0];asset=d['assets'][0]
assert post['status']=='scheduled' and asset['status']=='verified'
due=datetime.strptime(post['scheduled_at'],'%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
assert due>datetime.now(timezone.utc)
local=due.astimezone(timezone(timedelta(hours=7)))
export=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));remote=json.loads((V/'verification/trypost-media.json').read_text(encoding='utf-8'))
assert remote['status']=='passed' and remote['matches_local_export'];assert remote['sha256']==export['sha256']==post['export_sha256']==asset['sha256']
assert hashlib.sha256((P/asset['local_file']).read_bytes()).hexdigest()==export['sha256']
assert len(post['observed_media'])==1
media=post['observed_media'][0];assert media['original_filename']=='terima-kasih-yang-melihat-v1.mp4';assert media['size']==export['bytes'];assert media['meta']['duration']==export['duration_s']
assert json.loads((V/'verification/preview-cleanup.json').read_text(encoding='utf-8'))['status']=='passed'
assert not any(k in json.dumps(d) for k in ('upload_token','upload_url','signature='))
post.update(scheduled_at_utc=due.isoformat(),scheduled_at_local=local.isoformat(),timezone='Asia/Jakarta')
post['verification'].update(schedule='future service-selected queue slot verified against fresh UTC time',media_bytes=media['size'],media_duration_s=media['meta']['duration'],media_filename=media['original_filename'],public_served_media='HTTP200 without credentials; full bytes and SHA-256 match local export')
asset.update(verification='Direct HTTP201 upload, exact attached identity and metadata readback, public HTTP200 full-file SHA-256 matches verified local export.',public_sha256=remote['sha256'])
file.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
end=f'''
## Final outcome — queue endpoint complete

Agent-verified v1 with arrival correction completed all dependencies through queue delivery. Direct local upload returned HTTP201. Trypost post `{post['trypost_post_id']}` was created exactly once after a zero-match account/content duplicate check. Attached media `{asset['media_id']}` matched filename, {export['bytes']} bytes and server-measured {export['duration_s']}s. Readback confirmed exact caption, instagram_reel, connected @eliansatya, schedule_mode=queue and status=scheduled. Public served file returned HTTP200 without credentials and its complete SHA-256 matched the local export. An initial Python-default user-agent request was refused with HTTP403; the ordinary browser user-agent request succeeded, without any deployment or authentication change.

Actual schedule: **{local:%d %B %Y}, {local:%H:%M} WIB**, returned {post['scheduled_at']} UTC; verified future against the current clock. This is the service-selected next configured queue slot, not an invented custom time. published_at remains null; no live post is claimed. See [PUBLISHING.json](PUBLISHING.json).

Deliverables: [MP4](exports/terima-kasih-yang-melihat-v1.mp4), [SRT](exports/terima-kasih-yang-melihat.srt), [package](CONTENT_PACKAGE.md), [export proof](exports/export-proof.png), [storyboard HTML](video/boards/storyboard.html) and [PNG](video/boards/storyboard.png). Export full decode and all six cue checks passed. Listening limits are documented in VERIFICATION.md; no human approval fabricated. The delivery render completed; a wrapper print-encoding error was repaired without rerendering valid output.

Preview PID24372/port3002 released and port ownership verified before packaging/upload. No remaining production dependency or review. Future publication monitoring is outside this completed queue request. HyperFrames desktop app remains an editing option: https://hyperframes.dev/studio/download?os=windows .

Next: create the explicitly requested local Git commit for this episode and its narrow tracker addition. Preserve the unrelated pre-existing jangan-sahut board files/registry change. Existing ignore rules keep video/audio binaries and generated proof images local; source, stills, captions, receipts and written verification remain eligible for Git.
'''
p=P/'EPISODE.md';text=p.read_text(encoding='utf-8').replace('## Current state\n','## Initial state (historical)\n');p.write_text(text+end,encoding='utf-8')
with (P/'CONTENT_PACKAGE.md').open('a',encoding='utf-8') as f:f.write(f"\n## Queue receipt\n\nScheduled for **{local:%d %B %Y}, {local:%H:%M} WIB** in Trypost, Instagram @eliansatya. Post ID `{post['trypost_post_id']}`. Status scheduled, published_at null. Exact account/caption/media/schedule readback and public served file hash passed. See PUBLISHING.json.\n")
with (V/'BRIEF.md').open('a',encoding='utf-8') as f:f.write(f"\n## Completed handoff\n\nV1 with arrival correction exported and queued: {local.isoformat()}. Receipt ../PUBLISHING.json. Pipeline-owned preview stopped and port ownership verified. Human approval and live publication are not claimed.\n")
with (V/'REVIEW.md').open('a',encoding='utf-8') as f:f.write('\n## Export confirmation\n\nDelivery export verified: 90s, 1080x1920, 2700 frames, full decode clear, all six waveform cue matches passed; -13.60 LUFS / -1.66 dBTP. Decoded proof inspected across every scene. Preview released. Exact file publicly served by Trypost with matching SHA-256 and queued; receipt in ../PUBLISHING.json.\n')
with (P/'VERIFICATION.md').open('a',encoding='utf-8') as f:f.write(f"\nQueue endpoint verified: Trypost `{post['trypost_post_id']}`, {local.isoformat()}, status scheduled. Exact caption/account/media readback, public full-file SHA-256 and future schedule checks passed. Preview cleanup passed; no live publication claimed.\n")
tracker_path=ROOT/'TRACKER.json';tracker=json.loads(tracker_path.read_text(encoding='utf-8'));next(x for x in tracker['productions'] if x['slug']==P.name).update(stage='publishing',status='complete');tracker_path.write_text(json.dumps(tracker,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all((ROOT/x['path']).is_dir() for x in tracker['boards']+tracker['productions'])
print(json.dumps(dict(status='complete',post_id=post['trypost_post_id'],scheduled_at_local=local.isoformat())))
