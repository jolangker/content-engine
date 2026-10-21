# Integrated refinement — proposal v1.2

2026-10-21. Updated after the user's creative response. Confirmed requirements are relatable question hooks, richer animation and multiple beats within each frame, exactly 16 frames and two dramatic frames with background/text inversion. Detailed visual studies remain awaiting review. The current package is described in DIRECTION.md, EDITORIAL.md, frame.md and AUDIO.md; those files supersede earlier planning suggestions below where noted.

## Recommended audience experience

The viewer recognizes a small relationship moment, sees how the interaction unfolds, and leaves with a more precise way to observe or respond. Warmth comes from accurate details and spoken language. Clarity comes from showing the relationship between actions.

Creative shorthand: **a small moment, a visible pattern, a concrete possibility**.

This refines the existing editorial and abstract relational concept. Existing pillars and sourcing standards continue to provide its scope.

## Observations informing the proposal

| Observed material | Observation | Creative implication |
| --- | --- | --- |
| Active style board versus frame.md | Original studies use illustrative metadata superseded by the fixed production chrome. | New independent studies should demonstrate the actual production identity and caption band. |
| `kabar-baik` encoded frame 1 | Large quote, actor pair, supporting sentence and spoken captions share the frame. | Give each channel a distinct purpose; supporting copy should earn its place. |
| `kabar-baik` encoded frame 7 | Concept heading, three response qualities and captions create several simultaneous reading demands. | Stage the explanation and let one response become visible in an action. |
| Scripts for `bentuk-dukungan` and `kabar-baik` | Each of 14 script lines is assigned to one frame with main and supporting copy. | Separate spoken phrasing from visual shot decisions; allow an action or comparison to develop across shots. |
| `kabar-baik` storyboard | Repeated establish → develop → reveal-and-hold descriptions appear across all 14 frames. | Specify the narrative event and timing shape of each beat rather than repeating an entrance recipe. |
| Existing audio direction and cue plan | Sparse material cues already have meaningful triggers; BGM is optional. | Refine event phrasing and continuity, then assess the mix during production. Listening quality cannot be inferred from these documents. |

These are design judgments drawn from a limited artifact review, not audience-performance findings.

## Editorial framework

### Sharpen the promise

Help viewers name what happened, follow the interaction, and consider a response suited to the situation. An episode should resolve its opening question and provide an observable distinction.

### Start at the consequential moment

Open with a relatable question about a specific everyday relationship experience. Give the necessary context as the situation develops and answer that question within the episode. A term or general maxim can wait until its explanatory value is clear.

Illustrative hook study: “Pernah nggak, lo cuma pengen cerita, tapi dia langsung ngasih solusi?” This is fictional copy, not a verified psychological claim.

### Develop one meaningful turn

Use the sequence as a flexible reasoning path: concrete event → how the interaction develops → the distinction that clarifies it → a response or observation to try. Internal feelings and motives are possibilities unless established by the scenario or evidence. Avoid presenting an imagined motive as access to another person's mind.

The original three reusable formats remain available. Vary their viewpoint: the person speaking, the person responding, or the interaction between them. The five pillars include ordinary positive moments, repair, needs and boundaries; conflict does not need to initiate every episode.

### Keep nuance with its claim

Place qualifications where they change the explanation. Preserve the existing standards for source mapping, association versus causation, popular versus scientific terms and uneven responsibility. A diagram must preserve the same uncertainty as the narration. Production research remains responsible for every factual episode claim.

### End with something identifiable

Choose one ending: a specific observation, an adaptable sentence, or a criterion for a next step. Return to the opening situation where useful. A broad reflective question should be made specific enough that the viewer can recognize what it asks them to observe.

Illustrative ending study: “Kalau belum jelas, lo bisa tanya: ‘Lo mau gue dengerin dulu, atau bantu mikir?’” Suitability depends on the episode context; this is not universal advice.

## Content concept and channel roles

| Channel | Primary role | Application |
| --- | --- | --- |
| Narration | Context, sequence, interpretation and limits | Natural connected speech; script paragraphs can span shots. |
| Main typography | A memorable line, definition or distinction | One visual reading priority at a time; full communication examples may be longer. |
| Forms and diagrams | Make an interaction or distinction visible | Position, direction, boundary, timing and traces carry explanatory meaning. |
| Supporting labels | Clarify what an element represents | Use close to the relevant element when needed; omit a second summary sentence if it adds no information. |
| Captions | Accessible record of spoken words | Preserve full coverage and existing safe band; emphasis text is selective. |

Quoted speech may intentionally appear in both captions and main typography. Review the combined reading load instead of applying a blanket ban on repetition. The v2 limit of 0–5 emphasis words is not reinstated.

## Visual direction

### Inherited proposed tokens

Retain exact active colors: canvas `#F3EDE3`, ink `#302B28`, accent `#A34F3F`, sand `#D8C8B5`. Retain Newsreader 400 regular/italic for intimate speech and reflection; DM Sans 400/500 for explanation, labels, captions and metadata. Use existing local font assets and licenses.

Keep 1080 × 1920 at 30 fps as the working production canvas. Retain the active content, caption and chrome geometry from root frame.md. The later draft specification will carry these exact values in YAML; this proposal does not create a competing specification.

### Broaden the function of the existing primitives

Organic forms represent participants; a path represents movement or a relationship only when its meaning is established. A boundary marks a specific limit; a trace records a previous state. Small markers can represent an event, an agreed time or a shared focus when introduced clearly. Preserve participant identity within an episode. Color and scale must not silently encode gender, blame, diagnosis or worth.

A shrinking form or space is a conceptual depiction of a narrated experience, not a measurement. Explanatory arrows must not imply causal certainty beyond the source.

### Build six independent composition studies

| Study | Communicative need | Frame proposal | Illustrative copy |
| --- | --- | --- | --- |
| A — A relatable question | Recognize a small experience | Large conversational question; two asymmetric actors and a withheld path. | “Pernah nggak, lo cuma pengen cerita?” |
| B — A dramatic interruption | Follow attention changing | Charcoal field, cream type and an attention path turning toward another focus. | “Lo masih pengen cerita. Dia sudah beralih.” |
| C — A time not agreed | Make a concrete distinction | One quoted word becomes a visual object; a timeline ends at an unresolved boundary. | “Nanti. Terus, kapan?” |
| D — A response develops | Observe sequence | Diagram dominates with two response paths, followed by an inviting quote. | “Terus, gimana?” |
| E — A dramatic articulation | Make a withheld need explicit | Charcoal field and large cream italic quote; a held path punctuates the line. | “Gue masih butuh didengar.” |
| F — A positive shared moment | Show warmth beyond conflict | Forms orient toward one shared event, with a direct invitation above. | “Ceritain lagi. Gue dengerin.” |

These are independent studies across different topics, not an episode sequence. Copy is fictional. The package shows production chrome, caption examples, label hierarchy and static motion poses. The user's later requirement supersedes the optional charcoal suggestion: exactly two of the sixteen episode frames invert the background and text at dramatic script moments. Their positions follow the script; example positions are not mandatory.

## Motion language

Motion should make a verb readable. Describe the relevant starting state, action and consequence before choosing an animation technique.

- **Approach:** one form travels toward an established destination; stopping distance gives the action its meaning.
- **Withhold:** a movement begins and stops before connection; the held state remains readable.
- **Redirect:** attention or a path turns toward another focus while the original participant stays locatable.
- **Repeat:** a previous response leaves a trace, allowing recurrence to be recognized.
- **Agree:** two movements settle around a concrete shared reference such as an agreed time.
- **Open:** a shared focus gains room, expressing a positive invitation in the illustrative scenario.

Vary timing by narrative function. Some shots begin with their state already visible; some develop continuously; some use one late reveal or a purposeful still hold. Carry a participant, path or reference point through related shots where it aids continuity. The same comparison may preserve its framing deliberately.

Continue planning approximately 85–95 seconds and 170–200 initial spoken words, now with exactly 16 meaningful shots per the user's response. Plan multiple internal visual beats in every shot; 3–5 action/response/emphasis changes is an initial production guideline, adjusted for reading and shot length. Actual narration determines timing. Subtitle changes alone are not visual beats. No animation is generated or validated by this static board.

## Audio direction

Retain narration as the main sound, using the existing project synthesis contract when production is requested. Board refinement does not regenerate narration or select another voice.

Direct delivery through changes in communicative intent: immediate and conversational in the opening; precise during explanation; open when quoting a possible response; quieter at a reflective ending. Reserve a pause for a thought that needs to land, without automatically slowing every sentence.

Retain the existing contact/air/connection library. Plan a cue around an actual event and specify whether it accompanies the start, movement or landing. Related shots may share one continuous event without retriggering a sound at every cut. Silence can establish a held or unresolved moment.

BGM remains an episode-specific choice. If used, a restrained instrumental supports continuity and leaves narration clear. A positive scene can use lighter delivery or a rounded material cue without a genre change. No fixed cue quota, raw gain or music requirement is added. Final perceptual balance requires listening during production; no audio demo is implied here.

## Proposed review criteria

- The opening situation and its resolved question can be stated in one sentence each.
- Each shot contributes a new observation, relation, distinction or response.
- Main type, labels and captions have clear reading priorities.
- Shapes and diagrams provide information beyond accompanying the words.
- Sequence review shows purposeful differences in focal scale, alignment, actor presence and timing.
- Source uncertainty survives both narration and graphics.
- Sound triggers correspond to events and the ending has time to settle.

## Review endpoint

The user's response supplied concrete creative requirements, enabling development of the revised board package. Review the resulting static visual studies next. Active v1.1 remains available while that visual review is pending; existing productions retain their recorded direction.
