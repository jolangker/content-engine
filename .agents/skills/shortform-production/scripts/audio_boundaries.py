"""Place editorial pauses only in measured quiet audio, on a shared sample/frame clock."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path
import subprocess

import numpy as np

RATE = 48000
FPS = 30


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def decode(path, rate=RATE):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-vn', '-ac', '1',
                          '-ar', str(rate), '-f', 'f32le', 'pipe:1'], capture_output=True, check=True)
    samples = np.frombuffer(raw.stdout, '<f4').copy()
    if not len(samples) or not np.isfinite(samples).all() or not np.any(samples):
        raise ValueError(f'Invalid narration audio: {path}')
    return samples


def write_pcm(path, samples):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(RATE),
                    '-ac', '1', '-i', 'pipe:0', '-c:a', 'pcm_s24le', str(path)],
                   input=np.asarray(samples, dtype='<f4').tobytes(), capture_output=True, check=True)


def normalize_after_placement(source, destination, integrated=-16, true_peak=-2, lra=7):
    """Normalize once after quiet splices, so gain/limiter edges cannot split speech."""
    target = f'loudnorm=I={integrated}:TP={true_peak}:LRA={lra}'
    first = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(source), '-af',
                            target + ':print_format=json', '-f', 'null', '-'],
                           capture_output=True, text=True, check=True)
    measured = json.JSONDecoder().raw_decode(first.stderr[first.stderr.rfind('{'):])[0]
    settings = (target + f':measured_I={measured["input_i"]}:measured_TP={measured["input_tp"]}'
                f':measured_LRA={measured["input_lra"]}:measured_thresh={measured["input_thresh"]}'
                f':offset={measured["target_offset"]}:linear=true:print_format=json')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(source), '-af', settings,
                    '-ar', str(RATE), '-ac', '1', '-c:a', 'pcm_s24le', str(destination)],
                   capture_output=True, check=True)
    return {'order': 'native speech -> verified quiet splices -> one final normalization',
            'target_i': integrated, 'target_tp': true_peak, 'target_lra': lra,
            'input_measurement': measured}


def quiet_intervals(samples, rate=RATE, threshold_db=-55, min_seconds=.04):
    """Return contiguous 5ms RMS windows below threshold; boundaries are samples."""
    block = round(rate * .005)
    count = len(samples) // block
    frames = samples[:count * block].reshape(count, block)
    rms = np.sqrt(np.mean(frames.astype('float64') ** 2, axis=1))
    quiet = rms < 10 ** (threshold_db / 20)
    edges = np.diff(np.r_[False, quiet, False].astype(int))
    return [(int(a * block), int(b * block))
            for a, b in zip(np.where(edges == 1)[0], np.where(edges == -1)[0])
            if (b - a) * block >= round(min_seconds * rate)]


def select_gap(intervals, previous_word, next_word, rate=RATE):
    """Use alignment as a search hint; refuse placement unless a quiet interval exists."""
    hint = (previous_word['end'] + next_word['start']) / 2
    candidates = []
    for a, b in intervals:
        center = (a + b) / (2 * rate)
        if not hint - .8 <= center <= hint + .35:
            continue
        # Exclude a pause before the previous word or after the following word.
        if b / rate <= previous_word['start'] or a / rate >= next_word['end']:
            continue
        distance = max(0, a / rate - hint, hint - b / rate)
        candidates.append((distance, abs(center - hint), -(b - a), a, b))
    if not candidates:
        raise ValueError(f'No verified quiet interval near {hint:.3f}s: '
                         f'{previous_word["text"]} / {next_word["text"]}; realign or review this recording')
    _, _, _, a, b = min(candidates)
    return a, b


def place(samples, words, word_ends, pause_seconds, pre_roll=0, fps=FPS, rate=RATE):
    """Preserve every speech sample and insert pauses into verified quiet intervals.

    word_ends contains exclusive cumulative indices for every scene, including the last.
    Native word timestamps are estimates, reanchored within each acoustic utterance.
    """
    if not word_ends or word_ends[-1] != len(words) or len(pause_seconds) != len(word_ends) - 1:
        raise ValueError('Scene word ranges and pause list do not cover the narration')
    if any(a >= b for a, b in zip([0] + word_ends[:-1], word_ends)):
        raise ValueError('Empty or unordered scene word ranges')
    intervals = quiet_intervals(samples, rate)
    leading = round(pre_roll * rate)
    boundaries, shift = [], leading
    chunks, cursor = [np.zeros(leading, dtype='<f4')], 0
    for i, (word_end, pause) in enumerate(zip(word_ends[:-1], pause_seconds)):
        if pause < 0:
            raise ValueError('Pause duration must be nonnegative')
        a, b = select_gap(intervals, words[word_end - 1], words[word_end], rate)
        cut, silence = (a + b) // 2, round(pause * rate)
        if cut <= cursor:
            raise ValueError('Selected acoustic boundaries are not strictly ordered')
        quiet_start, quiet_end = a + shift, b + shift + silence
        frame = round((quiet_start + quiet_end) * fps / (2 * rate))
        sampled = frame * rate / fps
        guard = round(.08 * rate)
        if sampled - quiet_start < guard or quiet_end - sampled < guard:
            raise ValueError(f'Insufficient quiet margin at scene {i + 1}: '
                             'extend the editorial pause or review the acoustic boundary')
        boundaries.append({'after_scene': i + 1, 'source_quiet_start_sample': a,
                           'source_quiet_end_sample': b, 'source_cut_sample': cut,
                           'original_time': cut / rate, 'seconds': silence / rate,
                           'sample': cut, 'inserted_samples': silence,
                           'placed_pause_start_sample': cut + shift,
                           'placed_quiet_start_sample': quiet_start, 'placed_quiet_end_sample': quiet_end,
                           'visual_frame': frame, 'visual_s': frame / fps,
                           'outgoing_quiet_ms': (sampled - quiet_start) * 1000 / rate,
                           'incoming_quiet_ms': (quiet_end - sampled) * 1000 / rate})
        chunks.extend([samples[cursor:cut], np.zeros(silence, dtype='<f4')])
        cursor, shift = cut, shift + silence
    chunks.append(samples[cursor:])
    placed = np.concatenate(chunks)
    # Preserve all source samples exactly before the final 24-bit PCM encoding.
    recovered, cursor, inserted = [], leading, 0
    for b in boundaries:
        stop = b['source_cut_sample'] + leading + inserted
        recovered.append(placed[cursor:stop])
        cursor = stop + b['inserted_samples']
        inserted += b['inserted_samples']
    recovered.append(placed[cursor:])
    if not np.array_equal(np.concatenate(recovered), samples):
        raise ValueError('Speech sample preservation failed')
    moved, utterances, begin = [], [], 0
    for i, end in enumerate(word_ends):
        offset = leading + sum(b['inserted_samples'] for b in boundaries[:i])
        onset = boundaries[i - 1]['source_quiet_end_sample'] if i else 0
        finish = boundaries[i]['source_quiet_start_sample'] if i < len(boundaries) else len(samples)
        # Refine first/last edges against the signal, without synthesizing or stretching speech.
        active = samples[onset:finish]
        block = round(rate * .005)
        count = len(active) // block
        rms = np.sqrt(np.mean(active[:count * block].astype('float64').reshape(count, block) ** 2, axis=1))
        voiced = np.where(rms >= 10 ** (-55 / 20))[0]
        if not len(voiced):
            raise ValueError(f'Utterance {i + 1} has no measured signal')
        onset += int(voiced[0] * block)
        finish = onset + int((voiced[-1] - voiced[0] + 1) * block)
        old_start, old_end = words[begin]['start'], words[end - 1]['end']
        if old_end <= old_start:
            raise ValueError('Invalid native utterance span')
        scale = (finish - onset) / rate / (old_end - old_start)
        for word in words[begin:end]:
            start = (onset + offset) / rate + (word['start'] - old_start) * scale
            stop = (onset + offset) / rate + (word['end'] - old_start) * scale
            moved.append({**word, 'start': round(start, 8), 'end': round(stop, 8)})
        utterances.append({'word_start': begin, 'word_end': end,
                           'speech_start': (onset + offset) / rate,
                           'speech_end': (finish + offset) / rate,
                           'timestamp_anchor_scale': scale})
        begin = end
    return placed, moved, boundaries, utterances


def verify(video, export=None):
    video = Path(video).resolve()
    receipt = json.loads((video / 'audio_boundaries.json').read_text(encoding='utf-8'))
    narration = video / receipt['path']
    if digest(narration) != receipt['sha256'] or digest(video / 'timing.json') != receipt['timing_sha256']:
        raise ValueError('Stale narration or boundary timing')
    samples = decode(narration)
    timing = json.loads((video / 'timing.json').read_text(encoding='utf-8'))
    markup = (video / 'index.html').read_text(encoding='utf-8')
    hosts = [tag for tag in re.findall(r'<div\b[^>]+>', markup)
             if 'data-composition-src=' in tag and 'captions' not in tag]
    if len(hosts) != len(timing['scenes']):
        raise ValueError('Rendered scene hosts do not cover the verified scene map')
    for host, scene in zip(hosts, timing['scenes']):
        for key in ('start', 'duration'):
            value = re.search(r'data-' + key + r'="([^"]+)"', host)
            if value is None or abs(float(value[1]) - scene[key]) > 1e-7:
                raise ValueError('HTML scene host differs from the verified sample/frame map')
    checked = []
    actual = decode(export) if export else None
    for b, scene in zip(receipt['boundaries'], timing['scenes'][1:]):
        cut = b['visual_frame'] * RATE // FPS
        if abs(scene['start'] - b['visual_frame'] / FPS) > 1e-7:
            raise ValueError('Scene cut differs from verified integer video frame')
        span = samples[cut - round(.06 * RATE):cut + round(.06 * RATE)]
        db = float(20 * np.log10(max(np.sqrt(np.mean(span.astype('float64') ** 2)), 1e-10)))
        if db > -54:
            raise ValueError(f'Active narration at scene cut {b["after_scene"]}: {db:.2f}dBFS')
        row = {'after_scene': b['after_scene'], 'visual_s': b['visual_s'],
               'narration_cut_rms_dbfs': db, 'incoming_quiet_ms': b['incoming_quiet_ms'],
               'outgoing_quiet_ms': b['outgoing_quiet_ms']}
        if actual is not None:
            region = actual[cut - round(.04 * RATE):cut + round(.04 * RATE)]
            export_db = float(20 * np.log10(max(np.sqrt(np.mean(region.astype('float64') ** 2)), 1e-10)))
            row['export_cut_rms_dbfs'] = export_db
            # Board SFX must not mask an incoming narration leak at these quiet cuts.
            if export_db > -45:
                raise ValueError(f'Export is not quiet at scene cut {b["after_scene"]}: {export_db:.2f}dBFS')
        checked.append(row)
    result = {'status': 'passed', 'boundaries': checked, 'narration_sha256': receipt['sha256'],
              'timing_sha256': receipt['timing_sha256'], 'listening': 'not performed; acoustic measurements only'}
    if export:
        result['export_sha256'] = digest(export)
    dest = video / 'verification' / ('audio-boundaries-export-v2.json' if export else 'audio-boundaries-preflight-v2.json')
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', type=Path, required=True)
    parser.add_argument('--export', type=Path)
    args = parser.parse_args()
    report = verify(args.video, args.export)
    print(json.dumps({'status': report['status'], 'boundaries': len(report['boundaries'])}))
