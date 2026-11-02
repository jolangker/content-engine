"""Package only a verified export and persist the exact external posting intent."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rep=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));video=P/rep['local_file']
assert rep['status']=='passed' and hashlib.sha256(video.read_bytes()).hexdigest()==rep['sha256']
copy='''Pita meteran bisa masuk sendiri karena pegas pengembali. Saat pengunci digeser, lidah lentur menjepit pita ke penopangnya. Pegas tetap menarik, tetapi gerak pitanya ditahan.

Di video ini kita membedah satu contoh pengunci geser dengan pin pemandu dan tonjolan penahan. Bentuk pengunci pada meteran lain dapat berbeda.

Ilustrasi mekanisme disederhanakan; gerak diperlambat dan lenturan diperbesar.
Rujukan: US5806202A, US5210956A, EP3318834B1 (Google Patents).

#DiBalikBenda #CaraKerja #Meteran #Mekanisme'''
assert len(copy)<=2200 and copy.count('#')<=5
(V/'post-caption.txt').write_text(copy+'\n',encoding='utf-8')
package=f'''# Content package — v1

## Recommended title
Meteran: siapa yang menarik, siapa yang menahan?

Alternatives:
- Kenapa pita meteran bisa kembali sendiri?
- Apa yang terjadi saat tombol meteran dikunci?

## Instagram caption
{copy}

## Editorial search keywords
meteran gulung, pegas pengembali, pengunci meteran, cara kerja meteran, pin pemandu, lidah lentur, spring return tape measure, sliding tape lock

## Cover
Implemented opening frame: “Ditarik, kok kembali?” See [cover](exports/{P.name}-v1-cover.png). Provider cover offset:0ms. No separate artwork promised.

## Delivery metadata
- Production: {P.name}; board di-balik-benda v6.
- Destination: Instagram Reel @dibalikbenda.id, Admin's Workspace.
- Language: Indonesian.
- Video: [MP4]({rep['local_file']}) — {rep['duration_s']}s,1080x1920,9:16,30fps,2700frames,H.264/AAC MP4.
- File bytes: {rep['bytes']}; SHA256: `{rep['sha256']}`.
- Captions: burned in, with [SRT](exports/{P.name}-v1.srt) and [VTT](exports/{P.name}-v1.vtt) sidecars. Provider word times are estimates anchored to measured quiet scene boundaries.
- Narration: ElevenLabs eleven_v4; preserved original, derived pitch-preserving tempo1.298313253 to fit the board's90s duration plus observation gaps. No resynthesis.
- Sound:18 synchronized existing material/editorial cues; no BGM by creative choice.
- Verification: full decode,2700frames, caption fit, full HyperFrames checks, mechanical state and seam checks, encoded boundary and cue-presence analysis. Listening unavailable; no perceptual or phone-speaker approval claimed.
- Queue: next configured slot, timezone Asia/Jakarta. Actual returned schedule recorded in [receipt](PUBLISHING.json).
- Optional sponsorship, mentions and account settings: unset; no invented declarations.

Evidence: [SOURCES.md](SOURCES.md). Licensed assets: [credits](video/assets/audio/sfx/CREDITS.md). No source-patent lock geometry is generalized to every meteran.
'''
for f in [video,P/f'exports/{P.name}-v1-cover.png',P/f'exports/{P.name}-v1.srt',P/f'exports/{P.name}-v1.vtt']:assert f.is_file()
(P/'CONTENT_PACKAGE.md').write_text(package,encoding='utf-8')
accounts=json.loads((R/'boards/di-balik-benda/ACCOUNTS.json').read_text())['accounts'];assert len(accounts)==1
a=accounts[0];stamp=datetime.now(timezone.utc).isoformat()
intent=dict(provider='trypost',workspace_id=a['workspace_id'],workspace_name=a['workspace_name'],social_account_id=a['social_account_id'],service='instagram',handle=a['handle'],content_type='instagram_reel',content=copy,media_export_sha256=rep['sha256'],meta=dict(cover_offset_ms=0),status='scheduled',queue='next')
dump(V/'posting-intent.json',intent)
payload_hash=hashlib.sha256(json.dumps(intent,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
receipt=dict(schema_version=2,assets=[dict(provider='trypost',local_file=rep['local_file'],sha256=rep['sha256'],bytes=rep['bytes'],status='planned',attempt_started_at=stamp,workspace_id=a['workspace_id'],source='local_upload')],posts=[dict(provider='trypost',workspace_id=a['workspace_id'],workspace_name=a['workspace_name'],social_account_id=a['social_account_id'],service='instagram',handle=a['handle'],content_type='instagram_reel',export_sha256=rep['sha256'],payload_sha256=payload_hash,requested_delivery='queue',requested_due_at=None,attempt_started_at=stamp,status='planned',planned_payload_file='video/posting-intent.json')])
assert not (P/'PUBLISHING.json').exists(), 'Reconcile previous delivery first'
dump(P/'PUBLISHING.json',receipt)
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('\n## Verified export and package\nv1 MP4, cover and caption sidecars verified. CONTENT_PACKAGE.md matches export SHA256 '+rep['sha256']+'. Requested queue, one inherited Instagram target. Receipt prepared before upload/write; no duplicate post creation authorized.\n')
t=R/'TRACKER.json';d=json.loads(t.read_text(encoding='utf-8'));e=next(x for x in d['productions'] if x['slug']==P.name);e.update(stage='publishing',status='in_progress');dump(t,d)
print(json.dumps(dict(bytes=rep['bytes'],sha256=rep['sha256'],caption_chars=len(copy),targets=1,payload_sha256=payload_hash)))
