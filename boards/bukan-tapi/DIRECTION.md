# Bukan, Tapi

Working name: Bukan, Tapi. Revision 1, approved by the user on 2026-11-23 (editorial v1 and visual v1, with the narrated motion preview). The music sample was added after that approval under a delegated choice.

## Brief

On 2026-11-23 the user supplied five reference clips (`milyty.zip`) through `video-to-board`. The analysis and board vision were presented in Indonesian and accepted with "cocok", which authorised building this package. Requested endpoint: a reusable board. No episode, publishing or account setup was requested.

## Direction

Narrated Indonesian parables of 75–110 seconds for a general audience. The viewer thinks they know the ending, is turned around, and leaves with one quotable contrastive line. Flat outlined 2D stage with original bean characters, lowercase captions with the spoken word in an orange box, a new picture on every narration clause.

- [Editorial framework v1](EDITORIAL.md)
- [Visual specification v1](frame.md)
- [Production contract](CONTRACT.json)
- [Style board source](style-board.html) and [PNG](style-board.png)
- [Motion preview MP4](motion-preview.mp4) and its [editable project](motion-preview/index.html)
- [Study source](studies/studies.html) with four rendered stills in `studies/`
- [Drawing kit](assets/kit.js), [sample scenes and pilot](assets/scenes.js), [export script](export-board.cjs)
- [Reference evidence and adaptation matrix](references/ANALYSIS.md), [look comparison](references/compare-look.png)
- [Voice configuration](AUDIO.json): Eman Lawa (`aAmDu76s8GN3Gq749D7h`). [Publishing accounts](ACCOUNTS.json): none configured.

## Decisions

Accepted by the user on 2026-11-23 (vision only):

- Keep the reference story shape, stage framing, caption position and shot rhythm.
- Stay flat 2D and voice-led, with original character design instead of the reference stick figures.
- New palette with one fixed highlight colour, an open-licensed typeface, an ElevenLabs Indonesian narrator, original stories.

Accepted by the user on 2026-11-23 after hearing the narrated preview ("ya"):

- Board narration voice: ElevenLabs "Eman Lawa - Calm, Deep and Reassuring" (`aAmDu76s8GN3Gq749D7h`), `eleven_v4`. It was the only candidate sampled.

Accepted by the user on 2026-11-23 as the whole board ("setuju"):

- The name "Bukan, Tapi" and slug `bukan-tapi`.
- Bean characters, the four stage palettes, orange `#FF7A2F` as the highlight (the references use green), Plus Jakarta Sans.
- Contract numbers: 75–110 s, first motion within 1 s, no static stretch over 2 s, at most five whip slides.

Open:

- Music: the user delegated the choice ("terserah devin"). The agent placed a CC0 soft piano track under the pilot as an example of the direction. It is a sample, not a fixed board track; each episode sources its own bed in the same character. The user has not commented on it.
- Viewer-facing series name, account handles, recurring cast or new archetypes per episode.

## Provenance

Reference: five user-supplied clips, analysed locally; see [references/ANALYSIS.md](references/ANALYSIS.md). No reference character, wording, story, music or watermark is reused. Drawings and motion are original and built in code. Plus Jakarta Sans variable: The Plus Jakarta Sans Project Authors, SIL OFL 1.1 (`assets/fonts/`). Pilot effects: `pop`, `whoosh-short` and `sparkle` from the bundled media-use SFX library. Pilot music: "Relaxing piano-AR22-2_43" by AngeloRizzo, CC0 1.0, https://freesound.org/people/AngeloRizzo/sounds/717150 (found through Openverse; stored at `motion-preview/audio/bgm-relaxing-piano.mp3`). All sample copy and figures are illustrative.

## Rendered review

Inspected by the agent on 2026-11-23.

- **Style board**, 1440 px wide. Checked at board scale and in a zoomed crop: font loads, no overflow, swatches match `frame.md`.
- After approval the "draft" label was removed from the style-board lede and the PNG re-exported from the same source; nothing else on the board changed.
- **Studies**, 1080 x 1920 each: hook (dusk), dialogue (room), cutaway (night), reveal (workshop).
- **Motion preview**, 16.0 s, 1080 x 1920, 30 fps. Seven shots on the illustrative "Dua tukang kayu" opening: hook with both carpenters, order cutaway, path A, whip slide into path B, sharpening close-up, wide score, push-in on the false expectation. It stops before the reversal. `hyperframes check` passes with 0 errors and 0 warnings.
- **Fingerprint** (`episode_qa.py --fingerprint`, caption region `60,1400,960,200`): first motion 0.2 s, longest static 0.2 s, held share 0.0. References: first motion 0.2 s on all five, longest static 0–1.6 s, held share 0–2.4%.
- **Narration**: one `eleven_v4` take of the candidate voice through the ElevenLabs MCP (279 credits), stored at `motion-preview/audio/narration.mp3` with word times in `narration.words.json`. 38 words in 15.36 s, 2.47 words per second (references 2.44–2.55). `align_narration.py` ASR check passed at 0.97 similarity with no spoken tags or clipped edges; word times are faster-whisper mapped, not CTC-aligned (Wav2Vec2 is not installed). Captions and cuts are timed to this take with a 0.15 s lead-in. Average shot 2.3 s (references 2.4–3.1 s, one at 4.6 s).
- **Mix**: voice plus six pops, one whoosh and one sparkle on visible events (`motion-preview/audio/pilot-dry.wav`), with the piano bed (source 0.9–16.9 s) set 28 dB below the mix by integrated loudness, no ducking, 0.4 s fade-in and 1.2 s fade-out. Result −14.1 LUFS, true peak −1.6 dBTP (`motion-preview/audio/pilot-mix.wav`). The references measure a 27–30 dB voice-to-music margin.
- **Look comparison**: [compare-look.png](references/compare-look.png). Caption band, figure scale and bubble/tag placement line up; the colours differ by design.
- `CONTRACT.json` validates with `episode_qa.py --contract`.

Known limits:

- Listening: `human` for the voice only. The user received the narrated preview without music and accepted the voice; they gave no notes on pronunciation or effect balance. The agent checked wording and levels by measurement only.
- The music bed was chosen and levelled by measurement only (low spectral centroid, little percussive energy); the agent cannot hear it and the user has not reviewed it. At a 28 dB margin it is barely audible, as in the references.
- The whip slide shows a visible seam in the hills for a few frames.
- The pilot covers hook, setup, both paths and the false expectation. The reversal and closing maxim exist only as a static study.
- Captions overlap the workbench in the bench shots.
- Interiors, night and dusk palettes are shown as stills only.
- No preview server was started; nothing needs cleanup.

## Next action

Board approved on 2026-11-23 and ready for production selection. Optional: user listens to the music sample in the preview; fix the whip-slide seam in a later revision.
