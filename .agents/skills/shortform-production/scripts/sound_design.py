"""Apply and verify local, top-level SFX plans without synthesizing narration."""
import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
import subprocess


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def motion_digest(path):
    # HyperFrames check stamps editor identities without changing motion.
    text = Path(path).read_text(encoding='utf-8')
    text = re.sub(r'\s+data-hf-id=(?:"[^"]*"|\x27[^\x27]*\x27)', '', text)
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def local_file(video, name):
    path = (video / name).resolve()
    if not path.is_relative_to(video.resolve()) or not path.is_file():
        raise ValueError(f'Missing/out-of-project asset: {name}')
    return path


class AudioHTML(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.audio = []
        self.duration = None
        self.ids = []
        self.hidden = []
        self.stack = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.append(a['id'])
        hidden = ('hidden' in a or 'data-hidden' in a and a['data-hidden'] != 'false'
                  or any(k in a.get('style', '').replace(' ', '').lower()
                         for k in ['display:none', 'visibility:hidden']))
        inherited = any(h for _, h in self.stack)
        if self.duration is None and 'data-composition-id' in a and 'data-duration' in a:
            self.duration = float(a['data-duration'])
        if tag == 'audio':
            self.audio.append(a)
            if hidden or inherited:
                self.hidden.append(a.get('id'))
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append((tag, hidden or inherited))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


def decode(path, rate=48000):
    import numpy as np
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-vn', '-ac', '1', '-ar', str(rate),
                        '-f', 'f32le', 'pipe:1'], capture_output=True, check=True)
    samples = np.frombuffer(r.stdout, dtype='<f4').astype(float)
    if not len(samples) or not np.isfinite(samples).all() or not np.any(samples):
        raise ValueError(f'Empty, silent or invalid audio: {path}')
    return samples


def inputs(video):
    video = Path(video).resolve()
    if (video / 'audio_boundaries.json').exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location('narration_boundary_check', Path(__file__).with_name('audio_boundaries.py'))
        boundary_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(boundary_module)
        boundary_module.verify(video)
    plan = read_json(video / 'sound_design.json')
    text = (video / 'index.html').read_text(encoding='utf-8')
    parsed = AudioHTML(text)
    if plan.get('version') != 1 or parsed.duration is None:
        raise ValueError('Expected plan version 1 and a finite composition duration')
    if len(parsed.ids) != len(set(parsed.ids)):
        raise ValueError('Duplicate composition IDs')
    for role in ('narration', 'bgm', 'sfx'):
        d = plan['decisions'][role]
        if d.get('mode') not in ('use', 'none') or not d.get('reason', '').strip():
            raise ValueError(f'Unresolved {role} decision')
    if plan['timing_sha256'] != digest(video / 'timing.json'):
        raise ValueError('Stale cue timing: revalidate against timing.json')
    for name, expected in plan.get('motion_sources', {}).items():
        if motion_digest(local_file(video, name)) != expected:
            raise ValueError(f'Stale motion trigger: revalidate {name}')
    voice = next((a for a in parsed.audio if a.get('id') == 'narration'), None)
    if plan['decisions']['narration']['mode'] == 'use':
        if not voice or plan['narration_sha256'] != digest(local_file(video, voice['src'])):
            raise ValueError('Stale/missing placed narration: revalidate cue timing')
    assets = {a['id']: a for a in plan['assets']}
    if len(assets) != len(plan['assets']):
        raise ValueError('Duplicate asset IDs')
    for asset in assets.values():
        if not asset.get('source') or digest(local_file(video, asset['path'])) != asset['sha256']:
            raise ValueError(f'Changed asset or missing provenance: {asset["id"]}')
        decode(local_file(video, asset['path']))
    cues = plan['cues']
    if (plan['decisions']['sfx']['mode'] == 'use') != bool(cues):
        raise ValueError('SFX decision does not match cues')
    if len({c['id'] for c in cues}) != len(cues):
        raise ValueError('Duplicate cue IDs')
    for c in cues:
        for key in ('scene', 'purpose', 'trigger'):
            if not c.get(key):
                raise ValueError(f'Cue {c["id"]} needs {key}')
        if not re.fullmatch(r'sfx-[a-z0-9-]+', c['id']) or c['asset'] not in assets:
            raise ValueError('Cue requires a unique sfx-* ID and known asset')
        nums = [float(c[k]) for k in ('start', 'duration', 'volume')]
        if not all(math.isfinite(n) for n in nums):
            raise ValueError('Cue values must be finite')
        start, duration, volume = nums
        source_duration = len(decode(local_file(video, assets[c['asset']]['path']))) / 48000
        if start < 0 or duration <= 0 or volume <= 0 or volume > 4 or start + duration > parsed.duration + .001:
            raise ValueError(f'Invalid cue timing/gain: {c["id"]}')
        if duration > source_duration + .025:
            raise ValueError(f'Cue exceeds source duration: {c["id"]}')
    return plan, text, parsed, assets


def apply_plan(video):
    video = Path(video).resolve()
    plan, text, parsed, assets = inputs(video)
    # Replace only this helper's block and explicitly adopted legacy IDs.
    text = re.sub(r'\n?<!-- sound-design:start -->.*?<!-- sound-design:end -->\n?', '\n', text, flags=re.S)
    for cue_id in plan.get('replaces', []):
        text = re.sub(r'<audio\b(?=[^>]*\bid="' + re.escape(cue_id) + r'")[^>]*>\s*</audio>\s*', '', text)
    clips = []
    for c in plan['cues']:
        attrs = {'id': c['id'], 'src': assets[c['asset']]['path'], 'data-start': c['start'],
                 'data-duration': c['duration'], 'data-volume': c['volume'],
                 'data-track-index': c.get('track', 4), 'data-audio-group': 'sfx'}
        clips.append('<audio ' + ' '.join(f'{k}="{html.escape(str(v), quote=True)}"' for k, v in attrs.items()) + '></audio>')
    block = '\n<!-- sound-design:start -->\n' + '\n'.join(clips) + '\n<!-- sound-design:end -->\n'
    if plan['decisions']['narration']['mode'] == 'use':
        text, n = re.subn(r'(<audio\b(?=[^>]*\bid="narration")[^>]*>\s*</audio>)', lambda m: m[0] + block, text, count=1)
        if n != 1:
            raise ValueError('Cannot locate top-level narration insertion point')
    else:
        text = text.replace('</body>', block + '</body>')
    meta = read_json(video / 'audio_meta.json') if (video / 'audio_meta.json').exists() else {}
    meta['sfx'] = [{**c, 'file': assets[c['asset']]['path']} for c in plan['cues']]
    meta['sound_design'] = {'path': 'sound_design.json', 'sha256': digest(video / 'sound_design.json'), 'needs_revalidation': False}
    (video / 'index.html').write_text(text, encoding='utf-8')
    (video / 'audio_meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    storyboard = video / 'STORYBOARD.md'
    if storyboard.exists():
        board = storyboard.read_text(encoding='utf-8')
        board = re.sub(r'\n?<!-- sound-cues:start -->.*?<!-- sound-cues:end -->\n?', '\n', board, flags=re.S)
        lines = ['\n<!-- sound-cues:start -->', '## Current sound cues', '',
                 'Authority: [sound_design.json](sound_design.json). BGM: ' + plan['decisions']['bgm']['mode']
                 + ' — ' + plan['decisions']['bgm']['reason'], '',
                 '| Cue | Scene | Main time (s) | Asset | Gain | Purpose / trigger |',
                 '| --- | --- | --- | --- | --- | --- |']
        for c in plan['cues']:
            values = [c['id'], c['scene'], f'{c["start"]:.3f}', c['asset'], c['volume'], c['trigger']]
            lines.append('| ' + ' | '.join(str(v).replace('|', '\\|') for v in values) + ' |')
        lines.extend(['', 'Intentional silence: ' + plan.get('silence', plan['decisions']['sfx']['reason']),
                      '<!-- sound-cues:end -->', ''])
        storyboard.write_text(board.rstrip() + '\n' + '\n'.join(lines), encoding='utf-8')
    return check_plan(video)


def check_plan(video):
    plan, text, parsed, assets = inputs(video)
    actual = {a['id']: a for a in parsed.audio if a.get('id', '').startswith('sfx-') or a.get('data-audio-group') == 'sfx'}
    if set(actual) != {c['id'] for c in plan['cues']}:
        raise ValueError('Planned SFX do not match placed SFX IDs')
    for c in plan['cues']:
        a = actual[c['id']]
        if a.get('src') != assets[c['asset']]['path'] or c['id'] in parsed.hidden:
            raise ValueError(f'Missing/hidden/mismatched source: {c["id"]}')
        if any(a.get(k) for k in ('data-fx-chain', 'data-automation', 'data-playback-rate', 'data-media-start')):
            raise ValueError('Processed cues need a processed reference verifier')
        for attr, field in [('data-start', 'start'), ('data-duration', 'duration'), ('data-volume', 'volume')]:
            if abs(float(a.get(attr, -1)) - c[field]) > .001:
                raise ValueError(f'Cue/track mismatch: {c["id"]} {field}')
    return {'status': 'passed', 'cues': len(plan['cues']), 'plan_sha256': digest(Path(video) / 'sound_design.json'),
            'composition_sha256': digest(Path(video) / 'index.html'), 'listening': 'not established by automated checks'}


def verify_export(video, export):
    """Detect each frozen cue near its planned time; fail if absent or materially retimed."""
    import numpy as np
    report = check_plan(video)
    plan, _, parsed, assets = inputs(video)
    signal = decode(export)
    voice_clip = next((a for a in parsed.audio if a.get('id') == 'narration'), None)
    voice_reference = np.zeros(len(signal))
    if voice_clip:
        if float(voice_clip.get('data-playback-rate', 1)) != 1:
            raise ValueError('Retimed voice needs a retimed reference for export verification')
        voice = decode(local_file(Path(video), voice_clip['src']))
        source_start = round(float(voice_clip.get('data-media-start', 0)) * 48000)
        voice_start = round(float(voice_clip.get('data-start', 0)) * 48000)
        length = min(len(voice) - source_start, len(signal) - voice_start,
                     round(float(voice_clip['data-duration']) * 48000))
        voice_reference[voice_start:voice_start+length] = voice[source_start:source_start+length]
    results = []
    for c in plan['cues']:
        ref = decode(local_file(Path(video), assets[c['asset']]['path']))[:round(c['duration'] * 48000)]
        # Compare a 25 ms timing neighborhood using a high-pass residual to
        # reduce low-frequency voice masking; this is presence evidence, not listening.
        def highpass(x):
            return x[1:] - .95 * x[:-1]
        ref = highpass(ref)
        center = round(c['start'] * 48000)
        lo = max(0, center - 1200)
        end = center + len(ref) + 1202
        window = highpass(signal[lo:end])
        spoken = highpass(voice_reference[lo:end])
        voice_energy = float(np.dot(spoken, spoken))
        voice_gain = float(np.dot(window, spoken) / voice_energy) if voice_energy > 1e-12 else 0
        # Remove the locally fitted narration, rather than mistaking strong
        # speech energy for an absent effect. This preserves the cue waveform.
        window = window - voice_gain * spoken
        size = 1 << (len(window) + len(ref) - 2).bit_length()
        corr = np.fft.irfft(np.fft.rfft(window, size) * np.fft.rfft(ref[::-1], size), size)
        corr = corr[len(ref)-1:len(window)]
        norm = np.dot(ref, ref)
        offset = int(np.argmax(corr))
        observed = window[offset:offset+len(ref)]
        gain = float(np.dot(observed, ref) / norm)
        denominator = float(np.sqrt(np.dot(observed, observed) * norm))
        similarity = float(np.dot(observed, ref) / denominator) if denominator > 1e-12 else 0
        delta = (lo + offset - center) / 48000
        passed = .45 <= gain / c['volume'] <= 1.8 and similarity >= .25 and abs(delta) <= .025
        results.append({'id': c['id'], 'passed': passed, 'offset_s': delta, 'matched_gain': gain,
                        'authored_gain': c['volume'], 'similarity': similarity, 'fitted_voice_gain': voice_gain})
    report.update(export_sha256=digest(export), assets={a['id']: a['sha256'] for a in plan['assets']}, cue_matches=results)
    if not all(r['passed'] for r in results):
        report['status'] = 'failed'
    name = 'sound-design-export-v2.json' if (Path(video) / 'audio_boundaries.json').exists() else 'sound-design-export.json'
    out = Path(video) / 'verification' / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    if report['status'] != 'passed':
        raise ValueError(f'Export cue verification failed; inspect {out}')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--export', type=Path)
    args = parser.parse_args()
    result = apply_plan(args.video) if args.apply else verify_export(args.video, args.export) if args.export else check_plan(args.video)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
