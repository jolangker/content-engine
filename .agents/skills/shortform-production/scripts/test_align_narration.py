"""Unit and integration tests for WhisperX-style CTC forced alignment and ASR script verification (no network/API calls)."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from align_narration import (
    align_audio_to_script,
    ctc_align_words,
    normalize_for_asr,
    strip_delivery_tags,
    verify_asr_against_script,
)


class AlignNarrationTests(unittest.TestCase):
    def test_strip_delivery_tags_preserves_punctuation_and_newlines(self):
        raw = '[calm] Halo, "kamu"! [pause] Isi air 60%.\n[warmly] Selesai.'
        self.assertEqual(strip_delivery_tags(raw), 'Halo, "kamu"! Isi air 60%.\nSelesai.')

    def test_indonesian_number_and_percent_normalization(self):
        self.assertEqual(
            normalize_for_asr('Isi air 60% atau 1.500 liter dalam 3,5 jam.', lang='id'),
            normalize_for_asr('isi air enam puluh persen atau seribu lima ratus liter dalam tiga koma lima jam', lang='id'),
        )
        self.assertEqual(
            normalize_for_asr('25 ekor dan 100 lubang', lang='id'),
            normalize_for_asr('dua puluh lima ekor dan seratus lubang', lang='id'),
        )

    def test_english_number_and_percent_normalization(self):
        self.assertEqual(
            normalize_for_asr('Wait 40 seconds for 105 items and 60% load.', lang='en'),
            normalize_for_asr('wait forty seconds for one hundred and five items and sixty percent load', lang='en'),
        )

    def test_verify_asr_passes_with_phonetic_aliases_and_number_words(self):
        script = '[calm] Kalau kamu punya 20 maggot Cherax, pisahkan dalam 2 wadah.'
        heard = 'kalau kamu punya dua puluh magot seraks pisahkan dalam dua wadah'
        res = verify_asr_against_script(
            script, heard, lang='id', aliases={'maggot': 'magot', 'cherax': 'seraks'},
        )
        self.assertTrue(res['passed'], res)
        self.assertTrue(res['numbers_matched'])
        self.assertEqual(res['tags_spoken'], [])

    def test_verify_asr_fails_on_wrong_number_even_when_similarity_is_high(self):
        script = '[calm] Pasang pipa sepanjang 15 sentimeter di dasar kolam halaman rumahmu sekarang.'
        heard = 'pasang pipa sepanjang lima puluh sentimeter di dasar kolam halaman rumahmu sekarang'
        res = verify_asr_against_script(script, heard, lang='id', threshold=0.80)
        self.assertFalse(res['passed'])
        self.assertFalse(res['numbers_matched'])
        self.assertEqual(len(res['number_mismatches']), 1)

    def test_verify_asr_detects_delivery_tag_spoken_aloud(self):
        script = 'Kalau airnya keruh, [whispering] buka keran kuras di bawah.'
        heard = 'kalau airnya keruh whispering buka keran kuras di bawah'
        res = verify_asr_against_script(script, heard, lang='id', threshold=0.75)
        self.assertFalse(res['passed'])
        self.assertEqual(len(res['tags_spoken']), 1)
        self.assertEqual(res['tags_spoken'][0]['tag'], '[whispering]')

    def test_verify_asr_detects_clipped_opening_and_closing_words(self):
        script = 'Bentangkan terpal tebal di sudut halaman lalu isi air bersih.'
        heard = 'terpal tebal di sudut halaman lalu isi air'
        res = verify_asr_against_script(script, heard, lang='id', threshold=0.70)
        self.assertFalse(res['passed'])
        self.assertIn('opening_words_missing', res['clipped_edges'])
        self.assertIn('closing_words_missing', res['clipped_edges'])

    def test_ctc_align_words_recovers_exact_frame_windows_and_preserves_script_casing(self):
        vocab = {'<pad>': 0, '|': 1, 'h': 2, 'a': 3, 'l': 4, 'o': 5, 'k': 6, 'm': 7, 'u': 8}
        # 50 frames covering 1.0 second (20 ms per frame):
        # "Halo," at frames 5..17 (0.10s..0.34s), silence/sep 17..25, "Kamu!" at 25..42 (0.50s..0.84s)
        logits = np.full((50, len(vocab)), -8.0, dtype=np.float64)
        logits[:5, 0] = 0.0
        for f, ch in [(5, 'h'), (6, 'h'), (7, 'h'), (8, 'a'), (9, 'a'), (10, 'a'),
                      (11, 'l'), (12, 'l'), (13, 'l'), (14, 'o'), (15, 'o'), (16, 'o')]:
            logits[f, vocab[ch]] = 0.0
        logits[17:25, 1] = 0.0
        for f, ch in [(25, 'k'), (26, 'k'), (27, 'k'), (28, 'a'), (29, 'a'), (30, 'a'), (31, 'a'),
                      (32, 'm'), (33, 'm'), (34, 'm'), (35, 'm'), (36, 'u'), (37, 'u'), (38, 'u'), (39, 'u'), (40, 'u'), (41, 'u')]:
            logits[f, vocab[ch]] = 0.0
        logits[42:, 0] = 0.0
        # Normalize to log-probabilities
        log_probs = logits - np.log(np.exp(logits).sum(axis=-1, keepdims=True))

        words = ctc_align_words(log_probs, ['Halo,', 'Kamu!'], vocab, duration_s=1.0, blank_id=0)
        self.assertEqual([w['text'] for w in words], ['Halo,', 'Kamu!'])
        self.assertAlmostEqual(words[0]['start'], 0.10, delta=0.04)
        self.assertAlmostEqual(words[0]['end'], 0.34, delta=0.04)
        self.assertAlmostEqual(words[1]['start'], 0.50, delta=0.04)
        self.assertAlmostEqual(words[1]['end'], 0.84, delta=0.04)
        self.assertLess(words[0]['end'], words[1]['start'])

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'Requires local FFmpeg tools')
    def test_full_align_audio_to_script_pipeline_with_mocked_models(self):
        with tempfile.TemporaryDirectory() as tmp:
            mp3 = Path(tmp) / 'take.mp3'
            subprocess.run(
                ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=1.2', '-b:a', '128k', str(mp3)],
                check=True,
            )
            fake_asr_words = [
                {'text': 'halo', 'start': 0.12, 'end': 0.48, 'probability': 0.95},
                {'text': 'dunia', 'start': 0.56, 'end': 1.04, 'probability': 0.93},
            ]
            fake_ctc = [
                {'text': 'Halo,', 'start': 0.14, 'end': 0.46, 'score': 0.98},
                {'text': 'Dunia!', 'start': 0.58, 'end': 1.02, 'score': 0.97},
            ]
            with patch('align_narration.transcribe_with_padding', return_value=('halo dunia', fake_asr_words, [])), \
                 patch('align_narration.run_wav2vec2_ctc_alignment', return_value=(fake_ctc, 'mock-wav2vec2')):
                out = align_audio_to_script(mp3, '[calm] Halo, Dunia!', lang='id')
            self.assertEqual(out['alignment_method'], 'ctc_wav2vec2_forced')
            self.assertTrue(out['asr_verification']['passed'])
            self.assertEqual([w['text'] for w in out['words']], ['Halo,', 'Dunia!'])
            self.assertEqual([w['id'] for w in out['words']], ['w0000', 'w0001'])


if __name__ == '__main__':
    unittest.main()
