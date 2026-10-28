# Agent Guide

This workspace manages short-form content production. Communicate in natural Indonesian unless the user requests another language. Write project documentation and agent instructions in English; scripts, captions, and narration use the production's chosen language.

## Workflow ownership

- [shortform-board](.agents/skills/shortform-board/SKILL.md) owns reusable editorial and visual direction, static style boards, board review, and account configuration.
- [video-to-board](.agents/skills/video-to-board/SKILL.md) owns reference-video analysis and vision alignment for new boards, with one approval gate before board creation; shortform-board owns the resulting package.
- [shortform-production](.agents/skills/shortform-production/SKILL.md) owns episode intake, stages, revisions, reviews, packaging, and delivery. Read [invocation](.agents/skills/shortform-production/references/invocation.md) for options, topic delegation, automation, stage caps, or saved execution policies.
- The project-local [hyperframes](.agents/skills/hyperframes/SKILL.md) consolidated contract owns video authoring. Its task references and local `hyperframes-cli`, `hyperframes-registry`, and `media-use` skills own technical execution. Load references for the current operation; its compatibility reference lists the historical inputs still read by production scripts.
- [motion-graphics](.agents/skills/motion-graphics/SKILL.md) specializes in kinetic type, data, maps, and overlays within an assigned scene, inheriting the production's style, timing, audio, and review policy.
- [trypost-mcp](.agents/skills/trypost-mcp/SKILL.md) owns external draft, scheduling, publication, and status operations, with direct local-media upload. Production handoffs follow [publishing](.agents/skills/shortform-production/references/publishing.md).
- Project-specific skills belong in `.agents/skills/`.

## State and storage

Read [TRACKER.json](TRACKER.json), then the relevant board or production documents and latest feedback. Verify the files support their recorded state. The tracker contains only `boards` and `productions`; update the relevant entry after a stage transition or review. Detailed choices, feedback, and next actions belong in `DIRECTION.md` or `EPISODE.md`.

Discussion and context-free invocation stay in conversation until a concrete board direction or production is requested. The production skill owns bare-invocation intake and overlap checks.

- Boards live at their registered paths under `boards/`. Their identity and sourcing rules apply only to productions selecting them.
- Production-specific files belong in `productions/<slug>/`. Initialize HyperFrames in its initially empty `video/` subfolder; resume existing layouts in place. See [storage](.agents/skills/shortform-production/references/storage.md).
- Preserve the recorded board on continuation unless the user changes it. For a new production, use an explicit/delegated choice or sufficient direct guidance; resolve a material missing direction before building.
- Board `ACCOUNTS.json` stores default account identities; new productions inherit the full list unless overridden. Continuations retain saved targets. See [board accounts](.agents/skills/shortform-board/references/board-files.md#publishing-accounts) and [target inheritance](.agents/skills/shortform-production/references/publishing.md#target-inheritance). Account configuration alone authorizes no delivery.

## Review and verification

Use the production skill's hook, script, visual-storyboard, and final-preview checkpoints. [Invocation](.agents/skills/shortform-production/references/invocation.md#automation-and-review) owns automation activation, persistence, render authorization, and endpoint conflicts. Approval accepts the presented version; it does not waive later checkpoints. Combine reviews of the same result across skills and retain technical/creative verification under automation.

Before starting/resuming a preview or temporary server, and before ending its work, follow [preview lifecycle](.agents/skills/shortform-production/references/preview.md) for ownership, reuse, review holds, and verified cleanup.

## Research and audio

- For factual claims, script development, or revised explanations, use [research and script](.agents/skills/shortform-production/references/research.md). Keep supporting evidence separate from creative references.
- Use Jina for internet research and read selected source bodies. Use Context7 first for current library, framework, SDK, API, CLI, and cloud-service documentation: resolve the library, then query one concept at a time. General refactoring and business-logic debugging use ordinary code inspection.
- For narration, BGM, SFX, or alignment, use [audio generation](.agents/skills/shortform-production/references/audio.md). Narration uses explicit ElevenLabs `eleven_v4`, delivery tags, and the root `.env` `ELEVENLABS_VOICE_ID` unless the user explicitly selects an episode voice. The maintained `narration.py` entry point validates provenance and cache reuse; retain provider/voice/model on failure and preserve completed audio until authorized regeneration. SFX prioritize the existing media-use library under that contract.

## Understanding code

If the root contains `.codegraph/`, use `codegraph_explore` or `codegraph explore "<question or symbols>"` before text search or code reads to understand symbols and execution paths. Otherwise use ordinary search; creating an index is the user's decision.
