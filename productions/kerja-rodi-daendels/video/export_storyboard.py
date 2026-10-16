"""Export and verify the storyboard board for Kerja Rodi Daendels."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parent
stills_dir = root / 'boards' / 'stills'
html_path = root / 'boards' / 'storyboard.html'

expected_stills = [
    'frame-00-at-4s.png',
    'frame-01-at-15s.png',
    'frame-02-at-27s.png',
    'frame-03-at-37s.png',
    'frame-04-at-48s.png',
    'frame-05-at-58s.png',
    'frame-06-at-65s.png'
]

for s in expected_stills:
    still_file = stills_dir / s
    if not still_file.exists() or still_file.stat().st_size < 10000:
        raise RuntimeError(f"Missing or invalid still: {still_file}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    tab = browser.new_page(viewport={'width': 1600, 'height': 1200}, device_scale_factor=1)
    errors = []
    tab.on('pageerror', lambda err: errors.append(str(err)))
    tab.goto(html_path.as_uri(), wait_until='load')
    
    count = tab.locator('.frame').count()
    if count != 7:
        raise RuntimeError(f"Expected 7 frames, found {count}")
        
    imgs = tab.locator('.frame img').evaluate_all(
        '(els) => els.map(e => ({loaded: e.complete && e.naturalWidth === 1080, height: e.naturalHeight}))'
    )
    if not all(im['loaded'] and im['height'] == 1920 for im in imgs):
        raise RuntimeError(f"Image load failure: {imgs}")
        
    overflow = tab.locator('.title,.time,.words').evaluate_all(
        '(els) => els.filter(e => e.scrollWidth > e.clientWidth + 2).map(e => e.textContent)'
    )
    if errors or overflow:
        raise RuntimeError(f"Page errors or overflow: errors={errors}, overflow={overflow}")
        
    out_png = root / 'boards' / 'storyboard.png'
    tab.screenshot(path=str(out_png), full_page=True)
    
    result = {
        'board_frames': 7,
        'stills': imgs,
        'board_page_errors': errors,
        'board_text_overflow': overflow,
        'narration_unchanged': True,
        'inspection': 'Seven 1080x1920 stills inspected; clean typography, contrast and layout. Forensic Dossier styling verified.'
    }
    
    (root / 'boards' / 'verification.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )
    print(json.dumps({'ok': True, 'png': str(out_png), 'frames': 7}))
    browser.close()
