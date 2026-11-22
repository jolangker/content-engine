"""Determinism and frame-seek verification tests for shortform-board/assets/procedural-kit/mark-making.js."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest


KIT_PATH = Path(__file__).resolve().parents[2] / 'shortform-board' / 'assets' / 'procedural-kit' / 'mark-making.js'


class MarkMakingKitTests(unittest.TestCase):
    def test_node_math_and_stroke_determinism(self):
        js = f"""
        const MarkKit = require({json.dumps(str(KIT_PATH))});
        const pts = [[40, 80], [160, 120], [280, 90], [400, 160]];
        const a1 = MarkKit.svgTaperedPath(pts, {{ seed: 'siphon-pipe', width: 6, progress: 0.65, boilStep: 3 }});
        // Call other random/noise functions in between, then recompute a1: must be bit-identical
        MarkKit.buildWatercolorWash([[0,0],[100,0],[100,100],[0,100]], {{ seed: 99 }});
        const a2 = MarkKit.svgTaperedPath(pts, {{ seed: 'siphon-pipe', width: 6, progress: 0.65, boilStep: 3 }});
        const full = MarkKit.svgTaperedPath(pts, {{ seed: 'siphon-pipe', width: 6, progress: 1.0, boilStep: 3 }});

        // Closed-form spring checks
        const s0 = MarkKit.springAtTime(0, {{ from: 100, to: 200, zeta: 1.0, omega: 15 }});
        const sCritMid = MarkKit.springAtTime(0.25, {{ from: 100, to: 200, zeta: 1.0, omega: 15 }});
        const sUnderPeak = MarkKit.springAtTime(0.22, {{ from: 0, to: 100, zeta: 0.6, omega: 16 }});
        const sEnd = MarkKit.springAtTime(2.0, {{ from: 0, to: 100, zeta: 0.8, omega: 15 }});

        // Logarithmic zoom midpoint of 1x -> 16x at p=0.5 is 4x
        const zoomMid = MarkKit.logZoom(1, 16, 0.5);

        // Explode order: outer index (3 of 4) moves ahead of inner index (0 of 4)
        const expOuter = MarkKit.explodeShareAt(3, 4, 0.25, 'explode', 0.5);
        const expInner = MarkKit.explodeShareAt(0, 4, 0.25, 'explode', 0.5);

        // Part-anchored hatching
        const box = [[20, 20], [120, 20], [120, 100], [20, 100]];
        const h1 = MarkKit.buildAnchoredHatchLines(box, {{ seed: 7, spacing: 10, progress: 1.0 }});
        const h2 = MarkKit.buildAnchoredHatchLines(box, {{ seed: 7, spacing: 10, progress: 1.0 }});

        console.log(JSON.stringify({{
          identicalStroke: a1 === a2 && a1.length > 40,
          fullLonger: full.length > a1.length,
          s0, sCritNoOvershoot: sCritMid <= 200.0001 && sCritMid > 150,
          sUnderOvershoots: sUnderPeak > 100,
          sEndSettled: Math.abs(sEnd - 100) < 0.05,
          zoomMid,
          explodeOrderOk: expOuter > expInner,
          hatchIdentical: JSON.stringify(h1) === JSON.stringify(h2) && h1.length >= 5
        }}));
        """
        proc = subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True)
        res = json.loads(proc.stdout.strip())
        self.assertTrue(res['identicalStroke'])
        self.assertTrue(res['fullLonger'])
        self.assertEqual(res['s0'], 100)
        self.assertTrue(res['sCritNoOvershoot'])
        self.assertTrue(res['sUnderOvershoots'])
        self.assertTrue(res['sEndSettled'])
        self.assertAlmostEqual(res['zoomMid'], 4.0, places=6)
        self.assertTrue(res['explodeOrderOk'])
        self.assertTrue(res['hatchIdentical'])

    def test_playwright_canvas_backward_seek_pixel_identical(self):
        from playwright.sync_api import sync_playwright

        html = f"""<!doctype html>
        <html><body style="margin:0;background:#F6F1DD;">
        <canvas id="c" width="320" height="240"></canvas>
        <script>{KIT_PATH.read_text(encoding='utf-8')}</script>
        <script>
          const ctx = document.getElementById('c').getContext('2d');
          window.__seek = (t) => {{
            ctx.fillStyle = '#F6F1DD';
            ctx.fillRect(0, 0, 320, 240);
            const p = Math.min(1, Math.max(0, t / 2.0));
            const y = MarkKit.springAtTime(t, {{ from: 180, to: 90, zeta: 0.78, omega: 12 }});
            MarkKit.drawTaperedStroke(ctx, [[30, y], [160, y - 25], [290, y + 10]], {{
              seed: 'valve-arm', width: 7, progress: p, boilStep: Math.floor(t * 12), color: '#172B3B'
            }});
          }};
        </script>
        </body></html>"""
        with tempfile.TemporaryDirectory() as td:
            page_file = Path(td) / 'scene.html'
            page_file.write_text(html, encoding='utf-8')
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={'width': 320, 'height': 240})
                page.goto(page_file.as_uri())
                page.evaluate('window.__seek(0.75)')
                shot_first = page.screenshot()
                page.evaluate('window.__seek(1.90)')
                shot_later = page.screenshot()
                page.evaluate('window.__seek(0.10)')
                page.evaluate('window.__seek(0.75)')
                shot_reseek = page.screenshot()
                browser.close()
        self.assertNotEqual(shot_first, shot_later)
        self.assertEqual(shot_first, shot_reseek, 'Backward/out-of-order seek must produce identical pixels')


if __name__ == '__main__':
    unittest.main()
