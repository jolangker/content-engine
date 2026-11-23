"""Render the draft style board and the thumbnail study; fails on browser errors, missing font or clipped text."""
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

here = Path(__file__).resolve().parent
url = (here / 'style-board.html').as_uri()
with sync_playwright() as p:
    browser = p.chromium.launch()
    errors = []
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('requestfailed', lambda r: errors.append(r.url))
    page.goto(url, wait_until='load')
    page.evaluate('document.fonts.ready')
    qa = page.evaluate('''() => ({font: document.fonts.check('900 24px "DM Sans"'),
      overflow: document.documentElement.scrollWidth > innerWidth,
      clipped: [...document.querySelectorAll('.income-card p, .thumb-panel h2, figcaption, .timeline span')]
        .filter(e => e.scrollWidth > e.clientWidth + 1).map(e => e.textContent)})''')
    if errors or not qa['font'] or qa['overflow'] or qa['clipped']:
        raise SystemExit(f'{errors} {qa}')
    page.screenshot(path=str(here / 'style-board.png'), full_page=True)
    width = page.evaluate("document.querySelector('#thumbnail').parentElement.getBoundingClientRect().width")
    big = browser.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1080 / width)
    big.goto(url, wait_until='load')
    big.evaluate('document.fonts.ready')
    for name, sel in (('thumbnail-study.png', '#thumbnail'), ('income-study.png', '#market')):
        out = here / name
        big.locator(sel).locator('xpath=..').screenshot(path=str(out))
        Image.open(out).convert('RGB').resize((1080, 1920), Image.LANCZOS).save(out)
    phone = browser.new_page(viewport={'width': 390, 'height': 844})
    phone.goto(url, wait_until='load')
    phone.evaluate('document.fonts.ready')
    if phone.evaluate('document.documentElement.scrollWidth > innerWidth'):
        raise SystemExit('horizontal overflow at 390 px')
    phone.screenshot(path=str(here / 'style-board-phone.png'), full_page=True)
    browser.close()
print('ok', qa)
