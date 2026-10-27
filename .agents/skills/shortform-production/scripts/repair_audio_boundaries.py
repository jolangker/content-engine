"""Repair preserved Ruang di Antara narration placement without resynthesis or reposting."""
from __future__ import annotations

import argparse
import html
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys

import numpy as np

import audio_boundaries as acoustic
import sound_design

ROOT = Path(__file__).resolve().parents[4]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def attr(tag, key):
    m = re.search(r'(?<![\w-])' + re.escape(key) + r'="([^"]*)"', tag)
    return m[1] if m else None


def set_attr(tag, key, value):
    if re.search(r'(?<![\w-])' + re.escape(key) + r'="', tag):
        return re.sub(r'(?<![\w-])' + re.escape(key) + r'="[^"]*"', lambda _: f'{key}="{value}"', tag)
    return tag[:-1] + f' {key}="{value}">'


def archive(production):
    baseline = production / 'revisions/audio-boundaries-v1'
    if (baseline / 'manifest.json').exists():
        return baseline
    video = production / 'video'
    version = re.search(r'hyperframes@([\d.]+)', (video / 'package.json').read_text(encoding='utf-8'))[1]
    for command, name in [(['history', '--since', 'mine', '--who', 'codex-audio-boundaries', '--json'], 'history-before'),
                           (['history', 'begin', '--who', 'codex-audio-boundaries', '--label', 'Repair acoustic scene boundaries'], 'history-begin')]:
        result = subprocess.run([shutil.which('npx.cmd'), '--yes', f'hyperframes@{version}', *command],
                                cwd=video, capture_output=True, text=True, encoding='utf-8')
        dest = video / 'verification' / f'{name}-audio-v2.log'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(result.stdout + '\n' + result.stderr, encoding='utf-8')
        if result.returncode:
            raise RuntimeError(f'History command failed; inspect {dest}')
    files = list(production.glob('*.py')) + list(production.glob('*.md'))
    files += list((production / 'exports').glob('*.srt')) + list((production / 'exports').glob('*.vtt'))
    files += [p for p in video.glob('*') if p.is_file() and p.suffix in ('.json', '.html', '.md')]
    files += list((video / 'compositions').rglob('*.html')) + list((video / 'compositions').rglob('*.json'))
    manifest = {}
    for source in files:
        relative = source.relative_to(production)
        target = baseline / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        manifest[relative.as_posix()] = acoustic.digest(source)
    dump(baseline / 'manifest.json', {'purpose': 'Pre-repair source snapshot; existing v1 MP4/audio files retained in place.',
                                     'files': manifest, 'hyperframes_version': version})
    return baseline


def restore_master(video, baseline):
    root = (baseline / 'video/index.html').read_text(encoding='utf-8')
    tag = next(t for t in re.findall(r'<audio\b[^>]+>', root) if attr(t, 'id') == 'narration')
    played = acoustic.decode(video / attr(tag, 'src'))
    pre_roll = float(attr(tag, 'data-start'))
    old_placement = read(baseline / 'video/placement.json') if (baseline / 'video/placement.json').exists() else {}
    native = acoustic.decode(video / read(baseline / 'video/audio_meta.json')['voices'][0]['path'])
    if old_placement.get('pauses'):
        # Rejoining an already limited old mix can leave gain/filter discontinuities
        # at the old split syllable. Splice the untouched recording, then normalize.
        return native, pre_roll, old_placement
    master = played
    if abs(len(master) - len(native)) > 2:
        raise ValueError('Restored normalized master does not match the native recording duration')
    n = min(len(master), len(native))
    # Historical loudnorm can apply time-varying limiting; normalized and native
    # waveforms need not be related by one constant gain. Preserve the normalized
    # samples exactly rather than applying a second normalization pass.
    if float(np.corrcoef(master[:n], native[:n])[0, 1]) < .90:
        raise ValueError('Restored normalized master does not match preserved speech')
    return master, pre_roll, old_placement


def caption_groups(baseline, words):
    # Keep the accepted phrase grouping and copy from the previous SRT.
    srt = next((baseline / 'exports').glob('*.srt')).read_text(encoding='utf-8-sig')
    norm = lambda s: re.sub(r'\W', '', s.casefold())
    groups, cursor = [], 0
    for block in re.split(r'\n\s*\n', srt.strip()):
        lines = block.splitlines()
        if len(lines) < 3:
            continue
        text = ' '.join(lines[2:])
        tokens = text.split()
        end = cursor + len(tokens)
        if [norm(w) for w in tokens] != [norm(w['text']) for w in words[cursor:end]]:
            raise ValueError(f'Caption copy does not match preserved narration: {text}')
        groups.append({'text': text, 'word_start': cursor, 'word_end': end})
        cursor = end
    if cursor != len(words):
        raise ValueError('Caption groups do not cover every narration word')
    return groups


def repair(production, rebuild=False):
    production = Path(production).resolve()
    video = production / 'video'
    if (video / 'audio_boundaries.json').exists() and not rebuild:
        result = acoustic.verify(video)
        print(json.dumps({'slug': production.name, 'status': 'already_prepared',
                          'boundaries': len(result['boundaries'])}), flush=True)
        return result
    baseline = archive(production)
    old_timing = read(baseline / 'video/timing.json')
    old_scenes = old_timing['scenes']
    native = read(baseline / 'video/audio_meta.json')['voices'][0]
    words = native['words']
    word_ends = [s.get('word_end', s.get('word_last', -1) + 1) for s in old_scenes]
    master, pre_roll, old_placement = restore_master(video, baseline)
    pauses = {p['after_scene']: p['seconds'] for p in old_placement.get('pauses', [])}
    placed, moved, boundaries, utterances = acoustic.place(
        master, words, word_ends, [pauses.get(i, 0) for i in range(1, len(old_scenes))], pre_roll)
    previous_duration = old_timing.get('duration_s', old_timing.get('duration'))
    duration = math.ceil((previous_duration - 1e-7) * 30) / 30
    if len(placed) / acoustic.RATE > duration:
        raise ValueError('Repaired narration exceeds retained composition duration')
    starts = [0] + [b['visual_s'] for b in boundaries]
    ends = starts[1:] + [duration]
    scenes = []
    for i, (old, start, end, utterance) in enumerate(zip(old_scenes, starts, ends, utterances)):
        scene = {**old, **utterance, 'start': start, 'end': end, 'duration': end - start,
                 'start_frame': round(start * 30), 'end_frame': round(end * 30),
                 'word_first': utterance['word_start'], 'word_last': utterance['word_end'] - 1}
        if 'words' in scene:
            scene['words'] = moved[utterance['word_start']:utterance['word_end']]
        scenes.append(scene)
    timing = {**old_timing, 'duration_s': duration, 'voice_duration_s': len(placed) / acoustic.RATE,
              'words': moved, 'scenes': scenes,
              'basis': 'Preserved native-speed speech; measured quiet-region pause placement; integer 30fps scene cuts. '
                       'Word timestamp estimates reanchored to each measured acoustic utterance; no speech time stretching.'}
    dump(video / 'timing.json', timing)
    acoustic.write_pcm(video / 'assets/audio/narration-boundary-master.wav', master)
    dest = video / 'assets/audio/narration-boundaries-v2.wav'
    if old_placement.get('pauses'):
        unnormalized = video / 'assets/audio/narration-boundaries-v2-before-level.wav'
        acoustic.write_pcm(unnormalized, placed)
        target = (-18, -1.5, 11) if production.name == 'jeda-punya-waktu-kembali' else (-16, -2, 7)
        normalization = acoustic.normalize_after_placement(unnormalized, dest, *target)
    else:
        acoustic.write_pcm(dest, placed)
        normalization = {'order': 'unchanged continuous normalized recording; no old speech splice to reconstruct'}
    receipt = {'version': 2, 'path': dest.relative_to(video).as_posix(), 'sha256': acoustic.digest(dest),
               'source': native['path'], 'source_sha256': acoustic.digest(video / native['path']),
               'master_path': 'assets/audio/narration-boundary-master.wav',
               'master_sha256': acoustic.digest(video / 'assets/audio/narration-boundary-master.wav'),
               'duration_s': len(placed) / acoustic.RATE, 'duration': len(placed) / acoustic.RATE,
               'pre_roll_s': pre_roll, 'speech_speed': 1,
               'speech_samples_preserved_before_normalization': True, 'normalization': normalization,
               'timestamp_precision': 'Acoustic scene anchors; individual word timestamps remain estimates.',
               'sample_rate': acoustic.RATE, 'fps': 30, 'timing_sha256': acoustic.digest(video / 'timing.json'),
               'boundaries': boundaries, 'baseline': str(baseline.relative_to(production))}
    dump(video / 'audio_boundaries.json', receipt)
    dump(video / 'placement.json', {**receipt, 'pauses': boundaries, 'words': moved})
    for name in ['scenes.json', 'scene_schedule.json']:
        if (baseline / 'video' / name).exists():
            dump(video / name, scenes)
    root = (baseline / 'video/index.html').read_text(encoding='utf-8')
    root_tag = next(t for t in re.findall(r'<div\b[^>]+>', root) if attr(t, 'id') == 'root')
    root = root.replace(root_tag, set_attr(root_tag, 'data-duration', f'{duration:.8f}'))
    if (video / 'index.motion.json').exists():
        root_motion = read(video / 'index.motion.json')
        root_motion['duration'] = duration
        dump(video / 'index.motion.json', root_motion)
    host_tags = [t for t in re.findall(r'<div\b[^>]+>', root)
                 if attr(t, 'data-composition-src') and 'captions' not in attr(t, 'data-composition-src')]
    assert len(host_tags) == len(scenes)
    for old, new, host in zip(old_scenes, scenes, host_tags):
        ratio = new['duration'] / old['duration']
        path = attr(host, 'data-composition-src')
        comp = (baseline / 'video' / path).read_text(encoding='utf-8')
        # Scale local clip windows and direct timeline children, preserving all geometry/corrections.
        comp = re.sub(r'\bdata-(start|duration)="([\d.]+)"',
                      lambda m: f'data-{m[1]}="{float(m[2]) * ratio:.8f}"', comp)
        scale = f'''/* audio-boundaries-v2: retain relative choreography */
const audioBoundaryScale={ratio:.12f};
const audioBoundaryChildren=tl.getChildren(false,true,true).map(child=>({{child,start:child.startTime(),duration:child.duration(),delay:child.delay()}}));
audioBoundaryChildren.forEach(x=>{{x.child.duration(x.duration*audioBoundaryScale);x.child.delay(x.delay*audioBoundaryScale);x.child.startTime(x.start*audioBoundaryScale);}});
'''
        comp, count = re.subn(r'(?=window\.__timelines\[)', lambda _: scale, comp, count=1)
        if count != 1:
            raise ValueError(f'No timeline registration in {path}')
        (video / path).write_text(comp, encoding='utf-8')
        motion = (baseline / 'video' / path).with_suffix('.motion.json')
        if motion.exists():
            sidecar = read(motion)
            sidecar['duration'] = new['duration']
            for assertion in sidecar.get('assertions', []):
                for key in ('bySec', 'atSec', 'startSec', 'endSec'):
                    if isinstance(assertion.get(key), (int, float)):
                        assertion[key] *= ratio
            dump((video / path).with_suffix('.motion.json'), sidecar)
        changed_host = set_attr(set_attr(host, 'data-start', f'{new["start"]:.8f}'), 'data-duration', f'{new["duration"]:.8f}')
        root = root.replace(host, changed_host)
    narration_tag = next(t for t in re.findall(r'<audio\b[^>]+>', root) if attr(t, 'id') == 'narration')
    changed = narration_tag
    for key, value in {'src': receipt['path'], 'data-start': '0', 'data-duration': f'{receipt["duration_s"]:.8f}'}.items():
        changed = set_attr(changed, key, value)
    root = root.replace(narration_tag, changed)
    (video / 'index.html').write_text(root, encoding='utf-8')
    # Keep inherited caption geometry; replace timing and retain every accepted phrase.
    original_captions = (baseline / 'video/compositions/captions.html').read_text(encoding='utf-8')
    style = re.search(r'<style>(.*?)</style>', original_captions, re.S)[1]
    style = style.replace('../assets/', 'assets/')
    old_class = 'caption-group' if '.caption-group' in style else 'capline' if '.capline' in style else 'cap'
    if old_class == 'cap':
        style += '\n.cap{opacity:1}'
    script_data = read(video / 'script_data.json') if (video / 'script_data.json').exists() else []
    groups = caption_groups(baseline, words)
    nodes = []
    for j, group in enumerate(groups):
        index = next(i for i, s in enumerate(scenes) if s['word_start'] <= group['word_start'] < s['word_end'])
        s = scenes[index]
        if group['word_end'] > s['word_end']:
            raise ValueError('Caption phrase crosses a semantic scene boundary')
        dark = s.get('dark', False) or (script_data and script_data[index].get('dramatic', False)) or (production.name == 'kabar-baik' and index == 2)
        start = max(s['start'], moved[group['word_start']]['start'])
        stop = min(s['end'], moved[group['word_end'] - 1]['end'] + .10)
        if j + 1 < len(groups):
            stop = min(stop, moved[groups[j + 1]['word_start']]['start'])
        group.update(start=start, end=stop, scene=index + 1, dark=bool(dark),
                     words=moved[group['word_start']:group['word_end']])
        color = '#F3EDE3' if dark else '#302B28'
        text = html.escape(group['text'])
        if old_class == 'cap':
            text = f'<div style="background:{"#302B28" if dark else "#F3EDE3"};color:{color}">{text}</div>'
        nodes.append(f'<div id="caption-{j:03d}" class="clip {old_class}" data-start="{start:.8f}" '
                     f'data-duration="{stop-start:.8f}" data-track-index="0" data-layout-allow-caption-zone="true" style="color:{color}">{text}</div>')
    captions = f'<template><style>{style}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{duration}">' + ''.join(nodes) + f'</div><script>const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:{duration}}},0);window.__timelines.captions=tl;</script></template>'
    (video / 'compositions/captions.html').write_text(captions, encoding='utf-8')
    dump(video / 'caption_groups.json', groups)
    if (baseline / 'video/captions.json').exists():
        dump(video / 'captions.json', groups)
    def timestamp(seconds, separator=','):
        ms = round(seconds * 1000)
        return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}{separator}{ms%1000:03}'
    for extension, separator in [('srt', ','), ('vtt', '.')]:
        body = '\n\n'.join(f'{i+1}\n{timestamp(g["start"],separator)} --> {timestamp(g["end"],separator)}\n{g["text"]}' for i, g in enumerate(groups)) + '\n'
        if extension == 'vtt':
            body = 'WEBVTT\n\n' + body
        (production / 'exports' / f'{production.name}-v2.{extension}').write_text(body, encoding='utf-8')
    plan = read(baseline / 'video/sound_design.json')
    for cue in plan['cues']:
        i = next(i for i, s in enumerate(old_scenes) if s['start'] <= cue['start'] < s['start'] + s['duration'])
        cue['start'] = round(scenes[i]['start'] + (cue['start'] - old_scenes[i]['start']) * scenes[i]['duration'] / old_scenes[i]['duration'], 8)
    plan['timing_sha256'] = acoustic.digest(video / 'timing.json')
    plan['narration_sha256'] = receipt['sha256']
    plan['motion_sources'] = {path: sound_design.motion_digest(video / path) for path in plan['motion_sources']}
    dump(video / 'sound_design.json', plan)
    subprocess.run([sys.executable, str(Path(__file__).with_name('sound_design.py')), '--video', str(video), '--apply'], check=True, capture_output=True)
    report = acoustic.verify(video)
    note = '\n## Audio boundary revision v2\n\nUser requested correction after the 2026-10-27 investigation. Reused the existing narration and inherited gain; verified quiet insertion points and integer 30fps cuts. Original visual geometry, scene-specific corrections and relative choreography retained. V1 sources are snapshotted in revisions/audio-boundaries-v1; existing v1 export/delivery receipts remain historical. Scope: verified local v2 export and package; no remote replacement or repost. Current state: verification in progress.\n'
    episode = production / 'EPISODE.md'
    if '## Audio boundary revision v2' not in episode.read_text(encoding='utf-8'):
        with episode.open('a', encoding='utf-8') as f:
            f.write(note)
    story = video / 'STORYBOARD.md'
    table = '\n## Audio boundary revision v2 — current measured scene windows\n\nTimes in earlier planning sections are historical. These are the revised render windows; speech remains at native speed.\n\n| Scene | Start | End | Speech start | Speech end |\n| --- | --- | --- | --- | --- |\n'
    table += '\n'.join(f'| {i+1:02} | {s["start"]:.6f} | {s["end"]:.6f} | {s["speech_start"]:.6f} | {s["speech_end"]:.6f} |' for i,s in enumerate(scenes)) + '\n'
    source_story = story.read_text(encoding='utf-8')
    source_story = re.sub(r'\n## Audio boundary revision v2 — current measured scene windows.*', '', source_story, flags=re.S)
    story.write_text(source_story + table, encoding='utf-8')
    if (video / 'BRIEF.md').exists():
        brief = video / 'BRIEF.md'
        text = brief.read_text(encoding='utf-8')
        if '## Audio boundary revision v2' not in text:
            brief.write_text(text + note, encoding='utf-8')
    tracker = read(ROOT / 'TRACKER.json')
    next(e for e in tracker['productions'] if e['slug'] == production.name).update(stage='verification', status='in_progress')
    dump(ROOT / 'TRACKER.json', tracker)
    print(json.dumps({'slug': production.name, 'status': 'prepared', 'boundaries': len(boundaries),
                      'minimum_incoming_quiet_ms': min(b['incoming_quiet_ms'] for b in boundaries),
                      'duration_s': duration, 'caption_groups': len(groups)}), flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--production', type=Path)
    parser.add_argument('--board', choices=['ruang-di-antara'])
    parser.add_argument('--rebuild', action='store_true', help='Reapply from the preserved v1 snapshot')
    args = parser.parse_args()
    if bool(args.production) == bool(args.board):
        parser.error('Select one production or the board')
    targets = [args.production] if args.production else [ROOT / e['path'] for e in read(ROOT / 'TRACKER.json')['productions'] if e['board'] == args.board]
    for target in targets:
        repair(target, args.rebuild)
