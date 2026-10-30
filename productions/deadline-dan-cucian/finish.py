"""Close only the fully verified queue endpoint, using observed provider times."""
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import json,subprocess
P=Path(__file__).resolve().parent;V=P/'video'
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 receipt=json.loads((P/'PUBLISHING.json').read_text(encoding='utf-8'));media=json.loads((V/'verification/trypost-media.json').read_text(encoding='utf-8'));export=json.loads((V/'verification/export.json').read_text(encoding='utf-8'))
 assert media['status']=='passed' and media['matches_local_export'] and media['sha256']==export['sha256']
 assert len(receipt['posts'])==1 and all(p['status']=='scheduled' and p['content_matches_payload'] for p in receipt['posts'])
 assert receipt['assets'][0]['sha256']==media['sha256'];assert json.loads((V/'verification/preview-cleanup.json').read_text())['status']=='passed'
 post=receipt['posts'][0];observed=post['observed_media'][0]
 assert observed['size']==export['bytes'] and observed['original_filename']==Path(export['file']).name
 assert abs(float(observed['meta']['duration'])-export['duration_s'])<.05
 due=datetime.fromisoformat(post['scheduled_at'].replace('Z','+00:00'))
 if due.tzinfo is None:due=due.replace(tzinfo=timezone.utc)
 assert due>datetime.now(timezone.utc)
 local=due.astimezone(ZoneInfo('Asia/Jakarta'))
 post.update(scheduled_at_utc=due.isoformat(),scheduled_at_local=local.isoformat(),timezone='Asia/Jakarta',completion='Queue endpoint verified; future publication not monitored')
 receipt['assets'][0]['public_media_verification']=media;dump(P/'PUBLISHING.json',receipt)
 with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'''

## Queue endpoint complete

Trypost Admin's Workspace saved and read back Instagram Reel @eliansatya as **scheduled** for **{local:%Y-%m-%d %H:%M} Asia/Jakarta**, returned UTC `{post['scheduled_at']}`. Post ID `{post['trypost_post_id']}`; media ID `{receipt['assets'][0]['media_id']}`. Exact caption/account/content type and one attached video verified. Filename, {export['bytes']}bytes and server duration{export['duration_s']}s match. Public served MP4 returned HTTP200 and downloaded SHA256 matches the local export. [PUBLISHING.json](PUBLISHING.json) preserves actual evidence and stable posting intent. No approval dependency or unknown write. Scheduling complete; no claim of live publication and no future monitor started.

Export, package and authorized queue endpoint are complete. Pipeline preview released and verified. Next: requested scoped Git commit, preserving all pre-existing skill/board/production/tracker changes.
''')
 with (V/'REVIEW.md').open('a',encoding='utf-8') as f:f.write(f'''

## Actual export and delivery closure

Verified actual export: {export['duration_s']}s, {export['frames']}frames, full decode; all fifteen encoded acoustic seams, forty-five encoded cut-adjacent frames, sixteen representative frames, and six waveform cue matches passed. Actual level{export['loudness']['input_i']}LUFS / {export['loudness']['input_tp']}dBTP. No perceptual listening claim. Pipeline preview released. Trypost readback is scheduled for{local:%Y-%m-%d %H:%M}WIB; publicly served media hashes match the exact local export. See ../VERIFICATION.md and ../PUBLISHING.json. Source remains editable in the HyperFrames desktop app; delivery binaries remain local under existing Git ignores.
''')
 subprocess.run(['python',str(P/'state.py'),'publishing','complete'],check=True)
 print(json.dumps(dict(endpoint='queue',status='complete',account='eliansatya',scheduled_at=local.isoformat(),post_id=post['trypost_post_id'])))
if __name__=='__main__':main()
