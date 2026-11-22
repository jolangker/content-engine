# Agent Guide

This workspace manages short-form content production. Communicate in natural Indonesian unless the user requests another language. Write project documentation and agent instructions in English; scripts, captions, and narration use the production's chosen language.

## Workflow ownership

- [shortform-board](.agents/skills/shortform-board/SKILL.md) owns reusable editorial and visual direction, static style boards, playable motion previews, production contracts, board review, and account configuration. New visual directions and board revamps use its [visual craft guidance](.agents/skills/shortform-board/references/visual-craft.md).
- [video-to-board](.agents/skills/video-to-board/SKILL.md) uses [rea-video](.agents/skills/rea-video/SKILL.md) to analyze references, then presents a board vision for approval. The resulting package follows `shortform-board`.
- [shortform-production](.agents/skills/shortform-production/SKILL.md) owns episode intake, stages, revisions, reviews, packaging, and delivery. Read [invocation](.agents/skills/shortform-production/references/invocation.md) for options, topic delegation, automation, stage caps, or saved execution policies.
- The project-local [hyperframes](.agents/skills/hyperframes/SKILL.md) consolidated contract owns video authoring, including kinetic type, data, maps, and overlays. Its task references and local `hyperframes-cli`, `hyperframes-registry`, and `media-use` skills own technical execution. Load references for the current operation.
- External draft, scheduling, publication, and status operations follow the production's [publishing contract](.agents/skills/shortform-production/references/publishing.md) using available provider tools. Insights on published episodes follow its [performance review](.agents/skills/shortform-production/references/performance.md).
- Project-specific skills belong in `.agents/skills/`.

Keep installed HyperFrames skills (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, and `media-use`) unchanged so upstream updates can replace them safely. Put project-specific workflow, review, and presentation adaptations in `shortform-production` and its references, and pass them as run context when using HyperFrames.

Resolve skill handoffs against the current session catalog and existing `SKILL.md` files. Use the installed HyperFrames task references for video work and the board's visual-craft guidance for static studies when an upstream route has no installed skill. Preserve the installed skill set during production setup; missing optional routes do not authorize installation.

For 3D scene planning, authoring, revisions, or board studies, read [Three.js integration](.agents/skills/shortform-production/references/threejs.md) before using the installed `threejs-*` craft skills. It owns project adaptation and dependency provenance; keep those upstream copies unchanged as well.

## State and storage

Read [TRACKER.json](TRACKER.json), then the relevant board or production documents and latest feedback. Verify the files support their recorded state. The tracker contains only `boards` and `productions`; update the relevant entry after a stage transition or review. Detailed choices, feedback, and next actions belong in `DIRECTION.md` or `EPISODE.md`.

Discussion and context-free invocation stay in conversation until a concrete board direction or production is requested. The production skill owns bare-invocation intake and overlap checks.

- Boards live at their registered paths under `boards/`. Their identity and sourcing rules apply only to productions selecting them.
- Production-specific files belong in `productions/<slug>/`. Initialize HyperFrames in its initially empty `video/` subfolder; resume existing layouts in place. See [storage](.agents/skills/shortform-production/references/storage.md).
- Preserve the recorded board on continuation unless the user changes it. For a new production, use an explicit/delegated choice or sufficient direct guidance; resolve a material missing direction before building.
- Board `ACCOUNTS.json` stores default account identities; new productions inherit the full list unless overridden. Continuations retain saved targets. See [board accounts](.agents/skills/shortform-board/references/board-files.md#publishing-accounts) and [target inheritance](.agents/skills/shortform-production/references/publishing.md#target-inheritance). Account configuration alone authorizes no delivery.

## Review and verification

Use the production skill's hook, script, visual-storyboard, and final-preview checkpoints. [Invocation](.agents/skills/shortform-production/references/invocation.md#automation-and-review) owns automation activation, persistence, render authorization, and endpoint conflicts. Approval accepts the presented version; it does not waive later checkpoints. Combine reviews of the same result across skills and retain technical/creative verification under automation. Every production passes the production skill's [quality gate](.agents/skills/shortform-production/references/quality-gate.md) against its board contract at storyboard, verification and export, and a reviewer other than its author reviews the film before the delivery render.

Before starting/resuming a preview or temporary server, and before ending its work, follow [preview lifecycle](.agents/skills/shortform-production/references/preview.md) for ownership, reuse, review holds, and verified cleanup.

## Research and audio

- For factual claims, hook/script writing or revisions, and revised explanations, use [research and script](.agents/skills/shortform-production/references/research.md). Hook and script work uses that skill's [hook and script craft](.agents/skills/shortform-production/references/script-craft.md) as its writing guide. Keep supporting evidence separate from creative references.
- Use SearXNG MCP for internet search and page reading, and read selected source bodies. Use Context7 first for current library, framework, SDK, API, CLI, and cloud-service documentation: resolve the library, then query one concept at a time. Use MarkItDown MCP for document text extraction. General refactoring and business-logic debugging use ordinary code inspection.
- For narration, BGM, SFX, or alignment, use [audio generation](.agents/skills/shortform-production/references/audio.md). Generate narration through the connected ElevenLabs MCP with explicit `eleven_v4`, delivery tags, and board-aware voice resolution. `narration.py` prepares MCP calls, imports completed audio and timing, and validates provenance/cache reuse; it makes no direct SDK/REST calls. MCP owns authentication; root `.env` supplies only the default voice ID. Preserve completed audio until authorized regeneration. SFX prioritize the existing media-use library under that contract.

## Understanding code

If the root contains `.codegraph/`, use `codegraph_explore` or `codegraph explore "<question or symbols>"` before text search or code reads to understand symbols and execution paths. Otherwise use ordinary search; creating an index is the user's decision.
