"""Package a verified export; persist posting intent before any external write."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rep=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));video=P/rep['local_file']
assert rep['status']=='passed' and hashlib.sha256(video.read_bytes()).hexdigest()==rep['sha256']
copy='''Sayapnya turun, gabusnya naik. Di pembuka gabus bersayap, sektor gigi pada kedua lengan berkaitan dengan alur melingkar pada batang tengah. Saat lengan ditekan, batang naik dan spiral yang tertanam membawa gabus keluar.

Video ini menjelaskan contoh mekanisme dengan poros tetap dan badan yang bertumpu pada bibir botol, seperti konstruksi pada Gambar 1 US4063473A. Bentuk produk lain dapat berbeda.

Ilustrasi penampang disederhanakan, bukan skala; gerak diperlambat.
Rujukan: US4063473A dan EP3130558A1 (Google Patents).

#DiBalikBenda #CaraKerja #Mekanisme #PembukaGabus'''
assert len(copy)<=2200 and copy.count('#')<=5
(V/'post-caption.txt').write_text(copy+'\n',encoding='utf-8')
timing=json.loads((V/'timing.json').read_text(encoding='utf-8'))
package=f'''# Content package — v1

## Recommended title
Sayap turun, kenapa gabus naik?

Alternatives:
- Gigi tersembunyi di pembuka gabus bersayap
- Diputar dulu, ditekan kemudian: perjalanan satu gabus

## Instagram caption
{copy}

## Hashtags
#DiBalikBenda #CaraKerja #Mekanisme #PembukaGabus

## Editorial search keywords
pembuka gabus, pembuka botol bersayap, corkscrew, winged corkscrew, sektor gigi, alur melingkar, tuas, cara kerja pembuka gabus

## Cover
Implemented opening frame: “Turun, kok naik?” [Cover](exports/{P.name}-v1-cover.png), provider offset0ms. No independent artwork promised.

## Verified delivery metadata
- Production: {P.name}; Di Balik Benda approved v6.
- Destination: Instagram Reel @dibalikbenda.id, Admin's Workspace.
- Language: Indonesian.
- [MP4]({rep['local_file']}): {rep['duration_s']}s,1080x1920,9:16,30fps,2700frames,H.264/AAC.
- File: {rep['bytes']}bytes; SHA256 `{rep['sha256']}`.
- Captions: burned in plus [SRT](exports/{P.name}-v1.srt) / [VTT](exports/{P.name}-v1.vtt).69 groups at46px. Word times remain estimates reanchored to acoustic scene boundaries.
- Narration: ElevenLabs eleven_v4, preserved95.44s original; pitch-preserving derived tempo{timing['tempo']:.9f}; original source retained, no resynthesis.
- Sound:16 existing material/editorial cues; no BGM to leave small interactions clear. [Credits](video/assets/audio/sfx/CREDITS.md).
- Verification: full HyperFrames checks, frame-state/seam proof,15 acoustic boundaries, caption fit, full-file decode, encoded cue matching and loudness analysis. Listening and phone-speaker audition unavailable; no perceptual approval claimed.
- Queue: next configured slot in Asia/Jakarta; actual schedule in [receipt](PUBLISHING.json). No monitoring beyond scheduling requested.
- Optional sponsorship, mentions and account settings unset. No invented declarations.

[Technical evidence](SOURCES.md) bounds the mechanism to a documented construction, not all marketed products. [Review](video/REVIEW.md) records limitations.
'''
for f in [video,P/f'exports/{P.name}-v1-cover.png',P/f'exports/{P.name}-v1.srt',P/f'exports/{P.name}-v1.vtt']:assert f.is_file()
(P/'CONTENT_PACKAGE.md').write_text(package,encoding='utf-8')
a=json.loads((R/'boards/di-balik-benda/ACCOUNTS.json').read_text())['accounts'][0];stamp=datetime.now(timezone.utc).isoformat()
intent=dict(provider='trypost',workspace_id=a['workspace_id'],workspace_name=a['workspace_name'],social_account_id=a['social_account_id'],service='instagram',handle=a['handle'],content_type='instagram_reel',content=copy,media_export_sha256=rep['sha256'],meta=dict(cover_offset_ms=0),status='scheduled',queue='next')
dump(V/'posting-intent.json',intent)
payload_hash=hashlib.sha256(json.dumps(intent,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
receipt=dict(schema_version=2,assets=[dict(provider='trypost',local_file=rep['local_file'],sha256=rep['sha256'],bytes=rep['bytes'],status='planned',attempt_started_at=stamp,workspace_id=a['workspace_id'],source='local_upload')],posts=[dict(provider='trypost',workspace_id=a['workspace_id'],workspace_name=a['workspace_name'],social_account_id=a['social_account_id'],service='instagram',handle=a['handle'],content_type='instagram_reel',export_sha256=rep['sha256'],payload_sha256=payload_hash,payload=intent,requested_delivery='queue',requested_due_at=None,attempt_started_at=stamp,status='planned')])
assert not (P/'PUBLISHING.json').exists(), 'Reconcile previous delivery first'
dump(P/'PUBLISHING.json',receipt)
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('\n## Verified export and package\nv1 MP4, cover and caption sidecars verified. Package matches SHA256 '+rep['sha256']+'. Queue endpoint, sole inherited Instagram account. Intent/fingerprint persisted before upload and creation.\n')
t=R/'TRACKER.json';d=json.loads(t.read_text(encoding='utf-8'));next(x for x in d['productions'] if x['slug']==P.name).update(stage='publishing',status='in_progress');dump(t,d)
print(json.dumps(dict(bytes=rep['bytes'],sha256=rep['sha256'],caption_chars=len(copy),targets=1,payload_sha256=payload_hash)))
