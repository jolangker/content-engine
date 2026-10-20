# Audio generation and resolution

Use this guide for the `audio` stage of short-form production: generate narration, sound effects (SFX), and background music (BGM), then establish actual duration and word timestamps for captions.

## 1. Audio stage completion criteria

The audio stage connects the script (`SCRIPT.md`) and visual storyboard (`STORYBOARD.md`) to the final HyperFrames animation:

- Convert scripted narration into audio files.
- Measure the full audio duration (`duration_s`) and each scene's time range to replace storyboard estimates.
- Produce word timestamps (alignment) for HyperFrames captions.
- Complete the stage when narration, BGM, and SFX each have an explicit use/none decision with a creative reason, all planned assets exist with measured durations, and scene timing is updated. A voice-only mix is valid when intentional; an empty SFX array by itself is not a decision.

## Sound design: plan, assemble, verify

Keep the production's sound decisions in `video/sound_design.json`, independently of narration requests and caches. Record each role's mode (`use` or `none`) and reason. For each SFX cue record its ID, scene, narrative purpose, exact visual/word trigger, local asset and provenance, composition start, duration, and initial gain. Add a readable cue table and intentional silence to `STORYBOARD.md`. Select cue density from the board and message, rather than adding an effect to every transition.

Resolve estimated cue times against measured narration and actual motion before assembly. Store the timing-file and placed-narration hashes in the plan; changed speech, pacing, or motion requires rechecking affected cues. Narration synthesis owns voice metadata only: preserve supplemental media records and mark existing sound design for timing revalidation. Its completion does not complete the whole audio stage.

Use `scripts/sound_design.py` from this skill for plans using local assets and top-level audio clips:

```bash
python .agents/skills/shortform-production/scripts/sound_design.py --video productions/<slug>/video --apply
python .agents/skills/shortform-production/scripts/sound_design.py --video productions/<slug>/video --check
python .agents/skills/shortform-production/scripts/sound_design.py --video productions/<slug>/video --export productions/<slug>/exports/<version>.mp4
```

`--apply` validates inputs, writes managed SFX clips, supplemental metadata and the storyboard cue table, and preserves narration and unrelated clips. Call it after a builder rewrites the composition. Include the audio `--check` preflight in project check/render wrappers when using this plan. `--check` fails on stale timing/narration, missing or altered assets, cue/track mismatches, hidden clips, or out-of-range timing. `--export` additionally uses cue waveform matching with a fitted narration residual on decoded MP4 audio; it writes evidence under `verification/`. This helper requires NumPy and FFmpeg and covers explicit local top-level SFX without per-cue FX or automation. Nested/processed cues need equivalent verification through their owning HyperFrames timeline and processed reference, not an unsupported success claim. The JSON plan carries `version`, `decisions`, `timing_sha256`, `narration_sha256`, `motion_sources` (scene path to `motion_digest` hash, ignoring editor identity stamps), `assets` (ID, path, SHA-256, source), and `cues` (ID, asset, scene, purpose, trigger, start, duration, volume, track).

Before rendering, reconcile every planned cue with its actual track and verify source hashes and audible source content. After rendering, verify the effects in the MP4 at their expected times, not just that an AAC stream exists. Check full-file decode, clipping/loudness and speech intelligibility alongside cue presence. Inspect the audiovisual result when playback is available; objective presence and level measurements do not prove perceptual balance. Record unavailable listening explicitly and present the file for listening without claiming human approval. Keep evidence tied to plan, composition, asset and export hashes so later edits invalidate it.

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

**Reuse first.** Inspect the selected board's sound library, existing production sound plans/media ledgers, and the bundled library at `.agents/skills/media-use/audio/assets/sfx/`. Choose by narrative function, timbre, intensity, duration and fit with narration. An existing suitable sound can serve several cues and productions; each episode still chooses its own placement and gain. A new episode does not require new SFX or a new treatment pass.

Copy the selected frozen file into the production and preserve its source, treatment, license/credits and content hash. Copying an existing asset for a self-contained render is reuse. Keep a useful treated variant in the owning board's `assets/audio/sfx/` with a manifest so later productions can reuse its exact bytes without processing it again. Other boards may reuse it when its actual sound fits their direction; availability alone is not creative fit.

When nothing suitable exists, source a suitable effect or adapt an existing one; use the `sound-effects` skill for a genuinely missing sound. Record the gap that justified new generation/treatment. Reuse the resulting asset on later episodes when appropriate. Preserve completed exports when only the reusable library or preparation policy changes.

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
3. **Update `TRACKER.json`**: If the requested endpoint is audio (`--until=audio` or equivalent), deliver the verified audio and timing metadata, record `stage: "audio"`, `status: "complete"` once any required review is resolved, and stop. Otherwise, once the audio stage is complete, set `stage: "production"` and `status: "in_progress"`.
4. Continue to the `production` stage to assemble scenes in HyperFrames only when it is within the resolved endpoint.
