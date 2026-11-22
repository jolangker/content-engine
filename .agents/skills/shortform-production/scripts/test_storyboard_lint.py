"""Unit and real-production tests for storyboard_lint.py."""
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from storyboard_lint import lint_storyboard


class StoryboardLintTests(unittest.TestCase):
    def _write_sb(self, tmp: Path, content: str, script: str | None = None) -> tuple[Path, Path | None]:
        sb = tmp / 'STORYBOARD.md'
        sb.write_text(content, encoding='utf-8')
        sc = None
        if script is not None:
            sc = tmp / 'SCRIPT.md'
            sc.write_text(script, encoding='utf-8')
        return sb, sc

    def test_clean_storyboard_with_matching_spoken_numbers_and_varied_camera_passes(self):
        with tempfile.TemporaryDirectory() as td:
            sb, sc = self._write_sb(
                Path(td),
                """---
format: 1080x1920
---
## Frame 1: Pasang bak awal (0-5s)
- duration: 5s
- shot: wide
- camera: hold
- scene: Keeper sets wooden pond frame onto shaded clay soil.
- on_screen_text: Isi Air 60%
- voiceover: Bentangkan terpal lalu isi air enam puluh persen saja.

## Frame 2: Pipa kuras bawah (5-10s)
- duration: 5s
- shot: close cutaway
- camera: push
- scene: Screwed PVC bottom drain flushes settled dark sludge outward.
- on_screen_text: Pipa 15 cm
- voiceover: Sambungkan pipa lima belas sentimeter di dasar bak.

## Frame 3: Kembali ke halaman utuh (10-15s)
- duration: 5s
- shot: wide
- camera: pull
- scene: Clear water circulates around stacked shelter pipes in the yard.
""",
                script='Isi air 60% dan sambungkan pipa 15 cm.',
            )
            res = lint_storyboard(sb, script_path=sc, lang='id', strict_fields=True)
            self.assertEqual(res['status'], 'passed', res)

    def test_rejects_abstract_scene_number_mismatch_copy_overflow_and_push_streak(self):
        with tempfile.TemporaryDirectory() as td:
            sb, sc = self._write_sb(
                Path(td),
                """## Frame 1: Hook (0-4s)
- duration: 4s
- camera: push
- scene: Title card fades in on black gradient background
- on_screen_text: Kapasitas Naik 40%
- voiceover: Kapasitas naik enam puluh persen.

## Frame 2: Step 2 (4-8s)
- duration: 4s
- camera: zoom-in
- scene: Water valve opens inside tank wall.
- on_screen_text: Ini kalimat label layar yang terlalu panjang melebihi delapan kata batas maksimal

## Frame 3: Step 3 (8-12s)
- duration: 4s
- camera: snap-zoom
- scene: Float ball rises to shut inlet nozzle.
""",
                script='Kapasitas naik 60%.',
            )
            res = lint_storyboard(sb, script_path=sc, lang='id', strict_fields=True)
            self.assertEqual(res['status'], 'failed')
            err_ids = {e['id'] for e in res['errors']}
            self.assertIn('abstract-scene', err_ids)
            self.assertIn('bookend-text-card', err_ids)
            self.assertIn('number-sync', err_ids)
            self.assertIn('on-screen-copy-length', err_ids)
            self.assertIn('camera-push-run', err_ids)

    def test_existing_real_productions_pass_storyboard_lint(self):
        root = Path(__file__).resolve().parents[4]
        for slug in ('maggot-jalan-ke-wadah', 'meteran-pegas-dan-rem'):
            prod = root / 'productions' / slug
            res = lint_storyboard(prod / 'video' / 'STORYBOARD.md', script_path=prod / 'SCRIPT.md', strict_fields=True)
            self.assertEqual(res['status'], 'passed', f'{slug} failed: {res}')


if __name__ == '__main__':
    unittest.main()
