from PIL import Image,ImageDraw
from pathlib import Path
import json
V=Path(__file__).resolve().parent
plan=json.loads((V/'scene-plan.json').read_text(encoding='utf-8'))
for part in range(3):
    sheet=Image.new('RGB',(1000,4*495),(248,244,232));d=ImageDraw.Draw(sheet)
    for row,s in enumerate(plan[part*4:part*4+4]):
        y=row*495;d.text((12,y+5),s['id']+' / sequential motion samples without captions',fill='#173B42')
        for col,u in enumerate([8,38,66,94]):
            im=Image.open(V/f'verification/world/{s["id"]}-{u}.png').convert('RGB');im.thumbnail((240,445));sheet.paste(im,(col*250,y+28))
    sheet.save(V/f'verification/world/motion-strip-{part+1}.jpg',quality=92)
