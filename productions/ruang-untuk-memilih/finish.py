"""Close the verified queue endpoint, preserving receipts and other productions."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
P=Path(__file__).resolve().parent;V=P/'video';R=P.parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
export=read(V/'verification/export.json');receipt=read(P/'PUBLISHING.json');post=receipt['posts'][0];asset=receipt['assets'][0];remote=read(V/'verification/trypost-media.json')
assert post['status']=='scheduled' and post['content_matches_payload']
assert post['trypost_post_id']=='01a17f39-79b9-7397-979a-19d6e45130a6'
assert datetime.fromisoformat(post['scheduled_at']).replace(tzinfo=timezone.utc)>datetime.now(timezone.utc)
assert post['scheduled_at']=='2026-10-30 07:00:00' and post['published_at'] is None
assert asset['status']=='verified' and remote['status']=='passed' and remote['matches_local_export']
assert remote['sha256']==export['sha256']==hashlib.sha256((P/export['file']).read_bytes()).hexdigest()
assert read(V/'verification/preview-cleanup.json')['recorded_process_still_owns_port'] is False
copy=read(P/'delivery-copy.json');assert copy['caption']==post['payload']['content']
payload_hash=hashlib.sha256(json.dumps(post['payload'],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest();assert payload_hash==post['payload_sha256']
assert post['observed_media'][0]['size']==export['bytes']
post.update(schedule_timezone='Asia/Jakarta',scheduled_at_utc='2026-10-30T07:00:00Z',scheduled_at_local='2026-10-30T14:00:00+07:00',public_served_media_verification='video/verification/trypost-media.json')
asset['verification']='HTTP201 local upload; exact attached media ID, original filename, bytes and duration; public served HTTP200 full bytes and SHA-256 match the verified export.'
(P/'PUBLISHING.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
note='''
## Final outcome - queue complete

The requested automated pipeline is complete through actual scheduling, with no human approval claimed. V1 is 90.033333s, 1080x1920, 30fps, H.264/AAC, 2701 frames. All 182 spoken words have burned captions and an SRT. Complete storyboard precedes synthesis/animation; final technical, independent visual and encoded cut-frame reviews pass. Fifteen encoded acoustic boundaries and six waveform cue matches pass. Audio was measured, not perceptually heard.

Trypost Local, Admin's Workspace, Instagram @eliansatya: post 01a17f39-79b9-7397-979a-19d6e45130a6, observed scheduled. Actual next configured queue slot: **2026-10-30 14:00 WIB**, returned 2026-10-30 07:00:00 UTC. Exact caption, account, content type and attached media readback match. Public served HTTP200 copy is 4,106,102 bytes with SHA-256 d0a65ee4ee6036bc89658c52f6e8cc71c527f6b001123607e45c6f0967557bfa, identical to the local export. published_at remains null; scheduling does not claim live publication. No future monitoring requested.

[MP4](exports/ruang-untuk-memilih-v1.mp4), [SRT](exports/ruang-untuk-memilih.srt), [content package](CONTENT_PACKAGE.md), [delivery receipt](PUBLISHING.json), [decoded proof](exports/export-proof.png), [storyboard HTML](video/boards/storyboard.html) and [PNG](video/boards/storyboard.png).

Pipeline-owned preview PID21516/port3002 was stopped after verified export; status and TCP ownership confirm cleanup before packaging/upload. No unrelated server stopped. The HyperFrames desktop app remains an optional editing surface: https://hyperframes.dev/studio/download?os=windows . Anonymous successful-render feedback was sent as required by the project-local HyperFrames skill; no production text or asset was submitted.

Repository handoff: only this production and its tracker row enter the requested local commit. Existing ignore rules retain generated audio/video binaries and final proofs locally. No pipeline work remains.
'''
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(note)
with (P/'CONTENT_PACKAGE.md').open('a',encoding='utf-8') as f:f.write('\n## Actual queue result\n\nTrypost post 01a17f39-79b9-7397-979a-19d6e45130a6: scheduled for 2026-10-30 14:00 Asia/Jakarta (07:00 UTC). Exact copy/media verified; public served bytes match the export SHA-256. [Receipt](PUBLISHING.json). This establishes scheduling; published_at is null.\n')
(P/'VERIFICATION.md').write_text('''# Verification evidence

V1 agent-verified under --automation. No human approval or perceptual listening claimed.

- Research/script: SOURCES.md and SCRIPT.md; original source body and institutional definition; fictional illustration identified.
- Static storyboard: video/boards/verification.json, complete HTML/PNG, sixteen styled stills before synthesis/animation.
- Audio provenance: video/audio_request.json, audio_meta.json, .media/audio/voice request fingerprint and native alignment.
- Timing: video/timing.json, audio_boundaries.json; unaltered native speed and measured quiet placement.
- Technical: video/verification/hyperframes-check.json; zero errors, warnings assessed in video/REVIEW.md.
- Visual: four motion sheets, review-manifest.json, independent-review.md, exact-seams.json; eighteen forward/reverse seeks and full preview playback.
- Export: video/verification/export.json; full decode, 90.033333s/2701 frames, H.264/AAC 1080x1920/30fps, -13.56 LUFS/-1.28 dBTP.
- Encoded pixels: exports/export-proof.png, video/verification/encoded-cuts.png/json; exact suspect cuts and adjacent frames clean.
- Encoded sound: video/verification/sound-design-export-v2.json and audio-boundaries-export-v2.json; six cues/fifteen seams pass.
- Preview lifecycle: video/verification/preview-owner.json and preview-cleanup.json; only owned PID released, no listener remains.
- Delivery: PUBLISHING.json and video/verification/trypost-media.json; scheduled state, exact UTF-8 caption/account/media and public full-byte SHA-256 match.

The immutable export SHA-256 is d0a65ee4ee6036bc89658c52f6e8cc71c527f6b001123607e45c6f0967557bfa. Queue endpoint complete at 2026-10-30 14:00 WIB; no live publication or future monitoring claimed.
''',encoding='utf-8')
tracker=R/'TRACKER.json';d=read(tracker);next(x for x in d['productions'] if x['slug']==P.name).update(stage='publishing',status='complete');tracker.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all((R/x['path']).is_dir() for x in d['boards']+d['productions'])
# Confirm local delivery links after every requested artifact exists.
for name in ('CONTENT_PACKAGE.md','EPISODE.md'):
    for target in re.findall(r'\]\(([^)]+)\)',(P/name).read_text(encoding='utf-8')):
        if '://' not in target:assert (P/target.split('#')[0]).exists(),target
print(json.dumps(dict(stage='publishing',status='complete',post_id=post['trypost_post_id'],scheduled_at_local=post['scheduled_at_local'],sha256=export['sha256'])))
