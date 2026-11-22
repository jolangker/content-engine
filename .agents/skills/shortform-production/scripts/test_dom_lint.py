"""Headless Playwright tests for dom_lint.py (Gate G5 anti-slop + readcheck hold duration) and episode_qa integration."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from dom_lint import lint_production_dom, required_read_seconds
from episode_qa import composition_digest


class DomLintTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.prod = Path(self.temp.name) / 'productions' / 'demo'
        self.video = self.prod / 'video'
        (self.video / 'compositions').mkdir(parents=True)
        (self.video / 'verification').mkdir()
        (self.prod / 'CONTRACT.json').write_text(json.dumps({
            'schema_version': 1,
            'format': {'width': 540, 'height': 960, 'fps': 30},
            'captions': {'region': [40, 740, 460, 140]},
            'craft': {'dom_lint': True},
        }), encoding='utf-8')

    def _write_project(self, scenes: dict[str, tuple[float, str]]):
        hosts = []
        cursor = 0.0
        for sid, (dur, html) in scenes.items():
            (self.video / 'compositions' / f'{sid}.html').write_text(
                f'<template><div id="root" style="position:relative;width:540px;height:960px;background:#F6F1DD;">{html}</div></template>',
                encoding='utf-8',
            )
            hosts.append(
                f'<div id="{sid}" class="clip" data-composition-src="compositions/{sid}.html" '
                f'data-track-kind="graphics" data-start="{cursor}" data-duration="{dur}"></div>'
            )
            cursor += dur
        (self.video / 'index.html').write_text(
            f'<!doctype html><html><body><div id="root" data-composition-id="main" data-duration="{cursor}" '
            f'data-width="540" data-height="960">{"".join(hosts)}</div></body></html>',
            encoding='utf-8',
        )

    def test_required_read_seconds_scales_with_length(self):
        self.assertEqual(required_read_seconds('Katup'), 0.4)
        self.assertGreater(required_read_seconds('Air naik melewati pipa saringan bawah'), 1.8)

    def test_clean_scene_with_readable_label_and_caption_exclusion_passes(self):
        self._write_project({
            's01': (
                3.0,
                '<div style="position:absolute;left:180px;top:300px;font-size:36px;color:#202F27;">Pipa Siphon</div>'
                '<div class="caption" style="position:absolute;left:50px;top:760px;font-size:28px;">01 / 05 tidak dihitung di area caption</div>',
            ),
        })
        report = lint_production_dom(self.prod, step=0.25)
        self.assertEqual(report['status'], 'passed', report)
        self.assertEqual(report['composition_sha256'], composition_digest(self.video))

    def test_detects_corner_chrome_counter_and_unreadable_flash_text(self):
        # Add minimal inline window.__seek to flash a 6-word sentence for only 0.2s
        flash_scene = """
        <div style="position:absolute;left:16px;top:14px;font-size:18px;letter-spacing:0.12em;text-transform:uppercase;color:#111;">01 / OVERVIEW</div>
        <div id="flash" style="position:absolute;left:80px;top:400px;font-size:32px;color:#111;">Kalimat panjang ini cuma lewat sebentar sekali</div>
        <script>
          window.__seek = (t) => {
            const el = document.getElementById('flash');
            if (el) el.style.display = (t >= 0.2 && t < 0.45) ? 'block' : 'none';
          };
        </script>
        """
        self._write_project({'s01': (3.0, flash_scene)})
        report = lint_production_dom(self.prod, step=0.2)
        self.assertEqual(report['status'], 'failed')
        rules = {h['rule'] for h in report['g5_anti_slop']['hits']}
        self.assertTrue(rules & {'C1', 'C2', 'C3'}, rules)
        self.assertGreaterEqual(report['readcheck']['fail_count'], 1)

    def test_detects_pinned_non_board_pill_across_three_scenes(self):
        pill = '<div style="position:absolute;left:180px;top:220px;font-size:28px;color:#222;">Label Diam Terus</div>'
        self._write_project({'s01': (2.0, pill), 's02': (2.0, pill), 's03': (2.0, pill)})
        report = lint_production_dom(self.prod, step=0.5)
        self.assertEqual(report['status'], 'failed')
        self.assertIn('PINNED', {h['rule'] for h in report['g5_anti_slop']['hits']})


if __name__ == '__main__':
    unittest.main()
