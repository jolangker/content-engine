// Bukan, Tapi — sample compositions and the motion pilot. Copy and figures are illustrative.
import * as K from "./kit.js";
const { W, H, HORIZON, PALETTES: P, BODY, lerp, span, outCubic, outBack, inOut } = K;

// Camera: scale about a focus point, plus a slide (dx for the whip, dy to keep the action above the caption band).
function cam(c, { zoom = 1, fx = W / 2, fy = HORIZON, dx = 0, dy = 0 }, draw) {
  c.save(); c.translate(fx + dx, fy + dy); c.scale(zoom, zoom); c.translate(-fx, -fy); draw(); c.restore();
}
const holdSaw = (o) => (c) => K.saw(c, o);

// ---- Static studies: four unrelated illustrative stories, one communication need each.
export const STUDIES = {
  hook(c) {
    K.stage(c, P.dusk, { sunX: 260, sunY: 380 });
    K.coins(c, 250, 1200, 1.1, 2); K.coins(c, 830, 1200, 1.1, 2);
    K.bean(c, 300, 1500, 1.25, { color: BODY.plum, face: "smug", look: 0.6, armR: 60, hat: "cap" });
    K.bean(c, 780, 1500, 1.25, { color: BODY.sand, face: "calm", look: -0.6, armR: 20, hat: "bun", flip: true });
    K.tag(c, 300, 760, "modal sama", { tilt: -4 }); K.tag(c, 780, 760, "modal sama", { tilt: 3 });
    K.caption(c, ["dua", "pedagang,"], 1, { y: 1640 });
  },
  dialogue(c) {
    K.stage(c, P.room, { indoor: true });
    K.bean(c, 320, 1480, 1.35, { color: BODY.teal, face: "calm", look: 0.7, armR: 70, hat: "band" });
    K.bean(c, 790, 1480, 0.9, { color: BODY.clay, face: "worry", look: -0.8, armL: 20, armR: 30, flip: true, sweat: 1 });
    K.bubble(c, 420, 640, "ini boleh kamu\nhabiskan hari ini.", { tail: -1 });
    K.caption(c, ["kata", "ayahnya"], 1, { y: 1640 });
  },
  cutaway(c) {
    K.stage(c, P.night, { sunX: 820, sunY: 360 });
    cam(c, { zoom: 1.5, fx: 540, fy: 1250 }, () => { K.coins(c, 540, 1330, 1.5, 7); });
    K.sparkle(c, 760, 900, 46); K.sparkle(c, 330, 1040, 30);
    K.tag(c, 540, 660, "hari ke-30", { size: 54, tilt: -3 });
    K.tag(c, 760, 1180, "+ 7 keping", { size: 44, tilt: 4, fill: K.HILITE });
    K.caption(c, ["sedikit", "demi", "sedikit"], 0, { y: 1640 });
  },
  reveal(c) {
    K.stage(c, P.workshop, { sunX: 250, sunY: 400 });
    K.planks(c, 300, 1330, 1.2, 4); K.planks(c, 800, 1330, 1.2, 9);
    K.bean(c, 300, 1560, 1.1, { color: BODY.clay, face: "shock", look: 0.8, armL: 30, armR: 30, hat: "cap", sweat: 2 });
    K.bean(c, 800, 1560, 1.1, { color: BODY.teal, face: "glad", look: -0.5, armR: 150, hat: "band", flip: true, hold: holdSaw({ angle: -70, sharp: 1 }) });
    K.tag(c, 300, 1060, "62 papan", { tilt: -4 }); K.tag(c, 800, 860, "100 papan", { tilt: 3, fill: K.HILITE, size: 54 });
    K.caption(c, ["yang", "sering", "berhenti"], 2, { y: 1680 });
  },
};

// ---- Motion pilot: "Dua tukang kayu". Word times come from the recorded take
// (motion-preview/audio/narration.words.json) plus a 0.15 s lead-in.
export const DURATION = 16;
export const NARRATION = [
  { text: "Dua tukang kayu dapat pesanan yang sama:", start: 0.15, end: 2.09, words: [[0.15, 0.41], [0.41, 0.69], [0.69, 1.07], [1.07, 1.25], [1.25, 1.63], [1.63, 1.79], [1.79, 2.09]] },
  { text: "seratus papan, tenggat satu hari.", start: 2.53, end: 4.65, words: [[2.53, 2.91], [2.91, 3.39], [3.71, 4.07], [4.07, 4.33], [4.33, 4.65]] },
  { text: "Tukang pertama menggergaji tanpa henti sejak pagi.", start: 5.13, end: 8.01, words: [[5.13, 5.47], [5.47, 5.77], [5.77, 6.47], [6.47, 6.97], [6.97, 7.27], [7.27, 7.61], [7.61, 8.01]] },
  { text: "Tukang kedua berhenti tiap jam,", start: 8.37, end: 9.87, words: [[8.37, 8.63], [8.63, 8.99], [8.99, 9.37], [9.37, 9.65], [9.65, 9.87]] },
  { text: "hanya untuk mengasah gergajinya.", start: 10.25, end: 11.87, words: [[10.25, 10.47], [10.47, 10.73], [10.73, 11.25], [11.25, 11.87]] },
  { text: "Siapa pun pasti mengira,", start: 12.41, end: 13.53, words: [[12.41, 12.67], [12.67, 12.85], [12.85, 13.07], [13.07, 13.53]] },
  { text: "yang tak pernah berhenti akan menang.", start: 13.83, end: 15.51, words: [[13.83, 13.93], [13.93, 14.09], [14.09, 14.31], [14.31, 14.77], [14.77, 15.11], [15.11, 15.51]] },
];
export const CUTS = [2.45, 5.05, 8.25, 10.15, 12.3, 13.75];
const GROUPS = K.timeWords(NARRATION);
const WHIP = [8.07, 8.43];

function carpenter(c, x, y, s, who, o = {}) {
  const a = who === "a";
  K.bean(c, x, y, s, { color: a ? BODY.clay : BODY.teal, hat: a ? "cap" : "band", flip: !a, ...o });
}
const sawing = (t, rate) => Math.sin(t * rate * Math.PI * 2);

function shot(c, t) {
  if (t < CUTS[0]) { // hook: both carpenters, the order lands
    const push = lerp(1, 1.06, span(t, 0, CUTS[0]));
    cam(c, { zoom: push, fy: 1200 }, () => {
      K.stage(c, P.workshop, { drift: t * 30 });
      const nod = t > 1.5 ? 6 * Math.sin((t - 1.5) * 6) * (1 - span(t, 1.5, 2.4)) : 0;
      carpenter(c, 290, 1380, 1.05, "a", { face: t > 1.3 ? "smug" : "calm", look: 0.7, armR: lerp(10, 95, outBack(span(t, 0.1, 0.5))), lean: nod, hold: holdSaw({ angle: -60 }) });
      carpenter(c, 790, 1380, 1.05, "b", { face: "calm", look: -0.6, armR: lerp(10, 80, outBack(span(t, 0.35, 0.75))), lean: -nod, hold: holdSaw({ angle: -60 }), blink: t > 2.0 && t < 2.15 });
      K.tag(c, 540, 640, "pesanan sama", { grow: outBack(span(t, 0.25, 0.6)), size: 56, tilt: -3 });
    });
  } else if (t < CUTS[1]) { // cutaway: the order itself
    const u = t - CUTS[0], n = Math.min(10, 1 + Math.floor(u / 0.11));
    cam(c, { zoom: lerp(1.25, 1.34, span(u, 0, 2.2)), fx: 540, fy: 1300 }, () => {
      K.stage(c, P.workshop, { sunX: lerp(300, 760, inOut(span(u, 0.9, 2.1))), sunY: 420 - 90 * Math.sin(span(u, 0.9, 2.1) * Math.PI) });
      K.planks(c, 540, 1420, 1.5, n);
    });
    K.tag(c, 540, 600, "100 papan", { grow: outBack(span(u, 0.15, 0.5)), size: 64, fill: K.HILITE, tilt: -3 });
    K.tag(c, 760, 1240, "tenggat: 1 hari", { grow: outBack(span(u, 1.0, 1.35)), tilt: 4 });
  } else if (t < CUTS[2]) { // path A: never stops
    const u = t - CUTS[1], s = sawing(u, 2.6), done = 3 + Math.floor(u * 3.2);
    const dx = t > WHIP[0] ? -1500 * Math.pow(span(t, WHIP[0], CUTS[2]), 2) : 0;
    if (dx) cam(c, { zoom: 1.2, fx: 470, fy: 1300, dy: -150 }, () => K.stage(c, P.workshop, { sunX: -400 })); // keeps the bands continuous behind the slide
    cam(c, { zoom: lerp(1.12, 1.2, span(u, 0, 2.8)), fx: 470, fy: 1300, dx, dy: -150 }, () => {
      K.stage(c, P.workshop, { sunX: 300, sunY: 430 });
      K.planks(c, 860, 1500, 0.95, Math.min(done, 12));
      K.bench(c, 520, 1640, 1.1, { cut: (u * 2.6) % 1 });
      K.dust(c, 590, 1440, u);
      carpenter(c, 330, 1470, 1.2, "a", { face: "worry", look: 0.9, armR: 62 + s * 22, lean: 10 + s * 4, squash: 0.5 + s * 0.5, sweat: u > 1.2 ? 2 : 1, hold: holdSaw({ angle: -8 + s * 5 }) });
    });
    K.tag(c, 820, 560, `${done} papan`, { grow: outBack(span(u, 0.2, 0.5)) * (dx ? 0 : 1), tilt: 4 });
  } else if (t < CUTS[3]) { // path B: stops every hour
    const u = t - CUTS[2], stop = span(u, 0.9, 1.15), s = sawing(u, 1.7) * (1 - stop);
    const dx = t < WHIP[1] ? 1500 * Math.pow(1 - span(t, CUTS[2], WHIP[1]), 2) : 0;
    if (dx) cam(c, { zoom: 1.12, fx: 610, fy: 1300, dy: -150 }, () => K.stage(c, P.workshop, { sunX: -400 }));
    cam(c, { zoom: 1.12, fx: 610, fy: 1300, dx, dy: -150 }, () => {
      K.stage(c, P.workshop, { sunX: 780, sunY: 400 });
      K.planks(c, 220, 1500, 0.95, 4);
      K.bench(c, 560, 1640, 1.1, { cut: 0.4 });
      if (!stop) K.dust(c, 500, 1440, u, 5);
      carpenter(c, 750, 1470, 1.2, "b", { face: stop ? "calm" : "calm", look: lerp(-0.9, 0.2, stop), armR: lerp(62 + s * 18, 120, outBack(stop)), lean: lerp(8, -4, stop), blink: u > 1.4 && u < 1.52, hold: holdSaw({ angle: lerp(-8, -75, outCubic(stop)) }) });
    });
    K.tag(c, 330, 600, "tiap jam: berhenti", { grow: outBack(span(u, 1.05, 1.4)), tilt: -4 });
  } else if (t < CUTS[4]) { // close cutaway: sharpening
    const u = t - CUTS[3], s = sawing(u, 2.2);
    cam(c, { zoom: lerp(1.5, 1.62, span(u, 0, 2.1)), fx: 540, fy: 1380, dy: -130 }, () => {
      K.stage(c, P.workshop, { horizon: 1180, sunX: 250, sunY: 500 });
      K.bench(c, 540, 1700, 1.3);
      K.stone(c, 540, 1453, 1.2);
      c.save(); c.translate(430 + s * 70, 1385); K.saw(c, { angle: -4, sharp: span(u, 1.0, 1.5) }); c.restore();
      if (u > 0.3) for (let i = 0; i < 3; i++) K.sparkle(c, 600 + s * 70 + i * 46, 1350 - ((u * 220 + i * 60) % 110), 16 - i * 3);
    });
    K.bubble(c, 620, 860, "asah dulu.", { grow: outBack(span(u, 0.35, 0.7)), tail: -1, size: 60 });
  } else if (t < CUTS[5]) { // wide: the score so far
    const u = t - CUTS[4], s = sawing(u, 2.6);
    K.stage(c, P.workshop, { sunX: 560, sunY: 330, drift: 200 + u * 30 });
    K.planks(c, 290, 1180, 1.05, 9); K.planks(c, 790, 1180, 1.05, 6);
    carpenter(c, 290, 1420, 1.0, "a", { face: "worry", look: 0.6, armR: 62 + s * 22, lean: 8 + s * 4, sweat: 2, hold: holdSaw({ angle: -8 + s * 5 }) });
    carpenter(c, 790, 1420, 1.0, "b", { face: "calm", look: -0.3, armR: 118, hold: holdSaw({ angle: -75, sharp: 1 }), blink: u > 0.8 && u < 0.92 });
    K.tag(c, 290, 790, "38 papan", { grow: outBack(span(u, 0.15, 0.45)), tilt: -4, size: 52 });
    K.tag(c, 790, 890, "27 papan", { grow: outBack(span(u, 0.5, 0.8)), tilt: 3, size: 52 });
  } else { // false expectation: push in on the one who never stops
    const u = t - CUTS[5], s = sawing(u, 2.6);
    cam(c, { zoom: lerp(1.3, 1.5, outCubic(span(u, 0, 2.4))), fx: 470, fy: 1250, dy: -190 }, () => {
      K.stage(c, P.workshop, { sunX: 760, sunY: 420 });
      K.planks(c, 800, 1480, 1, 11);
      K.bench(c, 520, 1640, 1.1, { cut: (u * 2.6) % 1 });
      K.dust(c, 590, 1440, u);
      carpenter(c, 330, 1470, 1.2, "a", { face: "smug", look: 0.2, armR: 62 + s * 22, lean: 10 + s * 4, squash: 0.5 + s * 0.5, sweat: 2, hold: holdSaw({ angle: -8 + s * 5 }) });
    });
    K.tag(c, 700, 480, "pasti menang?", { grow: outBack(span(u, 0.9, 1.25)), size: 62, tilt: -4, fill: K.HILITE });
  }
}

export function renderPilot(c, t) {
  c.clearRect(0, 0, W, H);
  shot(c, Math.min(t, DURATION - 0.001));
  K.captionAt(c, GROUPS, t, { y: 1500 });
}
