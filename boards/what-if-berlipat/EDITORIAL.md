# What If It Doubled: editorial framework

Editorial revision 1, approved on 2026-11-22. Working name: What If Berlipat. It applies to productions that select this board.

## Purpose and audience

One ordinary object. Its count doubles every day. The film follows the real arithmetic until the scale is absurd, and shows it rather than explains it.

- Audience: general viewers worldwide, United States first. No prior knowledge, no local references.
- Experience: "look at this". The viewer should want to send it to someone. The film does not ask a question, pick a fight, or invite corrections, and has no call to comment.
- Language: English first. An Indonesian version is made only when the user asks for it for a given episode: a second upload of the same film with translated on-screen text. Numbers, days and comparators stay identical between versions.
- Platforms: YouTube Shorts and Facebook Reels are the monetised targets. TikTok is for reach. One 1080 x 1920 master serves all three; safe zones are in [frame.md](frame.md#framing).
- Runtime: 20 to 40 seconds. Never under 10 seconds.

## Format rules

1. **Hook, 0 to 2 s.** The question is on screen in the first frame with the single object: "What if the rice on your plate doubled every day?" It names the object and where it normally lives. No title card, no channel intro.
2. **Day 1.** One object on its everyday surface. The day chip and the count appear: Day 1, 1.
3. **Doubling.** Day *d* has exactly 2^(d-1) objects. The counter shows the exact integer every time it changes. Days accelerate; the camera pulls back slowly while the object fills its plate, then a room, a building, a city and beyond. The pull-back is unbroken for as long as one scene can hold both ends of it; the screen is covered by the object's colour only for a big jump, to a city, a country or the planet, that no single scene can contain.
4. **One comparator per scale jump.** Each jump is measured against one thing a global viewer already knows, shown in the scene and tagged with a real number in the same unit as the mass.
5. **Payoff, last seconds.** One deadpan sentence stating the final fact, with its day: "Day 69: Earth is 1 cm deep in rice." No exclamation mark, no joke on top, no moral.
6. **Loop.** The last frame matches the first, so the film restarts without a visible seam.

A new information beat lands every 2 to 4 seconds: a new day, a new scale, a comparator, or the payoff.

## What changes every episode

The series is a premise, not a template. Each episode differs from every earlier one in all of these:

- **Premise.** A new object with its own reason to be interesting: how it packs, what it weighs, where it would pile up, what it would bury. Changing the object alone is not a new episode.
- **Opening place.** Where the object naturally sits: a plate, a desk, a pocket, a court, a windowsill.
- **Scale path.** Which four or five rungs of the ladder are shown, and by which measure the object grows: volume, mass, length laid end to end, or area covered.
- **Comparators.** No episode reuses another episode's full comparator set. Record each episode's set in its production notes so the next one can check.
- **World and hero colour.** A ramp and hero colour that suit the object.
- **Ending.** Where the arithmetic stops is the episode's own: a room, a country, the planet, the Moon's orbit.

No "part 2", no numbered sequels, no "more tomorrow". Every film is complete on its own and titled by its premise.

## Numbers and sources

Every number on screen is computed, not estimated by eye.

- Day *d* count is 2^(d-1). Use integer arithmetic; never round the count.
- State the per-object figure used (volume, bulk volume with packing, mass, or length), with a source and the date it was read.
- State each comparator's figure with a source: height, floor area, volume, land area, radius.
- For each scale jump and for the payoff, keep the working: count, per-object figure, total, comparator figure, and the first day on which the total passes it.
- Round only the words. "2.1 billion" may name 2,147,483,648; the digits stay exact. A payoff measure is rounded down, never up.
- Say how the mass is assumed to behave when it matters: loose packing for grains and balls, a solid block for cubes, an even layer for planet-scale coverage.
- Keep a `SOURCES.md` in the production with the links, the quoted figures, and the calculation table. Research follows the production's research contract.

The figures in the board's studies and motion preview are illustrative. They were worked out to keep the samples plausible, and they are not verified claims. A production recomputes and sources its own.

## On-screen text

- Question, day chip, count, unit line, comparator tags, payoff. Nothing else.
- All of it must be readable with the sound off, at phone size.
- Sentence case for the question and payoff. Uppercase for unit lines and tags.
- No emoji, no hashtags or handles in the frame, no "wait for it", no arrows.

## Voice and sound

- No narration, ever. The film has no voice; the payoff is read, not spoken.
- Sound effects carry the film and are dense. Every visible event has its own sound:
  - a tick on each day change, tightening and rising as the days shorten;
  - the object's own material sound, growing with the count (a few grains pattering, then a pour, then a roar);
  - a distinct hit on each scale jump, never the same take twice in one episode;
  - a short stamp when a comparator tag lands;
  - a dry, small sound on the payoff after a beat of near silence;
  - a reversed sweep on the rewind that ends on the first tick.
- The object's material sound is new for every episode, like its scene and comparators.
- Music stays thin and under the effects.
- Tone is deadpan throughout. The numbers are the joke.
- No narration voice is needed: [AUDIO.json](AUDIO.json) stays empty.

## Packaging

- Title: the question or the payoff fact, in plain words. No "part", no series numbering.
- Description: one line with the payoff, then the key assumptions and sources in brief.
- Indonesian upload, on request only: translated title, description and on-screen text; same film.
- Publishing accounts are not configured: [ACCOUNTS.json](ACCOUNTS.json).

## Illustrative premises

Examples to show range, not a backlog and not verified:

| Object | Starts on | Measure | Possible path |
| --- | --- | --- | --- |
| Grain of rice | A plate | Bulk volume | Plate, bedroom, stadium, a city, Earth's surface |
| Tennis ball | A court | Packed volume | Court, house, arena, a mountain |
| Die | A game board | Solid block edge | Table, room, Statue of Liberty, Manhattan |
| Sheet of paper | A desk | Stack height | Desk, tower, cruising altitude, the Moon |
| Coin | A pocket | Mass | Pocket, a car, a cargo ship, a mountain |

## Open fields

- Publishing accounts for each platform. The user will supply them.
- A fixed series title treatment for platform metadata, if any.
