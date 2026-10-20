from pathlib import Path
import json,uuid,datetime,hashlib
P=Path(__file__).resolve().parent
v=json.loads((P/'exports/verification.json').read_text())['summary']
assert hashlib.sha256((P/v['local_file']).read_bytes()).hexdigest()==v['sha256']
caption=(P/'caption.txt').read_text(encoding='utf-8').strip()
package=f'''# Content package — Jeda yang kembali

Version: agent-verified final look v1, exported 2026-10-20. Board: approved Ruang di Antara v1.1. Destination: Instagram @eliansatya, My Organization. Delivery: Buffer draft only, no scheduled time.

## Recommended title

Minta jeda, lalu kapan kembali?

## Alternative hooks

- “Nanti aja.” Tapi, nanti itu kapan?
- Setelah minta ruang, apa percakapannya dilanjutkan?

## Ready-to-paste Instagram caption

{caption}

## Hashtags

#RuangDiAntara #KomunikasiPasangan #PsikologiHubungan #KonflikHubungan #RefleksiDiri

## Editorial keywords

jeda saat konflik, komunikasi pasangan, demand withdraw, pola mendesak menarik diri, kesepakatan kembali, konflik hubungan, ruang dalam hubungan

Instagram has no separate editorial-keyword field in this handoff. Hashtags are already included once in the ready-to-paste caption.

## Cover-text recommendation

“Nanti aja.” Terus, kapan?

The actual opening composition already uses this text; no separate cover artwork was commissioned. A draft may use a 1.5-second video thumbnail frame.

## Verified delivery metadata

| Field | Value |
| --- | --- |
| Slug | jeda-yang-kembali |
| Account | Instagram @eliansatya |
| Language | Indonesian, lo–gua |
| Video | [jeda-yang-kembali.mp4](exports/jeda-yang-kembali.mp4) |
| Format | MP4, H.264 / yuv420p / AAC stereo 48 kHz |
| Size | 1080×1920, 9:16, 30 fps, {v['frames']} frames |
| Duration | {v['duration_s']:.6f} seconds |
| Bytes | {v['bytes']:,} |
| SHA-256 | {v['sha256']} |
| Captions | Burned-in Indonesian, 45 timed phrases; optional [SRT](exports/jeda-yang-kembali.srt) |
| Narration | ElevenLabs Brian / eleven_v4, 187 spoken words; original 84.64s |
| Mix | Voice only, native gain + true-peak ceiling; encoded {v['encoded_audio_lufs']} LUFS stereo / {v['encoded_true_peak_dbtp']} dBTP |
| Proof | [14-scene contact sheet](exports/jeda-yang-kembali-contact-sheet.jpg), [verification](exports/verification.json) |
| Delivery settings | Reel, shouldShareToFeed true, saveToDraft true, automatic scheduling capability; no dueAt |

## Editorial and provenance notes

Illustrative dialogue and abstract animation; no real people or personal relationship claims. Source 1 supports the concept as an observational interaction pattern, not a diagnosis or causal guarantee. Source 2 is practitioner guidance, not a trial of this episode's exact return-time wording. Source credits remain in the caption. Narration is synthetic; graphics are original deterministic animation based on the approved board. No licensed music or stock video used. Local fonts ship with their OFL licenses.

External delivery receipts: [PUBLISHING.json](PUBLISHING.json). The requested draft is complete only when the receipt records its actual saved Buffer ID and draft status.
'''
(P/'CONTENT_PACKAGE.md').write_text(package,encoding='utf-8')
receipt=P/'PUBLISHING.json'
if not receipt.exists():
    asset={'local_file':v['local_file'],'sha256':v['sha256'],'bytes':v['bytes'],'public_id':f'content-pipeline/jeda-yang-kembali/{v["sha256"]}-{uuid.uuid4()}','status':'planned','attempt_started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'requested_overwrite':False}
    receipt.write_text(json.dumps({'schema_version':1,'assets':[asset],'posts':[]},indent=2)+'\n',encoding='utf-8')
tracker=P.parent.parent/'TRACKER.json';data=json.loads(tracker.read_text())
next(e for e in data['productions'] if e['slug']==P.name).update(stage='publishing',status='in_progress')
tracker.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'package':'CONTENT_PACKAGE.md','caption_characters':len(caption),'asset':json.loads(receipt.read_text())['assets'][-1]}))
