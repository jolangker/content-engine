"""Generate source/placed-waveform proof and optional local listening excerpts."""
from pathlib import Path
import json
import subprocess

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
audit = json.loads((OUT / 'measurements.json').read_text(encoding='utf-8'))
fig, axes = plt.subplots(3, 2, figsize=(14, 9), layout='constrained')
examples = []
for row, (slug, n, word) in enumerate([
        ('gua-kira-udah-kelihatan', 8, 'Ini'),
        ('coba-hal-baru-berdua', 6, 'Lo'),
        ('terima-kasih-yang-melihat', 14, 'Jadi')]):
    prod = next(p for p in audit['productions'] if p['slug'] == slug)
    boundary = next(b for b in prod['boundaries'] if b['after_scene'] == n)
    video = ROOT / 'productions' / slug / 'video'
    placement = json.loads((video / 'placement.json').read_text(encoding='utf-8'))

    def decode(path):
        return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path),
                              '-ac', '1', '-ar', '48000', '-f', 'f32le', 'pipe:1'],
                              capture_output=True, check=True).stdout, '<f4')

    source = decode(video / placement['source'])
    placed = decode(ROOT / prod['audio_path'])
    cut, visual = boundary['source_cut_s'], boundary['planned_visual_s']
    pause, actual = boundary['inserted_silence_s'], boundary['sampled_visual_s']
    # Find the end of the last >=50ms quiet run before each selected source cut.
    # Test three thresholds so these estimates do not pretend to be phoneme truth.
    origin = round((cut - .7) * 48000)
    crop = source[origin:round((cut + .25) * 48000)]
    frames = crop[:len(crop) // 240 * 240].reshape(-1, 240)
    db = 20 * np.log10(np.maximum(np.sqrt(np.mean(frames ** 2, axis=1)), 1e-10))
    onsets = []
    for threshold in (-55, -50, -45):
        quiet_start, intervals = None, []
        for i, quiet in enumerate(db < threshold):
            if quiet and quiet_start is None:
                quiet_start = i
            if quiet_start is not None and (not quiet or i == len(db) - 1):
                end = i if not quiet else i + 1
                if end - quiet_start >= 10 and origin / 48000 + end * .005 <= cut:
                    intervals.append((quiet_start, end))
                quiet_start = None
        assert intervals, (slug, threshold)
        onset = origin / 48000 + intervals[-1][1] * .005
        onsets.append({'threshold_dbfs': threshold, 'source_signal_onset_s': onset,
                       'signal_before_pause_ms': (cut - onset) * 1000,
                       'placed_signal_onset_s': onset + visual - pause - cut})
    examples.append({'slug': slug, 'after_scene': n, 'following_word': word,
                     'source_cut_s': cut, 'inserted_pause_s': pause,
                     'placed_pause_start_s': visual - pause, 'planned_visual_s': visual,
                     'sampled_visual_s': actual, 'onset_estimates': onsets,
                     'limitation': '5ms RMS windows, >=50ms preceding quiet, thresholds -55/-50/-45 dBFS. Signal onset is not phoneme-level ground truth; independent ASR supports word identity.'})
    for col, (wave, start, end) in enumerate([
            (source, cut - .5, cut + .5),
            (placed, visual - pause - .5, visual + .5)]):
        ax = axes[row, col]
        lo, hi = round(start * 48000), round(end * 48000)
        ax.plot(np.arange(lo, hi, 3) / 48000, wave[lo:hi:3], lw=.45, color='#302B28')
        ax.set_xlim(start, end)
        ax.grid(alpha=.18)
        ax.set_xlabel('Seconds')
        ax.set_ylabel('Amplitude')
        if col == 0:
            ax.axvline(cut, color='#A34F3F', label='Insertion cut')
            ax.axvline(boundary['native_next_start_s'], color='#4477AA', ls='--', label='Native next-word timestamp')
            ax.set_title(f'{slug} | {n:02d} > {n+1:02d} | source')
        else:
            ax.axvspan(visual - pause, visual, color='#D8C8B5', alpha=.7, label='Inserted silence')
            ax.axvline(actual, color='#A34F3F', label='First new video frame')
            ax.axvline(boundary['mapped_next_word_start_s'], color='#4477AA', ls='--', label='Mapped next-word timestamp')
            ax.set_title('Placed WAV: waveform split around inserted silence')
        ax.legend(fontsize=7, loc='upper right')
    for label, path, center in [('source', video / placement['source'], cut),
                                ('export', ROOT / prod['export'], actual)]:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(path), '-ss', str(center - 2),
                        '-t', '4', '-ac', '1', '-ar', '48000', str(OUT / f'{slug}-{label}-seam{n:02d}.wav')], check=True)
fig.suptitle('Ruang di Antara: source cut versus placed narration\nActive waveform at a cut is a risk indicator; word identity requires independent alignment/listening.', fontsize=14)
fig.savefig(OUT / 'waveform-evidence.png', dpi=150)
(OUT / 'selected-onsets.json').write_text(json.dumps(examples, indent=2) + '\n', encoding='utf-8')
print('Wrote waveform proof, onset estimates, and six 4-second listening excerpts.')
