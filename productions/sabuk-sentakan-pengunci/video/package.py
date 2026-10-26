"""Package the verified export and its exact destination copy."""
from pathlib import Path
import json,hashlib
V=Path(__file__).resolve().parent;P=V.parent
report=json.loads((V/'verification/export.json').read_text(encoding='utf-8'));sound=json.loads((V/'verification/sound-design-export.json').read_text(encoding='utf-8'))
assert report['status']=='passed' and sound['status']=='passed' and report['sha256']==sound['export_sha256']
video=P/report['file'];assert hashlib.sha256(video.read_bytes()).hexdigest()==report['sha256']
for ext in ['srt','vtt']:assert (P/'exports'/f'{P.name}-v1.{ext}').is_file()
caption='''Ditarik pelan, sabuk bisa memanjang. Disentak, malah mengunci. Apa yang berubah di dalamnya?

Pada contoh desain ini, roda inersia menahan perubahan putaran yang mendadak. Gerak antargigi menggeser pelat pembawa, lalu lengannya mengayunkan pengunci ke roda bergigi gulungan.

Roda inersia memicu gerakan. Pengunci dan roda bergigilah yang menahan pelepasan pita.

Ini ilustrasi jalur sensor tarikan pada desain US3918658A. Geometri, jarak, dan waktu disederhanakan untuk memperlihatkan hubungan bagian. Sensor gerak kendaraan memakai jalur lain; detailnya dapat berbeda antardesain.

Referensi teknis: https://patents.google.com/patent/US3918658A/en

#DiBalikBenda #SabukPengaman #CaraKerja #Mekanisme #SainsSehariHari'''
assert len(caption)<=2200 and caption.count('#')==5
(P/'CAPTION.txt').write_text(caption+'\n',encoding='utf-8')
doc=f'''# Content package — sabuk-sentakan-pengunci v1

## Title

Recommended: **Kenapa sabuk mengunci saat disentak?**

Alternatives: “Roda kecil yang memicu pengunci sabuk”; “Siapa yang sebenarnya menahan gulungan sabuk?”

## Instagram @dibalikbenda.id caption

```text
{caption}
```

## Hashtags and editorial keywords

Hashtags: #DiBalikBenda #SabukPengaman #CaraKerja #Mekanisme #SainsSehariHari

Editorial keywords (no dedicated Instagram keyword field used): sabuk pengaman, seatbelt retractor, roda inersia, pengunci gulungan, pinion, pelat pembawa, ratchet, pawl, sensor tarikan

Cover text recommendation: **Pelan bisa. Disentak terkunci.** Matches the existing opening. No separate custom cover was requested or uploaded.

## Verified delivery

- Production: sabuk-sentakan-pengunci; board: di-balik-benda v5; language: Indonesian.
- Target: Trypost Admin's Workspace; Instagram @dibalikbenda.id; account 01a172c9-3761-700a-9798-00febaa9fa90.
- Requested endpoint: next configured queue slot, Asia/Jakarta. Actual returned schedule goes in PUBLISHING.json.
- [Video v1]({report['file']}): {report['duration_s']} seconds, 1080×1920 (9:16), 30fps / 2700 frames, H.264/{report['pixel_format']} MP4 with AAC; {report['bytes']} bytes.
- SHA-256: `{report['sha256']}`.
- Captions burned in; [SRT](exports/{P.name}-v1.srt), [VTT](exports/{P.name}-v1.vtt). Delivery tags removed; 200 spoken words.
- [Copy-only caption](CAPTION.txt), [evidence ledger](SOURCES.md), [storyboard HTML](video/boards/storyboard.html), [full storyboard PNG](video/boards/storyboard.png), [review](video/REVIEW.md).
- Full decode, 90s duration, dimensions and frame count passed. All {len(sound['cue_matches'])} cue waveforms verified in encoded output. Loudness {report['lufs']} LUFS; true peak {report['true_peak_dbtp']} dBTP. Audio measured, not heard; no auditory or phone-speaker review claimed.
- Original narration is 95.44s; derived pitch-preserving tempo 1.08 fits board duration. Native timestamps scaled by that factor; not independently transcribed after treatment.
- Original 2.5D schematic of the cited patent pathway, not a universal product diagram, crash-performance claim or repair guide. Reused illustrative material and bundled editorial cues have provenance in video/assets/audio/sfx; no new SFX generation and no BGM.
- Content type: instagram_reel. Optional cover, sponsorship, mentions, audience designation and service metadata unset.
'''
(P/'CONTENT_PACKAGE.md').write_text(doc,encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write(f'\n## Verified export and content package\nVersion v1, {report["duration_s"]}s, 1080x1920, 30fps/2700 frames, {report["bytes"]} bytes, SHA-256 {report["sha256"]}. Full decode and all {len(sound["cue_matches"])} encoded SFX checks passed. Loudness {report["lufs"]} LUFS, true peak {report["true_peak_dbtp"]} dBTP. Decoded proof inspected. CONTENT_PACKAGE.md/CAPTION.txt tied to this export. Queue delivery already authorized; proceed without another approval gate.\n')
print(json.dumps(dict(status='packaged',caption_characters=len(caption),sha256=report['sha256'])))
