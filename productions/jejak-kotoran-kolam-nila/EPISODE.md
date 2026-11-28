# Jejak Kotoran di Kolam Nila

## Brief

- `topic_selection: user`. On 2026-11-21 the user replied “setuju” to the recommended first candidate, following one piece of fish waste from a backyard Nile tilapia tank to a settling chamber. The board was explicitly selected at invocation.
- Board: `budidaya-di-halaman`, revision 1, draft. Inherit its [direction](../../boards/budidaya-di-halaman/DIRECTION.md), [editorial guide](../../boards/budidaya-di-halaman/EDITORIAL.md), and [frame specification](../../boards/budidaya-di-halaman/frame.md).
- Angle: start with a visible settling particle near the bottom outlet, follow it into a settling chamber, and reveal the separate route that brings circulating water back. Use the pump on the return side and gravity flow into the chamber. See [sources and scope](SOURCES.md).
- Editorial comparison: the competing shortlist angles on feeding distribution and morning surface behavior offer useful observations. Following a single particle makes the selected question readable as one continuous route and gives the wide yard reveal a concrete payoff. The board's pond study covers rainwater overflow. The published toilet-cistern episode covers a float valve and domestic water levels. Neither explains the separation of settleable fish waste from a recirculating stream. Checked the tracker and production directories for overlap.
- Defaults inferred from the board: 9:16 educational animation, 1080 × 1920 and about 55–60 seconds, for Indonesian-speaking general viewers. Use a yard-scale cutaway with an illustrative grow-out tank rather than an earthen pond. Keep the focal particle readable across scale changes and preserve the board's caption treatment. Use a warm Indonesian narration with the inherited default voice policy, a quiet instrumental bed, and timed water or valve cues if the approved scene plan calls for them.
- `execution_policy: human_review`. Retain the hook, script, visual storyboard, and final preview checkpoints. `endpoint: content_package`. `delivery: package`.

## Publishing targets

```yaml
publishing_targets:
  source: board
  board_accounts_file: boards/budidaya-di-halaman/ACCOUNTS.json
  board_accounts_sha256: a755eaf48dcdc490d71b1043e905bc0ac2cd14ef37164f98d6f97d16ac2a5461
  accounts: []
```

## Research and hook review

Research checked which solids settle, the documented flow order, and the limits of the settling step. [SOURCES.md](SOURCES.md) records the findings and the illustration limits. The idea originally described a particle sucked through a pump. In the chosen illustrated system, the particle travels through the bottom pipe into the settler before the pump returns water to the tank. The primary visual payoff is the same particle stopping in the settler while the return flow continues.

Hook review v2. The user requested an opening that begins with “Kalau kamu…”.

1. **Follow a particle** — “Kalau kamu lihat kotoran nila ini masuk pipa, coba tebak. Pas airnya balik ke kolam, dia ikut nggak?” The opening follows the marked particle into the pipe. The payoff locates it at the bottom of the settling chamber.
2. **Start with the practical problem** — “Kalau kamu bikin air kolam muter terus, gimana caranya biar kotorannya bisa ngumpul di satu tempat?” The opening shows recirculation first. The payoff reveals the chamber as a place where settleable solids can collect.
3. **Show the split first** — “Kalau kamu intip bak ini dari samping, airnya keluar di atas, tapi kotorannya ngumpul di bawah. Kok bisa?” The opening shows the outlet and the deposited solids in one cutaway. The payoff explains why particles have time to sink there.

Recommendation: option 1. It places the opening action at the pipe and gives the viewer one object to track through the later reveal.

`hook_selection: user`. Interpreted “cocok” immediately following the revised recommendation as acceptance of hook 1 in v2. Its wording is carried into script v1 verbatim.

## Script review

[Script v1](SCRIPT.md) uses six narration beats and an estimated 58-second duration. It shows the fast-flow comparison before revealing the baffle, then closes the return loop and answers where the tracked particle goes. The claim check follows the research boundaries for settleable versus suspended solids, downstream treatment, and the documented sludge outlet. The visual comparison and time compression are schematic. Estimated timing will be verified with actual narration after storyboard review.

`stage: script`, `status: awaiting_review`, `next_action: review script v1`. Human script approval pending.
