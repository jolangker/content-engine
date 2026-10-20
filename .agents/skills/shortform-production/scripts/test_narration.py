"""Regression checks for voice selection and stale/corrupt audio reuse; no API calls."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from narration import cached_result, file_hash, fingerprint, generation_payload, merge_supplemental_audio, resolve_voice, words_from_alignment


class NarrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / '.env').write_text('ELEVENLABS_VOICE_ID="zephlyn-id" # selected voice\n', encoding='utf-8')
        self.request = {'provider': 'elevenlabs', 'voice': 'zephlyn-id', 'tts_model': 'eleven_v4', 'lang': 'id',
                        'voice_resolution': {'source': 'project_env'}, 'lines': [{'id': 'narration', 'text': '[calm] Halo lo.'}]}

    def test_project_file_wins_over_inherited_shell(self):
        with patch.dict(os.environ, {'ELEVENLABS_VOICE_ID': 'old-shell-voice'}):
            self.assertEqual(resolve_voice(self.root)[0], 'zephlyn-id')

    def test_stale_request_fails_before_generation(self):
        self.request['voice'] = 'brian-id'
        with self.assertRaisesRegex(ValueError, 'prepare the request again'):
            generation_payload(self.request, self.root)

    def test_missing_voice_fails_instead_of_falling_back(self):
        (self.root / '.env').write_text('ELEVENLABS_VOICE_ID=\n', encoding='utf-8')
        with self.assertRaises(ValueError):
            resolve_voice(self.root)

    def test_explicit_override_needs_recorded_reason(self):
        self.request['voice'] = 'episode-voice'
        self.request['voice_resolution'] = {'source': 'episode_override'}
        with self.assertRaises(ValueError):
            generation_payload(self.request, self.root)
        self.request['voice_resolution']['reason'] = 'User requested a character voice for this episode'
        self.assertEqual(generation_payload(self.request, self.root)['voice_id'], 'episode-voice')

    def test_identity_changes_when_any_audible_input_changes(self):
        payload = generation_payload(self.request, self.root)
        original = fingerprint(payload)
        for key, replacement in [('voice_id', 'other'), ('model_id', 'other'), ('text', '[serious] Halo lo.'),
                                 ('language_code', 'en'), ('output_format', 'mp3_22050_32'), ('seed', 42)]:
            self.assertNotEqual(original, fingerprint({**payload, key: replacement}))

    def test_cache_requires_identity_and_both_file_hashes(self):
        dest = self.root / 'voice.mp3'
        dest.write_bytes(b'original-audio')
        alignment = dest.with_suffix('.alignment.json')
        alignment.write_text('{"alignment": {}}', encoding='utf-8')
        self.assertIsNone(cached_result(dest, 'request-a'))
        receipt = dest.with_suffix('.request.json')
        record = {'request_sha256': 'request-a', 'audio_sha256': file_hash(dest), 'alignment_sha256': file_hash(alignment)}
        receipt.write_text(json.dumps(record), encoding='utf-8')
        self.assertIsNotNone(cached_result(dest, 'request-a'))
        self.assertIsNone(cached_result(dest, 'request-b'))
        dest.write_bytes(b'changed-audio')
        self.assertIsNone(cached_result(dest, 'request-a'))
        dest.write_bytes(b'original-audio')
        alignment.write_text('{"alignment": "changed"}', encoding='utf-8')
        self.assertIsNone(cached_result(dest, 'request-a'))

    def test_voice_regeneration_preserves_other_audio_and_invalidates_cue_review(self):
        original = {'sfx': [{'id': 'observation'}], 'bgm': {'path': 'bed.wav'}, 'bgm_pending': False,
                    'voices': [{'path': 'old.wav'}]}
        (self.root / 'audio_meta.json').write_text(json.dumps(original), encoding='utf-8')
        plan = self.root / 'sound_design.json'
        plan.write_text('{"decisions": {"sfx": "use"}}', encoding='utf-8')
        result = merge_supplemental_audio(self.root, {'voices': [{'path': 'new.wav'}], 'sfx': [], 'bgm': None})
        self.assertEqual(result['sfx'], original['sfx'])
        self.assertEqual(result['bgm'], original['bgm'])
        self.assertEqual(result['voices'][0]['path'], 'new.wav')
        self.assertTrue(result['sound_design']['needs_revalidation'])
        self.assertEqual(plan.read_text(), '{"decisions": {"sfx": "use"}}')

    def test_tags_do_not_become_caption_words(self):
        text = '[calm] Halo lo.'
        alignment = {'characters': list(text), 'character_start_times_seconds': [i / 10 for i in range(len(text))],
                     'character_end_times_seconds': [(i + 1) / 10 for i in range(len(text))]}
        words = words_from_alignment({'alignment': alignment})
        self.assertEqual([word['text'] for word in words], ['Halo', 'lo.'])
        self.assertEqual(words[0]['start'], .7)

    def test_invalid_normalized_alignment_uses_valid_raw_alignment(self):
        raw = {'characters': ['Halo', ' ', '[quiet]', 'lo.'],
               'character_start_times_seconds': [0, .4, .5, .8],
               'character_end_times_seconds': [.4, .5, .8, 1.2]}
        words = words_from_alignment({'normalized_alignment': {'characters': ['broken']}, 'alignment': raw})
        self.assertEqual([(w['text'], w['start'], w['end']) for w in words], [('Halo', 0, .4), ('lo.', .8, 1.2)])

    def test_invalid_native_timing_requires_same_audio_recovery(self):
        for start, end in [(-1, 1), (1, 0), (float('nan'), 1), (0, float('inf')), (True, 1), (0, 0)]:
            with self.subTest(start=start, end=end), self.assertRaisesRegex(ValueError, 'without resynthesis'):
                words_from_alignment({'alignment': {'characters': ['Halo'],
                    'character_start_times_seconds': [start], 'character_end_times_seconds': [end]}})

    def test_project_rejects_other_models_before_synthesis(self):
        self.request['tts_model'] = 'eleven_multilingual_v2'
        with self.assertRaisesRegex(ValueError, 'eleven_v4'):
            generation_payload(self.request, self.root)


if __name__ == '__main__':
    unittest.main()
