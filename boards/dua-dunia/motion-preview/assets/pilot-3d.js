import * as THREE from "./vendor/three.module.min.js";
import {
  TOKENS,
  loadPolyforkModels,
  createRenderer,
  createDaylightScene,
  createCapsuleCitizen,
  animateStandingCitizen,
  createDiegeticPlaque,
  populatePolyforkStreet,
  populatePedestrians,
  stepPedestrians,
  stepVehicles,
} from "./kit-3d.js";

function renderSplitScreen(renderer, sceneTop, camTop, sceneBot, camBot, w, h) {
  const halfH = Math.floor(h / 2);
  renderer.setScissorTest(true);
  renderer.setViewport(0, halfH, w, h - halfH);
  renderer.setScissor(0, halfH, w, h - halfH);
  renderer.render(sceneTop, camTop);
  renderer.setViewport(0, 0, w, halfH);
  renderer.setScissor(0, 0, w, halfH);
  renderer.render(sceneBot, camBot);
  renderer.setScissorTest(false);
}

function clamp01(x) {
  return Math.max(0, Math.min(1, x));
}

function easeOutCubic(x) {
  const t = clamp01(x);
  return 1 - Math.pow(1 - t, 3);
}

function easeOutBack(x) {
  const t = clamp01(x);
  const c1 = 1.70158;
  const c3 = c1 + 1;
  return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
}

// Word-level synced karaoke cues matched to audio/narration.mp3 timestamps
const CAPTION_CUES = [
  {
    start: 0.0,
    end: 2.25,
    words: [
      { text: "Kalau", s: 0.0 },
      { text: "bus", s: 0.22 },
      { text: "kota", s: 0.42 },
      { text: "digratiskan", s: 0.7 },
      { text: "besok,", s: 1.28 },
    ],
  },
  {
    start: 2.25,
    end: 3.55,
    words: [
      { text: "macet", s: 2.3 },
      { text: "langsung", s: 2.56 },
      { text: "hilang?", s: 2.8 },
    ],
  },
  {
    start: 3.55,
    end: 5.45,
    words: [
      { text: "Kita", s: 3.64 },
      { text: "bikin", s: 3.86 },
      { text: "dua", s: 4.18 },
      { text: "kota", s: 4.32 },
      { text: "sama", s: 4.62 },
      { text: "persis.", s: 4.8 },
    ],
  },
  {
    start: 5.45,
    end: 8.6,
    words: [
      { text: "Bedanya", s: 5.54 },
      { text: "satu:", s: 6.22 },
      { text: "tarif", s: 6.94 },
      { text: "bus", s: 7.26 },
      { text: "Rp", s: 7.52 },
      { text: "0.", s: 7.96 },
    ],
  },
  {
    start: 8.6,
    end: 11.65,
    words: [
      { text: "Di", s: 8.74 },
      { text: "Kota", s: 8.88 },
      { text: "Berbayar,", s: 9.1 },
      { text: "mobil", s: 9.84 },
      { text: "menumpuk.", s: 10.1 },
    ],
  },
  {
    start: 11.65,
    end: 13.75,
    words: [
      { text: "Tahun", s: 11.8 },
      { text: "pertama", s: 12.06 },
      { text: "sempat", s: 12.52 },
      { text: "seret", s: 13.04 },
      { text: "dulu.", s: 13.3 },
    ],
  },
  {
    start: 13.75,
    end: 17.05,
    words: [
      { text: "Tahun", s: 14.44 },
      { text: "ketiga,", s: 14.62 },
      { text: "Kota", s: 15.34 },
      { text: "Gratis", s: 15.58 },
      { text: "nyalip!", s: 16.0 },
    ],
  },
];

function renderCaptionHtml(t) {
  const cue =
    CAPTION_CUES.find((c) => t >= c.start && t < c.end) ||
    CAPTION_CUES[CAPTION_CUES.length - 1];
  let activeIdx = 0;
  for (let i = 0; i < cue.words.length; i++) {
    if (t >= cue.words[i].s) activeIdx = i;
  }
  return cue.words
    .map((w, i) => (i === activeIdx ? `<span class="active">${w.text}</span>` : w.text))
    .join(" ");
}

export async function createPilotController({
  canvas,
  overlayEl,
  modelsBaseUrl = "./assets/models",
}) {
  const models = await loadPolyforkModels(modelsBaseUrl);
  const renderer = createRenderer(canvas, 1080, 1920);

  // Beat 1 (0.0 - 3.55s): Street-level hook with bustling pedestrians + natural standing commuters
  const hookScene = createDaylightScene();
  const { vehicles: hookVehicles } = populatePolyforkStreet(hookScene, models, {
    crowded: false,
    busLane: true,
  });
  const hookPedestrians = populatePedestrians(hookScene, {
    count: 24,
    mood: "smile",
    excludeNearCenter: true,
  });

  const plaque = createDiegeticPlaque("HALTE BUS", {
    width: 2.7,
    height: 0.85,
    bg: TOKENS.navyHud,
  });
  plaque.position.set(0.35, 0.16, 4.9);
  plaque.rotation.y = -0.1;
  hookScene.add(plaque);

  const c1 = createCapsuleCitizen({ shirtColor: TOKENS.capsuleOrange, mood: "smile" });
  c1.position.set(-1.35, 0.16, 6.2);
  c1.rotation.y = 0.28;
  hookScene.add(c1);

  const c2 = createCapsuleCitizen({
    shirtColor: TOKENS.capsuleTeal,
    mood: "neutral",
    sunglasses: true,
    tie: true,
  });
  c2.position.set(0.05, 0.16, 6.35);
  c2.rotation.y = -0.22;
  hookScene.add(c2);

  const hookCam = new THREE.PerspectiveCamera(42, 1080 / 1920, 0.1, 200);

  // Beat 2 (3.55 - 11.65s): 50/50 split-screen twin worlds with bustling sidewalks
  const sceneTop = createDaylightScene();
  const { vehicles: vTop } = populatePolyforkStreet(sceneTop, models, {
    crowded: false,
    busLane: true,
  });
  const pedsTop = populatePedestrians(sceneTop, { count: 26, mood: "smile" });
  const topPlaque = createDiegeticPlaque("TARIF Rp 0", {
    width: 3.4,
    height: 0.9,
    bg: TOKENS.navyHud,
    posts: false,
  });
  topPlaque.position.set(-5.2, 2.0, 4.4);
  sceneTop.add(topPlaque);

  const sceneBot = createDaylightScene();
  const { vehicles: vBot } = populatePolyforkStreet(sceneBot, models, {
    crowded: true,
    busLane: false,
  });
  const pedsBot = populatePedestrians(sceneBot, { count: 22, mood: "mixed" });

  const splitCamTop = new THREE.PerspectiveCamera(42, 1080 / 960, 0.1, 200);
  const splitCamBot = new THREE.PerspectiveCamera(42, 1080 / 960, 0.1, 200);

  // Beat 3 (11.65 - 17.0s): Dimmed elevated city backdrop + Crossover Data HUD
  const dataScene = createDaylightScene();
  const { vehicles: vData } = populatePolyforkStreet(dataScene, models, {
    crowded: false,
    busLane: true,
  });
  const pedsData = populatePedestrians(dataScene, { count: 22, mood: "smile" });
  const dataCam = new THREE.PerspectiveCamera(44, 1080 / 1920, 0.1, 200);

  overlayEl.innerHTML = `
    <div class="disclaimer stroke-text">Eksperimen pikiran. Angka dari model.</div>

    <div id="hook-layer" class="layer">
      <div id="hook-headline" class="headline stroke-text">ANGKUTAN UMUM<br/>GRATIS?</div>
    </div>

    <div id="split-layer" class="layer">
      <div id="dim-top" class="dim-half top"></div>
      <div id="dim-bot" class="dim-half bottom"></div>
      <div class="split-divider"></div>
      <div class="panel-label top stroke-text">Kota Gratis</div>
      <div class="panel-label bottom stroke-text">Kota Berbayar</div>
      <div id="center-pill" class="center-pill">10.000 warga</div>
    </div>

    <div id="data-layer" class="layer">
      <div id="data-backdrop" class="data-backdrop"></div>
      <div id="data-callout" class="callout-title stroke-text">Nyalip!</div>
      <div id="hud-card" class="hud-card">
        <div class="hud-title">Kecepatan rata-rata harian (km/jam)</div>
        <svg viewBox="0 0 820 430" width="820" height="430" style="overflow:visible;">
          <line x1="40" y1="360" x2="780" y2="360" stroke="#9EB4C2" stroke-width="4" />
          <path id="line-amber" d="M 55 245 L 235 235 L 420 230 L 600 245 L 765 268" fill="none" stroke="#E8A838" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" />
          <path id="line-green" d="M 55 245 L 235 298 L 420 230 L 600 135 L 765 72" fill="none" stroke="#78A55E" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" />
          <g id="crossover-mark">
            <line x1="420" y1="230" x2="420" y2="360" stroke="#FFFDF5" stroke-width="4" stroke-dasharray="10 10" />
            <circle cx="420" cy="230" r="14" fill="#FFFDF5" stroke="#142A36" stroke-width="5" />
            <text x="420" y="195" text-anchor="middle" fill="#FFFDF5" font-size="30" font-weight="700">Tahun 3</text>
          </g>
          <g id="legend-green">
            <circle cx="555" cy="78" r="11" fill="#78A55E" />
            <text x="576" y="88" fill="#FFFDF5" font-size="28" font-weight="600">Kota Gratis</text>
          </g>
          <g id="legend-amber">
            <circle cx="555" cy="312" r="11" fill="#E8A838" />
            <text x="576" y="322" fill="#FFFDF5" font-size="28" font-weight="600">Kota Berbayar</text>
          </g>
          <text x="55" y="405" text-anchor="middle" fill="#D5E3EC" font-size="28" font-weight="600">Thn 0</text>
          <text x="235" y="405" text-anchor="middle" fill="#D5E3EC" font-size="28" font-weight="600">Thn 1</text>
          <text x="420" y="405" text-anchor="middle" fill="#D5E3EC" font-size="28" font-weight="600">Thn 3</text>
          <text x="600" y="405" text-anchor="middle" fill="#D5E3EC" font-size="28" font-weight="600">Thn 6</text>
          <text x="765" y="405" text-anchor="middle" fill="#D5E3EC" font-size="28" font-weight="600">Thn 10</text>
        </svg>
      </div>
    </div>

    <div class="caption-band stroke-text"><span id="caption-text"></span></div>
  `;

  const hookLayer = overlayEl.querySelector("#hook-layer");
  const hookHeadline = overlayEl.querySelector("#hook-headline");
  const splitLayer = overlayEl.querySelector("#split-layer");
  const dimTop = overlayEl.querySelector("#dim-top");
  const dimBot = overlayEl.querySelector("#dim-bot");
  const centerPill = overlayEl.querySelector("#center-pill");
  const dataLayer = overlayEl.querySelector("#data-layer");
  const dataBackdrop = overlayEl.querySelector("#data-backdrop");
  const dataCallout = overlayEl.querySelector("#data-callout");
  const hudCard = overlayEl.querySelector("#hud-card");
  const lineAmber = overlayEl.querySelector("#line-amber");
  const lineGreen = overlayEl.querySelector("#line-green");
  const crossoverMark = overlayEl.querySelector("#crossover-mark");
  const captionText = overlayEl.querySelector("#caption-text");

  const amberLen = lineAmber.getTotalLength();
  const greenLen = lineGreen.getTotalLength();
  lineAmber.style.strokeDasharray = `${amberLen}`;
  lineGreen.style.strokeDasharray = `${greenLen}`;

  function renderAt(rawT) {
    const t = Math.max(0, Math.min(17.0, Number(rawT) || 0));
    captionText.innerHTML = renderCaptionHtml(t);

    if (t < 3.55) {
      // Beat 1: Street-level hook (natural standing idle + walking crowd + bus glide)
      hookLayer.style.display = "block";
      splitLayer.style.display = "none";
      dataLayer.style.display = "none";

      stepVehicles(hookVehicles, t * 1.25 + 0.8);
      stepPedestrians(hookPedestrians, t + 2.0);
      // Feet planted on sidewalk; natural breathing, head turn, and relaxed arm sway
      animateStandingCitizen(c1, t, 0.0);
      animateStandingCitizen(c2, t, 1.8);

      const p = clamp01(t / 3.55);
      hookCam.position.set(-2.25 + p * 0.9, 3.6 + p * 0.18, 17.2 - p * 1.15);
      hookCam.lookAt(0.1, 2.1, -1.0);

      renderer.setScissorTest(false);
      renderer.setViewport(0, 0, 1080, 1920);
      renderer.render(hookScene, hookCam);

      const hIn = easeOutBack(t / 0.32);
      const hOut = t > 3.28 ? 1 - clamp01((t - 3.28) / 0.24) : 1;
      hookHeadline.style.opacity = `${clamp01(t / 0.2) * hOut}`;
      hookHeadline.style.transform = `scale(${0.86 + 0.14 * hIn})`;
    } else if (t < 11.65) {
      // Beat 2: 50/50 twin-world split-screen comparison
      hookLayer.style.display = "none";
      splitLayer.style.display = "block";
      dataLayer.style.display = "none";

      const lt = t - 3.55;
      stepVehicles(vTop, lt * 1.45 + 1.2);
      stepVehicles(vBot, lt * 0.45 + 0.3);
      stepPedestrians(pedsTop, lt + 1.0);
      stepPedestrians(pedsBot, lt + 4.0);

      const drift = lt * 0.45;
      splitCamTop.position.set(-5.2 + drift, 10.6, 15.6 - lt * 0.14);
      splitCamTop.lookAt(-1.4 + drift * 0.5, 1.4, -0.5);

      splitCamBot.position.set(-5.2 + drift, 10.6, 15.6 - lt * 0.14);
      splitCamBot.lookAt(-1.4 + drift * 0.5, 1.4, -0.5);

      renderSplitScreen(renderer, sceneTop, splitCamTop, sceneBot, splitCamBot, 1080, 1920);

      // Spotlight dimming switches smoothly at t = 8.6s (lt = 5.05s) right as "Di Kota Berbayar" begins
      const flip = easeOutCubic((lt - 4.9) / 0.35);
      dimTop.style.opacity = `${0.44 * flip}`;
      dimBot.style.opacity = `${0.44 * (1 - flip)}`;

      const pillPop = easeOutBack((lt - 0.15) / 0.3);
      centerPill.textContent = lt < 5.05 ? "10.000 warga" : "1 bus = 30 mobil";
      centerPill.style.opacity = `${clamp01((lt - 0.1) / 0.2)}`;
      centerPill.style.transform = `translate(-50%, -50%) scale(${0.84 + 0.16 * pillPop})`;
    } else {
      // Beat 3: Crossover data HUD over dimmed bustling 3D city
      hookLayer.style.display = "none";
      splitLayer.style.display = "none";
      dataLayer.style.display = "block";

      const lt = t - 11.65;
      stepVehicles(vData, lt * 1.2 + 2.0);
      stepPedestrians(pedsData, lt + 3.0);
      dataCam.position.set(-10 + lt * 0.72, 16.2 - lt * 0.14, 18.0 - lt * 0.32);
      dataCam.lookAt(0 + lt * 0.35, 1.0, 0);

      renderer.setScissorTest(false);
      renderer.setViewport(0, 0, 1080, 1920);
      renderer.render(dataScene, dataCam);

      const fade = easeOutCubic(lt / 0.35);
      dataBackdrop.style.opacity = `${fade}`;
      hudCard.style.opacity = `${fade}`;
      hudCard.style.transform = `translateY(${(1 - fade) * 32}px)`;

      // Curves draw progressively between lt = 0.3s and lt = 4.3s
      const drawP = easeOutCubic((lt - 0.3) / 4.0);
      lineAmber.style.strokeDashoffset = `${amberLen * (1 - drawP)}`;
      lineGreen.style.strokeDashoffset = `${greenLen * (1 - drawP)}`;

      // Crossover marker + "Nyalip!" headline pop at t = 14.55s (lt = 2.9s) synced with "tahun ketiga"
      const crossP = easeOutBack((lt - 2.85) / 0.35);
      const crossOp = clamp01((lt - 2.8) / 0.2);
      crossoverMark.style.opacity = `${crossOp}`;
      dataCallout.style.opacity = `${crossOp}`;
      dataCallout.style.transform = `scale(${0.82 + 0.18 * crossP})`;
    }
  }

  return { renderAt };
}
