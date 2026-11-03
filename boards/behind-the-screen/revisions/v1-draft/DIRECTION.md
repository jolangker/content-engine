# Behind the Screen — draft v1

Status: `awaiting_review`. Created 2026-11-03 after the user selected this concept from the international niche research with “boleh kita coba board Behind the Screen”. This authorizes development of a reviewable draft; the visual and editorial package has not yet been accepted.

## Purpose and selected concept

English-language vertical explainers for people who use digital services every day and want to understand an unexpected result. Proposed initial audience: non-specialist adults in the US, UK, Canada and Australia. These are positioning choices, not measured audience demographics.

Audience promise: **Understand what happens behind your everyday clicks.**

The selected concept follows a familiar action through the hidden process and returns to the visible result. The viewer should finish able to explain one causal relationship, with the relevant limit or exception. This extends the project's explanatory craft into digital systems while giving the new board its own identity.

## Proposed package

- [EDITORIAL.md](EDITORIAL.md): scope, pillars, narration, story structure, sourcing and topic candidates.
- [frame.md](frame.md): canonical visual tokens, framing, captions and conceptual motion/audio.
- [DESIGN-PHILOSOPHY.md](DESIGN-PHILOSOPHY.md): the rationale for the visual medium and initial plan critique.
- `style-board.html` / `style-board.png`: editable direction sheet and inspected export.
- `studies/`: three independent original SVG compositions and their 1080 × 1920 PNG exports: passkey sign-in, private-browsing boundaries, and a CDN cache hit. They are composition studies, not a three-scene episode or completed scripts.
- [assets/SOURCES.md](assets/SOURCES.md): font provenance and source boundaries for illustrative claims.
- [VERIFICATION.md](VERIFICATION.md): export and visual review findings.
- [ACCOUNTS.json](ACCOUNTS.json): no accounts selected; no targets inferred from other boards.
- [AUDIO.json](AUDIO.json): narration voice undecided; `null` inherits the root environment default when an authorized production resolves audio.

## Proposed visual direction

**Open interfaces:** familiar screens become opaque illustrated planes that separate to expose a specific relationship. Blue paths carry requests or responses; teal marks a resolved state; amber identifies an input or unresolved step. Spatial boundaries make local and remote processes distinguishable. Nothing is a literal view inside a real application unless verified and identified.

Pale lilac ground, white interface surfaces, deep aubergine ink, cobalt transit, teal resolution and amber input. Bricolage Grotesque Bold gives the question a human voice; Instrument Sans Regular/Bold carries UI, annotations and captions. The subject's interface rectangles, boundaries and routing paths provide the forms. No pre-existing account, artist or brand style is copied.

The subject-grounded plan replaces an initial generic technology aesthetic with legible screens, route direction and explicit boundaries. The three studies intentionally vary their composition: a local/remote exchange, a boundary comparison, and a spatial delivery route. Details are in the design philosophy and canonical frame specification.

## Evidence and interpretation

The earlier Reddit discussion supplied audience questions, not proof of technical behavior or market size. Factual anchors for these static studies were read from FIDO Alliance, Google Chrome Help and Cloudflare Learning Center; see assets/SOURCES.md. No Reddit comment is used as a technical authority. UI and route diagrams are original explanatory abstractions.

Product/version differences, sync/recovery behavior, privacy exceptions and routing conditions must be reverified in episode research. The passkey study concerns local biometric verification, not a claim that every private key is device-bound. The private-browsing study is scoped to Chrome Incognito after all Incognito windows close; downloads and bookmarks are separate exceptions. The CDN study assumes an available cached copy and does not promise the geographically nearest server or universal caching.

## Review and next action

- Concept: selected by the user on 2026-11-03.
- Editorial and visual v1: proposed; no approval of unseen artifacts inferred.
- Motion/audio: conceptual only. No narration, music, animation or episode is generated.
- Current phase: static visual and editorial v1 package complete and verified, awaiting user feedback. The delivered board image is 1800 × 2505; each independent vertical study is 1080 × 1920.
- Agent review: inspected the full direction sheet, each native-size study, the three studies at 384px width, and a headline-hidden diagram comparison. Separated the local verification compartment, anchored the signed-proof leader to its route, and interrupted the inactive cache path around its label. All final fonts loaded; no out-of-frame text, HTML overflow or browser errors were reported. See VERIFICATION.md.
- Next action: present the visual and editorial draft together, then incorporate the user's feedback.
- Preview lifecycle: use local files and a short-lived headless browser for export. No temporary preview server is required.
