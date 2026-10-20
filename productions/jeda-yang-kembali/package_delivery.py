"""Package the verified local corrective export; external receipts remain version-specific."""
from pathlib import Path
import hashlib
import json

P=Path(__file__).resolve().parent
v=json.loads((P/'exports/verification-v2.json').read_text(encoding='utf-8'))['summary']
a=json.loads((P/'video/audio_meta.json').read_text(encoding='utf-8'))
captions=json.loads((P/'video/caption_groups.json').read_text(encoding='utf-8'))
assert hashlib.sha256((P/v['local_file']).read_bytes()).hexdigest()==v['sha256']
caption=(P/'caption.txt').read_text(encoding='utf-8').strip()
source_duration=a.get('pacing',{}).get('source_duration_s',a['total_duration_s'])
package=f'''# Content package — Jeda yang kembali

Version: corrective local revision v2, exported 2026-10-20. Board: Ruang di Antara v1.1, implementation correction 2026-10-20. Destination identity: Instagram @eliansatya, My Organization. Current delivery: verified local export and package. The existing Buffer draft and Cloudinary receipt describe v1 and have not been replaced.

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

Keywords are editorial discovery guidance. Hashtags already appear once in the ready-to-paste caption.

## Cover text

“Nanti aja.” Terus, kapan?

This text appears in the opening composition. A separate cover asset was not requested.

## Verified delivery metadata

| Field | Value |
| --- | --- |
| Production | jeda-yang-kembali, corrective v2 |
| Board | Ruang di Antara v1.1 / implementation 2026-10-20 |
| Destination | Instagram @eliansatya |
| Language | Indonesian, lo–gua |
| Video | [jeda-yang-kembali-v2.mp4]({v['local_file']}) |
| Format | MP4, H.264 / yuv420p / AAC stereo 48 kHz |
| Size | 1080×1920, 9:16, 30 fps, {v['frames']} frames |
| Duration | {v['duration_s']:.6f} seconds |
| Bytes | {v['bytes']:,} |
| SHA-256 | {v['sha256']} |
| Captions | Burned-in Indonesian, {len(captions)} phrases; [SRT](exports/jeda-yang-kembali-v2.srt) |
| Narration | ElevenLabs / voice `{a['voice_id']}` (Zephlyn verified for this revision) / `{a['tts_model']}`; 187 spoken words |
| Narration timing | Native source {source_duration:.2f}s; {a.get('pacing',{}).get('added_silence_s',0):.2f}s inserted between ideas; no speech-rate change |
| Mix | Voice only; {v['encoded_audio_lufs']} LUFS stereo / {v['encoded_mono_downmix_lufs']} LUFS mono / {v['encoded_true_peak_dbtp']} dBTP |
| Proof | [14-scene contact sheet](exports/jeda-yang-kembali-v2-contact-sheet.jpg), [export verification](exports/verification-v2.json), [verification notes](video/VERIFICATION.md) |
| External delivery | Existing v1 draft retained; v2 has no external upload, schedule or publication |

## Editorial and provenance

Spoken copy, factual claims and source credits are unchanged from v1. Illustrative dialogue and abstract graphics show an interaction pattern, not diagnoses or a guarantee. Source 1 supports the observational concept; source 2 is practitioner guidance rather than a trial of this exact wording. See [SOURCES.md](SOURCES.md). Narration is synthetic. Visuals are deterministic original CSS/SVG using the approved board; local fonts retain OFL licenses. No stock footage or music is used.

The board's shared header/footer fixes series identity across scenes. Content composition changes focal scale, placement and actor presence according to the explanation. Existing [PUBLISHING.json](PUBLISHING.json) receipts identify the preserved v1 export only. Updating that external draft requires a separate version-specific handoff.
'''
(P/'CONTENT_PACKAGE.md').write_text(package,encoding='utf-8')
print(json.dumps({'package':'CONTENT_PACKAGE.md','revision':'v2','video':v['local_file'],'external_delivery':'v1 retained'}))