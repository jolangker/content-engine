# Automatic topic selection

Read for `--topic=auto` or an explicit instruction to choose the topic. This delegates one topic and angle for one production; [invocation](invocation.md) owns execution and delivery. A discussion about this option does not start production.

## Select before creating files

1. Resolve the board using the invocation contract and read its registered editorial and visual documents. Identify its subject scope, audience, pillars, sourcing rules, and duration/format constraints. With neither a suitable board nor explicit creative direction, report the missing basis; account availability is not a basis for choosing a niche.
2. Read production topics in `TRACKER.json` and inspect relevant `EPISODE.md`, `SCRIPT.md`, and content packages for likely overlaps, including unfinished work. Compare the audience question, central claim, scenario, and takeaway, not just titles. Exclude repetitions; use a related topic only when its new angle gives a materially different takeaway and record that distinction. Account for existing production folders missing from the tracker before creating a conflicting slug.
3. Build a small internal shortlist of distinct candidates. Compare board fit, usefulness to the intended audience, novelty against existing work, evidence availability, and feasibility within the board's format. Use the project's research workflow for source discovery when factual/current evidence affects viability. Keep source-backed findings separate from hypotheses; describe a topic as trending only with current evidence.
4. Select the strongest viable candidate without asking the user to pick from a menu. State the topic, angle, and a short reason in progress commentary, then continue. If evidence makes the lead candidate unsuitable, choose another before committing it. If no suitable candidate remains, report the concrete limitation instead of producing unsupported claims.
5. Once a supported direction is clear enough to name, assign a unique slug using [storage](storage.md), create the production folder and tracker row, and record the decision in `EPISODE.md`: `topic_selection: auto`, selected topic/angle, board revision, concise candidate comparison, overlap check, and evidence leads. Continue full claim verification in [research and script](research.md), retaining URLs and qualifications in `SOURCES.md`.

Selection is complete when one topic and angle fit the board, are meaningfully distinct from existing episodes, have a credible evidence path where needed, and are recorded in the new production. Topic discovery is intake, not a new root tracker stage. Source discovery supports selection; it does not replace full research.

## Continue the selected run

- `--topic=auto` delegates the topic decision; `--automation` separately removes later human review gates. Without automation, select the topic without a topic-picking pause, then follow the run's normal script/storyboard/preview review policy.
- For external delivery, preflight identity and available integrations before costly synthesis/render work. Resolve target channels only from the requested account or an established board mapping. Missing required access or account identity remains a blocker under the invocation contract; automatic topic selection does not authorize guessing a destination.
- Once the production exists, freeze its topic for that run. On interruption, resume the recorded production and earliest unfinished stage rather than discovering another topic. A clearly new invocation creates at most one new episode; it does not launch a recurring publisher or process the whole shortlist.
- If full research later invalidates the selected explanation, narrow or revise that episode's angle within the board and record the change. Preserve work and explain a broader topic replacement; a verified claim is not inferred from a topic's initial feasibility.
