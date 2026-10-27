"""Regression checks for split incoming syllables, sample preservation, and frame clocks."""
import unittest
from unittest.mock import patch
from pathlib import Path
import json
import tempfile
import numpy as np
from audio_boundaries import place, quiet_intervals, select_gap, RATE
from repair_audio_boundaries import attr, restore_master


class BoundaryTests(unittest.TestCase):
    def test_editor_identity_does_not_hide_narration_id(self):
        tag = '<audio data-hf-id="hf-editor" id="narration" src="voice.wav">'
        self.assertEqual(attr(tag, 'id'), 'narration')

    def test_old_normalized_split_is_rebuilt_from_the_untouched_recording(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / 'video').mkdir()
            (base / 'video/index.html').write_text('<audio id="narration" src="old-limited.wav" data-start="0">')
            (base / 'video/placement.json').write_text(json.dumps({'pauses': [{'sample': 2, 'seconds': .5}]}))
            (base / 'video/audio_meta.json').write_text(json.dumps({'voices': [{'path': 'native.mp3'}]}))
            native = np.array([.1, .2, .3, .4], dtype='<f4')
            old_limited = np.array([.2, .4, 0, 0, .9, 1], dtype='<f4')
            with patch('repair_audio_boundaries.acoustic.decode', side_effect=[old_limited, native]):
                master, pre_roll, placement = restore_master(base / 'current', base)
            np.testing.assert_array_equal(master, native)
            self.assertEqual(pre_roll, 0)

    def test_wrong_provider_hint_does_not_split_incoming_speech(self):
        audio = np.zeros(RATE * 2, dtype='<f4')
        audio[4800:24000] = .2
        audio[36000:80000] = .3
        words = [{'text': 'old.', 'start': .1, 'end': .78},
                 {'text': 'Next', 'start': .86, 'end': 1.7}]
        placed, moved, boundaries, utterances = place(audio, words, [1, 2], [.35])
        b = boundaries[0]
        self.assertLess(b['source_cut_sample'], 36000)
        self.assertGreaterEqual(b['incoming_quiet_ms'], 80)
        self.assertGreaterEqual(b['outgoing_quiet_ms'], 80)
        # The entire incoming signal occurs after the new visual, without interruption.
        self.assertGreater(utterances[1]['speech_start'], b['visual_s'])
        start = 36000 + round(.35 * RATE)
        np.testing.assert_array_equal(placed[start:start + 44000], audio[36000:80000])

    def test_native_gap_without_inserted_silence_has_frame_safe_cut(self):
        audio = np.zeros(RATE * 2, dtype='<f4')
        audio[1000:20000] = .2
        audio[40000:85000] = .2
        words = [{'text': 'old.', 'start': .1, 'end': .7},
                 {'text': 'New', 'start': .8, 'end': 1.9}]
        output, _, boundaries, _ = place(audio, words, [1, 2], [0], pre_roll=.3)
        self.assertEqual(boundaries[0]['visual_frame'] / 30, boundaries[0]['visual_s'])
        np.testing.assert_array_equal(output[14400:], audio)

    def test_active_continuous_audio_refuses_insertion(self):
        audio = np.full(RATE * 2, .2, dtype='<f4')
        words = [{'text': 'one', 'start': .1, 'end': .9},
                 {'text': 'two', 'start': 1, 'end': 1.9}]
        with self.assertRaisesRegex(ValueError, 'No verified quiet'):
            place(audio, words, [1, 2], [.5])

    def test_too_short_gap_without_pause_refuses_unsafe_video_margin(self):
        audio = np.full(RATE * 2, .2, dtype='<f4')
        audio[24000:26400] = 0
        words = [{'text': 'one', 'start': .1, 'end': .5},
                 {'text': 'two', 'start': .55, 'end': 1.9}]
        with self.assertRaisesRegex(ValueError, 'Insufficient quiet margin'):
            place(audio, words, [1, 2], [0])

    def test_three_scenes_preserve_source_and_sample_rounded_pause_budget(self):
        audio = np.zeros(RATE * 3, dtype='<f4')
        audio[1000:20000] = .1
        audio[35000:65000] = .2
        audio[85000:135000] = .3
        words = [{'text': 'one.', 'start': .1, 'end': .5},
                 {'text': 'two.', 'start': .8, 'end': 1.5},
                 {'text': 'three.', 'start': 1.8, 'end': 2.9}]
        output, moved, boundaries, _ = place(audio, words, [1, 2, 3], [.273751, .358754])
        self.assertEqual(len(output), len(audio) + round(.273751 * RATE) + round(.358754 * RATE))
        self.assertTrue(all(a['end'] <= b['start'] for a, b in zip(moved, moved[1:])))
        self.assertEqual(len(boundaries), 2)


if __name__ == '__main__':
    unittest.main()
