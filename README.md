# Content Engine

Skill-driven workspace for short-form video production. Reusable creative boards define editorial, visual, motion, audio, and quality-gate contracts; episodes run from brief and research through [HyperFrames](.agents/skills/hyperframes/SKILL.md) rendering, automated verification, content packaging, and optional Trypost delivery.

See [`AGENTS.md`](AGENTS.md) for the authoritative agent operating rules, and [`TRACKER.json`](TRACKER.json) for the live registry of boards and productions.

## Workflows

| Skill | Use when | Entrypoint |
| --- | --- | --- |
| `shortform-board` | Exploring, creating, or revising a reusable creative board (editorial framework, `frame.md`, style board, playable motion preview, `CONTRACT.json`, `AUDIO.json`, `ACCOUNTS.json`). | [`.agents/skills/shortform-board/SKILL.md`](.agents/skills/shortform-board/SKILL.md) |
| `video-to-board` | Deriving a new creative board from supplied reference clips via `rea-video` analysis and a single vision-alignment gate. | [`.agents/skills/video-to-board/SKILL.md`](.agents/skills/video-to-board/SKILL.md) |
| `shortform-production` | Creating, continuing, or revising an episode through export, `CONTENT_PACKAGE.md`, optional Trypost publishing, or published-episode performance review. | [`.agents/skills/shortform-production/SKILL.md`](.agents/skills/shortform-production/SKILL.md) |
| `board-export` | Exporting a board as a standalone, tool-agnostic creative-direction package under `exports/`. | [`.agents/skills/board-export/SKILL.md`](.agents/skills/board-export/SKILL.md) |

Upstream craft and media skills (`hyperframes*`, `media-use`, `threejs-*`, `scenario-blender-*`, `rea-video`, `polyfork`) are tracked in [`skills-lock.json`](skills-lock.json). Keep those upstream copies unchanged so updates apply cleanly; put project adaptations in `.agents/skills/shortform-production/` or `.agents/skills/shortform-board/`.

## Workspace Layout

```text
TRACKER.json          Shared registry of boards and productions (slug, status, stage, path only)
AGENTS.md             Agent operating rules, review gates, and tool routing
boards/<slug>/        Tracked reusable creative systems (DIRECTION.md, frame.md, EDITORIAL.md,
                      CONTRACT.json, ACCOUNTS.json, AUDIO.json, style-board.*, motion-preview.*)
productions/<slug>/   Episode workspaces with tracked editorial records and a composite storyboard PNG
references/           Local reference clips and _analysis/ outputs (gitignored)
.agents/skills/       Project-owned and upstream skills plus Python QA/audio/board scripts
```

Storage conventions that matter across runs:

- **`TRACKER.json` stays minimal.** Detailed choices, approvals, review notes, and next actions live inside `boards/<slug>/DIRECTION.md` or `productions/<slug>/EPISODE.md`.
- **Git keeps a lightweight episode archive.** The [production storage guide](.agents/skills/shortform-production/references/storage.md#git-archive) lists the tracked records and storyboard PNG. Composition files, individual stills, audio, exports, and reference clips stay outside Git.
- **HyperFrames initializes inside `productions/<slug>/video/`.** Keep `video/` empty before scaffolding and pass `--skip-skills` so the installed skill set stays intact. See [board files](.agents/skills/shortform-board/references/board-files.md) and [production storage](.agents/skills/shortform-production/references/storage.md).

## Running Productions

`shortform-production` accepts skill-prompt options (parsed in the prompt, not shell flags) to control board selection, topic discovery, review automation, stage caps, and external delivery:

```text
# Interactive production using a registered board (stops at human checkpoints, finishes at content_package)
shortform-production --board=di-balik-benda "How a mechanical stapler clinches a staple"

# Auto-discover 10 candidate topics, keep human hook selection, then automate through export + package
shortform-production --board=budidaya-di-halaman --topic=auto --automation=after-hook

# Stop after a specific stage (brief | research | script | storyboard | audio | production | verification | preview | export | content_package | publishing)
shortform-production --board=ruang-di-antara --until=storyboard "Topic..."

# Schedule to the board's inherited Trypost accounts after verified export + package
shortform-production --board=di-balik-benda --delivery=queue --at=2026-11-25T19:00:00+07:00
```

See [invocation options](.agents/skills/shortform-production/references/invocation.md) for option validation, delayed automation (`after-topic`, `after-hook`, `after-script`, `after-storyboard`), target overrides (`--channel`), and delivery precedence.

Every episode snapshots its board's `CONTRACT.json` at `brief` and passes the [quality gate](.agents/skills/shortform-production/references/quality-gate.md) (storyboard craft lint, headless DOM anti-slop & read-time checks, independent 7-dimension jury review, and audio/motion checks) at `storyboard`, `verification`, and `export`.

## Setup

1. **Environment variables:** Copy [`.env.example`](.env.example) to `.env` and fill in:
   - `ELEVENLABS_VOICE_ID` — workspace fallback voice ID. Voice resolution runs in order: episode override → `boards/<slug>/AUDIO.json` → root `.env`.
2. **Local CLI tools on `PATH`:**
   - **Python 3** — runs QA, storyboard/DOM lint, narration synthesis/alignment, and reference-comparison scripts.
   - **Node.js & HyperFrames CLI** — video scaffolding, preview, checks, and rendering.
   - **`ffmpeg` / `ffprobe`** — audio/video inspection, loudness measurement, and mixing.
   - **`@elevenlabs/cli`** — preferred transport for narration (`eleven_v4` with timestamps), optional SFX, and music generation (`elevenlabs auth status` to verify login, `elevenlabs auth login` to sign in).
   - **Playwright (optional, required when `craft.dom_lint` is enabled)** — powers `dom_lint.py` headless anti-slop and text read-time checks.
3. **Optional MCP integrations:**
   - **ElevenLabs MCP** — narration transport when the CLI is not signed in; single take only ([transport choice](.agents/skills/shortform-production/references/audio.md#choose-the-elevenlabs-transport)).
   - **Trypost Local** — drafts, queue scheduling, immediate publishing ([publishing](.agents/skills/shortform-production/references/publishing.md)), and published-episode metrics ([performance](.agents/skills/shortform-production/references/performance.md)).
   - **Web research, Context7, MarkItDown** — claim verification, current library/CLI docs, and document extraction during research.

## Verification and Tests

Run the offline regression suites (no external API calls):

```bash
python -m unittest discover -s .agents/skills/shortform-production/scripts -p "test_*.py"
python -m unittest discover -s .agents/skills/video-to-board/scripts -p "test_*.py"
```

Validate a board's or episode's production contract:

```bash
python .agents/skills/shortform-production/scripts/episode_qa.py --contract boards/<slug>
python .agents/skills/shortform-production/scripts/episode_qa.py --contract productions/<slug>
```
