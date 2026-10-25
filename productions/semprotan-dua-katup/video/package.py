from pathlib import Path
import json,datetime
V=Path(__file__).resolve().parent;P=V.parent;R=P.parent.parent
r=json.loads((V/'verification/export.json').read_text(encoding='utf-8'))
caption='''Kenapa semprotan botol tidak menyedot cairan kembali dari ujungnya?

Pada pompa pemicu konvensional, dua katup satu arah mengatur jalur cairan. Saat ditekan, piston mendorong cairan menuju nosel. Saat dilepas, pegas mengembalikan piston dan ruang pompa terisi lagi dari botol melalui pipa celup.

Gerak tangan bolak-balik, aliran utamanya tetap dari botol menuju nosel.

Ilustrasi skematis untuk satu rancangan konvensional: bentuk katup dan jalur ventilasi berbeda antarproduk. Penampang tidak berskala; gerak diperlambat. Ilustrasi asli dan narasi sintetis.

Rujukan produsen: https://apackaginggroup.com/blogs/news/all-plastic-trigger-sprayer-guide
Penjelasan teknis pembanding: https://patents.google.com/patent/US20140014691A1/en

#DiBalikBenda #CaraKerja #Semprotan #Mekanisme #SainsSehariHari'''
(P/'publish-caption.txt').write_text(caption,encoding='utf-8')
content=f'''# Content package — Di Balik Benda

## Recommended title

Kenapa semprotan botol tidak menyedot balik dari ujungnya?

Alternatives:
- Dua katup di balik satu semprotan
- Saat pemicu dilepas, pompa justru mengisi ulang

## Instagram caption

{caption}

## Hashtags

#DiBalikBenda #CaraKerja #Semprotan #Mekanisme #SainsSehariHari

## Editorial keywords

cara kerja semprotan, pompa pemicu, trigger sprayer, piston, katup satu arah, pipa celup, pengisian ulang, Di Balik Benda

## Cover

Implemented opening-frame cover at 3.7 seconds: “Dua katup. Satu arah.” [Cover](exports/cover.jpg). Buffer thumbnailOffset: 3700 milliseconds.

## Delivery metadata

- Slug: {P.name}; board: di-balik-benda v3; version: v1.
- Account: Instagram @dibalikbenda.id, Buffer channel 6adccfe4778b240e2fafeaf9, My Organization.
- Indonesian Reel, share to feed true, AI disclosure true for original agent-created illustration and synthetic narration.
- User selected immediate publication; Asia/Jakarta. No future queue time or commercial partnership.
- [Video]({r['file']}): {r['duration_s']}s, {r['width']}x{r['height']}, 9:16, {r['fps']} fps, H.264/AAC MP4, {r['bytes']} bytes.
- SHA-256: {r['sha256']}.
- Captions: burned in and [SRT](exports/semprotan-dua-katup.srt).
- [Evidence and limitations](SOURCES.md), [script](SCRIPT.md), [storyboard HTML](video/boards/storyboard.html), [storyboard PNG](video/boards/storyboard.png).
- Verification: zero-error/zero-warning HyperFrames 0.8.193 check; 2700 frames; full decode clean; loudness {r['loudness']['input_i']} LUFS, true peak {r['loudness']['input_tp']} dBTP. Native narration waveform matched at six export locations. Agent verification under automation; no human approval or perceptual listening claimed.
- Local Manrope and IBM Plex Mono with OFL licenses; original SVG; no third-party sound recording or BGM. Voice request/cache/processing in video/audio_meta.json; source preserved.
- Sponsorship, geolocation and optional commercial metadata unset.

## Next action

Host this exact verified file, publish once through Buffer, and save provider receipts in PUBLISHING.json. Completion requires observed sent, then commit this run's changes without push.
'''
(P/'CONTENT_PACKAGE.md').write_text(content,encoding='utf-8')
for path in [r['file'],'exports/semprotan-dua-katup.srt','exports/cover.jpg','video/boards/storyboard.png']:assert (P/path).is_file()
tpath=R/'TRACKER.json';t=json.loads(tpath.read_text(encoding='utf-8'));next(x for x in t['productions'] if x['slug']==P.name).update(stage='content_package',status='complete');tpath.write_text(json.dumps(t,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
ep=P/'EPISODE.md';ep.write_text(ep.read_text(encoding='utf-8')+f'\n## Export and content package\n\nVerified v1: {r["sha256"]}, {r["bytes"]} bytes, exactly 90 seconds, 1080x1920, 30 fps, 2700 frames, H.264/AAC. Full decode, objective loudness and waveform matching passed; delivered proof frames inspected. Package, SRT and cover match this version. Next: hosting and immediate publication under delegated authorization.\n',encoding='utf-8')
print(json.dumps(dict(stage='content_package',status='complete',sha256=r['sha256'],caption_characters=len(caption))))
