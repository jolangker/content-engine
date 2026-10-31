---
name: board-export
description: Export a creative board as a standalone, tool-agnostic creative-direction package with portable visual references. Use when handing off a board's concept, art direction, design language, and storytelling principles to another agent or designer.
---

# Board Export

Turn a board into a portable creative-direction package that another agent or designer can apply without access to the source project. The deliverable is a folder of Markdown guidance and visual references, readable without skill installation or discovery. Preserve the reasoning behind the look as well as its visible attributes.

## Establish the source and destination

For discussion, explain the proposed extraction in conversation. Create files when the user requests a board export. Identify the board, revision, requested scope, and output location from the request and available context. Resolve an ambiguous board selection before extracting it.

In this workspace, read `TRACKER.json` and the selected board's `DIRECTION.md` to locate its active package and latest decisions. Other workspaces may supply a board folder, images, or documents directly; the local filenames are discovery hints, not requirements for using this skill.

Export to `exports/<board-slug>-creative-direction/` unless the user specifies another destination. Keep source boards and their approval state unchanged. Updating an existing package requires inspecting its contents and preserving unrelated user edits.

## Extract the creative system

Read [extraction guidance](references/extraction.md) when performing an extraction. Inspect the current direction, visual specification, editorial guidance, relevant motion/audio guidance, and actual visual artifacts. Read only the assets and history needed to establish the selected revision; archived studies are not the active direction.

Capture concept, audience experience, art direction, color semantics, typography, composition, visual primitives, storytelling, and applicable motion/audio intent. Preserve specific creative constraints and explain their purpose. Separate accepted decisions, adaptable defaults, observations, and unresolved matters.

Translate implementation details into observable creative behavior. Preserve an intentional 2.5D illustration lock even when the original implementation used SVG. Describe causal motion, readable holds, and framing rather than prescribing a timeline library. Keep original canvas measurements as reference measurements with scaling guidance.

Extract the board's actual direction. Do not fill unspecified fields with house-style defaults or silently redesign it. If only images are available, label inferred principles as observations and leave unobservable motion, audio, editorial intent, and approval unknown.

## Package the handoff

Use [package guidance](references/package.md) for the output structure and consumer instructions. Write agent instructions in English; preserve original names and clearly marked illustrative copy in their source language.

The exported folder must carry all instructions and required visual references. Use relative links within the folder. Include redistributable assets and their licenses when needed; describe a fallback for unavailable or nonredistributable resources. Retain required audience-facing identity, while excluding publishing account IDs, credentials, and delivery configuration.

Use `README.md` as the consumer entrypoint, linking to `CREATIVE-DIRECTION.md` and the bundled visual references. Explain the creative identity and intended use, how to adapt it to the requested deliverable, and how to assess fidelity. Let the consumer choose tools. The package must work without this extractor, a skill loader, other project skills, a specific renderer, a project tracker, or the source board folder. Add a skill wrapper only when explicitly requested.

Export a snapshot of the selected source revision. Record source evidence and any uncertainty inside the package. Future source changes require a requested refresh; they do not silently change the package.

## Verify and deliver

- Follow every internal file link and check that required references and assets are present inside the exported folder. Record external resources as optional or unresolved dependencies rather than claiming self-containment.
- Search the output for absolute local paths, parent links escaping the folder, renderer commands, tool-specific APIs, project-only references, operational account data, and inherited workflow gates. Remove or translate required runtime dependencies; a renderer name in a historical provenance note is harmless.
- Compare the extracted rules with the selected source revision and inspected visuals. Check exact tokens, creative exclusions, required versus advisory numbers, and approval scope. Resolve contradictions through evidence or disclose them.
- Simulate a consumer with only the exported folder: can it understand the concept, make a representative composition, explain its choices, and review fidelity without retrieving the original board? Treat this as a reasoning check unless an artifact was actually produced.
- Check that `README.md` provides a usable entrypoint and that the creative direction and required references are complete. Structural validation does not establish visual fidelity or cross-agent execution.

Deliver the package path and its `README.md`, extraction scope, and material limits. Report actual verification performed. Exporting the package does not generate a production, render media, install a skill, or publish anything unless requested.
