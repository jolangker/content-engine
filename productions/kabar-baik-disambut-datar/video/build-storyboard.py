"""Author the static storyboard from approved narration and board v2 tokens."""
from pathlib import Path
import json
import re
import html
import shutil

ROOT = Path(__file__).resolve().parent
EPISODE = ROOT.parent
BOARD = EPISODE.parent.parent / 'boards' / 'ruang-di-antara'
PAPER, INK, BRICK, SAND = '#F3EDE3', '#302B28', '#A34F3F', '#D8C8B5'

for name in ('assets/fonts', 'assets/vendor', 'compositions/frames', 'boards/stills', 'capture/extracted'):
    (ROOT / name).mkdir(parents=True, exist_ok=True)
for name in ('newsreader.ttf', 'newsreader-italic.ttf', 'dm-sans.ttf', 'Newsreader-OFL.txt', 'DM-Sans-OFL.txt'):
    shutil.copyfile(BOARD / 'assets' / name, ROOT / 'assets/fonts' / name)

source = (EPISODE / 'SCRIPT.md').read_text(encoding='utf-8')
paragraphs = re.findall(r'^    (.+)$', source, re.M)
context = re.split(r'(?<=[.!?])\s+', paragraphs[4])
voices = [paragraphs[0], paragraphs[1], ' '.join(paragraphs[2:4]),
          ' '.join(context[:4]), ' '.join(context[4:]), paragraphs[5], paragraphs[6],
          paragraphs[7], paragraphs[8], paragraphs[9], paragraphs[10], paragraphs[11],
          ' '.join(paragraphs[12:14]), ' '.join(paragraphs[14:16])]
if ' '.join(' '.join(voices).split()) != ' '.join(' '.join(paragraphs).split()):
    raise ValueError('Narration segmentation changed the approved script')

durations = [4, 4, 4, 9, 7, 5, 6, 9, 3, 7, 7, 7, 10, 8]
titles = ['Pulang membawa cerita', 'Kabar baiknya', 'Perhatian di layar', 'Latihan semalam',
          'Berani maju', 'Cerita yang tertahan', 'Berbagi kabar baik', 'Respons yang terlibat',
          'Kembali ke ruang tamu', 'Ceritain', 'HP diletakkan', 'Lihat konteksnya',
          'Menjanjikan waktu', 'Benar-benar kembali']
slugs = ['pulang', 'kabar-baik', 'layar', 'latihan', 'presentasi', 'tertahan', 'berbagi',
         'terlibat', 'kembali', 'ceritain', 'hp-diletakkan', 'konteks', 'waktu', 'hadir']
purposes = [
    'Mengenalkan siapa yang datang, ruang yang dibagi, dan antusiasme awal.',
    'Memberi isi konkret pada kabar baik: presentasi yang dipuji.',
    'Memperlihatkan arah perhatian pada momen jawaban singkat, tanpa menyimpulkan niat.',
    'Membuka usaha sebelum pencapaian supaya arti kabar baik dapat diikuti.',
    'Memperlihatkan keberanian yang tadinya diragukan dalam satu situasi kerja.',
    'Menampilkan gestur menarik diri dan catatan yang tidak jadi dibuka.',
    'Mengenalkan berbagi pengalaman positif lewat ruang percakapan bersama (C1).',
    'Memberi nama satu pembeda respons dan menyampaikan asosiasi secara terbatas (C2–C3).',
    'Mengembalikan posisi ruang dan pemeran sebelum mencoba respons lain.',
    'Memperlihatkan perhatian dan rasa ingin tahu lewat contoh dialog.',
    'Membuat peralihan perhatian terlihat lewat tindakan pada HP.',
    'Mengingatkan bahwa satu respons tidak cukup untuk menilai kepedulian (C4).',
    'Memberi contoh mengakui kabar baik dan memperjelas kapan bisa mendengar.',
    'Memperlihatkan tindak lanjut dan memberi ruang pada satu pertanyaan penutup.'
]
actions = [
    'A masuk dari pintu kiri, membawa tas dan kartu catatan; B ada di ruang yang sama.',
    'Medium A membuka telapak tangan; kartu presentasi masih di tangan satunya.',
    'Close-up B: kepala dan tangan mengarah ke HP; A menjadi potongan foreground.',
    'Kilas balik: A berlatih di meja, laptop terbuka, lembar catatan tersusun.',
    'Kilas balik: A berdiri di depan bidang presentasi; dua siluet audiens di foreground.',
    'Kembali ke rumah: tangan A menurunkan kartu catatan; bahu dan gestur tertahan.',
    'Overhead meja dan tangan dua pemeran: ruang untuk cerita berada di antara mereka.',
    'Two-shot: badan dan gestur B menghadap A; meja menjadi bidang yang dibagi.',
    'Sudut yang mengulang shot pembuka; B mulai menoleh dari HP kepada A.',
    'Medium B mengangkat kepala dan membuka telapak tangan, mengundang cerita.',
    'Close-up tangan meletakkan HP di meja; gestur A tetap terlihat di belakang.',
    'Sudut kerja B: catatan dan pena menunjukkan adanya kegiatan yang belum selesai.',
    'B mengakui kabar baik sambil menunjuk catatan yang hendak dibereskan; jam menjadi konteks waktu.',
    'Two-shot penutup: catatan ditutup, HP telungkup, B kembali menghadap A yang bercerita.'
]
captions = [
    ['Bayangin, lo pulang', 'bawa kabar baik.'],
    ['“Tadi presentasi gue', 'dipuji atasan.”'],
    ['“Oh, bagus.”'],
    ['Semalam lo latihan', 'berkali-kali.'],
    ['Jadi, pujian tadi', 'terasa penting buat lo.'],
    ['“Ya udah.', 'Nggak usah cerita panjang.”'],
    ['Berbagi kabar baik', 'dengan orang dekat.'],
    ['Respons yang antusias', 'dan terlibat.'],
    ['Di adegan tadi,', 'responsnya bisa begini:'],
    ['“Ceritain, bagian mana', 'yang paling dipuji?”'],
    ['Sekarang, detail yang tadinya', 'ketahan punya tempat.'],
    ['Satu jawaban pendek', 'belum cukup buat menilai.'],
    ['“Gue seneng dengernya.', 'Kasih gue sepuluh menit.”'],
    ['Coba ingat kabar baik', 'terakhir yang dia bagi.']
]
types = ['hook', 'social_proof', 'pain_point', 'social_proof', 'social_proof', 'pain_point',
         'product_intro', 'feature_showcase', 'feature_showcase', 'social_proof',
         'benefit_highlight', 'feature_showcase', 'feature_showcase', 'cta']
beats = ['anticipation', 'delight', 'tension', 'recognition', 'relief', 'disappointment',
         'orientation', 'clarity', 'anticipation', 'warmth', 'connection', 'consideration', 'reassurance', 'reflection']

def path(d, fill=INK, stroke=None, sw=0, extra=''):
    return f'<path d="{d}" fill="{fill}"' + (f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else '') + f' {extra}/>'

def line(d, color=INK, width=8, extra=''):
    return path(d, 'none', color, width, extra)

def rect(x,y,w,h,fill,rx=0,stroke=None,sw=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"' + (f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '') + '/>'

def ellipse(x,y,rx,ry,fill,extra=''):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" {extra}/>'

def group(content,x=0,y=0,s=1,rotate=0,flip=False):
    return f'<g transform="translate({x} {y}) rotate({rotate}) scale({-s if flip else s} {s})">{content}</g>'

def phone(x,y,s=1,angle=0,back=False):
    art=rect(-55,-103,110,206,INK,18)
    if back:
        art += rect(-45,-93,90,186,SAND,13) + ellipse(-24,-70,9,9,INK) + ellipse(-24,-40,9,9,INK)
    else:
        art += rect(-43,-84,86,166,SAND,9) + line('M-14 -93 H14',PAPER,5)
        art += path('M-43 15 L43 -35 L43 82 L-43 82 Z',PAPER)
        art += line('M-12 68 H12',INK,4)
    return group(art,x,y,s,angle)

def notes(x,y,s=1,angle=0,closed=False):
    art=rect(-85,-60,170,120,SAND,5,INK,5)
    if not closed:
        art += path('M-76 -51 H76 V51 H-76 Z',PAPER)
        art += line('M-54 -25 H36 M-54 -3 H53 M-54 20 H14',INK,5)
    else:
        art += line('M-55 -59 V59',INK,5) + rect(-36,-25,79,7,BRICK,3)
    return group(art,x,y,s,angle)

def cup(x,y,s=1):
    return group(ellipse(0,24,40,12,SAND)+path('M-26 -30 H26 V21 Q0 35 -26 21 Z',PAPER,INK,5)+line('M26 -23 C65 -30 62 10 28 10',INK,6)+ellipse(0,-30,25,8,SAND),x,y,s)

def table(x=565,y=1180,s=1):
    return group(line('M-150 20 L-180 270 M160 15 L190 250 M20 15 L25 290',INK,13)+ellipse(0,0,240,60,INK),x,y,s)

def room(door=False,wall_art=True):
    art=rect(0,0,1080,1920,PAPER)+rect(0,1310,1080,610,SAND)
    art += line('M0 1310 H1080',INK,4)+line('M0 1570 L1080 1390 M0 1810 L1080 1540',INK,3, 'opacity=".18"')
    if door:
        art+=rect(105,245,285,1050,SAND,2)+rect(130,275,230,995,INK,1)
        art+=path('M136 280 L327 320 V1274 L136 1270 Z',SAND)+ellipse(292,806,9,10,INK)
    elif wall_art:
        art+=rect(145,325,225,300,SAND,1)+rect(162,342,191,265,PAPER)
        art+=path('M180 590 V505 Q260 375 337 505 V590 Z',BRICK)
    art+=rect(740,265,225,580,SAND,1)+rect(752,277,201,556,PAPER)
    art+=path('M752 277 H953 V467 L752 750 Z',SAND)
    art+=line('M852 277 V834 M752 550 H953',PAPER,12)
    art+=line('M723 866 H980',INK,7)
    return art

def seated(x,y,s=1,color=BRICK,pose='talk',flip=False):
    # Local silhouette faces right; no gender or diagnostic facial coding.
    chair=path('M-143 147 Q-100 114 -67 146 L-49 347 L-139 365 Z',SAND)
    chair+=line('M-125 350 L-140 570 M-39 351 L-12 546',INK,12)
    lower=path('M-52 306 L51 318 L134 415 L102 466 L12 392 L-48 399 Z',INK)
    lower+=path('M107 433 L158 543 L123 559 L70 457 Z',INK)+path('M123 542 L177 551 L189 570 H119 Z',INK)
    torso=path('M-52 89 Q-4 66 55 99 L86 298 Q16 351 -83 309 Z',color)
    head=ellipse(6 if pose=='phone' else 0,7 if pose=='phone' else 0,61,69,INK)
    head+=path('M-22 48 L26 50 L31 103 L-17 105 Z',INK)
    if pose=='phone':
        arms=line('M43 124 Q91 196 157 190',color,53)+line('M148 191 L177 169',BRICK,28)
        arms+=phone(177,136,.63,-17)+line('M-37 132 Q-25 238 111 258',color,49)+line('M104 258 L153 217',BRICK,27)
    elif pose=='busy':
        arms=line('M45 124 Q120 173 169 245',color,52)+line('M160 241 L190 257',BRICK,25)
        arms+=line('M-42 133 Q-71 241 60 276',color,48)+line('M57 277 L96 283',BRICK,28)
        arms+=line('M181 233 L199 288',INK,7)
    elif pose=='listen':
        arms=line('M45 130 Q107 207 156 164',color,53)+line('M151 167 L183 140',BRICK,27)
        arms+=line('M-42 134 Q-67 267 79 293',color,49)+line('M72 293 L113 279',BRICK,28)
    else:
        arms=line('M43 124 Q89 177 147 135',color,52)+line('M140 139 L180 122',BRICK,29)
        arms+=line('M-43 135 Q-66 251 47 272',color,49)+line('M42 273 L87 267',BRICK,27)
    return group(chair+lower+torso+head+arms,x,y,s,flip=flip)

def standing(x,y,s=1,color=BRICK,pose='talk'):
    legs=path('M-57 328 L-16 340 L-19 563 L-61 566 Z',INK)+path('M9 341 L51 328 L86 558 L45 571 Z',INK)
    legs+=path('M-63 554 L-14 557 L6 579 H-76 Z',INK)+path('M44 551 L86 551 L112 577 H40 Z',INK)
    body=path('M-62 91 Q-4 69 55 95 L80 342 Q0 373 -84 336 Z',color)
    body+=ellipse(0,1,62,69,INK)+path('M-22 53 L27 53 L29 103 L-19 103 Z',INK)
    if pose=='down':
        arms=line('M-49 127 Q-90 240 -61 328',color,51)+line('M-57 321 L-34 352',BRICK,27)
        arms+=line('M45 126 Q90 239 45 300',color,51)+line('M46 297 L-7 302',BRICK,28)+notes(-5,332,.66,12)
    else:
        arms=line('M44 127 Q110 179 174 126',color,52)+line('M166 130 L202 115',BRICK,28)
        arms+=line('M-47 129 Q-100 238 -52 290',color,50)+line('M-55 287 L-17 278',BRICK,29)+notes(-19,272,.65,-7)
    return group(legs+body+arms,x,y,s)

def clock(x,y,s=1):
    art=ellipse(0,0,99,99,INK)+ellipse(0,0,89,89,PAPER)
    for xx,yy in ((0,-68),(68,0),(0,68),(-68,0)):
        art+=ellipse(xx,yy,5,5,INK)
    art+=line('M0 0 L0 -44 M0 0 L42 24',INK,9)+ellipse(0,0,8,8,BRICK)
    return group(art,x,y,s)

def scene_art(n):
    art=room(door=n in (1,9))
    if n==1:
        art+=seated(841,817,.88,INK,'phone',True)
        art+=standing(418,623,1.12)
        art+=path('M287 1075 Q282 1015 309 1006 L365 1015 L371 1174 L291 1171 Z',INK)
        art+=line('M300 1017 Q301 969 341 1010',INK,9)
    elif n==2:
        art+=standing(449,553,1.37)
        art+=path('M970 831 Q813 835 795 1009 L786 1430 H1080 Z',INK)
    elif n==3:
        art=room()+seated(664,652,1.34,INK,'phone',True)
        art+=path('M0 846 Q104 801 180 870 L260 1377 H0 Z',BRICK)
    elif n==4:
        art=rect(0,0,1080,1920,PAPER)+rect(755,228,208,503,INK)+line('M860 229 V731 M755 495 H963',PAPER,12)
        art+=seated(350,653,1.24,BRICK,'busy')
        art+=rect(122,1127,860,47,INK,5)+line('M164 1174 L138 1422 M932 1174 L958 1422',INK,15)
        art+=path('M603 895 L866 932 L841 1124 L587 1085 Z',SAND,INK,8)
        art+=path('M587 1085 L841 1124 L884 1140 L577 1130 Z',INK)
        art+=notes(489,1147,.77,-4)+line('M286 1086 V793',INK,13)
        art+=path('M205 806 L267 676 L332 806 Z',BRICK)
    elif n==5:
        art=rect(0,0,1080,1920,PAPER)+rect(160,255,756,618,SAND,3)
        art+=rect(181,278,714,572,PAPER)+rect(224,342,324,25,BRICK,4)
        art+=rect(224,404,549,13,SAND,3)+rect(224,441,425,13,SAND,3)
        art+=rect(582,525,226,229,SAND)+ellipse(695,637,67,67,BRICK)
        art+=standing(464,648,1.12)
        art+=ellipse(236,1251,66,73,INK)+path('M105 1440 Q105 1310 237 1321 Q351 1324 366 1440 Z',INK)
        art+=ellipse(822,1277,70,78,INK)+path('M679 1440 Q695 1348 820 1347 Q942 1345 970 1440 Z',INK)
    elif n==6:
        art=rect(0,0,1080,1920,PAPER)+rect(130,266,822,1090,SAND,2)
        art+=standing(576,604,1.27,pose='down')
        art+=path('M130 266 H310 L130 1356 Z',PAPER)
    elif n==7:
        art=rect(0,0,1080,1920,PAPER)+ellipse(542,1052,370,342,SAND)
        art+=path('M110 1022 L262 910 L438 1020 L389 1105 L210 1038 L110 1130 Z',BRICK)
        art+=path('M970 1103 L815 987 L654 1070 L682 1148 L823 1104 L970 1194 Z',INK)
        art+=path('M390 1010 Q444 964 483 998 Q508 1027 482 1051 L450 1070 L432 1106 L394 1102 Z',BRICK)
        art+=path('M675 1066 Q634 1022 597 1053 Q576 1082 604 1106 L645 1127 L665 1157 L697 1142 Z',BRICK)
        art+=notes(545,918,.95,-13)+cup(539,1190,1.15)
    elif n==8:
        art=room()+seated(292,780,1.0,BRICK,'talk')+seated(816,780,1.0,INK,'listen',True)+table(555,1170,1.0)
        art+=cup(540,1142,.8)
    elif n==9:
        art=room(door=True)+standing(397,631,1.08)+seated(834,793,.95,INK,'listen',True)+table(695,1197,.73)
        art+=phone(666,1177,.55,-55)
    elif n==10:
        art=room()+seated(635,714,1.3,INK,'listen',True)
        art+=path('M0 1096 Q158 999 270 1140 L321 1445 H0 Z',BRICK)
        art+=notes(276,1288,.8,-17)
    elif n==11:
        art=rect(0,0,1080,1920,PAPER)+path('M104 845 L975 628 L975 1420 L104 1420 Z',SAND)
        art+=line('M105 1272 L975 1057',INK,5)
        art+=phone(502,1080,2.2,-16,True)
        art+=path('M930 476 L1040 647 L824 999 L714 947 Z',INK)
        art+=path('M726 929 L692 1010 Q664 1041 631 1002 L599 955 Q581 930 604 910 Q621 895 641 920 L657 939 L680 889 L694 818 Q697 788 720 792 Q743 799 735 832 L729 867 L761 820 Q778 794 798 812 Q814 827 798 853 L761 921 L799 876 Q820 851 840 873 Q854 892 833 914 L770 987 Z',BRICK)
        art+=path('M103 601 L209 568 L315 783 L246 823 Z',BRICK)+path('M246 813 Q262 849 288 843 L327 805 Q345 784 326 767 Q308 754 292 775 L275 793 Z',BRICK)
    elif n==12:
        art=room()+seated(640,683,1.18,INK,'busy',True)
        art+=rect(135,1165,813,40,INK,4)+line('M177 1205 L159 1420 M910 1205 L936 1420',INK,13)
        art+=notes(460,1141,1.03,-8)+phone(775,1146,.47,-67,True)+cup(815,1079,.83)
    elif n==13:
        art=room(wall_art=False)+clock(285,450,1.15)+seated(699,753,1.05,INK,'listen',True)
        art+=table(483,1188,.88)+notes(469,1159,.8,0)+phone(596,1179,.45,-65,True)
    elif n==14:
        art=room()+seated(286,777,1.0,BRICK,'talk')+seated(805,777,1.0,INK,'listen',True)+table(547,1172,.96)
        art+=cup(462,1135,.72)+cup(638,1147,.72)+phone(551,1179,.38,-75,True)+notes(775,1275,.56,-7,True)
    return '<svg class="illustration" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920" aria-hidden="true">'+art+'</svg>'

font_css="""@font-face{font-family:'Newsreader';src:url('../../assets/fonts/newsreader.ttf') format('truetype');font-weight:400;font-style:normal;font-display:block}
@font-face{font-family:'Newsreader';src:url('../../assets/fonts/newsreader-italic.ttf') format('truetype');font-weight:400;font-style:italic;font-display:block}
@font-face{font-family:'DM Sans';src:url('../../assets/fonts/dm-sans.ttf') format('truetype');font-weight:100 900;font-style:normal;font-display:block}"""
frames=[]
start=0
for i,(title,slug,voice,duration) in enumerate(zip(titles,slugs,voices,durations),1):
    ident=f'frame-{i:02d}'
    headline={7:('Ikut senang.',True),8:('Aktif-konstruktif',False),10:('Ceritain.',True)}.get(i)
    label=(f'<p class="emphasis" style="font-style:{"italic" if headline[1] else "normal"};font-size:{88 if i==8 else 122}px">{html.escape(headline[0])}</p>' if headline else '')
    css=font_css+f"\n#{ident}-root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden;background:{PAPER};color:{INK}}}\n#{ident}-root .illustration{{display:block;position:absolute;inset:0;width:100%;height:100%}}\n#{ident}-root .emphasis{{position:absolute;left:116px;top:205px;max-width:846px;margin:0;font-family:'Newsreader';font-weight:400;line-height:1.02;letter-spacing:-.035em;color:{INK}}}"
    page=f'<!doctype html><html lang="id"><head><meta charset="UTF-8"></head><body><template><style>{css}</style><div id="{ident}-root" data-composition-id="{ident}" data-width="1080" data-height="1920" data-duration="{duration}">{scene_art(i)}{label}</div><script>window.__timelines["{ident}"] = gsap.timeline({{paused:true}});</script></template></body></html>'
    rel=f'compositions/frames/{i:02d}-{slug}.html'
    (ROOT/rel).write_text(page,encoding='utf-8')
    frames.append(dict(number=i,id=ident,title=title,src=rel,start=start,end=start+duration,duration=duration,poster=start+duration/2,voiceover=voice,purpose=purposes[i-1],action=actions[i-1],caption=captions[i-1],type=types[i-1],beat=beats[i-1]))
    start+=duration

caption_css=font_css.replace('../../assets/','../assets/')+f"\n#captions-root{{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}}\n#captions-root .caption{{position:absolute;left:112px;right:160px;top:1510px;bottom:auto;width:auto;height:150px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'DM Sans';font-size:48px;font-weight:500;line-height:1.22;color:{INK};text-align:center}}\n#captions-root .caption span{{display:block;background:{PAPER};padding:4px 16px;max-width:100%;border-radius:5px}}"
caption_rows=''.join(f'<div id="caption-{f["number"]:02d}" class="caption clip" data-start="{f["start"]}" data-duration="{f["duration"]}">'+''.join(f'<span>{html.escape(t)}</span>' for t in f['caption'])+'</div>' for f in frames)
(ROOT/'compositions/captions.html').write_text(f'<!doctype html><html lang="id"><head><meta charset="UTF-8"></head><body><template><style>{caption_css}</style><div id="captions-root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="90">{caption_rows}</div><script>window.__timelines["captions"] = gsap.timeline({{paused:true}});</script></template></body></html>',encoding='utf-8')
hosts='\n'.join(f'<div id="host-{f["id"]}" class="clip" data-composition-id="{f["id"]}" data-composition-src="{f["src"]}" data-start="{f["start"]}" data-duration="{f["duration"]}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>' for f in frames)
hosts+='<div id="host-captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="90" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:30"></div>'
(ROOT/'index.html').write_text(f'''<!doctype html><html lang="id" data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080,height=1920"><title>Kabar baik disambut datar — storyboard v1</title><script src="assets/vendor/gsap.min.js"></script><style>*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:{PAPER}}}#root{{position:relative;width:100%;height:100%;overflow:hidden}}.clip{{position:absolute;inset:0;width:100%;height:100%}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1080" data-height="1920">{hosts}</div><script>window.__timelines["main"]=gsap.timeline({{paused:true}});</script></body></html>''',encoding='utf-8')

story='''---
format: 1080x1920
duration: 90s
message: "Kabar baik dapat diberi ruang untuk dinikmati bersama lewat perhatian dan rasa ingin tahu terhadap cerita pasangan."
arc: story-explainer
audience: orang dewasa yang merefleksikan hubungan romantis
mode: collaborative
music: none
board: ruang-di-antara-v2
layout_review: awaiting_review
---

# Storyboard visual v1 — Kabar baik disambut datar

Naskah v1, 175 kata, disetujui pengguna pada 18 Oktober 2026 melalui “cocok”. Empat belas shot ini memperinci enam beat editorial yang diterima; narasi dipertahankan. Timing estimasi total 90 detik. Status built berarti pose statis tersedia untuk review, bukan layout sudah diterima pengguna. Belum ada animasi atau audio.

## Video direction

Satu rumah sebagai jangkar; A berbaju bata di kiri, B berbaju arang di kanan. Kedua warna netral secara moral dan tidak mengodekan gender. Kilas balik mempertahankan pakaian A. Variasi shot: ruang, medium, close-up HP/tangan, kilas balik latihan, situasi presentasi, overhead meja, lalu percakapan yang berlanjut. Setiap shot memberi konteks, gestur, atau keadaan baru. Tiga teks penekanan maksimal 0–5 kata; subtitle contoh pada satu track tersendiri. Tidak ada foto/footage. Lihat frame.md untuk token dan area subtitle.

Rencana gerak berikut adalah catatan untuk tahap selanjutnya: masuk/menoleh, tangan yang tertahan, HP yang diletakkan, dan orientasi tubuh yang berubah. Semua pose saat ini statis. Tidak menambah motion atau efek sebelum review layout.

'''
script='''# SCRIPT — kabar-baik-disambut-datar

**Status:** approved narration v1; per-shot timing is an estimate, layout awaits review.
**Voice:** belum dipilih untuk episode ini; tidak ada sintesis pada tahap storyboard.
**Voice settings:** belum ditentukan.
**Voice direction:** Satu narator, Indonesia register lo–gua, dekat dan observatif. Dialog hangat, jeda singkat pada cerita yang tertahan. Jangan mengubah teks yang sudah disetujui.

'''
for f in frames:
    act='Kejadian' if f['number']<=3 else 'Pengalaman batin' if f['number']<=6 else 'Konsep dan respons' if f['number']<=11 else 'Konteks dan tindak lanjut'
    story+=f'''## Frame {f['number']} — {f['title']} ({f['start']}–{f['end']}s)

- act: {act}
- scene: {f['action']}
- duration: {f['duration']}s
- poster: {f['duration']/2}s
- transition_in: cut
- status: outline
- src: {f['src']}
- type: {f['type']}
- persuasion: Concretization + demonstration
- beat: {f['beat']}
- voiceover: {json.dumps(f['voiceover'],ensure_ascii=False)}
- layout_review: awaiting_review

narrativeRole: {f['purpose']}
keyMessage: {f['purpose']}
Visual: {f['action']}
Teks penekanan: { {7:'Ikut senang.',8:'Aktif-konstruktif',10:'Ceritain.'}.get(f['number'],'tidak ada') }
Ruang subtitle: y=1510–1660, satu atau dua baris pendek, terpisah dari tindakan utama.
Medium: ilustrasi SVG.

'''
    script+=f'''## Line {f['number']} — {f['title']} (Frame {f['number']})

**Time:** {f['start']} – {f['end']}s
**Delivery:** {'Hangat dan penasaran.' if f['number'] in (1,2,9,10,11,14) else 'Observatif, beri ruang pada akhir frasa.'}

    {f['voiceover']}

'''
(ROOT/'STORYBOARD.md').write_text(story,encoding='utf-8')
(ROOT/'SCRIPT.md').write_text(script,encoding='utf-8')
(ROOT/'assets/approved-narration.txt').write_text('\n\n'.join(paragraphs)+'\n',encoding='utf-8')
(ROOT/'capture/extracted/visible-text.txt').write_text('Pilihan pengguna: 4\nPersetujuan naskah: cocok\nTopik yang dipilih: Lo bawa kabar baik. Dia cuma jawab, Oh, bagus.\n\nNarasi v1 yang disetujui:\n\n'+'\n\n'.join(paragraphs),encoding='utf-8')
(ROOT/'capture/extracted/tokens.json').write_text(json.dumps(dict(title='Kabar baik disambut datar',description='Ikut hadir dalam kebahagiaan pasangan',colors=[PAPER,INK,BRICK,SAND],fonts=['Newsreader','DM Sans']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'boards/frames.json').write_text(json.dumps(frames,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'assets/SOURCES.md').write_text('''# Provenance aset storyboard v1

- Seluruh ilustrasi SVG: dibuat khusus untuk episode dari skenario narasi yang disetujui; bentuk dan gestur mengikuti board ruang-di-antara v2. Tidak berasal dari foto, stok, atau temuan penelitian.
- Font lokal disalin dari boards/ruang-di-antara/assets/: Newsreader regular/italic dan DM Sans. Lisensi OFL ikut disalin ke assets/fonts/.
- GSAP 3.14.2: https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js, disimpan lokal di assets/vendor/gsap.min.js; header lisensi asli dipertahankan.
- Bukti klaim dan batas penjelasan: ../SOURCES.md pada folder produksi.
''',encoding='utf-8')
print(json.dumps(dict(frames=len(frames),duration=start,narration_words=len(' '.join(voices).split()),snapshot_at=','.join(str(f['poster']).rstrip('0').rstrip('.') if '.' in str(f['poster']) else str(f['poster']) for f in frames)),ensure_ascii=False))
