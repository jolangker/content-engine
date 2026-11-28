"use strict";

// Revision 6 studies. Reuses the drawing helpers from studies.js.

function scale(ctx, x, top, floor, { fish: count = 3, dip = 0, needle = 1 } = {}) {
  for (const post of [x - 62, x + 62]) {
    line(ctx, [[post, top], [post, floor]], "#6F4E3A", 9);
    line(ctx, [[post - 2, top + 4], [post - 2, floor - 4]], "#9A7456", 2.5);
  }
  line(ctx, [[x - 74, top], [x + 74, top]], "#6F4E3A", 10);
  line(ctx, [[x, top + 4], [x, top + 22]], "#3E4A44", 2.5);
  oval(ctx, x, top + 38, 17, 17, "#F4EBD0", "#3E4A44", 3);
  const angle = -Math.PI / 2 - .9 + needle * 1.7;
  line(ctx, [[x, top + 38], [x + 12.7 * Math.cos(angle), top + 38 + 12.7 * Math.sin(angle)]], "#A64C35", 2.4);
  oval(ctx, x, top + 38, 2.4, 2.4, "#3E4A44");
  ctx.save();
  ctx.translate(0, dip);
  line(ctx, [[x, top + 55 - dip], [x, top + 70]], "#3E4A44", 2.5);
  line(ctx, [[x, top + 70], [x - 36, top + 92]], "#3E4A44", 1.6);
  line(ctx, [[x, top + 70], [x + 36, top + 92]], "#3E4A44", 1.6);
  polygon(ctx, [[x - 40, top + 91], [x + 40, top + 91], [x + 30, top + 114], [x - 30, top + 114]], "#3E8C93", "#245256", 3);
  for (const [fx, fy, rot, dir] of [[x - 16, top + 88, -.25, 1], [x + 14, top + 87, .2, -1], [x, top + 82, .05, 1]].slice(0, count)) {
    ctx.save();
    ctx.translate(fx, fy);
    ctx.rotate(rot);
    fish(ctx, 0, 0, .78, dir, "#D9C49A", true);
    ctx.restore();
  }
  line(ctx, [[x - 40, top + 92], [x + 40, top + 92]], "#245256", 3);
  ctx.restore();
}

function basin(ctx, x, floor, count = 3) {
  oval(ctx, x, floor + 2, 46, 6, "#2546333A");
  polygon(ctx, [[x - 45, floor - 32], [x + 45, floor - 32], [x + 34, floor], [x - 34, floor]], "#3E8C93", "#245256", 3);
  oval(ctx, x, floor - 32, 45, 7, "#5EB5BC", "#245256", 3);
  for (const [fx, fy, rot, dir] of [[x - 20, floor - 37, -.3, 1], [x + 16, floor - 38, .25, -1], [x - 1, floor - 42, 0, 1]].slice(0, count)) {
    ctx.save();
    ctx.translate(fx, fy);
    ctx.rotate(rot);
    fish(ctx, 0, 0, .8, dir, "#D9C49A", true);
    ctx.restore();
  }
}

// The beam overhang and nail the price tag hangs from, in world units (nail at 300, 297).
function tagNail(ctx) {
  line(ctx, [[262, 295.2], [314, 295.2]], "#6F4E3A", 16);
  line(ctx, [[262, 291], [312, 291]], "#9A7456", 2.5);
  oval(ctx, 300, 297, 3.2, 3.2, "#3E4A44");
}

function market(ctx) {
  terrain(ctx, 512, { top: "#D6DDB8", horizon: color("sky"), sun: [452, 120, 31],
    earth: color("soil"), ridge: "#76A07C", seed: 61 });
  house(ctx, 472, 500, .42);
  banana(ctx, 30, 500, .9);
  const grouped = (x, s, draw) => {
    ctx.save();
    ctx.translate(x, 500);
    ctx.scale(s, s);
    draw();
    ctx.restore();
  };
  grouped(150, 1.6, () => scale(ctx, 0, -128, 0));
  grouped(318, 1.35, () => basin(ctx, 0, 0));
  grouped(432, 1.45, () => person(ctx, 0, 1));
  tagNail(ctx);

  polygon(ctx, [[57, 542], [437, 542], [413, 682], [99, 682]], "#304D55", "#233B3C", 5);
  polygon(ctx, [[65, 541], [430, 541], [405, 670], [107, 670]], color("water"));
  oval(ctx, 247, 541, 191, 15, "#78C7C4", "#203E4B", 3);
  polygon(ctx, [[86, 600], [413, 600], [405, 670], [107, 670]], "#41929F80");
  line(ctx, [[68, 556], [426, 556]], "#B4E0D4", 3);
  for (const [x, y, s, d] of [[168, 590, .95, 1], [300, 612, 1.05, -1], [222, 642, .78, 1], [352, 648, .74, -1]]) {
    fish(ctx, x, y, s, d, "#D9C49A", true);
  }
  const outlet = [[416, 566], [456, 566], [473, 585], [473, 624]];
  line(ctx, outlet, "#415B57", 20);
  line(ctx, outlet, "#BBC5AB", 11);
}

function thumbnail(ctx) {
  box(ctx, 0, 0, 540, 124, "#323D4E");
  ctx.save();
  ctx.translate(0, 120);
  pond(ctx);
  ctx.restore();
}

function cropGuides(ctx) {
  thumbnail(ctx);
  box(ctx, 0, 0, 540, 120, "#10161CB0");
  box(ctx, 0, 840, 540, 120, "#10161CB0");
  box(ctx, 0, 120, 540, 90, "#10161C60");
  box(ctx, 0, 750, 540, 90, "#10161C60");
  for (const [y0, y1, dash] of [[120, 840, []], [210, 750, [9, 7]]]) {
    ctx.beginPath();
    ctx.rect(4, y0, 532, y1 - y0);
    ctx.setLineDash(dash);
    ctx.lineWidth = 3;
    ctx.strokeStyle = "#FFD44D";
    ctx.stroke();
    ctx.setLineDash([]);
  }
}

for (const [id, draw] of Object.entries({ market, thumbnail, crop: cropGuides })) {
  const canvas = document.getElementById(id);
  const ctx = canvas.getContext("2d");
  ctx.scale(2, 2);
  ctx.lineJoin = "round";
  ctx.lineCap = "round";
  draw(ctx);
}
