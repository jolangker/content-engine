"""Build revision v2: fixed board chrome, scene-led layouts, measured Zephlyn timing."""
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
PRE, END = .4, 1.2
D = math.ceil((A['total_duration_s'] + PRE + END) * 30) / 30
layouts = [
    ('quote-and-gap', 'Large opening quote; unequal forms separated by an interrupted connection.', 'Quote leads; response withdraws across a large gap.'),
    ('diagonal-pursuit', 'Large pursuer upper-left, smaller retreating response lower-right.', 'Flat horizontal relation becomes a descending pursuit.'),
    ('cycle-first', 'Large cycle above a lower concept title.', 'The interaction diagram becomes the focal element.'),
    ('split-attention', 'Charcoal field; original issue left, reactions right.', 'A split field shows attention shifting away from the initial issue.'),
    ('unknown-motive', 'One large actor and an oversized unanswered question.', 'Remove the second actor; uncertainty becomes the focal point.'),
    ('space-first', 'Forms occupy opposing edges; boundaries frame an open center; text below.', 'Open space leads before the explanatory title.'),
    ('agreement-sequence', 'Three typographic agreement steps; no actor pair.', 'Replace the diagram with a staggered verbal structure.'),
    ('spoken-intent', 'Large italic quotation with one small speaker.', 'Switch to intimate first-person speech and asymmetric scale.'),
    ('time-anchor', 'A large 20.00 anchor above two small agreement endpoints.', 'A concrete time dominates the frame.'),
    ('return-route', 'A rising return route links a lower-left and upper-right form.', 'The spatial direction reverses the earlier retreat.'),
    ('rejoined-conversation', 'Compact connected pair above a large lower reflection.', 'Compress the distance and move text below the interaction.'),
    ('missed-agreement', 'Descending typographic sequence: Sepakat. Tertunda. Terulang?', 'Follow-through is represented by repeated broken steps, without an actor pair.'),
    ('safety-boundary', 'One protected form left of a firm boundary; safety words right.', 'One clear boundary and one person replace mutual-response imagery.'),
    ('reflection-and-path', 'Small open return path above a large reflective question.', 'Reduce the diagram and let the closing question carry the frame.'),
]
offset = 0
for i, scene in enumerate(S):
    count = len(scene['vo'].split())
    scene.update(number=i + 1, id=f'{i+1:02d}-{scene["kind"]}', words=W[offset:offset+count], word_start=offset, word_end=offset+count)
    offset += count
    scene['start'] = 0 if i == 0 else PRE + scene['words'][0]['start'] - .07
    scene['layout'], scene['composition'], scene['visual_change'] = layouts[i]
for i, scene in enumerate(S):
    scene['end'] = S[i+1]['start'] if i+1 < len(S) else D
    scene['duration'] = scene['end'] - scene['start']
    scene['cue1'] = max(.8, min(scene['duration']*.45, PRE+scene['words'][min(4,len(scene['words'])-1)]['start']-scene['start']))
    scene['cue2'] = min(scene['duration']-1, max(scene['duration']*.55, PRE+scene['words'][min(8,len(scene['words'])-1)]['start']-scene['start']))
(V / 'timing.json').write_text(json.dumps({'duration': D, 'pre_roll': PRE, 'tail': END, 'scenes': S}, ensure_ascii=False, indent=2), encoding='utf-8')

for name in ('chrome.css', 'chrome.html'):
    (V / 'assets/board').mkdir(parents=True, exist_ok=True)
    shutil.copy2(BOARD / 'components' / name, V / 'assets/board' / name)
chrome_css = (V / 'assets/board/chrome.css').read_text(encoding='utf-8')
chrome_html = (V / 'assets/board/chrome.html').read_text(encoding='utf-8')
FONT = "@font-face{font-family:Newsreader;src:url('../../assets/fonts/newsreader.ttf')}@font-face{font-family:Newsreader;src:url('../../assets/fonts/newsreader-italic.ttf');font-style:italic}@font-face{font-family:'DM Sans';src:url('../../assets/fonts/dm-sans.ttf')}"
assertions = []
for scene in S:
    i, sid, duration, c1, c2 = (scene[k] for k in ('number','id','duration','cue1','cue2'))
    prefix = f'el-{sid}'
    dark = i == 4
    ink, bg, accent = ('#F3EDE3','#302B28','#D8C8B5') if dark else ('#302B28','#F3EDE3','#A34F3F')
    svg, content, movements, actor_ids = [], [], [], []
    title_xywh = (88,260,848,104)
    support_xyw = (88,1370,848)
    title_lines = None
    title_style = ''
    title_from = ['y:22','x:-28','y:18','x:24','opacity:0','y:-18','x:-20','scale:.97','y:20','x:-20','y:16','x:26','y:18','scale:.98'][i-1]

    def actor(name, x, y, width, height, color, move_x=0, move_y=0):
        ident = f'{prefix}-{name}'
        actor_ids.append(ident)
        color_value = ink if color == 'ink' else '#A34F3F'
        content.append(f'<div id="{ident}" class="actor actor-{name}" style="left:{x-width/2}px;top:{y-height/2}px;width:{width}px;height:{height}px;background:{color_value}"></div>')
        # Motion has a cause and a reaction; entrances follow the scene's direction.
        start = .18 if len(actor_ids) == 1 else min(c1, .85)
        origin = 'x:-16' if i in (2,10) else 'y:14'
        movements.append(f"tl.fromTo('#{ident}',{{opacity:0,{origin}}},{{opacity:1,x:0,y:0,duration:.58,ease:'power2.out'}},{start});")
        if move_x or move_y:
            movements.append(f"tl.fromTo('#{ident}',{{x:0,y:0}},{{x:{move_x},y:{move_y},duration:1.05,ease:'power3.inOut',immediateRender:false}},{max(c1,start+.63)});")

    def path(data, dashed=False, color=None):
        css = 'path dashed' if dashed else 'path trace'
        extra = ' stroke-dasharray="12 14"' if dashed else ''
        svg.append(f'<path class="{css}" d="{data}" fill="none" stroke="{color or accent}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"{extra}/>')

    def label(text, x, y, width=700, size=34, color=None, cls='label'):
        content.append(f'<p class="{cls}" style="left:{x}px;top:{y}px;width:{width}px;font-size:{size}px;color:{color or ink}">{html.escape(text)}</p>')

    if i == 1:
        title_xywh=(88,280,848,134);title_lines=['“Nanti aja.”','Terus, kapan?']
        actor('a',215,1090,190,245,'ink');actor('b',750,1010,140,185,'accent',75,-15)
        path('M315 1080 H470');path('M560 1060 L680 1015',True)
        label('Kapan?',455,1180,300,52)
    elif i == 2:
        title_xywh=(88,260,670,116)
        actor('a',215,810,220,285,'ink',110,35);actor('b',790,1135,105,145,'accent',30,55)
        path('M330 825 C530 815 605 1050 735 1095',True)
        label('Minta jawaban',88,1040,380,36);label('Mundur',675,1280,240,34)
    elif i == 3:
        title_xywh=(88,1120,848,100);support_xyw=(88,1400,848)
        actor('a',220,710,155,210,'ink',20,0);actor('b',780,710,155,210,'accent',-20,0)
        path('M250 590 C360 375 700 375 760 590');path('M755 835 C645 1040 365 1040 250 835')
        label('Mendesak',380,340,390,42);label('Menjauh',395,1000,330,42)
    elif i == 4:
        title_xywh=(88,250,848,104)
        path('M500 680 V1220',color='#D8C8B5')
        label('Persoalan awal',88,690,360,40);label('Cara kita ngobrol',560,690,370,40)
        svg.append(f'<circle cx="235" cy="945" r="25" fill="none" stroke="{ink}" stroke-width="5"/>')
        actor('b',655,1025,110,145,'accent',20,-30)
        actor('c',845,915,80,115,'ink')
        path('M290 955 C440 1190 650 1220 760 1090',True)
    elif i == 5:
        title_xywh=(88,250,790,104)
        actor('a',270,1005,230,300,'ink')
        content.append(f'<div id="{prefix}-question" class="hero" style="left:635px;top:690px;width:260px;font-size:340px">?</div>')
        path('M410 990 L610 880',True)
        label('Alasannya belum diketahui',490,1200,440,38)
    elif i == 6:
        title_xywh=(88,1110,848,112);support_xyw=(88,1400,848)
        actor('a',205,675,185,250,'ink',-20,0);actor('b',820,675,135,190,'accent',20,0)
        path('M405 410 V920',True);path('M625 410 V920',True)
        label('Ruang untuk mereda',325,975,600,36)
    elif i == 7:
        title_xywh=(88,270,848,106)
        title_lines=['Tujuannya.','Waktunya.','Tindak lanjutnya.']
        title_style='line-height:1.1'
        path('M105 1140 H905')
        for x in (105,505,905):svg.append(f'<circle cx="{x}" cy="1140" r="11" fill="{accent}"/>')
        support_xyw=(88,1310,848)
    elif i == 8:
        title_xywh=(115,390,790,120);title_style=f'font-style:italic;color:{accent}'
        actor('a',790,1190,145,195,'accent')
        path('M165 1040 C345 1020 510 1110 650 1150')
        label('Contoh bahasa',88,1180,500,32)
    elif i == 9:
        title_xywh=(88,250,848,92)
        content.append(f'<div id="{prefix}-time" class="hero" style="left:88px;top:660px;width:848px;font-size:260px;letter-spacing:-.055em">20.00</div>')
        actor('a',205,1170,100,130,'ink');actor('b',815,1170,100,130,'accent')
        path('M265 1170 H755');path('M505 1120 V1220')
    elif i == 10:
        title_xywh=(88,250,670,104)
        actor('a',210,1040,135,180,'ink',55,-25);actor('b',780,600,160,215,'accent',-25,30)
        path('M290 1030 C615 1170 930 950 785 735')
        label('Kembali sesuai kesepakatan',88,1220,800,38)
    elif i == 11:
        title_xywh=(88,850,848,132);title_lines=['Mereda, lalu','kembali.']
        actor('a',340,510,180,240,'ink',18,0);actor('b',660,510,180,240,'accent',-18,0)
        path('M445 510 H555')
        label('Lanjut membahas',88,1260,700,36)
    elif i == 12:
        title_xywh=(88,250,848,102);support_xyw=(88,1400,848)
        label('Sepakat.',88,800,650,85,cls='step step-a')
        label('Tertunda.',280,1010,650,96,accent,cls='step step-b')
        label('Terulang?',500,1210,435,100,accent,cls='step step-c')
        path('M110 920 H250',True);path('M330 1135 H460',True)
    elif i == 13:
        title_xywh=(88,250,848,104)
        actor('a',285,1030,205,275,'ink',-20,0)
        path('M550 710 V1280',color=ink)
        label('Keselamatan lo lebih dulu',625,820,300,48)
    elif i == 14:
        title_xywh=(88,790,848,118)
        actor('a',325,445,105,140,'ink',15,0);actor('b',695,445,130,175,'accent',-15,0)
        path('M395 445 C465 325 555 325 615 445')
    x,y,width,size=title_xywh
    if title_lines:
        gap = 'margin-bottom:90px;' if i == 7 else ''
        title_text=''.join(f'<span class="title-line" style="display:block;{gap}">{html.escape(line)}</span>' for line in title_lines)
    else:
        title_text=html.escape(scene['text'])
    sx,sy,sw=support_xyw
    support_size=32 if i in (3,6,12) else 37
    content.insert(0,f'<h1 id="{prefix}-headline" class="headline" style="left:{x}px;top:{y}px;width:{width}px;font-size:{size}px;{title_style}">{title_text}</h1>')
    content.append(f'<p id="{prefix}-support" class="support" style="left:{sx}px;top:{sy}px;width:{sw}px;font-size:{support_size}px">{html.escape(scene["support"])}</p>')
    css=FONT+chrome_css+f'''
#root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden;color:{ink};--rda-meta-ink:{ink};font-family:'DM Sans',sans-serif}}
.ground{{position:absolute;inset:0;background:{bg}}}
.headline{{position:absolute;margin:0;font-family:Newsreader,serif;font-weight:400;line-height:1.06;letter-spacing:-.025em}}
.diagram{{position:absolute;inset:0;width:100%;height:100%;overflow:visible}}
.actor{{position:absolute;border-radius:43% 55% 44% 49%;z-index:2}}
.actor-b{{border-radius:53% 44% 51% 43%}}
.label,.support,.step{{position:absolute;margin:0;line-height:1.3;font-family:'DM Sans',sans-serif}}
.step{{font-family:Newsreader,serif;line-height:1.06}}
.hero{{position:absolute;font-family:Newsreader,serif;line-height:1.05}}
'''
    chrome=chrome_html.replace('{{frame_number}}',f'{i:02d}').replace('{{frame_count}}',str(len(S)))
    js=f'''const tl=gsap.timeline({{paused:true}});
tl.fromTo('#{prefix}-headline',{{opacity:0,{title_from}}},{{opacity:1,x:0,y:0,scale:1,duration:.62,ease:'power3.out'}},.08);
{''.join(movements)}
// Stroke-trace primitive adapted from the installed registry component: measured geometry, one finite reveal.
document.querySelectorAll('#{prefix}-svg .trace').forEach((node,index)=>{{
 const length=node.getTotalLength();
 tl.fromTo(node,{{strokeDasharray:length,strokeDashoffset:length,opacity:1}},{{strokeDashoffset:0,duration:1.05,ease:'sine.inOut'}},{c1}+index*.18);
}});
'''
    if 'dashed' in ''.join(svg):
        js+=f"tl.fromTo('#{prefix}-svg .dashed',{{opacity:0}},{{opacity:1,duration:.6,stagger:.12,ease:'power2.out'}},{c1});\n"
    if any('class="label"' in element for element in content):
        js+=f"tl.fromTo('[data-composition-id=\"{sid}\"] .label',{{opacity:0,y:9}},{{opacity:1,y:0,duration:.5,stagger:.16,ease:'sine.out'}},{c1+.15});\n"
    if i == 7:
        js+=f"tl.fromTo('#{prefix}-headline .title-line',{{opacity:0,x:-20}},{{opacity:1,x:0,duration:.5,stagger:{max(.6,(c2-.2)/2)},ease:'power2.out'}},.12);\n"
    if i == 12:
        for cls,at in [('step-a',.4),('step-b',c1),('step-c',c2)]:
            js+=f"tl.fromTo('[data-composition-id=\"{sid}\"] .{cls}',{{opacity:0,x:-24}},{{opacity:1,x:0,duration:.5,ease:'power2.out'}},{at});\n"
    if i in (5,9):
        js+=f"tl.fromTo('#{prefix}-{'question' if i==5 else 'time'}',{{opacity:0,scale:.94}},{{opacity:1,scale:1,duration:.7,ease:'power2.out'}},{c1});\n"
    js+=f"tl.fromTo('#{prefix}-support',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.5,ease:'sine.out'}},{c2});\nwindow.__timelines['{sid}']=tl;"
    markup=f'''<template><style>{css}</style>
<div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-duration="{duration:.6f}" data-board-revision="2026-10-20" data-layout="{scene['layout']}">
<div id="{prefix}-ground" class="clip ground" data-start="0" data-duration="{duration:.6f}" data-track-index="0"></div>
<svg id="{prefix}-svg" class="diagram" viewBox="0 0 1080 1920" aria-hidden="true">{''.join(svg)}</svg>
{''.join(content)}
{chrome}
</div><script>{js}</script></template>'''
    (V / f'compositions/frames/{sid}.html').write_text(markup,encoding='utf-8')
    assertions.append({'kind':'appearsBy','selector':f'#{prefix}-headline','bySec':scene['start']+.8})
    assertions.extend({'kind':'staysInFrame','selector':f'#{ident}'} for ident in actor_ids)
    for kind in ('header','footer'):
        assertions.append({'kind':'staysInFrame','selector':f'[data-composition-id="{sid}"] [data-board-chrome="{kind}"]'})

# Keep one root sidecar: all assertions resolve uniquely on the assembled timeline.
(V / 'index.motion.json').write_text(json.dumps({'duration':D,'assertions':assertions},indent=2),encoding='utf-8')
# Superseded per-scene v1 assertions referenced actors that some v2 scenes deliberately omit.
for old in (V / 'compositions/frames').glob('*.motion.json'):
    old.write_text(json.dumps({'duration':next(s['duration'] for s in S if s['id']==old.name.removesuffix('.motion.json')),'assertions':[]},indent=2),encoding='utf-8')

groups=[]
for scene in S:
    group=[]
    for word in scene['words']:
        proposed=' '.join(item['text'] for item in group+[word])
        if group and (len(proposed)>37 or len(group)>=6):groups.append(group);group=[]
        group.append(word)
        if re.search(r'[.?!:]$',word['text']) and len(group)>=2:groups.append(group);group=[]
    if group:groups.append(group)
captions=[]
for j,group in enumerate(groups):
    start=PRE+group[0]['start'];end=PRE+group[-1]['end']+.12
    if j+1<len(groups):end=min(end,PRE+groups[j+1][0]['start']-.025)
    captions.append({'id':f'caption-{j:03d}','start':start,'end':end,'text':' '.join(word['text'] for word in group),'words':group})
(V / 'caption_groups.json').write_text(json.dumps(captions,ensure_ascii=False,indent=2),encoding='utf-8')
hosts='\n'.join(f'<div id="scene-{s["id"]}" class="clip scene" data-composition-id="{s["id"]}" data-composition-src="compositions/frames/{s["id"]}.html" data-start="{s["start"]:.6f}" data-duration="{s["duration"]:.6f}" data-width="1080" data-height="1920" data-track-index="0"></div>' for s in S)
cap_markup='\n'.join(f'<div id="{c["id"]}" class="clip caption" data-start="{c["start"]:.6f}" data-duration="{c["end"]-c["start"]:.6f}" data-track-index="2"><span class="caption-inner">{html.escape(c["text"])}</span></div>' for c in captions)
audio_mix_path=V / 'audio_mix.json'
gain=json.loads(audio_mix_path.read_text(encoding='utf-8'))['gain_db'] if audio_mix_path.exists() else 0
fx=html.escape(json.dumps({'version':1,'nodes':[{'type':'gain','id':'voice-level','params':{'gain':gain}},{'type':'truepeak','id':'voice-ceiling','params':{'ceiling':-3,'lookahead':3,'release':80}}]},separators=(',',':')),quote=True)
index=f'''<!doctype html><html><head><meta charset="utf-8"><title>Jeda yang kembali — v2</title><script src="assets/gsap.min.js"></script>
<style>@font-face{{font-family:'DM Sans';src:url('assets/fonts/dm-sans.ttf')}}
*{{box-sizing:border-box}}html,body{{margin:0;width:100%;height:100%;overflow:hidden;background:#F3EDE3}}
#root{{width:100%;height:100%;position:relative;background:#F3EDE3;overflow:hidden}}
.scene{{position:absolute;inset:0;width:100%;height:100%}}
.caption{{position:absolute;left:88px;top:1550px;width:848px;height:180px;z-index:100;display:flex;align-items:center;justify-content:center}}
.caption-inner{{font:500 46px/1.25 'DM Sans',sans-serif;color:#F3EDE3;background:#302B28;padding:17px 26px;border-radius:14px;max-width:848px;text-align:center}}
</style></head><body><div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{D:.6f}">{hosts}{cap_markup}
<audio id="narration" src="{A['voices'][0]['path']}" data-start="{PRE}" data-duration="{A['total_duration_s']}" data-track-index="1" data-volume="1" data-fx-chain="{fx}"></audio>
</div><script>const tl=gsap.timeline({{paused:true}});window.__timelines['main']=tl;</script></body></html>'''
(V / 'index.html').write_text(index,encoding='utf-8')

story=f'''---
format: 1080x1920
duration: {D:.6f}s
message: A pause needs an explicit and kept agreement to return.
mode: autonomous
music: none
layout_approved: false
execution_policy: automation
revision: v2
board_implementation_revision: 2026-10-20
---

## Video direction

User-authorized corrective revision: Zephlyn from project .env; fixed board chrome; varied content composition. Spoken copy and sources are unchanged. One full-script ElevenLabs/eleven_v4 request; {A.get('pacing',{}).get('source_duration_s',A['total_duration_s']):.2f}s native source, {A['total_duration_s']:.2f}s with measured reading pauses and no speech-rate change. Shared chrome sources are copied from the board into assets/board. Header/footer stay fixed through every scene, including dark scene 04. Agent verification and rendering remain delegated; no new human visual approval is claimed.

Composition choices and differences are explicit below. Motion uses finite stroke traces and cause/response action; no ambient loops, camera moves or B-roll. The installed svg-stroke-trace primitive supplies the measured-path technique; its decorative drift/glow is omitted to preserve board direction.

'''
for scene in S:
    scene['proof_at']=round(scene['start']+min(scene['duration']-.35,scene['cue2']+.65),3)
    story+=f'''## Frame {scene['number']} — {scene['title']}

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
(V / 'STORYBOARD.md').write_text(story,encoding='utf-8')
(V / 'timing.json').write_text(json.dumps({'duration':D,'pre_roll':PRE,'tail':END,'scenes':S},ensure_ascii=False,indent=2),encoding='utf-8')

def timestamp(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(P / 'exports').mkdir(exist_ok=True)
(P / 'exports/jeda-yang-kembali-v2.srt').write_text('\n\n'.join(f'{i+1}\n{timestamp(c["start"])} --> {timestamp(c["end"])}\n{c["text"]}' for i,c in enumerate(captions))+'\n',encoding='utf-8')
print(json.dumps({'scenes':len(S),'captions':len(captions),'duration':D,'assertions':len(assertions),'voice':A['voice_id'],'midpoints':','.join(str(scene['proof_at']) for scene in S)}))


# Reapply the separate sound design plan after rebuilding the root.
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".agents/skills/shortform-production/scripts"))
from sound_design import apply_plan
if (V / "sound_design.json").exists():
    apply_plan(V)
