from pathlib import Path
import json
V=Path(__file__).resolve().parent;P=V.parent;R=P.parent.parent
r=json.loads((V/'verification/export.json').read_text(encoding='utf-8'))
caption='''Kunci bisa masuk, tapi belum tentu bisa diputar. Kenapa?

Pada silinder pin konvensional, gerigi anak kunci mengatur tinggi beberapa pasangan pin. Semuanya harus menempatkan titik pertemuan pin bawah dan pin atas pada batas antara inti dan rumah kunci: shear line.

Satu gerigi terlalu rendah atau terlalu tinggi masih dapat menghalangi putaran. Setelah batasnya bebas, inti memutar penggerak di belakangnya.

Contoh ilustratif: lima ruang pin, satu shear line. Penampang tidak berskala dan gerak diperlambat. Ilustrasi dibuat untuk penjelasan; narasi sintetis.

Rujukan: Schlage, Rekeying Quick Start Guide — https://www.schlage.com/content/dam/sch-us/documents/pdf/installation-manuals/P513-325.pdf
Penjelasan silang: https://www.lockwiki.com/index.php/Pin_tumbler

#DiBalikBenda #CaraKerja #Kunci #Mekanisme #SainsSehariHari'''
(P/'publish-caption.txt').write_text(caption,encoding='utf-8')
content=f'''# Content package — Di Balik Benda

## Recommended title

Kenapa kunci masuk, tapi tidak bisa diputar?

Alternatives:
- Gerigi anak kunci sebenarnya mengatur apa?
- Satu batas yang membuat inti kunci bisa berputar

## Instagram caption

{caption}

## Editorial keywords

cara kerja kunci, silinder pin, pin tumbler, shear line, anak kunci, mekanisme pintu, Di Balik Benda

## Cover

Implemented: opening-frame cover at 3.7 seconds, “Masuk, belum tentu berputar”. [Cover](exports/cover.jpg). Buffer video thumbnailOffset: 3700 milliseconds.

## Delivery metadata

- Slug: {P.name}; board: di-balik-benda v3; version: v1.
- Account: Instagram @dibalikbenda.id; exact Buffer channel 6adccfe4778b240e2fafeaf9, My Organization.
- Indonesian; Reel, share to feed true; AI-generated disclosure true for synthetic narration and agent-created illustration.
- Immediate publication explicitly requested; timezone Asia/Jakarta. No future schedule or paid partnership.
- [Video]({r['file']}): {r['duration_s']}s, {r['width']}x{r['height']}, 9:16, {r['fps']}fps, H.264/AAC MP4, {r['bytes']} bytes.
- SHA-256: {r['sha256']}.
- Captions: burned in plus [SRT](exports/kunci-garis-geser.srt).
- [Source and limitations](SOURCES.md), [script](SCRIPT.md), [static board](video/boards/storyboard.html), [board PNG](video/boards/storyboard.png).
- Verification: zero-error/zero-warning HyperFrames check; 2700 frames; full decode clean; loudness {r['loudness']['input_i']} LUFS, true peak {r['loudness']['input_tp']} dBTP. Agent verification under explicit automation; no human approval or perceptual listening claimed.
- Original SVG; local Manrope and IBM Plex Mono fonts with OFL licenses. No third-party audio or music; narration source and processing in video/audio_meta.json.
- Sponsorship and branded-content metadata unset; no supporting context for either.

## Next action

Host this exact verified file with Cloudinary, then publish once through Buffer under the user's selected endpoint. Record remote receipts in PUBLISHING.json.
'''
(P/'CONTENT_PACKAGE.md').write_text(content,encoding='utf-8')
for f in [r['file'],'exports/kunci-garis-geser.srt','exports/cover.jpg','video/boards/storyboard.png']:assert (P/f).is_file()
t=R/'TRACKER.json';d=json.loads(t.read_text());next(x for x in d['productions'] if x['slug']==P.name).update(stage='content_package',status='complete');t.write_text(json.dumps(d,indent=2)+'\n')
ep=P/'EPISODE.md';ep.write_text(ep.read_text(encoding='utf-8')+f'\n## Export and package\n\nVerified v1 export {r["sha256"]}, {r["bytes"]} bytes, exactly {r["duration_s"]}s / 2700 frames, 1080x1920, H.264/AAC. Full decode and objective audio checks passed. CONTENT_PACKAGE.md matches the delivered file, caption, SRT and opening-frame cover. Next: Cloudinary and immediate Buffer publication; no repeated approval gate under active automation.\n',encoding='utf-8')
print(json.dumps(dict(stage='content_package',status='complete',caption_characters=len(caption),export_sha256=r['sha256'])))
