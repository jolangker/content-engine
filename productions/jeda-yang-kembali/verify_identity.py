"""Verify canonical series chrome in source and rendered scene-boundary pixels."""
from pathlib import Path
import json
from PIL import Image, ImageChops

P = Path(__file__).resolve().parent
V = P / 'video'
board = P.parents[1] / 'boards/ruang-di-antara'
css = (board / 'components/chrome.css').read_text(encoding='utf-8')
assert (V / 'assets/board/chrome.css').read_text(encoding='utf-8') == css
scenes = json.loads((V / 'timing.json').read_text(encoding='utf-8'))['scenes']
for scene in scenes:
    source = (V / f'compositions/frames/{scene["id"]}.html').read_text(encoding='utf-8')
    assert css in source, scene['id']
    assert source.count('data-board-chrome="header"') == 1
    assert source.count('data-board-chrome="footer"') == 1
    assert f'{scene["number"]:02d} / {len(scenes)}' in source

files = sorted((V / 'verification/v2-chrome').glob('frame-*.png'))
assert len(files) == len(scenes) * 2
expected, results = {}, []
max_delta = 0
for path in files:
    image = Image.open(path).convert('RGB')
    background = image.getpixel((10, 10))
    regions = {}
    for name, rect in {'header': (80, 90, 700, 145), 'footer': (80, 1790, 700, 1850)}.items():
        crop = image.crop(rect)
        mask = ImageChops.difference(crop, Image.new('RGB', crop.size, background)).convert('L').point(lambda n: 255 if n > 35 else 0)
        box = mask.getbbox()
        assert box is not None, (path.name, name)
        absolute = [box[0] + rect[0], box[1] + rect[1], box[2] + rect[0], box[3] + rect[1]]
        expected.setdefault(name, absolute)
        delta = max(abs(a-b) for a,b in zip(absolute, expected[name]))
        # Inverting cream/charcoal shifts the antialiased glyph edge by at most one pixel.
        assert delta <= 1, (path.name, name, absolute, expected[name])
        max_delta = max(max_delta, delta)
        regions[name] = absolute
    results.append({'frame': path.name, 'pixel_bounds': regions})
report = {'ok': True, 'source_scenes': len(scenes), 'sample_count': len(files), 'maximum_pixel_edge_delta': max_delta,
          'scope': 'Every scene start+0.04s and end-0.04s, including dark scene; series label and handle',
          'expected_pixel_bounds': expected, 'results': results}
(V / 'verification/chrome-v2.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({key: value for key,value in report.items() if key != 'results'}))
