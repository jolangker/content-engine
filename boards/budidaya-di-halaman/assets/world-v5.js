"use strict";

// Visual v5 shared Living World (4-plane 2.5D depth parallax, swaying foliage,
// yard micro-life, reactive lighting/weather) and Event-Driven Camera helpers.
// Pure deterministic functions of time `t` so any frame renders identically.

const V5_PARALLAX = {
  sky: 0.18,
  horizon: 0.45,
  midground: 0.80,
  hero: 1.00,
  foreground: 1.14,
};

function v5Clamp01(v) {
  return Math.min(1, Math.max(0, v));
}

function v5Lerp(a, b, t) {
  return a + (b - a) * t;
}

function v5HexToRgb(hex) {
  const h = hex.replace("#", "");
  return [
    parseInt(h.slice(0, 2), 16),
    parseInt(h.slice(2, 4), 16),
    parseInt(h.slice(4, 6), 16),
  ];
}

function v5MixHex(a, b, p) {
  const t = v5Clamp01(p);
  const ca = v5HexToRgb(a);
  const cb = v5HexToRgb(b);
  const r = Math.round(v5Lerp(ca[0], cb[0], t));
  const g = Math.round(v5Lerp(ca[1], cb[1], t));
  const bl = Math.round(v5Lerp(ca[2], cb[2], t));
  return `rgb(${r},${g},${bl})`;
}

// Damped physical impulse for tactile camera micro-settles (2-5 px, ~0.16s).
function v5Impulse(t, at, amp = 3.5, decay = 24, freq = 38) {
  if (t < at) return 0;
  const dt = t - at;
  if (dt > 0.35) return 0;
  return amp * Math.exp(-decay * dt) * Math.sin(freq * dt);
}

// Apply 2.5D parallax transform for a depth plane relative to the active camera.
// World space is 540x960 (scaled 2x onto 1080x1920 canvas).
function v5ApplyPlane(ctx, cam, factor) {
  const cx = 270;
  const cy = 480;
  const z = 1 + (cam.zoom - 1) * factor;
  const dx = (cx - cam.x) * factor + (cam.shakeX || 0) * Math.min(1, factor);
  const dy = (cy - cam.y) * factor + (cam.shakeY || 0) * Math.min(1, factor);
  ctx.translate(cx + dx, cy + dy);
  ctx.scale(z, z);
  ctx.translate(-cx, -cy);
}

// Project a world coordinate (wx, wy) on plane 1.0 onto 1080x1920 DOM screen pixels.
function v5WorldToScreen(wx, wy, cam) {
  const cx = 270;
  const cy = 480;
  const z = cam.zoom;
  const dx = (cx - cam.x) + (cam.shakeX || 0);
  const dy = (cy - cam.y) + (cam.shakeY || 0);
  const sx = (cx + dx + (wx - cx) * z) * 2;
  const sy = (cy + dy + (wy - cy) * z) * 2;
  return { x: sx, y: sy, scale: z };
}

function v5Cloud(ctx, x, y, s, fill) {
  oval(ctx, x, y, 36 * s, 9 * s, fill);
  oval(ctx, x - 17 * s, y - 2 * s, 14 * s, 10 * s, fill);
  oval(ctx, x + 3 * s, y - 8 * s, 21 * s, 12 * s, fill);
  oval(ctx, x + 24 * s, y - 3 * s, 15 * s, 9 * s, fill);
}

function v5Bird(ctx, x, y, s, flapPhase, tint = "#394D46AA") {
  const wing = Math.sin(flapPhase) * 4.5 * s;
  ctx.save();
  ctx.translate(x, y);
  ctx.strokeStyle = tint;
  ctx.lineWidth = Math.max(1.2, 1.8 * s);
  ctx.lineCap = "round";
  ctx.beginPath();
  ctx.moveTo(-8 * s, wing);
  ctx.quadraticCurveTo(-4 * s, -3 * s - wing * 0.4, 0, 0);
  ctx.quadraticCurveTo(4 * s, -3 * s - wing * 0.4, 8 * s, wing);
  ctx.stroke();
  ctx.restore();
}

function v5Butterfly(ctx, x, y, t, s = 1, tint = "#FFE47A") {
  const flap = 0.35 + 0.65 * Math.abs(Math.sin(t * 14));
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(Math.sin(t * 3.1) * 0.25);
  oval(ctx, -3.5 * s * flap, -2 * s, 4.5 * s * flap, 3.2 * s, tint, "#5A4A2E88", 0.8, -0.35);
  oval(ctx, 3.5 * s * flap, -2 * s, 4.5 * s * flap, 3.2 * s, tint, "#5A4A2E88", 0.8, 0.35);
  oval(ctx, -2.5 * s * flap, 2 * s, 3.0 * s * flap, 2.2 * s, "#FFF4C4", null, 0, 0.2);
  oval(ctx, 2.5 * s * flap, 2 * s, 3.0 * s * flap, 2.2 * s, "#FFF4C4", null, 0, -0.2);
  ctx.restore();
}

function v5Fireflies(ctx, t, seam, intensity) {
  if (intensity <= 0.02) return;
  const spots = [
    [95, seam - 62, 0.0],
    [168, seam - 34, 1.7],
    [340, seam - 76, 3.1],
    [458, seam - 46, 4.4],
    [255, seam - 28, 2.3],
  ];
  for (const [bx, by, ph] of spots) {
    const x = bx + Math.sin(t * 1.1 + ph) * 16;
    const y = by + Math.cos(t * 1.5 + ph * 1.3) * 9;
    const pulse = 0.35 + 0.65 * Math.pow(0.5 + 0.5 * Math.sin(t * 3.4 + ph * 2), 2);
    const a = intensity * pulse;
    oval(ctx, x, y, 7.5, 7.5, `rgba(255, 226, 110, ${(0.22 * a).toFixed(3)})`);
    oval(ctx, x, y, 2.4, 2.4, `rgba(255, 248, 195, ${(0.9 * a).toFixed(3)})`);
  }
}

// Plane 0: Sky gradient, sun/moon arc, heat shimmer or dusk stars, drifting clouds.
function v5DrawSkyPlane(ctx, t, seam, cam, opts = {}) {
  const {
    top = "#515C72",
    horizon = "#ECC88E",
    sun = [441, 225, 40],
    dusk = 0,
    heat = 0,
    rain = 0,
    cloudTint = "#FFF8E5",
  } = opts;

  ctx.save();
  v5ApplyPlane(ctx, cam, V5_PARALLAX.sky);
  const grad = ctx.createLinearGradient(0, -140, 0, seam + 40);
  grad.addColorStop(0, top);
  grad.addColorStop(1, horizon);
  box(ctx, -180, -180, 900, seam + 300, grad);

  // Faint stars at dusk/night
  if (dusk > 0.2) {
    const starAlpha = (dusk - 0.2) * 0.75;
    for (const [sx, sy, r, ph] of [
      [70, 74, 1.4, 0], [165, 52, 1.1, 1.4], [250, 96, 1.5, 2.2],
      [345, 62, 1.2, 3.5], [478, 86, 1.6, 0.9], [118, 140, 1.1, 4.1],
    ]) {
      const tw = 0.55 + 0.45 * Math.sin(t * 2.6 + ph);
      oval(ctx, sx, sy, r, r, `rgba(255,248,220,${(starAlpha * tw).toFixed(3)})`);
    }
  }

  // Sun with subtle drift and soft ambient rays
  const sunX = sun[0] - t * 1.4;
  const sunY = sun[1] + Math.sin(t * 0.25) * 4;
  const sunR = sun[2];
  const sunVis = Math.max(0.15, 1 - rain * 0.75);
  oval(ctx, sunX, sunY, sunR * 1.65, sunR * 1.65, `rgba(248,218,135,${(0.16 * sunVis).toFixed(3)})`);
  oval(ctx, sunX, sunY, sunR, sunR, `rgba(248,218,135,${(0.42 * sunVis).toFixed(3)})`);
  oval(ctx, sunX, sunY, sunR * 0.72, sunR * 0.72, `rgba(255,242,185,${(0.95 * sunVis).toFixed(3)})`);

  // Subtle midday heat shimmer waves in upper sky when heat > 0
  if (heat > 0.05) {
    ctx.strokeStyle = `rgba(255,235,170,${(0.32 * heat).toFixed(3)})`;
    ctx.lineWidth = 2.2;
    for (let i = 0; i < 4; i++) {
      const y = seam - 70 - i * 32;
      ctx.beginPath();
      for (let x = 40; x <= 500; x += 20) {
        const wy = y + Math.sin(x * 0.04 + t * 5 + i * 1.3) * 3.5;
        if (x === 40) ctx.moveTo(x, wy);
        else ctx.lineTo(x, wy);
      }
      ctx.stroke();
    }
  }

  // Continuous drifting multi-layer clouds
  const cloudSpeed = 10 + rain * 16;
  const cloudOpacity = rain > 0.2 ? 0.72 : 0.62;
  const clouds = [
    [60, seam - 210, 0.96, 1.0],
    [255, seam - 180, 1.32, 0.72],
    [460, seam - 235, 0.74, 1.25],
    [155, seam - 135, 0.85, 0.58],
  ];
  const baseFill = rain > 0.2 ? v5MixHex(cloudTint, "#6E7B8C", rain * 0.75) : cloudTint;
  ctx.save();
  ctx.globalAlpha = cloudOpacity;
  for (const [cx0, cy0, sc, mult] of clouds) {
    const x = (((cx0 + t * cloudSpeed * mult) % 740) + 740) % 740 - 100;
    v5Cloud(ctx, x, cy0, sc, baseFill);
  }
  ctx.restore();
  ctx.restore();
}

// Plane 1: Rolling distant hills, treeline silhouettes, gliding distant birds.
function v5DrawHorizonPlane(ctx, t, seam, cam, opts = {}) {
  const { hill = "#8EB69C", ridge = "#779765", birds = true, dusk = 0 } = opts;
  ctx.save();
  v5ApplyPlane(ctx, cam, V5_PARALLAX.horizon);

  const hillCol = dusk > 0 ? v5MixHex(hill, "#3D5654", dusk * 0.65) : hill;
  const ridgeCol = dusk > 0 ? v5MixHex(ridge, "#2E453B", dusk * 0.68) : ridge;

  polygon(ctx, [
    [-160, seam - 88], [-60, seam - 106], [54, seam - 101], [132, seam - 112],
    [210, seam - 95], [274, seam - 88], [369, seam - 115], [445, seam - 93],
    [540, seam - 89], [700, seam - 102], [700, seam + 30], [-160, seam + 30],
  ], hillCol);

  polygon(ctx, [
    [-160, seam - 55], [0, seam - 58], [105, seam - 50], [173, seam - 82],
    [231, seam - 68], [330, seam - 54], [414, seam - 79], [540, seam - 66],
    [700, seam - 60], [700, seam + 40], [-160, seam + 40],
  ], ridgeCol);

  // Subtle distant tree domes along the ridge
  for (const [tx, ty, rx, ry] of [
    [32, seam - 58, 22, 15], [164, seam - 76, 26, 17], [308, seam - 56, 20, 14],
    [422, seam - 74, 28, 18], [525, seam - 64, 24, 15],
  ]) {
    oval(ctx, tx, ty, rx, ry, v5MixHex(ridgeCol, "#253D34", 0.22));
  }

  // Gliding distant silhouette birds
  if (birds) {
    const b1x = (((110 + t * 24) % 720) + 720) % 720 - 90;
    const b1y = seam - 155 + Math.sin(t * 1.1) * 8;
    v5Bird(ctx, b1x, b1y, 1.0, t * 6.5);
    v5Bird(ctx, b1x - 24, b1y + 11, 0.78, t * 6.5 + 1.1);
    const b2x = (((430 - t * 18) % 720) + 720) % 720 - 90;
    const b2y = seam - 196 + Math.cos(t * 0.9) * 6;
    v5Bird(ctx, b2x, b2y, 0.68, t * 7.2 + 2.0);
  }
  ctx.restore();
}

// Animated wind-swaying banana tree (replaces static banana()).
function v5SwayingBanana(ctx, x, floor, scale, t, wind = 1.0) {
  ctx.save();
  ctx.translate(x, floor);
  ctx.scale(scale, scale);
  const trunkSway = Math.sin(t * 1.8 * wind + x * 0.03) * 3.5 * wind;
  line(ctx, [[-4, 0], [1 + trunkSway * 0.45, -44], [-3 + trunkSway, -88]], "#69794A", 10);
  const leaves = [
    { pts: [[-3, -79], [-33, -115], [-68, -115], [-53, -96], [-26, -89]], fill: "#4E7951", ph: 0.0 },
    { pts: [[-2, -80], [24, -119], [62, -115], [46, -97], [23, -96]], fill: "#5A8E5D", ph: 0.9 },
    { pts: [[0, -72], [40, -91], [75, -78], [52, -70], [30, -76]], fill: "#6F9A59", ph: 1.7 },
    { pts: [[-7, -73], [-35, -90], [-74, -70], [-53, -69], [-27, -78]], fill: "#729C60", ph: 2.4 },
    { pts: [[-4, -84], [-17, -113], [-10, -140], [4, -122], [5, -102]], fill: "#5A8E5D", ph: 3.1 },
  ];
  for (const leaf of leaves) {
    const ang = Math.sin(t * (2.1 + 0.5 * wind) + leaf.ph) * 0.055 * wind;
    ctx.save();
    ctx.translate(trunkSway, 0);
    ctx.translate(leaf.pts[0][0], leaf.pts[0][1]);
    ctx.rotate(ang);
    ctx.translate(-leaf.pts[0][0], -leaf.pts[0][1]);
    polygon(ctx, leaf.pts, leaf.fill);
    line(ctx, [leaf.pts[0], leaf.pts[2]], "#365C4380", 1.5);
    ctx.restore();
  }
  ctx.restore();
}

// Backyard house with dusk warm window illumination + subtle porch light.
function v5House(ctx, x, floor, scale, { roof = "#A64C35", windowGlow = 0 } = {}) {
  ctx.save();
  ctx.translate(x, floor);
  ctx.scale(scale, scale);
  box(ctx, 0, -105, 151, 105, "#F8E6AE");
  polygon(ctx, [[151, -105], [181, -120], [181, -7], [151, 0]], "#C9AB82");
  polygon(ctx, [[-15, -103], [54, -161], [129, -161], [169, -103]], roof);
  polygon(ctx, [[169, -103], [129, -161], [170, -157], [199, -115], [181, -105]], "#753E39");
  for (let y = -151; y < -105; y += 8) {
    line(ctx, [[54 - (y + 151) * 1.12, y], [134 + (y + 151) * 0.6, y]], "#F7C38855", 1.7);
  }
  box(ctx, 19, -77, 42, 33, "#59684A");
  const paneColor = v5MixHex("#CAD8C8", "#FFE27A", windowGlow);
  box(ctx, 23, -73, 34, 25, paneColor);
  if (windowGlow > 0.1) {
    oval(ctx, 40, -60, 40, 28, `rgba(255,220,105,${(0.28 * windowGlow).toFixed(3)})`);
  }
  line(ctx, [[39, -72], [39, -47]], "#59684A", 2);
  box(ctx, 97, -73, 31, 73, "#8E644C");
  box(ctx, 100, -68, 25, 30, "#A07956");
  oval(ctx, 105, -33, 2, 2, "#F0BE6B");
  if (windowGlow > 0.1) {
    oval(ctx, 112, -84, 4, 4, "#FFF2B2");
    oval(ctx, 112, -82, 26, 18, `rgba(255,224,120,${(0.24 * windowGlow).toFixed(3)})`);
  }
  ctx.restore();
}

// Plane 2: Yard midground (fence, swaying shrubs, house, swaying banana, butterfly/fireflies).
function v5DrawMidgroundPlane(ctx, t, seam, cam, opts = {}) {
  const {
    houseAt = [362, seam - 10, 0.8],
    bananaAt = [86, seam - 11, 1.1],
    wind = 1.0,
    windowGlow = 0,
    butterfly = true,
    fireflies = 0,
    gardenGrowth = 0.0,
  } = opts;

  ctx.save();
  v5ApplyPlane(ctx, cam, V5_PARALLAX.midground);

  // Subtle low wooden yard fence spanning across the background yard
  const fenceY = seam - 22;
  line(ctx, [[-120, fenceY - 8], [660, fenceY - 8]], "#8B694D88", 3);
  line(ctx, [[-120, fenceY + 2], [660, fenceY + 2]], "#76573E88", 3);
  for (let fx = -100; fx <= 640; fx += 34) {
    box(ctx, fx, fenceY - 14, 5, 28, "#8B694D88");
  }

  // Swaying yard shrubs that grow slightly lusher with gardenGrowth (0..1)
  const gScale = 1 + 0.35 * gardenGrowth;
  for (const [sx, r, col, ph] of [
    [12, 26, "#5B8E4C", 0.2], [202, 20, "#669A55", 1.5],
    [325, 22, "#57894A", 2.7], [516, 28, "#629651", 0.8],
  ]) {
    const sw = Math.sin(t * 2.2 * wind + ph) * 2.5 * wind;
    oval(ctx, sx + sw, seam - 12 * gScale, r * gScale, r * 0.62 * gScale, col);
    oval(ctx, sx + r * 0.45 + sw * 0.8, seam - 8 * gScale, r * 0.72 * gScale, r * 0.48 * gScale, "#76AD58");
  }

  if (houseAt) v5House(ctx, houseAt[0], houseAt[1], houseAt[2], { windowGlow });
  if (bananaAt) v5SwayingBanana(ctx, bananaAt[0], bananaAt[1], bananaAt[2], t, wind);

  // Daytime butterfly fluttering gently near the banana tree
  if (butterfly && fireflies < 0.3) {
    const bx = (bananaAt ? bananaAt[0] : 90) + 52 + Math.sin(t * 1.45) * 34;
    const by = seam - 92 + Math.sin(t * 2.9) * 14 + Math.cos(t * 1.1) * 10;
    v5Butterfly(ctx, bx, by, t, 0.95);
  }

  // Dusk fireflies
  if (fireflies > 0) {
    v5Fireflies(ctx, t, seam, fireflies);
  }
  ctx.restore();
}

// Plane 3: Hero soil strata + calm caption ground + animated swaying surface grass.
function v5DrawEarthHeroBase(ctx, t, seam, opts = {}) {
  const { earth = "#9D5634", deepSoil = "#743E2C", seed = 13, wind = 1.0, wetness = 0.0 } = opts;
  const earthCol = wetness > 0 ? v5MixHex(earth, "#6D3A22", wetness * 0.45) : earth;
  const grassCol = wetness > 0 ? v5MixHex("#76AD58", "#4D7E3F", wetness * 0.4) : "#76AD58";

  box(ctx, -180, seam, 900, 1200 - seam, earthCol);
  polygon(ctx, [
    [-180, seam + 50], [95, seam + 44], [150, seam + 76], [248, seam + 85],
    [320, seam + 51], [441, seam + 62], [720, seam + 44], [720, seam + 204],
    [437, seam + 198], [368, seam + 211], [290, seam + 183], [189, seam + 193],
    [88, seam + 172], [-180, seam + 187],
  ], "#BE795055");
  // Calm deep soil stratum behind lower caption band (y >= 690 in 540x960 = 1380px)
  polygon(ctx, [
    [-180, seam + 310], [60, seam + 296], [145, seam + 308], [237, seam + 282],
    [328, seam + 298], [432, seam + 284], [720, seam + 305], [720, 1200], [-180, 1200],
  ], deepSoil);
  polygon(ctx, [
    [-180, seam + 430], [87, seam + 412], [163, seam + 422], [238, seam + 392],
    [361, seam + 412], [443, seam + 394], [720, seam + 418], [720, 1200], [-180, 1200],
  ], "#532E2290");

  // Grass turf strip
  box(ctx, -180, seam - 17, 900, 20, grassCol);
  box(ctx, -180, seam + 3, 900, 6, "#537D43");

  // Restrained soil flecks (kept calm & subtle in caption zone)
  const rand = seededRandom(seed);
  for (let i = 0; i < 95; i++) {
    const x = -80 + rand() * 700;
    const y = seam + 17 + rand() * (920 - seam);
    const radius = rand() * 2.8 + 0.6;
    const alpha = y > 665 ? 0.14 : 0.24;
    oval(ctx, x, y, radius, radius * 0.52, i % 3 ? `rgba(243,180,121,${alpha})` : `rgba(72,40,20,${alpha})`, null, 1, rand() - 0.5);
  }
  // Swaying grass tufts along the ground seam
  for (let i = 0; i < 42; i++) {
    const x = -80 + rand() * 700;
    const y = seam - 4 - rand() * 9;
    const ph = rand() * 6.28;
    const sw = Math.sin(t * (2.6 + 0.8 * wind) + ph) * 2.2 * wind;
    line(ctx, [[x - 2 + sw, y - 5], [x, y], [x + 3 + sw, y - 7]], "#487F42AA", 1.3);
  }
}

// Plane 4: Optional subtle foreground grass silhouettes at far margins on wide shots
// (kept completely clear of the central caption box y 690..785).
function v5DrawForegroundEdgeGrass(ctx, t, seam, cam, wind = 1.0) {
  ctx.save();
  v5ApplyPlane(ctx, cam, V5_PARALLAX.foreground);
  const tufts = [
    [-12, seam + 8, 1.0, 0.3], [14, seam + 12, 0.85, 1.4],
    [526, seam + 10, 0.9, 2.1], [548, seam + 8, 1.05, 0.8],
  ];
  for (const [gx, gy, sc, ph] of tufts) {
    const sw = Math.sin(t * 2.8 * wind + ph) * 4.5 * wind;
    ctx.strokeStyle = "#2E5637AA";
    ctx.lineWidth = 3 * sc;
    ctx.lineCap = "round";
    for (const off of [-6, 0, 6]) {
      ctx.beginPath();
      ctx.moveTo(gx + off, gy + 12);
      ctx.quadraticCurveTo(gx + off + sw * 0.5, gy - 8 * sc, gx + off * 1.4 + sw, gy - 22 * sc);
      ctx.stroke();
    }
  }
  ctx.restore();
}

// Reactive rain streaks across the frame (used in rain study & storm episodes).
function v5DrawRain(ctx, t, intensity = 0.8) {
  if (intensity <= 0.02) return;
  ctx.save();
  ctx.strokeStyle = `rgba(220,242,245,${(0.45 * intensity).toFixed(3)})`;
  ctx.lineWidth = 1.8;
  ctx.lineCap = "round";
  const count = Math.round(44 * intensity);
  for (let i = 0; i < count; i++) {
    const seed = (i * 137.5) % 1;
    const x0 = ((i * 53 + t * 140) % 620) - 40;
    const y0 = ((i * 97 + t * 540) % 980) - 40;
    const len = 18 + seed * 14;
    ctx.beginPath();
    ctx.moveTo(x0, y0);
    ctx.lineTo(x0 - len * 0.24, y0 + len);
    ctx.stroke();
  }
  ctx.restore();
}
