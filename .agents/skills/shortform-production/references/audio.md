# Audio generation and resolution

Read for the production's audio stage. Resolve narration, SFX, and BGM separately from the accepted brief and board. Generate through the [ElevenLabs transport](#choose-the-elevenlabs-transport) and the relevant installed ElevenLabs skill for each audio role. Source SFX from existing media-use assets first.

## Completion

Record an explicit use/none decision and creative reason for each audio role. Complete the stage when planned assets exist, durations and spoken-word alignment are measured, scene ranges in `STORYBOARD.md` match the actual narration, and the take has been [listened to](#listen-to-the-take-and-the-mix) or its listening recorded as unavailable. A voice-only mix is valid when intentional; an empty SFX array alone is not a decision.

## Choose the ElevenLabs transport

Before any ElevenLabs generation (narration, SFX, or music), check available transports in priority order without spending credits:

1. **API key (default)**: `ELEVENLABS_API_KEY` is configured with a non-placeholder value in the project root `.env`, and `python .agents/skills/shortform-production/scripts/narration.py --check-api` succeeds (`GET /v1/user`).
2. **CLI**: `elevenlabs` is on PATH and `elevenlabs auth status` reports `logged_in: true`.
3. **MCP**: an ElevenLabs MCP server is connected in the session, offers the tool the role needs (`creative_generate_speech` for narration), and a read-only call such as `account_get_usage` succeeds.

Select the highest-priority available transport that supports the role: **API key → CLI → MCP**. Record the chosen transport (`elevenlabs_api`, `elevenlabs_cli`, or `elevenlabs_mcp`) in `EPISODE.md`. Never print or persist `ELEVENLABS_API_KEY` in artifacts, logs, or receipts. When none is available, or no available transport supports the role, stop and ask the user to configure `ELEVENLABS_API_KEY` in the project root `.env`, sign in with `elevenlabs auth login` for the CLI, or connect the ElevenLabs MCP server in their agent harness.

Generate exactly one take per request on any transport. MCP speech defaults to 2 variations, so always pass `generations_count: 1`. Never call a generation tool again to retry an uncertain run; check its status or history first.

## Voiceover: ElevenLabs

Use explicit `provider: elevenlabs` and `tts_model: eleven_v4`. Resolve the voice with [narration.py](../scripts/narration.py) in this order: an explicit user-selected episode override with its reason, the selected board's `AUDIO.json` `voice_id`, then the project root `.env` key `ELEVENLABS_VOICE_ID`. The [board configuration contract](../../shortform-board/references/board-files.md#narration-voice) defines unset values and validation. Shell settings, examples, and historical episodes do not override these sources. An unset board voice with no root default is an error. Preserve completed audio and its historical metadata until regeneration is authorized.

Prepare the full final narration as one `lines` entry with ID `narration`. Preserve punctuation and paragraphs; keep visual directions and on-screen copy outside the spoken text. One continuous recording supplies every scene's timing. Split only when an actual provider limit or explicit user request requires it; document the reason and use a suitable [alternative integration](audio-alternatives.md).

Before synthesis, verify that this exact spoken text retains the script's accepted speaker cues and satisfies any board-required POV check under [research and script](research.md#develop-the-script). On an audio-stage resume, reuse the recorded check only when it covers this wording and the production's recorded editorial revision; otherwise complete the affected check before generating.

Read the installed `text-to-speech` skill for model settings and delivery. Choose concise English tags in square brackets where the speaker's intent, energy, pace, or relationship to the listener changes. Store tagged narration in `audio_request.json`. Keep captions and word counts to spoken words.

### Maintained workspace synthesis entry point

Write `video/audio_request.json` with the resolved literal voice, its provenance, and the full tagged script. Replace all placeholders before generation:

```json
{
  "provider": "elevenlabs",
  "board": "<SELECTED_BOARD_SLUG>",
  "lang": "id",
  "voice": "<RESOLVED_VOICE_ID>",
  "voice_resolution": {"source": "project_env", "key": "ELEVENLABS_VOICE_ID"},
  "tts_model": "eleven_v4",
  "lines": [
    {"id": "narration", "text": "<FULL_FINAL_NARRATION_WITH_DELIVERY_TAGS>"}
  ]
}
```

Prepare `voice` and `voice_resolution` together with `resolve_voice(root, board="<SELECTED_BOARD_SLUG>")`. For a configured board voice, the returned resolution is `{"source": "board_config", "board": "<SELECTED_BOARD_SLUG>", "path": "boards/<SELECTED_BOARD_SLUG>/AUDIO.json", "key": "voice_id"}`; root fallback uses the `project_env` resolution shown above. Pass the selected board even when it currently inherits the root default. Omit `board` only for a production with no board.

For an explicit episode voice use `resolve_voice(root, override="<VOICE_ID>", reason="<USER_AUTHORIZED_REASON>", board="<SELECTED_BOARD_SLUG>")`. Its resolution source is `episode_override`. The helper checks the request against the production's registered board in `TRACKER.json` and the current voice configuration. Rebuild a stale request from its selected source before synthesis.

From the project root:

```bash
python .agents/skills/shortform-production/scripts/narration.py --video productions/<slug>/video --check
python .agents/skills/shortform-production/scripts/narration.py --video productions/<slug>/video
```

`--check` inspects the request and cache without network calls or writes. `cached` reuses a verified take, `resume_api` or `resume_cli` recovers a saved response, and `awaiting_api` or `awaiting_cli` indicates a new take is needed. Run without `--check` to write `audio_meta.json` or generate the new take when authorized. By default (`--transport auto`), the helper prefers `ELEVENLABS_API_KEY` from the project root `.env` (`elevenlabs_api`) and falls back to the signed-in `@elevenlabs/cli` on PATH (`elevenlabs_cli`) when no API key is configured; pass `--transport cli` if the preflight `--check-api` failed and you are falling back to CLI. Both local transports require `ffprobe`. On the MCP transport, generate and import the single take with [MCP narration](elevenlabs-mcp.md). The project voice default is configured separately in `.env`.

On the API key transport, the helper sends one `POST /v1/text-to-speech/{voice_id}/with-timestamps` request with `xi-api-key` from `.env`; on the CLI transport, it calls `elevenlabs text-to-speech convert_with_timestamps` once. Both use the resolved voice, `eleven_v4`, the full tagged script, and explicit language and MP3 format. It checks the MP3 and word timings before returning `ready`. It caps the final native word end at the file duration when only that endpoint exceeds it by up to 100 ms. Narration, native timing, and request receipts live in `video/.media/audio/voice/`. Existing valid API, CLI, MCP, and SDK cache sets are reusable by request and file hashes.

If an API or CLI take has missing or invalid timing, use [timing recovery](audio-alternatives.md) (`align_narration.py` or `--auto-align`) on the saved MP3; do not write ad-hoc per-episode alignment scripts. It runs padded `faster-whisper` ASR verification (catching spoken delivery tags, numeric mismatches, and clipped edge words) followed by `Wav2Vec2` CTC forced alignment onto exact script words. Declare `"asr_aliases": {"maggot": "magot"}` in `audio_request.json` when phonetic loanwords differ in ASR. Review playback when available before marking the stage ready. Report failures and check for a completed take before retrying an uncertain request.

A changed narration requires timing, captions, and affected exports to be rebuilt. When changing the resolver, alignment, or cache implementation, run `python -m unittest discover -s .agents/skills/shortform-production/scripts -p "test_*narration*.py"`; it makes no API calls.

For old shared-engine files or a completed historical take awaiting import, read [integration compatibility](audio-alternatives.md).

## Sound effects: media-use first

1. Inspect the [bundled media-use manifest](../../media-use/audio/assets/sfx/manifest.json) and its existing local files first. Choose by narrative function, timbre, intensity, duration, and fit with narration and the board. Reuse a fitting file across cues or episodes with episode-specific timing and gain.
2. If the bundled files do not fit, inspect frozen board/production assets and their provenance, including previously treated media-use variants. Keep useful variants in the owning board's library for later reuse.
3. For a remaining gap, use media-use's [SFX sourcing guidance](../../media-use/audio/references/sfx.md) to retrieve a suitable effect. The generic resolver searches Openverse first, so inspect the bundled library before invoking retrieval. Record an unresolved required cue or revise the plan with a creative reason when no source fits.

Copy selected bytes into the production's `video/` directory and retain source, treatment, license/credits, and SHA-256. Copying a frozen file is reuse, not another treatment pass. Preserve completed exports when updating the reusable library or sourcing policy.

When the user requests new SFX generation, read the installed `sound-effects` skill and generate one take on the [chosen transport](#choose-the-elevenlabs-transport): via the REST API (`POST /v1/sound-generation` with `ELEVENLABS_API_KEY` from `.env`), on the CLI (`elevenlabs text-to-sound-effects convert`), or via MCP. Save the result in `video/` and record the model, prompt, file hash, and cue placement.

## Background music

Resolve use/none from the brief and board. Source an instrumental track matching its mood through media-use and mix it below the narration. For requested original music, read the installed `music` skill and generate one take on the [chosen transport](#choose-the-elevenlabs-transport): via the REST API (`POST /v1/music` with `ELEVENLABS_API_KEY` from `.env`), on the CLI (`elevenlabs music compose` with `--force-instrumental true`; if CLI 1.12.2 asks for deprecated `music_prompt` fields, pass `--music-prompt=null`), or via MCP. Save the result in `video/` and record the model, prompt or composition plan, and file hash.

## Sound design: plan, assemble, verify

Record each role's decision in `video/sound_design.json`. When placing or revising SFX/BGM, read [sound design](sound-design.md) for cue planning, `sound_design.py`, provenance, timing/motion hashes, and verification in the actual export. Preserve supplemental media when narration is regenerated and revalidate affected cue timing.

## Listen to the take and the mix

Measurements show that sound is present and level; someone has to hear whether it is right. Listen twice: to the narration take before it is placed, and to the mix in the draft proof. Take the first route available in [native audio review](../../video-to-board/references/video-analysis.md#native-audio-review), with the take or the proof's audio as the source, and record it as `listening` in the [gate record](quality-gate.md#review-the-film):

| `listening` | Who heard it |
| --- | --- |
| `agent` | This session received the audio natively. |
| `worker` | An Antigravity worker through Orca. |
| `human` | The user listened; their response is recorded in `EPISODE.md`. |
| `silent` | The film has no audio by decision. |
| `unavailable` | Nobody has heard it. The gate discloses this at every checkpoint. |

In the take, listen for a delivery tag read aloud, a mispronounced name, term or number, a clipped first or last syllable, a pace or pause that fights the meaning, and delivery that misses the board's voice. In the mix, listen for an effect masking a word, an effect with no visible event, a jump at a scene seam, and music or effects standing above the narration. Record each finding with its timestamp in `video/REVIEW.md`. A take that fails on wording or pronunciation returns to the script or to an authorized regeneration.

Mix to the contract's loudness window: −15 to −13 LUFS integrated with a true peak at or below −0.5 dBTP unless the contract sets another. The gate measures both on the export.

## Files and handoff

All render media belongs inside `video/`. The default voice cache is `video/.media/audio/voice/`; keep SFX/BGM in self-contained local media folders. Consume the paths written to `audio_meta.json`. Alternative integrations' output paths are documented with those integrations.

After audio is ready:

1. Update `STORYBOARD.md` scene boundaries and word/time ranges from the measured full recording. Total voiceover duration is not each scene's duration.
2. Record provider/model/voice, actual duration, review state, and any listening limits in `EPISODE.md`.
3. At an audio-only endpoint, deliver verified audio and timing, resolve any required review, and record `audio: complete`. Otherwise continue from the earliest unfinished stage within the resolved endpoint; after a fresh audio stage this is `production: in_progress`.

## Narration boundaries and editorial pauses

Use [acoustic boundary placement](audio-boundaries.md) when narration spans scene changes or editorial silence is inserted. Provider timestamps locate the text; decoded audio determines a safe splice. Scene cuts, captions and cues must share the final placement map and integer video-frame clock. Complete verification only after every narration seam passes the boundary preflight and the actual export check.
