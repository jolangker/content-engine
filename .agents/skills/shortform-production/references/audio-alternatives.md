# Audio integration compatibility

Read for timing recovery or historical production recordings. Use the maintained [ElevenLabs CLI workflow](audio.md#voiceover-elevenlabs) for new narration.

## Recover timing for a saved CLI take

If `narration.py` reports a saved CLI take with invalid timing, align the exact MP3 it names. Run `elevenlabs forced-alignment create` with the MP3 and approved spoken text with delivery tags removed, or use local alignment from the media-use [TTS-to-captions guidance](../../media-use/audio/references/tts-to-captions.md). Inspect the measured words against the approved text in the production language.

Write timing JSON with the MP3's SHA-256 and measured word start/end times in seconds, for example `{"audio_sha256": "<MP3_SHA256>", "words": [{"text": "Halo", "start": 0.0, "end": 0.4}]}`. Pass the file to `narration.py --video ... --timings ...` to validate the saved take and finish the cache. If a run was interrupted and left `.media/audio/voice/.narration.lock`, confirm the process has exited before clearing the empty lock directory and rerunning. Check ElevenLabs history for a completed take if the process ended before saving a response.

## Reuse historical recordings

Consume the recorded paths in `audio_meta.json`, including legacy media under `video/assets/voice/`, `video/assets/bgm/`, and `video/assets/sfx/`. For an already downloaded MCP take with a completed run receipt, use [legacy import](elevenlabs-mcp.md).
