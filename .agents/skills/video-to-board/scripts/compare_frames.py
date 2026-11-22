"""Side-by-side proportion & palette comparator for reference clones (adapted from cth9191/animate/tools/compare.mjs).
Places a reference frame beside our rendered board study or motion-preview frame at matched height (960px)
with a 10% proportion grid and quantized palette similarity report.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from clone_measure import trim_flat_borders


def _quantized_palette(rgb: np.ndarray, top_k: int = 6) -> tuple[list[dict], dict[int, float]]:
    pixels = rgb.reshape(-1, 3)[::4]
    total = float(max(1, len(pixels)))
    q = (pixels.astype(np.int32) >> 4)
    keys = (q[:, 0] << 8) | (q[:, 1] << 4) | q[:, 2]
    counts: dict[int, list[float]] = {}
    for px, k in zip(pixels, keys):
        ik = int(k)
        c = counts.get(ik)
        if c is None:
            counts[ik] = [float(px[0]), float(px[1]), float(px[2]), 1.0]
        else:
            c[0] += float(px[0])
            c[1] += float(px[1])
            c[2] += float(px[2])
            c[3] += 1.0
    dist = {k: v[3] / total for k, v in counts.items()}
    top = sorted(counts.values(), key=lambda x: x[3], reverse=True)[:top_k]
    out = []
    for rs, gs, bs, cnt in top:
        col = [int(round(rs / cnt)), int(round(gs / cnt)), int(round(bs / cnt))]
        out.append({'hex': f'#{col[0]:02x}{col[1]:02x}{col[2]:02x}', 'rgb': col, 'share': round(cnt / total, 4)})
    return out, dist


def compare_reference_and_render(
    reference_image: Path,
    ours_image: Path,
    output_image: Path,
    *,
    auto_trim: bool = True,
    draw_grid: bool = True,
    target_height: int = 960,
) -> dict:
    ref_arr = np.array(Image.open(reference_image).convert('RGB'))
    our_arr = np.array(Image.open(ours_image).convert('RGB'))

    ref_box = [0, 0, int(ref_arr.shape[1]), int(ref_arr.shape[0])]
    if auto_trim:
        ref_arr, ref_box = trim_flat_borders(ref_arr)

    ref_pal, ref_dist = _quantized_palette(ref_arr)
    our_pal, our_dist = _quantized_palette(our_arr)

    # Histogram intersection over 3x3x3 coarse neighborhood for perceptual tolerance
    overlap = 0.0
    for k_ref, p_ref in ref_dist.items():
        r0, g0, b0 = (k_ref >> 8) & 15, (k_ref >> 4) & 15, k_ref & 15
        matched = 0.0
        for dr in (-1, 0, 1):
            for dg in (-1, 0, 1):
                for db in (-1, 0, 1):
                    rr, gg, bb = r0 + dr, g0 + dg, b0 + db
                    if 0 <= rr < 16 and 0 <= gg < 16 and 0 <= bb < 16:
                        nk = (rr << 8) | (gg << 4) | bb
                        matched += our_dist.get(nk, 0.0)
        overlap += min(p_ref, matched)

    ref_img = Image.fromarray(ref_arr)
    our_img = Image.fromarray(our_arr)
    rw = max(1, int(round(ref_img.width * target_height / ref_img.height)))
    ow = max(1, int(round(our_img.width * target_height / our_img.height)))
    ref_resized = ref_img.resize((rw, target_height), Image.Resampling.LANCZOS)
    our_resized = our_img.resize((ow, target_height), Image.Resampling.LANCZOS)

    gap = 24
    head = 44
    canvas = Image.new('RGB', (rw + ow + gap * 3, target_height + head + gap), (30, 32, 36))
    canvas.paste(ref_resized, (gap, head))
    canvas.paste(our_resized, (gap * 2 + rw, head))

    draw = ImageDraw.Draw(canvas, 'RGBA')
    draw.text((gap, 14), f'REFERENCE ({ref_img.width}x{ref_img.height})', fill=(235, 235, 235))
    draw.text((gap * 2 + rw, 14), f'OURS ({our_img.width}x{our_img.height}) · palette_match={overlap * 100:.1f}%', fill=(255, 212, 77))

    if draw_grid:
        grid_col = (255, 40, 95, 95)
        for x_start, width in ((gap, rw), (gap * 2 + rw, ow)):
            for k in range(1, 10):
                gx = int(round(x_start + width * k / 10.0))
                gy = int(round(head + target_height * k / 10.0))
                draw.line([(gx, head), (gx, head + target_height)], fill=grid_col, width=1)
                draw.line([(x_start, gy), (x_start + width, gy)], fill=grid_col, width=1)

    output_image.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_image)
    return {
        'output': str(output_image),
        'reference_trimmed_box': ref_box,
        'palette_neighborhood_overlap': round(min(1.0, overlap), 4),
        'reference_palette': ref_pal,
        'ours_palette': our_pal,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, required=True, help='Reference still/frame PNG or JPG')
    parser.add_argument('--ours', type=Path, required=True, help='Rendered board study or motion-preview frame PNG/JPG')
    parser.add_argument('--out', type=Path, required=True, help='Output side-by-side comparison PNG')
    parser.add_argument('--no-trim', action='store_true', help='Disable automatic border/letterbox trimming on reference')
    parser.add_argument('--no-grid', action='store_true', help='Disable 10%% proportion grid overlay')
    args = parser.parse_args()

    res = compare_reference_and_render(
        args.reference,
        args.ours,
        args.out,
        auto_trim=not args.no_trim,
        draw_grid=not args.no_grid,
    )
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
