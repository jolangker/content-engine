"""Export the static style board. Requires Playwright Python and its Chromium."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parent
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1100}, device_scale_factor=1)
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto((root / "style-board.html").as_uri(), wait_until="load")
    page.evaluate("document.fonts.ready")
    fonts = page.evaluate("""() => ({
        newsreader: document.fonts.check('400 40px Newsreader'),
        newsreaderItalic: document.fonts.check('italic 400 40px Newsreader'),
        dmSans: document.fonts.check('400 20px "DM Sans"'),
        faces: [...document.fonts].map(f => ({family:f.family,status:f.status}))
    })""")
    if not all(fonts[k] for k in ("newsreader", "newsreaderItalic", "dmSans")):
        raise RuntimeError(f"Fonts did not load: {fonts}")
    overflow = page.evaluate("""() => [...document.querySelectorAll('h1,h2,h3,p,.frame,.frame-footer')]
        .filter(e=>e.scrollWidth>e.clientWidth+2 || e.scrollHeight>e.clientHeight+2)
        .map(e=>({element:e.tagName, className:e.className, text:e.textContent.slice(0,90)}))""")
    if errors or overflow:
        raise RuntimeError(json.dumps({"pageErrors":errors,"overflow":overflow}))
    height = page.evaluate("Math.ceil(document.querySelector('main').getBoundingClientRect().height)")
    page.screenshot(path=root / "style-board.png", full_page=True)
    for index, frame in enumerate(page.locator('.frame').all(), start=1):
        frame.screenshot(path=root / f"study-{index:02d}.png")
    # Dynamic page height keeps the export on a single sheet after typography edits.
    page.add_style_tag(content=f"@page {{ size: 1600px {height}px; margin: 0; }}")
    page.pdf(path=root / "style-board.pdf", print_background=True, prefer_css_page_size=True)
    print(json.dumps({"width":1600,"height":height,"fonts":fonts,"overflow":overflow,"pageErrors":errors}))
    browser.close()
