# Explainer Grammars, Motion Devices & Measured Curves

Read when planning scene visual grammar at `storyboard` or choreographing camera, transitions, and GSAP timelines at `production`. Keep HyperFrames' [motion reference](../../hyperframes/references/motion.md) as the render contract; apply the domain-specific rules below to avoid slide-deck pacing and uniform motion.

## 1. Pick the visual grammar from the narration job

Match each sequence (or board) to what the spoken argument is doing; never mix incompatible grammars inside one beat:

| Spoken job | Visual grammar | Core staging rule | Typical shot / beat | Primary curve & seam |
| --- | --- | --- | --- | --- |
| **Mechanism / transformation** ("how X turns into Y", hidden assemblies) | **State-Morph / Cutaway** (3b1b / *Di Balik Benda*) | Stage only the active parts; morph or actuate one state directly into the next; color = functional role (input / active / output) | 3–6 s per causal link; 0.5 s settle hold | Smooth S-curve (`cubic-bezier(0.65,0,0.35,1)` / `power2.inOut`), `zoomThrough` or carried landmark |
| **Scale / system overview** (micro-to-macro, backyard ecosystem) | **Layered World Scale-Travel** (Kurzgesagt / *Budidaya*) | Concrete illustrated world with continuous landmarks; logarithmic camera zoom (`scale = s0 * Math.pow(s1/s0, p)`) across scales | 4.5–8 s per view; internal state read every <= 4 s | `cubic-bezier(0.75,0,0.25,1)` camera; ambient subordinate to primary flow |
| **Evidence / documents / real captures** (news, studies, screenshots) | **Investigation Desk** (Vox) | Real source artifact fills the stage on a tactile surface; highlighter/red-line callouts draw on stepped 12 fps | 2.5–5 s per exhibit; 1.4–1.8 s montage | `sine.inOut` desk pan/push; stepped callout strokes |
| **Step-by-step causal deduction** ("why A leads to B leads to C") | **Continuous Surface / Whiteboard** (RSA) | Draw each node ~0.3–0.5 s after its spoken cue on one shared canvas; camera pans along the chain and pulls wide at payoff | 5–7 s per cluster | `sine.inOut` pan (1.0–1.8 s); final wide pull |
| **Relatable interpersonal moment** (everyday conflict, dialogue, reaction) | **Pose-Snap Character Acting** (Storytime / *Ruang di Antara*) | Fast 0.10–0.16 s pose transitions (`expo.out` + subtle settle), then hold expression readable; reaction close-up on the emotional turn | 2–4.5 s per beat | `expo.out` pose change; hard cut on reaction or palette inversion |
| **Quantitative claim / trend** (comparisons, thresholds, ratios) | **Honest Coordinate Chart** | Build axes/units first, grow data second, mark **one** takeaway last; land live counters exactly on the spoken number (`t_start = t_word - dur`) | 3–5.5 s per chart | `quint.out` / `power4.out`; never put a lone stat on a flat solid card |

## 2. Measured motion laws (frame-accurate defaults at 30 fps)

Derived from frame-by-frame analysis of professional motion pieces (`motionmaxxing` & `cinetic`):

- **Asymmetric easing by role:**
  - **Arrive (decelerate):** `expo.out` or `power4.out`, `10–14 frames` (`0.33–0.47 s`), putting ~70% of travel in the first `4–6 frames` with a long settle tail.
  - **Reposition / Camera:** `power2.inOut` or `sine.inOut`, `18–36 frames` (`0.6–1.2 s`).
  - **Leave (accelerate):** `power3.in` or `expo.in`, `6–9 frames` (`0.20–0.30 s` — 40–50% shorter than arrival), cut at peak speed.
- **Arrive from oversize or edge, never `scale(0)`:** Hero marks, callout pills, and insets enter from `1.08×–1.35×` settling to `1.0×`, by mask/clip-path reveal, or from off-frame momentum. Growing cards from `scale: 0` reads as generic UI template code.
- **Restrain bounce:** Critically damped (`zeta = 1.0`) by default; at most one spring class (`zeta = 0.72–0.85`, 4–8% overshoot) when physical weight demands it. Opacity and color never overshoot.
- **Parallax & container hierarchy:** When a card or inset scales `+20%`, scale its inner content `+8%`; separate background, mid-stage, and foreground planes at `1.0 : 1.08 : 1.16` during pans.
- **Transient emphasis color:** Highlight newness on the spoken trigger word, then cool or pass emphasis to the affected part when the next causal step begins.

## 3. Velocity handoff & camera punctuation

- **Camera is punctuation, not wallpaper:**
  1. **Hold still** while an internal mechanism actuates or the viewer reads a label.
  2. **Gentle push / pan / pull (`0.6–1.5 s`)** guides the eye to the next component or reveals the whole system.
  3. **Snap-zoom (`0.25–0.30 s`, +18–32%) or slam (`0.17 s`)** is an accent reserved for the hook turn, critical failure, or payoff — at most `1/3` of scenes.
  4. **Never chain 3 push-ins in a row:** after pushing in to inspect a detail, pull back, track laterally along the flow path, or cut to an orthogonal angle (`storyboard_lint.py` fails 3+ consecutive pushes).
- **Velocity-handoff cuts (`dv-velocity-handoff-cut`):**
  - Instead of cutting between two parked frames, accelerate the outgoing camera/subject over the final `6–12 frames` (`power2.in`) and open the incoming scene already moving in the **same vector** at `0.6–1.2×` that speed, decelerating (`expo.out`) over `12–24 frames` to its readable hold.
- **Carried-object seams:** Keep one shared physical landmark (pipe rim, shaft axis, table edge, water surface) at matched screen coordinates across a cut, or grow an inset frame until it becomes the next scene's stage.

## 4. Emotion-to-motion personality presets (for boards & episodes)

When translating a board's emotional tone into concrete timing tokens:

| Board personality | Arrival curve & duration | Camera cadence | Stagger & hold character |
| --- | --- | --- | --- |
| **Crisp / Mechanical** (*Di Balik Benda*) | `power4.out`, `0.30–0.38 s`, zero bounce (`zeta = 1.0`) | Locked diagnostic macro holds; decisive axial tracks | Tight `40–60 ms` part staggers; `0.5 s` post-contact verification hold |
| **Warm / Cultivated** (*Budidaya di Halaman*) | `cubic-bezier(0.22,1,0.36,1)`, `0.40–0.55 s` | Smooth `0.8–1.2 s` cutaway push & lateral route follow | Organic `70–110 ms` staggers; calm day-to-dusk light shifts |
| **Reflective / Human** (*Ruang di Antara*) | `sine.out` / `power3.out`, `0.45–0.65 s` | Intimate two-shot / reaction framing; deliberate stillness before turns | Phrase-paced reveals; `0.8–1.4 s` breath before emotional pivot |
| **Investigative / Urgent** (Documentary / Tech) | `expo.out`, `0.24–0.32 s`, stepped `12 fps` callouts | Snappy desk pans + hard punch-ins on evidence | Crisp `35–50 ms` staggers; J-cut audio leading picture by `2–4 frames` |
