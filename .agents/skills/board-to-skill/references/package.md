# Portable skill package

Use the smallest folder that carries the actual creative system. A typical export is:

```text
<board-slug>-creative-direction/
  SKILL.md
  references/
    creative-direction.md
    provenance.md
  assets/
    style-board.png
    ...additional necessary references or licensed assets
```

The entrypoint and creative direction are required. Keep provenance separate when its evidence would otherwise distract the consumer; a short evidence note can live in the creative direction. Add only assets actually used by the instructions. Avoid empty directories and unfinished template fields.

## Consumer entrypoint

Write a short `SKILL.md` with valid YAML `name` and `description`. Use a lowercase hyphenated name under 64 characters. The description identifies the board's characteristic treatment and the tasks for which to apply it, rather than advertising generic design capability.

The body should provide these behaviors in concrete terms:

1. Read the linked creative direction and inspect its bundled visual references before designing.
2. Apply the user's requested task and deliverable using available tools. Carry the board's accepted identity, purpose, and constraints into the result.
3. Distinguish creative invariants, adaptable defaults, and constraints specific to the original format. Keep fixed values when applicable; explain changes needed for an explicitly requested adaptation.
4. Choose composition and content through the board's decision logic. Use reference studies as examples, with new material appropriate to the task.
5. Review the actual deliverable against the direction's observable fidelity criteria. Verify motion or sound through playback when those properties are part of the deliverable; static references establish appearance and planned behavior only.
6. Report the result and material deviations or verification limits.

Use plain instructions and relative Markdown links that any agent with filesystem access can read. Tool-specific UI metadata is optional and must not carry essential instructions. Agents without a skill loader can be given `SKILL.md` directly; whether a host auto-discovers the folder depends on that host.

## Creative direction

Organize only the sections supported by the source. Useful contents are:

- **Identity and purpose:** name, concept, audience experience, creative promise, intended scope.
- **Art direction:** medium, volume, material, light, texture, realism, and characteristic exclusions.
- **Design language:** exact palette with semantic roles; typography families, weights and roles; primitives; grouping, hierarchy, whitespace, scale and annotations.
- **Composition:** reading priorities, reference measurements and canvas, adaptation rules, identity placement, legibility and safe areas.
- **Story and voice:** reusable progression, viewpoint, rhetorical choices, language and content integrity where these affect the creative result.
- **Motion and sound:** how change communicates meaning, state continuity, attention, holds, event relationships and delivery character. Mark conceptual properties accurately.
- **Source format:** duration, aspect ratio, scene structure and other genuine format requirements, each distinguished from a recommendation or example.
- **Fidelity review:** source-specific observable checks and characteristic failure modes, with links to the relevant bundled studies.

Keep hard creative constraints visibly distinct from adjustable guidance. Preserve units and reference conditions for numbers. Leave unsupported decisions open rather than inventing fallback requirements.

Include at least one short, source-grounded application example when it clarifies how the direction makes decisions. Label it illustrative and avoid introducing unsupported real-world claims. The examples should exercise the concept, not merely describe its aesthetic with adjectives.

## Provenance

Record the source board identity, selected revision per layer, extraction date, approval scope, inspected artifacts, and unresolved conflicts or limitations. For material decisions, provide a compact mapping to their source and status. Include a brief record of which implementation details were translated or omitted.

List included assets with their provenance and license status where applicable. Keep operational account configuration and secrets out of the package. The package is a fixed snapshot; source paths and URLs are optional audit locators, not dependencies the consumer must fetch.

## Relocation check

Evaluate the package as if its folder had been copied to another machine with no source repository. Every required instruction, example, image and permitted asset must remain reachable inside it. Treat unavailable fonts, optional external references and unverified properties explicitly. Do not claim a live cross-agent test merely because the Markdown was reviewed.
