# Alternative audio integrations

Read only when the user explicitly selects a shared-engine or direct SDK/CLI integration, or when an authorized recovery needs it. Routine production follows [the default audio contract](audio.md). Every production narration path retains the explicit ElevenLabs provider, resolved voice, and `eleven_v4` model; existing valid audio is reused before another paid request. SFX selection follows [media-use first](audio.md#sound-effects-media-use-first), even when using an alternative engine.

## Shared engine

The [maintained workspace entry point](audio.md#maintained-workspace-synthesis-entry-point) remains the default: it enforces voice provenance and verified caching. Use this alternative only for an explicitly selected shared-engine integration; it synthesizes again rather than sharing that cache. Validate the prepared request with `narration.py --check` first. Preserve its literal provider, resolved voice and `tts_model`; workflow adapters' HeyGen/Kokoro defaults do not apply to this workspace.

The engine at `media-use/audio/scripts/audio.mjs` handles TTS, SFX, transcription/alignment (word timestamps), and `audio_meta.json` generation in one run:

1. Create `productions/<slug>/video/audio_request.json` using the project policy and resolved voice (replace every placeholder before execution). Populate both `voice` and `voice_resolution` from `resolve_voice(root, board="<SELECTED_BOARD_SLUG>")`; the example shows root fallback provenance, which must be replaced when a board or episode override is selected. Replace the placeholder narration with the full approved script in the production's language:

   ```json
   {
     "provider": "elevenlabs",
     "board": "<SELECTED_BOARD_SLUG>",
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
3. For ElevenLabs, the engine forwards `tts_model` to `convert_with_timestamps` with SDK retries disabled: one TTS request returns MP3 audio and character alignment. It decodes MP3 to a real 44.1 kHz mono WAV locally, converts alignment into word timestamps (preferring valid `normalized_alignment`, then `alignment`), and removes bracketed delivery tags without shifting spoken-word timing. Local transcription is used only when neither alignment is usable; a failed TTS request stops without replacing existing metadata or changing the provider/model. If decoding fails, retain the generated `.source-*.mp3` for recovery without paid resynthesis. Use an ElevenLabs SDK version that provides this method. The engine requires an explicit voice and records the selected model in `audio_meta.json`.
4. The shared engine writes voices to `video/assets/voice/`, BGM to `video/assets/bgm/`, SFX to `video/assets/sfx/`, and word timestamps to `audio_meta.json`. Consume the recorded paths; the maintained workspace entry point uses its separate `video/.media/audio/voice/` cache.

## Direct invocation

When using the direct path, send the full narration in one synthesis call. The example uses placeholder text; replace it with all approved narration in the production's language.

1. Use the ElevenLabs CLI or a Python script:

   ```bash
   elevenlabs text-to-speech convert \
     --voice-id <RESOLVED_VOICE_ID> \
     --model-id eleven_v4 \
     --text "<FULL_APPROVED_NARRATION_WITH_SCRIPT_SPECIFIC_AUDIO_TAGS>" \
     --output ./productions/<slug>/video/assets/audio/vo_full.mp3
   ```
2. The direct CLI example does not retrieve native alignment. Prefer the maintained entry point when timestamps are needed without additional transcription. For recorded audio or output without alignment, transcribe locally:

   ```bash
   npx hyperframes transcribe ./productions/<slug>/video/assets/audio/vo_full.mp3 --language id --dir ./productions/<slug>/video
   ```
