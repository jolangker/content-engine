"""Verify and capture the entire static storyboard, without a server."""
from pathlib import Path
import html
import json
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parent;V=P/'video';B=V/'boards'
lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));times=json.loads((V/'scene_schedule.json').read_text(encoding='utf-8'));stills=sorted((B/'stills').glob('frame-*.png'));assert len(stills)==len(lines)==16
cards=[]
for x,t,f in zip(lines,times,stills):cards.append(f'<div class="frame"><img src="stills/{f.name}" alt="Frame {x["id"]:02d}"><div class="title">{x["id"]:02d}: {html.escape(x["title"])}</div><div class="time">{t["start"]:.2f}–{t["end"]:.2f}s · {"charcoal" if x["dramatic"] else "cream"}</div><p class="words">{html.escape(x["text"])}</p></div>')
page='''<!doctype html><html lang="en"><head><meta charset="UTF-8"><style>*{box-sizing:border-box}body{margin:0;padding:44px;background:#e7e1d8;color:#302B28;font:16px/1.45 Arial,sans-serif}h1{font-size:34px;margin:6px 0 12px}.intro{margin:0 0 28px;max-width:1080px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;align-items:start}.frame{background:#fffaf3;border:1px solid #d8c8b5;border-radius:10px;padding:12px;overflow:hidden}.frame img{width:100%;height:auto;display:block}.title{font-size:16px;font-weight:700;margin:14px 0 6px}.time{font-size:13px;color:#5d5147}.words{font-size:14px;margin:8px 0 2px;min-height:84px}.eyebrow{text-transform:uppercase;letter-spacing:.12em;font-size:12px}footer{margin-top:26px;font-size:13px}</style></head><body><div class="eyebrow">Ruang di Antara · storyboard v1 · 16 scenes</div><h1>Terima kasih yang melihat</h1><p class="intro">Static scene poses before narration synthesis and animation. Agent-selected topic and Hook 1 under immediate automation. Editorial v1.3 / visual v1.2. Exactly two charcoal turns: 08 and 10. Captions are script excerpts; timings are estimates.</p><main class="grid">'''+''.join(cards)+'''</main><footer>Agent layout review, no human approval claimed. Source boundaries: ../../SOURCES.md. Target approximately 90 seconds.</footer></body></html>'''
(B/'storyboard.html').write_text(page,encoding='utf-8')
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    try:
        tab=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1);tab.goto((B/'storyboard.html').as_uri(),wait_until='load');tab.evaluate('document.fonts.ready');tab.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
        result=tab.evaluate('''()=>({count:document.querySelectorAll('.frame').length,images:[...document.images].map(i=>({src:i.getAttribute('src'),w:i.naturalWidth,h:i.naturalHeight})),width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})''')
        assert result['count']==16 and all(i['w']==1080 and i['h']==1920 for i in result['images']);tab.screenshot(path=str(B/'storyboard.png'),full_page=True);(B/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:result[k] for k in ('count','width','height')}))
    finally:browser.close()
