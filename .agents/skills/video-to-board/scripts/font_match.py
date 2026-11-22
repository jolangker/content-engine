"""Metric font matcher for video-to-board clones (adapted from cinetic/scripts/font-match.mjs).
Measures ink width, x-height, cap height, and stem thickness on a reference crop or numeric target,
then ranks local OFL fonts across weights and tracking in headless Chromium.
"""
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
import re

import numpy as np
from PIL import Image


def discover_local_ofl_fonts(project_root: Path) -> list[dict]:
    """Discover bundled OFL .ttf/.woff2 font files across boards/ and hyperframes frame presets."""
    search_roots = [
        project_root / 'boards',
        project_root / '.agents' / 'skills' / 'hyperframes' / 'assets' / 'frame-presets',
    ]
    seen_names: set[str] = set()
    fonts: list[dict] = []
    for root in search_roots:
        if not root.is_dir():
            continue
        for f in sorted(root.rglob('*')):
            if f.suffix.lower() not in ('.ttf', '.woff2', '.otf') or 'italic' in f.stem.lower():
                continue
            family = re.sub(r'[-_](?:Regular|Bold|ExtraBold|SemiBold|Medium|Light|\d{3}|Variable.*)$', '', f.stem, flags=re.I)
            key = f'{family.lower()}:{f.stem.lower()}'
            if key in seen_names:
                continue
            seen_names.add(key)
            fonts.append({'name': f.stem, 'family': family, 'path': f.resolve()})
    return fonts


def measure_crop_ink_metrics(image_path: Path, box: list[float] | None = None) -> dict:
    """Measure target text ink width, height, and median vertical stem thickness from a reference image crop."""
    img = Image.open(image_path).convert('L')
    arr = np.array(img, dtype=np.float32)
    if box and len(box) == 4:
        h, w = arr.shape
        x0, y0, x1, y1 = box
        if max(box) <= 1.0:
            x0, y0, x1, y1 = x0 * w, y0 * h, x1 * w, y1 * h
        arr = arr[max(0, int(y0)):min(h, int(y1)), max(0, int(x0)):min(w, int(x1))]

    if arr.size == 0:
        raise ValueError('Empty crop box for font measurement')

    # Determine polarity: is ink darker or lighter than background border?
    border = np.concatenate([arr[0, :], arr[-1, :], arr[:, 0], arr[:, -1]])
    bg_val = float(np.median(border))
    contrast = np.abs(arr - bg_val)
    thresh = max(24.0, float(contrast.max()) * 0.42)
    ink = contrast >= thresh
    if not ink.any():
        raise ValueError('No legible text ink contrast detected in crop')

    ys, xs = np.where(ink)
    ink_w = int(xs.max() - xs.min() + 1)
    ink_h = int(ys.max() - ys.min() + 1)
    sub = ink[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

    # Dense horizontal row band (~x-height) vs full cap/ascender height
    row_density = sub.mean(axis=1)
    dense_rows = np.where(row_density >= max(0.12, float(row_density.max()) * 0.45))[0]
    xh = int(dense_rows[-1] - dense_rows[0] + 1) if len(dense_rows) >= 2 else int(round(ink_h * 0.72))
    xh = max(6, min(ink_h, xh))

    # Horizontal run lengths inside the middle band estimate vertical stem thickness
    mid_band = sub[max(0, sub.shape[0] // 3):max(1, (2 * sub.shape[0]) // 3), :]
    runs = []
    for row in mid_band:
        edges = np.diff(np.r_[0, row.astype(np.int8), 0])
        starts = np.where(edges == 1)[0]
        ends = np.where(edges == -1)[0]
        runs.extend(int(e - s) for s, e in zip(starts, ends) if 1 <= (e - s) <= max(4, ink_h // 2))
    stem = float(np.median(runs)) if runs else max(2.0, ink_h * 0.14)

    return {
        'ink_width_px': ink_w,
        'cap_height_px': ink_h,
        'x_height_px': xh,
        'stem_px': round(stem, 2),
    }


def match_fonts(
    text: str,
    target_metrics: dict,
    candidate_fonts: list[dict],
    *,
    weights: tuple[int, ...] = (400, 500, 600, 700, 800),
    top_n: int = 6,
    sheet_path: Path | None = None,
) -> list[dict]:
    """Render candidate fonts in headless Chromium, match x-height & stem weight, and rank by natural width fit."""
    from playwright.sync_api import sync_playwright

    if not candidate_fonts:
        raise ValueError('No candidate font files discovered or supplied')

    font_faces_css = []
    font_entries = []
    for idx, f in enumerate(candidate_fonts):
        alias = f'CandFont_{idx}'
        ext = f['path'].suffix.lower().lstrip('.')
        fmt = 'woff2' if ext == 'woff2' else ('opentype' if ext == 'otf' else 'truetype')
        b64 = base64.b64encode(f['path'].read_bytes()).decode('ascii')
        font_faces_css.append(
            f'@font-face {{ font-family: "{alias}"; src: url("data:font/{ext};base64,{b64}") format("{fmt}"); font-weight: 100 900; }}'
        )
        font_entries.append({'alias': alias, 'name': f['name'], 'family': f['family'], 'path': str(f['path'])})

    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
    {' '.join(font_faces_css)}
    body {{ margin: 0; background: #fff; color: #000; }}
    </style></head><body><canvas id="cv" width="2400" height="320"></canvas></body></html>"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1200, 'height': 800})
        page.set_content(html, wait_until='load')
        page.evaluate('() => document.fonts.ready')

        ranked = page.evaluate(
            """([entries, text, target, weights]) => {
                const cv = document.getElementById('cv');
                const ctx = cv.getContext('2d', { willReadFrequently: true });

                function measureRender(alias, weight, fontSizePx, trackingEm) {
                    ctx.fillStyle = '#fff';
                    ctx.fillRect(0, 0, cv.width, cv.height);
                    ctx.fillStyle = '#000';
                    ctx.font = `${weight} ${fontSizePx}px "${alias}", sans-serif`;
                    if ('letterSpacing' in ctx) ctx.letterSpacing = `${(trackingEm * fontSizePx).toFixed(2)}px`;
                    ctx.textBaseline = 'alphabetic';
                    ctx.fillText(text, 40, 220);
                    const img = ctx.getImageData(0, 0, cv.width, cv.height).data;
                    let x0 = cv.width, y0 = cv.height, x1 = 0, y1 = 0;
                    const rowCounts = new Float32Array(cv.height);
                    for (let y = 0; y < cv.height; y++) {
                        let cnt = 0;
                        for (let x = 0; x < cv.width; x++) {
                            const ink = img[(y * cv.width + x) * 4] < 140;
                            if (ink) {
                                if (x < x0) x0 = x;
                                if (x > x1) x1 = x;
                                if (y < y0) y0 = y;
                                if (y > y1) y1 = y;
                                cnt++;
                            }
                        }
                        rowCounts[y] = cnt;
                    }
                    if (x1 <= x0 || y1 <= y0) return null;
                    const inkW = x1 - x0 + 1;
                    const inkH = y1 - y0 + 1;
                    let maxRow = 0;
                    for (let y = y0; y <= y1; y++) if (rowCounts[y] > maxRow) maxRow = rowCounts[y];
                    let dy0 = y0, dy1 = y1;
                    while (dy0 < y1 && rowCounts[dy0] < maxRow * 0.45) dy0++;
                    while (dy1 > dy0 && rowCounts[dy1] < maxRow * 0.45) dy1--;
                    const xh = Math.max(4, dy1 - dy0 + 1);

                    // Stem width in mid-band
                    const runs = [];
                    const my0 = Math.floor(y0 + inkH * 0.35), my1 = Math.ceil(y0 + inkH * 0.65);
                    for (let y = my0; y <= my1; y++) {
                        let run = 0;
                        for (let x = x0; x <= x1 + 1; x++) {
                            const ink = x <= x1 && img[(y * cv.width + x) * 4] < 140;
                            if (ink) run++;
                            else if (run > 0) {
                                if (run <= inkH * 0.6) runs.push(run);
                                run = 0;
                            }
                        }
                    }
                    runs.sort((a, b) => a - b);
                    const stem = runs.length ? runs[Math.floor(runs.length / 2)] : inkH * 0.14;
                    return { inkW, inkH, xh, stem };
                }

                // Measure lowercase probe to calibrate x-height ratio cleanly even on all-caps text
                const results = [];
                for (const ent of entries) {
                    const probe = measureRender(ent.alias, 600, 100, 0);
                    if (!probe) continue;
                    const fittedSize = Math.max(14, Math.round(100 * (target.cap_height_px / probe.inkH)));
                    let bestW = null;
                    for (const w of weights) {
                        const m = measureRender(ent.alias, w, fittedSize, 0);
                        if (!m) continue;
                        const stemErr = Math.abs(m.stem - target.stem_px);
                        if (!bestW || stemErr < bestW.stemErr) {
                            bestW = { weight: w, m, stemErr };
                        }
                    }
                    if (!bestW) continue;
                    const natDeltaPct = ((bestW.m.inkW - target.ink_width_px) / Math.max(1, target.ink_width_px)) * 100;
                    const charSpaces = Math.max(1, text.length - 1);
                    const neededTrackingEm = (target.ink_width_px - bestW.m.inkW) / (charSpaces * fittedSize);
                    results.push({
                        name: ent.name,
                        family: ent.family,
                        path: ent.path,
                        alias: ent.alias,
                        matched_weight: bestW.weight,
                        matched_font_size_px: fittedSize,
                        natural_width_px: bestW.m.inkW,
                        natural_width_delta_pct: +natDeltaPct.toFixed(2),
                        recommended_letter_spacing_em: +neededTrackingEm.toFixed(4),
                        measured_stem_px: +bestW.m.stem.toFixed(2),
                        score: +(Math.abs(natDeltaPct) + bestW.stemErr * 2.5).toFixed(3),
                    });
                }
                results.sort((a, b) => a.score - b.score);
                return results;
            }""",
            [font_entries, text, target_metrics, list(weights)],
        )

        top_picks = ranked[:top_n]
        if sheet_path and top_picks:
            rows_html = ''.join(
                f'<div style="padding:14px 24px;border-bottom:1px solid #ddd;">'
                f'<div style="font:13px monospace;color:#555;margin-bottom:4px;">'
                f'#{i + 1} {r["name"]} · w={r["matched_weight"]} · size={r["matched_font_size_px"]}px · '
                f'track={r["recommended_letter_spacing_em"]:+.3f}em · widthΔ={r["natural_width_delta_pct"]:+.1f}%</div>'
                f'<div style="font-family:\'{r["alias"]}\';font-weight:{r["matched_weight"]};'
                f'font-size:{min(64, r["matched_font_size_px"])}px;letter-spacing:{r["recommended_letter_spacing_em"]}em;">{text}</div>'
                f'</div>'
                for i, r in enumerate(top_picks)
            )
            page.set_content(
                f'<!doctype html><html><head><meta charset="utf-8"><style>{" ".join(font_faces_css)} '
                f'body{{margin:0;background:#F8F9F5;color:#172B3B;}}</style></head><body>{rows_html}</body></html>',
                wait_until='load',
            )
            page.evaluate('() => document.fonts.ready')
            sheet_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(sheet_path), full_page=True)

        browser.close()

    for r in top_picks:
        r.pop('alias', None)
    return top_picks


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--text', required=True, help='Exact sample text line visible in the reference')
    parser.add_argument('--crop', type=Path, help='Reference image or crop containing --text')
    parser.add_argument('--box', help='Optional x0,y0,x1,y1 crop coordinates inside --crop (px or 0..1)')
    parser.add_argument('--target-width', type=int, help='Direct target ink width in px (if --crop is omitted)')
    parser.add_argument('--target-height', type=int, help='Direct target cap/ink height in px (if --crop is omitted)')
    parser.add_argument('--target-stem', type=float, default=6.0, help='Direct target stem thickness in px')
    parser.add_argument('--candidates', help='Optional comma-separated font file paths to test alongside discovered OFL fonts')
    parser.add_argument('--project-root', type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument('--top', type=int, default=6)
    parser.add_argument('--json', type=Path, help='Write full match report to JSON')
    parser.add_argument('--sheet', type=Path, help='Optional PNG comparison sheet of top ranked faces')
    args = parser.parse_args()

    if args.crop:
        box = [float(v) for v in args.crop and (args.box.split(',') if args.box else [])] or None
        target = measure_crop_ink_metrics(args.crop, box=box)
    elif args.target_width and args.target_height:
        target = {
            'ink_width_px': args.target_width,
            'cap_height_px': args.target_height,
            'x_height_px': round(args.target_height * 0.72),
            'stem_px': args.target_stem,
        }
    else:
        parser.error('Provide either --crop <image> or --target-width and --target-height')

    fonts = discover_local_ofl_fonts(args.project_root.resolve())
    if args.candidates:
        for raw in args.candidates.split(','):
            p = Path(raw.strip()).resolve()
            if p.is_file():
                fonts.append({'name': p.stem, 'family': p.stem, 'path': p})

    matches = match_fonts(args.text, target, fonts, top_n=args.top, sheet_path=args.sheet)
    payload = {'target': target, 'text': args.text, 'candidates_tested': len(fonts), 'matches': matches}
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
