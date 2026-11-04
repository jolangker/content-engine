"""Create platform copy and delivery metadata from the verified export."""
from pathlib import Path
import hashlib,json,shutil
P=Path(__file__).resolve().parent;V=P/'video';R=P.parents[1]
r=json.loads((V/'verification/export.json').read_text());video=P/r['file'];assert video.is_file() and hashlib.sha256(video.read_bytes()).hexdigest()==r['sha256']
caption='''Lo udah bilang bakal buang sampah. Tapi malamnya, kantongnya masih di depan pintu. Rencana lo udah punya tanda buat mulai belum?

Implementation intentions, atau niat implementasi, menghubungkan situasi yang bisa dikenali dengan tindakan yang spesifik. Misalnya: “Setelah cuci piring malam ini, gua bawa kantong sampah ke tempat sampah luar.”

Ini contoh fiktif untuk tugas yang memang sudah disepakati. Waktu dan tempatnya tetap harus memungkinkan. Kalau ada hambatan, ubah rencananya bersama.

Rencana ini nggak menggantikan pembagian tugas yang adil, kesediaan menjalankan tugas, atau tanggung jawab lo atas hasilnya. Pasangan juga nggak otomatis jadi pengingat pribadi.

Saat lo bilang “nanti”, coba lanjutkan: setelah kejadian apa, lo mulai melakukan apa?

Rujukan: Gollwitzer (1999), Implementation intentions: Strong effects of simple plans. https://doi.org/10.1037/0003-066X.54.7.493

#RuangDiAntara #Relasi #KomunikasiPasangan #PsikologiSehariHari'''
assert len(caption)<=2200 and caption.count('#')<=5
copy=dict(title='Nanti itu kapan?',caption=caption,content_type='instagram_reel',meta={},hashtags=['RuangDiAntara','Relasi','KomunikasiPasangan','PsikologiSehariHari'])
(P/'delivery-copy.json').write_text(json.dumps(copy,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
target=json.loads((P/'target_snapshot.json').read_text())['accounts'][0]
doc=f'''# Content package — Nanti itu kapan?

## Titles

Recommended: **Nanti itu kapan?**

Alternatives: “Niatnya sudah ada, mulainya kapan?” / “Setelah cuci piring, baru apa?”

## Instagram caption — ready to paste

{caption}

## Hashtags

#RuangDiAntara #Relasi #KomunikasiPasangan #PsikologiSehariHari

## Editorial keywords

implementation intentions, niat implementasi, rencana jika maka, komunikasi pasangan, pembagian tugas rumah, tanggung jawab, pemicu tindakan

Instagram has no dedicated keyword field for this upload; these are editorial discovery terms, separate from hashtags.

## Cover text

“Nanti itu kapan?” is implemented in the opening frame. No separate cover artwork/upload requested; optional cover setting remains unset.

## Verified delivery metadata

| Field | Value |
| --- | --- |
| Production / version | nanti-itu-kapan / v1 |
| Board | ruang-di-antara, editorial v1.4 / visual and audio v1.2 |
| Language / destination | Indonesian, Instagram Reel |
| Account | @{target['handle']} / {target['workspace_name']} |
| Workspace / account ID | {target['workspace_id']} / {target['social_account_id']} |
| Video | [{video.name}]({r['file']}) |
| Captions | [SRT](exports/nanti-itu-kapan.srt), full spoken words burned in and sidecar |
| Proof | [Encoded-frame sheet](exports/export-proof.png) |
| Actual duration | {r['duration_s']:.6f}s |
| Dimensions / aspect / FPS | {r['width']}x{r['height']} / 9:16 / {r['fps']} |
| Format | MP4, H264 {r['pixel_format']}, AAC |
| Bytes | {r['bytes']} |
| SHA-256 | {r['sha256']} |
| Requested action | Trypost next configured queue slot, Asia/Jakarta; actual schedule in PUBLISHING.json |
| Review | Agent-verified under immediate --automation; no human approval claimed |

All linked files exist and match verified v1. Claim boundaries: [sources](SOURCES.md), [script](SCRIPT.md). Fictional example; no guaranteed remembering, completion or relationship improvement. Research attribution accompanies publishable copy. Narration and six licensed material SFX are self-contained; no BGM. SFX attribution/provenance: video/assets/board/audio/sfx/CREDITS.md and sound_design.json. Perceptual listening unavailable; encoded sound measured rather than heard. Optional publishing settings remain unset. Queue receipt is separate from proof of live publication.
'''
(P/'CONTENT_PACKAGE.md').write_text(doc,encoding='utf-8')
for f in [video,P/'exports/nanti-itu-kapan.srt',P/'exports/export-proof.png']:assert f.is_file(),f
for name in ('publishing_prepare.py','record_delivery.py'):shutil.copy2(R/'productions/buku-sketsa-dibuka-lagi'/name,P/name)
print(json.dumps(dict(package='CONTENT_PACKAGE.md',caption_characters=len(caption),video_sha256=r['sha256'])))
