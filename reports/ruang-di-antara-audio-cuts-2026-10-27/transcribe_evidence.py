"""Offline independent ASR of preserved source recordings; never alters productions."""
from pathlib import Path
import json
import os
import subprocess
import time

os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'

import numpy as np
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

model = WhisperModel('large-v3', device='cpu', compute_type='int8',
                     cpu_threads=8, local_files_only=True)
jobs = [
    ('terima-kasih-yang-melihat', 0, None),
    ('gua-kira-udah-kelihatan', 32, 39),
    ('coba-hal-baru-berdua', 32, 38),
]
results = []
for slug, start, end in jobs:
    video = ROOT / 'productions' / slug / 'video'
    placement = json.loads((video / 'placement.json').read_text(encoding='utf-8'))
    source = video / placement['source']
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(source),
                          '-ar', '16000', '-ac', '1', '-f', 'f32le', 'pipe:1'],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, dtype='<f4').copy()
    audio = audio[round(start * 16000):None if end is None else round(end * 16000)]
    begun = time.time()
    segments, info = model.transcribe(audio, language='id', word_timestamps=True,
                                      beam_size=5, vad_filter=False,
                                      condition_on_previous_text=False)
    words, text = [], []
    for seg in segments:
        text.append(seg.text)
        words.extend({'text': w.word.strip(), 'start': round(w.start + start, 4),
                      'end': round(w.end + start, 4), 'probability': w.probability}
                     for w in seg.words)
    record = {'slug': slug, 'source': str(source.relative_to(ROOT)),
              'crop_start': start, 'crop_end': end, 'model': 'cached faster-whisper-large-v3',
              'device': 'cpu', 'compute_type': 'int8', 'language': 'id',
              'elapsed_s': time.time() - begun, 'text': ''.join(text), 'words': words,
              'limitation': 'Independent ASR estimates, not perceptual listening or phoneme-level ground truth.'}
    results.append(record)
    (OUT / 'independent-asr.json').write_text(json.dumps(results, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'slug': slug, 'elapsed_s': record['elapsed_s'], 'word_count': len(words), 'text': record['text']}, ensure_ascii=True), flush=True)
