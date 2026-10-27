"""Package the verified export and exact, source-bounded Instagram copy."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;V=P/'video';E=P/'exports'
CAPTION='''Jeda balasan dan dugaan.

Pesan lo belum dibalas. Dari mana kesimpulan “dia udah nggak peduli” itu datang?

Attribution, atau atribusi, adalah penjelasan yang kita buat tentang penyebab perilaku seseorang. “Belum dibalas” adalah kejadian; “dia sengaja menghindar” menambahkan dugaan tentang niat. Membayangkan dia sibuk juga masih dugaan sebelum ada informasi.

Coba pisahkan kejadian, tafsiran, lalu pertanyaan: “Gua belum dapat balasan sejak tadi. Gua jadi khawatir. Lo bisa ngobrol kapan?” Setelah ada jawaban, lihat juga tindakan dan kesepakatan kalian.

Mengenali atribusi nggak otomatis membuktikan dugaan lo salah. Memahami kemungkinan alasan juga nggak menghapus dampak pengabaian berulang, tanggung jawab, atau batas yang lo butuhkan.

Adegan pesan dan contoh kalimat adalah ilustrasi. Rujukan membedakan penjelasan sebab dan penilaian tanggung jawab/kesengajaan; ini bukan diagnosis atau jaminan hasil percakapan.

Sumber: Ellison dkk. (2016), “Interplay between Marital Attributions and Conflict Behavior in Predicting Depressive Symptoms”. https://pmc.ncbi.nlm.nih.gov/articles/PMC4767684/

#RuangDiAntara #Atribusi #KomunikasiPasangan #RelasiSehariHari'''
def main():
    r=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));s=json.loads((V/'verification/sound-design-export-v2.json').read_text(encoding='utf-8'));a=json.loads((V/'verification/audio-boundaries-export-v2.json').read_text(encoding='utf-8'))
    assert r['full_decode']=='passed' and s['status']=='passed' and a['status']=='passed'
    assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
    assert len(CAPTION)<=2200 and len([w for w in CAPTION.split() if w.startswith('#')])<=5
    assert (E/f'{P.name}.srt').exists()
    data=dict(title='Jeda balasan dan dugaan',alternatives=['Belum dibalas, sudah disimpulkan?','Apa yang lo lihat, apa yang lo simpulkan?'],caption=CAPTION,hashtags=['RuangDiAntara','Atribusi','KomunikasiPasangan','RelasiSehariHari'],keywords='attribution, atribusi, tafsiran pesan, komunikasi pasangan, dugaan tentang niat, batas dalam relasi',cover='Belum dibalas',cover_status='Existing opening frame; no separate artwork requested; optional cover metadata unset',metadata=r)
    (P/'delivery-copy.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(P/'publish-caption.txt').write_text(CAPTION+'\n',encoding='utf-8')
    doc=f'''# Content package — Jeda balasan dan dugaan

Verified v1, Instagram @eliansatya, Admin's Workspace. Requested delivery: next configured Trypost queue slot. Agent-verified under immediate automation; no human approval claimed.

## Title

Recommended: Jeda balasan dan dugaan

Alternatives:

- Belum dibalas, sudah disimpulkan?
- Apa yang lo lihat, apa yang lo simpulkan?

## Instagram caption — ready to paste

{CAPTION}

## Hashtags

#RuangDiAntara #Atribusi #KomunikasiPasangan #RelasiSehariHari

## Editorial search keywords

{data['keywords']}

Editorial keywords; no dedicated Instagram tags field is asserted.

## Cover

“Belum dibalas” matches the existing opening frame. No separate cover artwork requested or generated; optional cover metadata is unset.

## Verified delivery metadata

| Field | Value |
| --- | --- |
| Production / board | {P.name} / ruang-di-antara |
| Board revision | Editorial v1.3, visual/audio v1.2, implementation 2026-10-21 |
| Workspace | Admin's Workspace / 01a171dd-5281-730d-af07-f2168d17add7 |
| Account | Instagram @eliansatya / 01a172ed-9899-7177-ab1e-627c835e4a57 |
| Content type | instagram_reel |
| Language / version | Indonesian lo–gua / v1 |
| Duration | {r['duration_s']} seconds |
| Dimensions / aspect | {r['width']}x{r['height']} / 9:16 |
| FPS / frames | {r['fps']} / {r['frames']} |
| Container / video | MP4 / H.264 {r['pixel_format']} |
| Audio | AAC; native-speed ElevenLabs eleven_v4, six reused licensed cues, no BGM |
| Captions | All 182 words burned in, SRT sidecar |
| Caption length / hashtags | {len(CAPTION)} characters / 4 |
| Bytes | {r['bytes']} |
| SHA-256 | {r['sha256']} |
| Audio measurement | {r['loudness']['input_i']} LUFS / {r['loudness']['input_tp']} dBTP |
| Schedule request | Next configured slot, daily 14:00 Asia/Jakarta; actual schedule in PUBLISHING.json |
| Optional metadata | Unset; no invented feed-sharing, audience, sponsorship or rights declarations |

## Files and verification

- [MP4](exports/{P.name}-v1.mp4)
- [SRT](exports/{P.name}.srt)
- [Decoded export proof](exports/export-proof.png)
- [Storyboard HTML](video/boards/storyboard.html) / [PNG](video/boards/storyboard.png)
- [Sources](SOURCES.md)
- [Review](video/REVIEW.md)
- [SFX credits and provenance](video/assets/board/audio/sfx/CREDITS.md)

Full file decode, encoded frame count/duration, all six cue waveform matches and fifteen acoustic seams pass. Visual samples reviewed at phone scale. Perceptual listening unavailable; audio measurements do not establish human listening approval. Copy preserves the distinction between an inference and observed information and does not excuse repeated impact. Queue completion establishes scheduling, not live publication.
'''
    (P/'CONTENT_PACKAGE.md').write_text(doc,encoding='utf-8')
    print(json.dumps(dict(caption_characters=len(CAPTION),sha256=r['sha256'],package='CONTENT_PACKAGE.md')))
if __name__=='__main__':main()
