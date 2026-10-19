"""Build deterministic static HyperFrames poses from the approved episode plan.

Run from any directory. Re-running writes only this production's storyboard source
files; it does not generate audio, animation, video exports, or review approval.
"""
from pathlib import Path
import html
import json
import re
import shutil
import urllib.request

PROD = Path(__file__).resolve().parent
VIDEO = PROD / "video"
BOARD = PROD.parents[1] / "boards" / "ruang-di-antara"
if not (VIDEO / "BRIEF.md").exists():
    raise SystemExit("Initialize HyperFrames and write BRIEF.md first")
existing_storyboard = VIDEO / "STORYBOARD.md"
if existing_storyboard.exists():
    existing_text = existing_storyboard.read_text(encoding="utf-8")
    if "layout_approved: true" in existing_text or "- status: animated" in existing_text:
        raise SystemExit("Preserve approved/animated layouts; revise only the affected compositions instead of rebuilding all poses")

INK, PAPER, BRICK, SAND = "#302B28", "#F3EDE3", "#A34F3F", "#D8C8B5"
fonts = VIDEO / "assets" / "fonts"
fonts.mkdir(parents=True, exist_ok=True)
for name in ["newsreader.ttf", "newsreader-italic.ttf", "dm-sans.ttf", "Newsreader-OFL.txt", "DM-Sans-OFL.txt"]:
    shutil.copy2(BOARD / "assets" / name, fonts / name)
vendor = VIDEO / "assets" / "vendor"
vendor.mkdir(parents=True, exist_ok=True)
if not (vendor / "gsap.min.js").exists():
    urllib.request.urlretrieve("https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js", vendor / "gsap.min.js")

script = (PROD / "SCRIPT.md").read_text(encoding="utf-8")
narration = script.split("## Reading copy\n\n", 1)[1].split("\n## Timing and delivery", 1)[0].strip()
paras = narration.split("\n\n")
assert len(paras) == 14 and len(narration.split()) == 180

def text(lines, x=88, y=230, size=112, color=INK, italic=False, width=850, cls="headline"):
    if isinstance(lines, str):
        lines = [lines]
    spans = "".join(f'<span>{html.escape(line)}</span>' for line in lines)
    return f'<div class="{cls}" style="left:{x}px;top:{y}px;width:{width}px;font-size:{size}px;color:{color};font-style:{"italic" if italic else "normal"}">{spans}</div>'

def label(content, x, y, width=800, size=40, color=INK):
    return f'<p class="label" style="left:{x}px;top:{y}px;width:{width}px;font-size:{size}px;color:{color}">{html.escape(content)}</p>'

def actor(x, y, r=85, color=INK, kind=0):
    d = ("M-87,-17 C-90,-70 -57,-98 -11,-96 C42,-99 88,-67 88,-14 C97,36 64,89 13,94 C-47,103 -87,62 -87,-17Z"
         if kind == 0 else "M-83,-28 C-77,-80 -31,-103 13,-91 C64,-81 92,-44 86,10 C88,65 49,91 2,94 C-50,96 -93,49 -83,-28Z")
    return f'<path d="{d}" transform="translate({x} {y}) scale({r/94:.4f})" fill="{color}"/>'

def path(d, color=BRICK, width=4, dashed=False, opacity=1):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"'+(' stroke-dasharray="10 13"' if dashed else '')+'/>'

def ring(x, y, rx, ry=None, color=BRICK, dashed=True):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry or rx}" fill="none" stroke="{color}" stroke-width="4"'+(' stroke-dasharray="10 13"' if dashed else '')+'/>'

def svg(content):
    return f'<svg class="diagram" viewBox="0 0 1080 1920" aria-hidden="true">{content}</svg>'

def mark(x, y, w=80, color=BRICK):
    return svg(path(f'M{x},{y} h{w}', color, 5))

CSS = '''
@font-face{font-family:Newsreader;src:url("assets/fonts/newsreader.ttf") format("truetype");font-style:normal;font-weight:100 900;font-display:block}
@font-face{font-family:Newsreader;src:url("assets/fonts/newsreader-italic.ttf") format("truetype");font-style:italic;font-weight:100 900;font-display:block}
@font-face{font-family:"DM Sans";src:url("assets/fonts/dm-sans.ttf") format("truetype");font-weight:100 900;font-display:block}
*{box-sizing:border-box}#root{position:absolute;inset:0;width:100%;height:100%;overflow:hidden;color:#302B28}
.clip{position:absolute;inset:0}.paper{background:#F3EDE3}.dark-paper{background:#302B28}
.diagram{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.headline{position:absolute;font-family:Newsreader,serif;font-weight:400;line-height:1.045;letter-spacing:-.035em;margin:0}
.headline span{display:block}.label{position:absolute;margin:0;font-family:"DM Sans",sans-serif;font-weight:400;line-height:1.3;letter-spacing:-.018em}
.series{position:absolute;left:88px;top:101px;font:500 26px/1.3 "DM Sans",sans-serif;letter-spacing:.095em;text-transform:uppercase}
.number{position:absolute;right:144px;top:101px;font:500 26px/1.3 "DM Sans",sans-serif;letter-spacing:.05em}
.foot{position:absolute;left:88px;bottom:82px;font:400 26px/1.3 "DM Sans",sans-serif}
'''

frames = []
def add(slug, title, duration, scene, key, role, content, typ="feature_showcase", persuasion="Progressive disclosure", beat="comprehension", dark=False):
    i = len(frames)+1
    start = sum(f["duration"] for f in frames)
    frames.append(dict(i=i,slug=slug,title=title,duration=duration,start=start,end=start+duration,
                       scene=scene,key=key,role=role,content=content,type=typ,persuasion=persuasion,beat=beat,dark=dark))

# 01: Imagined future dominates the actual distance.
add("baru-beberapa-obrolan", "Baru beberapa obrolan", 5,
    "Two actual actors and an oversized dashed bridge above their actual distance.",
    "A few conversations can sit alongside an imagined shared future.", "Open the concrete gap between experience and imagined closeness.",
    text(["Baru beberapa", "obrolan."]) + text(["Sudah kebayang", "hidup bareng."], y=515, size=103, color=BRICK, italic=True)
    + svg(path("M267,1228 C250,925 400,828 560,845 C740,858 832,1020 824,1230", BRICK, 4, True)
          + path("M352,1264 H475", INK, 5) + actor(261,1264,90) + actor(824,1264,90,BRICK,1))
    + label("yang sudah terjadi", 153,1418,400,34) + label("yang dibayangkan", 385,1005,450,34,BRICK),
    typ="hook", persuasion="Concretization", beat="recognition")

# 02: The observation has a small solid connection; the conclusion is visibly larger.
add("kopi-dan-kesimpulan", "Kopi dan kesimpulan", 7,
    "A small solid coffee memory and a large outlined thought are connected only by interpretation.",
    "Remembering a preference and imagining understanding are different claims.", "Expose observation versus interpretation by the second beat.",
    text(["Dia ingat", "kopi lo."],size=124) + mark(88,535)
    + label("KEJADIAN",88,585,700,28)
    + svg(actor(214,884,79)+actor(614,884,79,BRICK,1)+path("M293,884 H535",INK,5)
          +path("M615,972 C618,1030 484,1055 484,1120",BRICK,4,True)
          +path("M142,1142 Q120,1120 154,1100 H827 Q860,1100 860,1135 V1380 Q860,1415 827,1415 H155 Q125,1415 125,1380 V1145",BRICK,4,True))
    + text(["“Dia bakal", "ngerti gue.”"],x=182,y=1162,size=91,color=BRICK,italic=True,width=665)
    + label("TAFSIR",182,1360,580,28,BRICK),typ="social_proof",persuasion="Concretization + comparison",beat="recognition")

# 03: Unknown attributes stay open, not negative.
add("yang-belum-lo-tahu", "Yang belum lo tahu", 7,
    "A solid actor surrounded by three labelled open spaces.", "Compatibility still contains unknowns.",
    "Give the missing shared experience concrete dimensions without judging the person.",
    text(["Yang belum", "lo tahu"],size=118)
    +svg(actor(542,1080,106,BRICK,1)+path("M473,992 L330,830",INK,4)+path("M642,1070 H767",INK,4)+path("M491,1171 L346,1328",INK,4)
          +ring(279,772,69,51,SAND)+ring(828,1070,67,51,SAND)+ring(294,1377,69,51,SAND))
    +label("menghadapi",140,600,400,38)+label("perbedaan",140,650,400,38)
    +label("menepati janji",623,1160,300,38)+label("menghormati batas",96,1450,720,38),
    persuasion="Rule of three",beat="curiosity")

# 04: Pull back and compare lengths of lived vs imagined connection.
add("kedekatan-yang-dibayangkan", "Kedekatan yang dibayangkan", 6,
    "A short solid shared segment becomes an outlined unfinished extension.", "Part of the closeness remains imagined.",
    "Make the episode's central distinction visible in one continuous line.",
    text(["Kedekatan", "yang lo", "bayangkan"],size=112,color=BRICK,italic=True)
    +svg(actor(222,1005,82)+actor(820,1328,82,BRICK,1)+path("M304,1005 H419",INK,6)
          +path("M419,1005 C650,1005 490,1220 660,1240 C740,1250 754,1280 760,1310",BRICK,4,True))
    +label("sudah dialami",88,1158,430,36)+label("belum dijalani bersama",415,1450,510,36,BRICK),
    typ="pain_point",persuasion="Visual metaphor",beat="recognition")

# 05: Concept introduction; no person receives a diagnosis.
add("limerence", "Limerence", 9,
    "The concept title sits above an attention path repeatedly returning toward another person.",
    "Involuntary preoccupation and wanting reciprocation are described features.", "Name the concept after the viewer recognizes the illustrative scene.",
    text("Limerence",size=145) + mark(88,465)
    +label("Terpaku pada seseorang.",88,540,size=45)
    +label("Sangat ingin dibalas.",88,610,size=45)
    +label("Pikiran sulit dialihkan.",88,680,size=45)
    +svg(actor(240,1170,94)+actor(812,1170,94,BRICK,1)
          +path("M334,1170 C475,940 664,945 716,1109",BRICK,4)
          +path("M334,1170 C469,1025 627,1061 716,1150",BRICK,4)
          +path("M334,1170 C481,1370 650,1366 716,1224",BRICK,4))
    +label("perhatian kembali ke dia",247,1450,680,36),typ="product_intro",persuasion="Progressive disclosure",beat="clarity")

# 06: The question remains in the gap.
add("perasaan-yang-belum-jelas", "Perasaan yang belum jelas", 4,
    "Two large solid actors frame an unanswered question in the space between them.", "The other person's feelings are unknown.",
    "Hold uncertainty without inventing the other person's intentions.",
    text(["“Dia ngerasa", "sama, nggak?”"],y=285,size=110,italic=True)
    +svg(actor(172,1110,154)+actor(876,1110,154,BRICK,1)+path("M329,1110 H418",INK,5)+path("M618,1110 H719",INK,5))
    +text("?",x=461,y=994,size=174,color=BRICK,width=150)
    +label("belum ada jawaban",296,1405,600,38),persuasion="Question→answer pairing (question held open)",beat="uncertainty")

# 07: A repeat reading loop, not a screenshot-based claim about anybody real.
add("mencari-tanda", "Mencari tanda", 7,
    "A conversation fragment anchors repeated attention paths and an outlined possibility.", "Rereading an interaction may become a search for signs.",
    "Show the script's invented example of sign-seeking.",
    text(["Mencari", "tanda"],size=126)
    +svg(path("M172,774 H777 Q817,774 817,814 V1000 Q817,1040 777,1040 H335 L261,1104 V1040 H172 Q132,1040 132,1000 V814 Q132,774 172,774Z",INK,4)
          +path("M739,1100 C870,1210 730,1384 474,1371 C253,1354 184,1221 248,1124",BRICK,4)
          +path("M247,1124 L228,1180 M247,1124 L299,1154",BRICK,4)
          +ring(788,1313,130,104,BRICK))
    +text("“Ingat kopi lo.”",x=190,y=845,size=70,width=620)
    +label("dibaca lagi",120,1450,350,38)
    +label("harapan membesar",497,1450,460,36,BRICK),persuasion="Demonstration",beat="recognition")

# 08: The only charcoal pressure frame; the person remains real and solid.
add("menjaga-kemungkinan", "Menjaga kemungkinan", 6,
    "Multiple outlined explanations surround the same solid conversation on a charcoal field.", "Interpretations can preserve an imagined possibility.",
    "Expose effort to retain hope without asserting manipulation by the other person.",
    text(["Menjaga", "kemungkinan"],size=108,color=PAPER)
    +svg(actor(214,1235,91,PAPER)+actor(810,1235,91,BRICK,1)
          +path("M305,1235 C376,807 751,732 794,1144",SAND,4,True)
          +path("M305,1235 C429,1047 663,1045 719,1193",PAPER,4,True)
          +path("M305,1235 C490,1480 683,1470 756,1302",SAND,4,True))
    +text("“Mungkin…”",x=240,y=778,size=88,color=SAND,italic=True,width=690)
    +label("mencari penjelasan lagi",145,1450,760,38,PAPER),persuasion="Accumulation",beat="tension",dark=True)

# 09: The wide reveal: the imagined relationship dwarfs the experienced part.
add("hubungan-yang-belum-dijalani", "Hubungan yang belum dijalani", 6,
    "A large outlined imagined structure surrounds a much smaller shared solid segment.", "What repeats mentally may be a version of a relationship not yet lived.",
    "Reveal the object of repeated imagination while preserving actual distance.",
    text(["Hubungan", "yang belum", "dijalani"],size=111)
    +svg(path("M162,1036 C162,774 830,774 830,1036 V1310 C830,1515 162,1515 162,1310 Z",BRICK,4,True)
          +path("M238,1254 H364",INK,6)+actor(178,1254,65)+actor(812,1254,65,BRICK,1)
          +path("M364,1254 C520,1141 601,1141 746,1254",BRICK,4,True))
    +label("yang sudah dialami",310,1330,580,36),typ="benefit_highlight",persuasion="Visual metaphor",beat="recognition")

# 10: Explicitly avoid a diagnostic equivalence.
add("satu-kebiasaan-belum-cukup", "Satu kebiasaan belum cukup", 5,
    "An imagined-future outline and the concept label remain separated by an open interval.", "Imagining a future alone does not establish limerence.",
    "Qualify the explanation before the viewer turns the scenario into a diagnosis.",
    text(["Satu kebiasaan", "belum cukup."],size=106)
    +label("Untuk menyimpulkan limerence.",88,570,size=43)
    +svg(ring(281,1070,152,120,BRICK)+path("M454,1070 H493",SAND,4)+path("M601,1070 H639",SAND,4))
    +text("?",x=512,y=1001,size=107,color=BRICK,width=120)
    +label("membayangkan",103,1254,450,37)+label("masa depan",103,1308,450,37)
    +text("limerence",x=665,y=1025,size=66,width=300),typ="branding",persuasion="Qualification",beat="clarity")

# 11: Everyday impact as questions rather than scores or diagnostic thresholds.
add("perhatikan-dampaknya", "Perhatikan dampaknya", 6,
    "An attention path interrupts a simple day line, paired with two open reflective questions.", "Consider ability to redirect attention and the effect on everyday life.",
    "Move from recognizing an illustration to observing personal impact without a checklist.",
    text(["Perhatikan", "dampaknya."],size=119)
    +svg(path("M126,924 H890",SAND,5)+path("M300,908 V940 M531,908 V940 M757,908 V940",SAND,4)
          +path("M215,927 C385,650 722,680 738,939 C747,1119 413,1131 399,938 C388,765 729,787 843,934",BRICK,5)
          +actor(167,924,48)+actor(891,924,48,BRICK,1))
    +label("Sulit dialihkan?",88,1192,size=48)+label("Keseharian terganggu?",88,1300,size=48),
    persuasion="Question→answer pairing (reflection)",beat="reflection")

# 12: Two lanes differentiate fact and hope; do not frame as a treatment.
add("pisahkan-dua-hal", "Pisahkan dua hal", 6,
    "One path divides into a solid observation lane and a dashed expectation lane.", "An observation and the expectation attached to it can be named separately.",
    "Offer a concrete distinction with no promise of curing preoccupation.",
    text(["Coba", "pisahkan."],size=136)
    +svg(path("M525,715 V861 C525,937 257,927 257,1007 V1030",INK,5)
          +path("M525,861 C525,937 799,927 799,1007 V1030",BRICK,4,True))
    +text(["Yang", "terjadi"],x=88,y=1100,size=88,width=390)
    +text(["Yang lo", "harapkan"],x=563,y=1100,size=84,color=BRICK,italic=True,width=395)
    +label("kejadian",88,1430,370,34)+label("harapan / tafsir",563,1430,380,34,BRICK),
    typ="benefit_highlight",persuasion="Comparison",beat="clarity")

# 13: The full callback has two vertically separated panels for phone legibility.
add("ingat-kopi-belum-tahu-cocok", "Ingat kopi ≠ sudah tahu cocok", 10,
    "Coffee observation and compatibility conclusion occupy two clearly labelled horizontal bands.", "Remembering a coffee order does not establish compatibility as partners.",
    "Ground the distinction in the same familiar example and leave room for mutual learning.",
    text(["Ingat kopi ≠", "sudah tahu cocok"],size=91)
    +svg(path("M88,724 H928",INK,4)+path("M88,1108 H928",BRICK,4,True)
          +actor(193,1438,58)+actor(824,1438,58,BRICK,1)+path("M252,1438 H374",INK,5))
    +label("YANG TERJADI",88,660,size=28)
    +text(["“Dia inget", "kopi gue.”"],x=105,y=785,size=92,width=760)
    +label("YANG LO SIMPULKAN",88,1040,size=28,color=BRICK)
    +text(["“Dia pasti cocok", "jadi pasangan gue.”"],x=105,y=1163,size=74,color=BRICK,italic=True,width=790),
    typ="social_proof",persuasion="Callback + comparison",beat="comprehension")

# 14: No invented resolution; the modest lived connection remains.
add("yang-dibangun-berdua", "Yang dibangun berdua", 6,
    "Two real actors and a modest shared segment remain below a spacious closing question.", "Ask what closeness has actually been built together.",
    "Land the reflection without inventing mutual commitment or dismissing the feeling.",
    text(["Apa yang sudah", "kalian bangun", "berdua?"],y=300,size=108)
    +svg(actor(232,1225,92)+actor(813,1225,92,BRICK,1)+path("M324,1225 H472",INK,5)
          +path("M472,1225 H684",SAND,4,True))
    +label("ruang untuk saling mengenal",133,1450,800,38),typ="cta",persuasion="Callback + reflection",beat="reflection")

assert sum(f["duration"] for f in frames) == 90
out = VIDEO / "compositions" / "frames"
out.mkdir(parents=True, exist_ok=True)
hosts = []
for f in frames:
    ident = f'limerence-{f["i"]:02d}'
    filename = f'{f["i"]:02d}-{f["slug"]}.html'
    foreground = PAPER if f["dark"] else INK
    ground = "dark-paper" if f["dark"] else "paper"
    body = f'''<!doctype html><html lang="id"><head><meta charset="utf-8"></head><body><template>
<style>{CSS}</style>
<div id="root" data-composition-id="{ident}" data-width="1080" data-height="1920" data-duration="{f['duration']}">
<div id="{ident}-background" class="clip {ground}" data-start="0" data-duration="{f['duration']}" data-track-index="0"></div>
<div id="{ident}-content" class="clip" data-start="0" data-duration="{f['duration']}" data-track-index="1" style="color:{foreground}">
<div class="series">Ruang di Antara</div><div class="number">{f['i']:02d} / 14</div>
{f['content']}
<div class="foot">@eliansatya</div>
</div></div>
<script>const hold=gsap.timeline({{paused:true}});hold.to({{p:0}},{{p:1,duration:{f['duration']},ease:"none"}},0);window.__timelines["{ident}"]=hold;</script>
</template></body></html>'''
    (out / filename).write_text(body, encoding="utf-8")
    f["src"] = f"compositions/frames/{filename}"
    f["poster"] = f["start"] + f["duration"]/2
    hosts.append(f'<section id="scene-{f["i"]:02d}-{f["slug"]}" class="clip" data-composition-id="{ident}" data-composition-src="{f["src"]}" data-start="{f["start"]}" data-duration="{f["duration"]}" data-track-index="1" data-width="1080" data-height="1920"></section>')

index = '''<!doctype html><html lang="id" data-resolution="portrait"><head><meta charset="utf-8">
<meta name="viewport" content="width=1080, height=1920"><title>Limerence — static storyboard</title>
<script src="assets/vendor/gsap.min.js"></script><style>
*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#F3EDE3}
#root{position:relative;width:100%;height:100%;overflow:hidden;background:#F3EDE3}.clip{position:absolute;inset:0}
</style></head><body><div id="root" data-composition-id="limerence" data-start="0" data-duration="90" data-width="1080" data-height="1920">'''+"\n".join(hosts)+'''</div>
<script>const hold=gsap.timeline({paused:true});hold.to({p:0},{p:1,duration:90,ease:"none"},0);window.__timelines["limerence"]=hold;</script></body></html>'''
(VIDEO / "index.html").write_text(index, encoding="utf-8")

extract = VIDEO / "capture" / "extracted"
extract.mkdir(parents=True, exist_ok=True)
(extract / "visible-text.txt").write_text(narration+"\n", encoding="utf-8")
(VIDEO / "user_script.txt").write_text(narration+"\n", encoding="utf-8")
(extract / "tokens.json").write_text(json.dumps(dict(title="Kenal dia, atau mengisi yang belum lo tahu?",description="Ruang di Antara v1.1 — limerence",colors=[PAPER,INK,BRICK,SAND],fonts=["Newsreader","DM Sans"]),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

script_lines = ["# Narration — approved v1", "", "Approved 2026-10-18. Preserve wording verbatim. The source is ../SCRIPT.md. Timing remains estimated.", ""]
for f,p in zip(frames,paras):
    script_lines += [f'## Frame {f["i"]}: {f["title"]}', "", p, ""]
(VIDEO / "SCRIPT.md").write_text("\n".join(script_lines),encoding="utf-8")

sb = ['---','format: 1080x1920','duration: 90s','message: "Distinguish imagined closeness from what two people have actually experienced together."',
      'arc: concept-explainer','audience: Indonesian-speaking adults reflecting on romantic attraction','mode: collaborative','music: none',
      'stage: styled-static-sketches','plan_approved: 2026-10-19','layout_approved: false','---','',
      '# Limerence — storyboard v1','',
      'The 14-frame plan and portrait canvas were accepted with “cocok” on 2026-10-19. These are static poses only. All timings are estimates; the 180 approved spoken words remain verbatim. `music: none` prevents an automatic music request during this visual-only stage and does not mark the future narrated film silent.','',
      'Visual grammar: actual people and observed actions are solid; imagined connections use open/dashed strokes. Both real actors remain solid. One charcoal field (08); cream elsewhere. Reserve y=1570–1760 for later two-line captions. No audio generation, animation, or video export is part of this review.','']
for f,p in zip(frames,paras):
    act = 1 if f['i']<=4 else 2 if f['i']<=9 else 3 if f['i']<=11 else 4
    sb += [f'## Frame {f["i"]}: {f["title"]} ({f["start"]}-{f["end"]}s)','',
           '- status: outline',f'- act: {act}',f'- src: {f["src"]}',f'- duration: {f["duration"]}s',f'- poster: {f["poster"]}',
           '- transition_in: cut',f'- type: {f["type"]}',f'- persuasion: {f["persuasion"]}',f'- beat: {f["beat"]}',
           f'- scene: {f["scene"]}',f'- voiceover: {json.dumps(p,ensure_ascii=False)}','',
           f'narrativeRole: {f["role"]}',f'keyMessage: {f["key"]}','',
           'Static pose: see the mounted composition and its storyboard still. The visual plan is approved; the posed layout is awaiting review. `built` will be set only after the actual snapshot is inspected.','']
(VIDEO / "STORYBOARD.md").write_text("\n".join(sb),encoding="utf-8")
(VIDEO / "storyboard-data.json").write_text(json.dumps([{k:v for k,v in f.items() if k!='content'} for f in frames],ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(dict(frames=len(frames),seconds=90,words=len(narration.split()),snapshot_at=','.join(str(f['poster']) for f in frames)),ensure_ascii=False))
