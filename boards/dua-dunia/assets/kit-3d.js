// Dua Dunia — Reusable Hybrid 3D Diorama Kit (Polyfork GLBs + Procedural Capsule Characters)
// Deterministic render-at-time(t) for both static board studies and HyperFrames motion previews.
import * as THREE from "./vendor/three.module.min.js";
import { GLTFLoader } from "./vendor/GLTFLoader.js";

export const TOKENS = {
  navyHud: "#1C3A4A",
  navyStroke: "#142A36",
  creamText: "#FFFDF5",
  accentYellow: "#FAD668",
  worldCleanGreen: "#78A55E",
  worldCompareAmber: "#E8A838",
  skyTop: "#3B88C3",
  skyLow: "#78AFD8",
  asphalt: "#56595B",
  sidewalk: "#B8BDC0",
  warmFacade: "#CAA584",
  capsuleOrange: "#E67E35",
  capsuleTeal: "#3A9D8F",
  capsulePlum: "#7A5BA8",
};

const MODEL_FILES = {
  bus: "city-bus-49fd97.glb",
  hatchback: "compact-hatchback-386417.glb",
  towncar: "town-car-56eeb6.glb",
  shopRow: "one-storey-shop-row-83c958.glb",
  tenement: "brick-tenement-7d2014.glb",
  tree: "street-tree-0d33f3.glb",
};

export async function loadPolyforkModels(baseUrl = "../assets/models") {
  const loader = new GLTFLoader();
  const entries = await Promise.all(
    Object.entries(MODEL_FILES).map(async ([key, filename]) => {
      const gltf = await loader.loadAsync(`${baseUrl}/${filename}`);
      const root = gltf.scene;
      root.traverse((obj) => {
        if (obj.isMesh) {
          obj.castShadow = true;
          obj.receiveShadow = true;
          if (obj.material) {
            const mats = Array.isArray(obj.material) ? obj.material : [obj.material];
            for (const m of mats) {
              if ("roughness" in m) m.roughness = Math.max(m.roughness ?? 0.8, 0.78);
              if ("metalness" in m) m.metalness = Math.min(m.metalness ?? 0.05, 0.08);
            }
          }
        }
      });
      return [key, root];
    })
  );
  return Object.fromEntries(entries);
}

export function createRenderer(canvas, width, height) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, preserveDrawingBuffer: true });
  renderer.setSize(width, height, false);
  renderer.setPixelRatio(1);
  // Polyfork lighting rule: never use ACESFilmicToneMapping at exposure 1 (darkens colours ~30%).
  renderer.toneMapping = THREE.NoToneMapping;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  return renderer;
}

export function createDaylightScene() {
  const scene = new THREE.Scene();
  // Clean daytime sky backdrop
  const skyCanvas = document.createElement("canvas");
  skyCanvas.width = 4;
  skyCanvas.height = 256;
  const sctx = skyCanvas.getContext("2d");
  const grad = sctx.createLinearGradient(0, 0, 0, 256);
  grad.addColorStop(0, TOKENS.skyTop);
  grad.addColorStop(0.65, TOKENS.skyLow);
  grad.addColorStop(1, "#B8D8EC");
  sctx.fillStyle = grad;
  sctx.fillRect(0, 0, 4, 256);
  const skyTex = new THREE.CanvasTexture(skyCanvas);
  skyTex.colorSpace = THREE.SRGBColorSpace;
  scene.background = skyTex;

  const hemi = new THREE.HemisphereLight(0xd9eeff, 0x7e7b74, 1.15);
  scene.add(hemi);

  const sun = new THREE.DirectionalLight(0xfff9ec, 1.55);
  sun.position.set(24, 38, 22);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  sun.shadow.camera.near = 2;
  sun.shadow.camera.far = 140;
  const d = 45;
  sun.shadow.camera.left = -d;
  sun.shadow.camera.right = d;
  sun.shadow.camera.top = d;
  sun.shadow.camera.bottom = -d;
  sun.shadow.bias = -0.0005;
  scene.add(sun);

  return scene;
}

// Procedural ~1.75m toy-capsule character with articulated limbs & head for natural animation
export function createCapsuleCitizen({
  shirtColor = TOKENS.capsuleOrange,
  pantsColor = "#2E3B4E",
  skinColor = "#C98F63",
  hairColor = "#232326",
  mood = "smile", // "smile" | "frown" | "neutral"
  sunglasses = false,
  tie = false,
} = {}) {
  const g = new THREE.Group();
  const mat = (color, roughness = 0.82) =>
    new THREE.MeshStandardMaterial({ color, roughness, metalness: 0.02 });

  // Articulated legs pivoted at the hip (y = 0.65) so feet stay planted at y = 0 when standing
  const legGeo = new THREE.CylinderGeometry(0.11, 0.1, 0.58, 12);
  const shoeGeo = new THREE.SphereGeometry(0.13, 12, 8);
  const legs = [];
  for (const sx of [-0.14, 0.14]) {
    const legPivot = new THREE.Group();
    legPivot.position.set(sx, 0.65, 0);
    const leg = new THREE.Mesh(legGeo, mat(pantsColor));
    leg.position.set(0, -0.29, 0);
    leg.castShadow = true;
    legPivot.add(leg);
    const shoe = new THREE.Mesh(shoeGeo, mat("#1F2428"));
    shoe.scale.set(0.95, 0.55, 1.35);
    shoe.position.set(0, -0.58, 0.04);
    shoe.castShadow = true;
    legPivot.add(shoe);
    g.add(legPivot);
    legs.push(legPivot);
  }

  // Upper body group pivoted at waist (y = 0.65) for subtle breathing/sway without lifting feet
  const upperBody = new THREE.Group();
  upperBody.position.set(0, 0.65, 0);
  g.add(upperBody);

  // Torso (rounded capsule)
  const torso = new THREE.Mesh(new THREE.CapsuleGeometry(0.24, 0.28, 8, 16), mat(shirtColor));
  torso.position.y = 0.29;
  torso.castShadow = true;
  upperBody.add(torso);

  if (tie) {
    const tieMesh = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.32, 0.05), mat("#C93B3B"));
    tieMesh.position.set(0, 0.31, 0.23);
    upperBody.add(tieMesh);
  }

  // Arms pivoted at shoulders
  const armGeo = new THREE.CylinderGeometry(0.075, 0.07, 0.44, 10);
  const sleeveGeo = new THREE.CylinderGeometry(0.095, 0.09, 0.18, 10);
  const handGeo = new THREE.SphereGeometry(0.075, 10, 8);
  const arms = [];
  for (const sx of [-0.31, 0.31]) {
    const armPivot = new THREE.Group();
    armPivot.position.set(sx, 0.47, 0);
    const sleeve = new THREE.Mesh(sleeveGeo, mat(shirtColor));
    sleeve.position.y = -0.08;
    armPivot.add(sleeve);
    const arm = new THREE.Mesh(armGeo, mat(skinColor));
    arm.position.y = -0.25;
    arm.castShadow = true;
    armPivot.add(arm);
    const hand = new THREE.Mesh(handGeo, mat(skinColor));
    hand.position.y = -0.47;
    armPivot.add(hand);
    upperBody.add(armPivot);
    arms.push(armPivot);
  }

  // Head group pivoted at neck (y = 0.62 above waist -> 1.27 world)
  const headGroup = new THREE.Group();
  headGroup.position.set(0, 0.62, 0);
  upperBody.add(headGroup);

  const head = new THREE.Mesh(new THREE.SphereGeometry(0.28, 18, 14), mat(skinColor));
  head.position.y = 0.21;
  head.castShadow = true;
  headGroup.add(head);

  // Cap hair
  const hair = new THREE.Mesh(
    new THREE.SphereGeometry(0.292, 18, 12, 0, Math.PI * 2, 0, Math.PI * 0.48),
    mat(hairColor)
  );
  hair.position.y = 0.23;
  hair.rotation.x = -0.18;
  headGroup.add(hair);

  // Eyes / sunglasses
  if (sunglasses) {
    const lensMat = mat("#14191D", 0.35);
    for (const sx of [-0.095, 0.095]) {
      const lens = new THREE.Mesh(new THREE.SphereGeometry(0.068, 12, 10), lensMat);
      lens.scale.set(1, 0.85, 0.45);
      lens.position.set(sx, 0.23, 0.26);
      headGroup.add(lens);
    }
    const bridge = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.025, 0.03), lensMat);
    bridge.position.set(0, 0.24, 0.26);
    headGroup.add(bridge);
  } else {
    const eyeMat = mat("#181A1D", 0.4);
    for (const sx of [-0.09, 0.09]) {
      const eye = new THREE.Mesh(new THREE.SphereGeometry(0.036, 10, 8), eyeMat);
      eye.position.set(sx, 0.23, 0.265);
      headGroup.add(eye);
    }
  }

  // Mouth arc
  const mouthPts = [];
  const curveSign = mood === "smile" ? 1 : mood === "frown" ? -1 : 0;
  for (let i = 0; i <= 8; i++) {
    const u = (i / 8) * 2 - 1;
    const x = u * 0.075;
    const y = 0.115 - curveSign * (1 - u * u) * 0.038;
    const z = Math.sqrt(Math.max(0.01, 0.282 * 0.282 - x * x - (y - 0.21) * (y - 0.21)));
    mouthPts.push(new THREE.Vector3(x, y, z + 0.008));
  }
  const mouthCurve = new THREE.CatmullRomCurve3(mouthPts);
  const mouthMesh = new THREE.Mesh(
    new THREE.TubeGeometry(mouthCurve, 10, 0.014, 6, false),
    mat("#3A2318")
  );
  headGroup.add(mouthMesh);

  g.userData.leftLeg = legs[0];
  g.userData.rightLeg = legs[1];
  g.userData.leftArm = arms[0];
  g.userData.rightArm = arms[1];
  g.userData.arms = arms;
  g.userData.headGroup = headGroup;
  g.userData.upperBody = upperBody;
  return g;
}

// Natural idle animation for standing characters: feet stay planted, gentle breathing + head/arm gesture
export function animateStandingCitizen(citizen, t, phase = 0) {
  const { leftLeg, rightLeg, leftArm, rightArm, headGroup, upperBody } = citizen.userData;
  if (!upperBody) return;
  leftLeg.rotation.x = 0;
  rightLeg.rotation.x = 0;
  upperBody.position.y = 0.65 + Math.sin(t * 2.0 + phase) * 0.01;
  upperBody.rotation.z = Math.sin(t * 1.1 + phase) * 0.025;
  headGroup.rotation.y = Math.sin(t * 1.35 + phase * 1.7) * 0.14;
  headGroup.rotation.x = Math.sin(t * 1.8 + phase) * 0.045;
  leftArm.rotation.x = -0.06 + Math.sin(t * 1.6 + phase) * 0.08;
  rightArm.rotation.x = -0.08 + Math.cos(t * 1.4 + phase) * 0.1;
  leftArm.rotation.z = 0.06;
  rightArm.rotation.z = -0.06;
}

// Natural walk cycle: alternating leg & arm swing with subtle stride cadence
export function animateWalkingCitizen(citizen, t, speed = 1.5, phase = 0) {
  const { leftLeg, rightLeg, leftArm, rightArm, headGroup, upperBody } = citizen.userData;
  if (!upperBody) return;
  const stride = t * speed * 3.2 + phase;
  const swing = Math.sin(stride);
  leftLeg.rotation.x = swing * 0.46;
  rightLeg.rotation.x = -swing * 0.46;
  leftArm.rotation.x = -swing * 0.36;
  rightArm.rotation.x = swing * 0.36;
  leftArm.rotation.z = 0.05;
  rightArm.rotation.z = -0.05;
  upperBody.position.y = 0.65 + Math.abs(Math.cos(stride)) * 0.02;
  upperBody.rotation.z = swing * 0.028;
  headGroup.rotation.y = Math.sin(stride * 0.5) * 0.04;
}

// Diegetic 3D sign plaque (navy or green double-bordered rectangle with cream Fredoka text)
export function createDiegeticPlaque(text, { width = 3.2, height = 1.0, bg = TOKENS.navyHud, posts = true } = {}) {
  const group = new THREE.Group();
  const c = document.createElement("canvas");
  c.width = 512;
  c.height = Math.round(512 * (height / width));
  const ctx = c.getContext("2d");

  ctx.fillStyle = TOKENS.navyStroke;
  ctx.fillRect(0, 0, c.width, c.height);
  ctx.fillStyle = TOKENS.creamText;
  ctx.fillRect(8, 8, c.width - 16, c.height - 16);
  ctx.fillStyle = bg;
  ctx.fillRect(20, 20, c.width - 40, c.height - 40);

  ctx.fillStyle = TOKENS.creamText;
  ctx.font = `700 ${Math.round(c.height * 0.48)}px Fredoka, sans-serif`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(text, c.width / 2, c.height / 2 + 2);

  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  const board = new THREE.Mesh(
    new THREE.BoxGeometry(width, height, 0.14),
    [
      new THREE.MeshStandardMaterial({ color: TOKENS.navyStroke, roughness: 0.85 }),
      new THREE.MeshStandardMaterial({ color: TOKENS.navyStroke, roughness: 0.85 }),
      new THREE.MeshStandardMaterial({ color: TOKENS.navyStroke, roughness: 0.85 }),
      new THREE.MeshStandardMaterial({ color: TOKENS.navyStroke, roughness: 0.85 }),
      new THREE.MeshStandardMaterial({ map: tex, roughness: 0.82 }),
      new THREE.MeshStandardMaterial({ color: TOKENS.navyStroke, roughness: 0.85 }),
    ]
  );
  board.position.y = posts ? 2.1 : height / 2;
  board.castShadow = true;
  group.add(board);

  if (posts) {
    const postMat = new THREE.MeshStandardMaterial({ color: "#4D555B", roughness: 0.85 });
    for (const sx of [-width * 0.36, width * 0.36]) {
      const post = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.055, 2.0, 8), postMat);
      post.position.set(sx, 1.0, 0);
      post.castShadow = true;
      group.add(post);
    }
  }
  return group;
}

// Build a clean road + sidewalk strip
export function addRoadAndSidewalks(scene, { length = 120, roadWidth = 10, sidewalkWidth = 5 } = {}) {
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(240, 240),
    new THREE.MeshStandardMaterial({ color: "#7AA062", roughness: 0.92 })
  );
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -0.02;
  ground.receiveShadow = true;
  scene.add(ground);

  const road = new THREE.Mesh(
    new THREE.BoxGeometry(length, 0.04, roadWidth),
    new THREE.MeshStandardMaterial({ color: TOKENS.asphalt, roughness: 0.9 })
  );
  road.position.y = 0.0;
  road.receiveShadow = true;
  scene.add(road);

  // Dashed white lane divider
  const dashMat = new THREE.MeshStandardMaterial({ color: "#EAECE8", roughness: 0.85 });
  for (let x = -length / 2 + 2; x < length / 2; x += 6) {
    const dash = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.05, 0.24), dashMat);
    dash.position.set(x, 0.008, 0);
    scene.add(dash);
  }

  // Sidewalks
  const swMat = new THREE.MeshStandardMaterial({ color: TOKENS.sidewalk, roughness: 0.88 });
  for (const sz of [-(roadWidth / 2 + sidewalkWidth / 2), roadWidth / 2 + sidewalkWidth / 2]) {
    const sw = new THREE.Mesh(new THREE.BoxGeometry(length, 0.16, sidewalkWidth), swMat);
    sw.position.set(0, 0.08, sz);
    sw.receiveShadow = true;
    scene.add(sw);
  }
}

// Assemble a Polyfork street block (uses real-metre GLBs at y=0 without arbitrary rescaling)
export function populatePolyforkStreet(scene, models, { crowded = false, busLane = false } = {}) {
  addRoadAndSidewalks(scene);

  // Green painted bus lane if enabled
  if (busLane) {
    const lane = new THREE.Mesh(
      new THREE.BoxGeometry(120, 0.048, 3.8),
      new THREE.MeshStandardMaterial({ color: "#5E8E52", roughness: 0.88 })
    );
    lane.position.set(0, 0.005, -2.6);
    lane.receiveShadow = true;
    scene.add(lane);
  }

  // Far-side buildings (z = -14..-16, facing +Z toward street) + second background row for skyline depth
  const farSlots = [
    { key: "tenement", x: -34, z: -14.2, ry: 0 },
    { key: "shopRow", x: -21, z: -13.5, ry: 0 },
    { key: "tenement", x: -8, z: -14.2, ry: 0 },
    { key: "shopRow", x: 5, z: -13.5, ry: 0 },
    { key: "tenement", x: 18, z: -14.2, ry: 0 },
    { key: "shopRow", x: 31, z: -13.5, ry: 0 },
    // Background skyline blocks
    { key: "tenement", x: -26, z: -27, ry: 0 },
    { key: "tenement", x: -2, z: -27.5, ry: 0 },
    { key: "tenement", x: 22, z: -27, ry: 0 },
  ];
  for (const s of farSlots) {
    const inst = models[s.key].clone();
    inst.position.set(s.x, 0, s.z);
    inst.rotation.y = s.ry;
    scene.add(inst);
  }

  // Street trees along far and near sidewalks
  for (const tx of [-28, -17, -1, 13, 27]) {
    const tree = models.tree.clone();
    tree.position.set(tx, 0.14, -7.2);
    scene.add(tree);
  }
  for (const tx of [-22, -10, 14, 26]) {
    const tree = models.tree.clone();
    tree.position.set(tx, 0.14, 9.2);
    scene.add(tree);
  }

  // Dynamic vehicles list returned so caller can drive them deterministically at time t
  const vehicles = [];
  if (!crowded) {
    const bus1 = models.bus.clone();
    bus1.rotation.y = Math.PI / 2; // faces +X along road
    bus1.position.set(-4, 0.02, -2.5);
    scene.add(bus1);
    vehicles.push({ mesh: bus1, baseX: -4, speed: 5.5, span: 64 });

    const bus2 = models.bus.clone();
    bus2.rotation.y = Math.PI / 2;
    bus2.position.set(-34, 0.02, -2.5);
    scene.add(bus2);
    vehicles.push({ mesh: bus2, baseX: -34, speed: 5.5, span: 64 });

    const car1 = models.hatchback.clone();
    car1.rotation.y = -Math.PI / 2;
    car1.position.set(14, 0.02, 2.5);
    scene.add(car1);
    vehicles.push({ mesh: car1, baseX: 14, speed: -4.2, span: 64 });

    const car2 = models.towncar.clone();
    car2.rotation.y = -Math.PI / 2;
    car2.position.set(-12, 0.02, 2.5);
    scene.add(car2);
    vehicles.push({ mesh: car2, baseX: -12, speed: -4.6, span: 64 });
  } else {
    // Bumper-to-bumper private car congestion
    const keys = ["towncar", "hatchback", "towncar", "hatchback", "towncar", "hatchback", "towncar", "hatchback"];
    keys.forEach((k, idx) => {
      const m = models[k].clone();
      const laneZ = idx % 2 === 0 ? -2.4 : 2.4;
      const dir = idx % 2 === 0 ? 1 : -1;
      m.rotation.y = dir > 0 ? Math.PI / 2 : -Math.PI / 2;
      const bx = -22 + idx * 6.0;
      m.position.set(bx, 0.02, laneZ);
      scene.add(m);
      vehicles.push({ mesh: m, baseX: bx, speed: dir * 0.9, span: 56 });
    });
  }

  return { vehicles };
}

const PEDESTRIAN_SHIRTS = [
  TOKENS.capsuleOrange,
  TOKENS.capsuleTeal,
  TOKENS.capsulePlum,
  "#D95B5B",
  "#4B79B8",
  "#E8A838",
  "#6E9E58",
  "#E28FA6",
];
const PEDESTRIAN_SKINS = ["#C98F63", "#D8A67E", "#B67A50", "#E0B694"];
const PEDESTRIAN_PANTS = ["#2E3B4E", "#3B3F47", "#4A3F35", "#273742"];

// Populate bustling walking NPC pedestrians along both sidewalks (deterministic, zero Math.random)
export function populatePedestrians(scene, { count = 24, mood = "smile", excludeNearCenter = false } = {}) {
  const pedestrians = [];
  const span = 52;
  for (let i = 0; i < count; i++) {
    const farSide = i % 2 === 0 || (excludeNearCenter && i % 3 !== 0);
    const dir = i % 3 === 0 ? -1 : 1;
    // Far sidewalk: z in [-8.4, -5.6]; near sidewalk: z in [5.6, 8.2]
    const laneOffset = ((i * 37) % 10) / 10;
    let z = farSide ? -5.8 - laneOffset * 2.4 : 5.7 + laneOffset * 2.4;
    if (excludeNearCenter && !farSide && z < 7.1) {
      z = 7.4 + (laneOffset * 0.9); // keep clear of foreground HALTE BUS commuters
    }
    const baseX = -span / 2 + ((i * 7.3 + 2.1) % span);
    const speed = (1.15 + ((i * 19) % 8) * 0.11) * dir;
    const citizen = createCapsuleCitizen({
      shirtColor: PEDESTRIAN_SHIRTS[i % PEDESTRIAN_SHIRTS.length],
      pantsColor: PEDESTRIAN_PANTS[i % PEDESTRIAN_PANTS.length],
      skinColor: PEDESTRIAN_SKINS[i % PEDESTRIAN_SKINS.length],
      mood: mood === "mixed" ? (i % 3 === 0 ? "frown" : "neutral") : mood,
      sunglasses: i % 7 === 0,
      tie: i % 5 === 0,
    });
    citizen.position.set(baseX, 0.16, z);
    citizen.rotation.y = dir > 0 ? Math.PI / 2 : -Math.PI / 2;
    scene.add(citizen);
    pedestrians.push({
      mesh: citizen,
      baseX,
      speed,
      span,
      phase: i * 1.17,
    });
  }
  return pedestrians;
}

export function stepPedestrians(pedestrians, t) {
  for (const p of pedestrians) {
    const half = p.span / 2;
    let x = p.baseX + p.speed * t;
    x = ((((x + half) % p.span) + p.span) % p.span) - half;
    p.mesh.position.x = x;
    animateWalkingCitizen(p.mesh, t, Math.abs(p.speed), p.phase);
  }
}

export function stepVehicles(vehicles, t) {
  for (const v of vehicles) {
    const half = v.span / 2;
    let x = v.baseX + v.speed * t;
    x = ((((x + half) % v.span) + v.span) % v.span) - half;
    v.mesh.position.x = x;
  }
}
