# Bikin Kebun Kentang dalam Pot

## Brief

- Board [Budidaya di Halaman](../../boards/budidaya-di-halaman/DIRECTION.md), revision 4. Inherit [editorial v4](../../boards/budidaya-di-halaman/EDITORIAL.md), [visual v1](../../boards/budidaya-di-halaman/frame.md), and Pribs narration.
- Direct request `--board=budidaya-di-halaman --topic=auto --until=export --automation`. Automation active at intake. Topic, hooks, script, storyboard and final look are evaluated by the agent. The run authorizes a local export.
- `publishing_targets: []`, inherited from the board [accounts file](../../boards/budidaya-di-halaman/ACCOUNTS.json). `delivery: package` default with `until: export` taking precedence. No schedule.
- Indonesian second-person explainer for a general audience. 1080 × 1920, 30 fps, with a 90-second minimum. Target 100–115 seconds depending on measured delivery. Illustrated clay and green backyard set. Conversational narration and action-linked SFX. BGM none.
- Show an illustrative build of a whole opaque container system for one seed potato plant in suitable local conditions. Compress elapsed growing time. Focus on drainage, covering developing tubers, watering beneath the foliage, and one illustrative mature harvest.

## Delegated topic selection

| Candidate | Starting point → first use → changes → first result |
| --- | --- |
| 1. Kebun kentang dalam pot | Empty yard corner and solid tub → plant a seed tuber → open drainage, add mix around stems, check water below a full canopy → tip onto a mat to reveal the first harvest. |
| 2. Kolam lele terpal | Bare plot → test a lined pond → repair a leaking fitting and reroute rainfall overflow → working rain-ready pond. This echoes the board's worked example. |
| 3. Bak daphnia | Empty shallow tub → establish a starter culture → adjust shade and separate a harvest from the starter stock → collect a small live-feed sample. |
| 4. Bak benih ikan dengan hapa | Empty pond corner → hang a fine-mesh nursery → correct slack at the bottom and secure edges → show stock held in an accessible nursery. |
| 5. Kebun kacang rambat dalam pot | Empty patio → sow beans → add a trellis as stems reach and improve access to the shaded side → pick the first pods. |
| 6. Bedeng wortel dalam kotak dalam | Bare compact yard → sow a box of loose mix → thin crowding and expose a sample root in section → pull the first usable carrots. |
| 7. Rumah jamur tiram kecil | Empty shelf → place a ready colonized edible grow block → address drying and airflow → harvest a first flush in a suitable climate. |
| 8. Kebun stroberi dalam talang | Bare fence → mount a drained trough and plant plugs → adjust irrigation distribution and raise trailing fruit → collect ripe berries. |
| 9. Kebun ubi jalar dalam karung | Empty yard corner → establish slips in a drained sack → train spilling vines and tend the growing medium → empty the first sack. |
| 10. Bedeng kangkung jaring serangga | Bare plot → establish the bed and sow → install hoops and secure the cover after observed leaf damage → harvest a usable bunch. |

- `topic_selection: auto`. Selected candidate 1. Repeated visible interventions and the opaque-pot reveal give the same object a distinct role in the opening, middle and payoff. Candidate 2 is visually strong but adjacent to the board example and existing pond episodes. Candidates 3 and 4 would need narrower operating assumptions. Candidate 9 has a similar reveal and is reserved.
- Overlap checked across tracker and production folders. Nila follows solids, maggot follows selective harvest, and aquaponics establishes a fish-fed recirculating bed. Selada uses a wick and reservoir to supply water. This potato build instead drains water from an opaque container and ends with an underground-tuber harvest.
- Research questions covered in [SOURCES.md](SOURCES.md). Use the sequence drainage test → seed tuber planted → shoots emerge → add medium around stems → check moisture under leaves → water to bottom drainage → foliage dies back → tip pot and inspect harvest.

## Hook options

1. “Kalau kamu mau bikin kebun kentang di halaman, mulai dari pot kosong ini. Balik dulu potnya. Tempat keluarnya air ada di dasar.” Begins with the action needed to make the vessel work and opens a visual question the water test answers. **Selected by delegated automation.**
2. “Kalau kamu mau panen kentang dari satu pot, siapkan dulu wadah yang dindingnya rapat dan nggak tembus cahaya.” Leads with the harvest and gives the opaque wall a later payoff.
3. “Kalau kamu mau nanam kentang di pot, sisain ruang di atas media sejak awal. Ruang itu bakal kamu pakai lagi setelah daunnya tumbuh.” Leads with a future use of the pot, paid off in the hilling shot.

## Script review

The narrator addresses one builder, who stays the actor throughout. The narration begins with a physical action, follows an empty pot through first harvest, and closes with a congratulation and next-build question. Short clauses follow observed changes. The covered-tuber illustration is a transparency view of one opaque vessel. Growing stages are time-compressed and harvest size is illustrative.

## State

Script verified under delegated review. Next action is the visual storyboard and static poses.
## Storyboard review

Nine editable poses verified in order in video/boards/storyboard.html and its full 1760 × 1844 PNG. All nine stills are 1080 × 1920. Browser verification found zero missing images, text clipping or load errors. Reviewed the same yard across the full sheet, using the overhead canopy shot and linked drainage cuts for layout rhythm. Corrected the harvest vessel mouth to face its landing mat and aligned the final pot with its ground shadow. Re-captured the affected frames. Accepted by delegated automation. The next stage is measured speech and sound placement.

## Narration and assembly

ElevenLabs MCP generation 6FkxiPLYE0FSBiuvw9eP is the single Pribs / eleven_v4 take. Original 100.08 s audio imported with verified SHA and 262 measured Whisper tokens. Three hyphenated words combined two token intervals each. The normalized placed narration, 62 short caption phrases, four scene-linked contact and movement effects, and all nine scene starts share the 30 fps clock. Eight narration seams passed the decoded-sample preflight. The planned film length is 103.233333 s. HyperFrames checks and final look are in progress.

## Managed preview

Production-owned preview for video/ at http://127.0.0.1:3002/#project/video, PID 3880, port 3002. Started by this run after checking that the project had no preview. Retain during final inspection and render, then release and verify listener cleanup.

## Final state

Export complete, delegated automation. [MP4](exports/kentang-dalam-pot.mp4), [SRT](exports/kentang-dalam-pot.srt), and [1080 × 1920 cover](exports/kentang-dalam-pot-cover.png). The verified film is 103.233333 s and 3,097 frames at 1080 × 1920, 30 fps, with H.264 and AAC. [Encoded verification and creative review](video/REVIEW.md). The final preview used the same composition as the render. Verification includes full decode, nine decoded proof frames, eight acoustic cuts, and four matched sound effects. Direct listening was unavailable. The preview for video/ was stopped and not-running status and release of PID 3880's port 3002 were confirmed. Stage export, status complete, next action none.
