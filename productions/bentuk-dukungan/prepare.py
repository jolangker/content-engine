import json, pathlib, shutil, sys

P = pathlib.Path(__file__).resolve().parent
V = P / 'video'
ROOT = P.parent.parent
BOARD = ROOT / 'boards/ruang-di-antara'
sys.path.insert(0, str(ROOT / '.agents/skills/shortform-production/scripts'))
from narration import resolve_voice

voice, voice_resolution = resolve_voice(ROOT)
scenes = json.loads((P / 'scenes.json').read_text(encoding='utf-8'))

for folder in ['assets/fonts', 'assets/board', 'compositions/frames', 'capture/extracted', 'verification']:
    (V / folder).mkdir(parents=True, exist_ok=True)

# Copy fonts from board assets
for f in (BOARD / 'assets').iterdir():
    if f.suffix in ['.ttf', '.txt']:
        shutil.copy2(f, V / 'assets/fonts' / f.name)

# Copy board chrome components
for name in ('chrome.css', 'chrome.html'):
    shutil.copy2(BOARD / 'components' / name, V / 'assets/board' / name)

# Inherit board frame.md spec
spec = (BOARD / 'frame.md').read_text(encoding='utf-8') + '\n\n## Episode adaptation — Bentuk Dukungan\n\nUse one charcoal pressure scene (05). Scene layout and timing are recorded in STORYBOARD.md. Shared chrome is inherited unchanged; content changes scale and placement according to the beat. No B-roll or decorative motion.\n'
(V / 'frame.md').write_text(spec, encoding='utf-8')

# Audio request with script-specific delivery tags for eleven_v4
tags = {
    0: '[intimate, reflective, observant]',
    1: '[quiet tension, frustrated]',
    2: '[thoughtful, vulnerable]',
    3: '[gentle, empathetic]',
    4: '[deliberate, reflective]',
    5: '[clear, explanatory, grounding]',
    6: '[warm, calm, receptive]',
    7: '[structured, analytical]',
    8: '[measured, honest]',
    9: '[soft, grounded, quiet]',
    10: '[practical, encouraging]',
    11: '[direct, conversational]',
    12: '[open, inviting]',
    13: '[deep, quiet, open pause]'
}

tagged = '\n\n'.join((tags.get(i, '') + ' ' + s['vo']).strip() for i, s in enumerate(scenes))
req = {
    'provider': 'elevenlabs',
    'lang': 'id',
    'voice': voice,
    'voice_resolution': voice_resolution,
    'tts_model': 'eleven_v4',
    'speed': 1.0,
    'lines': [{'id': 'narration', 'text': tagged}],
    'bgm': {'mode': 'none'}
}
(V / 'audio_request.json').write_text(json.dumps(req, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Write video/package.json
pkg = {
    "name": "video",
    "private": True,
    "type": "module",
    "scripts": {
        "dev": "npx --yes hyperframes@0.8.181 preview",
        "check": "python ../../../.agents/skills/shortform-production/scripts/sound_design.py --video . --check && npx --yes hyperframes@0.8.181 check",
        "render": "python ../../../.agents/skills/shortform-production/scripts/sound_design.py --video . --check && npx --yes hyperframes@0.8.181 render",
        "publish": "npx --yes hyperframes@0.8.181 publish"
    }
}
(V / 'package.json').write_text(json.dumps(pkg, indent=2) + '\n', encoding='utf-8')

# Write video/hyperframes.json
hfj = {
    "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
    "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
    "paths": {
        "blocks": "compositions",
        "components": "compositions/components",
        "assets": "assets"
    },
    "media": {
        "autoProxy": True
    },
    "authoringSkill": "faceless-explainer"
}
(V / 'hyperframes.json').write_text(json.dumps(hfj, indent=2) + '\n', encoding='utf-8')

# Write video/BRIEF.md
brief = f'''---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "Distinguish emotional support from practical solutions; ask before solving."
destination: instagram-reels
aspect: 1080x1920
language: id
audience: Indonesian adults reflecting on relationship communication
length: 90s
angle: concept
voice: {voice}
execution_policy: automation
human_review: none
pre_render_authorization: delegated by the user's --automation instruction
---

## Intent

Produce one episode for approved Ruang di Antara v1.1. Explain support matching (Cutrona & Russell, 1990; Brock & Lawrence, 2009) through a concrete homecoming exchange, the difference between emotional validation and instrumental advice, and concrete communicative examples for both speaker and listener. Use 14 real visual compositions, intimate lo–gua voice, and a reflective close. Render authorization is delegated.

## Customizations

- Approved board palette (`#F3EDE3`, `#302B28`, `#A34F3F`, `#D8C8B5`), Newsreader + DM Sans, two faceless organic forms.
- One full-script ElevenLabs Zephlyn request with model eleven_v4.
- Indonesian captions, spoken words only, max 2 short lines, within safe zones (y1550–1740).
- Quiet reflective mix. No B-roll, no clinical diagnostic labeling.
'''
(V / 'BRIEF.md').write_text(brief, encoding='utf-8')

# Copy SCRIPT.md
shutil.copy2(P / 'SCRIPT.md', V / 'SCRIPT.md')

print(json.dumps({'scenes': len(scenes), 'words': sum(len(s['vo'].split()) for s in scenes), 'voice': voice, 'voice_resolution': voice_resolution, 'model': 'eleven_v4'}))
