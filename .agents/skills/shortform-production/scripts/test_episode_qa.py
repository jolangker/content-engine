"""Behavioral regression checks for the quality gate; synthetic local films, no API calls."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import numpy as np

from episode_qa import STANDING, budget, composition_digest, fingerprint, gate

W, H, FPS, SECONDS = 270, 480, 10, 12
REGION = [20, 380, 230, 60]


def encode(path, frames, amplitude=None):
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0']
    if amplitude:
        cmd += ['-f', 'lavfi', '-i', f'aevalsrc={amplitude}*sin(2*PI*1000*t):d={SECONDS}:s=48000', '-c:a', 'aac', '-b:a', '192k']
    cmd += ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', str(path)]
    subprocess.run(cmd, input=b''.join(f.tobytes() for f in frames), check=True)


def frames(animated):
    out = []
    for i in range(SECONDS * FPS):
        frame = np.full((H, W), 200, np.uint8)
        scene = i // (6 * FPS)
        x = 20 + (i % (6 * FPS)) * 3 if animated else 60
        frame[120 + 80 * scene:160 + 80 * scene, x:x + 40] = 40
        # Karaoke captions: a block that moves word by word inside the caption region.
        frame[390:430, 30 + (i // 3 % 6) * 35:60 + (i // 3 % 6) * 35] = 20
        out.append(frame)
    return out


def pose(path, x):
    frame = np.full((H, W), 200, np.uint8)
    frame[120:240, x:x + 80] = 40
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', f'{W}x{H}', '-i', 'pipe:0',
                    '-frames:v', '1', str(path)], input=frame.tobytes(), check=True)


class EpisodeQATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.films = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.films.cleanup)
        cls.still, cls.moving, cls.loud = (Path(cls.films.name) / name for name in ('still.mp4', 'moving.mp4', 'loud.mp4'))
        encode(cls.still, frames(False))
        encode(cls.moving, frames(True), amplitude=0.3055)   # about -14 LUFS
        encode(cls.loud, frames(True), amplitude=0.9)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.production = self.root / 'productions' / 'episode'
        self.video = self.production / 'video'
        (self.video / 'compositions').mkdir(parents=True)
        (self.video / 'verification').mkdir()
        hosts = ''.join(f'<div id="{s}" data-composition-src="compositions/{s}.html" data-track-kind="graphics" '
                        f'data-start="{6 * i}" data-duration="6"></div>' for i, s in enumerate(('s01', 's02')))
        (self.video / 'index.html').write_text(
            f'<html><body><div id="root" data-composition-id="main" data-duration="{SECONDS}" data-width="{W}" data-height="{H}">{hosts}'
            '<div id="caption-track" data-composition-src="compositions/captions.html" data-track-kind="captions" '
            f'data-start="0" data-duration="{SECONDS}"></div></div></body></html>', encoding='utf-8')
        for name in ('s01', 's02', 'captions'):
            self.scene(name, f'<script>window.__timelines["{name}"] = gsap.timeline({{paused: true}});</script>')
        words = 'Kalau kamu mau kolam, gali dulu. Tapi airnya turun.'.split()
        (self.video / 'timing.json').write_text(json.dumps({
            'duration_s': SECONDS, 'words': [{'text': w, 'start': .2 + .4 * i, 'end': .5 + .4 * i} for i, w in enumerate(words)],
            'scenes': [{'id': 's01', 'start': 0, 'end': 6}, {'id': 's02', 'start': 6, 'end': SECONDS}]}), encoding='utf-8')
        (self.video / 'sound_design.json').write_text(json.dumps({'decisions': {
            'narration': {'mode': 'use'}, 'bgm': {'mode': 'none'}, 'sfx': {'mode': 'use'}}}), encoding='utf-8')
        self.contract = {'schema_version': 1, 'captions': {'region': REGION},
                         'judged': [{'id': 'build-first', 'rule': 'The first spoken beat is a build action.'}]}
        self.save()
        self.use(self.moving)
        self.review()

    def scene(self, name, body):
        (self.video / 'compositions' / f'{name}.html').write_text(f'<template><div id="root">{body}</div></template>', encoding='utf-8')

    def save(self):
        (self.production / 'CONTRACT.json').write_text(json.dumps(self.contract), encoding='utf-8')

    def use(self, film):
        shutil.copy(film, self.video / 'verification' / 'proof.mp4')

    def review(self, reviewer='subagent', verdicts=None, extra='', listening='agent'):
        verdicts = verdicts or {}
        ids = [r['id'] for r in STANDING] + ['build-first']
        lines = [f'- [{verdicts.get(i, "pass")}] {i}: inspected on the beat sheet at phone width' for i in ids if verdicts.get(i) != 'drop']
        (self.video / 'REVIEW.md').write_text('\n'.join([
            '# Review', '', '## Gate record', '', f'composition_sha256: {composition_digest(self.video)}',
            f'independent_review: {reviewer}', f'listening: {listening}',
            'weakest_shot: s02, the square leaves before the line ends', '', *lines, extra]), encoding='utf-8')

    def storyboard(self, shots=('wide', 'close'), reads=('pot is set (0-2s); water test (2-4.5s)', 'waterline drops (0-3s); gap shows (3-6s)'),
                   end_x=150, hook_x=(20, 60, 150)):
        (self.video / 'STORYBOARD.md').write_text('---\nformat: 270x480\n---\n' + ''.join(
            f'\n## Frame {i + 1}: Beat {i + 1} ({6 * i}-{6 * i + 6}s)\n\n- duration: 6s\n- shot: {shot}\n- reads: {read}\n'
            for i, (shot, read) in enumerate(zip(shots, reads))), encoding='utf-8')
        boards = self.video / 'boards'
        shutil.rmtree(boards, ignore_errors=True)
        for i in range(len(shots)):
            pose(boards / 'stills' / f'frame-{i:02d}-at-{6 * i + 3}s.png', 60)
            pose(boards / 'poses' / f'{i + 1:02d}-a-start.png', 20)
            pose(boards / 'poses' / f'{i + 1:02d}-b-end.png', end_x)
        for second, x in zip((0, 1, 3), hook_x):
            pose(boards / 'poses' / f'hook-{second}.0s.png', x)
        (boards / 'storyboard.html').write_text('<html></html>', encoding='utf-8')
        pose(boards / 'storyboard.png', 60)

    def failed(self, verdict):
        return {c['id'] for c in verdict['checks'] if c['status'] == 'failed'}

    def test_animated_film_passes_and_records_a_verdict(self):
        verdict = gate(self.production, 'verification')
        self.assertEqual(verdict['status'], 'passed', verdict['disclose'])
        saved = json.loads((self.video / 'verification' / 'quality-gate-verification.json').read_text(encoding='utf-8'))
        self.assertEqual(saved['composition_sha256'], composition_digest(self.video))

    def test_caption_changes_do_not_count_as_motion(self):
        self.use(self.still)
        verdict = gate(self.production, 'verification')
        self.assertEqual(self.failed(verdict), {'motion-floor', 'hook-motion'})
        scenes = next(c for c in verdict['checks'] if c['id'] == 'motion-floor')['measured']
        self.assertGreater(scenes[0]['longest_static_seconds'], 5)

    def test_captions_track_without_region_fails_closed(self):
        self.contract['captions'] = {}
        self.save()
        self.use(self.still)
        self.assertIn('motion-floor', self.failed(gate(self.production, 'verification')))

    def test_still_scene_fails_unless_it_plays_footage(self):
        self.scene('s02', '<div data-no-timeline><img src="pose.png"></div>')
        self.review()
        self.assertEqual(self.failed(gate(self.production, 'verification')), {'scene-timelines'})
        self.scene('s02', '<div data-no-timeline><video src="shot.mp4" muted></video></div>')
        self.review()
        self.assertEqual(gate(self.production, 'verification')['status'], 'passed')

    def test_contract_limits_duration_hook_and_audio_roles(self):
        self.contract.update(duration_seconds={'min': 90}, hook={'first_sentence_max_seconds': 2, 'turn': {'markers': ['tapi'], 'max_seconds': 2}},
                             audio={'bgm': 'use'}, narration={'max_words_per_scene': 5}, scene_count={'min': 3})
        self.save()
        self.assertEqual(self.failed(gate(self.production, 'verification')),
                         {'duration', 'hook-first-sentence', 'hook-turn', 'audio-roles', 'words-per-scene', 'scene-count'})

    def test_misspelled_contract_field_is_rejected(self):
        self.contract['duration_second'] = {'min': 90}
        self.contract['hook'] = {'first_sentence_seconds': 2}
        self.save()
        with self.assertRaisesRegex(ValueError, 'duration_second, hook.first_sentence_seconds'):
            gate(self.production, 'verification')

    def test_review_must_cover_this_composition_and_every_rule(self):
        self.review(verdicts={'motion-variety': 'fail', 'build-first': 'drop'}, extra='- P0 · t=2s · s01 · label clipped · open')
        verdict = gate(self.production, 'verification')
        self.assertEqual(self.failed(verdict), {'judged-rules', 'open-p0'})
        self.assertEqual(next(c for c in verdict['checks'] if c['id'] == 'judged-rules')['measured'],
                         {'motion-variety': 'fail', 'build-first': 'missing'})
        self.review()
        self.scene('s01', '<script>window.__timelines["s01"] = gsap.timeline({paused: true}).to("#a", {x: 9});</script>')
        self.assertEqual(self.failed(gate(self.production, 'verification')), {'review-record'})

    def test_prose_about_p0_is_not_an_open_finding(self):
        self.review(extra='No P0 remains open after the fixes.')
        self.assertEqual(gate(self.production, 'verification')['status'], 'passed')

    def test_verdict_without_evidence_does_not_count(self):
        text = (self.video / 'REVIEW.md').read_text(encoding='utf-8').replace(
            '- [pass] ear-test: inspected on the beat sheet at phone width', '- [pass] ear-test')
        (self.video / 'REVIEW.md').write_text(text, encoding='utf-8')
        verdict = gate(self.production, 'verification')
        self.assertEqual(next(c for c in verdict['checks'] if c['id'] == 'judged-rules')['measured'], {'ear-test': 'no evidence'})

    def test_missing_reviewer_keeps_the_human_checkpoint_and_blocks_delivery(self):
        self.review(reviewer='unavailable')
        self.assertEqual(gate(self.production, 'verification')['status'], 'needs_human_review')
        self.assertIn('independent-review', self.failed(gate(self.production, 'export', self.moving)))
        self.review(reviewer='human')
        self.assertEqual(gate(self.production, 'export', self.moving)['status'], 'passed')

    def test_unheard_audio_is_disclosed_and_a_missing_listener_fails(self):
        self.review(listening='unavailable')
        verdict = gate(self.production, 'verification')
        self.assertEqual((verdict['status'], [c['id'] for c in verdict['disclose']]), ('passed', ['listening']))
        text = (self.video / 'REVIEW.md').read_text(encoding='utf-8').replace('listening: unavailable\n', '')
        (self.video / 'REVIEW.md').write_text(text, encoding='utf-8')
        self.assertEqual(self.failed(gate(self.production, 'verification')), {'listening'})

    def test_override_needs_authority_and_is_disclosed(self):
        self.contract.update(duration_seconds={'min': 90}, overrides=[{'check': 'duration', 'reason': 'User asked for a 12 second teaser'}])
        self.save()
        with self.assertRaisesRegex(ValueError, 'authority'):
            gate(self.production, 'verification')
        self.contract['overrides'][0]['authority'] = 'user'
        self.save()
        verdict = gate(self.production, 'verification')
        self.assertEqual(verdict['status'], 'passed')
        self.assertEqual([c['id'] for c in verdict['disclose']], ['duration'])

    def test_export_loudness_window(self):
        with self.assertRaisesRegex(ValueError, 'needs --film'):
            gate(self.production, 'export')
        self.assertEqual(gate(self.production, 'export', self.moving)['status'], 'passed')
        self.assertEqual(self.failed(gate(self.production, 'export', self.loud)), {'loudness'})

    def test_storyboard_plan_with_cadence_variety_and_poses_passes(self):
        self.storyboard()
        verdict = gate(self.production, 'storyboard')
        self.assertEqual(verdict['status'], 'passed', verdict['disclose'])
        self.assertTrue((self.video / 'verification' / 'quality-gate-storyboard.json').is_file())

    def test_storyboard_rejects_one_framing_and_one_long_read(self):
        self.storyboard(shots=('wide', 'wide', 'wide'), reads=('the whole build happens (0-6s)', 'water (0-2s); spill (2-6s)', 'fix (0-3s); test (3-6s)'))
        verdict = gate(self.production, 'storyboard')
        self.assertEqual(self.failed(verdict), {'shot-variety', 'reads-cadence'})
        self.assertEqual(next(c for c in verdict['checks'] if c['id'] == 'reads-cadence')['measured'], {1: '6.0s with nothing new'})

    def test_storyboard_needs_poses_that_differ(self):
        self.storyboard(end_x=20, hook_x=(60, 60, 60))
        verdict = gate(self.production, 'storyboard')
        self.assertEqual(self.failed(verdict), {'poses'})
        self.assertEqual(set(next(c for c in verdict['checks'] if c['id'] == 'poses')['measured']), {'hook', 1, 2})
        shutil.rmtree(self.video / 'boards' / 'poses')
        measured = next(c for c in gate(self.production, 'storyboard')['checks'] if c['id'] == 'poses')['measured']
        self.assertEqual(measured, {'hook': '0 of 3 poses', 1: 'needs a start and an end pose', 2: 'needs a start and an end pose'})

    def test_storyboard_holds_the_plan_to_contract_duration_and_scene_count(self):
        self.contract.update(duration_seconds={'min': 90}, scene_count={'min': 16, 'max': 16})
        self.save()
        self.storyboard()
        self.assertEqual(self.failed(gate(self.production, 'storyboard')), {'duration', 'scene-count'})

    def test_fingerprint_separates_a_held_clip_from_a_moving_one(self):
        held, moving = fingerprint(self.still, REGION), fingerprint(self.moving, REGION)
        self.assertGreater(held['held_share'], .9)
        self.assertEqual((moving['held_share'], moving['first_motion_seconds']), (0, .2))
        self.assertLess(fingerprint(self.still)['longest_static_seconds'], 1)
        self.assertAlmostEqual(moving['integrated_lufs'], -14, delta=1)

    def test_budget_uses_the_measured_rate_of_the_voice(self):
        (self.video / 'audio_meta.json').write_text(json.dumps({'voice_id': 'voice-a', 'voices': [
            {'duration_s': 10, 'words': [{}] * 25}]}), encoding='utf-8')
        self.contract['duration_seconds'] = {'min': 90, 'max': 120}
        self.save()
        result = budget(self.root, 250, 'voice-a', self.production)
        self.assertEqual((result['words_per_second'], result['narration_seconds'], result['film_seconds']), (2.5, 100.0, 120.0))
        self.assertEqual((result['fits'], result['words_for_range']), (True, [188, 250]))
        with self.assertRaisesRegex(ValueError, 'No measured narration'):
            budget(self.root, 250, 'voice-b')


if __name__ == '__main__':
    unittest.main()
