"""Rebuild assets/draw.js from the board's study helpers (the renderer cannot follow paths outside the project)."""
from pathlib import Path
here = Path(__file__).resolve().parent
cut = lambda s: s[:s.rindex('for (const [id, draw] of Object.entries(')]
a = cut((here / '../assets/studies.js').read_text(encoding='utf-8'))
b = cut((here / '../assets/studies-r6.js').read_text(encoding='utf-8')).replace('"use strict";\n', '')
(here / 'assets/draw.js').write_text('// Generated from ../assets/studies.js and ../assets/studies-r6.js (helpers only). Rebuild with build_draw.py.\n' + a + b, encoding='utf-8')
