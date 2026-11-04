"""Recheck changed carry motion, final title bounds, and storyboard arrival pose."""
from pathlib import Path
import json,shutil,subprocess
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification';ts=json.loads((V/'timing.json').read_text(encoding='utf-8'))['scenes'];s=ts[13]
times=[s['start']+s['duration']*f for f in (.08,.34,.63,.77,.86,.94)]+[ts[15]['start']+1]
r=subprocess.run([shutil.which('npx.cmd'),'--yes','hyperframes@0.9.1','snapshot','--at',','.join(f'{t:.8f}' for t in times),'--no-end','--describe','false','-o','verification/carry-repair'],cwd=V,capture_output=True,text=True,encoding='utf-8');(Q/'carry-repair.log').write_text(r.stdout+'\n'+r.stderr,encoding='utf-8');r.check_returncode()
files=sorted((Q/'carry-repair').glob('frame-*.png'));assert len(files)==7
sheet=Image.new('RGB',(1440,2*680),'#e7e1d8');draw=ImageDraw.Draw(sheet)
for n,f in enumerate(files):
    im=Image.open(f).convert('RGB');im.thumbnail((344,612));x=n%4*360+8;y=n//4*680+24;sheet.paste(im,(x,y));draw.text((x,y+620),f'{times[n]:.3f}s',fill='#302B28')
sheet.save(Q/'carry-repair.png')
stills=sorted((V/'boards/stills').glob('frame-*.png'));shutil.copy2(files[5],stills[13])
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True);page=browser.new_page(viewport=dict(width=1600,height=1000));page.goto('http://127.0.0.1:3003/#project/video');page.wait_for_timeout(2500);f=page.frames[1];f.wait_for_function('window.__player && window.__renderReady');f.evaluate('window.__player.pause()')
    def state(t):
        f.evaluate('(t)=>window.__player.seek(t)',t);page.wait_for_timeout(120)
        return f.evaluate('''()=>[...document.querySelectorAll('#f14 svg g[id^="f14-"]')].map(e=>({id:e.id,transform:e.getAttribute('transform'),opacity:getComputedStyle(e).opacity}))''')
    forward={t:state(t) for t in times[:6]};reverse={t:state(t) for t in reversed(times[:6])};assert forward==reverse
    f.evaluate('(t)=>window.__player.seek(t)',times[-1]);page.wait_for_timeout(120)
    title=f.evaluate('''()=>{const e=document.querySelector('#f16-heading'),r=document.createRange();r.selectNodeContents(e);const boxes=[...r.getClientRects()].map(x=>({x:x.x,y:x.y,width:x.width,height:x.height}));const box=e.getBoundingClientRect();return {text:e.textContent,container:{x:box.x,y:box.y,width:box.width,height:box.height},glyph_boxes:boxes,scroll:e.scrollWidth,width:e.clientWidth}}''')
    assert title['scroll']<=title['width'] and len(title['glyph_boxes'])>=2
    browser.close()
receipt=dict(seek_consistency=True,phase_times=times[:6],title=title,title_clipping_observed=False,storyboard_f14_updated=True,source='actual mounted player plus HyperFrames snapshots')
(Q/'carry-repair.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt))
