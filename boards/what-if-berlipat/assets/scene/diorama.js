// What If Berlipat — reusable low-poly scene kit for board studies and the motion preview.
// Units are metres. Everything is a pure function of its inputs: no clocks, no unseeded randomness.
import * as THREE from "../vendor/three.module.js";
import { LAND_W, LAND_H, LAND_HEX } from "./landmask.js";

export { THREE };

// One world = one hue in five values. The hero object brings the only other colour.
export const RAMPS = {
  cobalt: { backdrop: "#2F50E8", mid: "#2440C4", dark: "#1A2F99", deep: "#111F6B", light: "#9DAEFF" },
  plum: { backdrop: "#6A35C9", mid: "#5527A8", dark: "#401C82", deep: "#2A1159", light: "#C3A6F7" },
  pine: { backdrop: "#0E7C6B", mid: "#0B6557", dark: "#084D43", deep: "#05332D", light: "#86D8C6" },
};
export const HERO = { rice: "#FFFDF4", tennis: "#D9F23C", dice: "#F4493B" };
export const PAPER = "#FFFDF4";

export function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const clamp01 = (v) => Math.min(1, Math.max(0, v));
export const ease = {
  outCubic: (p) => 1 - Math.pow(1 - clamp01(p), 3),
  outExpo: (p) => (p >= 1 ? 1 : 1 - Math.pow(2, -10 * clamp01(p))),
  inCubic: (p) => Math.pow(clamp01(p), 3),
  outBack: (p) => {
    const c = 1.70158;
    const q = clamp01(p) - 1;
    return 1 + (c + 1) * q * q * q + c * q * q;
  },
};

export function flat(color) {
  return new THREE.MeshLambertMaterial({ color, flatShading: true });
}

function box(w, h, d, material, x = 0, y = 0, z = 0) {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
  mesh.position.set(x, y, z);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  return mesh;
}

// ---------------------------------------------------------------------------
// Stage: seamless backdrop, one key light, tinted fill, hard-edged contact shadow.
// ---------------------------------------------------------------------------
export function createStage(canvas, { ramp, width = 1080, height = 1920 } = {}) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(width, height, false);
  renderer.toneMapping = THREE.NoToneMapping;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFShadowMap;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(ramp.backdrop);

  const fill = new THREE.AmbientLight(new THREE.Color("#ffffff").lerp(new THREE.Color(ramp.light), 0.35), 2.05);
  const key = new THREE.DirectionalLight(0xffffff, 1.75);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  key.shadow.bias = -0.0004;
  key.shadow.normalBias = 0.02;
  scene.add(fill, key, key.target);

  const catcher = new THREE.Mesh(
    new THREE.PlaneGeometry(1, 1),
    new THREE.ShadowMaterial({ color: ramp.deep, opacity: 0.5 }),
  );
  catcher.rotation.x = -Math.PI / 2;
  catcher.receiveShadow = true;
  scene.add(catcher);

  const camera = new THREE.PerspectiveCamera(26, width / height, 0.01, 1000);

  // Frame a target. `screenY` is where the target sits vertically (0 top, 1 bottom) so the
  // flat backdrop above it stays free for type. `extent` is the scene half-size for shadows.
  // `light` is the key light's offset from the target in extents.
  function frame({ target = [0, 0, 0], distance, pitch = 32, yaw = 38, fov = 26, screenY = 0.66, extent, groundY = 0, light = [-1.6, 3.2, 1.9] }) {
    const t = new THREE.Vector3(...target);
    const p = THREE.MathUtils.degToRad(pitch);
    const y = THREE.MathUtils.degToRad(yaw);
    camera.fov = fov;
    camera.near = Math.max(0.005, distance / 200);
    camera.far = distance * 40 + extent * 40;
    camera.position.set(
      t.x + distance * Math.cos(p) * Math.sin(y),
      t.y + distance * Math.sin(p),
      t.z + distance * Math.cos(p) * Math.cos(y),
    );
    camera.lookAt(t);
    camera.setViewOffset(width, height, 0, -(screenY - 0.5) * height, width, height);
    camera.updateProjectionMatrix();
    camera.updateMatrixWorld();

    key.target.position.copy(t);
    key.position.set(t.x + extent * light[0], t.y + extent * light[1], t.z + extent * light[2]);
    const s = key.shadow.camera;
    s.left = s.bottom = -extent * 1.6;
    s.right = s.top = extent * 1.6;
    s.near = extent * 0.2;
    s.far = extent * 9;
    s.updateProjectionMatrix();
    key.shadow.bias = -0.0004;
    key.shadow.normalBias = extent * 0.004;
    catcher.scale.setScalar(extent * 80);
    catcher.position.set(t.x, groundY, t.z);
  }

  // Project a world point to frame pixels, for anchoring DOM labels.
  function project(point) {
    const v = new THREE.Vector3(...point).project(camera);
    return { x: (v.x * 0.5 + 0.5) * width, y: (-v.y * 0.5 + 0.5) * height };
  }

  return { renderer, scene, camera, key, fill, catcher, frame, project, render: () => renderer.render(scene, camera) };
}

// ---------------------------------------------------------------------------
// Table scale: a plate on a table, and a rice pile that doubles grain by grain.
// ---------------------------------------------------------------------------
export function buildTable(ramp, { surface = ramp.dark } = {}) {
  const group = new THREE.Group();
  const top = 0.75;
  group.add(box(1.4, 0.05, 0.9, flat(surface), 0, top - 0.025, 0));
  for (const [x, z] of [[-0.62, -0.38], [0.62, -0.38], [-0.62, 0.38], [0.62, 0.38]]) {
    group.add(box(0.06, top - 0.05, 0.06, flat(ramp.deep), x, (top - 0.05) / 2, z));
  }
  const profile = [
    [0.0, 0.0], [0.072, 0.0], [0.118, 0.014], [0.124, 0.014], [0.121, 0.019], [0.07, 0.005], [0.0, 0.005],
  ].map(([x, y]) => new THREE.Vector2(x, y));
  const plate = new THREE.Mesh(new THREE.LatheGeometry(profile, 16), flat(ramp.backdrop));
  plate.material.side = THREE.DoubleSide;
  plate.position.y = top;
  plate.castShadow = true;
  plate.receiveShadow = true;
  group.add(plate);
  group.userData.surfaceY = top + 0.005;
  return group;
}

export const GRAIN = { length: 0.0066, width: 0.0021 };

// Deposit `count` grains one by one onto a height field so earlier grains never move.
// Grain i (i > 0) is born on day floor(log2(i)) + 2 out of grain i - 2^(day - 2).
export function simulateRicePile(count, seed = 7) {
  const rnd = mulberry32(seed);
  const G = 120;
  const R = 0.085;
  const heights = new Float32Array(G * G);
  const cell = (2 * R) / G;
  const pos = new Float32Array(count * 3);
  const rot = new Float32Array(count * 3);
  const day = new Uint8Array(count);
  const parent = new Int32Array(count);
  const gauss = () => Math.sqrt(-2 * Math.log(1 - rnd())) * Math.cos(2 * Math.PI * rnd());
  for (let i = 0; i < count; i++) {
    const sigma = 0.0026 * Math.cbrt(i + 1);
    let x = i === 0 ? 0 : gauss() * sigma;
    let z = i === 0 ? 0 : gauss() * sigma;
    x = Math.max(-R * 0.95, Math.min(R * 0.95, x));
    z = Math.max(-R * 0.95, Math.min(R * 0.95, z));
    const gx = Math.floor((x + R) / cell);
    const gz = Math.floor((z + R) / cell);
    pos[i * 3] = x;
    pos[i * 3 + 1] = heights[gz * G + gx] + GRAIN.width * 0.5;
    pos[i * 3 + 2] = z;
    rot[i * 3] = i === 0 ? 0.5 : rnd() * Math.PI * 2;
    rot[i * 3 + 1] = i === 0 ? 0 : (rnd() - 0.5) * 0.7;
    rot[i * 3 + 2] = rnd() * Math.PI * 2;
    const reach = 3;
    for (let dz = -reach; dz <= reach; dz++) {
      for (let dx = -reach; dx <= reach; dx++) {
        const cx = gx + dx;
        const cz = gz + dz;
        if (cx < 0 || cz < 0 || cx >= G || cz >= G) continue;
        const fall = Math.max(0, 1 - Math.hypot(dx, dz) / (reach + 0.5));
        heights[cz * G + cx] += 0.00042 * fall;
      }
    }
    day[i] = i === 0 ? 1 : Math.floor(Math.log2(i)) + 2;
    parent[i] = i === 0 ? 0 : i - Math.pow(2, day[i] - 2);
  }
  return { count, pos, rot, day, parent };
}

export function buildRice(pile, color = HERO.rice) {
  const geometry = new THREE.IcosahedronGeometry(1, 0);
  geometry.scale(GRAIN.length / 2, GRAIN.width / 2, GRAIN.width / 2);
  const mesh = new THREE.InstancedMesh(geometry, flat(color), pile.count);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.frustumCulled = false;
  const dummy = new THREE.Object3D();
  // `tickTime[d]` is when day d starts; a grain travels from its parent in `hop` seconds.
  mesh.userData.update = (time, tickTime, hop = 0.26) => {
    for (let i = 0; i < pile.count; i++) {
      const born = tickTime[pile.day[i]];
      const p = i === 0 ? 1 : born === undefined ? 0 : clamp01((time - born) / hop);
      if (p <= 0) {
        dummy.scale.setScalar(0);
        dummy.position.set(0, -1, 0);
      } else {
        const e = ease.outCubic(p);
        const a = pile.parent[i] * 3;
        const b = i * 3;
        dummy.position.set(
          pile.pos[a] + (pile.pos[b] - pile.pos[a]) * e,
          pile.pos[a + 1] + (pile.pos[b + 1] - pile.pos[a + 1]) * e + Math.sin(Math.PI * p) * 0.006,
          pile.pos[a + 2] + (pile.pos[b + 2] - pile.pos[a + 2]) * e,
        );
        dummy.rotation.set(pile.rot[b + 2] * 0.15 * (1 - e), pile.rot[b], pile.rot[b + 1]);
        dummy.scale.setScalar(ease.outBack(p));
      }
      dummy.updateMatrix();
      mesh.setMatrixAt(i, dummy.matrix);
    }
    mesh.instanceMatrix.needsUpdate = true;
  };
  return mesh;
}

// A faceted cone that stands in for a pile once single items are too small to draw.
// Radius follows the real bulk volume at a 32 degree angle of repose.
export function buildPile(color, segments = 11) {
  const geometry = new THREE.ConeGeometry(1, 1, segments, 2);
  const rnd = mulberry32(31);
  const jitter = Array.from({ length: segments * 2 }, () => 1 + (rnd() - 0.5) * 0.16);
  const p = geometry.attributes.position;
  for (let i = 0; i < p.count; i++) {
    if (p.getY(i) > 0.45) continue;
    // Keyed by position, so the duplicated seam vertices move together.
    const turn = Math.round((Math.atan2(p.getZ(i), p.getX(i)) / (2 * Math.PI)) * segments + segments) % segments;
    const k = jitter[turn + (p.getY(i) > -0.25 ? segments : 0)];
    p.setX(i, p.getX(i) * k);
    p.setZ(i, p.getZ(i) * k);
  }
  geometry.translate(0, 0.5, 0);
  const mesh = new THREE.Mesh(geometry, flat(color));
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.userData.setVolume = (volume) => {
    const r = Math.cbrt(volume / 0.654);
    mesh.scale.set(r, r * 0.625, r);
    mesh.visible = volume > 0;
  };
  return mesh;
}

// ---------------------------------------------------------------------------
// Room and house scale: walls with openings, a hero mass that fills and spills.
// ---------------------------------------------------------------------------
function wallWithOpening(group, material, { axis, plane, from, to, height, thickness, opening }) {
  // axis "x": wall lies in the plane x = plane and runs along z; axis "z": the reverse.
  const add = (a0, a1, y0, y1) => {
    if (a1 - a0 <= 0.001 || y1 - y0 <= 0.001) return;
    const len = a1 - a0;
    const mid = (a0 + a1) / 2;
    const mesh = axis === "x"
      ? box(thickness, y1 - y0, len, material, plane, (y0 + y1) / 2, mid)
      : box(len, y1 - y0, thickness, material, mid, (y0 + y1) / 2, plane);
    group.add(mesh);
  };
  if (!opening) return add(from, to, 0, height);
  const o0 = opening.center - opening.width / 2;
  const o1 = opening.center + opening.width / 2;
  add(from, o0, 0, height);
  add(o1, to, 0, height);
  add(o0, o1, 0, opening.sill);
  add(o0, o1, opening.top, height);
}

function spillCone(color, segments = 10) {
  const geometry = new THREE.ConeGeometry(1, 1, segments, 1);
  geometry.translate(0, 0.5, 0);
  const mesh = new THREE.Mesh(geometry, flat(color));
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.userData.set = (height) => {
    mesh.visible = height > 0.01;
    mesh.scale.set(Math.max(0.001, height * 1.6), Math.max(0.001, height), Math.max(0.001, height * 1.6));
  };
  return mesh;
}

// Faceted top surface of a mass inside a box footprint, with a skirt down to the floor.
function buildMassSurface(color, w, d, cells = 14, seed = 11) {
  const rnd = mulberry32(seed);
  const n = cells + 1;
  const noise = new Float32Array(n * n);
  for (let i = 0; i < noise.length; i++) noise[i] = rnd() - 0.5;
  const tris = cells * cells * 2 + cells * 4 * 2;
  const geometry = new THREE.BufferGeometry();
  const position = new Float32Array(tris * 9);
  geometry.setAttribute("position", new THREE.BufferAttribute(position, 3));
  const mesh = new THREE.Mesh(geometry, flat(color));
  mesh.material.side = THREE.DoubleSide;
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.frustumCulled = false;
  // level: fill height; brim: wall height; heap: extra dome once the level passes the brim.
  mesh.userData.set = (level, brim, bump = 0.07) => {
    const flatLevel = Math.min(level, brim);
    const over = Math.max(0, level - brim);
    const hAt = (i, j) => {
      const u = i / cells;
      const v = j / cells;
      const dome = 16 * u * (1 - u) * v * (1 - v);
      const edge = Math.min(1, dome * 3);
      return Math.max(0, flatLevel + over * 3 * dome + noise[j * n + i] * bump * edge * Math.min(1, level * 4));
    };
    const xAt = (i) => -w / 2 + (w * i) / cells;
    const zAt = (j) => -d / 2 + (d * j) / cells;
    let o = 0;
    const put = (x, y, z) => {
      position[o++] = x;
      position[o++] = y;
      position[o++] = z;
    };
    for (let j = 0; j < cells; j++) {
      for (let i = 0; i < cells; i++) {
        put(xAt(i), hAt(i, j), zAt(j));
        put(xAt(i), hAt(i, j + 1), zAt(j + 1));
        put(xAt(i + 1), hAt(i + 1, j), zAt(j));
        put(xAt(i + 1), hAt(i + 1, j), zAt(j));
        put(xAt(i), hAt(i, j + 1), zAt(j + 1));
        put(xAt(i + 1), hAt(i + 1, j + 1), zAt(j + 1));
      }
    }
    const skirt = (x0, z0, h0, x1, z1, h1) => {
      put(x0, 0, z0); put(x0, h0, z0); put(x1, 0, z1);
      put(x1, 0, z1); put(x0, h0, z0); put(x1, h1, z1);
    };
    for (let i = 0; i < cells; i++) {
      skirt(xAt(i), zAt(0), hAt(i, 0), xAt(i + 1), zAt(0), hAt(i + 1, 0));
      skirt(xAt(i), zAt(cells), hAt(i, cells), xAt(i + 1), zAt(cells), hAt(i + 1, cells));
      skirt(xAt(0), zAt(i), hAt(0, i), xAt(0), zAt(i + 1), hAt(0, i + 1));
      skirt(xAt(cells), zAt(i), hAt(cells, i), xAt(cells), zAt(i + 1), hAt(cells, i + 1));
    }
    geometry.attributes.position.needsUpdate = true;
    geometry.computeVertexNormals();
  };
  return mesh;
}

// An open-top room. Camera sits on the +x/+z side, so the door and window face it.
export function buildRoom(ramp, hero, { size = 4, height = 2.5, thickness = 0.15 } = {}) {
  const group = new THREE.Group();
  const half = size / 2;
  const outer = half + thickness / 2;
  const wall = flat(ramp.mid);
  group.add(box(size + thickness * 2, 0.08, size + thickness * 2, flat(ramp.dark), 0, 0.04, 0));
  const span = { from: -half - thickness, to: half + thickness, height, thickness };
  const door = { center: 0.55, width: 0.95, sill: 0, top: 2.0 };
  const window_ = { center: -0.35, width: 1.3, sill: 0.9, top: 2.0 };
  wallWithOpening(group, wall, { axis: "x", plane: -outer, ...span });
  wallWithOpening(group, wall, { axis: "z", plane: -outer, ...span });
  wallWithOpening(group, wall, { axis: "x", plane: outer, ...span, opening: door });
  wallWithOpening(group, wall, { axis: "z", plane: outer, ...span, opening: window_ });

  const mass = buildMassSurface(hero, size, size);
  const doorSpill = spillCone(hero);
  doorSpill.position.set(outer + thickness / 2, 0, door.center);
  const windowSpill = spillCone(hero);
  windowSpill.position.set(window_.center, 0, outer + thickness / 2);
  group.add(mass, doorSpill, windowSpill);

  group.userData.setLevel = (level) => {
    mass.userData.set(level, height);
    mass.visible = level > 0.005;
    doorSpill.userData.set(Math.min(level, door.top) * 0.85);
    windowSpill.userData.set(Math.min(Math.max(0, (level - window_.sill) * 1.3), window_.top * 0.8));
  };
  group.userData.setLevel(0);
  return group;
}

// A two-storey house whose roof has been pushed off by the mass inside.
export function buildHouse(ramp, hero, seed = 5) {
  const group = new THREE.Group();
  const w = 9;
  const d = 7;
  const h = 5.4;
  const t = 0.25;
  const wall = flat(ramp.mid);
  const xo = w / 2 + t / 2;
  const zo = d / 2 + t / 2;
  const span = (from, to) => ({ from, to, height: h, thickness: t });
  wallWithOpening(group, wall, { axis: "x", plane: -xo, ...span(-zo - t / 2, zo + t / 2) });
  wallWithOpening(group, wall, { axis: "z", plane: -zo, ...span(-xo - t / 2, xo + t / 2) });
  // Near walls: split each into bays so every bay carries one opening.
  const bays = [
    { axis: "x", plane: xo, from: -zo - t / 2, to: 0, opening: { center: -1.9, width: 1.2, sill: 0, top: 2.2 } },
    { axis: "x", plane: xo, from: 0, to: zo + t / 2, opening: { center: 1.8, width: 1.5, sill: 3.2, top: 4.5 } },
    { axis: "z", plane: zo, from: -xo - t / 2, to: 0, opening: { center: -2.3, width: 1.6, sill: 0.9, top: 2.2 } },
    { axis: "z", plane: zo, from: 0, to: xo + t / 2, opening: { center: 2.3, width: 1.6, sill: 3.2, top: 4.5 } },
  ];
  for (const bay of bays) wallWithOpening(group, wall, { ...bay, height: h, thickness: t });

  const mass = buildMassSurface(hero, w, d, 12, seed);
  mass.userData.set(h + 0.55, h, 0.3);
  group.add(mass);
  const spills = [
    [xo + t / 2, -1.9, 2.0], [xo + t / 2, 1.8, 3.4], [-2.3, zo + t / 2, 1.9, true], [2.3, zo + t / 2, 3.3, true],
  ];
  for (const [a, b, height, alongZ] of spills) {
    const cone = spillCone(hero, 11);
    cone.position.set(alongZ ? a : a, 0, alongZ ? b : b);
    cone.userData.set(height);
    group.add(cone);
  }

  // Gable roof, lifted and tipped by the pressure.
  const roof = new THREE.Group();
  const shape = new THREE.Shape();
  shape.moveTo(-d / 2 - 0.5, 0);
  shape.lineTo(d / 2 + 0.5, 0);
  shape.lineTo(0, 2.6);
  shape.closePath();
  const prism = new THREE.Mesh(new THREE.ExtrudeGeometry(shape, { depth: w + 1, bevelEnabled: false }), flat(ramp.dark));
  prism.rotation.y = Math.PI / 2;
  prism.position.x = -(w + 1) / 2;
  prism.castShadow = true;
  roof.add(prism);
  roof.add(box(0.8, 1.6, 0.8, flat(ramp.deep), -2.4, 1.6, -1.2));
  roof.position.set(0.5, h + 1.15, 0.3);
  roof.rotation.set(0.1, 0.12, -0.2);
  group.add(roof);

  // Real-size balls around the foot of the spills: at this scale they are dots.
  const rnd = mulberry32(seed + 1);
  const count = 2600;
  const balls = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(0.0335, 0), flat(hero), count);
  const m = new THREE.Matrix4();
  for (let i = 0; i < count; i++) {
    const spill = spills[i % spills.length];
    const angle = rnd() * Math.PI * 2;
    const radius = spill[2] * 1.6 * (0.85 + Math.pow(rnd(), 2) * 0.9);
    const x = spill[0] + Math.cos(angle) * radius;
    const z = spill[1] + Math.sin(angle) * radius;
    const inside = Math.abs(x) < w / 2 + t && Math.abs(z) < d / 2 + t;
    m.makeTranslation(inside ? 0 : x, inside ? -5 : 0.0335, inside ? 0 : z);
    balls.setMatrixAt(i, m);
  }
  balls.castShadow = false;
  group.add(balls);
  return group;
}

// ---------------------------------------------------------------------------
// Landmark scale: a faceless low-poly Statue of Liberty at its real 93 m, and a block of cubes.
// ---------------------------------------------------------------------------
export function buildLiberty(ramp) {
  const group = new THREE.Group();
  const add = (geometry, color, x, y, z, rx = 0, ry = 0, rz = 0) => {
    const mesh = new THREE.Mesh(geometry, flat(color));
    mesh.position.set(x, y, z);
    mesh.rotation.set(rx, ry, rz);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    group.add(mesh);
    return mesh;
  };
  // Fort Wood: an eleven-point star, about 20 m to the terrace.
  const star = new THREE.Shape();
  for (let i = 0; i < 22; i++) {
    const r = i % 2 === 0 ? 46 : 31;
    const a = (i / 22) * Math.PI * 2;
    if (i === 0) star.moveTo(Math.cos(a) * r, Math.sin(a) * r);
    else star.lineTo(Math.cos(a) * r, Math.sin(a) * r);
  }
  star.closePath();
  add(new THREE.ExtrudeGeometry(star, { depth: 9, bevelEnabled: false }), ramp.dark, 0, 9, 0, Math.PI / 2);
  add(new THREE.BoxGeometry(40, 11, 40), ramp.dark, 0, 14.5, 0);
  // Pedestal to 47 m.
  add(new THREE.CylinderGeometry(9.5, 13, 20, 4), ramp.mid, 0, 30, 0, 0, Math.PI / 4);
  add(new THREE.BoxGeometry(17, 2.2, 17), ramp.mid, 0, 41, 0);
  add(new THREE.CylinderGeometry(7.5, 8.5, 5, 4), ramp.mid, 0, 44.5, 0, 0, Math.PI / 4);
  // Figure: robe, shoulders, head, crown, raised arm and torch, tablet. Heel to torch = 46 m.
  add(new THREE.CylinderGeometry(3.3, 6.2, 27, 7), ramp.light, 0, 60.5, 0);
  add(new THREE.CylinderGeometry(2.4, 4.2, 5, 7), ramp.light, 0, 75.5, 0);
  add(new THREE.IcosahedronGeometry(2.3, 0), ramp.light, 0, 80.2, 0);
  for (let i = 0; i < 7; i++) {
    const a = THREE.MathUtils.degToRad(-66 + i * 22);
    add(new THREE.ConeGeometry(0.42, 3.4, 4), ramp.light, Math.sin(a) * 3.3, 81.6 + Math.cos(a) * 3.3, 0.3, 0, 0, -a);
  }
  add(new THREE.CylinderGeometry(1.0, 1.35, 13, 5), ramp.light, 4.6, 82.5, 0, 0, 0, -0.24);
  add(new THREE.CylinderGeometry(1.5, 0.9, 1.6, 6), ramp.light, 6.1, 89.3, 0);
  add(new THREE.ConeGeometry(1.25, 3.2, 5), ramp.light, 6.1, 91.4, 0);
  add(new THREE.BoxGeometry(1.2, 6.5, 4.2), ramp.light, -4.6, 68.5, 2.2, 0.2, 0, 0.18);
  return group;
}

// A cube of side `side` assembled from n^3 blocks, with a bitten corner and a few fallen blocks.
export function buildBlockCube(color, side, n = 8, seed = 3) {
  const rnd = mulberry32(seed);
  const s = side / n;
  const cells = [];
  for (let x = 0; x < n; x++) {
    for (let y = 0; y < n; y++) {
      for (let z = 0; z < n; z++) {
        const surface = x === 0 || y === 0 || z === 0 || x === n - 1 || y === n - 1 || z === n - 1;
        if (!surface) continue;
        const corner = (n - 1 - x) + (n - 1 - y) + (n - 1 - z);
        if (corner < 2 || (corner === 2 && rnd() < 0.6) || (corner === 3 && rnd() < 0.2)) continue;
        cells.push([(x + 0.5) * s - side / 2, (y + 0.5) * s, (z + 0.5) * s - side / 2, 0]);
      }
    }
  }
  const fallen = [[0.62, 0.52, 0.5], [0.72, 0.2, 1.1], [0.36, 0.7, 0.3], [0.2, 0.78, 2.0]];
  for (const [fx, fz, turn] of fallen) cells.push([fx * side, s / 2, fz * side, turn]);
  const mesh = new THREE.InstancedMesh(new THREE.BoxGeometry(s, s, s), flat(color), cells.length);
  const dummy = new THREE.Object3D();
  cells.forEach(([x, y, z, turn], i) => {
    dummy.position.set(x, y, z);
    dummy.rotation.set(0, turn, 0);
    dummy.updateMatrix();
    mesh.setMatrixAt(i, dummy.matrix);
  });
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.frustumCulled = false;
  return mesh;
}

// ---------------------------------------------------------------------------
// Planet scale: a faceted globe whose faces flip to the hero colour as coverage spreads.
// ---------------------------------------------------------------------------
function isLand(lat, lon) {
  const col = Math.min(LAND_W - 1, Math.max(0, Math.floor((lon + 180) / 2)));
  const row = Math.min(LAND_H - 1, Math.max(0, Math.floor((90 - lat) / 2)));
  const index = row * LAND_W + col;
  return (parseInt(LAND_HEX[index >> 2], 16) >> (3 - (index & 3))) & 1;
}

// `origin` is where the pile started; `coverage` (0..1) is the covered share of the surface.
export function buildGlobe(ramp, hero, { radius = 1, detail = 14, origin = [35, -100], coverage = 0, seed = 9 } = {}) {
  const geometry = new THREE.IcosahedronGeometry(radius, detail);
  const position = geometry.attributes.position;
  const faces = position.count / 3;
  const color = new Float32Array(position.count * 3);
  geometry.setAttribute("color", new THREE.BufferAttribute(color, 3));
  const base = position.array.slice();
  const rnd = mulberry32(seed);
  const jitter = new Float32Array(faces);
  for (let i = 0; i < faces; i++) jitter[i] = rnd();
  const o = new THREE.Vector3().setFromSphericalCoords(
    1, THREE.MathUtils.degToRad(90 - origin[0]), THREE.MathUtils.degToRad(origin[1]),
  );
  const land = new THREE.Color(ramp.light);
  const sea = new THREE.Color(ramp.dark);
  const heroColor = new THREE.Color(hero);
  const heroSea = new THREE.Color(hero).lerp(new THREE.Color(ramp.backdrop), 0.3);
  const c = new THREE.Vector3();
  const mesh = new THREE.Mesh(geometry, new THREE.MeshLambertMaterial({ vertexColors: true, flatShading: true }));
  mesh.castShadow = true;
  mesh.userData.setCoverage = (share) => {
    // A spherical cap of angular radius a covers (1 - cos a) / 2 of the sphere.
    const cap = Math.acos(1 - 2 * clamp01(share));
    for (let f = 0; f < faces; f++) {
      const i = f * 9;
      c.set(
        base[i] + base[i + 3] + base[i + 6],
        base[i + 1] + base[i + 4] + base[i + 7],
        base[i + 2] + base[i + 5] + base[i + 8],
      ).normalize();
      const lat = 90 - THREE.MathUtils.radToDeg(Math.acos(c.y));
      const lon = THREE.MathUtils.radToDeg(Math.atan2(c.x, c.z));
      const covered = share >= 1 || c.angleTo(o) + (jitter[f] - 0.5) * 0.12 < cap;
      const onLand = isLand(lat, lon);
      // Covered land keeps the full hero colour and covered sea a shade of it, so Earth stays readable.
      const tint = covered ? (onLand ? heroColor : heroSea) : onLand ? land : sea;
      const lift = covered ? 1.012 : 1;
      for (let v = 0; v < 3; v++) {
        const k = i + v * 3;
        position.array[k] = base[k] * lift;
        position.array[k + 1] = base[k + 1] * lift;
        position.array[k + 2] = base[k + 2] * lift;
        color[k] = tint.r;
        color[k + 1] = tint.g;
        color[k + 2] = tint.b;
      }
    }
    position.needsUpdate = true;
    geometry.attributes.color.needsUpdate = true;
  };
  mesh.userData.setCoverage(coverage);
  return mesh;
}
