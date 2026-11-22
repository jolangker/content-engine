"""Precision reference-video measurer for video-to-board clones:
- Motion heatmap & cut beat-grid fitting (adapted from huashu-art-motion/scripts/analyze/breakdown.py)
- Auto-trimmed ground & saturated accent palette extraction (adapted from cth9191/animate/tools/measure/refs.mjs)
- Librosa HPSS percussive onset detection, tempo/beat grid, and vocal-to-BGM ducking/masking curve.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import subprocess

import librosa
import numpy as np
from PIL import Image, ImageDraw

HUE_FAMILIES = (
    'red-orange', 'yellow', 'yellow-green', 'green', 'emerald', 'green-cyan',
    'cyan', 'azure', 'blue', 'violet', 'magenta', 'pink-red',
)


def probe_video(path: Path) -> dict:
    proc = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)],
        capture_output=True, text=True, encoding='utf-8', check=True,
    )
    info = json.loads(proc.stdout)
    vstream = next(s for s in info['streams'] if s['codec_type'] == 'video')
    num, den = vstream['r_frame_rate'].split('/')
    return {
        'width': int(vstream['width']),
        'height': int(vstream['height']),
        'fps': float(num) / float(den),
        'duration': float(info['format']['duration']),
        'has_audio': any(s['codec_type'] == 'audio' for s in info['streams']),
    }


def decode_video_rgb(path: Path, target_w: int, target_h: int, sample_fps: float) -> np.ndarray:
    vf = f'fps={sample_fps},scale={target_w}:{target_h}:flags=area'
    proc = subprocess.run(
        ['ffmpeg', '-v', 'error', '-i', str(path), '-an', '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'],
        capture_output=True, check=True,
    )
    frame_bytes = target_w * target_h * 3
    n_frames = len(proc.stdout) // frame_bytes
    if n_frames < 2:
        raise ValueError(f'Too few video frames decoded from {path}')
    return np.frombuffer(proc.stdout[:n_frames * frame_bytes], dtype=np.uint8).reshape(n_frames, target_h, target_w, 3)


def decode_audio_mono(path: Path, sr: int = 22050) -> np.ndarray:
    proc = subprocess.run(
        ['ffmpeg', '-v', 'error', '-i', str(path), '-vn', '-ac', '1', '-ar', str(sr), '-f', 'f32le', 'pipe:1'],
        capture_output=True, check=True,
    )
    return np.frombuffer(proc.stdout, dtype='<f4').astype(np.float32)


def trim_flat_borders(rgb: np.ndarray) -> tuple[np.ndarray, list[int]]:
    """Drop flat screenshot letterboxing/borders within Manhattan distance 42 of corner pixel."""
    h, w, _ = rgb.shape
    corner = rgb[0, 0].astype(np.int16)
    diff = np.abs(rgb.astype(np.int16) - corner).sum(axis=-1)
    row_flat = (diff < 42).all(axis=1)
    col_flat = (diff < 42).all(axis=0)
    y0 = 0
    while y0 < h - 1 and row_flat[y0]:
        y0 += 1
    y1 = h - 1
    while y1 > y0 and row_flat[y1]:
        y1 -= 1
    x0 = 0
    while x0 < w - 1 and col_flat[x0]:
        x0 += 1
    x1 = w - 1
    while x1 > x0 and col_flat[x1]:
        x1 -= 1
    return rgb[y0:y1 + 1, x0:x1 + 1], [int(x0), int(y0), int(x1 - x0 + 1), int(y1 - y0 + 1)]


def extract_palette_and_accents(frames_rgb: np.ndarray, top_k: int = 8, caption_region_norm: list[float] | None = None) -> dict:
    """Quantize 16-level colour buckets across representative frames and isolate saturated accent hue families."""
    idxs = np.linspace(0, len(frames_rgb) - 1, min(12, len(frames_rgb)), dtype=int)
    sampled = []
    trim_box = [0, 0, int(frames_rgb.shape[2]), int(frames_rgb.shape[1])]
    for k, i in enumerate(idxs):
        fr, box = trim_flat_borders(frames_rgb[i])
        if k == 0:
            trim_box = box
        if caption_region_norm:
            fh, fw, _ = fr.shape
            rx0, ry0, rx1, ry1 = caption_region_norm
            mask = np.ones((fh, fw), dtype=bool)
            mask[max(0, int(ry0 * fh)):min(fh, int(math.ceil(ry1 * fh))),
                 max(0, int(rx0 * fw)):min(fw, int(math.ceil(rx1 * fw)))] = False
            sampled.append(fr[mask])
        else:
            sampled.append(fr.reshape(-1, 3))

    pixels = np.concatenate(sampled, axis=0)[::2]
    if len(pixels) == 0:
        return {'content_box': trim_box, 'palette': [], 'accents': []}

    buckets: dict[int, list[float]] = {}
    q = (pixels.astype(np.int32) >> 4)
    keys = (q[:, 0] << 8) | (q[:, 1] << 4) | q[:, 2]
    for px, key in zip(pixels, keys):
        b = buckets.get(int(key))
        if b is None:
            buckets[int(key)] = [float(px[0]), float(px[1]), float(px[2]), 1.0]
        else:
            b[0] += float(px[0])
            b[1] += float(px[1])
            b[2] += float(px[2])
            b[3] += 1.0

    total = float(len(pixels))
    ranked = sorted(buckets.values(), key=lambda v: v[3], reverse=True)[:top_k]
    palette = []
    for r_sum, g_sum, b_sum, cnt in ranked:
        rgb = [int(round(r_sum / cnt)), int(round(g_sum / cnt)), int(round(b_sum / cnt))]
        palette.append({
            'hex': f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}',
            'rgb': rgb,
            'share': round(cnt / total, 4),
        })

    # Saturated accents grouped into 12 x 30-degree hue families
    fams: list[list[tuple[int, int, int, float]]] = [[] for _ in range(12)]
    n_acc = 0
    for r, g, b in pixels[::2]:
        ri, gi, bi = int(r), int(g), int(b)
        mx, mn = max(ri, gi, bi), min(ri, gi, bi)
        sat = (mx - mn) / mx if mx > 0 else 0.0
        if mx < 120 or sat < 0.35:
            continue
        if mx == mn:
            hue = 0.0
        elif mx == ri:
            hue = ((gi - bi) / (mx - mn)) % 6
        elif mx == gi:
            hue = (bi - ri) / (mx - mn) + 2.0
        else:
            hue = (ri - gi) / (mx - mn) + 4.0
        deg = (hue * 60.0) % 360.0
        luma = 0.2126 * ri + 0.7152 * gi + 0.0722 * bi
        fams[int(deg // 30) % 12].append((ri, gi, bi, luma))
        n_acc += 1

    accents = []
    if n_acc > 0:
        for fam_idx, items in enumerate(fams):
            if len(items) < max(3, n_acc * 0.03):
                continue
            items_sorted = sorted(items, key=lambda x: x[3], reverse=True)
            cut = max(1, len(items_sorted) // 5)
            core_slice = items_sorted[:cut]
            core_rgb = [int(np.median([p[c] for p in core_rgb_src])) for c, core_rgb_src in enumerate([core_slice, core_slice, core_slice])]
            accents.append({
                'family': HUE_FAMILIES[fam_idx],
                'share_of_accents': round(len(items) / n_acc, 3),
                'core_hex': f'#{core_rgb[0]:02x}{core_rgb[1]:02x}{core_rgb[2]:02x}',
                'core_rgb': core_rgb,
            })
        accents.sort(key=lambda x: x['share_of_accents'], reverse=True)

    return {'content_box': trim_box, 'palette': palette, 'accents': accents[:5]}


def fit_cut_beat_grid(cut_seconds: list[float], fps: float) -> dict | None:
    """Fit t0 + k * step grid to detected cut timestamps (huashu breakdown.py method)."""
    if len(cut_seconds) < 4:
        return None
    arr = np.array(cut_seconds, dtype=np.float64)
    max_step = float(np.diff(arr).max())
    if max_step < 0.25:
        return None
    tol = max(0.06, 1.5 / max(10.0, fps))
    best = None
    for step in np.arange(0.25, min(max_step + 0.01, 12.0), 0.02):
        for t0 in arr[:3]:
            k = np.round((arr - t0) / step)
            res = arr - (t0 + k * step)
            inliers = np.abs(res) <= tol
            if inliers.mean() < 0.75:
                continue
            t0_ref = float(t0 + res[inliers].mean())
            res_ref = arr - (t0_ref + k * step)
            score = (round(float(inliers.mean()), 3), float(step))
            if best is None or score > best[0]:
                best = (
                    score,
                    round(float(step), 3),
                    round(t0_ref, 3),
                    round(float(np.abs(res_ref[inliers]).max()), 3),
                    round(60.0 / float(step), 1),
                )
    if not best:
        return None
    _, step_s, t0_s, max_err_s, implied_bpm = best
    return {
        't0_seconds': t0_s,
        'step_seconds': step_s,
        'max_residual_seconds': max_err_s,
        'implied_bpm_quarter': implied_bpm,
    }


def build_motion_heatmap(
    frames_rgb: np.ndarray,
    sample_fps: float,
    out_image: Path,
    *,
    cut_thresh: float = 16.0,
    caption_region_norm: list[float] | None = None,
) -> dict:
    """Detect cuts, measure per-segment motion area, and render red-overlay motion heatmap contact sheet."""
    gray = (0.299 * frames_rgb[..., 0] + 0.587 * frames_rgb[..., 1] + 0.114 * frames_rgb[..., 2]).astype(np.float32)
    n, h, w = gray.shape
    mask = np.ones((h, w), dtype=bool)
    if caption_region_norm:
        rx0, ry0, rx1, ry1 = caption_region_norm
        mask[max(0, int(ry0 * h)):min(h, int(math.ceil(ry1 * h))),
             max(0, int(rx0 * w)):min(w, int(math.ceil(rx1 * w)))] = False

    diffs = np.abs(np.diff(gray, axis=0))
    mean_diffs = np.array([float(d[mask].mean()) if mask.any() else float(d.mean()) for d in diffs])

    debounce = max(2, int(round(0.45 * sample_fps)))
    cuts_idx: list[int] = []
    for i in range(1, len(mean_diffs)):
        lo = max(0, i - 3)
        hi = min(len(mean_diffs), i + 4)
        neigh = [mean_diffs[k] for k in range(lo, hi) if k != i]
        neigh_med = float(np.median(neigh)) if neigh else 0.0
        is_hard = mean_diffs[i] > cut_thresh and mean_diffs[i - 1] <= cut_thresh * 0.75
        is_spike = mean_diffs[i] >= 5.5 and mean_diffs[i] >= max(5.5, 2.6 * (neigh_med + 0.25))
        if is_hard or is_spike:
            if not cuts_idx or (i - cuts_idx[-1]) >= debounce:
                cuts_idx.append(i + 1)

    bounds = [0] + cuts_idx + [n]
    tiles: list[Image.Image] = []
    segments: list[dict] = []

    for seg_i in range(len(bounds) - 1):
        a0 = bounds[seg_i] + (1 if seg_i > 0 else 0)
        b0 = bounds[seg_i + 1]
        t_start = round(bounds[seg_i] / sample_fps, 2)
        t_end = round(bounds[seg_i + 1] / sample_fps, 2)
        if b0 - a0 < 2:
            segments.append({'segment': seg_i + 1, 'start_s': t_start, 'end_s': t_end, 'active_area': 0.0})
            continue
        seq = gray[a0:b0]
        max_delta = np.abs(np.diff(seq, axis=0)).max(axis=0)
        active_mask = (max_delta > 20.0) & mask
        active_share = float(active_mask.sum() / max(1, mask.sum()))
        segments.append({
            'segment': seg_i + 1,
            'start_s': t_start,
            'end_s': t_end,
            'active_area': round(active_share, 4),
        })

        base = Image.fromarray(seq[0].astype(np.uint8)).convert('RGB')
        heat_arr = np.zeros((h, w, 3), dtype=np.uint8)
        heat_arr[..., 0] = np.clip(max_delta * 3.5, 0, 255).astype(np.uint8)
        if not mask.all():
            heat_arr[~mask, 2] = 70  # subtle blue tint over masked caption region
        blended = Image.blend(base, Image.fromarray(heat_arr), 0.55)
        draw = ImageDraw.Draw(blended)
        draw.rectangle([0, 0, w, 22], fill=(0, 0, 0))
        draw.text((6, 4), f'S{seg_i + 1} {t_start:.1f}-{t_end:.1f}s act={active_share * 100:.1f}%', fill=(255, 220, 77))
        tiles.append(blended)

    if tiles:
        cols = min(4, len(tiles))
        rows = math.ceil(len(tiles) / cols)
        sheet = Image.new('RGB', (cols * w, rows * h), (20, 20, 20))
        for idx, tile in enumerate(tiles):
            sheet.paste(tile, ((idx % cols) * w, (idx // cols) * h))
        out_image.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(out_image, quality=88)

    cut_seconds = [round(c / sample_fps, 3) for c in cuts_idx]
    return {
        'cuts_seconds': cut_seconds,
        'segment_count': len(segments),
        'mean_active_area': round(float(np.mean([s['active_area'] for s in segments])), 4) if segments else 0.0,
        'segments': segments,
        'cut_grid': fit_cut_beat_grid(cut_seconds, sample_fps),
    }


def analyze_reference_audio(video_path: Path, stems_dir: Path | None = None, sr: int = 22050) -> dict:
    """Extract librosa HPSS percussive onsets, tempo/beats, and stem-level ducking curve when stems exist."""
    y = decode_audio_mono(video_path, sr=sr)
    if y.size < sr // 2 or not np.any(y):
        return {'available': False}

    y_harm, y_perc = librosa.effects.hpss(y)
    onset_env = librosa.onset.onset_strength(y=y_perc, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units='frames', backtrack=True)
    onset_times = [round(float(t), 3) for t in librosa.frames_to_time(onset_frames, sr=sr)]
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    tempo_val = float(np.atleast_1d(tempo)[0])
    beat_times = [round(float(t), 3) for t in librosa.frames_to_time(beat_frames, sr=sr)]
    perc_ratio = round(float(np.sqrt(np.mean(y_perc ** 2)) / (np.sqrt(np.mean(y ** 2)) + 1e-12)), 4)

    result: dict = {
        'available': True,
        'tempo_bpm': round(tempo_val, 2),
        'beat_count': len(beat_times),
        'beats_seconds': beat_times[:120],
        'percussive_onset_count': len(onset_times),
        'percussive_onsets_seconds': onset_times[:150],
        'percussive_energy_ratio': perc_ratio,
    }

    # If rea-video stems (vocals.wav + music.wav) exist, measure exact BGM ducking & vocal-band clearance!
    vocals_wav = (stems_dir / 'vocals.wav') if stems_dir else None
    music_wav = (stems_dir / 'music.wav') if stems_dir else None
    if vocals_wav and vocals_wav.is_file() and music_wav and music_wav.is_file():
        v = decode_audio_mono(vocals_wav, sr=sr)
        m = decode_audio_mono(music_wav, sr=sr)
        n = min(len(v), len(m))
        if n > sr // 2:
            hop = 512
            v_rms = librosa.feature.rms(y=v[:n], hop_length=hop)[0]
            m_rms = librosa.feature.rms(y=m[:n], hop_length=hop)[0]
            v_peak = float(v_rms.max()) + 1e-12
            speaking = v_rms >= (v_peak * 0.12)
            gaps = ~speaking & (m_rms > 1e-5)
            bgm_during_speech_db = round(float(20.0 * np.log10(np.median(m_rms[speaking]) + 1e-12)), 2) if speaking.any() else None
            bgm_in_gaps_db = round(float(20.0 * np.log10(np.median(m_rms[gaps]) + 1e-12)), 2) if gaps.any() else None
            voice_during_speech_db = round(float(20.0 * np.log10(np.median(v_rms[speaking]) + 1e-12)), 2) if speaking.any() else None
            duck_depth = (
                round(bgm_in_gaps_db - bgm_during_speech_db, 2)
                if (bgm_in_gaps_db is not None and bgm_during_speech_db is not None) else 0.0
            )
            result['stems_ducking'] = {
                'voice_rms_db': voice_during_speech_db,
                'bgm_during_speech_db': bgm_during_speech_db,
                'bgm_in_gaps_db': bgm_in_gaps_db,
                'ducking_depth_db': duck_depth,
                'voice_to_bgm_margin_db': (
                    round(voice_during_speech_db - bgm_during_speech_db, 2)
                    if (voice_during_speech_db is not None and bgm_during_speech_db is not None) else None
                ),
            }
    return result


def measure_clone_reference(
    video_path: Path,
    out_dir: Path,
    *,
    caption_region: list[float] | None = None,
    stems_dir: Path | None = None,
    sample_fps: float = 6.0,
) -> dict:
    video_path = Path(video_path).resolve()
    out_dir = Path(out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    meta = probe_video(video_path)
    aspect = meta['width'] / meta['height']
    target_w = 270 if aspect < 1.0 else 480
    target_h = max(2, int(round(target_w / aspect / 2) * 2))

    region_norm = None
    if caption_region and len(caption_region) == 4:
        x, y, rw, rh = caption_region
        region_norm = [x / meta['width'], y / meta['height'], (x + rw) / meta['width'], (y + rh) / meta['height']]

    frames_rgb = decode_video_rgb(video_path, target_w, target_h, sample_fps=sample_fps)
    heatmap_path = out_dir / 'motion_heatmap.jpg'
    motion_info = build_motion_heatmap(frames_rgb, sample_fps, heatmap_path, caption_region_norm=region_norm)
    palette_info = extract_palette_and_accents(frames_rgb, caption_region_norm=region_norm)

    auto_stems = stems_dir
    if auto_stems is None and (out_dir.parent / 'stems').is_dir():
        auto_stems = out_dir.parent / 'stems'
    audio_info = analyze_reference_audio(video_path, stems_dir=auto_stems) if meta['has_audio'] else {'available': False}

    # Quantify share of visual cuts landing within +-80ms of a percussive audio onset
    cuts = motion_info['cuts_seconds']
    onsets = audio_info.get('percussive_onsets_seconds') or []
    synced_cuts = sum(1 for c in cuts if any(abs(c - o) <= 0.085 for o in onsets)) if (cuts and onsets) else 0

    report = {
        'source': video_path.name,
        'format': {'width': meta['width'], 'height': meta['height'], 'fps': round(meta['fps'], 3), 'duration_s': round(meta['duration'], 3)},
        'motion': {
            **motion_info,
            'heatmap_image': heatmap_path.name if heatmap_path.is_file() else None,
        },
        'visual_palette': palette_info,
        'audio_dsp': {
            **audio_info,
            'cuts_near_onset_share': round(synced_cuts / len(cuts), 3) if cuts else None,
        },
    }
    (out_dir / 'clone_metrics.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', type=Path, required=True, help='Reference video clip path')
    parser.add_argument('--out', type=Path, required=True, help='Output directory for clone_metrics.json and motion_heatmap.jpg')
    parser.add_argument('--caption-region', help='Burned-in caption box X,Y,W,H in source pixels to mask during motion & palette analysis')
    parser.add_argument('--stems-dir', type=Path, help='Optional rea-video stems/ folder containing vocals.wav and music.wav')
    parser.add_argument('--sample-fps', type=float, default=6.0)
    args = parser.parse_args()

    region = [float(x) for x in args.caption_region.split(',')] if args.caption_region else None
    report = measure_clone_reference(args.video, args.out, caption_region=region, stems_dir=args.stems_dir, sample_fps=args.sample_fps)
    print(json.dumps({
        'source': report['source'],
        'duration_s': report['format']['duration_s'],
        'segments': report['motion']['segment_count'],
        'mean_active_area': report['motion']['mean_active_area'],
        'top_palette': [p['hex'] for p in report['visual_palette']['palette'][:4]],
        'top_accents': [a['core_hex'] for a in report['visual_palette']['accents'][:3]],
        'tempo_bpm': report['audio_dsp'].get('tempo_bpm'),
        'cuts_near_onset_share': report['audio_dsp'].get('cuts_near_onset_share'),
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
