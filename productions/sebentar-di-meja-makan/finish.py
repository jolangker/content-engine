"""Close only a verified export/package/queue endpoint, retaining actual receipts."""
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1];V=P/'video';Q=V/'verification'
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    export=json.loads((Q/'export.json').read_text(encoding='utf-8'));assert hashlib.sha256((P/export['file']).read_bytes()).hexdigest()==export['sha256']
    for f in ('hyperframes-check.json','sound-design-export-v2.json','preview-cleanup.json','trypost-media.json'):
        d=json.loads((Q/f).read_text(encoding='utf-8'));assert d.get('ok',d.get('status')=='passed'),f
    assert json.loads((Q/'encoded-cuts.json').read_text(encoding='utf-8'))['visual_inspection']=='passed'
    assert (P/'CONTENT_PACKAGE.md').exists()
    receipt=json.loads((P/'PUBLISHING.json').read_text(encoding='utf-8'));targets=json.loads((P/'target_snapshot.json').read_text(encoding='utf-8'))['accounts'];assert len(receipt['posts'])==len(targets)==1
    for post,target in zip(receipt['posts'],targets):
        assert post['social_account_id']==target['social_account_id'] and post['workspace_id']==target['workspace_id']
        assert post['status']=='scheduled' and post['content_matches_payload']
        assert post['export_sha256']==export['sha256'] and post['observed_schedule_mode']=='queue'
        utc=datetime.fromisoformat(post['scheduled_at'].replace('Z','+00:00'))
        if utc.tzinfo is None:utc=utc.replace(tzinfo=timezone.utc)
        assert utc>datetime.now(timezone.utc)
        local=utc.astimezone(ZoneInfo('Asia/Jakarta'));post.update(scheduled_at_utc=utc.isoformat(),scheduled_at_local=local.isoformat(),timezone='Asia/Jakarta',completion='Queue endpoint verified; future publication not monitored')
    asset=receipt['assets'][0];assert asset['status']=='verified' and asset['sha256']==export['sha256']
    asset['public_delivery_verification']='video/verification/trypost-media.json: HTTP 200 and downloaded SHA-256 matches local export'
    dump(P/'PUBLISHING.json',receipt)
    post=receipt['posts'][0];local=datetime.fromisoformat(post['scheduled_at_local'])
    with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'''\n## Export, package and queue endpoint complete

Verified v1 export: {export['duration_s']:.6f}s, 1080x1920, 30fps, {export['frames']} frames, H.264/AAC, {export['bytes']} bytes, SHA-256 `{export['sha256']}`. Full decode passed. All fifteen actual encoded acoustic seams, forty-five encoded visual cut frames and six SFX waveform matches passed. Loudness {export['loudness']['input_i']} LUFS / {export['loudness']['input_tp']} dBTP; sound measured, not perceptually heard. Complete package and sidecar SRT exist. Pipeline-owned preview stopped and listener cleanup verified.

Trypost Admin's Workspace saved and read back Instagram Reel @eliansatya as **scheduled** for **{local.strftime('%Y-%m-%d %H:%M')} Asia/Jakarta**; returned UTC `{post['scheduled_at']}`. Post ID `{post['trypost_post_id']}`, media ID `{asset['media_id']}`. Exact account, caption, content type, one video attachment, original filename, bytes and server duration verified. Public served media returned HTTP 200; downloaded SHA-256 equals the local export. Stable intent, fingerprint, upload/attachment results and actual schedule retained in [PUBLISHING.json](PUBLISHING.json). Scheduling complete; no claim of live publication and no future monitor started.

All requested pipeline stages are complete under delegated automation. Human approval remains false. Commit the production sources, alignment, provenance and receipts plus only this tracker insertion. Generated media remain local under existing ignores. Preserve unrelated working changes.
''')
    d=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));next(x for x in d['productions'] if x['slug']==P.name).update(stage='publishing',status='complete');dump(R/'TRACKER.json',d)
    assert all((R/x['path']).is_dir() for x in d['boards']+d['productions'])
    print(json.dumps(dict(stage='publishing',status='complete',post_id=post['trypost_post_id'],scheduled_at_local=post['scheduled_at_local'],export_sha256=export['sha256'])))
if __name__=='__main__':main()
