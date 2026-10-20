from pathlib import Path
import json,datetime,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1];V=P/'video';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
v=json.loads((P/'exports/verification-v1.json').read_text(encoding='utf-8'));assert v['status']=='passed'
s=json.loads((V/'verification/sound-design-export.json').read_text(encoding='utf-8'));assert s['status']=='passed' and s['export_sha256']==v['sha256']
F=P/v['export'];assert hashlib.sha256(F.read_bytes()).hexdigest()==v['sha256']
caption=(P/'caption.txt').read_text(encoding='utf-8').strip()
package=f'''# Content package — Kabar baik v1

Verified export; prepared under delegated automation. Destination: Instagram @eliansatya, My Organization. Delivery requested: one Buffer draft.

## Title

Recommended: **Kabar baik juga butuh disambut.**

Alternatives:
- Saat “oh, bagus” terasa belum cukup.
- Ada ruang buat ikut senang?

## Instagram caption — ready to paste

{caption}

## Hashtags

#RuangDiAntara #KomunikasiPasangan #KabarBaik #PsikologiHubungan #Relasi

The ready-to-paste caption already contains this set; do not append it twice.

## Editorial search keywords

capitalization, active constructive responding, respons aktif konstruktif, kabar baik pasangan, komunikasi pasangan, merayakan keberhasilan, psikologi hubungan

## Cover

Implemented: opening-frame quotation **“Gue dapat promosi.”** The [cover](exports/cover-v1.png) is extracted from the verified MP4 at 5.357 s. Buffer video thumbnailOffset: 5357 ms, within the measured duration. Cover is an actual episode frame, not a different promise.

## Verified delivery metadata

| Field | Value |
| --- | --- |
| Production | kabar-baik / v1 |
| Board | ruang-di-antara v1.1; implementation 2026-10-20 |
| Language | Indonesian lo–gua |
| Destination | Instagram Reel, @eliansatya |
| Organization / channel | My Organization / 6ad6400e778b240e2f5a8060 |
| Video | [kabar-baik-v1.mp4](exports/kabar-baik-v1.mp4) |
| Duration | {v['duration']:.2f} s |
| Canvas / frame rate | 1080×1920, 9:16, 30 fps |
| Format | MP4, H.264 + AAC stereo 48 kHz |
| Captions | Burned in, plus [SRT](exports/kabar-baik.srt) and [VTT](exports/kabar-baik.vtt) |
| Proof | [14-scene contact sheet](exports/contact-sheet-v1.jpg) |
| Bytes | {v['bytes']} |
| SHA-256 | {v['sha256']} |
| Audio evidence | {v['integrated_lufs']} LUFS integrated / {v['true_peak_dbfs']} dBTP; no clipping; all 6 effects matched in decoded export |
| Voice | ElevenLabs / project-env voice 3mAVBNEqop5UbHtD8oxQ / eleven_v4; 84.48 s native-speed continuous take |
| Music / SFX | No music bed; reused frozen material effects from board library |
| Instagram settings | type reel; shouldShareToFeed true; isAiGenerated true (synthetic narration) |
| Schedule | None: saveToDraft true, mode addToQueue, schedulingType automatic |
| Review | Agent-verified, pre-render authorization delegated; human approval unset |

No sponsorship or third-party brand claims appear. Font licenses are in video/assets/fonts; SFX provenance and credits are in video/.media/audio/sfx and sound_design.json. Original research links and limitations are in [SOURCES.md](SOURCES.md). No realtime creative listen is claimed; perceptual mix/voice assessment remains a limitation of automated QA.

## Delivery status

Local content package complete. Continue the already authorized Cloudinary hosting and Buffer draft action, saving actual provider IDs/status in PUBLISHING.json. This package does not claim the post is live.
'''
(P/'CONTENT_PACKAGE.md').write_text(package,encoding='utf-8')
with (V/'VERIFICATION.md').open('a',encoding='utf-8') as f:
    f.write(f'''\n## Verified export\n\n[MP4](../exports/kabar-baik-v1.mp4): {v['duration']} s, 1080x1920, 30 fps, H.264/AAC stereo 48 kHz, {v['bytes']} bytes. SHA-256 `{v['sha256']}`. Full audiovisual decode passes. Integrated loudness {v['integrated_lufs']} LUFS and true peak {v['true_peak_dbfs']} dBTP; no clipping. All six effects match decoded export near authored time with zero detected timing offsets (similarity 0.815–0.994). See exports/verification-v1.json and verification/sound-design-export.json.\n\nThe decoded 14-scene contact sheet was visually inspected; scene 10 now reads “Buka ceritanya.” Captions, fixed chrome, layout, actor shapes and paths match the intended final sequence. Each scene's landed pose was extracted from the encoded file. No human listening approval is inferred from objective waveform evidence.\n\nRender: HyperFrames 0.8.181, drawelement capture / hardware Intel GPU; 2583 frames; completed in 113.0 s. No desktop-app offer line was emitted.\n''')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:
    f.write(f'\n## Verified local delivery\n\nContent package v1 is complete: 86.10 s MP4, 1080x1920/30 fps, SRT/VTT, extracted cover and decoded contact sheet. Export SHA-256 {v["sha256"]}. Framework and export checks pass; all six SFX detected at their authored times. See CONTENT_PACKAGE.md and video/VERIFICATION.md. Human approval remains unset and realtime listening was unavailable. Next: authorized original-file hosting and one Buffer draft; receipt PUBLISHING.json.\n')
tracker=json.loads((ROOT/'TRACKER.json').read_text(encoding='utf-8-sig'));row=next(x for x in tracker['productions'] if x['slug']=='kabar-baik');row.update(stage='content_package',status='complete');(ROOT/'TRACKER.json').write_text(json.dumps(tracker,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
public_id='content-pipeline/kabar-baik/'+v['sha256']
rp=P/'PUBLISHING.json'
if rp.exists():raise RuntimeError('Existing external receipt must be reconciled, not overwritten')
receipt=dict(schema_version=1,assets=[dict(local_file=v['export'],sha256=v['sha256'],bytes=v['bytes'],public_id=public_id,status='planned',attempt_started_at=now)],posts=[])
rp.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
row.update(stage='publishing',status='in_progress');(ROOT/'TRACKER.json').write_text(json.dumps(tracker,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status='package_verified',public_id=public_id,bytes=v['bytes'],caption_chars=len(caption))))
