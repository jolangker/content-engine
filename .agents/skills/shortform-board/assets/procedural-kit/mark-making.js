/**
 * mark-making.js — Deterministic, frame-seekable procedural illustration & motion kit
 * Distilled from anidoodle & huashu-art-motion for HyperFrames Canvas 2D and SVG compositions.
 *
 * Contract: Pure function of explicit parameters and integer seeds. Zero Math.random(), zero wall-clock state.
 * Safe for out-of-order, parallel, and repeated HyperFrames seeks.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.MarkKit = factory();
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  function hashSeed(input) {
    const str = String(input);
    let h = 2166136261 >>> 0;
    for (let i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = Math.imul(h, 16777619) >>> 0;
    }
    return h >>> 0;
  }

  function mulberry32(seed) {
    let a = (typeof seed === 'string' ? hashSeed(seed) : seed) >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function _lattice(seed, ix, iy) {
    let h = (seed ^ Math.imul(ix, 374761393) ^ Math.imul(iy, 668265263)) >>> 0;
    h = Math.imul(h ^ (h >>> 13), 1274126177) >>> 0;
    return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
  }

  function valueNoise2D(seed, x, y) {
    const s = typeof seed === 'string' ? hashSeed(seed) : seed >>> 0;
    const ix = Math.floor(x), iy = Math.floor(y);
    const fx = x - ix, fy = y - iy;
    const ux = fx * fx * (3 - 2 * fx);
    const uy = fy * fy * (3 - 2 * fy);
    const a = _lattice(s, ix, iy);
    const b = _lattice(s, ix + 1, iy);
    const c = _lattice(s, ix, iy + 1);
    const d = _lattice(s, ix + 1, iy + 1);
    return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy;
  }

  function fbm2D(seed, x, y, octaves) {
    const nOct = octaves || 3;
    const baseSeed = typeof seed === 'string' ? hashSeed(seed) : seed >>> 0;
    let total = 0, amp = 0.5, freq = 1, norm = 0;
    for (let i = 0; i < nOct; i++) {
      total += amp * valueNoise2D((baseSeed + i * 1013) >>> 0, x * freq, y * freq);
      norm += amp;
      amp *= 0.5;
      freq *= 2.02;
    }
    return (total / (norm || 1)) * 2 - 1;
  }

  /**
   * Closed-form analytical damped spring at explicit time t >= 0.
   * zeta = 1.0: critical (zero bounce); 0.72-0.85: crisp physical settle; < 0.6: playful.
   */
  function springAtTime(t, opts) {
    const o = opts || {};
    const from = o.from !== undefined ? o.from : 0;
    const to = o.to !== undefined ? o.to : 1;
    if (t <= 0) return from;
    const zeta = o.zeta !== undefined ? o.zeta : 0.82;
    const omega = o.omega !== undefined ? o.omega : 14.0;
    const v0 = o.velocity || 0;
    const x0 = from - to;
    let disp;
    if (Math.abs(zeta - 1.0) < 1e-4) {
      disp = (x0 + (v0 + omega * x0) * t) * Math.exp(-omega * t);
    } else if (zeta < 1.0) {
      const wd = omega * Math.sqrt(1 - zeta * zeta);
      const A = x0;
      const B = (v0 + zeta * omega * x0) / wd;
      disp = Math.exp(-zeta * omega * t) * (A * Math.cos(wd * t) + B * Math.sin(wd * t));
    } else {
      const s = Math.sqrt(zeta * zeta - 1);
      const r1 = -omega * (zeta - s);
      const r2 = -omega * (zeta + s);
      const c2 = (v0 - r1 * x0) / (r2 - r1);
      const c1 = x0 - c2;
      disp = c1 * Math.exp(r1 * t) + c2 * Math.exp(r2 * t);
    }
    return to + disp;
  }

  /** Logarithmic zoom interpolation for smooth scale-travel without late snap. */
  function logZoom(scaleStart, scaleEnd, progress) {
    const p = Math.max(0, Math.min(1, progress));
    if (scaleStart <= 0 || scaleEnd <= 0) return scaleStart + (scaleEnd - scaleStart) * p;
    return scaleStart * Math.pow(scaleEnd / scaleStart, p);
  }

  /** Staggered assembly explode/collapse: outer parts leave first and return home last. */
  function explodeShareAt(index, totalCount, progress, mode, stagger) {
    const p = Math.max(0, Math.min(1, progress));
    const n = Math.max(1, totalCount);
    const st = stagger !== undefined ? stagger : 0.45;
    // index 0 = innermost core, n-1 = outermost housing
    const rank = mode === 'collapse' ? index / Math.max(1, n - 1) : (n - 1 - index) / Math.max(1, n - 1);
    const start = rank * st;
    const span = Math.max(0.001, 1 - st);
    const local = Math.max(0, Math.min(1, (p - start) / span));
    const eased = local * local * (3 - 2 * local);
    return mode === 'collapse' ? 1 - eased : eased;
  }

  /** Resample a polyline cleanly and cut it at `progress` (0..1) along arc length for self-drawing strokes. */
  function slicePolyline(points, progress, stepPx) {
    const p = progress === undefined ? 1 : Math.max(0, Math.min(1, progress));
    if (!points || points.length < 2 || p <= 0) return [];
    const segs = [];
    let total = 0;
    for (let i = 1; i < points.length; i++) {
      const dx = points[i][0] - points[i - 1][0];
      const dy = points[i][1] - points[i - 1][1];
      const len = Math.hypot(dx, dy);
      if (len > 1e-4) {
        segs.push({ a: points[i - 1], b: points[i], len, accStart: total });
        total += len;
      }
    }
    if (total <= 1e-4) return [points[0].slice()];
    const targetLen = total * p;
    const step = Math.max(1.5, stepPx || 4);
    const count = Math.max(2, Math.ceil(targetLen / step) + 1);
    const out = [];
    let segIdx = 0;
    for (let k = 0; k < count; k++) {
      const d = (targetLen * k) / (count - 1);
      while (segIdx < segs.length - 1 && segs[segIdx].accStart + segs[segIdx].len < d) {
        segIdx++;
      }
      const s = segs[segIdx];
      const u = Math.max(0, Math.min(1, (d - s.accStart) / s.len));
      out.push([s.a[0] + (s.b[0] - s.a[0]) * u, s.a[1] + (s.b[1] - s.a[1]) * u, total > 0 ? d / total : 0]);
    }
    return out;
  }

  /**
   * Build a closed 2D polygon ribbon representing a tapered, pressure-varied, hand-wobbled ink/pencil stroke.
   * Pass `boilStep: Math.floor(t * 12)` for subtle on-twos animation boil, or 0 for locked marks.
   */
  function buildTaperedStrokePolygon(points, opts) {
    const o = opts || {};
    const width = o.width !== undefined ? o.width : 4.0;
    const taperStart = o.taperStart !== undefined ? o.taperStart : 0.22;
    const taperEnd = o.taperEnd !== undefined ? o.taperEnd : 0.28;
    const pressure = o.pressure !== undefined ? o.pressure : 0.25;
    const wobble = o.wobble !== undefined ? o.wobble : 1.1;
    const boilStep = o.boilStep || 0;
    const seed = hashSeed((o.seed !== undefined ? o.seed : 1) + ':boil:' + boilStep);

    const sampled = slicePolyline(points, o.progress !== undefined ? o.progress : 1, o.stepPx || 4);
    if (sampled.length < 2) return [];

    const left = [];
    const right = [];
    for (let i = 0; i < sampled.length; i++) {
      const pt = sampled[i];
      const prev = sampled[Math.max(0, i - 1)];
      const next = sampled[Math.min(sampled.length - 1, i + 1)];
      let tx = next[0] - prev[0];
      let ty = next[1] - prev[1];
      const tLen = Math.hypot(tx, ty) || 1;
      tx /= tLen;
      ty /= tLen;
      const nx = -ty, ny = tx;

      const u = i / (sampled.length - 1);
      let env = 1.0;
      if (taperStart > 0 && u < taperStart) env *= Math.sin((u / taperStart) * (Math.PI / 2));
      if (taperEnd > 0 && u > 1 - taperEnd) env *= Math.sin(((1 - u) / taperEnd) * (Math.PI / 2));

      const pressMod = 1 + pressure * fbm2D(seed, u * 5.5, 0.7, 2);
      const wob = wobble * fbm2D((seed + 7919) >>> 0, pt[0] * 0.025, pt[1] * 0.025, 2);
      const halfW = Math.max(0.25, 0.5 * width * env * pressMod);

      const cx = pt[0] + nx * wob;
      const cy = pt[1] + ny * wob;
      left.push([+(cx + nx * halfW).toFixed(2), +(cy + ny * halfW).toFixed(2)]);
      right.push([+(cx - nx * halfW).toFixed(2), +(cy - ny * halfW).toFixed(2)]);
    }
    return left.concat(right.reverse());
  }

  function polygonToSvgPath(poly) {
    if (!poly || poly.length < 3) return '';
    const parts = ['M ' + poly[0][0] + ' ' + poly[0][1]];
    for (let i = 1; i < poly.length; i++) {
      parts.push('L ' + poly[i][0] + ' ' + poly[i][1]);
    }
    parts.push('Z');
    return parts.join(' ');
  }

  function svgTaperedPath(points, opts) {
    return polygonToSvgPath(buildTaperedStrokePolygon(points, opts));
  }

  function drawTaperedStroke(ctx, points, opts) {
    const o = opts || {};
    const poly = buildTaperedStrokePolygon(points, o);
    if (poly.length < 3) return;
    ctx.save();
    if (o.opacity !== undefined) ctx.globalAlpha *= o.opacity;
    ctx.fillStyle = o.color || '#172B3B';
    ctx.beginPath();
    ctx.moveTo(poly[0][0], poly[0][1]);
    for (let i = 1; i < poly.length; i++) ctx.lineTo(poly[i][0], poly[i][1]);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }

  /**
   * Build an organic watercolour / gouache wash polygon that slightly misses or bleeds its pencil boundary.
   */
  function buildWatercolorWash(polygon, opts) {
    if (!polygon || polygon.length < 3) return [];
    const o = opts || {};
    const seed = hashSeed(o.seed !== undefined ? o.seed : 42);
    const bleed = o.bleed !== undefined ? o.bleed : 3.5;
    const shrink = o.shrink !== undefined ? o.shrink : 1.2;
    const dx = o.dx || 0;
    const dy = o.dy || 0;

    let cx = 0, cy = 0;
    for (let i = 0; i < polygon.length; i++) {
      cx += polygon[i][0];
      cy += polygon[i][1];
    }
    cx /= polygon.length;
    cy /= polygon.length;

    const closed = polygon.concat([polygon[0]]);
    const dense = slicePolyline(closed, 1.0, o.stepPx || 8);
    const out = [];
    for (let i = 0; i < dense.length - 1; i++) {
      const p = dense[i];
      const vx = p[0] - cx, vy = p[1] - cy;
      const vLen = Math.hypot(vx, vy) || 1;
      const n = fbm2D(seed, p[0] * 0.03, p[1] * 0.03, 3);
      const radial = -shrink + bleed * n;
      out.push([
        +(p[0] + dx + (vx / vLen) * radial).toFixed(2),
        +(p[1] + dy + (vy / vLen) * radial).toFixed(2),
      ]);
    }
    return out;
  }

  function _clipSegmentToPolygon(p0, p1, poly) {
    // Sample finely along segment for general concave/convex support in 2D illustrations
    const steps = Math.max(8, Math.ceil(Math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / 3));
    const inside = (x, y) => {
      let c = false;
      for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
        const xi = poly[i][0], yi = poly[i][1];
        const xj = poly[j][0], yj = poly[j][1];
        if (((yi > y) !== (yj > y)) && (x < ((xj - xi) * (y - yi)) / (yj - yi + 1e-12) + xi)) c = !c;
      }
      return c;
    };
    const runs = [];
    let cur = null;
    for (let k = 0; k <= steps; k++) {
      const u = k / steps;
      const x = p0[0] + (p1[0] - p0[0]) * u;
      const y = p0[1] + (p1[1] - p0[1]) * u;
      if (inside(x, y)) {
        if (!cur) cur = [[x, y], [x, y]];
        else cur[1] = [x, y];
      } else if (cur) {
        if (Math.hypot(cur[1][0] - cur[0][0], cur[1][1] - cur[0][1]) >= 2.0) runs.push(cur);
        cur = null;
      }
    }
    if (cur && Math.hypot(cur[1][0] - cur[0][0], cur[1][1] - cur[0][1]) >= 2.0) runs.push(cur);
    return runs;
  }

  /**
   * Part-anchored directional hatching clipped to a polygon.
   * Pass local polygon coordinates (or pass anchorX/anchorY matching part translation) so moving parts carry their marks without boiling.
   */
  function buildAnchoredHatchLines(polygon, opts) {
    if (!polygon || polygon.length < 3) return [];
    const o = opts || {};
    const spacing = Math.max(2.5, o.spacing || 8);
    const angle = ((o.angleDeg !== undefined ? o.angleDeg : -35) * Math.PI) / 180;
    const anchorX = o.anchorX || 0;
    const anchorY = o.anchorY || 0;
    const progress = o.progress !== undefined ? Math.max(0, Math.min(1, o.progress)) : 1.0;
    const rand = mulberry32(o.seed !== undefined ? o.seed : 101);

    let minX = 1e9, minY = 1e9, maxX = -1e9, maxY = -1e9;
    for (let i = 0; i < polygon.length; i++) {
      minX = Math.min(minX, polygon[i][0]);
      minY = Math.min(minY, polygon[i][1]);
      maxX = Math.max(maxX, polygon[i][0]);
      maxY = Math.max(maxY, polygon[i][1]);
    }
    const cx = anchorX || (minX + maxX) / 2;
    const cy = anchorY || (minY + maxY) / 2;
    const diag = Math.hypot(maxX - minX, maxY - minY) + spacing * 2;
    const dx = Math.cos(angle), dy = Math.sin(angle);
    const nx = -dy, ny = dx;

    const rawSegments = [];
    const count = Math.ceil((2 * diag) / spacing);
    for (let i = -count; i <= count; i++) {
      const jitter = (rand() - 0.5) * spacing * 0.22;
      const off = i * spacing + jitter;
      const ox = cx + nx * off;
      const oy = cy + ny * off;
      const p0 = [ox - dx * diag, oy - dy * diag];
      const p1 = [ox + dx * diag, oy + dy * diag];
      const clipped = _clipSegmentToPolygon(p0, p1, polygon);
      for (let c = 0; c < clipped.length; c++) rawSegments.push(clipped[c]);
    }

    if (progress >= 1.0) return rawSegments;
    const total = rawSegments.length;
    const fullCount = Math.floor(total * progress);
    const rem = total * progress - fullCount;
    const out = rawSegments.slice(0, fullCount);
    if (fullCount < total && rem > 0.05) {
      const s = rawSegments[fullCount];
      out.push([s[0], [s[0][0] + (s[1][0] - s[0][0]) * rem, s[0][1] + (s[1][1] - s[0][1]) * rem]]);
    }
    return out;
  }

  return {
    hashSeed,
    mulberry32,
    valueNoise2D,
    fbm2D,
    springAtTime,
    logZoom,
    explodeShareAt,
    slicePolyline,
    buildTaperedStrokePolygon,
    polygonToSvgPath,
    svgTaperedPath,
    drawTaperedStroke,
    buildWatercolorWash,
    buildAnchoredHatchLines,
  };
});
