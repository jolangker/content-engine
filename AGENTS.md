# Agent Guide

This workspace manages short-form content production. Use natural Indonesian when communicating with the user unless they request another language. Shared skills own the workflow; boards own niche, audience, account identity, and editorial and visual direction.

Write project documentation and agent instructions in English. Keep audience-facing scripts, captions, and narration in the language chosen for the production.

## Start from the current state

- Read [TRACKER.json](TRACKER.json), then the relevant board or production documents. Check the recorded status against existing files and the latest feedback before continuing.
- The tracker contains only `boards` and `productions`. Update the relevant entry after a stage transition or review outcome. Keep detailed content and feedback in production documents.
- Distinguish exploration, production requests, continuation, and revision. Work up to the endpoint the user requested.

## Choose the workflow

- To create, continue, or revise a production, read [shortform-production](.agents/skills/shortform-production/SKILL.md). It owns the production pipeline, `--board` selection, `--topic=auto` discovery, `--automation` execution policy, and optional external delivery.
- For Cloudinary hosting or asset reuse, read [cloudinary-mcp](.agents/skills/cloudinary-mcp/SKILL.md). For Buffer drafts, scheduling, publication, or posting-status reconciliation, read [buffer-mcp](.agents/skills/buffer-mcp/SKILL.md). Production-level handoffs and receipts follow shortform-production's [publishing contract](.agents/skills/shortform-production/references/publishing.md).
- For video or motion work, read [hyperframes](.agents/skills/hyperframes/SKILL.md) before choosing a workflow or starting production. Follow its routing, setup, and technical contracts; load domain skills as needed.
- To explore, create, continue, or revise a creative board, read [shortform-board](.agents/skills/shortform-board/SKILL.md). It owns concept exploration, style-board creation, editorial direction, and board review. It loads HyperFrames Creative as needed. Start episode production when requested.
- Project-local skills live in `.agents/skills/`. Store skills created specifically for this project there.

## Invocation without context

When the user invokes only the production skill:

First apply supplied options using the [invocation contract](.agents/skills/shortform-production/references/invocation.md). `--topic=auto` explicitly delegates selection: resolve the board and follow [automatic topic selection](.agents/skills/shortform-production/references/topic-selection.md), then begin one production. With no topic, target, or topic delegation, a context-free `--automation` invocation reports the missing target without creating artifacts. Otherwise, for a bare invocation:

1. Read the tracker and show unfinished productions, if any. Offer to continue one or start a new production; wait for the user's choice.
2. If there are no productions, ask which topic or source material they want to develop. Offer help finding ideas if needed.
3. Once production work is requested and the topic or material is clear enough to assign a slug, create the production folder and tracker entry, then begin the brief. Resolve the board and other information during intake as needed.

An initial discussion or invocation without context does not create folders, add production entries, or start media generation.

## Boards and storage

- Find boards in the tracker and read the documents at their registered paths. A board's framework and identity apply to productions that select it; a particular board name is not a universal skill default.
- Preserve the selected board when continuing a production unless the user explicitly changes it, including with `--board`. For a new production, follow the explicit choice; `--automation` delegates an unspecified choice under the invocation contract. Otherwise, if several candidates fit, recommend one with a reason and ask for a choice unless the user has delegated selection.
- Store all production-specific files in `productions/<slug>/`, including research, scripts, storyboards, assets, audio, compositions, and exports. Shared boards remain in `boards/`; the tracker remains at the root.
- Entry formats, slug rules, and production layouts are defined in [storage and state](.agents/skills/shortform-production/references/storage.md). Follow its `video/` subfolder rule so HyperFrames initialization does not conflict with preproduction files.

## Project review defaults

For a new production, pause by default after the script, visual storyboard, and final preview. Present a reviewable result, record `awaiting_review`, and wait for feedback before continuing to the next stage.

- `--automation` explicitly replaces these human checkpoints, including HyperFrames' final-look approval, with agent verification and delegated render authorization. The [invocation contract](.agents/skills/shortform-production/references/invocation.md) owns its persistence and scope. Keep quality checks; record no fabricated human approvals. External delivery still requires its selected endpoint and resolved target accounts.
- Requests such as "stop at the script" define the work's final endpoint. Review checkpoints define pauses within the pipeline.
- Explicit instructions such as "work straight through to the preview" may skip earlier checkpoints. Match the HyperFrames run shape to that instruction. Rendering follows the HyperFrames final-look gate unless the run explicitly delegates it through automation.
- "Approved" or "continue" accepts the result currently presented; it does not automatically remove later checkpoints. Honor existing approval for that version without asking again.
- Combine reviews of the same result with the HyperFrames workflow's checkpoints. Technical checks still apply when the user skips intermediate reviews.

## Research and documentation

- For factual claims or revised explanations, read [research and script](.agents/skills/shortform-production/references/research.md). Connect claims to sources and their limitations; distinguish creative references from supporting evidence.
- For voiceover synthesis, sound effects, BGM, or word alignment, read [audio generation](.agents/skills/shortform-production/references/audio.md).
- Use Tavily for web searches and current information. If it is unavailable or fails, use another search tool and mention the fallback.
- For libraries, frameworks, SDKs, APIs, CLIs, or cloud services, use Context7 first: call `resolve-library-id`, select the best match, then call `query-docs` with one concept per query. An explicit `/org/project` ID can be used directly. This covers syntax, configuration, setup, migration, and library-specific debugging; it is unnecessary for general programming concepts or business logic.

## Voiceover pipeline

- Use ElevenLabs with audio tags and model `eleven_v4`. Resolve the default voice from the project root `.env` key `ELEVENLABS_VOICE_ID` when preparing a new or explicitly regenerated narration request. This file is the source of truth for the default voice; inherited shell voice settings, examples, and historical episode choices do not override it. An explicit user-selected episode voice takes precedence and must be recorded with its reason. Missing voice configuration is an error, not a reason to pick a fallback.
- Set `provider`, `voice`, and `tts_model` explicitly in each audio request; see [audio generation](.agents/skills/shortform-production/references/audio.md). If generation fails, report the failure and retain these choices rather than switching provider, voice, or model automatically.
- Add delivery tags to suit the script and board; captions contain spoken words only. Preserve existing audio until its regeneration is requested or required by an authorized narration revision.
- Before paid synthesis, validate the resolved voice against the request. Reuse generated audio only when its recorded request fingerprint and audio/alignment hashes match; see the audio guide for the maintained synthesis entry point. Retain completed productions' original voice metadata as historical evidence.

## Understanding code

If the root contains `.codegraph/`, use CodeGraph before grep/find or reading code to understand symbols and execution paths: `codegraph_explore` when available, or `codegraph explore "<question or symbols>"`. Without `.codegraph/`, use ordinary search; creating an index is the user's decision.
