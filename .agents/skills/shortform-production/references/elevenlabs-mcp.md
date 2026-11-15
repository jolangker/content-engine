# ElevenLabs MCP execution and import

Read when generating or importing narration. [Audio generation](audio.md#voiceover-elevenlabs) owns the approved text, provider/model, voice precedence, and editorial checks. Use the connected `mcp__elevenlabs` tools; the local helper prepares/imports output and cannot call an agent's MCP tools itself. MCP owns authentication. The root `.env` voice ID remains configuration.

## Prepare and run

1. Run `narration.py --video productions/<slug>/video --check` from the project root. A cache hit reuses the verified recording: run without `--check` to restore metadata if needed. `awaiting_mcp` supplies `mcp_call.arguments`; `resume_mcp` supplies existing flow/session IDs. Recover an incomplete cache from saved output before considering authorized regeneration.
2. Resolve the configured voice against `creative_list_voices` before a fresh generation. Use IDs returned by that tool or explicitly supplied by the user. Preserve the configured selection; an unavailable voice is a blocker, not permission to substitute one. For a user-requested new voice, choose a fitting catalog voice and record it in board/episode configuration. Confirm `eleven_v4` availability with `creative_get_flow_node_types`; use `creative_get_model_guide` when needed. The connected tool schema is authoritative: the local OSS MCP server's `text_to_speech` interface differs from this connector.
3. Call `creative_generate_speech` once with the prepared `model_id`, `voice_id`, full tagged `prompt`, and explicit `generations_count: 1`. Every new narration call produces exactly one take; omitting this field invokes the connector's two-take default. Reuse an existing production flow when combining generated assets. The simple speech tool exposes neither seed nor voice settings nor language/output-format parameters: keep the script in the chosen language and resolve unsupported settings before generating.
4. Immediately save `video/audio_mcp_run.json` with `request_sha256`, `tool`, exact `arguments`, `flow_id`, `node_id`, all returned `session_ids`, and the initial structured result as `response`. On interruption, resume that run. If a timeout returns no IDs, inspect existing flows/results before deciding whether anything was generated.
5. If the rendered view tracks progress, let it finish; otherwise poll `creative_get_flow_run_status` with the saved flow and all sessions, respecting `poll_after_seconds`. Polling continues the same run. Never repeat generation as a status check or automatic retry. Preserve provider/voice/model on failure and report the failed run.
6. Save the completed structured result as `response`. Choose the authorized take, recording its `generation_id` and selection reason in `EPISODE.md`. Download its `media[].master_url` (or `media[].url` / matching `generations[].content_url`) promptly into `video/`; these URLs expire. Preserve this local output for recovery. If needed, convert locally to a real MP3, preserving the original and conversion provenance. Record the imported MP3's SHA-256 as `audio_sha256`.

Review the single take under the production's existing review policy. Retain historical variation IDs when recovering an older run; reuse its output without starting another generation. When a take feeds another MCP node, pin it with `creative_add_flow_asset_node` using the generation ID and connect that returned node in the same flow.

## Align and import

Use valid native character alignment when provided; otherwise transcribe/align the exact downloaded recording through [local timing recovery](audio-alternatives.md). Keep words free of delivery tags, with finite monotonic start/end times in seconds within the recording duration. Check wording/timing against the accepted script. Never synthesize again to obtain timestamps.

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

The helper validates current voice provenance, request/arguments, selected finished media, file hashes, MP3 duration, and timing before creating the cache and metadata. Cache receipts keep stable MCP IDs and omit signed URLs. `audio_meta.json` retains the existing voices/SFX/BGM contract and adds `tts_transport: elevenlabs_mcp` plus MCP provenance. Failed validation preserves previous metadata and downloaded output; fix/reimport locally. Archive working receipts when replacing an authorized request so their run IDs remain recoverable.

Complete when the helper returns `status: ready`, required listening/alignment review is recorded, and [the audio-stage handoff](audio.md#files-and-handoff) is satisfied. A prepared call, running flow, or downloaded file alone is not completed audio.
