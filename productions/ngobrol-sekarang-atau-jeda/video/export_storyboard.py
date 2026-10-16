"""Package posed stills for visual review; this does not render an animated film."""
from pathlib import Path
import json, html
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent
frames=json.loads((root/'boards/frame-manifest.json').read_text(encoding='utf-8'))
cards=[]
for f in frames:
    filename=f"frame-{f['n']-1:02d}-at-{f['poster']}s.png"
    assert (root/'boards/stills'/filename).stat().st_size > 10000
    cards.append(f'''<article class="frame"><img src="stills/{filename}" alt="Adegan {f['n']}: {html.escape(f['title'])}"><div class="copy"><div class="title">{f['n']:02d}: {html.escape(f['title'])}</div><div class="time">{f['start']:.1f} to {f['start']+f['duration']:.1f}s</div><p class="words">{html.escape(f['role'])}</p><details><summary>Narasi adegan</summary><p>{html.escape(f['vo'])}</p></details></div></article>''')
page='''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Storyboard 01 — Ngobrol sekarang atau jeda</title><style>
*{box-sizing:border-box}body{margin:0;background:#f2f1ee;color:#302B28;font-family:Arial,system-ui,sans-serif}main{max-width:1600px;margin:auto;padding:48px 50px 45px}header{border-bottom:1px solid #c8b9a8;padding-bottom:25px;margin-bottom:32px;display:flex;gap:30px;justify-content:space-between;align-items:flex-end}h1{font-size:39px;font-weight:500;letter-spacing:-1.2px;margin:12px 0}p{margin:0;line-height:1.5}.kicker{font-size:12px;text-transform:uppercase;letter-spacing:2px}.intro{max-width:680px;font-size:15px}.status{font-size:13px;line-height:1.65;max-width:260px;text-align:right}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:30px}.frame{overflow:hidden;border-radius:12px;background:#fff;border:1px solid #ded9d1;align-self:start}.frame img{width:100%;height:auto;display:block;aspect-ratio:9/16}.copy{padding:20px 22px 22px}.title{font-size:19px;font-weight:600;line-height:1.3}.time{margin:8px 0 12px;font-size:12px;letter-spacing:1px;color:#6e625b}.words{font-size:14px;min-height:43px}details{font-size:13px;margin-top:14px}details p{padding-top:12px}summary{cursor:pointer}footer{border-top:1px solid #c8b9a8;padding-top:20px;margin-top:30px;font-size:13px;display:flex;justify-content:space-between;gap:30px}@media(max-width:900px){main{padding:24px}.grid{grid-template-columns:repeat(2,minmax(0,1fr))}header{display:block}.status{text-align:left;margin-top:20px}}@media(max-width:560px){.grid{grid-template-columns:1fr}h1{font-size:31px}footer{display:block}}
</style></head><body><main data-composition-id="storyboard-review" data-no-timeline data-width="1600" data-height="2423" data-duration="1"><header><div><div class="kicker">Ruang di Antara / Storyboard 01</div><h1>Ngobrol sekarang atau jeda</h1><p class="intro">Dari urutan mendesak–menjauh ke jeda dengan rencana kembali. Enam pose statis dengan warna dan tipografi final sebagai dasar animasi.</p></div><p class="status">Naskah v1 disetujui<br>Storyboard v1 menunggu tinjauan<br>9:16 · estimasi 65 detik</p></header><section class="grid">'''+''.join(cards)+'''</section><footer><span>Yang ditinjau: layout, teks layar, dua karakter, dan kejelasan alur.</span><span>Timing perkiraan · audio & animasi belum dibuat</span></footer></main></body></html>'''
(root/'boards/storyboard.html').write_text(page,encoding='utf-8')
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    tab=browser.new_page(viewport={'width':1600,'height':1000},device_scale_factor=1)
    errors=[]
    tab.on('pageerror', lambda err:errors.append(str(err)))
    tab.goto((root/'boards/storyboard.html').as_uri(),wait_until='load')
    assert tab.locator('.frame').count()==6
    imgs=tab.locator('.frame img').evaluate_all('(els)=>els.map(e=>({loaded:e.complete&&e.naturalWidth===1080,height:e.naturalHeight}))')
    assert all(im['loaded'] and im['height']==1920 for im in imgs),imgs
    overflow=tab.locator('.title,.time,.words').evaluate_all('(els)=>els.filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>e.textContent)')
    assert not errors and not overflow, {'errors':errors,'overflow':overflow}
    tab.screenshot(path=str(root/'boards/storyboard.png'),full_page=True)
    result={'board_frames':6,'stills':imgs,'board_page_errors':errors,'board_text_overflow':overflow,'narration_unchanged':True,'inspection':'Six 1080x1920 stills inspected visually; frame 3 loop rerouted to clear label text. Static storyboard only; no animation or AV verification claimed.'}
    (root/'boards/verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
    browser.close()
