"""Unit and integration tests for Phase 3 video-to-board clone tools (clone_measure.py, font_match.py, compare_frames.py)."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import wave

import numpy as np
from PIL import Image, ImageDraw

from clone_measure import measure_clone_reference
from compare_frames import compare_reference_and_render
from font_match import discover_local_ofl_fonts, match_fonts, measure_crop_ink_metrics


def _write_wav(path: Path, samples: np.ndarray, sr: int = 22050) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as wf:
        wf.setparams((1, 2, sr, 0, 'NONE', 'not compressed'))
        wf.writeframes((np.clip(samples, -1.0, 1.0) * 32767).astype('<i2').tobytes())


class CloneToolsTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'Requires local FFmpeg')
    def test_clone_measure_extracts_heatmap_palette_accents_onsets_and_ducking(self):
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            fps = 10
            secs = 6
            w, h = 180, 320
            frames = []
            for i in range(secs * fps):
                fr = np.full((h, w, 3), (246, 241, 221), dtype=np.uint8)  # warm paper ground
                if i < 30:
                    x = 20 + i * 3
                    fr[80:140, x:x + 40] = (44, 112, 128)
                else:
                    y = 60 + (i - 30) * 4
                    fr[y:y + 50, 50:130] = (157, 86, 52)
                # Saturated yellow accent badge (< 5% of frame)
                fr[20:42, 60:120] = (255, 212, 77)
                frames.append(fr)

            sr = 22050
            audio = np.zeros(secs * sr, dtype=np.float32)
            # Percussive clicks every 0.5s (120 BPM)
            for beat in range(12):
                idx = int(beat * 0.5 * sr)
                burst = np.exp(-np.linspace(0, 25, 800)) * np.sin(2 * np.pi * 900 * np.arange(800) / sr)
                audio[idx:idx + 800] += 0.8 * burst.astype(np.float32)
            audio_wav = tmp / 'click.wav'
            _write_wav(audio_wav, audio, sr=sr)

            clip = tmp / 'ref.mp4'
            subprocess.run(
                [
                    'ffmpeg', '-v', 'error', '-y',
                    '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', str(fps), '-i', 'pipe:0',
                    '-i', str(audio_wav),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-c:a', 'aac', '-shortest', str(clip),
                ],
                input=b''.join(f.tobytes() for f in frames),
                check=True,
            )

            # Create mock rea-video stems with clear ducking under speech
            stems = tmp / 'stems'
            vocals = np.zeros(secs * sr, dtype=np.float32)
            music = np.full(secs * sr, 0.25, dtype=np.float32) * np.sin(2 * np.pi * 220 * np.arange(secs * sr) / sr).astype(np.float32)
            # Speech active in 1..4s, music ducked by ~12 dB during speech
            s0, s1 = sr, 4 * sr
            vocals[s0:s1] = 0.55 * np.sin(2 * np.pi * 500 * np.arange(s1 - s0) / sr).astype(np.float32)
            music[s0:s1] *= 0.25
            _write_wav(stems / 'vocals.wav', vocals, sr=sr)
            _write_wav(stems / 'music.wav', music, sr=sr)

            out_dir = tmp / 'metrics'
            report = measure_clone_reference(clip, out_dir, stems_dir=stems, sample_fps=5.0)
            self.assertTrue((out_dir / 'motion_heatmap.jpg').is_file())
            self.assertTrue((out_dir / 'clone_metrics.json').is_file())
            self.assertGreaterEqual(report['motion']['segment_count'], 2)
            self.assertTrue(any(a['family'] == 'yellow' for a in report['visual_palette']['accents']), report['visual_palette'])
            self.assertTrue(report['audio_dsp']['available'])
            self.assertGreater(report['audio_dsp']['percussive_onset_count'], 4)
            self.assertGreater(report['audio_dsp']['stems_ducking']['ducking_depth_db'], 6.0)

    def test_compare_frames_auto_trims_and_scores_palette_overlap(self):
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            # Reference with black letterbox bars top & bottom
            ref = np.zeros((300, 200, 3), dtype=np.uint8)
            ref[30:270, :] = (246, 241, 221)
            ref[100:180, 40:160] = (44, 112, 128)
            ref_path = tmp / 'ref.png'
            Image.fromarray(ref).save(ref_path)

            ours_match = np.full((240, 200, 3), (245, 240, 220), dtype=np.uint8)
            ours_match[70:150, 40:160] = (46, 110, 126)
            ours_path = tmp / 'ours.png'
            Image.fromarray(ours_match).save(ours_path)

            ours_diff = np.full((240, 200, 3), (15, 10, 80), dtype=np.uint8)
            diff_path = tmp / 'diff.png'
            Image.fromarray(ours_diff).save(diff_path)

            cmp_good = compare_reference_and_render(ref_path, ours_path, tmp / 'cmp_good.png')
            cmp_bad = compare_reference_and_render(ref_path, diff_path, tmp / 'cmp_bad.png')

            self.assertTrue((tmp / 'cmp_good.png').is_file())
            self.assertEqual(cmp_good['reference_trimmed_box'], [0, 30, 200, 240])
            self.assertGreater(cmp_good['palette_neighborhood_overlap'], 0.85)
            self.assertLess(cmp_bad['palette_neighborhood_overlap'], 0.20)

    def test_font_match_discovers_repo_ofl_fonts_and_ranks_rendered_crop(self):
        from playwright.sync_api import sync_playwright

        root = Path(__file__).resolve().parents[4]
        fonts = discover_local_ofl_fonts(root)
        self.assertGreaterEqual(len(fonts), 3, 'Expected bundled OFL fonts in boards/ or hyperframes presets')

        # Render a target reference crop using the first discovered font in Chromium, then verify font_match ranks its family at the top!
        chosen = fonts[0]
        import base64
        ext = chosen['path'].suffix.lower().lstrip('.')
        fmt = 'woff2' if ext == 'woff2' else 'truetype'
        b64 = base64.b64encode(chosen['path'].read_bytes()).decode('ascii')
        sample_text = 'Bikin Kolam Halaman'

        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            crop_path = tmp / 'ref_crop.png'
            sheet_path = tmp / 'sheet.png'
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={'width': 640, 'height': 160})
                page.set_content(
                    f'<!doctype html><html><head><style>'
                    f'@font-face{{font-family:"TargetF";src:url("data:font/{ext};base64,{b64}") format("{fmt}");font-weight:100 900;}}'
                    f'body{{margin:0;background:#F6F1DD;display:flex;align-items:center;justify-content:center;height:160px;}}'
                    f'#t{{font:700 52px "TargetF";color:#202F27;}}</style></head>'
                    f'<body><div id="t">{sample_text}</div></body></html>',
                    wait_until='load',
                )
                page.evaluate('() => document.fonts.ready')
                page.screenshot(path=str(crop_path))
                browser.close()

            target = measure_crop_ink_metrics(crop_path)
            self.assertGreater(target['ink_width_px'], 150)
            ranked = match_fonts(sample_text, target, fonts[:6], top_n=4, sheet_path=sheet_path)
            self.assertTrue(sheet_path.is_file())
            self.assertGreaterEqual(len(ranked), 1)
            # Top-2 matches should include the exact source family with tiny natural width delta
            top_families = {r['family'].lower() for r in ranked[:2]}
            self.assertIn(chosen['family'].lower(), top_families, ranked)


if __name__ == '__main__':
    unittest.main()
