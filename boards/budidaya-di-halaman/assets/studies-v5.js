"use strict";

// Visual v5 static studies for style-board.html:
// 1. depthLayers: 4-plane 2.5D parallax & living backyard study
// 2. weatherTime: 3-band reactive time-of-day & weather study (morning / midday / dusk rain)
// 3. eventCamera: 3-pose event-driven camera & organic foley diagram strip

function v5DepthBadge(ctx, x, y, text, tint = "#281D18DD") {
  ctx.save();
  ctx.font = '800 13px "DM Sans", sans-serif';
  const w = ctx.measureText(text).width + 18;
  ctx.fillStyle = tint;
  ctx.beginPath();
  ctx.roundRect(x, y, w, 24, 7);
  ctx.fill();
  ctx.fillStyle = "#FFD44D";
  ctx.fillText(text, x + 9, y + 16.5);
  ctx.restore();
}

function depthLayersStudy(ctx) {
  const t = 4.2;
  const cam = { x: 270, y: 480, zoom: 1.0, shakeX: 0, shakeY: 0 };
  const seam = 412;
  v5DrawSkyPlane(ctx, t, seam, cam, { top: "#515C72", horizon: "#ECC88E", sun: [445, 224, 40], dusk: 0.25 });
  v5DrawHorizonPlane(ctx, t, seam, cam, { birds: true, dusk: 0.15 });
  v5DrawMidgroundPlane(ctx, t, seam, cam, {
    houseAt: [358, seam - 10, 0.8],
    bananaAt: [82, seam - 11, 1.12],
    wind: 1.3,
    windowGlow: 0.65,
    butterfly: true,
    fireflies: 0.55,
    gardenGrowth: 0.5,
  });

  ctx.save();
  v5ApplyPlane(ctx, cam, V5_PARALLAX.hero);
  v5DrawEarthHeroBase(ctx, t, seam, { seed: 13, wind: 1.2, wetness: 0.2 });
  person(ctx, 118, 414);
  oval(ctx, 248, 454, 195, 38, "#A67A52");
  oval(ctx, 248, 455, 186, 31, "#326674", "#203E4B", 3);
  polygon(ctx, [[58, 457], [438, 457], [410, 625], [103, 625]], "#304D55", "#233B3C", 5);
  polygon(ctx, [[66, 455], [431, 455], [400, 613], [112, 613]], color("water"));
  oval(ctx, 248, 455, 175, 25, "#78C7C4");
  polygon(ctx, [[85, 522], [414, 522], [400, 613], [112, 613]], "#41929F80");
  line(ctx, [[68, 473], [425, 473]], "#B4E0D4", 3);
  for (const [x, y, w] of [[148, 454, 31], [216, 444, 42], [336, 446, 33]]) glint(ctx, x, y, w);
  fish(ctx, 178, 520, 1.1, 1, "#D9C49A", true);
  fish(ctx, 310, 548, 1.18, -1, "#E3D3AA", true);
  fish(ctx, 218, 580, 0.85, 1, "#C8C6A1", true);
  // Subtle parallax depth guide brackets
  v5DepthBadge(ctx, 22, 48, "0.18× Sky · drifting clouds & sun arc");
  v5DepthBadge(ctx, 22, 264, "0.45× Horizon · hills & gliding birds");
  v5DepthBadge(ctx, 152, 344, "0.80× Yard · swaying leaves, lit window, micro-life");
  v5DepthBadge(ctx, 22, 636, "1.00× Hero · ripples, wet soil & calm caption ground");
  ctx.restore();
  v5DrawForegroundEdgeGrass(ctx, t, seam, cam, 1.2);
}

function weatherTimeStudy(ctx) {
  const states = [
    {
      y0: 0, h: 320, label: "MORNING · warm breeze & butterfly",
      sky: { top: "#7DA7A8", horizon: "#F3DFB2", sun: [120, 118, 28], dusk: 0, heat: 0, rain: 0 },
      mid: { wind: 0.9, windowGlow: 0, butterfly: true, fireflies: 0 },
      wetness: 0.0, rain: 0,
    },
    {
      y0: 320, h: 320, label: "MIDDAY HEAT · harsh glare & shimmer",
      sky: { top: "#E7C475", horizon: "#F7E9BC", sun: [272, 72, 34], dusk: 0, heat: 0.9, rain: 0 },
      mid: { wind: 0.4, windowGlow: 0, butterfly: false, fireflies: 0 },
      wetness: 0.0, rain: 0,
    },
    {
      y0: 640, h: 320, label: "DUSK RAIN · wet earth, lit window & fireflies",
      sky: { top: "#2C384B", horizon: "#5C6A7B", sun: [450, 155, 22], dusk: 0.95, heat: 0, rain: 0.85 },
      mid: { wind: 2.0, windowGlow: 0.95, butterfly: false, fireflies: 0.85 },
      wetness: 0.85, rain: 0.85,
    },
  ];
  const cam = { x: 270, y: 480, zoom: 1.0, shakeX: 0, shakeY: 0 };
  for (const st of states) {
    ctx.save();
    ctx.beginPath();
    ctx.rect(0, st.y0, 540, st.h);
    ctx.clip();
    ctx.translate(0, st.y0);
    const seam = 228;
    v5DrawSkyPlane(ctx, 2.8, seam, cam, st.sky);
    v5DrawHorizonPlane(ctx, 2.8, seam, cam, { birds: st.rain < 0.2, dusk: st.sky.dusk });
    v5DrawMidgroundPlane(ctx, 2.8, seam, cam, {
      houseAt: [358, seam - 8, 0.72],
      bananaAt: [84, seam - 8, 0.92],
      ...st.mid,
    });
    v5DrawEarthHeroBase(ctx, 2.8, seam, { seed: 41, wind: st.mid.wind, wetness: st.wetness });
    // Mini pond landmark across all 3 weather states
    polygon(ctx, [[120, 240], [340, 240], [322, 304], [142, 304]], "#304D55", "#233B3C", 3);
    polygon(ctx, [[126, 240], [334, 240], [318, 298], [146, 298]], st.rain > 0.2 ? "#4A95A0" : color("water"));
    if (st.rain > 0.2) v5DrawRain(ctx, 2.8, st.rain);
    v5DepthBadge(ctx, 18, 16, st.label);
    ctx.restore();
    if (st.y0 > 0) line(ctx, [[0, st.y0], [540, st.y0]], "#281D18", 4);
  }
}

function eventCameraStudy(ctx) {
  const panels = [
    {
      title: "1. Living drift",
      note: "1.02× wide · yard air bed",
      zoom: 1.0, cx: 105, cy: 60, impact: false, arrow: false,
    },
    {
      title: "2. Snappy punch-in",
      note: "1.22× + 4px settle · foley hit",
      zoom: 1.24, cx: 88, cy: 64, impact: true, arrow: false,
    },
    {
      title: "3. Track & pull-back",
      note: "pan route · water drain SFX",
      zoom: 1.08, cx: 132, cy: 66, impact: false, arrow: true,
    },
  ];
  for (let i = 0; i < 3; i++) {
    const p = panels[i];
    ctx.save();
    ctx.beginPath();
    ctx.roundRect(i * 219, 0, 210, 120, 6);
    ctx.clip();
    ctx.translate(i * 219, 0);
    // Miniature living world + camera box
    box(ctx, 0, 0, 210, 120, color("soil"));
    box(ctx, 0, 0, 210, 44, "#E9DDA8");
    polygon(ctx, [[0, 32], [65, 25], [140, 31], [210, 24], [210, 44], [0, 44]], "#8EB69C");
    box(ctx, 0, 40, 210, 7, color("grass"));
    ctx.save();
    ctx.translate(105, 62);
    ctx.scale(p.zoom, p.zoom);
    ctx.translate(-p.cx, -p.cy);
    polygon(ctx, [[26, 48], [134, 48], [122, 92], [38, 92]], color("liner"), "#233B3C", 2.5);
    polygon(ctx, [[32, 52], [128, 52], [118, 87], [42, 87]], color("water"));
    line(ctx, [[128, 60], [160, 60], [174, 72], [174, 86]], "#BBC5AB", 5);
    if (p.impact) {
      // Impact ring + settle chevron
      oval(ctx, 84, 52, 16, 7, null, "#FFD44D", 2.2);
      line(ctx, [[84, 30], [84, 44]], "#FFD44D", 2.4);
      line(ctx, [[78, 39], [84, 45], [90, 39]], "#FFD44D", 2.4);
    }
    if (p.arrow) {
      line(ctx, [[110, 60], [168, 60]], "#FFD44D", 2.5, [4, 4]);
      line(ctx, [[162, 55], [169, 60], [162, 65]], "#FFD44D", 2.5);
    }
    ctx.restore();
    // Viewfinder frame marks
    ctx.strokeStyle = "#FFD44DCC";
    ctx.lineWidth = 2;
    ctx.strokeRect(8, 8, 194, 104);
    ctx.restore();
  }
}

for (const [id, draw] of Object.entries({
  "depth-layers": depthLayersStudy,
  "weather-time": weatherTimeStudy,
  "event-camera": eventCameraStudy,
})) {
  const canvas = document.getElementById(id);
  if (!canvas) continue;
  const ctx = canvas.getContext("2d");
  ctx.scale(2, 2);
  ctx.lineJoin = "round";
  ctx.lineCap = "round";
  draw(ctx);
}
