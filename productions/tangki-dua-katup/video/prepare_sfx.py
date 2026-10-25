"""Freeze reused sound textures and restrained, reproducible cue treatments.

No network, synthesis or narration changes. Run from any working directory.
These are illustrative material cues, not recordings of the depicted cistern.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import wave
import numpy as np

V = Path(__file__).resolve().parent
R = V.parents[2]
OUT = V / 'assets/audio/sfx'
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / 'sources'
RAW.mkdir(exist_ok=True)
PREV = R / 'productions/rel-bukan-dua-batang-besi/video/assets/audio/sfx'
BUNDLE = R / '.agents/skills/media-use/audio/assets/sfx'
RATE = 48000


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def decode(path, filters='anull'):
    cp = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-af', filters,
                         '-ar', str(RATE), '-ac', '1', '-f', 'f32le', '-'],
                        check=True, stdout=subprocess.PIPE)
    return np.frombuffer(cp.stdout, dtype='<f4').copy()


def onset(x, threshold_db=-40):
    # Keep 8 ms before the first supported onset; do not align to file silence.
    peak = float(np.max(np.abs(x)))
    idx = np.flatnonzero(np.abs(x) >= peak * 10 ** (threshold_db / 20))
    return max(0, int(idx[0]) - int(.008 * RATE)) if len(idx) else 0


def crossfade_repeat(x, duration, crossfade=.16):
    n = round(duration * RATE)
    k = min(round(crossfade * RATE), len(x)//4)
    out = x.copy()
    while len(out) < n:
        blend = np.linspace(0, 1, k, endpoint=False)
        out = np.concatenate((out[:-k], out[-k:] * (1-blend) + x[:k] * blend, x[k:]))
    return out[:n]


def write_pcm(path, x, peak_db, fade_out=.04):
    x = x.copy()
    peak = float(np.max(np.abs(x)))
    if not peak:
        raise ValueError('silent source')
    x *= 10**(peak_db/20) / peak
    a = min(round(.004*RATE), len(x)//4)
    b = min(round(fade_out*RATE), len(x)//4)
    x[:a] *= np.linspace(0, 1, a)
    x[-b:] *= np.linspace(1, 0, b)
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(np.clip(np.round(x*32767), -32768, 32767).astype('<i2').tobytes())
    return len(x)/RATE


specs = [
    dict(id='handle-contact', src=PREV/'chair.mp3', receipt=PREV/'chair.request.json',
         filters='highpass=f=180,lowpass=f=4200', length=.52, peak=-12,
         role='stylized material interaction',
         intent='Restrained short hinge/latch movement for the lever press and return; not literal toilet-handle recording.'),
    dict(id='chain-contact', src=PREV/'clip-seat.wav', receipt=PREV/'clip-seat.request.json',
         filters='highpass=f=900,lowpass=f=6500', length=.22, peak=-16,
         role='stylized material interaction',
         intent='Thin brief metallic contact to mark chain take-up or engagement; not a continuous chain-rattle claim.'),
    dict(id='rubber-seat', src=PREV/'splash.mp3', receipt=PREV/'splash.request.json',
         filters='highpass=f=110,lowpass=f=1300', length=.38, peak=-13,
         role='stylized wet-contact accent',
         intent='Soft low wet contact accent at flap reseating; adapted puddle Foley, not actual flapper acoustics.'),
    dict(id='water-flow', src=PREV/'drain-water.mp3', receipt=PREV/'drain-water.request.json',
         filters='highpass=f=140,lowpass=f=6000', length=12.0, peak=-16,
         role='illustrative physical water texture', repeat=True,
         intent='Close small-stream water texture for sustained tank discharge or overflow; shortened in placement to follow motion.'),
    dict(id='water-refill', src=PREV/'drain-water.mp3', receipt=PREV/'drain-water.request.json',
         filters='highpass=f=550,lowpass=f=8500', length=12.0, peak=-18,
         role='illustrative physical water texture', repeat=True, offset=.55,
         intent='Lighter filtered water texture for incoming refill, distinct from the fuller discharge bed; source is a generated small stream.'),
    dict(id='section-reveal', src=BUNDLE/'whoosh-short.mp3', receipt=None,
         filters='highpass=f=650,lowpass=f=4500', length=.42, peak=-23,
         role='editorial guidance',
         intent='Quiet airy cutaway/reassembly cue; never used to imply a physical internal mechanism sound.'),
]

assets=[]
for s in specs:
    src=s['src']
    raw=RAW/src.name
    # Same filename shared by flow/refill denotes the same exact source bytes.
    if raw.exists() and sha(raw)!=sha(src):
        raise ValueError('source filename conflict')
    shutil.copyfile(src, raw)
    receipt=None
    if s['receipt']:
        receipt=json.loads(s['receipt'].read_text(encoding='utf-8'))
        shutil.copyfile(s['receipt'], RAW/s['receipt'].name)
        # WAV treatment source hashes differ from original MP3 generation receipts.
        original=src.with_suffix('.mp3')
        if original.exists() and receipt.get('audio_sha256') != sha(original):
            raise ValueError('historical generation receipt does not match '+src.name)
        if original.exists() and original.name != raw.name:
            shutil.copyfile(original, RAW/original.name)
    x=decode(src,s['filters'])
    start=onset(x)+round(s.get('offset',0)*RATE)
    x=x[start:]
    if s.get('repeat'):
        x=crossfade_repeat(x,s['length'])
    else:
        x=x[:round(s['length']*RATE)]
    target=OUT/(s['id']+'.wav')
    duration=write_pcm(target,x,s['peak'],.12 if s.get('repeat') else .035)
    source=dict(path=str(src.relative_to(R)).replace('\\','/'),
                frozen_source=str(raw.relative_to(V)).replace('\\','/'),
                sha256=sha(src),
                provider='elevenlabs historical generated SFX' if receipt else 'bundled Pixabay SFX',
                license='Historical project-generated ElevenLabs asset; retained original request receipt' if receipt else 'Pixabay Content License',
                url='https://elevenlabs.io/terms-of-use' if receipt else 'https://pixabay.com/service/license-summary/',
                role=s['role'],intent=s['intent'])
    if receipt:
        source['original_request_sha256']=receipt['request_sha256']
        source['original_prompt']=receipt.get('payload',receipt.get('request',{})).get('text','')
    assets.append(dict(id=s['id'],path=str(target.relative_to(V)).replace('\\','/'),
                       sha256=sha(target),duration_s=round(duration,6),source=source,
                       treatment=dict(filters=s['filters'],trim_start_s=round(start/RATE,6),
                                      repeated_with_crossfade=bool(s.get('repeat')),peak_dbfs=s['peak'],
                                      sample_rate=RATE,channels=1)))

(OUT/'assets.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
notes=['# Reused sound assets','',
       'No new paid sound generation. No narration regeneration. These are designed illustrative textures and material accents, not a field recording or calibrated acoustic simulation of the depicted cistern.', '',
       'Reuse scan: board v4 has no frozen sound library; bundled library has UI/impact/whoosh textures, no water. Existing rail episode has generated water and material Foley with matching receipts. Openverse resolver queries for small metal chain rattle and rubber flap returned bundled pop/click-soft, rejected as literal Foley. Those fetched candidates are unused.', '',
       'Playback listening is unavailable to this helper. Waveform/onset, duration, source receipt and hash checks were performed; perceptual approval is not claimed. Root must verify the placed mix and its export.', '',
       'The source snippets are retained under `assets/audio/sfx/sources/`. Prior generated sources retain their original prompts and hashes. Their applicability here is an editorial timbre choice, not evidence of the mechanism\'s sound. Bundled whoosh is sourced under the Pixabay Content License; attribution is not required by that license.', '',
       '| Asset | Duration | Role / use |', '|---|---:|---|']
for a in assets:
    notes.append(f"| `{a['id']}` | {a['duration_s']:.3f}s | {a['source']['intent']} |")
notes+=['','## Sources','',
        '- Prior production: `productions/rel-bukan-dua-batang-besi/video/assets/audio/sfx/`, original ElevenLabs `eleven_text_to_sound_v2` generated assets and request receipts. Reused water was generated as a small stream in a concrete drainage channel; flow/refill are cropped, filtered and crossfaded adaptations.',
        '- Bundled `whoosh-short.mp3`: `.agents/skills/media-use/audio/assets/sfx/CREDITS.md`; [Pixabay Content License](https://pixabay.com/service/license-summary/).',
        '- [ElevenLabs terms](https://elevenlabs.io/terms-of-use) retained as provider reference; no assertion of CC0 licensing for generated assets.', '',
        'Exact treatment commands, input/output hashes, durations and source prompts are recorded in `assets/audio/sfx/assets.json`.']
(V/'SFX_SOURCES.md').write_text('\n'.join(notes)+'\n',encoding='utf-8')
shutil.copyfile(BUNDLE/'CREDITS.md', RAW/'BUNDLED_CREDITS.md')
print(json.dumps([dict(id=a['id'],path=a['path'],duration_s=a['duration_s'],sha256=a['sha256']) for a in assets],indent=2))
