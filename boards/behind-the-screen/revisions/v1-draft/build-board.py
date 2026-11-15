"""Build the original static direction sheet and its independent SVG studies.

No server, external asset fetch, audio generation or video initialization.
Run this script from any directory, then `node export-board.cjs`.
"""
from pathlib import Path
from html import escape
import hashlib
import json

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
STUDIES = ROOT / 'studies'
ASSETS.mkdir(exist_ok=True)
STUDIES.mkdir(exist_ok=True)

FILES = [
    'BricolageGrotesque-Bold.ttf', 'BricolageGrotesque-OFL.txt',
    'InstrumentSans-Regular.ttf', 'InstrumentSans-Bold.ttf', 'InstrumentSans-OFL.txt',
]
manifest = []
for name in FILES:
    target = ASSETS / name
    manifest.append({'file': name, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
(ASSETS / 'asset-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')

C = {'ground': '#F0EFF8', 'white': '#FFFFFF', 'ink': '#22213B',
     'blue': '#4054E8', 'teal': '#087C78', 'amber': '#F0B64A'}

FONT_CSS = """
@font-face{font-family:'Bricolage Grotesque';src:url('../assets/BricolageGrotesque-Bold.ttf');font-weight:700;font-style:normal}
@font-face{font-family:'Instrument Sans';src:url('../assets/InstrumentSans-Regular.ttf');font-weight:400;font-style:normal}
@font-face{font-family:'Instrument Sans';src:url('../assets/InstrumentSans-Bold.ttf');font-weight:700;font-style:normal}
text{font-family:'Instrument Sans',sans-serif;fill:#22213B}
.headline{font-family:'Bricolage Grotesque',sans-serif;font-weight:700;letter-spacing:-4px}
.caption{font-weight:700}
"""


def rect(x, y, w, h, fill='white', radius=24, stroke=None, sw=4, opacity=None, **attrs):
    a = f'x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{C.get(fill, fill)}"'
    if stroke:
        a += f' stroke="{C.get(stroke, stroke)}" stroke-width="{sw}"'
    if opacity is not None:
        a += f' opacity="{opacity}"'
    for k, v in attrs.items():
        a += f' {k.replace("_", "-")}="{v}"'
    return f'<rect {a}/>'


def text(x, y, content, size=38, weight=400, fill='ink', css='', anchor=None, **attrs):
    a = f'x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" style="fill:{C.get(fill, fill)}"'
    if css:
        a += f' class="{css}"'
    if anchor:
        a += f' text-anchor="{anchor}"'
    for k, v in attrs.items():
        a += f' {k.replace("_", "-")}="{v}"'
    return f'<text {a}>{escape(content)}</text>'


def lines(x, y, content, size=96, leading=102, **kw):
    return ''.join(text(x, y + i * leading, row, size=size, **kw) for i, row in enumerate(content))


def path(d, stroke='blue', sw=12, opacity=None, arrow=None, dash=None, fill='none'):
    a = f'd="{d}" fill="{C.get(fill, fill)}" stroke="{C.get(stroke, stroke)}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'
    if opacity is not None:
        a += f' opacity="{opacity}"'
    if arrow:
        a += f' marker-end="url(#{arrow})"'
    if dash:
        a += f' stroke-dasharray="{dash}"'
    return f'<path {a}/>'


def arrowhead(name, fill):
    return f'<marker id="{name}" viewBox="0 0 24 24" refX="21" refY="12" markerWidth="24" markerHeight="24" markerUnits="userSpaceOnUse" orient="auto"><path d="M2 2 L22 12 L2 22" fill="none" stroke="{C[fill]}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></marker>'


def base(name, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920" role="img" aria-labelledby="{name}-title">'
            f'<title id="{name}-title">{escape(title)}</title><style>{FONT_CSS}</style>'
            f'<defs>{arrowhead(name+"-blue", "blue")}{arrowhead(name+"-teal", "teal")}</defs>'
            + rect(0, 0, 1080, 1920, 'ground', 0) + body + '</svg>')


def caption(rows):
    return lines(540, 1628, rows, size=46, leading=58, css='caption', anchor='middle')


def movie_tile(x, y, w, h, suffix):
    # Original miniature landscape frame, used identically at each copy.
    return (f'<g transform="translate({x} {y}) scale({w/240} {h/140})">'
            + rect(0, 0, 240, 140, 'ground', 12)
            + f'<clipPath id="{suffix}"><rect width="240" height="140" rx="12"/></clipPath>'
            + f'<g clip-path="url(#{suffix})"><circle cx="176" cy="42" r="24" fill="{C["amber"]}"/>'
            + f'<path d="M-20 140L75 38L180 140Z" fill="{C["blue"]}"/>'
            + f'<path d="M65 150L174 68L270 150Z" fill="{C["teal"]}"/></g></g>')


def passkey():
    s = text(80, 180, 'Passkey sign-in', size=38)
    s += lines(80, 326, ['Your face stays.', 'Proof travels.'], css='headline', size=100, leading=110)
    # Source and destination each have a recognizable opaque surface.
    s += rect(104, 690, 412, 630, 'ink', 48, opacity=.12)
    s += rect(80, 666, 412, 630, 'ink', 48)
    s += rect(96, 682, 380, 598, 'white', 34)
    s += rect(225, 702, 120, 14, 'ink', 7)
    s += text(286, 791, 'example.com', size=34, anchor='middle')
    s += text(286, 883, 'Sign in', size=66, weight=700, anchor='middle')
    s += text(286, 946, 'Confirm on device', size=34, anchor='middle')
    s += rect(124, 978, 324, 266, 'ground', 20)
    s += rect(140, 1002, 292, 102, 'teal', 18)
    s += text(286, 1068, 'Approve', size=42, weight=700, fill='white', anchor='middle')
    s += text(286, 1160, 'PIN or biometrics', size=34, anchor='middle')
    s += text(286, 1218, 'Local check', size=34, weight=700, anchor='middle')
    s += text(286, 1380, 'Your device', size=40, weight=700, anchor='middle')
    s += text(286, 1434, 'Biometric check stays here', size=34, anchor='middle')
    s += rect(690, 1030, 300, 330, 'ink', 28, opacity=.12)
    s += rect(670, 1010, 300, 330, 'white', 28, 'ink', 4, stroke_opacity=.2)
    s += text(820, 1100, 'The website', size=40, weight=700, anchor='middle')
    s += path('M720 1152H920', 'ink', 5, opacity=.18)
    s += rect(710, 1195, 220, 88, 'teal', 16)
    s += text(820, 1252, 'Verified', size=38, weight=700, fill='white', anchor='middle')
    # Distinct routes prevent the local check from appearing to be transmitted.
    s += path('M820 1010V760Q820 724 784 724H528Q492 724 492 760V830', 'blue', 12, arrow='passkey-blue')
    s += rect(585, 640, 286, 68, 'ground', 0)
    s += text(728, 688, 'Challenge', size=38, weight=700, fill='blue', anchor='middle')
    s += path('M492 1060H548Q584 1060 584 1096V1234Q584 1270 620 1270H670', 'blue', 12, arrow='passkey-blue')
    s += text(615, 1478, 'Signed proof', size=38, weight=700, fill='blue')
    s += path('M650 1270L610 1310V1425', 'blue', 4)
    s += f'<circle cx="650" cy="1270" r="6" fill="{C["blue"]}"/>'
    s += caption(['Biometric data stays', 'on your device.'])
    return base('passkey', 'Passkey study: local biometric check and a proof sent to the website', s)


def privacy():
    s = text(80, 180, 'Chrome Incognito', size=38)
    s += lines(80, 326, ['Private from', 'whom?'], css='headline', size=110, leading=116)
    # Device boundary has a visible edge with a crossing request.
    s += rect(80, 620, 570, 820, 'ground', 32, 'ink', 4, stroke_opacity=.38)
    s += text(120, 700, 'On this device', size=40, weight=700)
    s += rect(120, 762, 490, 302, 'white', 24, 'ink', 4, stroke_opacity=.2)
    s += rect(120, 762, 490, 64, 'ink', 24)
    s += rect(120, 798, 490, 28, 'ink', 0)
    s += text(365, 807, 'Private session', size=34, fill='white', anchor='middle')
    s += text(162, 906, 'example.com', size=38, weight=700)
    s += rect(162, 942, 330, 18, 'blue', 5)
    s += rect(162, 984, 245, 18, 'ink', 5, opacity=.18)
    s += text(120, 1150, 'Local history', size=38, weight=700)
    s += text(120, 1205, 'after the session closes', size=34)
    s += text(140, 1310, 'example.com', size=38, opacity=.5)
    s += path('M124 1295H536', 'ink', 5)
    s += text(365, 1395, 'Not retained', size=36, weight=700, anchor='middle')
    s += path('M610 907H732', 'blue', 12, arrow='privacy-blue')
    s += text(694, 853, 'Visit', size=36, weight=700, fill='blue', anchor='middle')
    s += rect(752, 884, 246, 350, 'ink', 24, opacity=.12)
    s += rect(732, 864, 246, 350, 'white', 24, 'blue', 4)
    s += text(855, 953, 'Website', size=38, weight=700, anchor='middle')
    s += path('M774 1000H936', 'ink', 4, opacity=.18)
    s += rect(770, 1043, 170, 30, 'blue', 7)
    s += rect(770, 1091, 170, 30, 'blue', 7, opacity=.25)
    s += lines(855, 1298, ['Still receives', 'your visit'], size=34, leading=44, anchor='middle', weight=700, fill='blue')
    s += text(80, 1510, 'History record only; downloads and bookmarks differ.', size=34)
    s += caption(['Local history clears.', 'Sites still receive visits.'])
    return base('privacy', 'Chrome Incognito study: a local history boundary does not hide visits from the website', s)


def delivery():
    s = text(80, 180, 'Video delivery', size=38)
    s += lines(80, 326, ['The internet', 'has shortcuts.'], css='headline', size=104, leading=112)
    # Spatial schematic: the origin and edge retain the same recognizable media.
    s += text(740, 618, 'Origin', size=40, weight=700, anchor='middle')
    s += rect(602, 668, 300, 228, 'ink', 24, opacity=.12)
    s += rect(582, 648, 300, 228, 'white', 24, 'ink', 4, stroke_opacity=.2)
    s += movie_tile(622, 686, 220, 128, 'origin-landscape')
    s += path('M732 876V953 M732 1020V1030', 'ink', 6, opacity=.25, dash='12 18')
    s += text(450, 943, 'Cached earlier', size=34, anchor='middle')
    s += path('M585 932H700', 'ink', 4, opacity=.4)
    s += text(732, 1007, 'Nearby copy', size=40, weight=700, anchor='middle')
    s += rect(602, 1050, 300, 228, 'ink', 24, opacity=.12)
    s += rect(582, 1030, 300, 228, 'white', 24, 'teal', 4)
    s += movie_tile(622, 1068, 220, 128, 'edge-landscape')
    s += path('M582 1144H455Q409 1144 409 1190V1346Q409 1382 373 1382H324', 'blue', 12, arrow='delivery-blue')
    s += text(80, 1050, 'A shorter trip', size=38, weight=700, fill='blue')
    s += path('M215 1090V1126H365', 'blue', 4)
    s += rect(100, 1204, 244, 302, 'ink', 36, opacity=.12)
    s += rect(80, 1184, 244, 302, 'ink', 36)
    s += rect(96, 1200, 212, 270, 'white', 24)
    s += rect(165, 1214, 74, 10, 'ink', 5)
    s += movie_tile(112, 1270, 180, 105, 'viewer-landscape')
    s += path('M118 1412H286', 'ink', 5, opacity=.18)
    s += path('M118 1412H220', 'blue', 5)
    s += text(732, 1370, 'Copy available', size=34, weight=700, fill='teal', anchor='middle')
    s += caption(['A nearby copy can', 'shorten the trip.'])
    return base('delivery', 'CDN cache-hit study: content can travel from a nearby cached copy to a viewer', s)


samples = [
    ('passkeys', passkey(), 'Local approval. Remote proof.', 'A device and a service exchange information while the biometric check stays local.'),
    ('privacy', privacy(), 'A boundary, made visible.', 'A comparison of local history and a website receiving a visit. Chrome-specific scope.'),
    ('delivery', delivery(), 'Distance becomes the explanation.', 'A schematic cache hit preserves the origin, a nearby copy and the viewer.'),
]
for name, svg, _, _ in samples:
    (STUDIES / f'{name}.svg').write_text(svg, encoding='utf-8')


def mini_pose(kind):
    # Four static poses of the same abstract interface; no animation is asserted.
    s = '<svg viewBox="0 0 310 164" aria-hidden="true">'
    if kind == 'Open':
        for x, y, fill in [(72, 76, 'ink'), (54, 48, 'white'), (36, 20, 'white')]:
            s += rect(x, y, 180, 72, fill, 12, 'ink', 2, fill_opacity=.12 if fill == 'ink' else 1)
        s += rect(62, 42, 112, 9, 'blue', 3)
    elif kind == 'Follow':
        s += rect(22, 44, 86, 76, 'white', 12, 'ink', 2, stroke_opacity=.25)
        s += rect(204, 44, 86, 76, 'white', 12, 'ink', 2, stroke_opacity=.25)
        s += path('M108 82H204', 'blue', 5)
        s += rect(148, 70, 26, 24, 'blue', 5)
        s += path('M191 72L203 82L191 92', 'blue', 4)
    elif kind == 'Resolve':
        s += rect(64, 30, 184, 104, 'white', 12, 'teal', 3)
        s += rect(92, 58, 128, 44, 'teal', 8)
        s += text(156, 87, 'Verified', size=24, weight=700, fill='white', anchor='middle')
    else:
        s += rect(72, 38, 180, 96, 'ink', 12, opacity=.12)
        s += rect(60, 26, 180, 96, 'white', 12, 'ink', 2, stroke_opacity=.25)
        s += rect(86, 48, 126, 13, 'ink', 3)
        s += rect(86, 76, 90, 20, 'teal', 4)
    return s + '</svg>'


font_css = FONT_CSS.replace('../assets/', 'assets/')
sample_html = ''.join(
    f'<figure><div class="study" id="study-{name}">{svg.replace("../assets/", "assets/")}</div>'
    f'<figcaption><strong>{escape(title)}</strong><p>{escape(desc)}</p></figcaption></figure>'
    for name, svg, title, desc in samples
)
swatches = ''.join(f'<div class="swatch"><div style="background:{value}"></div><strong>{role}</strong><span>{value}</span></div>'
                   for role, value in [('Ground', C['ground']), ('Surface', C['white']), ('Ink', C['ink']),
                                       ('Exchange', C['blue']), ('Resolved', C['teal']), ('Input', C['amber'])])
motion = ''.join(f'<div class="pose">{mini_pose(name)}<strong>{name}</strong><span>{desc}</span></div>'
                 for name, desc in [('Open', 'Expose the relevant layer.'), ('Follow', 'Trace one exchange.'),
                                    ('Resolve', 'Show the changed state.'), ('Return', 'Answer the opening event.')])

html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Behind the Screen — creative board v1</title><style>
{font_css}
:root{{--canvas:{C['ground']};--surface:{C['white']};--ink:{C['ink']};--transit:{C['blue']};--resolved:{C['teal']};--input:{C['amber']}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--canvas);color:var(--ink);font-family:'Instrument Sans',sans-serif;font-size:24px}}
#board{{width:1800px;padding:64px 72px 42px;margin:auto;background:var(--canvas)}}
.status{{display:flex;justify-content:space-between;font-size:22px;margin-bottom:38px}}
.masthead{{display:grid;grid-template-columns:1.15fr 1fr;gap:88px;align-items:end;margin-bottom:54px}}
h1{{font:700 126px/.92 'Bricolage Grotesque',sans-serif;letter-spacing:-7px;margin:0}}
.promise{{font-size:38px;line-height:1.22;max-width:650px;margin:0 0 22px;font-weight:700}}
.intro{{font-size:25px;line-height:1.42;max-width:620px;margin:0}}
.study-heading{{display:flex;justify-content:space-between;align-items:baseline;padding-top:26px;border-top:2px solid #22213b30;margin-bottom:22px}}
h2{{font:700 32px/1.2 'Bricolage Grotesque',sans-serif;letter-spacing:-1px;margin:0}}
.study-heading p{{font-size:21px;margin:0}}
.studies{{display:grid;grid-template-columns:repeat(3,528px);gap:36px}}
figure{{margin:0}}.study{{width:528px;height:938.666667px;border-radius:8px;overflow:hidden;outline:2px solid #22213b26}}
.study svg{{display:block;width:100%;height:100%}}
figcaption{{padding:22px 0 0;font-size:22px;line-height:1.34}}figcaption strong{{font-size:25px}}figcaption p{{margin:10px 0 0;max-width:510px}}
.foundations{{margin-top:48px;border-top:2px solid #22213b30;padding-top:28px;display:grid;grid-template-columns:760px 1fr;gap:64px}}
.swatches{{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-top:24px}}
.swatch>div{{height:64px;border:1px solid #22213b26;border-radius:8px}}
.swatch strong,.swatch span{{display:block;font-size:20px;margin-top:9px}}.swatch span{{font-size:18px}}
.type-sample{{font:700 42px/1.05 'Bricolage Grotesque',sans-serif;letter-spacing:-1.6px;margin:20px 0 12px}}
.type-detail{{font-size:21px;line-height:1.4;margin:0}}
.motion{{margin-top:38px;padding-top:28px;border-top:2px solid #22213b30}}
.motion-heading{{display:flex;justify-content:space-between;align-items:baseline}}
.motion-heading p{{margin:0;font-size:21px}}
.poses{{display:grid;grid-template-columns:repeat(4,1fr);gap:28px;margin-top:4px}}
.pose svg{{width:100%;height:162px;display:block}}.pose strong{{font-size:25px;display:block}}.pose span{{font-size:21px;display:block;margin-top:6px}}
.editorial{{margin-top:36px;padding:28px 0 0;border-top:2px solid #22213b30;display:grid;grid-template-columns:1fr 1fr;gap:64px}}
.editorial p{{font-size:23px;line-height:1.4;margin:12px 0 0;max-width:780px}}
.foot{{font-size:18px;line-height:1.4;margin-top:32px;max-width:1500px}}
@media print{{@page{{size:1800px 2400px;margin:0}}body{{print-color-adjust:exact}}}}
</style></head><body><main id="board">
<div class="status"><span>Creative direction / draft v1</span><span>English explainers / vertical 9:16</span></div>
<header class="masthead"><h1>Behind<br>the Screen</h1><div><p class="promise">Understand what happens<br>behind your everyday clicks.</p><p class="intro">A familiar screen opens into the process underneath. Follow the exchange, see the boundary, return with an answer.</p></div></header>
<div class="study-heading"><h2>Three ways to reveal the invisible</h2><p>Independent composition studies / illustrative copy</p></div>
<section class="studies" aria-label="Independent vertical visual studies">{sample_html}</section>
<section class="foundations"><div><h2>Color carries a role</h2><div class="swatches">{swatches}</div></div><div><h2>Human questions. Precise explanations.</h2><p class="type-sample">Why did that happen?</p><p class="type-detail">Bricolage Grotesque Bold / questions<br>Instrument Sans Regular + Bold / UI, labels, captions</p></div></section>
<section class="motion"><div class="motion-heading"><h2>Meaning leads the movement</h2><p>Conceptual poses / no animation or sound generated</p></div><div class="poses">{motion}</div></section>
<section class="editorial"><div><h2>One familiar event. One causal answer.</h2><p>Identity, copies, connections and visibility. Explain the process at the moment it becomes useful, then return to the question the viewer arrived with.</p></div><div><h2>Clear enough to explain to someone else.</h2><p>Conversational English. Specific observers and destinations. A visible cause, a relevant exception, and an ending that changes what the viewer expects.</p></div></section>
<footer class="foot">Proposed direction, awaiting feedback. Original interface illustrations, not product screenshots. Study scopes: local biometric verification; Chrome Incognito history after the session closes; an available CDN cache hit. Source boundaries and exceptions are recorded in assets/SOURCES.md.</footer>
</main></body></html>'''
(ROOT / 'style-board.html').write_text(html, encoding='utf-8')
print(json.dumps({'source': str(ROOT / 'style-board.html'), 'studies': [name for name, *_ in samples], 'fontAssets': len(manifest)}))
