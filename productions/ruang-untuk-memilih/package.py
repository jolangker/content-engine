"""Package only the verified export, preserving the script's claim boundaries."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;V=P/'video';E=P/'exports'
CAPTION='''“Terserah lo.” Tapi respons setelahnya masih menyisakan ruang memilih?

Autonomy support, atau dukungan terhadap otonomi, memberi ruang buat pasangan menyampaikan keinginan dan memilih sesuai nilainya, dengan tekanan yang rendah.

Dalam contoh kelas keramik hari Sabtu ini, keinginan punya waktu bersama tetap bisa dibahas. Pendapat yang berbeda pun boleh disampaikan. Yang perlu diperhatikan: apakah alasan masing-masing mendapat ruang, atau kedekatan terasa bergantung pada kepatuhan?

Coba mulai dari: “Apa yang bikin kelas itu penting buat lo?” Dengarkan jawabannya, lalu sampaikan kebutuhan lo juga: “Gua ingin tetap punya waktu berdua. Kita atur waktunya gimana?”

Mendukung pilihan tetap melibatkan perhatian dan batas yang jelas. Satu kalimat belum cukup untuk menilai seluruh hubungan; perhatikan pola responsnya.

Adegan dan contoh dialog adalah ilustrasi. Penjelasan ini bukan diagnosis atau jaminan hasil percakapan.

Rujukan konsep: Weinstein dkk., “Autonomy support and diastolic blood pressure” (definisi dukungan otonomi dalam relasi; video ini tidak membuat klaim kesehatan): https://pmc.ncbi.nlm.nih.gov/articles/PMC4764637/
Penjelasan konsep: University of Rochester, Self-Determination Theory: https://www.urmc.rochester.edu/community-health/patient-care/self-determination-theory

#RuangDiAntara #Otonomi #KomunikasiPasangan #RelasiSehariHari'''
def main():
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    r=read(V/'verification/export.json');s=read(V/'verification/sound-design-export-v2.json');a=read(V/'verification/audio-boundaries-export-v2.json')
    assert r['full_decode']=='passed' and s['status']=='passed' and a['status']=='passed'
    assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
    assert len(CAPTION)<=2200 and len([w for w in CAPTION.split() if w.startswith('#')])<=5
    assert (E/f'{P.name}.srt').exists()
    data=dict(title='Ruang untuk memilih',alternatives=['Terserah, tapi masih boleh beda?','Dukung pilihan, bicarakan dampaknya'],caption=CAPTION,hashtags=['RuangDiAntara','Otonomi','KomunikasiPasangan','RelasiSehariHari'],keywords='autonomy support, dukungan otonomi, pilihan pasangan, waktu bersama, komunikasi pasangan, kesepakatan',cover='Terserah lo?',cover_status='Existing opening frame; no separate cover artwork or optional cover metadata',metadata=r)
    (P/'delivery-copy.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(P/'publish-caption.txt').write_text(CAPTION+'\n',encoding='utf-8')
    doc=f'''# Content package — Ruang untuk memilih

Verified v1 for Instagram @eliansatya, Admin's Workspace. Requested endpoint: next configured Trypost queue slot. Agent-verified under --automation; no human approval claimed.

## Title

Recommended: Ruang untuk memilih

Alternatives:

- Terserah, tapi masih boleh beda?
- Dukung pilihan, bicarakan dampaknya

## Instagram caption — ready to paste

{CAPTION}

## Hashtags

#RuangDiAntara #Otonomi #KomunikasiPasangan #RelasiSehariHari

## Editorial search keywords

{data['keywords']}

Editorial keywords; no dedicated Instagram tags field asserted.

## Cover

“Terserah lo?” matches the existing opening frame. No separate cover artwork requested; optional cover metadata unset.

## Verified delivery metadata

| Field | Value |
| --- | --- |
| Production / board | {P.name} / ruang-di-antara |
| Board revision | Editorial v1.3, visual/audio v1.2, implementation 2026-10-21 |
| Workspace | Admin's Workspace / 01a171dd-5281-730d-af07-f2168d17add7 |
| Account | Instagram @eliansatya / 01a172ed-9899-7177-ab1e-627c835e4a57 |
| Type / language / version | instagram_reel / Indonesian lo–gua / v1 |
| Duration | {r['duration_s']} seconds |
| Dimensions / aspect | {r['width']}x{r['height']} / 9:16 |
| FPS / frames | {r['fps']} / {r['frames']} |
| Container / video / audio | MP4 / H.264 {r['pixel_format']} / AAC |
| Sound | Native-speed ElevenLabs eleven_v4, six reused material cues, no BGM |
| Captions | All 182 spoken words burned in, SRT sidecar |
| Caption length / hashtags | {len(CAPTION)} characters / 4 |
| Bytes | {r['bytes']} |
| SHA-256 | {r['sha256']} |
| Levels | {r['loudness']['input_i']} LUFS / {r['loudness']['input_tp']} dBTP |
| Queue request | Next configured daily 14:00 Asia/Jakarta slot; actual schedule in PUBLISHING.json |
| Optional metadata | Unset; no invented feed-sharing, audience, sponsorship or rights declarations |

## Files and verification

- [MP4](exports/{P.name}-v1.mp4)
- [SRT](exports/{P.name}.srt)
- [Decoded proof](exports/export-proof.png)
- [Storyboard HTML](video/boards/storyboard.html) / [PNG](video/boards/storyboard.png)
- [Sources](SOURCES.md)
- [Review](video/REVIEW.md)
- [SFX credits](video/assets/board/audio/sfx/CREDITS.md)

Actual export full decode, frame count, fifteen encoded acoustic boundaries and all six cue waveform matches pass. Illustrated intermediate states, phone readability and every seam reviewed. Perceptual listening unavailable; measurements do not claim listening approval. Concept, hypothetical illustration and proposed response remain distinct. Scheduling completion does not claim live publication.
'''
    (P/'CONTENT_PACKAGE.md').write_text(doc,encoding='utf-8')
    print(json.dumps(dict(caption_characters=len(CAPTION),sha256=r['sha256'],package='CONTENT_PACKAGE.md')))
if __name__=='__main__':main()
