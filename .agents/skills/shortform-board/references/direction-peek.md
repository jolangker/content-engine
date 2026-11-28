# Animated direction peek

When proposing competing visual directions during exploration, show them visually and in motion before asking the user to choose. A direction peek is a lightweight, ephemeral, self-contained HTML preview that lets the user compare framing, typography, palette, and motion character at a glance.

## When to build a direction peek

Build an animated direction peek automatically whenever `shortform-board` proposes visual direction options:

- **New board exploration** presenting roughly 3–5 distinct directions.
- **Remix or refinement rounds** comparing combined or adjusted options before a direction is locked.
- **Visual revision or revamp** of an existing board when offering multiple alternative visual directions.

Skip the direction peek for:

- Operational edits (`ACCOUNTS.json`, `AUDIO.json`).
- Purely editorial or conceptual discussions where no visual options are being pitched (or when the user explicitly asks to discuss conceptually first).
- A single already-developed concept proceeding directly to full board package build.
- `video-to-board`, which already presents reference evidence and measurements at its approval gate.

## Delivery and ephemeral storage

Produce **one self-contained HTML file under 512 KB** with all CSS, JS, and inline SVG/Canvas code embedded.

- **In Orca** (when `ORCA_CHAT_SCRATCH_DIR` is set and writable): save the file directly in `ORCA_CHAT_SCRATCH_DIR` with a unique filename matching `[a-zA-Z0-9._-]+\.html` (for example, `direction-peek-craft-7a2c.html`). Show it inline in the reply by placing this directive on its own line outside any code block:

  ```text
  ::orca-visual{file="direction-peek-craft-7a2c.html" title="Creative direction peek"}
  ```

- **Outside Orca** (when `ORCA_CHAT_SCRATCH_DIR` is unset or unwritable): save the standalone HTML file to a local temporary/scratch folder **outside the repository** and provide a clickable file link so the user can open it in any browser.
- **Workspace hygiene:** Never create `boards/<slug>/` or modify `TRACKER.json` for a direction peek. After the user selects a direction, move on to the official board package (`DIRECTION.md`, `frame.md`, `style-board.html`, `motion-preview/`) without archiving the exploratory peek HTML in the repository; record only the chosen direction and rationale in `DIRECTION.md`.

## What each direction card shows

Render each proposed direction as a **9:16 vertical phone frame** (or the brief's target aspect ratio if explicitly non-vertical) running a **4–6 second looping 1–2 beat animation**:

1. **Hook entrance:** opening subject and hook line enter with the direction's intended rhythm and energy.
2. **Primary visual motion:** a brief-specific illustration, diagram, UI artifact, or mechanical/spatial graphic moving in a way that carries meaning.
3. **One short reveal or transition:** a beat shift, highlight, cutaway reveal, or framing move that previews how information unfolds.
4. **Sample caption and type treatment:** illustrative copy set in the direction's proposed display/body font pairing and caption placement.

Directly beneath each 9:16 stage, include a **compact info strip** with:

- Direction label/name (matching the chat summary).
- Palette swatches (hex values with roles).
- Font pairing (display + body/mono).
- A short one-line motion and audio mood cue.

Identify sample copy as illustrative; do not present unverified claims as episode facts.

## Layout, styling, and playback controls

- **Responsive side-by-side grid** (2–3 columns depending on count) so every card stays readable at a glance.
- **Auto-play loop on load** so the differences in pacing and feel are immediately visible.
- **Lightweight controls** in a compact top bar:
  - **Play / Pause** toggling all animations cleanly (sync CSS `animation-play-state` and any JS/rAF timers).
  - **Replay from 0s** resetting every direction's timeline to `t = 0` together so hooks can be compared fairly.
  - **Click-to-focus / zoom** on any card to open a larger phone-scale view with its own Replay and Close controls.
- **Theme and standalone browser compatibility:**
  - Style the outer shell and controls with Orca theme variables (`--background`, `--foreground`, `--card`, `--card-foreground`, `--muted`, `--muted-foreground`, `--border`, `--accent`, `--accent-foreground`, `--radius`, `--font-sans`, `--font-mono`), always paired with explicit fallback values (for example, `background: var(--background, #ffffff); color: var(--foreground, #171717)`) so the file renders cleanly in an ordinary browser too.
  - Never redefine Orca tokens on `:root`. Scope each direction's fixed creative palette inside its own stage class/ID.
  - Do not size the layout to `100vh`; let the embed fit the content height.

## Medium and asset rules

- Build every direction in **pure code inside the HTML**: inline SVG, CSS, Canvas 2D, and—only when a direction genuinely proposes 3D—lightweight Three.js loaded from an allowed CDN (`cdn.jsdelivr.net`, `unpkg.com`, `cdnjs.cloudflare.com`, `esm.sh`).
- Load proposed webfonts from `fonts.googleapis.com` / `fonts.gstatic.com` with clean fallback stacks.
- Do **not** include `<audio>` or `<video>` elements, do **not** fetch external images or remote data at runtime, and do **not** run external image generation for direction peeks.
- Use procedural gradients, grain, hatching, or layered vector geometry to express surface feel. Whenever a direction's real production medium would be richer (such as detailed 3D renders, painterly illustration, or photography), display a short badge or note on the card (for example, `Stylized proxy · final medium: 3D cutaway`) so the user judges structure, palette, typography, and motion rhythm accurately.

## Craft bar and proportional verification

- **Real differentiation:** vary visual structure, framing, typography, subject treatment, and motion physics across directions—never present the same layout with swapped colors or generic wireframe placeholder boxes.
- **Brief specificity:** draw recognizable motifs, objects, or illustrative copy tied to the user's actual topic.
- **Proportional verification before presenting:**
  - Confirm the HTML is complete, syntactically valid, under 512 KB, and follows the CDN, media, and CSS fallback rules.
  - Check that timelines loop cleanly and that Play/Pause, Replay from 0s, and click-to-focus work without JS errors.
  - Run a quick headless Chrome console/render check **only when** the peek uses complex Canvas 2D or Three.js scenes where runtime errors or blank canvases are likely; skip heavy screenshot loops for straightforward SVG/CSS peeks to keep exploration fast.

## Accompanying chat summary

Let the animated visual peek carry palette, typography, framing, and motion character. Keep the accompanying chat text concise and complementary:

- Give a brief, scannable entry per direction covering its **editorial angle / intended viewer experience**, **how an episode unfolds**, and **key trade-off**.
- Present the alternatives before giving **one clear recommendation** tied to the user's context, and invite the user to choose, remix elements across options, or redirect.
