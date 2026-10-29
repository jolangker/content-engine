"""Close the verified queue endpoint, preserving exact remote receipts."""
from pathlib import Path
import hashlib,json,subprocess
P=Path(__file__).resolve().parent;V=P/'video'
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
receipt=json.loads((P/'PUBLISHING.json').read_text(encoding='utf-8'));media=json.loads((V/'verification/trypost-media.json').read_text(encoding='utf-8'))
assert media['status']=='passed' and media['matches_local_export']
assert len(receipt['posts'])==1 and all(x['status']=='scheduled' and x['content_matches_payload'] for x in receipt['posts'])
assert receipt['assets'][0]['sha256']==media['sha256']
assert json.loads((V/'verification/preview-cleanup.json').read_text())['status']=='passed'
receipt['assets'][0]['public_media_verification']=media
receipt['posts'][0].update(scheduled_at_utc='2026-11-01T07:00:00Z',scheduled_at_local='2026-11-01T14:00:00+07:00',timezone='Asia/Jakarta',completion='Queue endpoint verified; future publication not monitored')
dump(P/'PUBLISHING.json',receipt)
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('''
## Queue endpoint complete

Trypost Admin's Workspace saved and read back Instagram Reel @eliansatya as **scheduled** for **2026-11-01 14:00 Asia/Jakarta**, returned UTC `2026-11-01 07:00:00`. Post ID `01a18988-63b1-738e-8850-49a21a8a5af6`; media ID `01a18988-2248-7192-bba7-79bd7dc3ee75`. Caption is an exact payload match; connected account/content type, filename, 4278479 bytes and server duration90 seconds match. Public served media returned HTTP200 and its downloaded SHA256 equals the verified local export. Receipt: [PUBLISHING.json](PUBLISHING.json). No pending approval, duplicate post or unresolved write. This completes scheduling, not a claim that the post is live. No future monitor is started.

All authorized production dependencies through verified export, package and queue are complete. Preview has been released. Next: make the requested scoped Git commit; preserve pre-existing gali-jadi/tong-hujan working-tree changes.
''')
with (V/'REVIEW.md').open('a',encoding='utf-8') as f:f.write('''
## Actual export and delivery closure

The required export checks passed: full decode,2700frames/90.0s, fifteen encoded audio seams, forty-five visual seam frames, all sixteen representative frames and six waveform cue matches. Actual level -13.73LUFS/-1.59dBTP; no perceptual listening claim. Preview cleanup verified. Final board capture1440x3206 includes the corrected scene15. Trypost readback is scheduled for2026-11-01 14:00WIB; public served MP4 bytes/hash match the local export. See ../VERIFICATION.md and ../PUBLISHING.json. HyperFrames technical feedback submitted under its skill; editable source can be reopened in the HyperFrames desktop app (https://hyperframes.dev/studio/download?os=windows&src=cli).
''')
subprocess.run(['python',str(P/'state.py'),'publishing','complete'],check=True)
print(json.dumps(dict(endpoint='queue',status='complete',account='eliansatya',scheduled_at='2026-11-01T14:00:00+07:00',post_id=receipt['posts'][0]['trypost_post_id'])))
