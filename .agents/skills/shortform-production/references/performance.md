# Performance review

Read when the user asks for insights, analytics or what is working on a board, before topic discovery on a board with published episodes, and when a publishing run completes. Published results are the evidence of what viewers respond to; this reference keeps them where topic and hook choices can use them. A review writes to the board's `insights/` folder and starts no production.

## Pull a snapshot

1. Resolve the board and its accounts from `ACCOUNTS.json`. List the board's productions whose `PUBLISHING.json` records a scheduled or published post, and confirm each post's live status with the provider.
2. Discover the connected provider's analytics tools and read each published post's metrics. Record what the provider returns: views or plays, reach, average watch time, completion or retention where offered, likes, comments, saves, shares, follows, and the time each metric was read. With no analytics tool connected, ask the user for the platform's insight numbers per post and record them as user-supplied.
3. Save `boards/<slug>/insights/<YYYY-MM-DD>/snapshot.json` as UTF-8 JSON with two-space indentation: `schema_version: 1`, `pulled_at`, `source`, and one entry per post with the production slug, account, post ID, `published_at`, its age in hours at reading, and the metrics. A metric the source did not give stays `null`.
4. Compare posts at comparable ages: 24 hours, 72 hours, 7 days. List a post younger than the comparison age and leave it out of the ranking.

## Read it against the episodes

Write `ANALYSIS.md` beside the snapshot. For each ranked post record, from its production files, the topic pillar, the hook's mechanism and first-sentence seconds, the duration, and its gate measurements where they exist. Then state:

- which topics, hook mechanisms and durations sit at the top and at the bottom, with their numbers;
- what the sample cannot show: few posts, different ages, a change of account or posting time;
- at most three experiments worth running next, each naming the one thing it changes.

A finding is provisional until a later snapshot repeats it. A proposed change to a board's rules is an experiment for the user to accept under the board's revision policy; record it in the board's `DIRECTION.md` as unapproved until then, and link the dated analysis from there.

## Use it

- Topic discovery reads the board's latest `ANALYSIS.md`: place each shortlisted topic against the best and worst performers, and let the recommendation cite the comparison.
- Each hook option names its mechanism and what the latest analysis shows for or against it.
- When a publishing run completes, record `next_action: performance snapshot after <the date seven days out>` in `EPISODE.md`.
