"""Package only the verified delivery and persist a stable posting intent."""
from pathlib import Path
import json,hashlib,datetime,re
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
verified=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));assert verified['status']=='passed'
file=P/verified['local_file'];assert hashlib.sha256(file.read_bytes()).hexdigest()==verified['sha256']
caption='''Pedalnya berhenti, rodanya tetap jalan. Kenapa bisa?

Di dalam freehub tipe pawl, pengait menahan sisi tegak gigi saat mengayuh. Saat roda melampaui penggeraknya, sisi miring gigi menekan pengait masuk, lalu pegas mengembalikannya.

Ilustrasi potongan disederhanakan; ukuran, celah, dan kecepatan gerak diperjelas. Bunyi kontak bersifat ilustratif. Desain freehub lain dapat memakai mekanisme berbeda.

Rujukan teknis:
https://patents.google.com/patent/US5460254A/en
https://www.elite-wheels.com/technology/understanding-bicycle-wheel-freehub-mechanisms

#DiBalikBenda #CaraKerja #Sepeda #Mekanisme #Freehub'''
assert len(caption)<=2200 and len(re.findall(r'#\w+',caption))<=5
files=[verified['local_file'],f'exports/{P.name}-v1.srt',f'exports/{P.name}-v1.vtt',f'exports/{P.name}-v1-cover.png']
assert all((P/f).is_file() and (P/f).stat().st_size for f in files)
package=f'''# Paket konten — Pedal Berhenti, Roda Tetap Jalan

## Judul
Rekomendasi: **Pedal Berhenti, Roda Tetap Jalan**

Alternatif:
- Bunyi Klik di Balik Roda Sepeda
- Kenapa Roda Tidak Menyeret Pedal?

## Caption Instagram siap unggah

{caption}

## Hashtag
#DiBalikBenda #CaraKerja #Sepeda #Mekanisme #Freehub

## Kata kunci editorial
cara kerja freehub, sepeda meluncur, pawl, pengait sepeda, ratchet, roda belakang, mekanisme satu arah, bunyi klik sepeda

Instagram tidak memakai kolom tag khusus untuk daftar ini.

## Sampul
Teks yang sudah ada pada gambar: **Pedal berhenti. Roda tetap jalan.**
Gambar diambil dari MP4 final pada2.0detik. Disertakan sebagai aset lokal; pengaturan cover khusus di Trypost tetap tidak disetel, sehingga tidak ada klaim cover ini diterapkan pada unggahan.

## Metadata pengiriman
| Field | Nilai |
| --- | --- |
| Production | {P.name} |
| Board | Di Balik Benda v6 |
| Bahasa | Indonesia |
| Tujuan | Instagram Reel, @dibalikbenda.id |
| Workspace | Admin's Workspace,01a171dd-5281-730d-af07-f2168d17add7 |
| Account ID | 01a172c9-3761-700a-9798-00febaa9fa90 |
| Versi | v1 |
| Durasi terukur | {verified['duration_s']:.3f}detik |
| Resolusi / rasio | 1080x1920 / 9:16 |
| Frame rate / jumlah | 30fps /2700frame |
| Format | MP4,H.264/AAC |
| Bytes | {verified['bytes']} |
| SHA-256 | {verified['sha256']} |
| Caption | Burned-in, dengan sidecar SRT dan VTT |
| Delivery | Slot antrean berikutnya; waktu aktual dicatat di PUBLISHING.json |
| Pengaturan opsional | Cover remote, sponsor, dan deklarasi lain tidak disetel |

## File
- [Video final]({files[0]})
- [SRT]({files[1]})
- [VTT]({files[2]})
- [Sampul lokal]({files[3]})
- [Storyboard HTML](video/boards/storyboard.html)
- [Storyboard PNG](video/boards/storyboard.png)
- [Sumber dan batas klaim](SOURCES.md)
- [Verifikasi file](video/verification/export.json)
- [Review dan batas pemeriksaan](video/REVIEW.md)

Ilustrasi mekanisme orisinal; bentuk, jarak dan waktu skematis. Font Manrope dan IBM Plex Mono disertai lisensi OFL. SFX memakai aset beku proyek dan klik editorial pustaka media-use dengan provenance di video/assets/audio/sfx/assets.json; tidak ada SFX baru yang dibuat. Audio diukur, belum didengar langsung di lingkungan ini.
'''
(P/'CONTENT_PACKAGE.md').write_text(package,encoding='utf-8')
(V/'post-caption.txt').write_text(caption,encoding='utf-8')
identity=dict(provider='trypost',workspace_id='01a171dd-5281-730d-af07-f2168d17add7',workspace_name="Admin's Workspace",social_account_id='01a172c9-3761-700a-9798-00febaa9fa90',service='instagram',handle='dibalikbenda.id')
payload=dict(**identity,content=caption,content_type='instagram_reel',media=dict(export_sha256=verified['sha256']),meta={},requested_delivery='queue',queue='next',requested_due_at=None)
dump(V/'posting-intent.json',dict(payload=payload,payload_sha256=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()))
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Verified export and content package\nFinal MP4 verified90s/2700frames,1080x1920,30fps,H.264/AAC; full decode and all16 decoded proof frames inspected. Export SHA-256 {verified["sha256"]}, {verified["bytes"]}bytes. Caption package matches all201 spoken words. CONTENT_PACKAGE.md includes3 titles, exact Instagram copy,5 hashtags, editorial keywords, local cover and verified delivery links.22 actual-export SFX/15 acoustic seams measured separately; no listening claim. Next: authorized direct upload and queue next for the saved exact board account; then receipt verification and commit.\n')
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));next(x for x in tracker['productions'] if x['slug']==P.name).update(stage='content_package',status='complete');dump(R/'TRACKER.json',tracker)
print(json.dumps(dict(title='Pedal Berhenti, Roda Tetap Jalan',caption_characters=len(caption),hashtags=5,sha256=verified['sha256'])))
