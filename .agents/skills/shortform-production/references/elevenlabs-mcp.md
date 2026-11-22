# Legacy ElevenLabs narration import

Use this offline import when an existing production has a finished MCP take, downloaded MP3, and completed generation receipt. Use the [CLI workflow](audio.md#voiceover-elevenlabs) for new takes.

## Align and import

Use valid native character alignment when available. For missing timing, [align the exact recording](audio-alternatives.md#recover-timing-for-a-saved-cli-take). Check the measured wording and timing against the approved script.

Save `video/audio_mcp_timings.json` with the imported MP3's `audio_sha256` and either `words` or historical `normalized_alignment`/`alignment` character arrays:

```json
{
  "audio_sha256": "<DOWNLOADED_MP3_SHA256>",
  "words": [{"text": "Halo", "start": 0.12, "end": 0.46}]
}
```

The completed run receipt has this shape. The example abbreviates `response`; save the full actual structured result, including all variations:

```json
{
  "request_sha256": "<FROM_HELPER>",
  "tool": "creative_generate_speech",
  "arguments": {"model_id": "eleven_v4", "voice_id": "<RESOLVED_ID>", "prompt": "<FULL_TAGGED_SCRIPT>", "generations_count": 1},
  "flow_id": "<RETURNED_FLOW>",
  "node_id": "<RETURNED_NODE>",
  "session_ids": ["<RETURNED_SESSION>"],
  "generation_id": "<SELECTED_GENERATION>",
  "audio_sha256": "<DOWNLOADED_MP3_SHA256>",
  "response": {"media": [{"generation_id": "<SELECTED_GENERATION>", "kind": "audio", "model_id": "eleven_v4", "voice": {"voice_id": "<RESOLVED_ID>"}}]}
}
```

Import from the project root:

```bash
python .agents/skills/shortform-production/scripts/narration.py --video productions/<slug>/video --import-mcp productions/<slug>/video/audio_mcp_run.json --audio productions/<slug>/video/narration-mcp.mp3 --timings productions/<slug>/video/audio_mcp_timings.json
```

The helper validates the saved take and timing, then records stable MCP IDs and `tts_transport: elevenlabs_mcp` in the cache and metadata. On validation failure, correct the receipt or timing and reimport the saved audio.

Finish with `status: ready`, the required listening and alignment review, and the [audio-stage handoff](audio.md#files-and-handoff).
