from pathlib import Path
import json, html, asyncio
from playwright.async_api import async_playwright
V=Path(__file__).resolve().parent/'video'
async def main():
    scenes=json.loads((V/'scenes.json').read_text(encoding='utf-8'))
    imgs=sorted((V/'boards/stills').glob('frame-*.png'))
    assert len(imgs)==16, len(imgs)
    cards=''
    for s,p in zip(scenes,imgs):
        cards+=f'<div class="frame"><img src="stills/{p.name}" alt="{s["n"]:02}"><div class="title">{s["n"]:02}: {html.escape(s["title"])}</div><div class="time">{s["start"]:.2f} to {s["start"]+s["duration"]:.2f}s</div><p class="words">{html.escape(s["purpose"])}</p></div>'
    doc=f'''<!doctype html><html><head><meta charset="utf-8"><style>*{{box-sizing:border-box}}body{{margin:0;padding:56px;background:#F3EDE3;color:#302B28;font:18px/1.4 system-ui,sans-serif}}h1{{font:52px/1.1 Georgia,serif;margin:0 0 16px}}header{{margin-bottom:36px}}.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:28px 24px}}.frame{{border:1px solid #D8C8B5;border-radius:12px;overflow:hidden;background:#f9f5ee}}img{{width:100%;display:block}}.title,.time,.words{{padding:0 18px}}.title{{font-weight:650;margin-top:18px}}.time{{font-size:16px;color:#695b51;margin-top:6px}}.words{{font-size:16px;margin:12px 0 20px}}</style></head><body><header><div>RUANG DI ANTARA · BOARD v1.2 · EPISODE 03</div><h1>Jeda punya waktu kembali.</h1><div>16 styled poses · 14 cream + 2 charcoal · Agent verification under delegated automation</div></header><main class="grid">{cards}</main></body></html>'''
    (V/'boards/storyboard.html').write_text(doc,encoding='utf-8')
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True)
        page=await browser.new_page(viewport=dict(width=1640,height=1000),device_scale_factor=1)
        await page.goto((V/'boards/storyboard.html').as_uri())
        await page.evaluate('document.fonts.ready')
        await page.wait_for_function('Array.from(document.images).every(x=>x.complete && x.naturalWidth>0)')
        report=await page.evaluate('({frames:document.querySelectorAll(".frame").length,images:[...document.images].map(i=>({w:i.naturalWidth,h:i.naturalHeight,src:i.getAttribute("src")})),width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})')
        assert report['frames']==16 and len(report['images'])==16
        await page.screenshot(path=str(V/'boards/storyboard.png'),full_page=True)
        (V/'boards/verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        await browser.close()
        print(json.dumps(report))
asyncio.run(main())
