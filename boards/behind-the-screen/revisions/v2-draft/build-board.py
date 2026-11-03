"""Build the v2 illustrated board and motion-planning poses. Static files only."""
from pathlib import Path
from html import escape
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
STUDIES = ROOT / 'studies'
ASSETS.mkdir(exist_ok=True)
STUDIES.mkdir(exist_ok=True)
FONT_SOURCE = ROOT.parents[1] / '.agents' / 'skills' / 'canvas-design' / 'canvas-fonts'
FILES = ['BricolageGrotesque-Bold.ttf', 'BricolageGrotesque-OFL.txt',
         'InstrumentSans-Regular.ttf', 'InstrumentSans-Bold.ttf', 'InstrumentSans-OFL.txt']
manifest = []
for name in FILES:
    shutil.copy2(FONT_SOURCE / name, ASSETS / name)
    manifest.append({'file': name, 'sha256': hashlib.sha256((ASSETS/name).read_bytes()).hexdigest()})
(ASSETS/'asset-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')

C = {'ground':'#F0EFF8', 'white':'#FFFFFF', 'ink':'#22213B',
     'blue':'#4054E8', 'teal':'#087C78', 'amber':'#F0B64A'}
FONT_CSS = """
@font-face{font-family:'Bricolage Grotesque';src:url('../assets/BricolageGrotesque-Bold.ttf');font-weight:700}
@font-face{font-family:'Instrument Sans';src:url('../assets/InstrumentSans-Regular.ttf');font-weight:400}
@font-face{font-family:'Instrument Sans';src:url('../assets/InstrumentSans-Bold.ttf');font-weight:700}
text{font-family:'Instrument Sans',sans-serif;fill:#22213B}
"""


def col(value):
    return C.get(value, value)


def attrs(values):
    return ''.join(f' {key.replace("_", "-")}="{escape(str(value), quote=True)}"' for key,value in values.items())


def group(body, transform='', **values):
    return f'<g transform="{transform}"{attrs(values)}>{body}</g>'


def rect(x, y, w, h, fill, r=24, stroke=None, sw=6, **values):
    if stroke:
        values.update(stroke=col(stroke), stroke_width=sw)
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{col(fill)}"{attrs(values)}/>'


def ellipse(cx, cy, rx, ry, fill, **values):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col(fill)}"{attrs(values)}/>'


def circle(cx, cy, r, fill, **values):
    return ellipse(cx, cy, r, r, fill, **values)


def path(d, fill='none', stroke=None, sw=6, **values):
    if stroke:
        values.update(stroke=col(stroke), stroke_width=sw, stroke_linecap='round', stroke_linejoin='round')
    return f'<path d="{d}" fill="{col(fill)}"{attrs(values)}/>'


def ribbon(d, fill='blue', width=64, outline=True, opacity=1):
    result = path(d, stroke='ink', sw=width+10) if outline else ''
    result += path(d, stroke=fill, sw=width)
    result += path(d, stroke='white', sw=9, opacity=.20)
    return group(result, opacity=opacity)


def ticket(x, y, scale=1, angle=0, fill='white', stripes='blue', token_id=''):
    b = rect(10, 12, 154, 112, 'ink', 18, opacity=.18)
    b += rect(0, 0, 154, 112, fill, 18, 'ink', 6)
    b += rect(24, 26, 54, 12, stripes, 5)
    b += rect(24, 53, 104, 10, stripes, 5)
    b += rect(24, 78, 79, 10, stripes, 5)
    return group(b, f'translate({x} {y}) rotate({angle}) scale({scale})', **({'id':token_id} if token_id else {}))


def proof(x, y, scale=1, angle=0, fill='blue'):
    b = path('M24 0H130L160 30V130L130 160H0V24Z', 'ink', opacity=.18, transform='translate(12 14)')
    b += path('M24 0H130L160 30V130L130 160H0V24Z', fill, 'ink', 7)
    b += path('M47 38V122 M79 51V109 M111 38V122', stroke='white', sw=12)
    return group(b, f'translate({x} {y}) rotate({angle} 80 80) scale({scale})', data_piece='proof-token')


def portrait(x, y, scale=1):
    # A local face metaphor, never the object carried to the service.
    b = circle(100, 100, 100, 'ground')
    b += path('M22 204C22 150 62 142 103 142C144 142 178 158 178 204Z', 'teal')
    b += path('M79 128V163Q104 182 125 158V123Z', 'amber', 'ink', 5)
    b += path('M49 64Q50 17 100 20Q155 19 151 85L143 117Q131 147 104 148Q66 147 55 108Z', 'amber', 'ink', 5)
    b += path('M49 89Q27 30 73 9Q110 -7 142 19Q174 42 149 84L131 49Q105 75 49 61Z', 'ink')
    b += path('M70 91L82 92 M121 91L132 90', stroke='ink', sw=7)
    b += path('M98 98L92 113L104 116 M86 130Q104 140 123 127', stroke='ink', sw=4)
    return group(b, f'translate({x} {y}) scale({scale})', data_piece='local-face')


def phone(x, y, scale=1, angle=0, mode='face', contact=False):
    b = rect(20, 26, 440, 780, 'ink', 60, opacity=.16)
    b += rect(0, 0, 440, 780, 'ink', 60)
    b += rect(18, 18, 404, 744, 'white', 44)
    b += rect(151, 32, 138, 20, 'ink', 10)
    b += rect(-7, 148, 14, 84, 'ink', 6)
    b += rect(433, 175, 14, 116, 'ink', 6)
    if mode=='face':
        b += portrait(103, 152, 1.18)
        # Four small held anchors frame the local check, not a transmitted face.
        for d in ['M80 190V126H140','M300 126H360V190','M80 362V426H140','M300 426H360V362']:
            b += path(d, stroke='teal', sw=7)
        b += rect(69, 510, 302, 96, 'teal', 28)
        b += circle(220, 558, 19 if contact else 25, 'white')
        b += rect(125, 680, 190, 9, 'ink', 4, opacity=.18)
    else:
        b += movie(51, 175, 338, 310, 'phone-film')
        b += rect(62, 553, 316, 8, 'ink', 4, opacity=.15)
        b += rect(62, 553, 215, 8, 'blue', 4)
        b += rect(62, 610, 165, 14, 'ink', 4)
        b += rect(62, 646, 255, 10, 'ink', 4, opacity=.2)
    b += rect(153, 732, 134, 9, 'ink', 4)
    return group(b, f'translate({x} {y}) rotate({angle} {220*scale} {390*scale}) scale({scale})', data_piece='phone')


def station(x, y, scale=1, inverse=False, resolved=False):
    # Illustrated service receiver: a metaphor, not a literal server interior.
    b = path('M220 30L252 56V406L220 380Z', 'ink', opacity=.2)
    b += path('M0 110C0 -14 220 -14 220 110V380H0Z', 'white', 'ink', 7)
    b += path('M16 112C16 12 204 12 204 112', stroke='ground', sw=20)
    b += rect(39, 122, 144, 166, 'ink', 20)
    b += rect(53, 137, 117, 136, 'teal' if resolved else 'ground', 14)
    b += path('M78 163V246 M108 176V233 M138 163V246', stroke='white' if resolved else 'ink', sw=10, opacity=1 if resolved else .2)
    b += circle(63, 337, 10, 'teal' if resolved else 'amber')
    b += path('M98 333H172', stroke='ink', sw=6, opacity=.25)
    return group(b, f'translate({x} {y}) scale({scale})', data_piece='service-receiver')


def movie(x, y, w, h, clip_id):
    b = f'<defs><clipPath id="{clip_id}"><rect width="300" height="230" rx="16"/></clipPath></defs>'
    b += rect(0, 0, 300, 230, 'ground', 16)
    land = circle(230, 54, 33, 'amber')
    land += path('M-30 240L99 52L231 240Z', 'blue')
    land += path('M95 240L218 103L328 240Z', 'teal')
    b += group(land, clip_path=f'url(#{clip_id})')
    return (f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 300 230" '
            f'preserveAspectRatio="xMidYMid slice" overflow="hidden">{b}</svg>')


def media_tile(x, y, scale=1, angle=0, tag='tile'):
    b = rect(12, 16, 266, 228, 'ink', 20, opacity=.18)
    b += rect(0, 0, 266, 228, 'white', 20, 'ink', 6)
    b += movie(18, 18, 230, 176, tag)
    b += rect(66, 204, 134, 7, 'ink', 3, opacity=.25)
    return group(b, f'translate({x} {y}) rotate({angle} 133 114) scale({scale})')


def cabinet(x, y, scale=1, tag='cabinet'):
    b = path('M300 12L334 40V454L300 430Z', 'ink', opacity=.22)
    b += rect(0, 0, 300, 430, 'white', 36, 'ink', 7)
    b += rect(20, 20, 260, 272, 'teal', 24)
    b += movie(40, 42, 220, 210, tag)
    b += path('M38 338H262 M38 376H186', stroke='ink', sw=10)
    b += circle(256, 378, 10, 'teal')
    b += path('M36 432V462 M264 432V462', stroke='ink', sw=12)
    return group(b, f'translate({x} {y}) scale({scale})')


def hand_back():
    b = path('M73 1660L104 1460L258 1340L455 1454L397 1660Z', 'teal', 'ink', 7)
    b += path('M148 1470C155 1375 178 1314 179 1202L163 987Q159 931 193 924Q228 917 243 974L277 1148L366 1114L396 1021Q408 980 439 989Q477 997 464 1046L445 1199L509 1161Q548 1135 568 1166Q590 1197 557 1228L503 1281L539 1266Q572 1253 589 1280Q608 1313 574 1338L499 1404Q445 1453 392 1474L355 1544Z', 'amber', 'ink', 7)
    b += path('M166 1483L342 1544', stroke='ink', sw=7)
    return group(b, data_piece='holding-hand')


def thumb(pressed=True):
    d = ('M322 1406C358 1363 368 1312 383 1262L447 1056Q463 1007 500 1020Q539 1033 518 1087L476 1237Q464 1314 463 1342' if pressed else
         'M322 1406C361 1342 376 1284 400 1226L460 1088Q481 1049 515 1069Q550 1091 522 1136L477 1255Q465 1324 463 1342')
    b = path(d, 'amber', 'ink', 7)
    b += path('M472 1052Q490 1035 508 1051L491 1097Q476 1104 463 1091Z', 'white', opacity=.5)
    return group(b, data_piece='touching-thumb')


def authentication(phase=2):
    b = ellipse(539, 1610, 365, 42, 'ink', opacity=.10)
    b += ribbon('M521 732C558 376 963 388 911 685L879 845', 'blue', 66, opacity=1 if phase>0 else .18)
    b += hand_back()
    b += phone(184, 481, 1.04, -12, contact=phase>0)
    b += station(752, 810, .98, resolved=phase==3)
    b += thumb(phase>0)
    if phase==1:
        b += proof(545, 653, .80, -18)
    elif phase==2:
        b += proof(711, 430, .96, 21)
    elif phase==3:
        b += proof(806, 950, .70, 0, 'teal')
    return b


def privacy(phase=2):
    b = ellipse(493, 1605, 350, 42, 'ink', opacity=.15)
    # The same request reaches the remote receiver before the local wipe.
    b += ribbon('M570 868C855 581 1090 1102 838 1236', 'white', 48)
    b += station(753, 1180, .86, resolved=phase>0)
    if phase>0:
        b += ticket(808, 1288, .69, 0, 'amber', 'ink', 'remote-visit')
    # Local browser is a physical illustrated object with a bounded interior.
    local = rect(24, 28, 605, 800, 'ink', 44, opacity=.23)
    local += rect(0, 0, 605, 800, 'white', 44, 'ink', 8)
    local += rect(0, 0, 605, 100, 'ink', 42)
    local += rect(0, 60, 605, 40, 'ink', 0)
    local += circle(47, 53, 9, 'amber')+circle(80, 53, 9, 'white')+circle(113, 53, 9, 'teal')
    local += rect(38, 134, 529, 600, 'ground', 24)
    local += '<defs><clipPath id="history-area"><rect x="38" y="134" width="529" height="600" rx="24"/></clipPath></defs>'
    paper = ''
    if phase<2:
        paper += ticket(106, 212, 1.15, -9, 'amber', 'ink')
        paper += ticket(291, 362, 1.15, 7, 'white', 'blue')
        paper += ticket(106, 525, 1.15, -5, 'white', 'blue')
    elif phase==2:
        paper += ticket(107, 212, 1.15, -9, 'amber', 'ink')
        paper += ticket(297, 360, 1.15, 7, 'white', 'blue')
        paper += path('M38 594C162 500 383 500 567 368V734H38Z', 'white')
        # Pieces are the discarded local record, not the outbound request.
        for x,y,a in [(137,608,-16),(262,590,19),(379,548,-18)]:
            paper += group(rect(0, 0, 64, 34, 'ground', 5, 'ink', 4), f'translate({x} {y}) rotate({a})')
    local += group(paper, clip_path='url(#history-area)')
    # The wipe is a bounded rolled sheet; it never covers the remote receiver.
    if phase>=2:
        yy=540 if phase==2 else 186
        local += path(f'M18 {yy+50}C172 {yy-25} 399 {yy+30} 589 {yy-54}', stroke='ink', sw=38)
        local += path(f'M18 {yy+46}C172 {yy-29} 399 {yy+26} 589 {yy-58}', stroke='white', sw=26)
    b += group(local, 'translate(107 509) rotate(-8 302 400)', data_piece='local-browser')
    # A retained received request is visible above the remote slot in the hero.
    if phase==2:
        b += ticket(789, 1015, 1.02, 14, 'amber', 'ink')
    return b


def delivery(phase=2):
    b = ellipse(430, 1634, 370, 42, 'ink', opacity=.10)
    b += ribbon('M747 602C1060 770 930 1020 491 1071', 'white', 40, opacity=.40)
    b += cabinet(638, 313, .75, 'far-film')
    b += ribbon('M356 1060C-10 1228 325 1517 678 1366', 'blue', 78)
    b += cabinet(120, 784, 1.08, 'near-film')
    b += phone(635, 1160, .65, 10, mode='movie')
    # The source picture stays on the near cabinet while a distinct copy moves.
    if phase==0:
        b += media_tile(242, 1041, .66, -5, 'moving-film-0')
    elif phase==1:
        b += media_tile(140, 1220, .72, -18, 'moving-film-1')
    elif phase==2:
        b += media_tile(327, 1360, .82, 17, 'moving-film-2')
    return b


def svg(name, illustration, background='ground', viewbox='0 0 1080 1920', width=1080, height=1920):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="{viewbox}" role="img" aria-labelledby="{name}-title">'
            f'<title id="{name}-title">{escape(name.replace("-", " "))} — original illustrative design study</title><style>{FONT_CSS}</style>'
            +rect(-200, -200, 1480, 2320, background, 0)
            +group(illustration, data_art='illustration')+'</svg>')


studies = [
    ('passkeys', svg('passkeys', authentication()), 'Identity / proof travels', 'Local face, separate proof. A touch drives the exchange.'),
    ('privacy', svg('privacy', privacy(), 'blue'), 'Privacy / clear locally', 'The local record disappears. A remote visit remains.'),
    ('delivery', svg('delivery', delivery()), 'Delivery / a nearby copy', 'One image stays. Another takes the shorter route.'),
]
for name, markup, *_ in studies:
    (STUDIES/f'{name}.svg').write_text(markup, encoding='utf-8')

poses=[]
for n,(title,note) in enumerate([
    ('Anticipate','The hand prepares. The face stays local.'),
    ('Act','Touch creates the next state.'),
    ('Travel','The proof follows a continuous arc.'),
    ('Land','The receiver changes after arrival.'),
]):
    markup=svg(f'pose-{n+1}', authentication(n), viewbox='80 350 940 1160', width=470, height=580)
    (STUDIES/f'pose-{n+1}.svg').write_text(markup, encoding='utf-8')
    # Prefix local IDs in a repeated inline sample, even though currently none collide.
    poses.append((markup,title,note))

inline=lambda markup: markup.replace('../assets/','assets/')
study_html=''.join(f'<figure><div class="study" id="study-{name}">{inline(markup)}</div><figcaption><strong>{escape(title)}</strong><p>{escape(note)}</p></figcaption></figure>' for name,markup,title,note in studies)
pose_html=''.join(f'<figure><div class="pose" id="pose-{i+1}">{inline(markup)}</div><figcaption><strong>{title}</strong><p>{note}</p></figcaption></figure>' for i,(markup,title,note) in enumerate(poses))
swatches=''.join(f'<div><i style="background:{value}"></i><span>{label}</span></div>' for label,value in [('Ground',C['ground']),('Surface',C['white']),('Contour',C['ink']),('Transfer',C['blue']),('State',C['teal']),('Touch',C['amber'])])
html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Behind the Screen — illustrated motion direction v2</title>
<style>{FONT_CSS.replace('../assets/','assets/')}
:root{{--ground:{C['ground']};--surface:{C['white']};--ink:{C['ink']};--blue:{C['blue']};--teal:{C['teal']};--amber:{C['amber']}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--ground);color:var(--ink);font:400 24px/1.35 'Instrument Sans',sans-serif}}
#board{{width:1800px;margin:auto;padding:60px 72px 38px}}
.status{{display:flex;justify-content:space-between;font-size:21px;margin-bottom:28px}}
header{{display:grid;grid-template-columns:1.2fr 1fr;gap:92px;align-items:end;margin-bottom:40px}}
h1{{font:700 94px/.94 'Bricolage Grotesque',sans-serif;letter-spacing:-4px;margin:0}}.promise{{font:700 38px/1.1 'Bricolage Grotesque',sans-serif;letter-spacing:-1px;margin:0 0 16px}}header p:last-child{{font-size:24px;margin:0;max-width:610px}}
.studies{{display:grid;grid-template-columns:repeat(3,528px);gap:36px}}figure{{margin:0}}.study{{width:528px;height:938.666667px;border-radius:12px;overflow:hidden;outline:2px solid #22213b20}}.study svg{{display:block;width:100%;height:100%}}
figcaption{{padding-top:16px}}figcaption strong{{font-size:24px}}figcaption p{{font-size:21px;margin:8px 0 0;max-width:515px}}
.motion-section{{margin-top:38px;padding-top:28px;border-top:2px solid #22213b30}}.section-heading{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:16px}}h2{{font:700 33px/1.2 'Bricolage Grotesque',sans-serif;letter-spacing:-1px;margin:0}}.section-heading p{{margin:0;font-size:21px}}
.poses{{display:grid;grid-template-columns:repeat(4,387px);gap:36px}}.pose{{width:387px;height:477.574px;border-radius:10px;overflow:hidden;background:var(--ground);outline:2px solid #22213b20}}.pose svg{{width:100%;height:100%;display:block}}.poses figcaption p{{font-size:20px;max-width:365px}}
.foundation{{display:grid;grid-template-columns:790px 1fr;gap:70px;margin-top:38px;padding-top:28px;border-top:2px solid #22213b30}}
.swatches{{display:flex;gap:15px;margin-top:20px}}.swatches>div{{width:114px}}.swatches i{{display:block;width:114px;height:48px;border-radius:8px;border:1px solid #22213b25}}.swatches span{{font-size:19px;display:block;margin-top:8px}}
.type{{font:700 38px/1.1 'Bricolage Grotesque',sans-serif;letter-spacing:-1px;margin:18px 0 10px}}.foundation p:last-child{{font-size:21px;margin:0}}
.footer{{display:flex;justify-content:space-between;font-size:19px;margin-top:28px;padding-top:24px;border-top:2px solid #22213b30}}
</style></head><body><main id="board">
<div class="status"><span>Behind the Screen / draft v2</span><span>Illustration-led motion direction</span></div>
<header><h1>Make the process<br>the performance.</h1><div><p class="promise">Big illustrations.<br>Small amounts of text.</p><p>The hand, the object and the transfer carry the explanation. These are independent studies, with zero text inside the frames.</p></div></header>
<section class="studies" aria-label="Three independent illustration studies">{study_html}</section>
<section class="motion-section"><div class="section-heading"><h2>Design the action before the animation</h2><p>Four planned poses / static, not a playback test</p></div><div class="poses">{pose_html}</div></section>
<section class="foundation"><div><h2>One visual language, expressive staging</h2><div class="swatches">{swatches}</div></div><div><h2>Type supports the moment</h2><p class="type">Only when it helps.</p><p>Bricolage Grotesque Bold + Instrument Sans.<br>Usually 0–3 emphasis words. Narration carries the detail.</p></div></section>
<footer class="footer"><span>Original vector illustrations / editable sources / 9:16</span><span>Illustrative metaphors / motion and audio remain to be tested</span></footer>
</main></body></html>'''
(ROOT/'style-board.html').write_text(html, encoding='utf-8')
print(json.dumps({'revision':2,'heroStudies':3,'motionPoses':4,'visibleTextInsideStudies':0}))
