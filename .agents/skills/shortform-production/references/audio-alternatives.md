# Audio integration compatibility

Read for historical shared-engine output or local alignment recovery. New narration uses [ElevenLabs MCP execution and import](elevenlabs-mcp.md); direct ElevenLabs SDK, REST, CLI, and the generic media-use TTS runner are no longer production synthesis paths. Keep installed media-use files unchanged and pass this project policy as run context.

Existing valid recordings, request receipts, native character alignment, and `audio_meta.json` remain usable at their recorded paths. The maintained helper accepts both historical native alignment and measured word arrays. Reuse completed media before generating again; an integration change alone does not authorize resynthesis.

When an MCP output lacks timing, transcribe/align the downloaded recording locally with media-use's [TTS-to-captions guidance](../../media-use/audio/references/tts-to-captions.md). Use the production language and inspect the resulting words against the approved spoken script. Normalize output into `{"audio_sha256": "<DOWNLOADED_FILE_SHA256>", "words": [{"text": "...", "start": 0.0, "end": 0.4}]}` for import. Obtain real word timestamps; segment-level estimates are insufficient. Read the current HyperFrames CLI docs before a CLI-based recovery.

Historical shared-engine recordings may live under `video/assets/voice/`, BGM under `video/assets/bgm/`, and SFX under `video/assets/sfx/`. Consume the paths recorded in `audio_meta.json`; do not relocate valid files merely to match the helper's `video/.media/audio/voice/` cache. An uncached historical recording can continue in its existing production, but cannot be relabeled as an MCP generation without real MCP provenance.
