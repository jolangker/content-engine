"""Render the review board and native-size studies; keep all output in this draft."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent


def luminance(value):
    rgb = [int(value[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in rgb]
    return sum(x * weight for x, weight in zip(rgb, (0.2126, 0.7152, 0.0722)))


def contrast(a, b):
    values = sorted((luminance(a), luminance(b)))
    return round((values[1] + 0.05) / (values[0] + 0.05), 2)


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1100}, device_scale_factor=1)
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto((ROOT / "style-board.html").as_uri(), wait_until="load")
    page.evaluate("document.fonts.ready")
    fonts = page.evaluate("""() => [...document.fonts].map(f => ({
        family: f.family, weight: f.weight, style: f.style, status: f.status
    }))""")
    overflow = page.evaluate("""() => [...document.querySelectorAll('main, h1, h2, h3, p, .label, .source, .sample-label, .brand, .bottom-mark')]
      .filter(e => e.scrollWidth > e.clientWidth + 2 || e.scrollHeight > e.clientHeight + 2)
      .map(e => ({tag: e.tagName, class: e.className, text: e.textContent.slice(0, 100)}))""")
    safe_violations = page.evaluate("""() => [...document.querySelectorAll('.frame')].flatMap(frame => {
      const r = frame.getBoundingClientRect();
      return [...frame.querySelectorAll('.brand,.sample-label,h3,.sheet,.annotation,.limit,.source')].flatMap(e => {
        const b = e.getBoundingClientRect();
        const box = {x:(b.left-r.left)/.4,y:(b.top-r.top)/.4,right:(b.right-r.left)/.4,bottom:(b.bottom-r.top)/.4};
        return box.x < 83 || box.y < 159 || box.right > 931 || box.bottom > 1541 ? [{class:e.className, ...box}] : [];
      });
    })""")
    pairs = {
        "paper_on_carbon": contrast("#EAE0D0", "#121110"),
        "ink_on_paper": contrast("#1A1816", "#EAE0D0"),
        "tape_on_carbon": contrast("#D4A359", "#121110"),
        "paper_on_red_large_display_only": contrast("#EAE0D0", "#C32822"),
    }
    contrast_failed = any(ratio < (3.0 if key.endswith("large_display_only") else 4.5) for key, ratio in pairs.items())
    if errors or overflow or safe_violations or any(f["status"] != "loaded" for f in fonts) or contrast_failed:
        raise RuntimeError(json.dumps({"errors": errors, "overflow": overflow, "safe": safe_violations, "fonts": fonts, "contrast": pairs}))
    page.screenshot(path=ROOT / "style-board.png", full_page=True, animations="disabled")
    dimensions = page.evaluate("({width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})")
    # Isolate each existing article, without changing its design or typography.
    for index in range(3):
        study = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        study.goto((ROOT / "style-board.html").as_uri(), wait_until="load")
        study.evaluate("document.fonts.ready")
        study.evaluate("""index => {
          const article = document.querySelectorAll('.frame')[index];
          article.remove();
          document.body.replaceChildren(article);
          article.style.transform = 'none';
          document.body.style.margin = '0';
        }""", index)
        study.locator('.frame').screenshot(path=ROOT / f"study-{index + 1:02d}.png", animations="disabled")
        # Phone-sized render for visual review; independent from the native export.
        if index == 1:
            study.set_viewport_size({"width": 360, "height": 640})
            study.add_style_tag(content=".frame { transform: scale(0.3333333333) !important; transform-origin: top left; }")
            study.screenshot(path=ROOT / "phone-study-02.png", animations="disabled")
        study.close()
    report = {"board": dimensions, "native_studies": "1080x1920", "fonts": fonts,
              "page_errors": errors, "text_overflow": overflow,
              "essential_safe_zone_violations": safe_violations, "text_contrast_ratios": pairs,
              "human_approval": False, "visual_inspection": "Pending; update after inspecting the exported PNGs."}
    (ROOT / "QA.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))
    browser.close()
