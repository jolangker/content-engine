// Generated from ../assets/studies.js and ../assets/studies-r6.js (helpers only). Rebuild with build_draw.py.
"use strict";

const theme = getComputedStyle(document.documentElement);
const color = (name) => theme.getPropertyValue("--" + name).trim();

function polygon(ctx, points, fill, stroke, width = 1) {
  ctx.beginPath();
  points.forEach(([x, y], index) => index ? ctx.lineTo(x, y) : ctx.moveTo(x, y));
  ctx.closePath();
  if (fill) {
    ctx.fillStyle = fill;
    ctx.fill();
  }
  if (stroke) {
    ctx.strokeStyle = stroke;
    ctx.lineWidth = width;
    ctx.stroke();
  }
}

function line(ctx, points, stroke, width = 1, dashes = []) {
  ctx.beginPath();
  points.forEach(([x, y], index) => index ? ctx.lineTo(x, y) : ctx.moveTo(x, y));
  ctx.strokeStyle = stroke;
  ctx.lineWidth = width;
  ctx.setLineDash(dashes);
  ctx.stroke();
  ctx.setLineDash([]);
}

function oval(ctx, x, y, rx, ry, fill, stroke, width = 1, rotation = 0) {
  ctx.beginPath();
  ctx.ellipse(x, y, rx, ry, rotation, 0, Math.PI * 2);
  if (fill) {
    ctx.fillStyle = fill;
    ctx.fill();
  }
  if (stroke) {
    ctx.lineWidth = width;
    ctx.strokeStyle = stroke;
    ctx.stroke();
  }
}

function box(ctx, x, y, width, height, fill) {
  ctx.fillStyle = fill;
  ctx.fillRect(x, y, width, height);
}

function glint(ctx, x, y, width, tint = "#F6F5D899") {
  ctx.beginPath();
  ctx.moveTo(x, y + 2);
  ctx.quadraticCurveTo(x + width * .45, y - 3, x + width, y + 1);
  ctx.strokeStyle = tint;
  ctx.lineWidth = 1.7;
  ctx.stroke();
}

function seededRandom(seed) {
  return () => {
    seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
    return seed / 4294967296;
  };
}

function cloud(ctx, x, y, scale, fill) {
  oval(ctx, x, y, 32 * scale, 8 * scale, fill);
  oval(ctx, x - 15 * scale, y - 2 * scale, 12 * scale, 9 * scale, fill);
  oval(ctx, x + 2 * scale, y - 7 * scale, 19 * scale, 11 * scale, fill);
  oval(ctx, x + 22 * scale, y - 3 * scale, 13 * scale, 8 * scale, fill);
}

function terrain(ctx, seam, { top, horizon, sun, earth, ridge, seed }) {
  const sky = ctx.createLinearGradient(0, 0, 0, seam);
  sky.addColorStop(0, top);
  sky.addColorStop(1, horizon);
  box(ctx, 0, 0, 540, seam, sky);
  oval(ctx, sun[0], sun[1], sun[2], sun[2], "#F8DA8766");
  oval(ctx, sun[0], sun[1], sun[2] * .73, sun[2] * .73, "#FFF2B9");
  cloud(ctx, 92, seam - 198, .95, "#FFF8E5AA");
  cloud(ctx, 339, seam - 181, 1.25, "#FFF8E588");
  cloud(ctx, 482, seam - 230, .64, "#FFF8E584");
  polygon(ctx, [[0, seam - 84], [54, seam - 99], [132, seam - 109], [210, seam - 94], [274, seam - 86],
    [369, seam - 113], [445, seam - 92], [540, seam - 88], [540, seam], [0, seam]], color("hill"));
  polygon(ctx, [[0, seam - 57], [105, seam - 49], [173, seam - 81], [231, seam - 67], [330, seam - 53],
    [414, seam - 78], [540, seam - 65], [540, seam + 10], [0, seam + 10]], ridge);
  box(ctx, 0, seam, 540, 960 - seam, earth);
  polygon(ctx, [[0, seam + 50], [95, seam + 44], [150, seam + 76], [248, seam + 85], [320, seam + 51],
    [441, seam + 62], [540, seam + 44], [540, seam + 204], [437, seam + 198], [368, seam + 211],
    [290, seam + 183], [189, seam + 193], [88, seam + 172], [0, seam + 187]], "#BE795064");
  polygon(ctx, [[0, seam + 331], [60, seam + 315], [145, seam + 326], [237, seam + 294], [328, seam + 311],
    [432, seam + 294], [540, seam + 323], [540, 960], [0, 960]], color("deep-soil"));
  polygon(ctx, [[0, seam + 450], [87, seam + 426], [163, seam + 438], [238, seam + 404], [361, seam + 426],
    [443, seam + 405], [540, seam + 432], [540, 960], [0, 960]], "#60372880");
  box(ctx, 0, seam - 17, 540, 20, color("grass"));
  box(ctx, 0, seam + 3, 540, 6, "#537D43");

  const random = seededRandom(seed);
  for (let i = 0; i < 100; i++) {
    const x = random() * 540;
    const y = seam + 17 + random() * (943 - seam);
    const radius = random() * 3 + .6;
    oval(ctx, x, y, radius, radius * .52, i % 3 ? "#F3B47935" : "#4828143A", null, 1, random() - .5);
  }
  for (let i = 0; i < 35; i++) {
    const x = random() * 540;
    const y = seam - 5 - random() * 9;
    line(ctx, [[x - 2, y - 4], [x, y], [x + 3, y - 6]], "#487F4288", 1.2);
  }
}

function house(ctx, x, floor, scale, roof = color("roof")) {
  ctx.save();
  ctx.translate(x, floor);
  ctx.scale(scale, scale);
  box(ctx, 0, -105, 151, 105, "#F8E6AE");
  polygon(ctx, [[151, -105], [181, -120], [181, -7], [151, 0]], "#C9AB82");
  polygon(ctx, [[-15, -103], [54, -161], [129, -161], [169, -103]], roof);
  polygon(ctx, [[169, -103], [129, -161], [170, -157], [199, -115], [181, -105]], "#753E39");
  for (let y = -151; y < -105; y += 8) {
    line(ctx, [[54 - (y + 151) * 1.12, y], [134 + (y + 151) * .6, y]], "#F7C38855", 1.7);
  }
  box(ctx, 19, -77, 42, 33, "#59684A");
  box(ctx, 23, -73, 34, 25, "#CAD8C8");
  line(ctx, [[39, -72], [39, -47]], "#59684A", 2);
  box(ctx, 97, -73, 31, 73, "#8E644C");
  box(ctx, 100, -68, 25, 30, "#A07956");
  oval(ctx, 105, -33, 2, 2, "#F0BE6B");
  ctx.restore();
}

function banana(ctx, x, floor, scale) {
  ctx.save();
  ctx.translate(x, floor);
  ctx.scale(scale, scale);
  line(ctx, [[-4, 0], [1, -44], [-3, -88]], "#69794A", 10);
  const leaves = [
    [[-3, -79], [-33, -115], [-68, -115], [-53, -96], [-26, -89]],
    [[-2, -80], [24, -119], [62, -115], [46, -97], [23, -96]],
    [[0, -72], [40, -91], [75, -78], [52, -70], [30, -76]],
    [[-7, -73], [-35, -90], [-74, -70], [-53, -69], [-27, -78]],
    [[-4, -84], [-17, -113], [-10, -140], [4, -122], [5, -102]]
  ];
  leaves.forEach((points, index) => {
    polygon(ctx, points, ["#4E7951", "#5A8E5D", "#6F9A59", "#729C60", "#5A8E5D"][index]);
    line(ctx, [points[0], points[2]], "#365C4380", 1.5);
  });
  ctx.restore();
}

function person(ctx, x, floor) {
  oval(ctx, x, floor + 3, 22, 5, "#2546333A");
  line(ctx, [[x - 5, floor - 31], [x - 7, floor - 5], [x - 13, floor - 1]], "#333C30", 8);
  line(ctx, [[x + 6, floor - 31], [x + 10, floor - 4], [x + 17, floor - 1]], "#333C30", 8);
  polygon(ctx, [[x - 10, floor - 61], [x + 8, floor - 62], [x + 15, floor - 31], [x - 12, floor - 30]], "#C97E48");
  line(ctx, [[x + 9, floor - 56], [x + 25, floor - 40], [x + 34, floor - 46]], "#CF9467", 7);
  oval(ctx, x + 1, floor - 73, 9, 11, "#DEAC70");
  oval(ctx, x - 1, floor - 80, 10.5, 7, "#35594C");
  line(ctx, [[x - 9, floor - 79], [x + 15, floor - 79]], "#35594C", 3.5);
  oval(ctx, x + 6, floor - 74, 1.1, 1.1, "#47352C");
  polygon(ctx, [[x + 29, floor - 40], [x + 48, floor - 42], [x + 45, floor - 22], [x + 33, floor - 22]], "#779971");
  line(ctx, [[x + 32, floor - 41], [x + 37, floor - 48], [x + 45, floor - 44]], "#466B62", 1.8);
}

function fish(ctx, x, y, s, direction, fill, whiskers = false) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(direction * s, s);
  polygon(ctx, [[-14, 0], [-27, -9], [-25, 0], [-28, 8]], fill);
  oval(ctx, 0, 0, 17, 6, fill);
  polygon(ctx, [[-4, -4], [2, -11], [8, -3]], fill);
  oval(ctx, 10, -1.5, 1.3, 1.3, "#2A403A");
  if (whiskers) {
    line(ctx, [[14, 1], [22, 4], [26, 3]], fill, 1.5);
    line(ctx, [[14, 3], [20, 7], [24, 7]], fill, 1.2);
  }
  ctx.restore();
}

function pond(ctx) {
  terrain(ctx, 404, { top: color("storm"), horizon: "#ECC88E", sun: [441, 239, 41],
    earth: color("soil"), ridge: "#779765", seed: 13 });
  banana(ctx, 86, 393, 1.1);
  house(ctx, 362, 394, .8);
  person(ctx, 117, 406);

  const waterline = [[65, 446], [430, 446], [399, 606], [111, 606]];
  oval(ctx, 247, 445, 195, 38, "#A67A52");
  oval(ctx, 247, 446, 186, 31, "#326674", "#203E4B", 3);
  polygon(ctx, [[57, 448], [437, 448], [409, 619], [102, 619]], "#304D55", "#233B3C", 5);
  polygon(ctx, waterline, color("water"));
  oval(ctx, 247, 446, 175, 25, "#78C7C4");
  polygon(ctx, [[84, 514], [413, 514], [399, 606], [111, 606]], "#41929F80");
  line(ctx, [[67, 464], [424, 464]], "#B4E0D4", 3);
  for (const [x, y, width] of [[147, 445, 31], [214, 435, 42], [277, 451, 19], [335, 437, 33], [155, 533, 24]]) {
    glint(ctx, x, y, width);
  }
  fish(ctx, 175, 512, 1.11, 1, "#D9C49A", true);
  fish(ctx, 307, 539, 1.20, -1, "#E3D3AA", true);
  fish(ctx, 214, 572, .86, 1, "#C8C6A1", true);
  fish(ctx, 345, 582, .8, -1, "#ABC6A5", true);

  const outlet = [[416, 496], [456, 496], [473, 515], [473, 562]];
  line(ctx, outlet, "#415B57", 20);
  line(ctx, outlet, "#BBC5AB", 11);
  line(ctx, outlet, "#67BCBF", 4.5);
  line(ctx, [[473, 564], [473, 598]], "#B6EBDB", 4, [4, 6]);
  polygon(ctx, [[433, 601], [456, 618], [484, 615], [518, 599], [536, 607], [516, 635], [446, 638]], "#543B30");
  glint(ctx, 457, 614, 32, "#B7E6CF");
  glint(ctx, 477, 621, 28, "#75C2BE");

  const scrim = ctx.createLinearGradient(0, 0, 0, 384);
  scrim.addColorStop(0, "#202B38A0");
  scrim.addColorStop(1, "#202B3800");
  box(ctx, 0, 0, 540, 384, scrim);
}

function hatchery(ctx) {
  terrain(ctx, 342, { top: "#D4DBC0", horizon: color("sky"), sun: [466, 125, 27],
    earth: "#975436", ridge: "#72A187", seed: 39 });
  banana(ctx, 486, 331, .92);
  house(ctx, 367, 326, .49, "#8E694F");
  for (const x of [35, 304]) box(ctx, x, 226, 12, 118, "#745744");
  polygon(ctx, [[11, 230], [46, 187], [286, 187], [327, 219], [310, 230]], "#497664");
  line(ctx, [[13, 227], [314, 227]], "#C7D299", 3);
  for (let x = 52; x < 310; x += 31) line(ctx, [[x, 192], [x - 22, 226]], "#95AE7C", 2);
  polygon(ctx, [[41, 341], [320, 341], [373, 379], [65, 379]], "#31574325");
  box(ctx, 60, 340, 95, 21, "#865C45");
  box(ctx, 75, 361, 10, 37, "#704936");
  box(ctx, 137, 361, 9, 37, "#704936");
  polygon(ctx, [[83, 339], [82, 304], [122, 304], [140, 316], [140, 339]], "#4F8E82", "#2A544C", 3);
  oval(ctx, 109, 320, 7, 7, "#EBCC76");
  line(ctx, [[118, 312], [129, 318]], "#73B6A9", 2);

  polygon(ctx, [[46, 407], [491, 407], [459, 664], [85, 664]], color("liner"), "#284D56", 4);
  polygon(ctx, [[45, 405], [106, 378], [456, 378], [491, 405]], "#3D7E88", "#284D56", 3);
  polygon(ctx, [[63, 412], [474, 412], [444, 650], [101, 650]], color("water"));
  polygon(ctx, [[77, 531], [458, 531], [444, 650], [101, 650]], "#418E9D7E");
  line(ctx, [[68, 422], [471, 422]], "#AFE0D5", 3);

  const hose = [[136, 327], [179, 330], [188, 352], [188, 571], [200, 600], [231, 613]];
  line(ctx, hose, "#244842", 9);
  line(ctx, hose, "#A9C5A1", 3);
  oval(ctx, 243, 614, 30, 9, "#37645C");
  oval(ctx, 243, 610, 29, 6, "#A1BA96");
  for (const [x, y, r] of [[237, 600, 3], [257, 583, 4], [230, 565, 6], [245, 532, 7],
    [222, 503, 5], [268, 478, 8], [239, 452, 9], [260, 430, 4]]) {
    oval(ctx, x, y, r, r, "#DEF7DE45", "#D7F6DD", 1.6);
  }
  line(ctx, [[279, 568], [287, 530], [285, 492], [278, 464]], "#E3F8D9BF", 3, [3, 7]);
  line(ctx, [[272, 470], [278, 462], [286, 467]], "#E3F8D9BF", 3);
  for (const [x, y, s, facing] of [[329, 471, .5, 1], [375, 492, .6, -1], [341, 526, .54, 1], [401, 534, .42, -1],
    [387, 583, .55, 1], [332, 568, .48, -1], [130, 495, .44, 1], [132, 543, .38, -1]]) {
    fish(ctx, x, y, s, facing, "#F3D89F");
  }
}

function harvest(ctx) {
  terrain(ctx, 378, { top: "#D0D7AC", horizon: color("sky"), sun: [102, 141, 35],
    earth: "#A45D39", ridge: "#6F9B71", seed: 87 });
  house(ctx, 77, 371, .61, "#9A583E");
  banana(ctx, 456, 368, 1.33);
  banana(ctx, 516, 371, .68);

  polygon(ctx, [[32, 378], [520, 378], [522, 611], [503, 652], [290, 652],
    [264, 598], [53, 598], [25, 563]], "#C78D63", "#865239", 4);
  polygon(ctx, [[53, 591], [266, 591], [297, 645], [506, 645], [503, 652], [290, 652], [264, 598], [53, 598]], "#956044");
  oval(ctx, 156, 594, 101, 8, "#70422D45");
  oval(ctx, 404, 649, 82, 7, "#70422D45");

  const culture = [[52, 340], [251, 340], [230, 514], [72, 514]];
  polygon(ctx, [[31, 515], [274, 515], [252, 541], [46, 541]], "#C49B65", "#784B37", 2);
  box(ctx, 54, 541, 18, 54, "#774D37");
  box(ctx, 233, 541, 18, 54, "#774D37");
  polygon(ctx, culture, "#B46A4E", "#6C4536", 4);
  polygon(ctx, [[63, 360], [240, 360], [222, 495], [82, 495]], "#81BBA4", "#694C4A", 2);
  oval(ctx, 152, 340, 101, 17, "#D39269", "#87503F", 3);
  oval(ctx, 152, 342, 88, 11, "#9DD0B0");
  line(ctx, [[68, 365], [236, 365]], "#D2E5B7", 2.6);

  const random = seededRandom(102);
  for (let i = 0; i < 30; i++) {
    oval(ctx, 92 + 116 * random(), 382 + 91 * random(), 1.2 + random() * 2, 1.3, "#F2DF9D", null, 1, random() - .5);
  }
  const spout = [[237, 437], [276, 437], [287, 450], [287, 468]];
  line(ctx, spout, "#394B40", 17);
  line(ctx, spout, "#C5BE94", 11);
  line(ctx, [[287, 470], [298, 485], [319, 510]], "#B1DED0", 5.5);
  line(ctx, [[287, 472], [303, 495], [321, 514]], "#E0F6DA", 2.2, [4, 5]);

  polygon(ctx, [[309, 560], [497, 560], [477, 650], [331, 650]], "#D1A66E", "#6D513D", 4);
  polygon(ctx, [[321, 581], [484, 581], [471, 640], [336, 640]], color("water"));
  line(ctx, [[322, 585], [482, 585]], "#A8D7C5", 2.6);
  glint(ctx, 360, 594, 30);

  line(ctx, [[440, 519], [498, 495], [522, 495]], "#654A37", 13);
  line(ctx, [[441, 517], [500, 494], [522, 494]], "#CEAB6D", 6);
  polygon(ctx, [[303, 507], [454, 507], [429, 549], [328, 549]], "#EFE1AB", "#5D5F4A", 3);
  for (let x = 321; x < 451; x += 13) {
    const slope = (378 - x) * .32;
    line(ctx, [[x, 509], [x + slope, 547]], "#A99565", 1.4);
  }
  line(ctx, [[314, 523], [444, 523]], "#A99565", 1.4);
  line(ctx, [[322, 536], [436, 536]], "#A99565", 1.4);
  for (const [x, y] of [[330, 515], [335, 520], [345, 516], [351, 521], [357, 514], [365, 520], [340, 524], [357, 525], [373, 515]]) {
    oval(ctx, x, y, 3.5, 2.2, "#B76644", null, 1, -.42);
  }
  for (const x of [338, 358, 379]) line(ctx, [[x, 553], [x + 2, 580]], "#B8ECDD", 3, [4, 5]);
}

function motionPoses(ctx) {
  for (let index = 0; index < 3; index++) {
    ctx.save();
    ctx.translate(index * 219, 0);
    box(ctx, 0, 0, 210, 120, color("soil"));
    box(ctx, 0, 0, 210, 34, color("sky"));
    box(ctx, 0, 34, 210, 6, color("grass"));
    polygon(ctx, [[0, 100], [67, 94], [108, 96], [147, 90], [210, 98], [210, 120], [0, 120]], color("deep-soil"));
    polygon(ctx, [[19, 40], [110, 40], [100, 84], [31, 84]], color("liner"), "#274647", 2);
    polygon(ctx, [[25, index ? 52 : 45], [104, index ? 52 : 45], [96, 79], [35, 79]], color("water"));
    const route = [[104, 56], [129, 56], [146, 68], [146, 81]];
    line(ctx, route, "#CFBF95", 6);
    polygon(ctx, [[132, 86], [151, 95], [180, 92], [190, 83], [199, 87], [183, 102], [147, 104]], "#52392E");
    if (index === 0) glint(ctx, 42, 48, 37);
    if (index > 0) line(ctx, route, "#8DDFD4", 2.3, [3, 3]);
    if (index === 2) {
      line(ctx, [[146, 83], [146, 93]], "#B2F0DA", 2.4, [2, 3]);
      glint(ctx, 147, 96, 27, "#9DDFCE");
    }
    ctx.restore();
  }
}


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

