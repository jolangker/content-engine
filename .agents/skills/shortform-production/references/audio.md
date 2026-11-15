# Audio generation and resolution

Read for the production's audio stage. Narration uses the connected ElevenLabs MCP; the workspace helper prepares requests and imports its output. SFX prioritize existing media-use assets. Resolve narration, SFX, and BGM separately from the accepted brief and board.

## Completion

Record an explicit use/none decision and creative reason for each audio role. Complete the stage when planned assets exist, durations and spoken-word alignment are measured, and scene ranges in `STORYBOARD.md` match the actual narration. A voice-only mix is valid when intentional; an empty SFX array alone is not a decision.

## Voiceover: ElevenLabs

Use explicit `provider: elevenlabs` and `tts_model: eleven_v4`. Resolve the voice with [narration.py](../scripts/narration.py) in this order: an explicit user-selected episode override with its reason, the selected board's `AUDIO.json` `voice_id`, then the project root `.env` key `ELEVENLABS_VOICE_ID`. The [board configuration contract](../../shortform-board/references/board-files.md#narration-voice) defines unset values and validation. Shell settings, examples, and historical episodes do not override these sources. An unset board voice with no root default is an error. Preserve completed audio and its historical metadata until regeneration is authorized.

Prepare the full final narration as one `lines` entry with ID `narration`. Preserve punctuation and paragraphs; keep visual directions and on-screen copy outside the spoken text. One continuous recording supplies every scene's timing. Split only when an actual provider limit or explicit user request requires it; document the reason and use a suitable [alternative integration](audio-alternatives.md).

Before synthesis, verify that this exact spoken text retains the script's accepted speaker cues and satisfies any board-required POV check under [research and script](research.md#develop-the-script). On an audio-stage resume, reuse the recorded check only when it covers this wording and the production's recorded editorial revision; otherwise complete the affected check before generating.

Choose delivery tags from the speaker's intent, emotional shifts, energy, pace, and relationship to the listener. Use concise English instructions in square brackets where delivery changes; tags are open-ended directions, not a fixed preset. Consult MCP's `creative_get_model_guide` for `eleven_v4` when needed. Store tagged narration in `audio_request.json`; captions and word counts contain spoken words only.

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

For an explicit episode voice use `resolve_voice(root, override="<VOICE_ID>", reason="<USER_AUTHORIZED_REASON>", board="<SELECTED_BOARD_SLUG>")`; its resolution source is `episode_override`. The helper also resolves the production's registered board from `TRACKER.json` and rejects a conflicting request board, stale voice, or changed source before preparing the MCP call. Rebuild a stale request from its selected source before synthesis.

From the project root:

```bash
python .agents/skills/shortform-production/scripts/narration.py --video productions/<slug>/video --check
```

`--check` validates without network calls or writes. On a cache miss it prints the exact `creative_generate_speech` arguments, or returns existing flow/session IDs to resume. Follow [ElevenLabs MCP execution and import](elevenlabs-mcp.md) before marking audio ready. Running the helper without import arguments also only prepares/resumes a call on a cache miss; the agent executes MCP tools. MCP authentication replaces the local SDK/API-key requirement.

Content-addressed MP3, alignment, and request receipts live together in `video/.media/audio/voice/`; reuse requires matching request and file hashes. Existing SDK-era cache sets remain reusable. A bare narration file is insufficient. The fingerprint retains provider, voice, model, tagged text, language, output format, and supplied settings for compatibility; unsupported new MCP settings fail before generation. A changed default leaves completed productions' audio and metadata intact.

MCP speech output does not guarantee native timestamps. Align/transcribe the exact downloaded recording locally, then import the audio, run receipt, and measured timing. The helper writes `audio_meta.json` only after verifying provenance, MP3 duration, and alignment. Report failures without automatic generation retry or provider/model fallback. Listen and inspect alignment when playback is available; state listening limits honestly.

A changed narration requires timing, captions, and affected exports to be rebuilt. When changing the resolver or cache implementation, run `python .agents/skills/shortform-production/scripts/test_narration.py`; it makes no API calls.

For old shared-engine files or local alignment recovery, read [integration compatibility](audio-alternatives.md). Production narration continues through MCP; installed media-use SDK examples do not override this project contract.

## Sound effects: media-use first

1. Inspect the [bundled media-use manifest](../../media-use/audio/assets/sfx/manifest.json) and its existing local files first. Choose by narrative function, timbre, intensity, duration, and fit with narration and the board. Reuse a fitting file across cues or episodes with episode-specific timing and gain.
2. If the bundled files do not fit, inspect frozen board/production assets and their provenance, including previously treated media-use variants. Keep useful variants in the owning board's library for later reuse.
3. For a remaining gap, use media-use's [SFX sourcing guidance](../../media-use/audio/references/sfx.md) to retrieve a suitable effect. The generic resolver searches Openverse first, so inspect the bundled library before invoking retrieval. Record an unresolved required cue or revise the plan with a creative reason when no source fits.

Copy selected bytes into the production's `video/` directory and retain source, treatment, license/credits, and SHA-256. Copying a frozen file is reuse, not another treatment pass. Preserve completed exports when updating the reusable library or sourcing policy.

New SFX generation requires an explicit user request for generation; a missing library match alone does not select it. Resolve any generation provider separately for that request.

## Background music

Resolve use/none from the brief and board. When used, select an instrumental track matching its mood through media-use; keep it clear of narration with the appropriate mix. An intentional no-music decision remains valid.

## Sound design: plan, assemble, verify

Record each role's decision in `video/sound_design.json`. When placing or revising SFX/BGM, read [sound design](sound-design.md) for cue planning, `sound_design.py`, provenance, timing/motion hashes, and verification in the actual export. Preserve supplemental media when narration is regenerated and revalidate affected cue timing.

## Files and handoff

All render media belongs inside `video/`. The default voice cache is `video/.media/audio/voice/`; keep SFX/BGM in self-contained local media folders. Consume the paths written to `audio_meta.json`. Alternative integrations' output paths are documented with those integrations.

After audio is ready:

1. Update `STORYBOARD.md` scene boundaries and word/time ranges from the measured full recording. Total voiceover duration is not each scene's duration.
2. Record provider/model/voice, actual duration, review state, and any listening limits in `EPISODE.md`.
3. At an audio-only endpoint, deliver verified audio and timing, resolve any required review, and record `audio: complete`. Otherwise continue from the earliest unfinished stage within the resolved endpoint; after a fresh audio stage this is `production: in_progress`.

## Narration boundaries and editorial pauses

Use [acoustic boundary placement](audio-boundaries.md) when narration spans scene changes or editorial silence is inserted. Provider timestamps locate the text; decoded audio determines a safe splice. Scene cuts, captions and cues must share the final placement map and integer video-frame clock. Complete verification only after every narration seam passes the boundary preflight and the actual export check.
