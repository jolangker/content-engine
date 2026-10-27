"""Resolve rounded review timestamps against the exact integer-frame scene clock."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification';T=json.loads((V/'timing.json').read_text(encoding='utf-8'))['scenes'];D=Q/'exact-seams';D.mkdir(exist_ok=True)
rows=[]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True);page=b.new_page(viewport=dict(width=1600,height=1100));page.goto('http://127.0.0.1:3002/#project/video');page.wait_for_timeout(2500);f=page.frames[1];f.wait_for_function('window.__player && window.__renderReady');f.evaluate('window.__player.pause()')
    for n in (6,12,16):
        s=T[n-1];cut=s['start_frame']/30
        for delta in (-1,0,1):
            t=cut+delta/30;f.evaluate('(t)=>window.__player.seek(t)',t);page.wait_for_timeout(160)
            # Source runtime has exact [start,end) scene-host windows; record every visible host.
            states=f.evaluate('''()=>[...document.querySelectorAll('.scene-host')].map(e=>({id:e.id,start:Number(e.dataset.start),display:getComputedStyle(e).display,visibility:getComputedStyle(e).visibility,opacity:getComputedStyle(e).opacity,rect:e.getBoundingClientRect().toJSON()})).filter(e=>e.display!=='none'&&e.visibility!=='hidden'&&Number(e.opacity)>0&&e.rect.width>0)''')
            dest=D/f'f{n:02d}-{delta+1}.png';f.locator('[data-composition-id="main"]').first.screenshot(path=str(dest))
            rows.append(dict(incoming=n,offset_frames=delta,time=t,visible_hosts=states,image=dest.relative_to(V).as_posix()))
    b.close()
sheet=Image.new('RGB',(1080,3*690),'#e7e1d8');draw=ImageDraw.Draw(sheet)
for k,r in enumerate(rows):
    im=Image.open(V/r['image']).convert('RGB');im.thumbnail((344,630));x=k%3*360+8;y=k//3*690+28;sheet.paste(im,(x,y));draw.text((x,y+638),f"F{r['incoming']:02} offset {r['offset_frames']:+d} | {r['time']:.8f}",fill='#302B28')
sheet.save(Q/'exact-seams.png');(Q/'exact-seams.json').write_text(json.dumps(dict(basis='exact integer frame boundary and adjacent frames in mounted preview',samples=rows),indent=2)+'\n',encoding='utf-8')
print(json.dumps([dict(incoming=r['incoming'],offset=r['offset_frames'],time=r['time'],visible=[x['id'] for x in r['visible_hosts']]) for r in rows]))
