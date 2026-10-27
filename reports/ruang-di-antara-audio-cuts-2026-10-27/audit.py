"""Reproduce timing, waveform and export-offset evidence without editing productions."""
from pathlib import Path
import hashlib
import json
import math
import re
import subprocess

import numpy as np
from scipy.signal import correlate

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def decode(path, rate):
    result = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-ar', str(rate),
                             '-ac', '1', '-f', 'f32le', 'pipe:1'],
                            capture_output=True, check=True)
    return np.frombuffer(result.stdout, dtype='<f4')


def rms_db(samples):
    return float(20 * np.log10(max(1e-10, np.sqrt(np.mean(samples.astype('float64') ** 2)))))


records = []
for item in read(ROOT / 'TRACKER.json')['productions']:
    if item['board'] != 'ruang-di-antara':
        continue
    production = ROOT / item['path']
    video = production / 'video'
    timing = read(video / 'timing.json')
    meta = read(video / 'audio_meta.json')
    native_words = meta['voices'][0]['words']
    scenes = timing['scenes']
    html = (video / 'index.html').read_text(encoding='utf-8')
    tag = next(t for t in re.findall(r'<audio[^>]+>', html) if 'id="narration"' in t)
    source = video / re.search(r'src="([^"]+)"', tag)[1]
    offset = float(re.search(r'data-start="([^"]+)"', tag)[1])
    export = next((production / 'exports').glob('*.mp4'))
    probe = json.loads(subprocess.check_output(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
         'stream=avg_frame_rate,r_frame_rate,start_time,nb_frames', '-of', 'json', str(export)]))['streams'][0]
    assert probe['avg_frame_rate'] == '30/1' and float(probe['start_time']) == 0, probe
    hosts = re.findall(r'<div\b[^>]*data-composition-src="compositions/(?!captions)[^>]+>', html)
    assert len(hosts) == len(scenes), (item['slug'], len(hosts), len(scenes))
    for host, scene in zip(hosts, scenes):
        assert abs(float(re.search(r'data-start="([^"]+)"', host)[1]) - scene['start']) < .0001
    placed_audio, export_audio = decode(source, 8000), decode(export, 8000)
    correlation = []
    for at in (2, 18, 35, 52, 65):
        template = placed_audio[round(at * 8000):round((at + 2) * 8000)]
        search = export_audio[round((at + offset - .25) * 8000):round((at + offset + 2.25) * 8000)]
        match = int(np.argmax(correlate(search, template, 'valid', method='fft')))
        correlation.append({'source_at_s': at, 'export_lag_ms': (match / 8000 - .25) * 1000,
                            'correlation': float(np.corrcoef(template, search[match:match + len(template)])[0, 1])})
    placement_file = video / 'placement.json'
    placement = read(placement_file) if placement_file.exists() else None
    raw = decode(video / placement['source'], 48000) if placement else None
    boundaries = []
    word_index = 0
    for i, scene in enumerate(scenes[:-1]):
        after, following = i + 1, scenes[i + 1]
        # Historical timing schemas use exclusive word_end or inclusive word_last.
        if 'word_end' in scene:
            word_index = scene['word_end']
        else:
            word_index = scene['word_last'] + 1
        cut = following['start']
        sampled = math.ceil((cut - 1e-7) * 30) / 30
        speech_start = following.get('speech_start')
        if speech_start is None:
            speech_start = following['words'][0]['start'] + timing.get('pre_roll', 0)
        row = {'after_scene': after, 'next_scene': after + 1, 'planned_visual_s': cut,
               'first_new_video_frame': round(sampled * 30), 'sampled_visual_s': sampled,
               'mapped_next_word_start_s': speech_start,
               'next_word_lead_before_new_visual_ms': max(0, (sampled - speech_start) * 1000),
               'previous_word': native_words[word_index - 1]['text'],
               'next_word': native_words[word_index]['text'],
               'native_previous_end_s': native_words[word_index - 1]['end'],
               'native_next_start_s': native_words[word_index]['start']}
        pause = next((p for p in placement['pauses'] if p['after_scene'] == after), None) if placement else None
        if pause:
            sample = pause['sample']
            before, after_audio = raw[sample - 1200:sample], raw[sample:sample + 1200]
            row.update({'source_cut_s': sample / 48000, 'inserted_silence_s': pause['seconds'],
                        'source_cut_before_25ms_rms_dbfs': rms_db(before),
                        'source_cut_after_25ms_rms_dbfs': rms_db(after_audio),
                        'cut_in_active_signal_screen': max(rms_db(before), rms_db(after_audio)) > -50})
        boundaries.append(row)
    records.append({'slug': item['slug'], 'export': str(export.relative_to(ROOT)),
                    'export_sha256': hashlib.sha256(export.read_bytes()).hexdigest(),
                    'audio_path': str(source.relative_to(ROOT)), 'audio_start_s': offset,
                    'fps': 30, 'video_probe': probe, 'html_scene_starts_match_timing': True,
                    'export_alignment_samples': correlation, 'boundaries': boundaries})
    print(item['slug'], 'early-word metadata seams:',
          [(b['after_scene'], round(b['next_word_lead_before_new_visual_ms'], 3)) for b in boundaries
           if b['next_word_lead_before_new_visual_ms'] > 0])

result = {'method': {'export_lag': 'FFT cross-correlation at 8kHz in five 2s windows per episode; resolution 0.125ms.',
                     'video_sampling': 'First sample at or after planned cut: ceil(cut*30)/30; latest seam 06/07 confirmed by decoding frames 1127 and 1128.',
                     'active_cut_screen': '25ms RMS immediately before and after source cut; flag above -50dBFS is an investigation screen, not a speech/word classifier.',
                     'limitation': 'Native word timestamps are estimates. No perceptual listening; ASR and waveform evidence are separately retained.'},
          'productions': records}
(OUT / 'measurements.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
