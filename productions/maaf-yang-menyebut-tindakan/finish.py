"""Reconcile verified scheduling and close the authorized pipeline."""
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[1];V=P/'video';Q=V/'verification'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    r=read(Q/'export.json');d=read(P/'PUBLISHING.json');media=read(Q/'trypost-media.json');post=d['posts'][0]
    assert r['sha256']==hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==media['sha256']
    assert media['status']=='passed' and media['matches_local_export']
    assert post['status']=='scheduled' and post['content_matches_payload']
    assert read(Q/'encoded-cuts.json')['visual_inspection']=='passed'
    assert read(Q/'sound-design-export-v2.json')['status']=='passed'
    assert read(Q/'preview-cleanup.json')['recorded_process_still_owns_port'] is False
    due=datetime.fromisoformat(post['scheduled_at']).replace(tzinfo=timezone.utc);assert due>datetime.now(timezone.utc)
    local=due.astimezone(ZoneInfo('Asia/Jakarta'))
    post.update(scheduled_at_utc=due.isoformat().replace('+00:00','Z'),scheduled_at_local=local.isoformat(),timezone='Asia/Jakarta')
    d['assets'][0]['public_served_verification']=media;dump(P/'PUBLISHING.json',d)
    final=f'''\n## Final outcome — queue complete

The automated pipeline is complete through actual scheduling. Title: **Maaf yang menyebut tindakan**. V1 MP4: {r['duration_s']:.0f}s,1080x1920,30fps,H.264/AAC,{r['frames']} frames,{r['bytes']:,} bytes. All183 spoken words have burned captions and an SRT. The complete storyboard preceded synthesis; later04 role and12/13 clock corrections were reflected in its poses and combined PNG. Full HyperFrames check, complete visual review, independent repair review, forward/reverse seeks,45 actual encoded cut samples, full-file decode,15 encoded acoustic seams and six cue waveform matches pass. Sound was measured, not perceptually heard. Export levels {r['loudness']['input_i']}LUFS/{r['loudness']['input_tp']}dBTP. No human approval claimed; --automation supplied delegated review/render authorization.

Trypost Local, Admin's Workspace, Instagram @eliansatya: post **{post['trypost_post_id']}**, observed **scheduled**, actual configured queue slot **{local.strftime('%Y-%m-%d %H:%M')} WIB** (returned {post['scheduled_at']} UTC). Exact caption/account/content type/media attachment readback passed. Public HTTP200 served copy has{media['bytes']:,} bytes and SHA-256 `{r['sha256']}`, identical to local export. published_at is null; this is scheduling, not a claim of live publication. No future monitoring was requested. Receipt: [PUBLISHING.json](PUBLISHING.json).

[MP4]({r['file']}), [SRT](exports/{P.name}.srt), [content package](CONTENT_PACKAGE.md), [decoded proof](exports/export-proof.png), [storyboard HTML](video/boards/storyboard.html), [PNG](video/boards/storyboard.png).

Pipeline-owned preview PID38080/port3002 was stopped after export verification; status returned not-running and no listener remains. No unrelated server was stopped. Optional continued editing: HyperFrames desktop app, https://hyperframes.dev/studio/download?os=windows . One anonymous successful-render feedback report was sent under the project HyperFrames skill; no script, assets, account identity or production paths were submitted.

Repository handoff: commit only this production and its tracker entry. Concurrent fan-production and preexisting creative-direction-skill work remain outside scope. Existing ignores keep generated audio/video and verification images local; source, metadata, receipts, stills and licenses are tracked. No pipeline work remains.
'''
    with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(final)
    verification=f'''# Verification — v1

- Complete static storyboard before synthesis:16 ordered1080x1920 stills, HTML and1440x3183 PNG; refreshed04/12/13 details inspected.
- Narration: one ElevenLabs eleven_v4 call, root project voice,76.08s native,183 aligned words; preserved native samples, pause insertion and final normalization,90s composition; individual word times remain estimates.
- Board:16 scenes,14 cream/two charcoal09/14; approved chrome/fonts preserved; full caption coverage48 groups.
- Full HyperFrames check passes all error gates; eleven group-loop static-linter warnings and sixteen26px chrome craft warnings are explained in video/REVIEW.md.
- Complete beat/phone/seam review,64 phase samples, independent reviewer and corrected exact-boundary follow-up;18 forward/reverse seeks match.17-significant-digit timing closes sub-frame gaps.45 actual encoded adjacent/cut frames pass visual inspection.
- Full MP4 decode passed;2700 frames,1080x1920,30fps,H.264/yuv420p,AAC stereo,90s,{r['bytes']:,} bytes. SHA-256 `{r['sha256']}`.
- All15 actual encoded narration boundaries and all six cue waveform matches pass. Levels {r['loudness']['input_i']}LUFS/{r['loudness']['input_tp']}dBTP. Perceptual listening unavailable; no human approval is claimed.
- Caption package1022 characters/three hashtags; source credits and workplace-scenario limits included.
- Scheduling readback: {post['trypost_post_id']},scheduled,{local.isoformat()}; exact copy/account/content type/attached media. Public served bytes/hash match local export; no future-monitoring claim.
- Preview38080/3002 cleanup verified; no unrelated process terminated.
'''
    (P/'VERIFICATION.md').write_text(verification,encoding='utf-8')
    with (V/'REVIEW.md').open('a',encoding='utf-8') as f:f.write('\n## Export verification completed\n\nActual v1 MP4 passed full decode, all45 adjacent/boundary visual samples,15 acoustic seams and six cue matches. Independent repair review closed all earlier P1s. See ../VERIFICATION.md and verification/export.json. Sound measured, not heard. Preview was released before packaging/upload; next queue slot was verified through Trypost readback and public served SHA-256 matching.\n')
    t=read(ROOT/'TRACKER.json');row=next(x for x in t['productions'] if x['slug']==P.name);row.update(stage='publishing',status='complete');dump(ROOT/'TRACKER.json',t)
    assert all((ROOT/x['path']).is_dir() for x in t['boards']+t['productions'])
    print(json.dumps(dict(status='complete',post=post['trypost_post_id'],scheduled=local.isoformat(),sha256=r['sha256'])))
if __name__=='__main__':main()
