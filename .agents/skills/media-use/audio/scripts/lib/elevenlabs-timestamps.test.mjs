import { test } from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { join, delimiter } from "node:path";
import { tmpdir } from "node:os";
import { fileURLToPath } from "node:url";
import { alignmentToWords, resolveVoiceId, synthesizeOne } from "./tts.mjs";

const alignment = text => ({
  characters: [...text],
  character_start_times_seconds: [...text].map((_, i) => i / 100),
  character_end_times_seconds: [...text].map((_, i) => (i + 1) / 100),
});

test("native words exclude delivery tags without shifting speech timing", () => {
  const text = "[warm] Halo [quiet] lo.";
  const words = alignmentToWords(alignment(text));
  assert.deepEqual(words.map(w => w.text), ["Halo", "lo."]);
  assert.equal(words[0].start, text.indexOf("Halo") / 100);
  assert.equal(words[1].start, text.indexOf("lo.") / 100);
});

test("malformed, nonfinite, reversed and empty native timings require transcription", () => {
  for (const value of [null, {}, { ...alignment("Halo"), character_end_times_seconds: [] },
    alignment("[warm]"), alignment("[unfinished"),
    ...[[-1, 1], [1, 0], [NaN, 1], [0, Infinity], [true, 1], [0, 0]].map(([start, end]) => ({
      characters: ["Halo"], character_start_times_seconds: [start], character_end_times_seconds: [end],
    }))]) assert.equal(alignmentToWords(value), null);
  const reversed = alignment("Hi");
  reversed.character_start_times_seconds = [.2, .1];
  reversed.character_end_times_seconds = [.3, .2];
  assert.equal(alignmentToWords(reversed), null);
});

test("ElevenLabs requires a resolved voice rather than silently choosing Rachel", async () => {
  await assert.rejects(resolveVoiceId({ provider: "elevenlabs" }), /explicit voice/);
  assert.equal(await resolveVoiceId({ provider: "elevenlabs", userVoice: "selected" }), "selected");
});

// Exercise the actual Python SDK bridge and engine CLI. A fixture module shadows
// the SDK, so these tests cannot contact ElevenLabs or consume synthesis credits.
const sdkFixture = `
import base64, json, os
from pathlib import Path
from types import SimpleNamespace
class Alignment:
    def __init__(self, data): self.data = data
    def model_dump(self): return self.data
class ElevenLabs:
    def __init__(self, **kwargs): self.text_to_speech = self
    def convert_with_timestamps(self, **kwargs):
        Path(os.environ['EL_TEST_LOG']).write_text(json.dumps(kwargs), encoding='utf-8')
        if os.environ.get('EL_TEST_MODE') == 'fail': raise RuntimeError('synthetic provider refusal')
        text = kwargs['text']
        data = {'characters': list(text),
                'character_start_times_seconds': [i / 100 for i in range(len(text))],
                'character_end_times_seconds': [(i + 1) / 100 for i in range(len(text))]}
        raw = None if os.environ.get('EL_TEST_MODE') == 'missing' else Alignment(data)
        normalized = Alignment({'characters': ['bad']}) if os.environ.get('EL_TEST_MODE') == 'raw' else raw
        audio = Path(os.environ['EL_TEST_AUDIO']).read_bytes()
        if os.environ.get('EL_TEST_MODE') == 'decode-fail': audio = b'invalid mp3'
        return SimpleNamespace(audio_base_64=base64.b64encode(audio).decode(),
                               normalized_alignment=normalized, alignment=raw)
`;

async function fixture(run) {
  const root = mkdtempSync(join(tmpdir(), "el-native-test-"));
  const keys = ["PYTHONPATH", "ELEVENLABS_API_KEY", "EL_TEST_AUDIO", "EL_TEST_LOG", "EL_TEST_MODE"];
  const saved = keys.map(key => [key, process.env[key]]);
  try {
    mkdirSync(join(root, "elevenlabs"));
    writeFileSync(join(root, "elevenlabs", "__init__.py"), "");
    writeFileSync(join(root, "elevenlabs", "client.py"), sdkFixture);
    const mp3 = join(root, "fixture.mp3");
    const ff = spawnSync("ffmpeg", ["-y", "-loglevel", "error", "-f", "lavfi", "-i",
      "anullsrc=r=44100:cl=mono", "-t", "1", mp3], { encoding: "utf8" });
    assert.equal(ff.status, 0, ff.stderr || String(ff.error));
    process.env.PYTHONPATH = root + (saved[0][1] ? delimiter + saved[0][1] : "");
    process.env.ELEVENLABS_API_KEY = "synthetic-not-a-real-key";
    process.env.EL_TEST_AUDIO = mp3;
    process.env.EL_TEST_LOG = join(root, "request-log.json");
    delete process.env.EL_TEST_MODE;
    await run(root);
  } finally {
    for (const [key, value] of saved) {
      if (value === undefined) delete process.env[key]; else process.env[key] = value;
    }
    rmSync(root, { recursive: true, force: true });
  }
}

test("SDK bridge forwards eleven_v4, produces real WAV and prefers valid native alignment", async () => {
  await fixture(async root => {
    process.env.EL_TEST_MODE = "raw";
    const wavAbs = join(root, "voice.wav");
    const result = await synthesizeOne({ provider: "elevenlabs", voiceId: "chosen-voice",
      text: "[warm] Halo lo.", wavAbs, hyperframesDir: root, model: "eleven_v4" });
    assert.equal(result.ok, true, result.error);
    assert.deepEqual(result.words.map(w => w.text), ["Halo", "lo."]);
    assert.equal(readFileSync(wavAbs).toString("ascii", 0, 4), "RIFF");
    const request = JSON.parse(readFileSync(process.env.EL_TEST_LOG, "utf8"));
    assert.equal(request.model_id, "eleven_v4");
    assert.equal(request.voice_id, "chosen-voice");
    assert.equal(request.text, "[warm] Halo lo.");
    assert.equal(request.output_format, "mp3_44100_128");
    assert.equal(request.request_options.max_retries, 0);
    // The shared adapter honors an explicit caller model; project intake is
    // responsible for restricting productions to eleven_v4 before this layer.
    const override = await synthesizeOne({ provider: "elevenlabs", voiceId: "chosen-voice",
      text: "Halo", wavAbs: join(root, "override.wav"), hyperframesDir: root, model: "test-explicit-model" });
    assert.equal(override.ok, true, override.error);
    assert.equal(JSON.parse(readFileSync(process.env.EL_TEST_LOG, "utf8")).model_id, "test-explicit-model");
  });
});

test("missing alignment retains successful audio for local transcription", async () => {
  await fixture(async root => {
    process.env.EL_TEST_MODE = "missing";
    const wavAbs = join(root, "voice.wav");
    assert.deepEqual(await synthesizeOne({ provider: "elevenlabs", voiceId: "chosen",
      text: "Halo", wavAbs, hyperframesDir: root }), { ok: true, words: null });
    assert.equal(readFileSync(wavAbs).toString("ascii", 0, 4), "RIFF");
    assert.equal(JSON.parse(readFileSync(process.env.EL_TEST_LOG, "utf8")).model_id, "eleven_v4");
  });
});

test("failed local decoding preserves the synthesized MP3 for recovery", async () => {
  await fixture(async root => {
    process.env.EL_TEST_MODE = "decode-fail";
    const result = await synthesizeOne({ provider: "elevenlabs", voiceId: "chosen",
      text: "Halo", wavAbs: join(root, "voice.wav"), hyperframesDir: root });
    assert.equal(result.ok, false);
    const source = readdirSync(root).find(name => name.startsWith("voice.wav.source-"));
    assert.ok(source);
    assert.equal(readFileSync(join(root, source), "utf8"), "invalid mp3");
  });
});

test("shared engine records eleven_v4 and stops on provider failure without replacing metadata", async () => {
  await fixture(async root => {
    const requestPath = join(root, "audio_request.json");
    const metaPath = join(root, "audio_meta.json");
    writeFileSync(requestPath, JSON.stringify({ provider: "elevenlabs", voice: "chosen",
      tts_model: "eleven_v4", lang: "id", lines: [{ id: "narration", text: "[warm] Halo lo." }] }));
    const engine = fileURLToPath(new URL("../audio.mjs", import.meta.url));
    const invoke = () => spawnSync(process.execPath, [engine, "--hyperframes", root,
      "--request", requestPath, "--only", "tts"], { encoding: "utf8", timeout: 30000 });
    const success = invoke();
    assert.equal(success.status, 0, success.stdout + success.stderr);
    const meta = JSON.parse(readFileSync(metaPath, "utf8"));
    assert.equal(meta.tts_model, "eleven_v4");
    assert.equal(meta.tts_provider, "elevenlabs");
    assert.deepEqual(meta.voices[0].words.map(w => w.text), ["Halo", "lo."]);
    const before = readFileSync(metaPath, "utf8");
    process.env.EL_TEST_MODE = "fail";
    const failure = invoke();
    assert.equal(failure.status, 1, failure.stdout + failure.stderr);
    assert.match(failure.stderr, /narration is incomplete/);
    assert.equal(readFileSync(metaPath, "utf8"), before);
    assert.ok(existsSync(join(root, meta.voices[0].path)));
  });
});
