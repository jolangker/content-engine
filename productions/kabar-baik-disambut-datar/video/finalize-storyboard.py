"""Package captured stills into the review board, preserving their pixels."""
from pathlib import Path
import json
import html
import math
import re
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
frames=json.loads((ROOT/'boards/frames.json').read_text(encoding='utf-8'))
stills=sorted((ROOT/'boards/stills').glob('frame-*-at-*.png'))
if len(stills)!=14 or len(frames)!=14:
    raise RuntimeError('All fourteen mounted shots must be captured before packaging')
for frame,still in zip(frames,stills):
    with Image.open(still) as source:
        if source.size!=(1080,1920):
            raise RuntimeError('Unexpected still resolution: '+still.name)
    frame['still']='stills/'+still.name
    frame['status']='built'

cards=[]
for f in frames:
    title=f'{f["number"]:02d}: {f["title"]}'
    cards.append(f'''<article class="frame" id="shot-{f['number']:02d}">
    <a class="still-link" href="{f['still']}" target="_blank" aria-label="Perbesar shot {f['number']}: {html.escape(f['title'])}"><img src="{f['still']}" width="1080" height="1920" alt="{html.escape(f['action'])}"></a>
    <div class="copy"><h2 class="title">{html.escape(title)}</h2>
    <p class="time">{f['start']}–{f['end']} detik · {f['duration']} detik</p>
    <p class="words">{html.escape(f['voiceover'])}</p>
    <p class="purpose">{html.escape(f['purpose'])}</p></div></article>''')
page='''<!doctype html><html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kabar baik disambut datar — Storyboard v1</title><style>
*{box-sizing:border-box}body{margin:0;background:#f5f2ec;color:#302b28;font-family:system-ui,-apple-system,'Segoe UI',sans-serif}main{max-width:1640px;margin:auto;padding:44px 30px 64px}header{padding-bottom:30px;margin-bottom:30px;border-bottom:1px solid #d8c8b5}.eyebrow{font-size:12px;font-weight:650;letter-spacing:.14em;text-transform:uppercase;color:#a34f3f}h1{font-size:clamp(30px,3.5vw,52px);line-height:1.12;letter-spacing:-.04em;margin:14px 0 16px}.meta{display:flex;gap:10px;flex-wrap:wrap}.meta span{border:1px solid #d8c8b5;padding:7px 11px;border-radius:30px;font-size:12px}.intro{max-width:820px;font-size:15px;line-height:1.6;margin:18px 0 0}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:25px;align-items:start}.frame{overflow:hidden;border:1px solid #ded5ca;border-radius:16px;background:#fffdf9;box-shadow:0 4px 14px #302b2806}.still-link{display:block;background:#f3ede3}.frame img{display:block;width:100%;height:auto;aspect-ratio:9/16}.copy{padding:17px 17px 20px}.title{font-size:16px;line-height:1.3;margin:0}.time{font-size:12px;color:#725548;margin:8px 0 14px}.words{font-size:13px;line-height:1.6;margin:0}.purpose{font-size:12px;line-height:1.5;color:#725548;border-top:1px solid #eee6dd;margin:16px 0 0;padding-top:12px}footer{border-top:1px solid #d8c8b5;padding-top:22px;margin-top:35px;font-size:13px;line-height:1.65}a{color:inherit;text-underline-offset:3px}a:focus-visible{outline:3px solid #a34f3f;outline-offset:4px}@media(max-width:1100px){.grid{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:760px){main{padding:26px 18px 44px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.copy{padding:13px}.title{font-size:14px}}@media(max-width:430px){.grid{grid-template-columns:1fr}.frame{max-width:370px;margin:auto}}
</style></head><body><main><header><div class="eyebrow">Ruang di Antara / episode baru</div><h1>Kabar baik disambut datar</h1><div class="meta"><span>Storyboard v1</span><span>14 shot</span><span>90 detik · estimasi</span><span>9:16</span><span>Review layout</span></div><p class="intro">Dari cerita yang tertahan, menuju percakapan yang mendapat tempat. Naskah v1 sudah disetujui. Setiap gambar memperlihatkan satu pose utama; ketuk gambar untuk membukanya pada ukuran penuh. Gerak dan audio dibuat setelah storyboard diterima.</p></header><section class="grid" aria-label="Empat belas shot dalam urutan cerita">'''+''.join(cards)+'''</section><footer><strong>Yang ditinjau:</strong> urutan adegan, framing, ilustrasi, teks penekanan, dan ruang subtitle. Subtitle pada gambar adalah contoh potongan frasa; timing akhir mengikuti narasi yang akan dibuat.<br><a href="storyboard.png" target="_blank">Buka ringkasan semua shot</a> · <a href="../STORYBOARD.md">Rencana adegan</a></footer></main></body></html>'''
(ROOT/'boards/storyboard.html').write_text(page,encoding='utf-8')
(ROOT/'boards/frames.json').write_text(json.dumps(frames,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
story=(ROOT/'STORYBOARD.md').read_text(encoding='utf-8')
story=story.replace('- status: outline','- status: built')
(ROOT/'STORYBOARD.md').write_text(story,encoding='utf-8')

paper,ink,brick,sand='#F3EDE3','#302B28','#A34F3F','#D8C8B5'
display=ImageFont.truetype(str(ROOT/'assets/fonts/newsreader.ttf'),64)
title_font=ImageFont.truetype(str(ROOT/'assets/fonts/dm-sans.ttf'),23)
small_font=ImageFont.truetype(str(ROOT/'assets/fonts/dm-sans.ttf'),19)
meta_font=ImageFont.truetype(str(ROOT/'assets/fonts/dm-sans.ttf'),25)
W=1760
margin=50
gap=24
card_w=(W-2*margin-3*gap)//4
image_w=card_w-2
image_h=round(image_w*1920/1080)
card_h=image_h+103
top=228
H=top+4*(card_h+gap)+78
sheet=Image.new('RGB',(W,H),paper)
draw=ImageDraw.Draw(sheet)
draw.text((margin,35),'RUANG DI ANTARA / STORYBOARD V1',font=small_font,fill=brick)
draw.text((margin,70),'Kabar baik disambut datar',font=display,fill=ink)
draw.text((margin,153),'14 shot  ·  90 detik (estimasi)  ·  9:16  ·  review layout',font=meta_font,fill=ink)
draw.line((margin,204,W-margin,204),fill=sand,width=2)

def fit_line(text,font,width):
    if draw.textlength(text,font=font)<=width:
        return text
    while text and draw.textlength(text+'…',font=font)>width:
        text=text[:-1]
    return text+'…'

for i,(f,still) in enumerate(zip(frames,stills)):
    col,row=i%4,i//4
    x,y=margin+col*(card_w+gap),top+row*(card_h+gap)
    draw.rounded_rectangle((x,y,x+card_w,y+card_h),radius=12,fill='#FFFDFA',outline=sand,width=1)
    with Image.open(still) as source:
        resized=source.convert('RGB').resize((image_w,image_h),Image.Resampling.LANCZOS)
        sheet.paste(resized,(x+1,y+1))
    draw.text((x+14,y+image_h+15),fit_line(f'{f["number"]:02d}  {f["title"]}',title_font,card_w-28),font=title_font,fill=ink)
    draw.text((x+14,y+image_h+55),f'{f["start"]}–{f["end"]} detik · {f["duration"]} detik',font=small_font,fill=brick)
draw.text((margin,H-48),'Naskah v1 disetujui · Seluruh pose statis · Layout menunggu review',font=small_font,fill=ink)
sheet.save(ROOT/'boards/storyboard.png',optimize=True)
print(json.dumps(dict(board='boards/storyboard.html',image='boards/storyboard.png',frames=len(frames),duration_estimate=90,word_count=sum(len(f['voiceover'].split()) for f in frames),image_size=sheet.size),ensure_ascii=False))
