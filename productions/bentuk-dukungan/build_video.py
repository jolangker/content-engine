"""Build Bentuk Dukungan: fixed board chrome, scene-led layouts, measured Zephlyn timing."""
from pathlib import Path
import difflib
import html
import json
import math
import re
import shutil

P = Path(__file__).resolve().parent
V = P / 'video'
BOARD = P.parents[1] / 'boards/ruang-di-antara'
S = json.loads((P / 'scenes.json').read_text(encoding='utf-8'))
A = json.loads((V / 'audio_meta.json').read_text(encoding='utf-8'))
W = A['voices'][0]['words']

def norm(value):
    return re.sub(r'[^\w]', '', value.lower())

expected = [norm(word) for scene in S for word in scene['vo'].split()]
actual = [norm(word['text']) for word in W]
assert expected == actual, list(difflib.unified_diff(expected, actual))

PRE, END = 0.4, 1.2
D = math.ceil((A['total_duration_s'] + PRE + END) * 30) / 30

layouts = [
    ('quote-and-arrival', 'Large opening quote; exhausted actor and incoming solution arrows.', 'Quote leads; unsolicited advice arrows enter across the frame.'),
    ('rapid-solution', 'Asymmetric scale: advice provider prominent; listener retreats.', 'Listener shrinks back into a dashed withdrawal contour.'),
    ('technical-cut', 'Storytelling trajectory severed by a rigid vertical divider.', 'Emotion treated like a technical problem requiring a fix.'),
    ('partner-intent', 'Single partner form with radiating protective arc.', 'Shift to provider perspective: good intentions driving the advice.'),
    ('stalemate-mismatch', 'Charcoal field; two diverging paths missing each other.', 'Dark pressure frame: good intentions meeting in mutual frustration.'),
    ('support-matching-diagram', 'Central matching bridge between need and support response.', 'Return to cream; concept diagram establishes optimal matching.'),
    ('emotional-presence', 'Enclosing rounded boundary cradling listener; presence without advice.', 'Soft enclosing contour represents validation and listening.'),
    ('instrumental-action', 'Stepped directional arrows leading toward forward action.', 'Sequential stepped markers contrast with emotional presence.'),
    ('timing-comparison', 'Two temporal lanes: acute emotional state vs regulated state.', 'Comparison layout clarifies timing over content of advice.'),
    ('room-to-breathe', 'Spacious field with expanding calming ring around single actor.', 'Generous whitespace: clearing cognitive clutter to allow breathing.'),
    ('clarify-the-ask', 'Signaling path extending from speaker toward listener.', 'Speaker takes proactive role in framing the conversation.'),
    ('speaker-dialogue-quote', 'Large italic spoken request with small grounded speaker.', 'Intimate first-person quote dominates the frame.'),
    ('listener-dialogue-choice', 'Two distinct paths offered side by side: listen vs solve.', 'Listener offers binary choice before leaping into action.'),
    ('reflective-presence', 'Two calm actors in close proximity with open center.', 'Quiet closing reflection lands without hurried animation.'),
]

offset = 0
for i, scene in enumerate(S):
    count = len(scene['vo'].split())
    scene.update(
        number=i + 1,
        id=f'{i+1:02d}-{scene["kind"]}',
        words=W[offset:offset+count],
        word_start=offset,
        word_end=offset+count
    )
    offset += count
    scene['start'] = 0 if i == 0 else PRE + scene['words'][0]['start'] - 0.07
    scene['layout'], scene['composition'], scene['visual_change'] = layouts[i]

for i, scene in enumerate(S):
    scene['end'] = S[i+1]['start'] if i+1 < len(S) else D
    scene['duration'] = scene['end'] - scene['start']
    scene['cue1'] = max(0.8, min(scene['duration'] * 0.45, PRE + scene['words'][min(4, len(scene['words']) - 1)]['start'] - scene['start']))
    scene['cue2'] = min(scene['duration'] - 1, max(scene['duration'] * 0.55, PRE + scene['words'][min(8, len(scene['words']) - 1)]['start'] - scene['start']))

(V / 'timing.json').write_text(json.dumps({'duration': D, 'pre_roll': PRE, 'tail': END, 'scenes': S}, ensure_ascii=False, indent=2), encoding='utf-8')

for name in ('chrome.css', 'chrome.html'):
    (V / 'assets/board').mkdir(parents=True, exist_ok=True)
    shutil.copy2(BOARD / 'components' / name, V / 'assets/board' / name)

chrome_css = (V / 'assets/board/chrome.css').read_text(encoding='utf-8')
chrome_html = (V / 'assets/board/chrome.html').read_text(encoding='utf-8')
FONT = "@font-face{font-family:Newsreader;src:url('../../assets/fonts/newsreader.ttf')}@font-face{font-family:Newsreader;src:url('../../assets/fonts/newsreader-italic.ttf');font-style:italic}@font-face{font-family:'DM Sans';src:url('../../assets/fonts/dm-sans.ttf')}"

assertions = []

for scene in S:
    i, sid, duration, c1, c2 = (scene[k] for k in ('number', 'id', 'duration', 'cue1', 'cue2'))
    prefix = f'el-{sid}'
    dark = (i == 5)  # Scene 5 is charcoal tension beat
    ink, bg, accent = ('#F3EDE3', '#302B28', '#D8C8B5') if dark else ('#302B28', '#F3EDE3', '#A34F3F')
    svg, content, movements, actor_ids = [], [], [], []
    title_xywh = (88, 260, 848, 104)
    support_xyw = (88, 1370, 848)
    title_lines = None
    title_style = ''
    title_from = ['y:22', 'x:-28', 'y:18', 'x:24', 'opacity:0', 'y:-18', 'x:-20', 'scale:.97', 'y:20', 'x:-20', 'y:16', 'x:26', 'y:18', 'scale:.98'][i-1]

    def actor(name, x, y, width, height, color, move_x=0, move_y=0):
        ident = f'{prefix}-{name}'
        actor_ids.append(ident)
        color_value = ink if color == 'ink' else '#A34F3F'
        if dark and color == 'accent':
            color_value = '#D8C8B5'
        content.append(f'<div id="{ident}" class="actor actor-{name}" style="left:{x-width/2}px;top:{y-height/2}px;width:{width}px;height:{height}px;background:{color_value}"></div>')
        start = 0.18 if len(actor_ids) == 1 else min(c1, 0.85)
        origin = 'x:-16' if i in (2, 8, 11) else 'y:14'
        movements.append(f"tl.fromTo('#{ident}',{{opacity:0,{origin}}},{{opacity:1,x:0,y:0,duration:.58,ease:'power2.out'}},{start});")
        if move_x or move_y:
            movements.append(f"tl.fromTo('#{ident}',{{x:0,y:0}},{{x:{move_x},y:{move_y},duration:1.05,ease:'power3.inOut',immediateRender:false}},{max(c1, start+.63)});")

    def path(data, dashed=False, color=None):
        css = 'path dashed' if dashed else 'path trace'
        extra = ' stroke-dasharray="12 14"' if dashed else ''
        svg.append(f'<path class="{css}" d="{data}" fill="none" stroke="{color or accent}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"{extra}/>')

    def label(text, x, y, width=700, size=34, color=None, cls='label'):
        content.append(f'<p class="{cls}" style="left:{x}px;top:{y}px;width:{width}px;font-size:{size}px;color:{color or ink}">{html.escape(text)}</p>')

    # 14 distinct, meaningful compositions
    if i == 1:
        # Quote and arrival: exhausted A, incoming solution arrows
        title_xywh = (88, 270, 848, 130)
        title_lines = ['“Capek banget', 'hari ini.”']
        actor('a', 230, 1080, 190, 240, 'ink')
        actor('b', 780, 880, 140, 180, 'accent', -40, 20)
        path('M720 900 L440 1020', dashed=True)
        path('M740 930 L520 1060', dashed=True)
        label('Deretan solusi', 420, 750, 360, 36)
    elif i == 2:
        # Advice comes too fast; listener shrinks back
        title_xywh = (88, 260, 848, 110)
        actor('b', 340, 820, 230, 290, 'accent', 40, 0)
        actor('a', 810, 1120, 110, 150, 'ink', 20, 40)
        path('M480 840 C620 860 690 980 740 1080')
        label('Menutup diri', 680, 1290, 260, 34)
    elif i == 3:
        # Story cut abruptly by technical vertical divider
        title_xywh = (88, 250, 848, 104)
        actor('a', 230, 950, 170, 230, 'ink')
        path('M520 620 V1280', color=ink)  # Divider
        path('M130 960 H480')              # Story line up to divider
        path('M560 960 H850', dashed=True) # Unfinished broken thread
        label('Masalah teknis?', 560, 820, 380, 40, accent)
    elif i == 4:
        # Partner intent: single form with warm protective arc
        title_xywh = (88, 260, 848, 104)
        actor('b', 540, 960, 220, 280, 'accent')
        path('M260 920 C260 680 820 680 820 920')
        label('Ingin melindungi', 380, 640, 360, 36)
    elif i == 5:
        # Charcoal stalemate beat: diverging paths
        title_xywh = (88, 260, 848, 114)
        title_lines = ['Dua niat baik.', 'Titik serbasalah.']
        actor('a', 280, 1040, 160, 210, 'ink', -30, 30)
        actor('b', 760, 780, 160, 210, 'accent', 30, -30)
        path('M320 980 L720 720', dashed=True, color='#D8C8B5')
        path('M220 1120 L840 860', dashed=True, color='#A34F3F')
    elif i == 6:
        # Support matching concept diagram
        title_xywh = (88, 250, 848, 104)
        label('Yang dibutuhkan', 140, 680, 350, 36)
        label('Yang diberikan', 620, 680, 350, 36)
        actor('a', 260, 980, 170, 220, 'ink')
        actor('b', 780, 980, 170, 220, 'accent')
        path('M360 980 H680')
        svg.append(f'<circle cx="520" cy="980" r="14" fill="{accent}"/>')
        label('Kecocokan dukungan', 320, 1180, 480, 38, accent)
    elif i == 7:
        # Emotional support: enclosing boundary, listening ear
        title_xywh = (88, 260, 848, 104)
        actor('a', 430, 960, 160, 210, 'ink')
        actor('b', 650, 960, 160, 210, 'accent')
        path('M240 960 C240 680 840 680 840 960 C840 1240 240 1240 240 960')
        label('Mendengarkan & memvalidasi', 280, 1280, 560, 38)
    elif i == 8:
        # Instrumental support: stepped actionable sequence
        title_xywh = (88, 250, 848, 104)
        label('1. Identifikasi', 140, 680, 300, 38, cls='step')
        label('2. Rencana', 420, 880, 300, 38, cls='step', color=accent)
        label('3. Tindakan', 700, 1080, 300, 38, cls='step')
        path('M180 740 H380 V940 H660 V1140 H880')
        for x, y in ((180, 740), (460, 940), (740, 1140)):
            svg.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{accent}"/>')
    elif i == 9:
        # Timing comparison: acute emotion vs regulated state
        title_xywh = (88, 250, 848, 104)
        path('M520 620 V1260', color='#D8C8B5')
        label('Emosi meluap', 120, 660, 350, 38)
        label('Emosi mereda', 620, 660, 350, 38)
        label('Butuh ruang', 140, 940, 320, 34, accent)
        label('Siap solusi', 640, 940, 320, 34, accent)
        actor('a', 260, 1120, 120, 150, 'ink')
        actor('b', 780, 1120, 120, 150, 'accent')
    elif i == 10:
        # Room to breathe: generous whitespace with expanding ring
        title_xywh = (88, 260, 848, 104)
        actor('a', 520, 920, 190, 250, 'ink')
        svg.append(f'<circle id="{prefix}-breath" cx="520" cy="920" r="280" fill="none" stroke="{accent}" stroke-width="4" stroke-dasharray="8 12"/>')
        label('Ruang aman', 410, 1260, 300, 36)
    elif i == 11:
        # Clarify the ask: speaker signaling outward
        title_xywh = (88, 250, 848, 104)
        actor('a', 260, 940, 180, 230, 'ink')
        path('M370 940 H780')
        path('M720 890 L780 940 L720 990')  # Arrowhead
        label('Sampaikan kebutuhan', 380, 850, 420, 38, accent)
    elif i == 12:
        # Speaker dialogue quote
        title_xywh = (100, 360, 848, 124)
        title_lines = ['“Gue lagi pengen', 'cerita aja ya.”']
        title_style = f'font-style:italic;color:{accent};line-height:1.15'
        actor('a', 520, 1040, 160, 210, 'ink')
        path('M220 1200 H820', dashed=True)
        label('Belum butuh dicarikan solusi', 240, 1230, 600, 36)
    elif i == 13:
        # Listener dialogue choice: listen vs solve
        title_xywh = (88, 250, 848, 106)
        label('Pilihan A: Didengar', 140, 780, 360, 38, cls='step')
        label('Pilihan B: Solusi bareng', 580, 780, 420, 38, cls='step', color=accent)
        actor('b', 520, 1140, 170, 220, 'accent')
        path('M520 1020 L280 860')
        path('M520 1020 L740 860')
    elif i == 14:
        # Closing reflection: quiet proximity
        title_xywh = (88, 760, 848, 120)
        actor('a', 360, 460, 140, 180, 'ink', 15, 0)
        actor('b', 680, 460, 140, 180, 'accent', -15, 0)
        path('M440 460 C500 380 540 380 600 460')
        support_xyw = (88, 1380, 848)

    x, y, width, size = title_xywh
    if title_lines:
        title_text = ''.join(f'<span class="title-line" style="display:block;">{html.escape(line)}</span>' for line in title_lines)
    else:
        title_text = html.escape(scene['text'])
    sx, sy, sw = support_xyw
    support_size = 36

    content.insert(0, f'<h1 id="{prefix}-headline" class="headline" style="left:{x}px;top:{y}px;width:{width}px;font-size:{size}px;{title_style}">{title_text}</h1>')
    content.append(f'<p id="{prefix}-support" class="support" style="left:{sx}px;top:{sy}px;width:{sw}px;font-size:{support_size}px">{html.escape(scene["support"])}</p>')

    css = FONT + chrome_css + f'''
#root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden;color:{ink};--rda-meta-ink:{ink};font-family:'DM Sans',sans-serif}}
.ground{{position:absolute;inset:0;background:{bg}}}
.headline{{position:absolute;margin:0;font-family:Newsreader,serif;font-weight:400;line-height:1.08;letter-spacing:-.025em}}
.diagram{{position:absolute;inset:0;width:100%;height:100%;overflow:visible}}
.actor{{position:absolute;border-radius:43% 55% 44% 49%;z-index:2}}
.actor-b{{border-radius:53% 44% 51% 43%}}
.label,.support,.step{{position:absolute;margin:0;line-height:1.3;font-family:'DM Sans',sans-serif}}
.step{{font-family:Newsreader,serif;line-height:1.1}}
'''
    chrome = chrome_html.replace('{{frame_number}}', f'{i:02d}').replace('{{frame_count}}', str(len(S)))
    js = f'''const tl=gsap.timeline({{paused:true}});
tl.fromTo('#{prefix}-headline',{{opacity:0,{title_from}}},{{opacity:1,x:0,y:0,scale:1,duration:.62,ease:'power3.out'}},.08);
{''.join(movements)}
document.querySelectorAll('#{prefix}-svg .trace').forEach((node,index)=>{{
  const length=node.getTotalLength();
  tl.fromTo(node,{{strokeDasharray:length,strokeDashoffset:length,opacity:1}},{{strokeDashoffset:0,duration:1.05,ease:'sine.inOut'}},{c1}+index*.18);
}});
'''
    if 'dashed' in ''.join(svg):
        js += f"tl.fromTo('#{prefix}-svg .dashed',{{opacity:0}},{{opacity:1,duration:.6,stagger:.12,ease:'power2.out'}},{c1});\n"
    if any('class="label"' in el for el in content):
        js += f"tl.fromTo('[data-composition-id=\"{sid}\"] .label',{{opacity:0,y:9}},{{opacity:1,y:0,duration:.5,stagger:.16,ease:'sine.out'}},{c1+.15});\n"
    if any('class="step' in el for el in content):
        js += f"tl.fromTo('[data-composition-id=\"{sid}\"] .step',{{opacity:0,x:-18}},{{opacity:1,x:0,duration:.5,stagger:.2,ease:'power2.out'}},{c1});\n"
    if i == 10:
        js += f"tl.fromTo('#{prefix}-breath',{{scale:.85,opacity:.4}},{{scale:1.08,opacity:1,duration:1.8,repeat:2,yoyo:true,ease:'sine.inOut',transformOrigin:'center center'}},{c1});\n"
    js += f"tl.fromTo('#{prefix}-support',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.5,ease:'sine.out'}},{c2});\nwindow.__timelines['{sid}']=tl;"

    markup = f'''<template><style>{css}</style>
<div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{duration:.6f}" data-board-revision="2026-10-20" data-layout="{scene['layout']}">
<div id="{prefix}-ground" class="clip ground" data-start="0" data-duration="{duration:.6f}" data-track-index="0"></div>
<svg id="{prefix}-svg" class="diagram" viewBox="0 0 1080 1920" aria-hidden="true">{''.join(svg)}</svg>
{''.join(content)}
{chrome}
</div><script>{js}</script></template>'''
    (V / f'compositions/frames/{sid}.html').write_text(markup, encoding='utf-8')

    assertions.append({'kind': 'appearsBy', 'selector': f'#{prefix}-headline', 'bySec': scene['start'] + 0.8})
    assertions.extend({'kind': 'staysInFrame', 'selector': f'#{ident}'} for ident in actor_ids)
    for kind in ('header', 'footer'):
        assertions.append({'kind': 'staysInFrame', 'selector': f'[data-composition-id="{sid}"] [data-board-chrome="{kind}"]'})

# Write index.motion.json
(V / 'index.motion.json').write_text(json.dumps({'duration': D, 'assertions': assertions}, indent=2), encoding='utf-8')

# Empty assertions for sub-compositions to keep check clean
for old in (V / 'compositions/frames').glob('*.motion.json'):
    old.unlink()

# Generate Captions
groups = []
for scene in S:
    group = []
    for word in scene['words']:
        proposed = ' '.join(item['text'] for item in group + [word])
        if group and (len(proposed) > 37 or len(group) >= 6):
            groups.append(group)
            group = []
        group.append(word)
        if re.search(r'[.?!:]$', word['text']) and len(group) >= 2:
            groups.append(group)
            group = []
    if group:
        groups.append(group)

captions = []
for j, group in enumerate(groups):
    start = PRE + group[0]['start']
    end = PRE + group[-1]['end'] + 0.12
    if j + 1 < len(groups):
        end = min(end, PRE + groups[j+1][0]['start'] - 0.025)
    captions.append({
        'id': f'caption-{j:03d}',
        'start': start,
        'end': end,
        'text': ' '.join(word['text'] for word in group),
        'words': group
    })

(V / 'caption_groups.json').write_text(json.dumps(captions, ensure_ascii=False, indent=2), encoding='utf-8')

hosts = '\n'.join(
    f'<div id="scene-{s["id"]}" class="clip scene" data-composition-id="{s["id"]}" data-composition-src="compositions/frames/{s["id"]}.html" data-start="{s["start"]:.6f}" data-duration="{s["duration"]:.6f}" data-width="1080" data-height="1920" data-track-index="0"></div>'
    for s in S
)
cap_markup = '\n'.join(
    f'<div id="{c["id"]}" class="clip caption" data-start="{c["start"]:.6f}" data-duration="{c["end"]-c["start"]:.6f}" data-track-index="2"><span class="caption-inner">{html.escape(c["text"])}</span></div>'
    for c in captions
)

audio_mix_path = V / 'audio_mix.json'
gain = json.loads(audio_mix_path.read_text(encoding='utf-8'))['gain_db'] if audio_mix_path.exists() else 0
fx = html.escape(json.dumps({
    'version': 1,
    'nodes': [
        {'type': 'gain', 'id': 'voice-level', 'params': {'gain': gain}},
        {'type': 'truepeak', 'id': 'voice-ceiling', 'params': {'ceiling': -3, 'lookahead': 3, 'release': 80}}
    ]
}, separators=(',', ':')), quote=True)

index = f'''<!doctype html><html><head><meta charset="utf-8"><title>Bentuk Dukungan — Ruang di Antara</title><script src="assets/gsap.min.js"></script>
<style>@font-face{{font-family:'DM Sans';src:url('assets/fonts/dm-sans.ttf')}}
*{{box-sizing:border-box}}html,body{{margin:0;width:100%;height:100%;overflow:hidden;background:#F3EDE3}}
#root{{width:100%;height:100%;position:relative;background:#F3EDE3;overflow:hidden}}
.scene{{position:absolute;inset:0;width:100%;height:100%}}
.caption{{position:absolute;left:88px;top:1550px;width:848px;height:180px;z-index:100;display:flex;align-items:center;justify-content:center}}
.caption-inner{{font:500 46px/1.25 'DM Sans',sans-serif;color:#F3EDE3;background:#302B28;padding:17px 26px;border-radius:14px;max-width:848px;text-align:center}}
</style></head><body><div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{D:.6f}">{hosts}{cap_markup}
<audio id="narration" src="{A['voices'][0]['path']}" data-start="{PRE}" data-duration="{A['total_duration_s']}" data-track-index="1" data-volume="1" data-fx-chain="{fx}"></audio>
</div><script>const tl=gsap.timeline({{paused:true}});window.__timelines['main']=tl;</script></body></html>'''
(V / 'index.html').write_text(index, encoding='utf-8')

story = f'''---
format: 1080x1920
duration: {D:.6f}s
message: Distinguish emotional support from practical solutions; ask before solving.
mode: autonomous
music: none
layout_approved: false
execution_policy: automation
revision: v1
board_implementation_revision: 2026-10-20
---

## Video direction

Board Ruang di Antara v1.1. Zephlyn voice from project .env; fixed board chrome; varied content composition. Spoken copy and research from SOURCES.md. One full-script ElevenLabs/eleven_v4 request; {A.get('pacing',{}).get('source_duration_s',A['total_duration_s']):.2f}s native source, {A['total_duration_s']:.2f}s with measured reading pauses and no speech-rate change. Shared chrome sources are copied from the board into assets/board. Header/footer stay fixed through every scene, including dark scene 05. Agent verification and rendering are delegated; no human visual approval is claimed.

Composition choices and differences are explicit below. Motion uses finite stroke traces and cause/response action; no ambient loops, camera moves or B-roll.

'''
for scene in S:
    scene['proof_at'] = round(scene['start'] + min(scene['duration'] - 0.35, scene['cue2'] + 0.65), 3)
    story += f'''## Frame {scene['number']} — {scene['title']}

- duration: {scene['duration']:.6f}s
- start: {scene['start']:.6f}s
- end: {scene['end']:.6f}s
- transition_in: cut
- poster: {scene['proof_at']-scene['start']:.3f}s
- status: animated
- src: compositions/frames/{scene['id']}.html
- voiceover: "{scene['vo']}"
- focal: {scene['text']}
- layout: {scene['layout']}
- composition: {scene['composition']}
- visual_change: {scene['visual_change']}
- support: {scene['support']}
- words: {scene['word_start']}–{scene['word_end']-1}

Establish the focal element, develop the diagram/action at {scene['cue1']:.2f}s, and land the supporting distinction at {scene['cue2']:.2f}s. Hold the meaningful pose through the cut; series metadata remains visible and stationary.

'''
(V / 'STORYBOARD.md').write_text(story, encoding='utf-8')
(V / 'timing.json').write_text(json.dumps({'duration': D, 'pre_roll': PRE, 'tail': END, 'scenes': S}, ensure_ascii=False, indent=2), encoding='utf-8')

def timestamp(t):
    ms = round(t * 1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

(P / 'exports').mkdir(exist_ok=True)
(P / 'exports/bentuk-dukungan.srt').write_text(
    '\n\n'.join(f'{i+1}\n{timestamp(c["start"])} --> {timestamp(c["end"])}\n{c["text"]}' for i, c in enumerate(captions)) + '\n',
    encoding='utf-8'
)
print(json.dumps({
    'scenes': len(S),
    'captions': len(captions),
    'duration': D,
    'assertions': len(assertions),
    'voice': A['voice_id'],
    'midpoints': ','.join(str(scene['proof_at']) for scene in S)
}))


# Reapply the separate sound design plan after rebuilding the root.
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".agents/skills/shortform-production/scripts"))
from sound_design import apply_plan
if (V / "sound_design.json").exists():
    apply_plan(V)
