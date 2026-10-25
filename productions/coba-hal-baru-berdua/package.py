"""Package only the verified encoded delivery version."""
from pathlib import Path
import hashlib
import json
P=Path(__file__).resolve().parent;V=P/'video';E=P/'exports'
CAPTION='''Coba hal baru berdua.

Makan di tempat yang sama, pulang lewat jalan yang sama. Kalau waktu berdua terasa itu-itu lagi, pengalaman baru masih kebagian tempat?

Self-expansion, atau perluasan diri, berkaitan dengan bertambahnya pengalaman, kemampuan, dan cara pandang. Salah satu jalannya dalam hubungan: mencoba sesuatu yang baru dan menarik bersama.

Mulai kecil: "Gua pengen bikin sesuatu bareng. Sabtu kita coba resep ini, mau?" Kalau nggak sama-sama tertarik, cari pilihan lain. Selesai mencoba, tanyakan bagian mana yang paling dinikmati.

Riset menemukan peningkatan penilaian kualitas hubungan sesaat setelah tugas baru bersama. Ini bukan jaminan perubahan yang bertahan atau penyelesaian masalah yang dibiarkan. Adegan memasak adalah ilustrasi.

Hal kecil apa yang ingin kalian pelajari bareng?

Sumber: Aron dkk. (2000), https://doi.org/10.1037/0022-3514.78.2.273

#RuangDiAntara #SelfExpansion #WaktuBerdua #RelasiSehariHari'''

def main():
    r=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));sound=json.loads((V/'verification/sound-design-export.json').read_text(encoding='utf-8'))
    file=P/r['file'];assert hashlib.sha256(file.read_bytes()).hexdigest()==r['sha256'];assert r['full_decode']=='passed' and sound['status']=='passed';assert len(CAPTION)<=2200 and len([w for w in CAPTION.split() if w.startswith('#')])<=5
    srt=E/'coba-hal-baru-berdua.srt';assert srt.exists()
    (P/'publish-caption.txt').write_text(CAPTION+'\n',encoding='utf-8')
    data=dict(title='Coba hal baru berdua',alternatives=['Bareng, tapi itu-itu lagi?','Pengalaman baru di waktu berdua'],caption=CAPTION,hashtags=['RuangDiAntara','SelfExpansion','WaktuBerdua','RelasiSehariHari'],keywords='self-expansion, perluasan diri, pengalaman baru, waktu berdua, kegiatan bersama pasangan, hubungan sehari-hari',cover='Itu-itu lagi?',cover_status='unimplemented recommendation; opening frame carries the same text',metadata=r)
    (P/'delivery-copy.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    doc=f'''# Content package — Coba hal baru berdua

Delivered version v1. Instagram @eliansatya in Admin's Workspace; requested endpoint: next configured Trypost queue slot. Agent-verified under delegated automation.

## Title

Recommended: Coba hal baru berdua

Alternatives:

- Bareng, tapi itu-itu lagi?
- Pengalaman baru di waktu berdua

## Instagram caption — ready to paste

{CAPTION}

## Hashtags

#RuangDiAntara #SelfExpansion #WaktuBerdua #RelasiSehariHari

## Editorial keywords

{data['keywords']}

These are editorial search keywords; no separate Instagram tags field is asserted.

## Cover

Suggested copy: "Itu-itu lagi?" matches the opening frame. A separate cover image was not requested or produced; optional cover metadata remains unset.

## Verified delivery metadata

| Field | Value |
| --- | --- |
| Production / board | coba-hal-baru-berdua / ruang-di-antara |
| Board revision | Editorial v1.3; visual and audio v1.2 |
| Workspace | Admin's Workspace / 01a171dd-5281-730d-af07-f2168d17add7 |
| Account | Instagram @eliansatya / 01a172ed-9899-7177-ab1e-627c835e4a57 |
| Content type | instagram_reel |
| Language | Indonesian, lo–gua |
| Version | v1 |
| Duration | {r['duration_s']} seconds |
| Dimensions / aspect | {r['width']} × {r['height']} / 9:16 |
| FPS / frames | {r['fps']} / {r['frames']} |
| Container / video | MP4 / H.264 {r['pixel_format']} |
| Audio | AAC; native-speed ElevenLabs eleven_v4; six reused licensed board cues; no BGM |
| Caption mode | All 193 spoken words burned in; SRT sidecar |
| Caption length / hashtags | {len(CAPTION)} characters / 4 |
| Bytes | {r['bytes']} |
| SHA-256 | {r['sha256']} |
| Encoded audio level | {r['loudness']['input_i']} LUFS / {r['loudness']['input_tp']} dBTP |
| Scheduling request | Next configured available slot, Asia/Jakarta; actual time in PUBLISHING.json after readback |
| Optional service metadata | Unset; no invented feed-sharing, sponsorship, audience or rights declarations |

## Delivery files

- [Video](exports/coba-hal-baru-berdua-v1.mp4)
- [SRT](exports/coba-hal-baru-berdua.srt)
- [Export proof](exports/export-proof.png)
- [Static storyboard](video/boards/storyboard.html)
- [Static storyboard PNG](video/boards/storyboard.png)
- [Sources and limits](SOURCES.md)
- [Verification](VERIFICATION.md)
- [Frozen SFX provenance and credits](video/assets/board/audio/sfx/CREDITS.md)

Objective full decode, levels and six cue waveform-presence checks passed. No direct perceptual listening was available; measurements are not a human listening approval. Planned copy matches the final narration and preserves the short-term research boundary. Source links and media licensing records are retained locally.
'''
    (P/'CONTENT_PACKAGE.md').write_text(doc,encoding='utf-8')
    print(json.dumps(dict(package='CONTENT_PACKAGE.md',caption_characters=len(CAPTION),bytes=r['bytes'],sha256=r['sha256'])))
if __name__=='__main__':main()
