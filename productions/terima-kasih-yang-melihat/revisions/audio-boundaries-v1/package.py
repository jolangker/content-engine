"""Package the verified export and exact audience-facing queue copy."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;V=P/'video';E=P/'exports'
CAPTION='''Terima kasih yang melihat.

“Makasih ya, udah masak.” Apa yang sebenarnya lo hargai dari dia malam itu?

Expressed gratitude, atau ungkapan rasa syukur, bisa menyebut manfaat yang lo terima sekaligus menghargai tindakan pasangan. Coba sebut satu usaha yang benar-benar lo lihat: “Makasih udah nyiapin makan walau hari lo juga padat. Gua menghargai waktu yang lo luangin.”

Dalam riset percakapan pasangan, penghargaan yang berfokus pada pasangan berkaitan dengan persepsi bahwa pasangan memahami, menghargai, dan peduli. Ini hubungan yang ditemukan dalam penelitian, bukan jaminan satu kalimat memperbaiki hubungan. Adegan makan malam adalah ilustrasi.

Kalau belum tahu ceritanya, tanya. Beri ruang buat jawabannya, tanpa menagih balasan.

Sumber: Algoe, Kurtz & Hilaire (2016), “Putting the ‘You’ in ‘Thank You’”. https://pmc.ncbi.nlm.nih.gov/articles/PMC4988174/

#RuangDiAntara #UngkapanSyukur #RelasiSehariHari #TerimaKasih'''

def main():
    r=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));s=json.loads((V/'verification/sound-design-export.json').read_text(encoding='utf-8'))
    assert r['full_decode']=='passed' and s['status']=='passed';assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256'];assert len(CAPTION)<=2200
    assert len([w for w in CAPTION.split() if w.startswith('#')])==4
    assert (E/'terima-kasih-yang-melihat.srt').exists()
    data=dict(title='Terima kasih yang melihat',alternatives=['Makasih untuk apa?','Sebut satu usaha yang lo lihat'],caption=CAPTION,hashtags=['RuangDiAntara','UngkapanSyukur','RelasiSehariHari','TerimaKasih'],keywords='expressed gratitude, ungkapan rasa syukur, terima kasih pada pasangan, menghargai usaha, kontribusi pasangan, relasi sehari-hari',cover='Makasih untuk apa?',cover_status='opening frame; no separate cover requested; optional metadata unset',metadata=r)
    (P/'delivery-copy.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(P/'publish-caption.txt').write_text(CAPTION+'\n',encoding='utf-8')
    doc=f'''# Content package — Terima kasih yang melihat

Verified version v1 (arrival correction), Instagram @eliansatya, Admin's Workspace. Requested delivery: next configured Trypost queue slot. Agent-verified under immediate automation; no human approval claimed.

## Title

Recommended: Terima kasih yang melihat

Alternatives:

- Makasih untuk apa?
- Sebut satu usaha yang lo lihat

## Instagram caption — ready to paste

{CAPTION}

## Hashtags

#RuangDiAntara #UngkapanSyukur #RelasiSehariHari #TerimaKasih

## Editorial search keywords

{data['keywords']}

Editorial keywords only; no separate Instagram tags field is asserted.

## Cover

“Makasih untuk apa?” matches the existing opening frame. No separate cover artwork requested or generated; optional cover metadata remains unset.

## Verified delivery metadata

| Field | Value |
| --- | --- |
| Production / board | terima-kasih-yang-melihat / ruang-di-antara |
| Board revision | Editorial v1.3, visual/audio v1.2, implementation 2026-10-21 |
| Workspace | Admin's Workspace / 01a171dd-5281-730d-af07-f2168d17add7 |
| Account | Instagram @eliansatya / 01a172ed-9899-7177-ab1e-627c835e4a57 |
| Content type | instagram_reel |
| Language | Indonesian, lo–gua |
| Version | v1, arrival correction |
| Duration | {r['duration_s']} seconds |
| Dimensions / aspect | {r['width']}x{r['height']} / 9:16 |
| FPS / frames | {r['fps']} / {r['frames']} |
| Container / video | MP4 / H.264 {r['pixel_format']} |
| Audio | AAC; native-speed ElevenLabs eleven_v4, six reused licensed cues, no BGM |
| Captions | All 194 spoken words burned in; SRT sidecar |
| Caption length / hashtags | {len(CAPTION)} characters / 4 |
| Bytes | {r['bytes']} |
| SHA-256 | {r['sha256']} |
| Audio level | {r['loudness']['input_i']} LUFS / {r['loudness']['input_tp']} dBTP |
| Schedule request | Next configured available slot at 14:00 Asia/Jakarta; actual returned schedule in PUBLISHING.json |
| Optional metadata | Unset; no invented feed-sharing, sponsorship, audience or rights declarations |

## Files and evidence

- [MP4](exports/terima-kasih-yang-melihat-v1.mp4)
- [SRT](exports/terima-kasih-yang-melihat.srt)
- [Decoded export proof](exports/export-proof.png)
- [Storyboard HTML](video/boards/storyboard.html) / [PNG](video/boards/storyboard.png)
- [Sources and claim boundaries](SOURCES.md)
- [Verification](VERIFICATION.md)
- [SFX provenance and license](video/assets/board/audio/sfx/CREDITS.md)

Full decode, frame inspection, loudness and six exported cue-presence checks passed. Perceptual listening unavailable; measurements do not establish human listening approval. The public copy preserves association, gives context to the feeling-cared-for gloss and identifies the dinner as illustration. See SOURCES.md C3 for the distinction from the separate emotion loving. Publication itself is not claimed by a queue result.
'''
    (P/'CONTENT_PACKAGE.md').write_text(doc,encoding='utf-8');print(json.dumps(dict(package='CONTENT_PACKAGE.md',caption_characters=len(CAPTION),bytes=r['bytes'],sha256=r['sha256'])))
if __name__=='__main__':main()
