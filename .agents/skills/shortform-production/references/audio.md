# Audio generation and resolution

Use this guide for the `audio` stage of short-form production: generate narration, sound effects (SFX), and background music (BGM), then establish actual duration and word timestamps for captions.

## 1. Audio stage completion criteria

The audio stage connects the script (`SCRIPT.md`) and visual storyboard (`STORYBOARD.md`) to the final HyperFrames animation:

- Convert scripted narration into audio files.
- Measure the full audio duration (`duration_s`) and each scene's time range to replace storyboard estimates.
- Produce word timestamps (alignment) for HyperFrames captions.
- Complete the stage when all narration, SFX, and music required by the brief or board are available, their durations are measured, and scene timing is updated.

## Default voiceover: full script, one request

For productions in this workspace, combine all approved narration into one TTS input and send it in one synthesis request to keep delivery and voice consistent. Preserve punctuation and paragraph breaks; keep visual directions and on-screen copy outside the narration input.

With the shared engine, use exactly one `lines` entry with ID `narration` containing the full script. Each entry triggers a separate TTS request, so divide scenes after synthesis using word timestamps from the complete audio. Store each scene's word/time ranges in `STORYBOARD.md`; use one continuous voiceover track as the timing reference for animation and captions. Place SFX according to those scene timings.

If the provider's input limit requires splitting, explain the limit and use as few segments as possible at natural narration breaks. An explicit user request for synthesis in separate parts can also override this default. When narration changes, regenerate the full narration by default; reuse audio that remains valid without another request.

## 2. Engine and provider selection

### Voiceover (TTS)

Follow the provider and model policy in the root `AGENTS.md`. Resolve the voice with `scripts/narration.py:resolve_voice`: an explicit user-authorized episode override with its reason takes precedence; otherwise read `ELEVENLABS_VOICE_ID` from the project root `.env`. Inherited shell voice settings, example IDs and historical production choices do not override that file. A missing voice is an error. Write the resolved literal ID and `voice_resolution` provenance into the new request. Preserve completed audio and its historical metadata until regeneration is authorized.

Choose delivery from the script before choosing tags. For each meaningful beat, infer the speaker's intent, emotional shift, vocal energy, pace, and relationship to the listener from the approved narration and board. Translate the audible direction into concise English instructions in square brackets at the points where delivery should change. Use tags where they help the performance; natural passages can remain untagged.

Audio tags are open-ended delivery instructions, not a closed vocabulary. Select or formulate tags that fit the passage rather than drawing from a fixed shortlist or repeating a preset across episodes. Consult the current [ElevenLabs prompting guide](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices#prompting-eleven-v4) when needed; its examples are starting points for exploration. Treat unfamiliar directions as candidates to verify by listening with the selected voice. Favor a coherent performance over tag variety for its own sake.

Store the full approved narration with its chosen tags in `audio_request.json`, while captions contain spoken words only. Exclude tags from narration word counts. Replace the placeholders in the examples below with this prepared text; the placeholders are not literal tags or synthesis input.

Listen to the result and inspect alignment: tags should direct delivery rather than appear as speech or captions. If alignment includes tags, remove their spans from captions while preserving the original spoken-word timestamps; if alignment is unusable, transcribe the same audio locally. Report synthesis failures without automatically switching provider, voice, or model.

### Sound Effects (SFX)

1. **Bundled library**: Use the 19-file SFX library at `.agents/skills/media-use/assets/sfx/` for standard transition effects (*whoosh*, *pop*, *click*, *riser*).
2. **ElevenLabs Sound Effects**: Use the `sound-effects` skill to generate specific effects or atmospheric textures from text descriptions.

### Background Music (BGM)

- Choose a subtle instrumental track that fits the board's mood, such as *calm reflective* or *cinematic lofi*.
- Keep music from competing with narration frequencies; apply ducking or a voiceover carve during HyperFrames assembly.

## 3. Execution paths

Choose one of the following paths as appropriate.

### Maintained workspace synthesis entry point

Use [scripts/narration.py](../scripts/narration.py) for continuous ElevenLabs narration in this workspace. It validates the request against the current voice source before any paid call and fingerprints the provider, voice, model, tagged text, language, output format and supplied settings. The content-addressed MP3, alignment and request receipt live together in `video/.media/audio/voice/`. Reuse requires matching request and file hashes; a bare `narration-full.mp3` is not a valid cache. Older audio stays available. A changed default does not retroactively relabel or regenerate completed productions.

Record request provenance as `"voice_resolution": {"source": "project_env", "key": "ELEVENLABS_VOICE_ID"}`. For an explicit episode override use `{"source": "episode_override", "reason": "<USER_AUTHORIZED_REASON>"}` and its literal `voice` ID. Rebuild a stale request from its selected source rather than silently overriding it during synthesis.

From the project root:

```bash
python .agents/skills/shortform-production/scripts/narration.py --video productions/<slug>/video --check
python .agents/skills/shortform-production/scripts/narration.py --video productions/<slug>/video
```

`--check` is read-only and makes no API call. The second command performs one full-script request when no verified cache exists. It uses native timestamps and MP3 output, writes `audio_meta.json` only after successful decoding/alignment, and retains the selected provider/voice/model on failure. A provider failure is reported without an automatic retry or fallback. If synthesis succeeded but alignment is unusable, transcribe that exact recording locally instead of resynthesizing it. After changing the voice, rebuild measured scene timing, captions and exports before treating the revision as complete.

After changing the resolver or cache behavior, run `python .agents/skills/shortform-production/scripts/test_narration.py` from the project root. These regression checks make no API calls.

### Alternative: Shared HyperFrames audio engine (`media-use`)

The engine at `media-use/audio/scripts/audio.mjs` handles TTS, SFX, Whisper transcription (word timestamps), and `audio_meta.json` generation in one run:

1. Create `productions/<slug>/video/audio_request.json` using the project policy and resolved voice (replace every placeholder before execution). Replace the placeholder narration with the full approved script in the production's language:

   ```json
   {
     "provider": "elevenlabs",
     "lang": "id",
     "voice": "<RESOLVED_VOICE_ID>",
     "voice_resolution": {"source": "project_env", "key": "ELEVENLABS_VOICE_ID"},
     "tts_model": "eleven_v4",
     "speed": 1.0,
     "lines": [
       { "id": "narration", "text": "<FULL_APPROVED_NARRATION_WITH_SCRIPT_SPECIFIC_AUDIO_TAGS>" }
     ],
     "bgm": {
       "mode": "none"
     }
   }
   ```
2. Run the engine with paths resolved from the project root or video directory. This example runs from the project root:

   ```bash
   node .agents/skills/media-use/audio/scripts/audio.mjs --request ./productions/<slug>/video/audio_request.json --hyperframes ./productions/<slug>/video --out ./productions/<slug>/video/audio_meta.json
   ```
3. For ElevenLabs, the engine uses `convert_with_timestamps`: one TTS request returns both audio and character alignment. The engine converts alignment into word timestamps, preferring `normalized_alignment`, then `alignment`. Local transcription is used only when neither alignment is available or valid; a failed TTS request does not trigger automatic resynthesis. Use an ElevenLabs SDK version that provides this method.
4. The engine writes assets to `video/.media/audio/` and word timestamps to `audio_meta.json`.

### Alternative: Direct CLI or SDK invocation (`text-to-speech`)

When using the direct path, send the full narration in one synthesis call. The example uses placeholder text; replace it with all approved narration in the production's language.

1. Use the ElevenLabs CLI or a Python script:

   ```bash
   elevenlabs text-to-speech convert \
     --voice-id <RESOLVED_VOICE_ID> \
     --model-id eleven_v4 \
     --text "<FULL_APPROVED_NARRATION_WITH_SCRIPT_SPECIFIC_AUDIO_TAGS>" \
     --output ./productions/<slug>/video/assets/audio/vo_full.mp3
   ```
2. The direct CLI example does not retrieve native alignment. Use Path A when timestamps are needed without additional transcription. For recorded audio or output without alignment, transcribe locally:

   ```bash
   npx hyperframes transcribe ./productions/<slug>/video/assets/audio/vo_full.mp3 --language id --dir ./productions/<slug>/video
   ```

## 4. File locations

All audio files used for rendering must be inside the `video/` directory so the HyperFrames runtime can access them:

```text
productions/<slug>/video/
  audio_request.json        Audio request configuration (when using the engine)
  audio_meta.json           Actual duration, word timestamps, and file paths
  .media/audio/
    voice/                  Full-script WAV/MP3 voiceover
    sfx/                    Sound effect files
    bgm/                    Background music files
  assets/audio/             Alternative location for manually supplied audio
```

## 5. Storyboard synchronization and next steps

After generating the audio:

1. **Update `STORYBOARD.md`**: Map word timestamps from `audio_meta.json` to scene boundaries in the full audio, then update each scene's duration and start/end times. The total voiceover duration is not the duration of each scene.
2. **Update `EPISODE.md`**: Record the voice model, voice ID, actual total duration, and audio approval status.
3. **Update `TRACKER.json`**: Once the audio stage is complete, set `stage: "production"` and `status: "in_progress"`.
4. Continue to the `production` stage to assemble scenes in HyperFrames.
