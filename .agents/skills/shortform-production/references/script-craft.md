# Hook and script craft

Read when writing or revising a hook or a script. The selected board's editorial guidance and the production's `CONTRACT.json` decide structure, voice and limits; this reference holds the short-form craft every board shares. [Research and script](research.md) owns research, the hook-selection checkpoint and storage.

HyperFrames' [vertical](../../hyperframes/references/types/vertical.md), [explainer](../../hyperframes/references/types/explainer.md) and [script and pacing](../../hyperframes/references/film.md#script-and-pacing) guidance supply the format craft: the first second, muted viewing, one worked example, words per scene. Apply them here; the contract's numbers take precedence where they differ.

## Budget the words first

A script is sized from the measured pace of the voice that will read it. Resolve the voice under [audio generation](audio.md#voiceover-elevenlabs), then from the project root:

```bash
python .agents/skills/shortform-production/scripts/episode_qa.py --budget <WORDS> --voice <VOICE_ID> --production productions/<slug>
```

It reports that voice's words per second across recorded productions, the predicted narration and film seconds, whether the film fits the contract's duration, and `words_for_range`. Write to that word range. For a voice with no recorded production, plan at 2.4 words per second and budget again after its first take. Budget before synthesis: a take that misses the duration costs a regeneration.

## Write the hook as three parts

A hook is what the viewer hears, sees and reads in the first seconds, decided together:

- **Spoken line.** The first sentence names a concrete situation, action or result and carries the tension or question. It ends within the contract's `hook.first_sentence_max_seconds` (5 seconds by default, about twelve words).
- **Frame 0.** State what is already on screen at the first frame (the subject, the result or the action under way) and what changes within the first second.
- **On-screen line.** The words a muted viewer reads at phone size while the spoken line plays: the caption group, a cover line or emphasis copy, as the board provides.

Each of the three hook options carries all three parts and the promise the episode pays. Options differ in mechanism (a result shown first, a puzzling behavior, a question inside a moment), beyond wording.

## Write for the ear and the picture

- **One sentence, one visible event.** Each sentence names something the picture shows while it is spoken. Move a sentence to where its picture is, or cut it.
- **Short spoken clauses, concrete nouns and verbs.** A term enters at the moment it is used. Spell numbers, units and abbreviations the way they are said.
- **Turn early.** The first shortfall, surprise or tension arrives while the viewer is still deciding to stay; the contract's judged rules give the board's timing.
- **Mark the beats.** Where a scene runs longer than about 19 spoken words, list the visible changes inside it, one per phrase, so the storyboard inherits a beat for every stretch of narration.
- **Pay the promise.** The ending returns to the opening situation and answers it with what the viewer has now seen.
- **Separate the layers.** Keep narration, captions and on-screen copy as separate lines in `SCRIPT.md`; on-screen copy adds to the spoken sentence.

## Cold-read the narration

Read the complete spoken text alone, in order, without headings, visual cues or metadata:

1. Every pronoun, speaker and instruction recipient resolves from speech.
2. After each paragraph a listener could say what happened and why.
3. Each sentence makes sense without the on-screen text.

Repair what fails and read again. A board's own continuity check, such as a POV contract, runs on top of this one.

## Record the script check

Before script review or delegated verification, record in `EPISODE.md`:

- spoken word count and the budget output (pace, predicted film seconds, fit);
- the first sentence's word count and predicted seconds;
- the selected hook's three parts;
- the cold-read result and any repairs;
- each contract judged rule that concerns the script, marked pass or fail with one line of evidence.

The script is ready for review when every item is recorded and passing.
