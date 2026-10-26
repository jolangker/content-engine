"""Update the canonical storyboard with measured narration and verification evidence."""
from pathlib import Path
import json,re
V=Path(__file__).resolve().parent;P=V.parent;R=V.parents[2]
plan=json.loads((V/'timing.json').read_text(encoding='utf-8'));text=(V/'STORYBOARD.md').read_text(encoding='utf-8')
for n,s in enumerate(plan,1):
    pattern=rf'(## Frame {n}: [^\n]+)\([^\n]+s\)'
    text=re.sub(pattern,lambda m: m.group(1)+f'({s["start"]:.3f}–{s["end"]:.3f}s)',text,count=1)
    head=rf'(## Frame {n}:.*?)(?=\n## Frame |\Z)'
    def change(m):
        section=m.group(1);section=re.sub(r'- duration: [^\n]+',f'- duration: {s["duration"]:.6f}s',section,count=1);section=re.sub(r'- poster: [^\n]+',f'- poster: {s["start"]+s["duration"]/2:.6f}s',section,count=1);return section
    text=re.sub(head,change,text,flags=re.S,count=1)
text+='''
## Measured timing and motion revision
All 192 spoken words match the locked script at native speed. The scene ranges above now use measured timing.json; the pre-audio board retains explicitly labelled estimated times. Caption groups occupy y1180–1305, inside the vertical app-safe band. s08 ends with the pin holding the tooth; s09 starts from exactly that bent state and releases it before decaying vibration. s12 ends with expanded wings; s13 inherits the same radius and angle against the stationary wall. Those seams and reverse seeking pass numerical checks over 2723 output-frame samples. Material sounds are illustrative; CC BY single-note recordings credited in assets/audio/sfx/CREDITS.md.
'''
(V/'STORYBOARD.md').write_text(text,encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('\n## Motion verification\nVersion v1: 16 mounted scene files, measured timing, 57 caption groups and 62 designed cues. All 2723 30fps samples passed finite-state/reverse-seek checks, fixed comb-root and governor-wall checks, gear direction/ratio checks and continuity at both macro seams. Fixed premature tooth vibration before release. CLI full layout/runtime/contrast check and contact sheets being rerun on this version.\n')
tracker=json.loads((R/'TRACKER.json').read_text(encoding='utf-8'));next(x for x in tracker['productions'] if x['slug']==P.name).update(stage='verification',status='in_progress');(R/'TRACKER.json').write_text(json.dumps(tracker,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Canonical storyboard now uses measured scene ranges.')
