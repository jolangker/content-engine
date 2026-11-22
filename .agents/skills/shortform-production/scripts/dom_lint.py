"""Headless Playwright DOM anti-slop linter (motionmaxxing G5 + pinned chrome) and on-screen text read-time verifier (readcheck) for HyperFrames projects."""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import math
from pathlib import Path
import re
import threading

from episode_qa import composition_digest, is_captions, load_contract, load_root

CJK_RE = re.compile(r'[\u3400-\u9fff\u3040-\u30ff\uac00-\ud7af]')
ZINC_PALETTE = ((0xD4, 0xD4, 0xD8), (0xA1, 0xA1, 0xAA), (0x71, 0x71, 0x7A), (0x52, 0x52, 0x5B))

COUNTER_NUM_RE = re.compile(r'^\s*0?\d{1,2}\s*(?:[/—–·]|-(?=\s*[A-Za-z]{3,}))\s*(?:0?\d{1,2}\b|[A-Za-z]{3,})')
COUNTER_WORD_RE = re.compile(r'^\s*(?:chapter|scene|act|step|part|film|episode|shot|take|bar|beat|bagian|bab|tahap)\s*#?0?\d+\b', re.I)
COUNTER_BARE_RE = re.compile(r'^\s*0\d\s*$')
META_RE = re.compile(
    r'\bBPM\b|\bFPS\b|\bFRAME\s*\d|\b(?:1920|3840|1280|1080)\s*[x×]\s*(?:1080|1920|2160|720)\b|'
    r'\bT\s*\+\s*\d|\bTC\b|\b\d{1,2}:\d{2}:\d{2}(?:[.:]\d+)?\b|\bREC\b',
    re.I,
)
GREETING_RE = re.compile(r'\bgood\s+(?:morning|afternoon|evening)\b|\bwelcome\s+back\b', re.I)
LABEL_VALUE_RE = re.compile(r'^[A-Za-z][A-Za-z ]{2,24}\s*[·•]\s*[$€£Rp]*\s?\d[\d,.]*\s?[kKmMbB%]?$')


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def _serve_directory(directory: Path):
    handler = partial(_QuietHandler, directory=str(directory.resolve()))
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def required_read_seconds(text: str, *, min_short: float = 0.40, min_phrase: float = 0.80) -> float:
    """Compute minimum continuous hold time for an on-screen non-caption text block (HyperFrames + readcheck)."""
    clean = ''.join(ch for ch in text if not ch.isspace())
    if not clean:
        return 0.0
    cjk_count = len(CJK_RE.findall(clean))
    latin_count = len(clean) - cjk_count
    words = [w for w in text.strip().split() if w]
    if cjk_count > 0:
        return round(max(min_phrase, cjk_count / 4.5 + latin_count / 15.0 + 0.6), 3)
    if len(words) <= 2 and latin_count <= 14:
        return min_short
    return round(max(min_phrase, 0.50 + 0.28 * len(words)), 3)


def _inside_region(bbox: list[float], region_norm: list[float] | None) -> bool:
    if not region_norm:
        return False
    rx0, ry0, rx1, ry1 = region_norm
    cx = (bbox[0] + bbox[2]) / 2.0
    cy = (bbox[1] + bbox[3]) / 2.0
    return (rx0 - 0.02) <= cx <= (rx1 + 0.02) and (ry0 - 0.02) <= cy <= (ry1 + 0.02)


def _build_scene_harness_html(scene_id: str, template_html: str, width: int, height: int, root_scripts: list[str]) -> str:
    # Unwrap <template>...</template> if present so HyperFrames sub-compositions mount identically to Studio/render.
    match = re.search(r'<template[^>]*>(.*)</template>', template_html, flags=re.S | re.I)
    inner = match.group(1) if match else template_html
    script_tags = '\n'.join(f'<script src="{src}"></script>' for src in root_scripts)
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
html, body {{ margin: 0; padding: 0; width: {width}px; height: {height}px; overflow: hidden; }}
#__hf_host {{ position: relative; width: {width}px; height: {height}px; overflow: hidden; }}
</style>
{script_tags}
<script>window.__timelines = window.__timelines || {{}};</script>
</head>
<body>
<div id="__hf_host">{inner}</div>
</body>
</html>"""


PAGE_SCAN_JS = r"""
() => {
  const W = window.innerWidth || 1080;
  const H = window.innerHeight || 1920;
  const cs = (e) => window.getComputedStyle(e);
  const rgba = (c) => {
    let m = /^rgba?\(([^)]+)\)/.exec(c || '');
    if (m) {
      const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(parseFloat);
      return [p[0] || 0, p[1] || 0, p[2] || 0, p.length > 3 ? p[3] : 1];
    }
    return [0, 0, 0, 0];
  };
  const hidden = (e) => {
    for (let n = e; n && n !== document.body; n = n.parentElement) {
      if (cs(n).display === 'none' || cs(n).visibility === 'hidden') return true;
    }
    return false;
  };
  const opacity = (e) => {
    let o = 1;
    for (let n = e; n && n.nodeType === 1; n = n.parentElement) {
      const v = parseFloat(cs(n).opacity);
      if (!Number.isNaN(v)) o *= v;
    }
    return o;
  };
  const hasAttrUp = (e, attr, val = null) => {
    for (let n = e; n && n !== document.body; n = n.parentElement) {
      if (n.hasAttribute && n.hasAttribute(attr)) {
        if (val === null || n.getAttribute(attr) === val) return true;
      }
    }
    return false;
  };
  const isCaptionClass = (e) => {
    for (let n = e; n && n !== document.body; n = n.parentElement) {
      const cls = typeof n.className === 'string' ? n.className : (n.getAttribute && n.getAttribute('class')) || '';
      const id = n.id || '';
      if (/\bcaption\b|\bsubtitle\b/i.test(cls) || /\bcaption\b|\bsubtitle\b/i.test(id)) return true;
    }
    return false;
  };
  const isSurface = (a) => {
    if (!a || a === document.body || a === document.documentElement) return false;
    if (a.hasAttribute && a.hasAttribute('data-ui')) return true;
    if (a.closest && a.closest('svg')) return false;
    const s = cs(a), c = rgba(s.backgroundColor);
    const filled = c[3] >= 0.3 || (s.backgroundImage && s.backgroundImage !== 'none');
    const rad = parseFloat(s.borderTopLeftRadius || '0') || 0;
    if (!filled || rad < 6) return false;
    const r = a.getBoundingClientRect();
    const area = (r.width * r.height) / (W * H);
    const full = r.width >= 0.9 * W && r.height >= 0.9 * H;
    const cy = (r.top + r.bottom) / 2 / H;
    const bar = r.width >= 0.6 * W && r.height <= 0.14 * H && (cy < 0.12 || cy > 0.88);
    return area >= 0.025 && !full && !bar;
  };
  const surfaceOf = (e) => {
    for (let n = e; n && n !== document.body; n = n.parentElement) {
      if (isSurface(n)) return n;
    }
    return null;
  };

  window.__nodeIds = window.__nodeIds || new WeakMap();
  window.__nextNodeId = window.__nextNodeId || 1;
  const nodeId = (e) => {
    if (!window.__nodeIds.has(e)) window.__nodeIds.set(e, window.__nextNodeId++);
    return window.__nodeIds.get(e);
  };

  const groups = new Map();
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = tw.nextNode(); n; n = tw.nextNode()) {
    const p = n.parentElement;
    if (!p || /^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE|TITLE|DEFS|DESC)$/.test(p.tagName.toUpperCase())) continue;
    const txt = (n.textContent || '').replace(/\s+/g, ' ').trim();
    if (!txt) continue;
    if (hidden(p) || opacity(p) < 0.08) continue;
    const rg = document.createRange();
    rg.selectNodeContents(n);
    const rs = [...rg.getClientRects()].filter((q) => q.width > 0.5 && q.height > 0.5);
    if (!rs.length) continue;
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    for (const q of rs) {
      x0 = Math.min(x0, q.left); y0 = Math.min(y0, q.top);
      x1 = Math.max(x1, q.right); y1 = Math.max(y1, q.bottom);
    }
    if (x1 <= 0 || x0 >= W || y1 <= 0 || y0 >= H) continue;
    let c = p;
    while (c.parentElement && c !== document.body && /^(inline|contents|tspan)$/i.test(c.tagName === 'tspan' ? 'tspan' : cs(c).display)) {
      c = c.parentElement;
    }
    const g = groups.get(c) || { c, parts: [], x0: 1e9, y0: 1e9, x1: -1e9, y1: -1e9, tops: new Set(), p };
    g.parts.push(txt);
    g.x0 = Math.min(g.x0, x0); g.y0 = Math.min(g.y0, y0);
    g.x1 = Math.max(g.x1, x1); g.y1 = Math.max(g.y1, y1);
    for (const q of rs) g.tops.add(Math.round(q.top / 4));
    groups.set(c, g);
  }

  const blocks = [];
  for (const g of groups.values()) {
    const text = g.parts.join(' ').replace(/\s+([.,;:!?])/g, '$1').trim();
    if (!text) continue;
    const s = cs(g.p);
    const fs = parseFloat(s.fontSize) || (g.y1 - g.y0) || 16;
    const lsRaw = s.letterSpacing === 'normal' ? 0 : parseFloat(s.letterSpacing) || 0;
    const letters = text.replace(/[^A-Za-z]/g, '');
    const sf = surfaceOf(g.c);
    const fullyInside = g.x0 >= -2 && g.y0 >= -2 && g.x1 <= W + 2 && g.y1 <= H + 2;
    blocks.push({
      id: String(nodeId(g.c)),
      tag: g.c.tagName.toLowerCase(),
      text: text.slice(0, 160),
      bbox: [+(g.x0 / W).toFixed(4), +(g.y0 / H).toFixed(4), +(g.x1 / W).toFixed(4), +(g.y1 / H).toFixed(4)],
      fs: +(fs / H).toFixed(4),
      ls: +(lsRaw / Math.max(1, fs)).toFixed(4),
      up: s.textTransform === 'uppercase' || (letters.length >= 3 && letters === letters.toUpperCase()),
      mono: /mono|menlo|courier|consolas/i.test(s.fontFamily || ''),
      color: rgba(s.color).slice(0, 3).map((v) => Math.round(v)),
      alpha: +(opacity(g.p)).toFixed(2),
      ta: cs(g.c).textAlign || 'start',
      lines: Math.max(1, g.tops.size),
      inUi: !!sf,
      uiId: sf ? String(nodeId(sf)) : '',
      uiCaptured: hasAttrUp(g.c, 'data-ui', 'captured'),
      allowChrome: hasAttrUp(g.c, 'data-allow-chrome') || hasAttrUp(g.c, 'data-board-chrome'),
      passReadcheck: hasAttrUp(g.c, 'data-pass-readcheck'),
      isCaption: isCaptionClass(g.c),
      fullyInside,
    });
  }

  const shapes = [];
  for (const e of document.body.querySelectorAll('*')) {
    const tag = e.tagName.toLowerCase();
    if (e.closest('svg') && tag !== 'svg') continue;
    if (/^(script|style|noscript|template|br|source|track|link|meta|html|body)$/.test(tag)) continue;
    if (e.id === '__hf_host' || e.id === 'root') continue;
    if (hidden(e)) continue;
    const op = opacity(e);
    if (op < 0.08) continue;
    const r = e.getBoundingClientRect();
    if (r.width < 1 || r.height < 1 || r.right <= 0 || r.left >= W || r.bottom <= 0 || r.top >= H) continue;
    const s = cs(e);
    const bg = rgba(s.backgroundColor);
    const media = /^(img|video|canvas|svg)$/.test(tag) || (s.backgroundImage && /url\(/.test(s.backgroundImage));
    const fill = bg[3] * op >= 0.08 || (s.backgroundImage && s.backgroundImage !== 'none');
    const border = ((parseFloat(s.borderTopWidth) || 0) >= 1 || (parseFloat(s.borderBottomWidth) || 0) >= 1) && rgba(s.borderTopColor)[3] > 0.08;
    if (!fill && !media && !border) continue;
    shapes.push({
      id: String(nodeId(e)),
      tag,
      bbox: [+(r.left / W).toFixed(4), +(r.top / H).toFixed(4), +(r.right / W).toFixed(4), +(r.bottom / H).toFixed(4)],
      w: +r.width.toFixed(1),
      h: +r.height.toFixed(1),
      media: !!media,
      fill: !!fill,
      border: !!border,
      inUi: !!surfaceOf(e.parentElement || e),
      selfSurface: isSurface(e),
      allowChrome: hasAttrUp(e, 'data-allow-chrome') || hasAttrUp(e, 'data-board-chrome'),
    });
    if (shapes.length >= 1200) break;
  }

  const explicitTexts = typeof window.TEXTS === 'function' ? (window.TEXTS(window.__currentSeekT || 0) || []) : null;
  return { blocks, shapes, explicitTexts };
}
"""


def _evaluate_scene_samples(
    scene_id: str,
    samples: list[tuple[float, dict]],
    scene_duration: float,
    step: float,
    region_norm: list[float] | None,
) -> tuple[list[dict], list[dict], set[tuple[str, tuple[float, ...]]]]:
    """Evaluate motionmaxxing G5 slop rules and on-screen text read-time holds for one scene."""
    slop_hits: list[dict] = []
    seen_rules: set[tuple[str, str]] = set()
    pinned_candidates: set[tuple[str, tuple[float, ...]]] = set()

    def record(rule: str, severity: str, t: float, text: str, note: str, bbox: list[float]):
        key = (rule, text[:40] or note[:40])
        if key in seen_rules:
            return
        seen_rules.add(key)
        slop_hits.append({
            'scene': scene_id,
            'rule': rule,
            'severity': severity,
            'time_s': round(t, 2),
            'text': text[:80],
            'bbox': bbox,
            'note': note,
        })

    # Track growing thin non-UI bars across samples (P1).
    bar_series: dict[str, list[tuple[float, float, list[float]]]] = {}

    for idx, (t, snap) in enumerate(samples):
        nxt = samples[idx + 1][1] if idx + 1 < len(samples) else snap
        blocks = [
            b for b in snap['blocks']
            if not b['isCaption'] and not _inside_region(b['bbox'], region_norm)
        ]
        next_blocks = [
            b for b in nxt['blocks']
            if not b['isCaption'] and not _inside_region(b['bbox'], region_norm)
        ]

        def is_stable(blk: dict) -> bool:
            return any(
                c['text'] == blk['text']
                and abs(c['bbox'][0] - blk['bbox'][0]) < 0.006
                and abs(c['bbox'][1] - blk['bbox'][1]) < 0.006
                for c in next_blocks
            )

        free = [b for b in blocks if not b['inUi'] and not b['allowChrome']]
        max_fs = max((b['fs'] for b in free), default=0.0)
        ui_clusters: dict[str, set[str]] = {}

        for b in blocks:
            txt = b['text']
            x0, y0, x1, y1 = b['bbox']
            cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
            if not b['allowChrome'] and is_stable(b):
                pinned_candidates.add((txt, tuple(round(v, 2) for v in b['bbox'])))

            # Vibe-coded UI tells (V1, V2, V4, V5)
            if not b['uiCaptured']:
                if GREETING_RE.search(txt):
                    record('V1', 'FAIL', t, txt, 'generic greeting header', b['bbox'])
                    ui_clusters.setdefault(b['uiId'] or 'page', set()).add('greeting')
                if LABEL_VALUE_RE.match(txt) and not META_RE.search(txt):
                    record('V2', 'FAIL', t, txt, 'vibe-coded "Label · Value" row', b['bbox'])
                    ui_clusters.setdefault(b['uiId'] or 'page', set()).add('label.value')
                if b['inUi'] and any(math.dist(b['color'], z) <= 10 for z in ZINC_PALETTE):
                    ui_clusters.setdefault(b['uiId'], set()).add('zinc')

            if b['inUi'] or b['allowChrome']:
                continue

            stab = is_stable(b)
            small = b['fs'] <= 0.04
            corner = (cx < 0.20 or cx > 0.80) and (cy < 0.12 or cy > 0.88)
            edge = y1 < 0.06 or y0 > 0.94 or x1 < 0.04 or x0 > 0.96
            if small and stab and (corner or edge):
                record('C1', 'FAIL', t, txt, 'held corner/edge micro-label chrome', b['bbox'])
            if b['up'] and b['ls'] >= 0.05 and b['fs'] <= 0.045 and len(re.sub(r'[^A-Za-z]', '', txt)) >= 3:
                record('C2', 'FAIL', t, txt, f"tracked uppercase chrome label (ls={b['ls']:.2f}em)", b['bbox'])
            if b['fs'] <= 0.06 and (COUNTER_NUM_RE.search(txt) or COUNTER_WORD_RE.search(txt) or (b['fs'] <= 0.05 and COUNTER_BARE_RE.search(txt))):
                if not re.match(r'^\s*24\s*/\s*7\b', txt):
                    record('C3', 'FAIL', t, txt, 'chapter/slide counter index', b['bbox'])
            if b['fs'] <= 0.06 and META_RE.search(txt):
                record('C4', 'FAIL', t, txt, 'production metadata text on screen', b['bbox'])

            # T1: letter-by-letter typed headline (>= 5% H growing mid-word)
            if b['fs'] >= 0.05 and idx + 1 < len(samples):
                grew = next(
                    (
                        c for c in next_blocks
                        if not c['inUi']
                        and abs(c['bbox'][1] - y0) < 0.02
                        and len(c['text']) > len(txt)
                        and c['text'].startswith(txt)
                    ),
                    None,
                )
                if grew:
                    rest = grew['text'][len(txt):]
                    last_tok = txt.split()[-1] if txt.split() else ''
                    next_toks = grew['text'].split()
                    tok_idx = max(0, len(txt.split()) - 1)
                    tok2 = next_toks[tok_idx] if tok_idx < len(next_toks) else ''
                    if not rest.startswith(' ') and len(tok2) > len(last_tok):
                        record('T1', 'FAIL', t, f'{txt} -> {grew["text"]}', 'letter-typed headline growth', b['bbox'])

        for uid, kinds in ui_clusters.items():
            if len(kinds) >= 2:
                record('V5', 'FAIL', t, uid, f'vibe-coded UI cluster ({", ".join(sorted(kinds))})', [0, 0, 1, 1])

        # C7 kicker over headline & D1 slide-deck layout (left-anchored headline + right media + subline/kicker)
        kickers: dict[str, dict] = {}
        for a in free:
            for b in free:
                if a is b or not (a['fs'] <= 0.04 and b['fs'] >= max(0.05, a['fs'] * 2.0)):
                    continue
                gap = b['bbox'][1] - a['bbox'][3]
                if -0.01 < gap < 0.06 and abs(a['bbox'][0] - b['bbox'][0]) < 0.025 and is_stable(a) and is_stable(b):
                    kickers[b['id']] = a
                    record('C7', 'FAIL', t, f"{a['text']} / {b['text']}", 'kicker stacked above headline', b['bbox'])

        for b in free:
            x0, y0, x1, y1 = b['bbox']
            cx = (x0 + x1) / 2.0
            if not (b['fs'] >= 0.05 and b['fs'] >= 0.85 * max_fs and 0.02 <= x0 < 0.18 and x1 < 0.72 and b['ta'] != 'center' and abs(cx - 0.5) > 0.08 and is_stable(b)):
                continue
            sub = next(
                (
                    c for c in free
                    if c is not b and 0.02 <= c['fs'] <= 0.65 * b['fs']
                    and -0.005 < (c['bbox'][1] - y1) < 0.08 and abs(c['bbox'][0] - x0) < 0.03
                ),
                None,
            )
            right_media = next(
                (
                    s for s in snap['shapes']
                    if (s['media'] or s['selfSurface'])
                    and 0.05 <= (s['bbox'][2] - s['bbox'][0]) * (s['bbox'][3] - s['bbox'][1]) <= 0.65
                    and (s['bbox'][0] + s['bbox'][2]) / 2.0 > 0.52
                    and s['bbox'][0] > x1 - 0.04
                ),
                None,
            )
            if right_media and (sub or b['id'] in kickers or b['lines'] >= 2):
                record('D1', 'FAIL', t, b['text'], 'slide-deck layout (left headline block + right-side media/card)', b['bbox'])

        for s in snap['shapes']:
            if s['media'] or s['inUi'] or s['selfSurface'] or s['allowChrome']:
                continue
            w = s['bbox'][2] - s['bbox'][0]
            h = s['bbox'][3] - s['bbox'][1]
            if h <= 0.016 and w >= 0.02:
                bar_series.setdefault(s['id'], []).append((t, w, s['bbox']))

    for sid, series in bar_series.items():
        if len(series) < 4:
            continue
        widths = [x[1] for x in series]
        grow = max(widths) - min(widths)
        ups = sum(1 for i in range(1, len(widths)) if widths[i] > widths[i - 1] + 0.004)
        downs = sum(1 for i in range(1, len(widths)) if widths[i] < widths[i - 1] - 0.004)
        if grow >= 0.12 and ups >= 3 and downs == 0:
            record('P1', 'FAIL', series[0][0], f'bar#{sid}', f'progress-bar chrome growing {min(widths):.2f}->{max(widths):.2f}W', series[0][2])

    # Evaluate on-screen text read-time (readcheck) across samples.
    seen_texts: dict[str, dict] = {}
    partial_texts: dict[str, dict] = {}
    for t, snap in samples:
        explicit = snap.get('explicitTexts')
        if explicit is not None:
            items = [
                {
                    'key': f"{it.get('id', '')}\0{it.get('text', '')}",
                    'text': str(it.get('text', '')).strip(),
                    'pass': bool(it.get('pass')),
                    'fullyInside': it.get('x0', 0) >= -2 and it.get('y0', 0) >= -2,
                }
                for it in explicit if str(it.get('text', '')).strip()
            ]
        else:
            items = [
                {
                    'key': b['text'],
                    'text': b['text'],
                    'pass': b['passReadcheck'],
                    'fullyInside': b['fullyInside'],
                }
                for b in snap['blocks']
                if not b['isCaption'] and not _inside_region(b['bbox'], region_norm)
            ]
        present_keys = set()
        for item in items:
            if item['pass']:
                continue
            key = item['key']
            if not item['fullyInside']:
                partial_texts.setdefault(key, {'scene': scene_id, 'text': item['text'], 'first_t': round(t, 2)})
                continue
            present_keys.add(key)
            entry = seen_texts.get(key)
            if entry is None:
                seen_texts[key] = {'scene': scene_id, 'text': item['text'], 'first_t': t, 'hold_s': step, 'ended': False}
            elif not entry['ended']:
                entry['hold_s'] = min(scene_duration, t + step) - entry['first_t']
        for key, entry in seen_texts.items():
            if key not in present_keys:
                entry['ended'] = True

    read_issues: list[dict] = []
    for key, p in partial_texts.items():
        if key not in seen_texts:
            read_issues.append({
                'scene': scene_id,
                'text': p['text'][:80],
                'first_t': p['first_t'],
                'hold_s': 0.0,
                'required_s': required_read_seconds(p['text']),
                'severity': 'FAIL',
                'reason': 'text box clipped outside viewport bounds',
            })

    for entry in seen_texts.values():
        need = required_read_seconds(entry['text'])
        # If the scene itself is shorter than `need` cleanly by design? No: if text cannot be read within the scene, it has too many words for that shot!
        hold = round(entry['hold_s'], 3)
        if hold + 1e-6 < need * 0.75:
            read_issues.append({
                'scene': scene_id,
                'text': entry['text'][:80],
                'first_t': round(entry['first_t'], 2),
                'hold_s': hold,
                'required_s': need,
                'severity': 'FAIL',
                'reason': f'held {hold:.2f}s < minimum readable {need:.2f}s',
            })
        elif hold + 1e-6 < need:
            read_issues.append({
                'scene': scene_id,
                'text': entry['text'][:80],
                'first_t': round(entry['first_t'], 2),
                'hold_s': hold,
                'required_s': need,
                'severity': 'WARN',
                'reason': f'tight hold {hold:.2f}s vs recommended {need:.2f}s',
            })

    return slop_hits, read_issues, pinned_candidates


def lint_production_dom(production: Path, *, step: float = 0.15) -> dict:
    """Run headless Chromium DOM anti-slop and read-time verification across every mounted scene in a production."""
    from playwright.sync_api import sync_playwright

    production = Path(production).resolve()
    video = production / 'video'
    contract, _, _, _ = load_contract(production)
    parsed = load_root(video)
    width = int(contract['format']['width'] or parsed.root.get('data-width') or 1080)
    height = int(contract['format']['height'] or parsed.root.get('data-height') or 1920)
    region = contract['captions']['region']
    region_norm = (
        [region[0] / width, region[1] / height, (region[0] + region[2]) / width, (region[1] + region[3]) / height]
        if region else None
    )

    local_scripts = [a for a in parsed.assets if a.endswith('.js') and '://' not in a]
    # Also retain CDN gsap if no local vendor script was listed on root.
    if not local_scripts:
        root_html = (video / 'index.html').read_text(encoding='utf-8')
        local_scripts = re.findall(r'<script[^>]+src=["\']([^"\']*gsap[^"\']*)["\']', root_html, flags=re.I)

    scene_hosts = [h for h in parsed.hosts if not is_captions(h)]
    server = _serve_directory(video)
    port = server.server_address[1]
    base_url = f'http://127.0.0.1:{port}'

    all_slop: list[dict] = []
    all_read: list[dict] = []
    scene_pins: list[tuple[str, set[tuple[str, tuple[float, ...]]]]] = []
    temp_files: list[Path] = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={'width': width, 'height': height}, device_scale_factor=1)
            page = context.new_page()

            if scene_hosts:
                targets = [
                    (
                        h.get('id') or Path(h['data-composition-src']).stem,
                        video / h['data-composition-src'],
                        float(h.get('data-duration') or 5.0),
                    )
                    for h in scene_hosts
                ]
            else:
                targets = [('main', video / 'index.html', float(parsed.root['data-duration']))]

            for idx, (scene_id, scene_file, dur) in enumerate(targets):
                raw_html = scene_file.read_text(encoding='utf-8')
                if scene_file.name == 'index.html' and '<template' not in raw_html.lower():
                    target_url = f'{base_url}/index.html'
                else:
                    harness_name = f'.__dom_lint_{idx}_{scene_id}.html'
                    harness_path = video / harness_name
                    harness_path.write_text(
                        _build_scene_harness_html(scene_id, raw_html, width, height, local_scripts),
                        encoding='utf-8',
                    )
                    temp_files.append(harness_path)
                    target_url = f'{base_url}/{harness_name}'

                page.goto(target_url, wait_until='load', timeout=30000)
                page.evaluate('() => document.fonts ? document.fonts.ready : Promise.resolve()')

                n_steps = max(2, int(math.ceil(dur / step)))
                times = [round(min(dur - 0.001, i * step), 4) for i in range(n_steps + 1)]
                # Deduplicate preserving order
                times = list(dict.fromkeys(t for t in times if t >= 0))

                samples: list[tuple[float, dict]] = []
                for t in times:
                    page.evaluate(
                        """([sid, t]) => {
                            window.__currentSeekT = t;
                            if (typeof window.__seek === 'function') { window.__seek(t); }
                            else if (window.__timelines && typeof window.__timelines === 'object') {
                                for (const k of Object.keys(window.__timelines)) {
                                    const tl = window.__timelines[k];
                                    if (tl && typeof tl.seek === 'function') {
                                        if (tl.pause) tl.pause();
                                        tl.seek(t, false);
                                    }
                                }
                            } else if (window.gsap && window.gsap.globalTimeline) {
                                window.gsap.globalTimeline.pause();
                                window.gsap.globalTimeline.seek(t, false);
                            }
                            if (typeof window.render === 'function') window.render(t);
                            if (typeof window.renderAt === 'function') window.renderAt(t);
                        }""",
                        [scene_id, t],
                    )
                    snap = page.evaluate(PAGE_SCAN_JS)
                    samples.append((t, snap))

                slop_hits, read_issues, pins = _evaluate_scene_samples(scene_id, samples, dur, step, region_norm)
                all_slop.extend(slop_hits)
                all_read.extend(read_issues)
                scene_pins.append((scene_id, pins))

            browser.close()
    finally:
        for tf in temp_files:
            tf.unlink(missing_ok=True)
        server.shutdown()
        server.server_close()

    # Check pinned non-board-chrome text across >= 3 consecutive scenes (Never-ship #9).
    if len(scene_pins) >= 3:
        for i in range(len(scene_pins) - 2):
            common = scene_pins[i][1] & scene_pins[i + 1][1] & scene_pins[i + 2][1]
            for txt, box in sorted(common):
                all_slop.append({
                    'scene': f"{scene_pins[i][0]}..{scene_pins[i + 2][0]}",
                    'rule': 'PINNED',
                    'severity': 'FAIL',
                    'time_s': 0.0,
                    'text': txt[:80],
                    'bbox': list(box),
                    'note': 'identical non-caption label/pill pinned at the same coordinates across 3+ consecutive scenes (mark intentional board chrome with data-board-chrome)',
                })

    slop_fails = [h for h in all_slop if h['severity'] == 'FAIL']
    read_fails = [r for r in all_read if r['severity'] == 'FAIL']
    comp_sha = composition_digest(video)
    report = {
        'status': 'passed' if (not slop_fails and not read_fails) else 'failed',
        'composition_sha256': comp_sha,
        'scenes_checked': len(scene_pins),
        'step_seconds': step,
        'g5_anti_slop': {
            'status': 'passed' if not slop_fails else 'failed',
            'fail_count': len(slop_fails),
            'hits': all_slop,
        },
        'readcheck': {
            'status': 'passed' if not read_fails else 'failed',
            'fail_count': len(read_fails),
            'warnings': len([r for r in all_read if r['severity'] == 'WARN']),
            'issues': all_read,
        },
    }
    out_path = video / 'verification' / 'dom-lint.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--production', type=Path, required=True, help='Path to productions/<slug>')
    parser.add_argument('--step', type=float, default=0.15, help='Timeline sample step in seconds (default: 0.15)')
    args = parser.parse_args()
    report = lint_production_dom(args.production, step=args.step)
    print(json.dumps({
        'status': report['status'],
        'scenes_checked': report['scenes_checked'],
        'g5_fails': report['g5_anti_slop']['fail_count'],
        'readcheck_fails': report['readcheck']['fail_count'],
        'composition_sha256': report['composition_sha256'],
    }, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['status'] == 'passed' else 1)


if __name__ == '__main__':
    main()
