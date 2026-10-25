from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
f=P/'exports/cerita-belum-selesai-v1.mp4'; sha=hashlib.sha256(f.read_bytes()).hexdigest()
verification=json.loads((P/'video/verification/export.json').read_text(encoding='utf-8'))
assert verification['status']=='passed' and verification['sha256']==sha
caption='''Lo cuma pengen cerita soal hari yang berat, kok obrolannya malah jadi daftar solusi?

Saran mungkin masuk akal. Sebelum menyusun jawaban, coba cek dulu apa yang lagi dibutuhkan.

“Gua dengerin dulu, atau lo pengen kita cari jalan keluar bareng?”

Kalau lo yang cerita: “Gua mau didengerin dulu. Nanti kita pikirin langkahnya.”

Satu respons belum cukup buat menebak niat seseorang. Adegan dan dialog di video ini ilustrasi.

Rujukan: HelpGuide, Active Listening — https://www.helpguide.org/relationships/communication/active-listening
Konteks riset: Weger dkk. (2014) — https://doi.org/10.1080/10904018.2013.813234

#RuangDiAntara #Komunikasi #Mendengarkan #Relasi'''
assert len(caption)<=2200 and caption.count('#')<=5
(P/'publish-caption.txt').write_text(caption,encoding='utf-8')
payload=dict(provider='trypost',workspace_id='01a171dd-5281-730d-af07-f2168d17add7',social_account_id='01a172ed-9899-7177-ab1e-627c835e4a57',content=caption,content_type='instagram_reel',media_source=dict(export_sha256=sha),meta={},requested_delivery='publish',requested_due_at=None)
fingerprint=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
receipt=P/'PUBLISHING.json'
assert not receipt.exists(),'Reconcile existing attempts before setup'
asset=dict(provider='trypost',local_file='exports/'+f.name,sha256=sha,bytes=f.stat().st_size,status='planned',attempt_started_at=now,workspace_id=payload['workspace_id'],source='local_upload')
post=dict(provider='trypost',workspace_id=payload['workspace_id'],workspace_name="Admin's Workspace",social_account_id=payload['social_account_id'],service='instagram',handle='eliansatya',content_type='instagram_reel',export_sha256=sha,payload_sha256=fingerprint,payload_serialization='JSON UTF-8; ensure_ascii=false; sorted keys; comma/colon separators without whitespace',payload=payload,requested_delivery='publish',requested_due_at=None,attempt_started_at=now,status='planned',preflight=dict(account_status='connected',publishes_directly=True,requires_approval=False,duplicate_search='No posts matched daftar solusi on the target account',max_content_length=2200,max_hashtags=5,max_video_duration_sec=900,max_video_bytes=314572800),execution_note='Stage attachment in an unsent post, verify public served video, then immediately publish under the explicit publish-now authorization. No draft review checkpoint.')
receipt.write_text(json.dumps(dict(schema_version=2,assets=[asset],posts=[post]),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
package=f'''# Content package — Cerita belum selesai v1

## Titles

Recommended: Cuma mau cerita, kok jadi daftar solusi?

Alternatives:
- Saran masuk akal, tapi ceritanya belum selesai
- Dengerin dulu atau cari jalan keluar bareng?

## Instagram caption (exact publication copy)

{caption}

## Hashtags

#RuangDiAntara #Komunikasi #Mendengarkan #Relasi

## Editorial keywords

mendengarkan aktif, curhat, respons pasangan, dukungan emosional, komunikasi hubungan, memberi saran, kebutuhan dukungan

## Cover

Opening-frame copy: Cuma mau cerita? No custom cover artwork or cover offset is supplied; optional upload settings remain unset.

## Delivery metadata

- Production: cerita-belum-selesai; board ruang-di-antara v1.2.
- Destination: Instagram @eliansatya; Trypost Admin's Workspace; exact saved account 01a172ed-9899-7177-ab1e-627c835e4a57.
- Requested action: publish now, explicitly requested on 2026-10-25; overrides the earlier export-only cap. Active automation is retained.
- Version: [cerita-belum-selesai-v1.mp4](exports/cerita-belum-selesai-v1.mp4).
- Format: MP4, H.264/AAC, 1080 × 1920 (9:16), 30 fps, 86s, {f.stat().st_size} bytes.
- SHA-256: {sha}.
- Captions: full spoken words burned in, plus [SRT](exports/cerita-belum-selesai.srt). SRT is a local sidecar; the video itself is uploaded.
- [Export proof sheet](exports/proof-sheet.jpg), [verification](VERIFICATION.md), [sources](SOURCES.md).
- No BGM. Board material SFX derived from Pixabay; attribution not required under recorded license; provenance retained in video/assets/board/audio/sfx/CREDITS.md. Local font licenses retained with the composition.
- Required Instagram metadata: none returned by the connected content-type tool. Optional feed-sharing, mentions, custom cover and other declarations are unset.
- Claims: fictional interaction and adaptable speech examples. No comparative research outcome, diagnostic claim or relationship guarantee. Both source links remain in the caption.
'''
(P/'CONTENT_PACKAGE.md').write_text(package,encoding='utf-8')
ep=P/'EPISODE.md';text=ep.read_text(encoding='utf-8');text=text.replace('- until: export','- until: publishing (explicit continuation: publish now via Trypost)').replace('- delivery: package default, capped before packaging by --until=export','- delivery: publish (2026-10-25 explicit continuation)').replace('- external_delivery: none requested; no upload, draft, queue or publication in scope.','- external_delivery: immediate Instagram publication via Trypost, explicitly requested on 2026-10-25.')
text+=f'''\n## Publish-now continuation — {now}\nUser requested “publish sekarang via trypost”, overriding the completed export cap and authorizing immediate publication. Reuse verified video/audio without rebuilding. Target membership remains the saved Instagram @eliansatya account in Admin's Workspace; live connection and direct publishing permissions verified. No prior episode receipt existed; account/content search returned no matching post. Package and exact caption prepared locally. A temporary unsent attachment will be verified before immediate publication; no human draft checkpoint. Publishing receipt: [PUBLISHING.json](PUBLISHING.json).\nBoard account file provenance: boards/ruang-di-antara/ACCOUNTS.json, SHA-256 {hashlib.sha256((ROOT/'boards/ruang-di-antara/ACCOUNTS.json').read_bytes()).hexdigest()}.\n'''
ep.write_text(text,encoding='utf-8')
brief=P/'video/BRIEF.md';text=brief.read_text(encoding='utf-8').replace('until: export','until: publishing').replace('delivery: package','delivery: publish');text+='\n## Publishing continuation\n2026-10-25: explicit publish-now request via Trypost extends the earlier export cap. Use the existing verified export and saved Instagram @eliansatya target. No video revision or regeneration requested.\n';brief.write_text(text,encoding='utf-8')
t=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8'))
next(x for x in t['productions'] if x['slug']==P.name).update(stage='publishing',status='in_progress')
(ROOT/'TRACKER.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(caption_characters=len(caption),hashtags=caption.count('#'),export_sha256=sha,payload_sha256=fingerprint,status='planned')))
