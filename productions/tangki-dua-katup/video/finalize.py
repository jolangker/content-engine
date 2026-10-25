from pathlib import Path
import json,hashlib
from plan import update_tracker
V=Path(__file__).resolve().parent;P=V.parent
report=json.loads((V/'verification/export.json').read_text(encoding='utf-8'))
sound=json.loads((V/'verification/sound-design-export.json').read_text(encoding='utf-8'))
check=json.loads((V/'verification/final-check.json').read_text(encoding='utf-8'))
motion=json.loads((V/'verification/motion.json').read_text(encoding='utf-8'))
cleanup=json.loads((V/'verification/preview-cleanup.json').read_text(encoding='utf-8'))
assert check['ok'] and sound['status']=='passed' and all(c['passed'] for c in sound['cue_matches'])
assert cleanup['listener_released'] and cleanup['state']=='not-running'
assert all(x['seek_deterministic'] for x in motion['results'])
assert (V/'boards/storyboard.png').is_file()
for name in ['tangki-dua-katup-v1.mp4','tangki-dua-katup.srt','tangki-dua-katup.vtt']:assert (P/'exports'/name).is_file()
text=f'''# Verified export v1

- Board: Di Balik Benda v4; original layered 2.5D SVG, Indonesian, 16 explanatory shots.
- Export: [MP4](exports/tangki-dua-katup-v1.mp4), {report['duration_s']} seconds, 1080×1920,30fps,2700 frames,H.264/AAC,{report['bytes']:,} bytes.
- SHA-256: `{report['sha256']}`.
- Captions: burned in plus [SRT](exports/tangki-dua-katup.srt) and [VTT](exports/tangki-dua-katup.vtt);167 aligned spoken words, no delivery tags.
- Full file decoding passed; measured loudness {report['loudness']['input_i']} LUFS and true peak {report['loudness']['input_tp']} dBTP. Six narration waveform windows passed.
- All31 placed SFX verified in actual MP4 with waveform matching, including expected onsets; sources and treatment in video/SFX_SOURCES.md.
- Framework check: zero errors and warnings in lint,runtime,layout,motion,contrast and craft. Informational cropped SVG bounds are intentional macro framing.
- Motion:1,616 samples across16 scenes, constant illustrative chain length and reverse-seek consistency passed. Representative final rendered frames inspected for every scene plus contact macros.
- Static storyboard: [HTML](video/boards/storyboard.html) and [PNG](video/boards/storyboard.png),16 ordered frames,1920×4035. Original pre-audio planning timing is retained; final measured timing is in video/timing.json and STORYBOARD.md. Repaired topology and moving-label anchors are included in both storyboard and film.
- Preview: pipeline-owned server PID28056,port3002,HTTP200 verified while held for render; stopped after export verification and listener release verified.
- Authorization: explicit --automation delegates agent verification and final render. Human approval is false. Endpoint --until=export reached; no content package,hosting or publication executed.

## Evidence and limits

Source map: [SOURCES.md](SOURCES.md). Functional generic lever/flapper/cup-float tank; internal fill-valve diaphragm and bowl siphon are outside scope. Refill/drain overlap preserved. Refill and fault overflow join below the closed outlet seal. Fixed-length chain is an illustrative quadratic,not a catenary simulation. Observation timing is slowed/compressed and labeled.

Direct perceptual listening and phone-speaker review were unavailable. Technical audio presence,alignment and levels passed; no subjective full-speed listening approval is claimed. Original full-script recording retained at native speed and pitch;10.48seconds of observation pauses added between phrases to support the90-second mechanism breakdown.
'''
(P/'VERIFIED.md').write_text(text,encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:
 f.write('\n## Export complete\n\n'+text.split('## Evidence and limits')[0].replace('# Verified export v1','Verified version v1')+'\nNext action: requested endpoint reached; stop. Preview cleanup verified. See VERIFIED.md and video/verification/ for evidence and listening limits.\n')
update_tracker('export','complete')
print(json.dumps({'stage':'export','status':'complete','duration':report['duration_s'],'bytes':report['bytes'],'cues':len(sound['cue_matches']),'preview_stopped':True}))
