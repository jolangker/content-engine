"""Inspect the local review page and export its desktop board and overview PNGs."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

PROD=Path(__file__).resolve().parent
VIDEO=PROD/'video'
BOARD=VIDEO/'boards'
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((BOARD/'storyboard.html').as_uri(),wait_until='load')
    page.evaluate('document.fonts.ready')
    images=page.evaluate('''() => [...document.querySelectorAll('.frame img')].map(i=>({loaded:i.complete&&i.naturalWidth===1080&&i.naturalHeight===1920,src:i.getAttribute('src')}))''')
    if len(images)!=14 or not all(i['loaded'] for i in images):
        raise RuntimeError(json.dumps(images))
    desktop_overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth')
    page.locator('details summary').first.click()
    assert page.locator('details').first.get_attribute('open') is not None
    page.locator('details summary').first.click()
    page.screenshot(path=BOARD/'storyboard.png',full_page=True)
    page.set_viewport_size({'width':390,'height':844})
    page.evaluate('scrollTo(0,0)')
    mobile_overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth')
    page.screenshot(path=BOARD/'storyboard-mobile.png',full_page=False)
    page.set_viewport_size({'width':2000,'height':1400})
    page.evaluate('scrollTo(0,0)')
    page.add_style_tag(content='''main{max-width:none;padding:28px 32px}header{max-width:1500px;margin-bottom:22px}h1{font-size:34px;margin-bottom:12px}.intro{font-size:14px;max-width:1200px;margin-bottom:12px}.legend{margin-top:12px}.grid{grid-template-columns:repeat(7,minmax(0,1fr));gap:14px}.card-body{padding:10px 11px 12px}.title{font-size:13px;margin:5px 0 0}.time{font-size:11px}.words,details,footer{display:none}.frame{border-radius:10px}''')
    page.screenshot(path=BOARD/'storyboard-overview.png',full_page=True)
    browser.close()
if errors or desktop_overflow or mobile_overflow:
    raise RuntimeError(json.dumps({'errors':errors,'desktopOverflow':desktop_overflow,'mobileOverflow':mobile_overflow}))
result={'frames':len(images),'allImagesLoaded':True,'desktopViewport':1440,'mobileViewport':390,'horizontalOverflow':False,'narrationDisclosure':'opens and closes','pageErrors':errors}
(BOARD/'page-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
