from pathlib import Path
from playwright.sync_api import sync_playwright
import json,html
V=Path(__file__).resolve().parent; B=V/'boards';S=json.loads((V/('timing.json' if (V/'timing.json').exists() else 'scene-plan.json')).read_text(encoding='utf-8'))['scenes']
imgs=sorted((B/'stills').glob('frame-*.png'))
assert len(imgs)==len(S)==16
cards=''
for s,img in zip(S,imgs):
    cards+=f'<div class="frame"><img src="stills/{img.name}"><div class="title">{s["number"]:02}: {html.escape(s["title"])}</div><div class="time">{s["start"]:.1f} to {s["start"]+s["duration"]:.1f}s</div><p>{html.escape(s["subtitle"])}</p></div>'
(B/'storyboard.html').write_text(f'''<!doctype html><html><meta charset="utf-8"><style>*{{box-sizing:border-box}}body{{margin:0;background:#ECEEE9;padding:32px;font-family:Arial,sans-serif;color:#172B3B}}h1{{font-size:34px;margin:0 0 12px}}.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:24px}}.frame{{background:#fff;border-radius:14px;overflow:hidden}}img{{width:100%;display:block}}.title{{font-size:21px;font-weight:bold;padding:14px 14px 5px}}.time,p{{margin:0;padding:0 14px 10px;font-size:17px}}</style><h1>Di Balik Benda — Silinder kunci</h1><p>16 shots · 90 seconds · Static layout plan · Agent verification under delegated automation</p><div class="grid">{cards}</div></html>''',encoding='utf-8')
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1600,'height':1000},device_scale_factor=1)
    page.goto((B/'storyboard.html').as_uri());page.evaluate('document.fonts.ready');page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
    assert page.locator('.frame').count()==16
    page.screenshot(path=str(B/'storyboard.png'),full_page=True)
    report=dict(count=16,all_images_loaded=True,size=page.evaluate('({width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})'),server='none; local file browser closed')
    browser.close()
(V/'verification').mkdir(exist_ok=True)
(V/'verification/storyboard.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report)
