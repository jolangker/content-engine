"""Export two reversed editorial studies beside a normal-mode reference."""
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
SOURCE = (ROOT / 'style-board.html').read_text(encoding='utf-8')
styles = re.search(r'<style>(.*?)</style>', SOURCE, re.S).group(1)
articles = re.findall(r'<article class="frame frame-[a-z]".*?</article>', SOURCE, re.S)


def reversed_article(source, label):
    source = source.replace('class="frame ', 'class="frame is-reversed ', 1)
    source = re.sub(r'STUDI [AB]', label, source)
    source = source.replace('shadow-a', 'shadow-a-reversed').replace('shadow-b', 'shadow-b-reversed')
    # Remap only authored illustration surfaces, not a screenshot or real historical scan.
    colors = {'#EAE0D0': '#121110', '#121110': '#EAE0D0', '#1A1816': '#EAE0D0',
              '#1D1B19': '#121110', '#D4A359': '#7C756B', '#7C756B': '#EAE0D0'}
    return re.sub(r'(fill|stroke)="(#[A-Fa-f0-9]{6})"',
                  lambda m: f'{m[1]}="{colors.get(m[2], m[2])}"', source)


studies = [articles[0], reversed_article(articles[0], 'BALIK 01'), reversed_article(articles[1], 'BALIK 02')]
labels = ['Referensi / Mode normal', 'Varian terang / Perbandingan', 'Varian terang / Pembacaan detail']
extra = '''
.frame.is-reversed{background:var(--paper);color:var(--bg)}
.frame.is-reversed .brand,.frame.is-reversed .sample-label,.frame.is-reversed h3{color:var(--bg)}
.frame.is-reversed h3 .mark{color:var(--red)}
.proof-title{font-size:40px;line-height:1.2;margin:30px 0 16px}
.proof-note{font-size:18px;line-height:1.5;max-width:1100px;margin:0 0 30px}
'''
markup = ''.join(f'<div><div class="study-window">{article}</div><div class="study-caption"><b>{label}</b></div></div>'
                 for article, label in zip(studies, labels))
html = f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Berkas Polemik / Uji warna terbalik</title><style>{styles}{extra}</style></head><body><main>
<header class="top"><b>BERKAS POLEMIK / UJI WARNA</b><span class="draft">STUDI STATIS · BUKAN URUTAN EPISODE</span></header>
<h1 class="proof-title">14 adegan gelap. 2 adegan warna terbalik.</h1>
<p class="proof-note">Usulan penempatan: dua momen dramatis sesuai naskah. Manila menjadi latar, karbon menjadi teks. Merah hanya untuk teks besar atau penanda; metadata tetap karbon.</p>
<div class="frames">{markup}</div></main></body></html>'''
(ROOT / 'reversed-studies.html').write_text(html, encoding='utf-8')


def luminance(color):
    v = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    v = [x / 12.92 if x <= .04045 else ((x+.055)/1.055)**2.4 for x in v]
    return sum(x*w for x, w in zip(v, (.2126, .7152, .0722)))


def contrast(a, b):
    x, y = sorted((luminance(a), luminance(b)))
    return (y+.05)/(x+.05)


pairs = {name: contrast(fg, bg) for name, fg, bg in [
    ('carbon_on_paper', '#121110', '#EAE0D0'), ('ink_on_paper', '#1A1816', '#EAE0D0'),
    ('red_on_paper', '#C32822', '#EAE0D0'), ('tape_on_paper', '#D4A359', '#EAE0D0'),
    ('steel_on_paper', '#7C756B', '#EAE0D0')]}
assert pairs['carbon_on_paper'] >= 7
assert pairs['red_on_paper'] >= 3
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width':1600, 'height':1100}, device_scale_factor=1)
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto((ROOT / 'reversed-studies.html').as_uri(), wait_until='load')
    page.evaluate('document.fonts.ready')
    fonts = page.evaluate('() => [...document.fonts].map(f=>({family:f.family,status:f.status}))')
    overflow = page.evaluate('''() => [...document.querySelectorAll('h1,h3,p,.brand,.sample-label')].filter(e=>e.scrollWidth>e.clientWidth+2 || e.scrollHeight>e.clientHeight+2).map(e=>e.textContent.trim())''')
    assert not errors and not overflow and all(f['status']=='loaded' for f in fonts), (errors, overflow, fonts)
    page.screenshot(path=ROOT/'reversed-studies.png', full_page=True)
    for i in range(2):
        native = browser.new_page(viewport={'width':1080,'height':1920}, device_scale_factor=1)
        native.goto((ROOT/'reversed-studies.html').as_uri(), wait_until='load')
        native.evaluate('document.fonts.ready')
        native.evaluate('''i=>{const e=document.querySelectorAll('.is-reversed')[i];e.remove();document.body.replaceChildren(e);e.style.transform='none';document.body.style.margin='0'}''', i)
        native.locator('.frame').screenshot(path=ROOT/f'reversed-study-{i+1:02d}.png')
        native.set_viewport_size({'width':360,'height':640})
        native.add_style_tag(content='.frame{transform:scale(.3333333333)!important;transform-origin:top left}')
        native.screenshot(path=ROOT/f'reversed-phone-{i+1:02d}.png')
        native.close()
    browser.close()
report = {'source_standard':'https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html',
          'ratios_unrounded':pairs, 'normal_text_minimum':4.5, 'large_text_minimum':3,
          'mode_count':{'normal':14,'reversed':2,'total':16},
          'page_errors':errors,'text_overflow':overflow,'fonts':fonts,
          'restriction':'Red on paper for large text only; yellow/steel on paper excluded from essential small text.',
          'inspection':'Pending visual inspection; contrast calculations do not establish video playback readability.'}
(ROOT/'reversed-contrast-QA.json').write_text(json.dumps(report,indent=2)+'\n', encoding='utf-8')
print(json.dumps(report))
