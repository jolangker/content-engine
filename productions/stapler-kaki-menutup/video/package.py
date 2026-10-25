from pathlib import Path
import json
V=Path(__file__).resolve().parent;P=V.parent;R=P.parents[1]
report=json.loads((V/'verification/export.json').read_text());sound=json.loads((V/'verification/sound-design-export.json').read_text())
caption='''Kita menekan dari atas. Tapi siapa yang menekuk kaki staples di bawah kertas?

Pada stapler manual dengan tekukan ke dalam, bilah mendorong satu staples menembus kertas. Ujung kakinya lalu mengikuti alur landasan logam yang diam, sehingga kawat menekuk ke dalam.

Sesudah tekanan dilepas, mekanisme penekan kembali dan pengumpan berpegas menyiapkan staples berikutnya.

Ilustrasi skematis asli, tidak berskala. Penampang dibuka dan gerak diperlambat untuk menjelaskan mekanisme; bentuk dan susunan pegas dapat berbeda antarproduk. Narasi sintetis, SFX ilustratif.

Rujukan mekanisme: https://patents.google.com/patent/US4666075A/en
Rujukan landasan: https://patents.google.com/patent/US6244491B1/en

#DiBalikBenda #CaraKerja #Stapler #Mekanisme #SainsSehariHari'''
(P/'publish-caption.txt').write_text(caption,encoding='utf-8')
doc=f'''# Content package — Stapler: siapa yang menekuk kakinya?

## Recommended title
Siapa yang menekuk kaki staples?

Alternatives:
- Satu tekan, lima tahap di dalam stapler
- Bilah mendorong, landasan membentuk

## Instagram caption
{caption}

## Hashtags
#DiBalikBenda #CaraKerja #Stapler #Mekanisme #SainsSehariHari

## Editorial keywords
cara kerja stapler, kaki staples, landasan stapler, anvil, bilah penekan, pengumpan pegas, staple clinching, mekanisme sehari-hari

## Cover
Implemented opening-frame cover at 2.0 s: “Siapa yang menekuk?” [Cover](exports/cover.jpg). Trypost supported media cover offset: 2000 ms. No separately uploaded cover required.

## Delivery metadata
- Production: {P.name}; board di-balik-benda v4; v1; Indonesian.
- Instagram @dibalikbenda.id, Trypost Admin's Workspace, account 01a172c9-3761-700a-9798-00febaa9fa90.
- Requested endpoint: next configured queue slot; timezone Asia/Jakarta. Exact future time belongs to the returned receipt, not an inferred date.
- [MP4]({report['file']}): {report['duration_s']} seconds, 1080×1920 (9:16), 30 fps, 2700 frames, H.264/AAC, {report['bytes']} bytes.
- SHA-256: {report['sha256']}.
- Captions: burned in plus [SRT](exports/stapler-kaki-menutup-v1.srt) and [VTT](exports/stapler-kaki-menutup-v1.vtt), spoken words only.
- [Script](SCRIPT.md), [sources](SOURCES.md), [storyboard HTML](video/boards/storyboard.html), [storyboard PNG](video/boards/storyboard.png).
- Validation: technical checks passed; 2723 temporal scene samples, reverse-seek equality, fixed anvil and conserved wire length; native-to-placed/export narration correlation; full decode; loudness {report['loudness']['input_i']} LUFS and peak {report['loudness']['input_tp']} dBTP; 19 event cues checked against decoded export.
- Perceptual limit: audio measured, not heard; no subjective full-speed audiovisual or phone-speaker listening approval claimed. Agent verification under delegated automation; no fabricated human approval.
- Rights: original schematic SVG, local Manrope/IBM Plex Mono under OFL, ElevenLabs generated narration and reused illustrative SFX with request provenance; Pixabay bundled editorial cue under its content license. Credits under video/assets/.
- Optional sponsorship, location and commercial metadata unset. Audience-facing synthetic narration/illustration disclosure included in caption. No unsupported platform setting inferred.

## Next action
Upload this exact verified file once through Trypost Local, schedule next, read it back, save PUBLISHING.json and commit the production plus its tracker row. Scheduling completion does not claim publication.
'''
(P/'CONTENT_PACKAGE.md').write_text(doc,encoding='utf-8')
for name in [report['file'],'exports/cover.jpg','exports/stapler-kaki-menutup-v1.srt','exports/stapler-kaki-menutup-v1.vtt','video/boards/storyboard.png']:assert (P/name).is_file()
tp=R/'TRACKER.json';t=json.loads(tp.read_text());next(s for s in t['productions'] if s['slug']==P.name).update(stage='content_package',status='complete');tp.write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Verified export and package\n\nv1 {report["sha256"]}, {report["bytes"]} bytes; 90.000 s, 2700 frames, 1080x1920, 30 fps, H.264/AAC. Full decode and waveform checks passed, 19 SFX cues verified in export. CONTENT_PACKAGE.md, cover, SRT and VTT match. Agent-verified under automation; no human or perceptual listening approval. Next: queue delivery then scoped commit.\n')
print(json.dumps({'stage':'content_package','status':'complete','caption_characters':len(caption),'sha256':report['sha256']}))
