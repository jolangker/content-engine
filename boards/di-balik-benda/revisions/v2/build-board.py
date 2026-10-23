"""Rebuild the editable static board and original schematic SVG studies."""
from pathlib import Path
from urllib.request import urlopen
import hashlib
import math

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
FONTS = {
    "manrope.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/Manrope%5Bwght%5D.ttf",
    "Manrope-OFL.txt": "https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/OFL.txt",
    "ibm-plex-mono.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/IBMPlexMono-Regular.ttf",
    "IBM-Plex-Mono-OFL.txt": "https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/OFL.txt",
}
for name, url in FONTS.items():
    destination = ASSETS / name
    if not destination.exists():
        with urlopen(url, timeout=40) as response:
            destination.write_bytes(response.read())
sources = ["# Asset provenance", "", "Retrieved 2026-10-23 from the Google Fonts source repository. Fonts are bundled locally with their original licenses. No generated images or external mechanical reference imagery were used.", ""]
for name, url in FONTS.items():
    sources += [f"- `{name}`: {url}", f"  - SHA-256: `{hashlib.sha256((ASSETS / name).read_bytes()).hexdigest()}`"]
sources += ["", "All illustrations are original code-authored schematic studies created for this board. They are not engineering evidence. Geometry needs verification against an identified real implementation before any factual production.", ""]
(ASSETS / "SOURCES.md").write_text("\n".join(sources), encoding="utf-8")


def svg(body, view="0 0 508 510", label="Conceptual mechanical illustration"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" role="img" aria-label="{label}">
    <defs>
      <linearGradient id="metal" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#758B9B"/><stop offset=".28" stop-color="#DCE3E6"/><stop offset=".53" stop-color="#B3C0C8"/><stop offset=".77" stop-color="#E7ECEC"/><stop offset="1" stop-color="#879BA9"/></linearGradient>
      <linearGradient id="polymer" x1="0" y1="0" x2="1" y2=".4"><stop stop-color="#42647A"/><stop offset=".48" stop-color="#29485D"/><stop offset="1" stop-color="#172B3B"/></linearGradient>
      <linearGradient id="blue" x1="0" y1="0" x2="1" y2=".4"><stop stop-color="#709CF3"/><stop offset=".48" stop-color="#2459C4"/><stop offset="1" stop-color="#173F8F"/></linearGradient>
      <linearGradient id="glass" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#E3EDF0" stop-opacity=".9"/><stop offset=".35" stop-color="#F8F9F5" stop-opacity=".3"/><stop offset="1" stop-color="#B8CED4" stop-opacity=".8"/></linearGradient>
      <pattern id="section" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><path d="M0 0V9" stroke="#9BAAB3" stroke-width="2"/></pattern>
    </defs>
    {body}</svg>'''


def label(x, y, text, color="#536775", size=18, anchor="start"):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="IBM Plex Mono,monospace" font-size="{size}" text-anchor="{anchor}">{text}</text>'


def leader(points, color="#536775"):
    x, y = points[-1]
    return f'<polyline points="{" ".join(f"{a},{b}" for a,b in points)}" fill="none" stroke="{color}" stroke-width="1.5"/><circle cx="{x}" cy="{y}" r="3.5" fill="{color}"/>'


def spring(cx, y, width, height, turns):
    # Schematic helix, with a continuous visible wire.
    points = []
    for n in range(turns * 40 + 1):
        t = n / 40 * 2 * math.pi
        points.append((cx + width / 2 * math.cos(t), y + height * n / (turns * 40) + 5 * math.sin(t)))
    coords = " ".join(f"{x:.2f},{yy:.2f}" for x, yy in points)
    return f'<polyline points="{coords}" fill="none" stroke="#526D80" stroke-width="6" stroke-linecap="round"/><polyline points="{coords}" fill="none" stroke="#DCE5E8" stroke-width="2" stroke-linecap="round"/>'


def gear(cx, cy, radius, teeth, fill, rotation=0):
    pts = []
    for i in range(teeth):
        for offset, r in [(0, radius*.82), (.16, radius), (.55, radius), (.72, radius*.82)]:
            a = ((i+offset)/teeth*2*math.pi) + rotation
            pts.append(f"{cx+math.cos(a)*r:.2f},{cy+math.sin(a)*r:.2f}")
    poly = " ".join(pts)
    spokes = ""
    for i in range(4):
        a = rotation + i*math.pi/2
        x, y = cx+math.cos(a)*radius*.5, cy+math.sin(a)*radius*.5
        spokes += f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="{radius*.17:.2f}" ry="{radius*.11:.2f}" fill="#F8F9F5" transform="rotate({a*180/math.pi:.1f} {x:.2f} {y:.2f})"/>'
    return f'<polygon points="{poly}" fill="#172B3B" opacity=".16" transform="translate(0 8)"/><polygon points="{poly}" fill="{fill}" stroke="#172B3B" stroke-width="2" stroke-linejoin="round"/>{spokes}<circle cx="{cx}" cy="{cy}" r="{radius*.18}" fill="url(#metal)" stroke="#536775" stroke-width="2"/><circle cx="{cx}" cy="{cy}" r="{radius*.055}" fill="#172B3B"/>'


pump = '''
<ellipse cx="495" cy="526" rx="128" ry="15" fill="#172B3B" opacity=".07"/>
<path d="M495 36V512" stroke="#A6B4BE" stroke-dasharray="4 7"/>
<!-- Original schematic pump actuator, separated to reveal component identity. -->
<path d="M438 45Q495 18 552 45V91Q495 118 438 91Z" fill="url(#polymer)" stroke="#172B3B" stroke-width="2"/>
<ellipse cx="495" cy="45" rx="57" ry="17" fill="#527084" stroke="#172B3B" stroke-width="2"/>
<path d="M448 50L378 65V95L448 84Z" fill="#365468" stroke="#172B3B" stroke-width="2"/>
<path d="M378 65L393 69V91L378 95Z" fill="#172B3B"/>
<ellipse cx="382" cy="80" rx="4" ry="7" fill="#C94422"/>
<path d="M485 108V177Q495 182 505 177V108" fill="url(#metal)" stroke="#758B9B" stroke-width="1.5"/>
<ellipse cx="495" cy="109" rx="10" ry="4" fill="#DCE3E6"/>
<path d="M465 199Q495 186 525 199V221Q495 235 465 221Z" fill="url(#blue)" stroke="#2459C4" stroke-width="2"/>
<ellipse cx="495" cy="199" rx="30" ry="10" fill="#739BEA"/>
<ellipse cx="495" cy="199" rx="12" ry="4.5" fill="#173F8F"/>
'''
pump += spring(495, 256, 49, 86, 7)
pump += '''
<path d="M445 378Q495 357 545 378V427Q495 450 445 427Z" fill="url(#glass)" stroke="#8DA5B1" stroke-width="2"/>
<ellipse cx="495" cy="378" rx="50" ry="17" fill="#DAE6E9" stroke="#8DA5B1" stroke-width="2"/>
<ellipse cx="495" cy="378" rx="34" ry="11" fill="#F8F9F5" stroke="#8DA5B1" stroke-width="2"/>
<path d="M470 400Q495 409 520 400V423Q495 435 470 423Z" fill="#2459C4" opacity=".22"/>
<path d="M489 451V504Q495 510 501 504V451" fill="url(#glass)" stroke="#8DA5B1" stroke-width="2"/>
<ellipse cx="495" cy="451" rx="6" ry="3" fill="#DCE7E9" stroke="#8DA5B1"/>
<path d="M594 44V99M588 91L594 99L600 91" fill="none" stroke="#C94422" stroke-width="3" stroke-linecap="round"/>
'''
pump += label(622,76,"TEKAN / INPUT",color="#C94422",size=16)
# The final anchor of each leader touches the actual illustrated component.
pump += leader([(207,144),(354,144),(438,74)]) + label(207,128,"Kepala tekan",size=20)
pump += leader([(660,212),(583,212),(522,210)],"#2459C4") + label(660,196,"Piston",color="#2459C4",size=20)
pump += leader([(215,302),(399,302),(470,295)]) + label(215,286,"Pegas",size=20)
pump += leader([(659,401),(593,401),(540,411)]) + label(659,384,"Rumah pompa",size=20)
pump += leader([(220,475),(408,475),(489,482)]) + label(220,458,"Saluran",size=20)
pump_svg = svg(pump,"0 0 960 550","Studi konseptual pompa terurai: kepala tekan, piston, pegas, rumah pompa, dan saluran")

valve = '''
<path d="M73 400H435" stroke="#CDD4D4" stroke-width="1.5"/>
<ellipse cx="256" cy="392" rx="167" ry="17" fill="#172B3B" opacity=".07"/>
<!-- Housing cross section; generic geometry, not a real valve design. -->
<path d="M72 231H181V195H331V231H437V345H331V367H181V345H72Z" fill="url(#metal)" stroke="#536775" stroke-width="2"/>
<path d="M73 232H181V196H331V232H437V345H331V366H181V345H73Z" fill="url(#section)" opacity=".6"/>
<path d="M72 259H208V225H304V259H437V316H287V281H234V316H72Z" fill="#F8F9F5" stroke="#536775" stroke-width="2"/>
<path d="M72 264H193V305H72Z" fill="#C94422" opacity=".12"/>
<path d="M312 265H437V311H312Z" fill="#167580" opacity=".12"/>
<path d="M242 113H270V241H242Z" fill="url(#metal)" stroke="#536775" stroke-width="2"/>
<path d="M224 230H288L300 252H212Z" fill="url(#blue)" stroke="#173F8F" stroke-width="2"/>
<rect x="200" y="91" width="112" height="28" rx="6" fill="#C94422"/>
<path d="M256 137V182M246 173L256 183L266 173" fill="none" stroke="#C94422" stroke-width="3" stroke-linecap="round"/>
<path d="M92 286H153M143 277L154 286L143 295" fill="none" stroke="#C94422" stroke-width="4" stroke-linecap="round"/>
<path d="M353 286H416M406 277L417 286L406 295" fill="none" stroke="#167580" stroke-width="4" stroke-linecap="round"/>
'''
valve += leader([(73,180),(151,180),(211,244)],"#2459C4") + label(73,161,"Bagian aktif",color="#2459C4",size=18)
valve += leader([(342,427),(342,396),(327,348)]) + label(342,452,"Bidang potong",size=16,anchor="middle")
valve_svg = svg(valve,label="Studi ilustratif potongan katup dengan bagian aktif dan arah input serta output")

zipper = '''
<path d="M120 43L252 440M386 43L252 440" fill="none" stroke="#D5DED9" stroke-width="56"/>
<path d="M105 45L236 441M401 45L268 441" fill="none" stroke="#B6C7BE" stroke-width="3" stroke-dasharray="3 6"/>
'''
# Two separated rows meet a schematic slider, then continue as an interlocked study.
for j in range(7):
    y = 57 + j*27
    xl = 133 + j*8.8
    xr = 372 - j*8.8
    zipper += f'<g transform="translate({xl} {y}) rotate(-18)"><path d="M-19 -9H9L18 -4V4L9 9H-19Z" fill="url(#metal)" stroke="#536775" stroke-width="1.5"/></g>'
    zipper += f'<g transform="translate({xr} {y+9}) rotate(18)"><path d="M19 -9H-9L-18 -4V4L-9 9H19Z" fill="url(#metal)" stroke="#536775" stroke-width="1.5"/></g>'
zipper += '''
<path d="M183 227Q253 203 323 227L296 359Q254 384 212 359Z" fill="url(#glass)" stroke="#8DA5B1" stroke-width="2"/>
<path d="M201 229L242 328M306 229L266 328" fill="none" stroke="#2459C4" stroke-width="4"/>
<path d="M242 227H267L255 277Z" fill="url(#blue)" stroke="#173F8F" stroke-width="2"/>
'''
for j in range(6):
    y = 309 + j*21
    zipper += f'<path d="M225 {y}H253L264 {y+6}L253 {y+12}H225Z" fill="url(#metal)" stroke="#536775" stroke-width="1.5"/>'
    zipper += f'<path d="M281 {y+10}H256L245 {y+16}L256 {y+22}H281Z" fill="url(#metal)" stroke="#536775" stroke-width="1.5"/>'
zipper += '<path d="M344 276L329 329M323 318L329 330L341 323" fill="none" stroke="#C94422" stroke-width="3" stroke-linecap="round"/>'
zipper += leader([(64,276),(122,276),(216,276)],"#2459C4")+label(43,251,"Area kontak",color="#2459C4",size=17)
zipper += leader([(310,442),(400,442),(400,358),(297,307)])+label(315,477,"Rumah transparan",size=16,anchor="middle")
zipper_svg = svg(zipper,label="Studi makro resleting dengan rumah transparan untuk memperlihatkan area kontak; geometri konseptual")

gears = '<ellipse cx="254" cy="405" rx="191" ry="19" fill="#172B3B" opacity=".07"/>'
gears += '<path d="M130 295L339 226" stroke="#CCD5D8" stroke-width="18" stroke-linecap="round"/>'
gears += gear(164,282,104,12,"url(#blue)",0.03)
gears += gear(335,226,78,9,"url(#metal)",.09)
gears += '''
<path d="M70 202A121 121 0 0 1 179 160M165 152L180 160L167 170" fill="none" stroke="#C94422" stroke-width="4" stroke-linecap="round"/>
<path d="M431 231A100 100 0 0 0 386 140M389 154L386 140L400 142" fill="none" stroke="#167580" stroke-width="4" stroke-linecap="round"/>
<circle cx="264" cy="246" r="27" fill="none" stroke="#C94422" stroke-width="2"/>
'''
gears += leader([(78,425),(163,425),(164,282)],"#C94422")+label(78,453,"INPUT",color="#C94422",size=18)
gears += leader([(370,345),(397,345),(397,270)],"#167580")+label(370,372,"OUTPUT",color="#167580",size=18)
gears += label(254,70,"GERAK → KONTAK → GERAK",size=15,anchor="middle")
gear_svg = svg(gears,label="Studi konseptual pasangan roda gigi untuk membedakan input, kontak, dan output")

for filename, illustration in [("exploded-pump.svg",pump_svg),("cutaway-valve.svg",valve_svg),("macro-zipper.svg",zipper_svg),("gear-transfer.svg",gear_svg)]:
    (ASSETS/filename).write_text(illustration, encoding="utf-8")

html = '''<!doctype html>
<html lang="id">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Di Balik Benda — Style Board v2 / 90 detik</title>
<style>
@font-face{font-family:Manrope;src:url('assets/manrope.ttf') format('truetype');font-weight:200 800;font-display:block}
@font-face{font-family:'IBM Plex Mono';src:url('assets/ibm-plex-mono.ttf') format('truetype');font-weight:400;font-display:block}
:root{--canvas:#ECEEE9;--surface:#F8F9F5;--ink:#172B3B;--muted:#536775;--line:#CDD4D4;--input:#C94422;--active:#2459C4;--output:#167580;--metal:#A6B4BE}
*{box-sizing:border-box}body{margin:0;background:var(--canvas);color:var(--ink);font-family:Manrope,sans-serif;-webkit-font-smoothing:antialiased}h1,h2,h3,p{margin:0}svg{display:block;width:100%;height:auto}svg text{font-weight:400}main{width:1700px;padding:48px 64px 32px;margin:0 auto}.mono{font-family:'IBM Plex Mono',monospace;font-weight:400}.eyebrow{font-size:15px;letter-spacing:.09em;text-transform:uppercase}.muted{color:var(--muted)}.topline{display:flex;justify-content:space-between;align-items:center;border-top:2px solid var(--ink);padding-top:15px}.stamp{display:flex;gap:12px;align-items:center}.stamp:before{content:'';width:11px;height:11px;background:var(--active);display:block;border-radius:50%}.masthead{display:grid;grid-template-columns:1.1fr 1fr;align-items:end;gap:40px;padding:33px 0 38px}.masthead h1{font-size:92px;line-height:.96;font-weight:800;letter-spacing:-.065em}.masthead .intro{padding:0 0 2px 14px}.intro h2{font-size:31px;line-height:1.2;font-weight:800;letter-spacing:-.035em;margin-bottom:13px}.intro p{font-size:21px;line-height:1.5;max-width:600px;color:var(--muted)}.hero-row{display:grid;grid-template-columns:1008px 540px;gap:24px}.hero{background:var(--surface);height:730px;position:relative;overflow:hidden;border:1px solid var(--line)}.panel-top{display:flex;justify-content:space-between;align-items:center;padding:28px 32px 0}.tag{font-family:'IBM Plex Mono',monospace;font-size:13px;color:var(--active);padding:7px 10px;border:1px solid #A5BCE7}.hero h2{font-size:48px;font-weight:800;letter-spacing:-.055em;line-height:1.07;position:absolute;left:32px;top:83px;z-index:1}.hero .hero-art{position:absolute;width:960px;left:24px;top:162px}.hero-note{position:absolute;left:32px;bottom:23px;font-size:13px;color:var(--muted)}.system{border-top:2px solid var(--ink);height:730px;padding-top:20px}.system h2{font-size:35px;letter-spacing:-.04em;line-height:1.1;margin:17px 0 14px;font-weight:800}.system .desc{font-size:19px;line-height:1.5;color:var(--muted);max-width:470px}.swatches{display:grid;grid-template-columns:repeat(5,1fr);gap:7px;margin:26px 0 24px}.swatch{height:65px;border:1px solid var(--line)}.swatches span{font-size:10px;letter-spacing:0}.swatches p{font-size:12px;margin-top:8px}.type-demo{border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:17px 0 20px}.type-demo .big{font-weight:800;font-size:46px;letter-spacing:-.055em;margin:5px 0}.type-demo .small{font-size:17px;color:var(--muted)}.legend{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:23px}.legend i{display:block;width:24px;height:4px;margin-bottom:10px}.legend h3{font-family:'IBM Plex Mono',monospace;font-size:14px;font-weight:400;margin-bottom:5px}.legend p{font-size:15px;line-height:1.4;color:var(--muted)}.flexible{font-size:16px;line-height:1.5;margin-top:23px;max-width:500px}.study-heading{display:flex;justify-content:space-between;align-items:end;margin:36px 0 19px}.study-heading h2{font-size:28px;font-weight:800;letter-spacing:-.035em}.study-heading p{font-size:14px;color:var(--muted)}.studies{display:grid;grid-template-columns:repeat(3,508px);gap:24px}.study{height:903px;width:508px;position:relative;background:var(--surface);border:1px solid var(--line);overflow:hidden}.study .meta{position:absolute;left:32px;right:32px;top:28px;display:flex;justify-content:space-between;font-size:12px;color:var(--muted)}.study h3{position:absolute;top:72px;left:32px;right:30px;font-size:42px;line-height:1.08;font-weight:800;letter-spacing:-.05em}.study .art{position:absolute;left:0;top:193px;width:508px}.study .explain{position:absolute;left:32px;right:32px;top:727px;font-size:23px;line-height:1.4;font-weight:500;letter-spacing:-.02em}.study .foot{position:absolute;left:32px;right:32px;bottom:28px;display:flex;justify-content:space-between;border-top:1px solid var(--line);padding-top:13px;font-size:11px;color:var(--muted)}.operation{margin-top:36px;padding:25px 0 24px;border-top:2px solid var(--ink);border-bottom:1px solid var(--line);display:grid;grid-template-columns:305px 1fr;gap:30px}.operation h2{font-size:30px;font-weight:800;letter-spacing:-.04em;margin:9px 0}.operation p{font-size:16px;line-height:1.5;color:var(--muted);max-width:290px}.poses{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}.pose{border-left:1px solid var(--line);padding-left:19px}.pose svg{height:91px;margin-bottom:13px}.pose .name{font-size:16px;font-weight:800;margin-bottom:6px}.pose .detail{font-size:13px;line-height:1.45;color:var(--muted)}.footer{padding-top:22px;display:flex;justify-content:space-between;gap:24px;font-size:12px;line-height:1.6;color:var(--muted)}.footer .disclaimer{max-width:960px}.footer .status{text-align:right;color:var(--ink)}
.pacing{margin-top:28px;padding:24px 0;border-bottom:1px solid var(--line)}.pacing-head{display:flex;justify-content:space-between;gap:40px;align-items:end;margin-bottom:22px}.pacing h2{font-size:32px;font-weight:800;letter-spacing:-.04em;margin-top:9px}.pacing-head p{font-size:17px;line-height:1.5;max-width:520px;color:var(--muted)}.timing-bar{display:flex;gap:7px}.segment{background:var(--surface);padding:14px 12px;border-bottom:3px solid var(--active);min-width:0}.segment .time{font-size:18px;display:block;margin-bottom:9px}.segment .job{font-size:14px;line-height:1.4;display:block}.pacing-note{font-size:14px;line-height:1.5;color:var(--muted);margin-top:16px}
@media print{body{print-color-adjust:exact;-webkit-print-color-adjust:exact}main{margin:0}@page{margin:0}}
</style></head>
<body><main id="board">
<div class="topline mono eyebrow"><div class="stamp">Di Balik Benda / 90 detik</div><div>Edukasi mekanisme · v2 · 23.10.2026</div></div>
<header class="masthead"><h1>DI BALIK<br>BENDA.</h1><div class="intro"><h2>Yang tersembunyi,<br>jadi terlihat.</h2><p>Benda sehari-hari dibuka, didekatkan, lalu diperlihatkan cara kerjanya. Ilustrasi memandu mata. Gerak menjelaskan hubungan.</p></div></header>
<section class="hero-row">
<div class="hero"><div class="panel-top"><span class="mono eyebrow">01 / Urai komponen</span><span class="tag">EXPLODED VIEW</span></div><h2>Setiap bagian<br>punya peran.</h2><div class="hero-art">__PUMP__</div><p class="hero-note mono">POMPA GENERIK / STUDI KONSEPTUAL / BUKAN PANDUAN PERAKITAN</p></div>
<aside class="system"><p class="mono eyebrow muted">Sistem visual / v1</p><h2>Seperti melihat lebih dekat.</h2><p class="desc">Permukaan mineral, volume yang terasa nyata, dan warna yang menunjukkan fungsi. Objek memimpin komposisi.</p>
<div class="swatches"><div><div class="swatch" style="background:#ECEEE9"></div><p>Mineral</p><span class="mono">#ECEEE9</span></div><div><div class="swatch" style="background:#172B3B"></div><p>Tinta</p><span class="mono">#172B3B</span></div><div><div class="swatch" style="background:#C94422"></div><p>Input</p><span class="mono">#C94422</span></div><div><div class="swatch" style="background:#2459C4"></div><p>Fokus</p><span class="mono">#2459C4</span></div><div><div class="swatch" style="background:#167580"></div><p>Output</p><span class="mono">#167580</span></div></div>
<div class="type-demo"><div class="mono eyebrow muted">Manrope 800 / 500</div><div class="big">Bongkar rasa ingin tahu.</div><div class="small mono">IBM PLEX MONO 400 / piston · pegas · poros</div></div>
<div class="legend"><div><i style="background:var(--input)"></i><h3>INPUT</h3><p>Gaya atau aksi yang memulai.</p></div><div><i style="background:var(--active)"></i><h3>FOKUS</h3><p>Bagian yang sedang diamati.</p></div><div><i style="background:var(--output)"></i><h3>OUTPUT</h3><p>Gerak atau aliran hasilnya.</p></div></div>
<p class="flexible">2D, 2,5D, atau 3D sesuai kebutuhan. Ruang kosong dan diam boleh dipakai saat membantu penjelasan.</p>
</aside></section>
<div class="study-heading"><h2>Satu identitas. Berbagai cara memperlihatkan.</h2><p class="mono">Studi mandiri · bukan urutan satu episode · 9:16</p></div>
<section class="studies">
<article class="study" id="study-01"><div class="meta mono"><span>DI BALIK BENDA</span><span>02 / POTONGAN</span></div><h3>Intip bagian<br>yang tertutup.</h3><div class="art">__VALVE__</div><p class="explain">Rumah dibuka sebagian.<br>Hubungan di dalam terlihat.</p><div class="foot mono"><span>CUTAWAY / STUDI KATUP</span><span>ILUSTRATIF</span></div></article>
<article class="study" id="study-02"><div class="meta mono"><span>DI BALIK BENDA</span><span>03 / MAKRO</span></div><h3>Dekatkan ke<br>titik penting.</h3><div class="art">__ZIPPER__</div><p class="explain">Satu area diperbesar.<br>Detail menjadi pusat cerita.</p><div class="foot mono"><span>MAKRO / STUDI RESLETING</span><span>ILUSTRATIF</span></div></article>
<article class="study" id="study-03"><div class="meta mono"><span>DI BALIK BENDA</span><span>04 / HUBUNGAN</span></div><h3>Ikuti geraknya.<br>Lihat kaitannya.</h3><div class="art">__GEARS__</div><p class="explain">Input, kontak, lalu output.<br>Gerak diberi arah dan urutan.</p><div class="foot mono"><span>TRANSFER / STUDI RODA GIGI</span><span>ILUSTRATIF</span></div></article>
</section>
<section class="operation"><div><span class="mono eyebrow muted">Bahasa gerak / konseptual</span><h2>Gerak punya tugas.</h2><p>Pose statis menunjukkan niat gerak. Timing, kamera, dan suara diuji saat membuat demo animasi.</p></div><div class="poses">
<div class="pose"><svg viewBox="0 0 200 90"><rect x="51" y="20" width="100" height="53" rx="17" fill="none" stroke="#A6B4BE" stroke-width="2"/><rect x="77" y="32" width="48" height="29" rx="6" fill="#2459C4"/><path d="M13 47H43M160 47H190" stroke="#CDD4D4" stroke-width="2"/></svg><p class="name">Isolasi</p><p class="detail">Konteks meredup.<br>Satu bagian tetap jelas.</p></div>
<div class="pose"><svg viewBox="0 0 200 90"><path d="M100 3V86" stroke="#CDD4D4" stroke-dasharray="3 5"/><ellipse cx="100" cy="16" rx="30" ry="8" fill="#172B3B"/><ellipse cx="100" cy="45" rx="24" ry="7" fill="#2459C4"/><ellipse cx="100" cy="73" rx="34" ry="9" fill="#A6B4BE"/><path d="M146 40V15M140 22L146 15L152 22" stroke="#C94422" stroke-width="2" fill="none"/></svg><p class="name">Urai</p><p class="detail">Komponen terpisah<br>mengikuti sumbunya.</p></div>
<div class="pose"><svg viewBox="0 0 200 90"><circle cx="62" cy="45" r="22" stroke="#A6B4BE" stroke-width="2" fill="none"/><circle cx="62" cy="45" r="6" fill="#2459C4"/><path d="M83 29L121 8M83 61L121 82" stroke="#CDD4D4" stroke-width="1.5"/><circle cx="155" cy="45" r="33" stroke="#2459C4" stroke-width="2" fill="none"/><circle cx="155" cy="45" r="16" fill="#2459C4"/></svg><p class="name">Dekatkan</p><p class="detail">Landmark dipertahankan<br>saat detail diperbesar.</p></div>
<div class="pose"><svg viewBox="0 0 200 90"><path d="M25 45H76M65 37L77 45L65 53" stroke="#C94422" stroke-width="3" fill="none"/><rect x="85" y="25" width="32" height="40" rx="4" fill="#2459C4"/><path d="M129 45H180M169 37L181 45L169 53" stroke="#167580" stroke-width="3" fill="none"/></svg><p class="name">Jalankan</p><p class="detail">Sebab mendahului akibat.<br>Tahan agar sempat dipahami.</p></div>
</div></section>
<section class="pacing"><div class="pacing-head"><div><span class="mono eyebrow muted">Default produksi / v2</span><h2>90 detik untuk membongkar proses.</h2></div><p>Mulai dari 14–18 shot penjelas. Tambahkan pose antara saat gerak, kontak, atau transfer perlu diperlihatkan lebih rinci.</p></div><div class="timing-bar">
<div class="segment" style="flex:7;border-color:var(--ink)"><span class="time mono">0–7 s</span><span class="job">Benda &amp;<br>pertanyaan</span></div>
<div class="segment" style="flex:15"><span class="time mono">7–22 s</span><span class="job">Urai bagian.<br>Kenali perannya.</span></div>
<div class="segment" style="flex:15;border-color:var(--input)"><span class="time mono">22–37 s</span><span class="job">Telusuri input<br>menuju kontak.</span></div>
<div class="segment" style="flex:25"><span class="time mono">37–62 s</span><span class="job">Perbesar titik penting.<br>Perlihatkan interaksi bertahap.</span></div>
<div class="segment" style="flex:15;border-color:var(--output)"><span class="time mono">62–77 s</span><span class="job">Ikuti hasilnya.<br>Amati perubahan.</span></div>
<div class="segment" style="flex:13;border-color:var(--ink)"><span class="time mono">77–90 s</span><span class="job">Kembali ke utuh.<br>Lihat satu siklus.</span></div>
</div><p class="pacing-note">Contoh alokasi, fleksibel sesuai mekanisme. Rancang 2–4 pose diagnostik untuk interaksi penting bila diperlukan. Jumlah shot bertambah; fps mengikuti brief episode. Tiap shot perlu mengungkap informasi baru.</p></section>
<footer class="footer mono"><div class="disclaimer">Semua gambar dan copy adalah studi desain konseptual, bukan diagram teknis terverifikasi. Bentuk, sambungan, dan gerak perlu divalidasi sebelum dipakai dalam episode. Preview ini statis; motion dan audio masih berupa arahan.</div><div class="status">ARAH PRODUKSI v2<br>Revisi sesuai arahan · 23.10.2026</div></footer>
</main></body></html>'''
for key, value in [("__PUMP__",pump_svg),("__VALVE__",valve_svg),("__ZIPPER__",zipper_svg),("__GEARS__",gear_svg)]:
    html=html.replace(key,value)
(ROOT/"style-board.html").write_text(html,encoding="utf-8")
print("Built style-board.html and four SVG studies; local fonts and licenses preserved.")
