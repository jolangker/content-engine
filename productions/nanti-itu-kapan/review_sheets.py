"""Make portable seam sheets and copy key review evidence out of CLI cache."""
from pathlib import Path
import json,shutil
from PIL import Image,ImageDraw
V=Path(__file__).resolve().parent/'video';Q=V/'verification';d=json.loads((Q/'review-manifest.json').read_text(encoding='utf-8'));s=d['review']['sheets']
for kind in ('beats','phone'):
    for n,f in enumerate(s[kind],1):shutil.copy2(f,Q/f'review-{kind}-{n}.jpg')
for page in range(3):
    images=[]
    for f in s['seams'][page*5:(page+1)*5]:
        im=Image.open(f).convert('RGB');im.thumbnail((1400,760));images.append(im.copy())
    height=sum(im.height+30 for im in images);sheet=Image.new('RGB',(1440,height),'#e7e1d8');draw=ImageDraw.Draw(sheet);y=0
    for n,im in enumerate(images,page*5+1):
        draw.text((15,y+5),f'Seam {n:02d}',fill='#302B28');sheet.paste(im,(20,y+25));y+=im.height+30
    sheet.save(Q/f'preview-seams-{page+1}.jpg')
print('Portable beats, phone and all fifteen seam strips saved.')
