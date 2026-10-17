import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { alignmentToWords, synthesizeOne } from './tts.mjs';

function alignment(text) {
  const characters = Array.from(text);
  return { characters, character_start_times_seconds: characters.map((_, i) => i / 10),
    character_end_times_seconds: characters.map((_, i) => (i + 1) / 10) };
}
test('character alignment groups Indonesian words, punctuation and paragraph breaks', () => {
  assert.deepEqual(alignmentToWords(alignment('Hai,\n kamu!')), [
    { text: 'Hai,', start: 0, end: 0.4 }, { text: 'kamu!', start: 0.6, end: 1.1 },
  ]);
});
test('missing, incomplete and nonmonotonic alignment requests local fallback', () => {
  for (const value of [null, {}, alignment('   '),
    { ...alignment('hi'), character_end_times_seconds: [1] },
    { ...alignment('hi'), character_start_times_seconds: [1, 0] },
    { ...alignment('hi'), character_end_times_seconds: [NaN, 1] }]) {
    assert.equal(alignmentToWords(value), null);
  }
});

test('ElevenLabs Python path makes one timestamp request, writes WAV, and returns native words or fallback', async () => {
  const root = mkdtempSync(join(tmpdir(), 'el-native-'));
  const saved = Object.fromEntries(['PYTHONPATH', 'ELEVENLABS_API_KEY', 'EL_TEST_MODE', 'EL_TEST_LOG'].map(k => [k, process.env[k]]));
  try {
    mkdirSync(join(root, 'elevenlabs'));
    writeFileSync(join(root, 'elevenlabs', '__init__.py'), '');
    writeFileSync(join(root, 'elevenlabs', 'client.py'), `
import os, json, base64
from types import SimpleNamespace
class Alignment:
    def model_dump(self):
        return {'characters':['H','a','i'], 'character_start_times_seconds':[0,0.1,0.2], 'character_end_times_seconds':[0.1,0.2,0.3]}
class TTS:
    def convert_with_timestamps(self, **kwargs):
        with open(os.environ['EL_TEST_LOG'], 'a') as f: f.write(json.dumps(kwargs) + '\\n')
        a = None if os.environ['EL_TEST_MODE'] == 'missing' else Alignment()
        return SimpleNamespace(audio_base_64=base64.b64encode(bytes(4410)).decode(), normalized_alignment=a, alignment=None)
class ElevenLabs:
    def __init__(self, **kwargs): self.text_to_speech = TTS()
`);
    process.env.PYTHONPATH = root;
    process.env.ELEVENLABS_API_KEY = 'synthetic-key';
    process.env.EL_TEST_LOG = join(root, 'calls.jsonl');
    for (const mode of ['native', 'missing']) {
      process.env.EL_TEST_MODE = mode;
      const wavAbs = join(root, mode, 'voice.wav');
      const result = await synthesizeOne({ provider: 'elevenlabs', text: 'Full script.\nSecond paragraph.', voiceId: 'test', model: 'test-model', wavAbs, hyperframesDir: root });
      assert.equal(result.ok, true, result.error);
      assert.equal(readFileSync(wavAbs).subarray(0, 4).toString(), 'RIFF');
      assert.deepEqual(result.words, mode === 'native' ? [{ text: 'Hai', start: 0, end: 0.3 }] : null);
    }
    const calls = readFileSync(process.env.EL_TEST_LOG, 'utf8').trim().split('\n').map(JSON.parse);
    assert.equal(calls.length, 2, 'one provider call per synthesis, including missing-alignment case');
    assert.ok(calls.every(c => c.text === 'Full script.\nSecond paragraph.' && c.model_id === 'test-model' && c.output_format === 'pcm_44100'));
  } finally {
    for (const [k,v] of Object.entries(saved)) { if (v === undefined) delete process.env[k]; else process.env[k] = v; }
    rmSync(root, { recursive: true, force: true });
  }
});
