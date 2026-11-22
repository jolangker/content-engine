"""Behavioral regression checks for sound plans; local files only, no API calls."""
import json
from pathlib import Path
import tempfile
import unittest
import wave
import numpy as np

from sound_design import apply_plan, check_plan, decode, digest, motion_digest, verify_export


def wav(path, values):
    with wave.open(str(path), 'wb') as f:
        f.setparams((1, 2, 48000, 0, 'NONE', 'not compressed'))
        f.writeframes((np.clip(values, -1, 1) * 32767).astype('<i2').tobytes())


class SoundDesignTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.video = Path(self.temp.name)
        t = np.arange(9600) / 48000
        self.sound = .5 * np.sin(2 * np.pi * (1700 * t + 7000 * t*t)) * np.sin(np.pi * t / .2)**2
        wav(self.video / 'cue.wav', self.sound)
        wav(self.video / 'voice.wav', .6 * np.sin(2*np.pi*2400*np.arange(96000)/48000))
        (self.video / 'timing.json').write_text('{}')
        (self.video / 'index.html').write_text('<html><body><div data-composition-id="main" data-duration="2">'
            '<audio id="narration" src="voice.wav" data-start="0" data-duration="2"></audio>'
            '<p id="keep">Keep visual content.</p></div></body></html>')
        (self.video / 'audio_meta.json').write_text('{"voices":[{"path":"voice.wav"}]}')
        self.plan = {'version': 1, 'decisions': {k: {'mode': mode, 'reason': 'Fixture creative decision'}
            for k, mode in [('narration', 'use'), ('bgm', 'none'), ('sfx', 'use')]},
            'timing_sha256': digest(self.video / 'timing.json'), 'narration_sha256': digest(self.video / 'voice.wav'),
            'assets': [{'id': 'contact', 'path': 'cue.wav', 'sha256': digest(self.video / 'cue.wav'), 'source': 'test chirp'}],
            'cues': [{'id': 'sfx-contact', 'asset': 'contact', 'scene': '1', 'purpose': 'Contact lands',
                      'trigger': 'Circle reaches point', 'start': .5, 'duration': .2, 'volume': .3}]}
        self.save()

    def save(self):
        (self.video / 'sound_design.json').write_text(json.dumps(self.plan), encoding='utf-8')

    def test_apply_keeps_voice_and_visuals_and_does_not_duplicate_cues(self):
        apply_plan(self.video)
        apply_plan(self.video)
        text = (self.video / 'index.html').read_text()
        self.assertEqual(text.count('id="sfx-contact"'), 1)
        self.assertIn('<p id="keep">Keep visual content.</p>', text)
        self.assertIn('id="narration" src="voice.wav" data-start="0" data-duration="2"', text)
        self.assertEqual(json.loads((self.video / 'audio_meta.json').read_text())['voices'], [{'path': 'voice.wav'}])

    def test_missing_placed_cue_fails_even_when_plan_exists(self):
        with self.assertRaisesRegex(ValueError, 'placed SFX'):
            check_plan(self.video)

    def test_rebuild_restores_readable_storyboard_cues(self):
        storyboard = self.video / 'STORYBOARD.md'
        storyboard.write_text('# Fresh builder scene plan\n')
        apply_plan(self.video)
        apply_plan(self.video)
        self.assertIn('# Fresh builder scene plan', storyboard.read_text())
        self.assertEqual(storyboard.read_text().count('| sfx-contact |'), 1)
        storyboard.write_text('# Rebuilt scene plan\n')
        apply_plan(self.video)
        self.assertIn('| sfx-contact |', storyboard.read_text())

    def test_stale_timing_and_changed_source_are_rejected(self):
        (self.video / 'timing.json').write_text('{"changed":true}')
        with self.assertRaisesRegex(ValueError, 'Stale cue timing'):
            apply_plan(self.video)
        self.plan['timing_sha256'] = digest(self.video / 'timing.json')
        self.save()
        (self.video / 'cue.wav').write_bytes(b'corrupted')
        with self.assertRaisesRegex(ValueError, 'Changed asset'):
            apply_plan(self.video)

    def test_changed_narration_requires_revalidation(self):
        wav(self.video / 'voice.wav', np.ones(96000) * .01)
        with self.assertRaisesRegex(ValueError, 'placed narration'):
            apply_plan(self.video)

    def test_editor_stamps_do_not_invalidate_motion_but_actual_edits_do(self):
        scene = self.video / 'scene.html'
        scene.write_text('<div id="actor">pose</div><script>move(1.5)</script>')
        self.plan['motion_sources'] = {'scene.html': motion_digest(scene)}
        self.save()
        scene.write_text('<div data-hf-id="hf-editor" id="actor">pose</div><script>move(1.5)</script>')
        apply_plan(self.video)
        scene.write_text('<div id="actor">pose</div><script>move(2.5)</script>')
        with self.assertRaisesRegex(ValueError, 'Stale motion trigger'):
            check_plan(self.video)

    def test_no_sfx_requires_reason_and_no_cues(self):
        self.plan['decisions']['sfx'] = {'mode': 'none', 'reason': ''}
        self.plan['cues'] = []
        self.save()
        with self.assertRaisesRegex(ValueError, 'Unresolved sfx'):
            apply_plan(self.video)
        self.plan['decisions']['sfx']['reason'] = 'Hold a quiet reflection'
        self.save()
        self.assertEqual(apply_plan(self.video)['cues'], 0)

    def test_gain_or_visibility_mismatch_fails(self):
        apply_plan(self.video)
        path = self.video / 'index.html'
        text = path.read_text()
        path.write_text(text.replace('data-volume="0.3"', 'data-volume="0"'))
        with self.assertRaisesRegex(ValueError, 'mismatch'):
            check_plan(self.video)
        path.write_text(text.replace('id="sfx-contact"', 'hidden id="sfx-contact"'))
        with self.assertRaisesRegex(ValueError, 'hidden'):
            check_plan(self.video)

    def test_export_verifier_detects_present_missing_and_mistimed_effects(self):
        apply_plan(self.video)
        mix = np.zeros(96000)
        mix[24000:33600] = self.sound * .3
        output = self.video / 'export.wav'
        voice = decode(self.video / 'voice.wav')
        wav(output, voice + mix)
        self.assertEqual(verify_export(self.video, output)['status'], 'passed')
        # A non-silent voice-like stream cannot stand in for the planned effect.
        wav(output, voice)
        with self.assertRaisesRegex(ValueError, 'verification failed'):
            verify_export(self.video, output)
        wav(output, voice + np.roll(mix, 9600))
        with self.assertRaisesRegex(ValueError, 'verification failed'):
            verify_export(self.video, output)

    def test_vocal_band_spectral_masking_fails_when_bgm_drowns_speech(self):
        apply_plan(self.video)
        t = np.arange(96000) / 48000
        mix = np.zeros(96000)
        mix[24000:33600] = self.sound * .3
        voice = decode(self.video / 'voice.wav')
        # Add loud continuous mid-band 1100 Hz + 1900 Hz bed masking the 300-3500 Hz speech band
        loud_bgm = 0.85 * np.sin(2 * np.pi * 1100 * t) + 0.75 * np.sin(2 * np.pi * 1900 * t)
        output = self.video / 'masked_export.wav'
        wav(output, voice * 0.25 + mix + loud_bgm)
        with self.assertRaisesRegex(ValueError, 'verification failed'):
            verify_export(self.video, output)
        saved = json.loads((self.video / 'verification' / 'sound-design-export.json').read_text(encoding='utf-8'))
        self.assertFalse(saved['vocal_masking']['passed'])


if __name__ == '__main__':
    unittest.main()
