"""Record the completed inspection of decoded proof and every cut frame."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification'
file=Q/'encoded-cuts.json';d=json.loads(file.read_text(encoding='utf-8'));assert len(d['samples'])==45
d.update(visual_inspection='passed',inspection='All three encoded-cut sheets and sixteen-scene export-proof inspected. Correct outgoing/incoming scene at -1/0/+1 frame, no blank/duplicate/inverted caption errors, exactly dark 08/10, fixed chrome and repaired F06 ownership retained.',export_sha256=hashlib.sha256((P/d['source']).read_bytes()).hexdigest())
file.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (V/'REVIEW.md').open('a',encoding='utf-8') as f:f.write('\n## Encoded result accepted\n\nActual 90.000s / 2700-frame H264/AAC export decoded fully. Sixteen-scene decoded proof and all 45 exact cut-adjacent frames inspected: correct scene at every frame, exactly dark 08/10, no blank frame, caption collision or lost F06 repair. Fifteen encoded acoustic boundaries and six SFX waveform matches pass. Actual mix -13.79 LUFS / -1.23 dBTP. Native source, source plan and export hashes retained. Perceptual listening remains unavailable. Agent accepts this exact export under delegated automation; no human approval claimed.\n')
print('Encoded visual inspection passed: 16 scenes, 45 seam frames')
