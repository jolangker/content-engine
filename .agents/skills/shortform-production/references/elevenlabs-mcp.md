# ElevenLabs MCP narration

Use this when the [transport check](audio.md#choose-the-elevenlabs-transport) selects MCP, or to import an existing production's finished MCP take with its downloaded MP3 and generation receipt.

## Generate one take

1. Prepare `video/audio_request.json` as in [audio generation](audio.md#maintained-workspace-synthesis-entry-point) and run `narration.py --check`. At `cached`, run `narration.py` without `--check` to refresh `audio_meta.json` from the cache (no API call) and stop. At `resume_cli`, finish the saved CLI take with `narration.py` instead of generating on MCP. At `awaiting_cli`, note its `request_sha256` and continue.
2. Call `creative_generate_speech` once with exactly `model_id: eleven_v4`, the resolved `voice_id`, the full tagged script as `prompt`, and `generations_count: 1` (optionally `flow_id`). The tool defaults to 2 variations; the import rejects any other count.
3. Poll `creative_get_flow_run_status` until it completes. Do not call the generation tool again to retry; a second call charges another take.
4. Read the finished generation with `creative_get_generations`, download its `full_res_url` to `video/narration-mcp.mp3`, and save the run receipt below as `video/audio_mcp_run.json`.
5. Import with `--auto-align` as below. It needs `faster-whisper`, `torch`, and `transformers`.

## Align and import

Use valid native character alignment when available. When MCP returns audio without word timestamps, run the maintained two-stage aligner + ASR script verifier (`faster-whisper` with silence padding + `Wav2Vec2` CTC forced alignment) instead of writing per-episode scripts:

```bash
python .agents/skills/shortform-production/scripts/align_narration.py --audio productions/<slug>/video/narration-mcp.mp3 --request productions/<slug>/video/audio_request.json --output productions/<slug>/video/audio_mcp_timings.json
```

Or pass `--auto-align` directly to `narration.py --import-mcp ... --audio ... --auto-align`. `align_narration.py` maps timestamps onto the exact spoken tokens of `audio_request.json` (preserving script casing/punctuation and stripping `[delivery tags]`) and fails if a delivery tag was spoken aloud, a number changed value, or edge words were clipped. For known phonetic loanwords, add `"asr_aliases": {"cherax": "seraks"}` in `audio_request.json`.

If supplying `--timings` explicitly, save `video/audio_mcp_timings.json` with the imported MP3's `audio_sha256` and either `words` or historical `normalized_alignment`/`alignment` character arrays:

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
