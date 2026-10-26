"""Package only after the actual export and decoded cue verification pass."""
from pathlib import Path
import json,hashlib
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
report=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));sound=json.loads((V/'verification/sound-design-export.json').read_text(encoding='utf-8'))
assert report['status']=='passed' and sound['status']=='passed' and report['sha256']==sound['export_sha256']
video=P/report['file'];assert hashlib.sha256(video.read_bytes()).hexdigest()==report['sha256']
for ext in ['srt','vtt']:assert (P/'exports'/f'{P.name}-v1.{ext}').is_file()
caption='''Tanpa baterai, kotak musik menyimpan tenaga dan urutan nada di tempat yang berbeda.

Pegas memberi tenaga. Pola pin menentukan urutan petikan. Sisir logam menghasilkan nada, sementara governor membatasi laju putaran.

Episode ini memakai contoh mekanisme pegas dengan governor gesek dua sayap. Ilustrasi disederhanakan, bukan skala asli; pola pin dan bunyi merupakan contoh, bukan reproduksi lagu tertentu.

Referensi teknis: US5449856A — https://patents.google.com/patent/US5449856A/en

Sampel nada ilustratif: “Eb1.aif”, “Eb2.aif”, “Db2.aif” oleh UbikPhonik (Freesound), CC BY 4.0; awal hening dipotong dan level disesuaikan, nada asli dipertahankan.
https://freesound.org/people/UbikPhonik/sounds/177954/
https://freesound.org/people/UbikPhonik/sounds/177953/
https://freesound.org/people/UbikPhonik/sounds/177952/
Lisensi: https://creativecommons.org/licenses/by/4.0/

#DiBalikBenda #KotakMusik #CaraKerja #Mekanisme #SainsSehariHari'''
assert len(caption)<=2200 and caption.count('#')==5
(P/'CAPTION.txt').write_text(caption+'\n',encoding='utf-8')
doc=f'''# Content package — kotak-musik-pin-dan-pegas v1

## Title
Recommended: **Kotak musik: lagunya disimpan di mana?**

Alternatives: “Bagaimana pin kecil membaca sebuah lagu?”; “Kenapa pegas kotak musik tidak melesat bebas?”

## Instagram @dibalikbenda.id caption
```text
{caption}
```

## Hashtags and editorial keywords
Hashtags: #DiBalikBenda #KotakMusik #CaraKerja #Mekanisme #SainsSehariHari

Editorial keywords (Instagram has no separate keywords field here): kotak musik, music box, silinder berpaku, pegas pita, sisir logam, governor gesek, centrifugal governor, pin dan pegas

Cover text recommendation: **Nadanya disimpan di mana?** Matches the existing opening frame. No separate custom cover was requested or uploaded.

## Verified delivery
- Production: kotak-musik-pin-dan-pegas; board: di-balik-benda v4; Indonesian.
- Target: Trypost Admin's Workspace, Instagram @dibalikbenda.id, account 01a172c9-3761-700a-9798-00febaa9fa90.
- Delivery intent: next configured queue slot; timezone Asia/Jakarta. Actual schedule is in PUBLISHING.json after Trypost returns it.
- [Video v1]({report['file']}): {report['duration_s']} seconds, 1080×1920 (9:16), 30fps / 2700 frames, H.264/{report['pixel_format']} MP4 with AAC audio; {report['bytes']} bytes.
- SHA-256: `{report['sha256']}`.
- Captions: burned in; [SRT](exports/{P.name}-v1.srt) and [VTT](exports/{P.name}-v1.vtt) supplied as sidecars. Literal delivery tags removed.
- [Copy-only caption](CAPTION.txt), [evidence ledger](SOURCES.md), [visual storyboard](video/boards/storyboard.html), [full storyboard PNG](video/boards/storyboard.png), [review](video/REVIEW.md).
- Full file decode, dimensions/frame count/duration and waveform cue checks passed. Audio measured {report['lufs']} LUFS, {report['true_peak_dbtp']} dBTP; perceptual listening unavailable and not claimed.
- All source-credit obligations included in the exact caption above. Illustrative music-box samples come from another instrument; no claim of acoustic reconstruction of the drawn cylinder.
- Content type: instagram_reel. No custom cover, sponsorship, mentions, audience designation or optional service metadata inferred.
'''
(P/'CONTENT_PACKAGE.md').write_text(doc,encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Verified export and package\nVersion v1: {report["duration_s"]} seconds, 1080×1920, 30fps, 2700 frames, {report["bytes"]} bytes; SHA-256 {report["sha256"]}. Full decode passed. All {len(sound["cue_matches"])} cues detected in the decoded MP4 with their planned gains/onsets. Loudness {report["lufs"]} LUFS, true peak {report["true_peak_dbtp"]} dBTP. Decoded proof sheet inspected. CONTENT_PACKAGE.md and CAPTION.txt match this exact export and include all CC BY credits. Next: explicit queue delivery already authorized; no human approval claimed.\n')
t=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));next(x for x in t['productions'] if x['slug']==P.name).update(stage='content_package',status='complete');(R/'TRACKER.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(caption_characters=len(caption),export_sha256=report['sha256'],status='packaged')))
