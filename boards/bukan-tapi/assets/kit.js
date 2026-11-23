// Bukan, Tapi — drawing kit. Original 2D shapes on Canvas; every picture is a pure function of its inputs.
export const W = 1080, H = 1920, HORIZON = 1010;
export const INK = "#1F2140", WHITE = "#FFFBF2", HILITE = "#FF7A2F";
export const PALETTES = {
  workshop: { skyTop: "#F9E7C4", skyLow: "#FCF3DF", far: "#E9C99A", near: "#D9A96E", ground: "#C98B52", groundLow: "#B5773F", sun: "#FFF6DA" },
  night: { skyTop: "#232B5C", skyLow: "#3D4A86", far: "#2E3A70", near: "#27315F", ground: "#3A4578", groundLow: "#2B3463", sun: "#F4EFD8" },
  room: { skyTop: "#F3D9C2", skyLow: "#F8E7D6", far: "#E6BFA2", near: "#D9A988", ground: "#A9705A", groundLow: "#8F5A47", sun: "#FFF3E2" },
  dusk: { skyTop: "#C9D8EE", skyLow: "#F6DDD0", far: "#A9B7D8", near: "#8E9CC6", ground: "#7A86B4", groundLow: "#66719E", sun: "#FFE9C7" },
};
export const BODY = { clay: "#E2674A", teal: "#2E9C93", plum: "#7C5BB3", moss: "#7FA650", sand: "#E8B656" };

export const clamp01 = (v) => Math.min(1, Math.max(0, v));
export const lerp = (a, b, p) => a + (b - a) * p;
export const span = (t, a, b) => clamp01((t - a) / (b - a));
export const outCubic = (p) => 1 - Math.pow(1 - clamp01(p), 3);
export const outBack = (p) => { p = clamp01(p); const c = 1.70158; return 1 + (c + 1) * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2); };
export const inOut = (p) => { p = clamp01(p); return p * p * (3 - 2 * p); };
const rnd = (i) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

function rr(c, x, y, w, h, r) { c.beginPath(); c.roundRect(x, y, w, h, r); }
function stroke(c, w = 8) { c.lineWidth = w; c.strokeStyle = INK; c.lineJoin = c.lineCap = "round"; c.stroke(); }

// Flat stage: sky, sun disc, two hill bands, ground. `drift` slides the hills for parallax.
export function stage(c, pal, { drift = 0, sunX = 800, sunY = 420, horizon = HORIZON, indoor = false } = {}) {
  const g = c.createLinearGradient(0, 0, 0, horizon);
  g.addColorStop(0, pal.skyTop); g.addColorStop(1, pal.skyLow);
  c.fillStyle = g; c.fillRect(-400, -400, W + 800, horizon + 400);
  if (indoor) {
    c.fillStyle = pal.far; c.fillRect(-400, horizon - 150, W + 800, 150);
    rr(c, 640, 300, 300, 360, 28); c.fillStyle = pal.sun; c.fill(); stroke(c, 8);
    c.beginPath(); c.moveTo(790, 300); c.lineTo(790, 660); c.moveTo(640, 480); c.lineTo(940, 480); stroke(c, 6);
  } else {
    c.fillStyle = pal.sun; c.beginPath(); c.arc(sunX, sunY, 92, 0, 7); c.fill();
    for (const [col, base, amp, k, par] of [[pal.far, horizon - 150, 70, 0.0052, 0.3], [pal.near, horizon - 60, 50, 0.0081, 0.6]]) {
      c.fillStyle = col; c.beginPath(); c.moveTo(-400, horizon + 4);
      for (let x = -400; x <= W + 400; x += 20) c.lineTo(x, base - amp * (0.5 + 0.5 * Math.sin((x + drift * par) * k + par * 9)));
      c.lineTo(W + 400, horizon + 4); c.fill();
    }
  }
  const gg = c.createLinearGradient(0, horizon, 0, H);
  gg.addColorStop(0, pal.ground); gg.addColorStop(1, pal.groundLow);
  c.fillStyle = gg; c.fillRect(-400, horizon, W + 800, H - horizon + 400);
  c.strokeStyle = INK; c.lineWidth = 6; c.beginPath(); c.moveTo(-400, horizon); c.lineTo(W + 400, horizon); c.stroke();
  c.globalAlpha = 0.16; c.fillStyle = INK;
  for (let i = 0; i < 26; i++) { rr(c, rnd(i) * (W + 300) - 150, horizon + 60 + rnd(i + 50) * 760, 40 + rnd(i + 9) * 70, 7, 4); c.fill(); }
  c.globalAlpha = 1;
}

// Bean person. (x, y) is the feet midpoint; s scales a 220 x 430 figure.
// o: color, face ("calm" | "glad" | "worry" | "shock" | "smug"), look (-1..1), armL/armR (deg, 0 = down, + = forward/up),
// lean (deg), squash (0..1), sit (0..1), hat ("cap" | "band" | "bun" | null), flip, blink, sweat
export function bean(c, x, y, s, o = {}) {
  const { color = BODY.clay, face = "calm", look = 0, armL = 8, armR = 8, lean = 0, squash = 0, sit = 0, hat = null, flip = false, blink = false, sweat = 0, hold = null } = o;
  c.save(); c.translate(x, y); c.scale(s * (flip ? -1 : 1), s);
  c.globalAlpha = 0.2; c.fillStyle = INK; c.beginPath(); c.ellipse(0, 6, 130, 20, 0, 0, 7); c.fill(); c.globalAlpha = 1;
  const leg = lerp(96, 36, sit), bw = 210 * (1 + squash * 0.08), bh = 320 * (1 - squash * 0.08);
  for (const lx of [-52, 52]) { rr(c, lx - 24, -leg - 10, 48, leg + 10, 20); c.fillStyle = INK; c.fill(); rr(c, lx - 34 + (lx > 0 ? 8 : -8) * 0 + 6, -22, 62, 26, 13); c.fill(); }
  c.translate(0, -leg); c.rotate((lean * Math.PI) / 180);
  const arm = (side, deg, front) => {
    const ax = side * (bw / 2 - 14), ay = -bh * 0.56, a = ((90 - deg) * Math.PI) / 180, L = 150;
    const ex = ax + Math.cos(a) * L * (front ? 1 : side), ey = ay + Math.sin(a) * L;
    c.beginPath(); c.moveTo(ax, ay); c.lineTo(ex, ey); c.lineWidth = 40; c.strokeStyle = INK; c.lineCap = "round"; c.stroke();
    c.lineWidth = 24; c.strokeStyle = color; c.stroke();
    c.beginPath(); c.arc(ex, ey, 27, 0, 7); c.fillStyle = color; c.fill(); stroke(c, 8);
    return [ex, ey];
  };
  arm(-1, armL, false);
  rr(c, -bw / 2, -bh, bw, bh, 100); c.fillStyle = color; c.fill(); stroke(c, 9);
  c.save(); rr(c, -bw / 2, -bh, bw, bh, 100); c.clip(); c.globalAlpha = 0.14; c.fillStyle = INK; c.fillRect(-bw / 2, -bh * 0.3, bw, bh); c.globalAlpha = 1; c.restore();
  const fy = -bh * 0.7, fx = look * 20;
  c.fillStyle = INK;
  for (const ex of [-40, 40]) {
    if (blink) { c.beginPath(); c.moveTo(fx + ex - 14, fy); c.lineTo(fx + ex + 14, fy); stroke(c, 7); }
    else { c.beginPath(); c.ellipse(fx + ex, fy, face === "shock" ? 15 : 11, face === "shock" ? 19 : 15, 0, 0, 7); c.fill(); }
  }
  const brow = { calm: [0, 0], glad: [-4, 0], worry: [10, -1], shock: [-14, 0], smug: [2, 1] }[face];
  for (const side of [-1, 1]) { c.beginPath(); c.moveTo(fx + side * 58, fy - 34 + brow[0] * (brow[1] ? -1 : 1) * 0 - (brow[1] === -1 ? -brow[0] : 0)); c.lineTo(fx + side * 24, fy - 34 - (brow[1] === -1 ? brow[0] : brow[1] === 1 ? -8 : 0) + (face === "shock" ? -14 : 0)); stroke(c, 7); }
  c.beginPath();
  if (face === "glad") c.arc(fx, fy + 30, 26, 0.15, Math.PI - 0.15);
  else if (face === "worry") c.arc(fx, fy + 62, 24, Math.PI + 0.35, -0.35);
  else if (face === "shock") c.ellipse(fx, fy + 46, 13, 17, 0, 0, 7);
  else if (face === "smug") { c.moveTo(fx - 22, fy + 44); c.quadraticCurveTo(fx + 6, fy + 56, fx + 28, fy + 36); }
  else { c.moveTo(fx - 18, fy + 44); c.lineTo(fx + 18, fy + 44); }
  stroke(c, 7);
  if (hat === "cap") { c.beginPath(); c.moveTo(-bw / 2 + 6, -bh + 74); c.quadraticCurveTo(0, -bh - 48, bw / 2 - 6, -bh + 74); c.closePath(); c.fillStyle = INK; c.fill(); rr(c, 20, -bh + 56, 130, 22, 11); c.fill(); }
  if (hat === "band") { c.save(); rr(c, -bw / 2, -bh, bw, bh, 100); c.clip(); c.fillStyle = WHITE; c.fillRect(-bw / 2, -bh + 52, bw, 30); c.strokeStyle = INK; c.lineWidth = 6; c.strokeRect(-bw / 2 - 9, -bh + 52, bw + 18, 30); c.restore(); }
  if (hat === "bun") { c.beginPath(); c.arc(0, -bh - 18, 36, 0, 7); c.fillStyle = INK; c.fill(); }
  for (let i = 0; i < sweat; i++) { const sx = (i ? 1 : -1) * (bw / 2 + 26 + i * 6), sy = -bh + 50 + i * 46; c.beginPath(); c.moveTo(sx, sy - 20); c.quadraticCurveTo(sx + 15, sy + 6, sx, sy + 12); c.quadraticCurveTo(sx - 15, sy + 6, sx, sy - 20); c.fillStyle = "#9FD8F2"; c.fill(); stroke(c, 5); }
  const hand = arm(1, armR, true);
  if (hold) { c.save(); c.translate(hand[0], hand[1]); hold(c); c.restore(); }
  c.restore();
}

export function saw(c, { angle = -20, sharp = 0 } = {}) {
  c.save(); c.rotate((angle * Math.PI) / 180);
  c.beginPath(); c.moveTo(20, -26); c.lineTo(250, -14); c.lineTo(250, 14);
  for (let i = 11; i >= 0; i--) { c.lineTo(30 + i * 19 + 9, 34); c.lineTo(30 + i * 19, 20); }
  c.closePath(); c.fillStyle = sharp ? "#F2F6FA" : "#C9CED6"; c.fill(); stroke(c, 6);
  rr(c, -46, -36, 74, 72, 22); c.fillStyle = "#7A4A2B"; c.fill(); stroke(c, 7);
  c.restore();
}
export function bench(c, x, y, s, { cut = 0 } = {}) {
  c.save(); c.translate(x, y); c.scale(s, s);
  for (const lx of [-150, 150]) { c.beginPath(); c.moveTo(lx - 30, 0); c.lineTo(lx, -150); c.lineTo(lx + 30, 0); stroke(c, 14); }
  rr(c, -230, -190, 460, 44, 10); c.fillStyle = "#E9C58F"; c.fill(); stroke(c, 8);
  c.beginPath(); c.moveTo(60, -190); c.lineTo(60, -190 + 44 * cut); stroke(c, 7);
  c.restore();
}
export function planks(c, x, y, s, n) {
  c.save(); c.translate(x, y); c.scale(s, s);
  for (let i = 0; i < n; i++) { rr(c, -120 + (i % 2) * 14, -34 * (i + 1), 240, 30, 8); c.fillStyle = i % 2 ? "#E9C58F" : "#DDB377"; c.fill(); stroke(c, 6); }
  c.restore();
}
export function coins(c, x, y, s, n) {
  c.save(); c.translate(x, y); c.scale(s, s);
  for (let i = 0; i < n; i++) { c.beginPath(); c.ellipse(0, -i * 22, 86, 24, 0, 0, 7); c.fillStyle = i % 2 ? "#FFD25E" : "#F5BE3B"; c.fill(); stroke(c, 6); }
  c.restore();
}
export function stone(c, x, y, s) { c.save(); c.translate(x, y); c.scale(s, s); rr(c, -110, -50, 220, 50, 12); c.fillStyle = "#8D93A6"; c.fill(); stroke(c, 8); c.restore(); }
export function sparkle(c, x, y, r) { c.save(); c.translate(x, y); c.beginPath(); for (let i = 0; i < 8; i++) { const a = (i * Math.PI) / 4, q = i % 2 ? r * 0.3 : r; c.lineTo(Math.cos(a) * q, Math.sin(a) * q); } c.closePath(); c.fillStyle = WHITE; c.fill(); stroke(c, 5); c.restore(); }
export function dust(c, x, y, t, n = 9) {
  c.fillStyle = "#F3DDB4";
  for (let i = 0; i < n; i++) { const p = (t * 1.6 + rnd(i)) % 1, a = -0.4 - rnd(i + 7) * 2.2; c.globalAlpha = 1 - p; c.beginPath(); c.arc(x + Math.cos(a) * p * 150, y + Math.sin(a) * p * 110 + p * p * 150, 9 - p * 5, 0, 7); c.fill(); }
  c.globalAlpha = 1;
}

const FONT = (px, w = 800) => `${w} ${px}px "Plus Jakarta Sans"`;
// Paper tag that follows an object: text on WHITE, ink outline, slight tilt, pops in with `grow`.
export function tag(c, x, y, text, { grow = 1, tilt = -3, size = 46, fill = WHITE, color = INK } = {}) {
  if (grow <= 0) return;
  c.save(); c.translate(x, y); c.rotate((tilt * Math.PI) / 180); c.scale(grow, grow);
  c.font = FONT(size); const w = c.measureText(text).width + 52, h = size + 34;
  rr(c, -w / 2, -h / 2, w, h, 18); c.fillStyle = fill; c.fill(); stroke(c, 7);
  c.fillStyle = color; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText(text, 0, 3);
  c.restore();
}
export function bubble(c, x, y, text, { grow = 1, tail = -1, size = 50 } = {}) {
  if (grow <= 0) return;
  c.save(); c.translate(x, y); c.scale(grow, grow);
  c.font = FONT(size, 700); const lines = text.split("\n"), w = Math.max(...lines.map((l) => c.measureText(l).width)) + 76, h = lines.length * size * 1.2 + 56;
  c.beginPath(); c.roundRect(-w / 2, -h, w, h, 44); c.moveTo(tail * 30 - 24, -4); c.lineTo(tail * 70, 54); c.lineTo(tail * 30 + 26, -4);
  c.fillStyle = WHITE; c.fill(); stroke(c, 8);
  c.fillStyle = WHITE; c.fillRect(tail * 30 - 20, -12, 42, 12);
  c.fillStyle = INK; c.textAlign = "center"; c.textBaseline = "middle";
  lines.forEach((l, i) => c.fillText(l, 0, -h + 28 + size * 0.6 + i * size * 1.2));
  c.restore();
}

// Caption: lowercase groups of 1–3 words centred at y; the spoken word sits in a HILITE box with ink text.
export function caption(c, words, active, { y = 1500, size = 68 } = {}) {
  c.save(); c.font = FONT(size); c.textBaseline = "middle"; c.textAlign = "left";
  const gap = size * 0.3, ws = words.map((w) => c.measureText(w).width), total = ws.reduce((a, b) => a + b, 0) + gap * (words.length - 1);
  let x = (W - total) / 2;
  words.forEach((w, i) => {
    if (i === active) { rr(c, x - 16, y - size * 0.68, ws[i] + 32, size * 1.36, 16); c.fillStyle = HILITE; c.fill(); stroke(c, 6); c.fillStyle = INK; c.fillText(w, x, y + 3); }
    else { c.lineWidth = 12; c.strokeStyle = INK; c.lineJoin = "round"; c.strokeText(w, x, y + 3); c.fillStyle = WHITE; c.fillText(w, x, y + 3); }
    x += ws[i] + gap;
  });
  c.restore();
}

// Split a sentence over [start, end) into caption groups with per-word times proportional to length.
export function timeWords(sentences) {
  const groups = [];
  for (const { text, start, end, words: measured } of sentences) {
    const words = text.split(" "), weights = words.map((w) => w.length + 2), total = weights.reduce((a, b) => a + b, 0);
    let t = start; const timed = words.map((w, i) => { const s = t; t += ((end - start) * weights[i]) / total; return measured ? { w: w.toLowerCase(), s: measured[i][0], e: measured[i][1] } : { w: w.toLowerCase(), s, e: t }; });
    for (let i = 0; i < timed.length;) {
      let n = 1; while (n < 3 && i + n < timed.length && timed.slice(i, i + n + 1).reduce((a, b) => a + b.w.length, 0) <= 16 && !/[.,:?]$/.test(timed[i + n - 1].w)) n++;
      groups.push(timed.slice(i, i + n)); i += n;
    }
  }
  return groups;
}
export function captionAt(c, groups, t, opts) {
  const g = groups.findLast((g) => g[0].s <= t); if (!g || t > g[g.length - 1].e + 0.25) return;
  caption(c, g.map((x) => x.w), g.findLastIndex((x) => x.s <= t), opts);
}
