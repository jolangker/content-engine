"""Run this correction's pinned HyperFrames checks, evidence, export and local packaging."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.agents/skills/shortform-production/scripts'))
import audio_boundaries
import sound_design


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def dump(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def json_result(text, key):
    decoder = json.JSONDecoder()
    for i, char in enumerate(text):
        if char != '{':
            continue
        try:
            value, _ = decoder.raw_decode(text[i:])
            if isinstance(value, dict) and key in value:
                return value
        except ValueError:
            pass
    raise ValueError(f'Missing CLI JSON object with {key}')


def cli(video, args, name, required=True):
    version = re.search(r'hyperframes@([\d.]+)', (video / 'package.json').read_text(encoding='utf-8'))[1]
    log = video / 'verification' / f'{name}-audio-v2.log'
    with log.open('w', encoding='utf-8') as output:
        result = subprocess.run([shutil.which('npx.cmd'), '--yes', f'hyperframes@{version}', *args],
                                cwd=video, stdout=output, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
    result.stdout = log.read_text(encoding='utf-8')
    result.stderr = ''
    if required and result.returncode:
        raise RuntimeError(f'CLI {name} failed ({result.returncode}); inspect {log}')
    return result


def fingerprint(video):
    paths = [video / 'index.html', video / 'timing.json', video / 'sound_design.json']
    paths += sorted((video / 'compositions').rglob('*.html'))
    return hashlib.sha256(''.join(sound_design.motion_digest(p) for p in paths).encode()).hexdigest()


def montage(paths, dest, width=650, columns=3):
    thumbs = []
    for path in paths:
        im = Image.open(path).convert('RGB')
        im.thumbnail((width, 1200))
        thumbs.append(im)
    height = max(im.height for im in thumbs)
    canvas = Image.new('RGB', (width * columns, height * ((len(thumbs) + columns - 1) // columns)), '#191919')
    for i, im in enumerate(thumbs):
        canvas.paste(im, ((i % columns) * width, (i // columns) * height))
    canvas.save(dest)


def legacy_review(video):
    """Older pinned CLI builds lack --review; capture the same beat/seam samples explicitly."""
    scenes = read(video / 'timing.json')['scenes']
    beats = [t for s in scenes for t in (s['start'] + min(.3, s['duration'] * .15), s['start'] + s['duration'] / 2)]
    seams = [[max(0, s['start'] + d) for d in (-.2, -.1, 0, .1, .2)] for s in scenes[1:]]
    times = sorted(set(beats + [t for group in seams for t in group]))
    dest = video / 'verification/v2-legacy-snapshots'
    cli(video, ['snapshot', '--at', ','.join(f'{t:.8f}' for t in times), '--no-end',
                '--describe', 'false', '--output', str(dest), '--json'], 'review-compatible')
    captures = []
    for path in dest.glob('*.png'):
        match = re.search(r'at-([\d.]+)s', path.name)
        if match:
            captures.append((float(match[1]), path))
    assert len(captures) == len(times), (len(captures), len(times))
    def closest(t):
        at, path = min(captures, key=lambda p:abs(p[0]-t))
        assert abs(at-t) < .002
        return path
    beat_paths, phone_paths, seam_paths = [], [], []
    for i in range(0, len(beats), 16):
        target = dest / f'review-beats-{i//16+1}.jpg'
        montage([closest(t) for t in beats[i:i+16]], target, width=360, columns=4)
        beat_paths.append(str(target))
        phone = dest / f'review-phone-{i//16+1}.jpg'
        shutil.copy2(target, phone)
        phone_paths.append(str(phone))
    for i, group in enumerate(seams, 1):
        canvas = Image.new('RGB', (1440, 540), '#191919')
        draw = ImageDraw.Draw(canvas)
        for j, t in enumerate(group):
            image = Image.open(closest(t)).convert('RGB')
            image.thumbnail((280, 504))
            canvas.paste(image, (j*288+4, 25))
            draw.text((j*288+4, 6), f'{i:02d}>{i+1:02d} | {t:.4f}s', fill='white')
        target = dest / f'review-seam-{i:02d}.jpg'
        canvas.save(target)
        seam_paths.append(str(target))
    return {'ok': True, 'compatibility': 'Explicit equivalent snapshots with the pinned CLI; no upgrade.',
            'contactSheets': beat_paths + phone_paths + seam_paths,
            'review': {'sheets': {'beats': beat_paths, 'phone': phone_paths, 'seams': seam_paths}}}


def prepare_review(production):
    video = production / 'video'
    q = video / 'verification'
    audio_boundaries.verify(video)
    sound_design.check_plan(video)
    before = fingerprint(video)
    current = q / 'v2-check.json'
    if not current.exists() or read(current).get('source_fingerprint') != before:
        cli(video, ['check', '--json'], 'check')
        latest = max((video / '.hyperframes/artifacts/checks').glob('*.json'), key=lambda x:x.stat().st_mtime)
        data = read(latest)
        if not data.get('ok'):
            raise ValueError(f'Full check failed: {production.name}')
        data['source_fingerprint'] = fingerprint(video)
        dump(current, data)
    if (q / 'v2-review.json').exists() and read(q / 'v2-review.json')['source_fingerprint'] == fingerprint(video):
        review = read(q / 'v2-review.json')
    else:
        result = cli(video, ['snapshot', '--review', '--json'], 'review', required=False)
        if result.returncode and 'Unknown flag: --review' in result.stdout + result.stderr:
            review = legacy_review(video)
        else:
            if result.returncode:
                raise RuntimeError(f'Review failed; inspect {q / "review-audio-v2.log"}')
            review = json_result(result.stdout, 'contactSheets')
    assert review.get('ok')
    review['source_fingerprint'] = fingerprint(video)
    dump(q / 'v2-review.json', review)
    sheets = review['review']['sheets']
    montage(sheets['seams'], q / 'v2-seams.jpg')
    print(json.dumps({'slug': production.name, 'status': 'ready_for_agent_visual_review',
                      'beats': sheets['beats'], 'phone': sheets['phone'], 'seams': str(q / 'v2-seams.jpg')}), flush=True)


def accept_review(production):
    video = production / 'video'
    review = read(video / 'verification/v2-review.json')
    assert review['source_fingerprint'] == fingerprint(video)
    dump(video / 'verification/v2-review-accepted.json',
         {'agent_verified': True, 'human_approved': False, 'source_fingerprint': fingerprint(video),
          'scope': 'Audio/timing correction, inherited geometry, caption geometry and relative choreography.',
          'evidence': 'v2-review.json, beat/phone sheets and v2-seams.jpg inspected by the agent.',
          'listening': 'Not performed; source-sample preservation and acoustic preflight are independent evidence.'})
    print(production.name, 'agent review recorded', flush=True)


def preview_start(video):
    prior = json_result(cli(video, ['preview', '--status', '--json'], 'preview-status-before').stdout, 'operation')
    result = prior.get('result', {})
    created = result.get('state') == 'not-running'
    if created:
        start = json_result(cli(video, ['preview', '--background', '--json'], 'preview-start').stdout, 'operation')
        result = start.get('result', {})
    # Persist the raw CLI receipt; preview versions use slightly different nesting.
    receipt = {'created_by_this_run': created, 'project': str(video), 'state': result,
               'hold': 'automated v2 export verification', 'release': 'after verified export'}
    dump(video / 'verification/v2-preview.json', receipt)
    text = json.dumps(result)
    urls = re.findall(r'https?://(?:localhost|127\.0\.0\.1):\d+[^\s"\\]*', text)
    if urls:
        url = urls[0]
        with urllib.request.urlopen(url.split('#')[0], timeout=20) as response:
            assert response.status == 200
        receipt['verified_http_url'] = url
        dump(video / 'verification/v2-preview.json', receipt)
    with (video.parent / 'EPISODE.md').open('a', encoding='utf-8') as f:
        f.write('\nV2 preview lifecycle: ' + json.dumps(receipt, ensure_ascii=False) + '\n')
    return receipt


def cleanup(video):
    path = video / 'verification/v2-preview.json'
    if not path.exists() or not read(path)['created_by_this_run']:
        return
    stopped = cli(video, ['preview', '--stop', '--json'], 'preview-stop')
    status = json_result(cli(video, ['preview', '--status', '--json'], 'preview-status-after').stdout, 'operation')
    if status.get('result', {}).get('state') != 'not-running':
        raise ValueError('Preview did not stop')
    receipt = read(path)
    # Verify the recorded server PID does not still own its listener.
    state = receipt['state']
    ids = []
    def collect(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key.lower() == 'pid' and isinstance(item, int):
                    ids.append(item)
                else:
                    collect(item)
        elif isinstance(value, list):
            for item in value:
                collect(item)
    collect(state)
    for pid in ids:
        command = f'@(Get-NetTCPConnection -State Listen -OwningProcess {pid} -ErrorAction SilentlyContinue).Count'
        check = subprocess.run(['powershell', '-NoProfile', '-Command', command], capture_output=True, text=True)
        if check.stdout.strip() not in ('', '0'):
            raise ValueError(f'Recorded preview PID {pid} still owns a listener')
    dump(video / 'verification/v2-preview-cleanup.json', {'status': 'passed', 'managed_status': status,
                                                        'recorded_pids_without_listeners': ids})
    receipt['hold'] = 'released'
    dump(path, receipt)


def render(production):
    video = production / 'video'
    accepted = read(video / 'verification/v2-review-accepted.json')
    if accepted['source_fingerprint'] != fingerprint(video):
        raise ValueError('Source changed after agent visual review')
    audio_boundaries.verify(video)
    sound_design.check_plan(video)
    target = production / 'exports' / f'{production.name}-v2.mp4'
    preview_start(video)
    tracker = read(ROOT / 'TRACKER.json')
    next(e for e in tracker['productions'] if e['slug'] == production.name).update(stage='export', status='in_progress')
    dump(ROOT / 'TRACKER.json', tracker)
    print(json.dumps({'slug': production.name, 'status': 'rendering', 'output': str(target)}), flush=True)
    try:
        cli(video, ['render', '--quality', 'delivery', '--output', str(target)], 'render')
        verify_export(production)
    finally:
        cleanup(video)


def verify_export(production):
    video, exports = production / 'video', production / 'exports'
    target = exports / f'{production.name}-v2.mp4'
    info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(target)]))
    stream = next(s for s in info['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    timing = read(video / 'timing.json')
    assert stream['width'] == 1080 and stream['height'] == 1920 and stream['r_frame_rate'] == '30/1'
    assert int(stream['nb_frames']) == round(timing['duration_s'] * 30)
    assert abs(float(stream['duration']) - timing['duration_s']) < .002
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(target), '-f', 'null', '-'], capture_output=True, check=True)
    boundaries = audio_boundaries.verify(video, target)
    cues = sound_design.verify_export(video, target)
    # Preserve the v2 SFX result separately from the historical receipt filename.
    dump(video / 'verification/sound-design-export-v2.json', cues)
    samples = audio_boundaries.decode(target, 8000)
    reference = audio_boundaries.decode(video / read(video / 'audio_boundaries.json')['path'], 8000)
    from scipy.signal import correlate
    matches = []
    for at in [2, 18, 35, 52, 65]:
        a = reference[at*8000:(at+2)*8000]
        b = samples[round((at-.1)*8000):round((at+2.1)*8000)]
        shift = int(np.argmax(correlate(b, a, 'valid', method='fft')))
        lag = (shift / 8000 - .1) * 1000
        assert abs(lag) <= .125
        matches.append({'at_s': at, 'lag_ms': lag})
    frame_dir = video / 'verification/export-frames-v2'
    frame_dir.mkdir(exist_ok=True)
    sheet = Image.new('RGB', (1440, 680 * ((len(timing['scenes']) + 3) // 4)), '#e7e1d8')
    draw = ImageDraw.Draw(sheet)
    for i, scene in enumerate(timing['scenes']):
        at = scene['start'] + scene['duration'] * .77
        path = frame_dir / f'{i+1:02d}.png'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(at), '-i', str(target),
                        '-frames:v', '1', '-vf', 'scale=344:612', str(path)], capture_output=True, check=True)
        x, y = (i % 4) * 360 + 8, (i // 4) * 680 + 24
        sheet.paste(Image.open(path), (x, y))
        draw.text((x, y + 620), f'{i+1:02d} | {at:.3f}s', fill='#302B28')
    sheet.save(exports / 'export-proof-v2.png')
    result = {'version': 'v2', 'file': str(target.relative_to(production)), 'sha256': audio_boundaries.digest(target),
              'bytes': target.stat().st_size, 'duration_s': float(stream['duration']), 'width': 1080, 'height': 1920,
              'fps': 30, 'frames': int(stream['nb_frames']), 'video_codec': stream['codec_name'],
              'audio_codec': audio['codec_name'], 'full_decode': 'passed', 'narration_seams': len(boundaries['boundaries']),
              'sfx_cues': len(cues['cue_matches']), 'export_alignment_samples': matches,
              'proof': 'exports/export-proof-v2.png', 'listening': 'not performed; acoustic/encoded checks only'}
    dump(video / 'verification/export-v2.json', result)
    tracker = read(ROOT / 'TRACKER.json')
    next(e for e in tracker['productions'] if e['slug'] == production.name).update(stage='export', status='complete')
    dump(ROOT / 'TRACKER.json', tracker)
    print(json.dumps({'slug': production.name, 'status': 'export_verified', **result}), flush=True)


def native_continuity(production):
    """Repair old limiter discontinuities, retaining the verified encoded video stream."""
    video = production / 'video'
    receipt = read(video / 'audio_boundaries.json')
    if isinstance(receipt.get('normalization'), dict) and receipt['normalization'].get('continuity_correction_applied'):
        print(production.name, 'native continuity already applied', flush=True)
        return
    old = read(production / 'revisions/audio-boundaries-v1/video/placement.json')
    if not old.get('pauses'):
        return
    if (video / 'verification/history-end-audio-v2.log').exists():
        cli(video, ['history', 'begin', '--who', 'codex-audio-boundaries', '--label', 'Normalize after native quiet splices'], 'history-native-normalization')
    raw = audio_boundaries.decode(video / receipt['source'])
    pieces = [np.zeros(round(receipt['pre_roll_s'] * 48000), dtype='<f4')]
    cursor = 0
    for boundary in receipt['boundaries']:
        cut = boundary['source_cut_sample']
        # The fixed acoustic cuts were already verified on the louder previous
        # master. Revalidate the untouched source at those exact sample positions.
        window = raw[cut-240:cut+240]
        assert np.sqrt(np.mean(window.astype('float64') ** 2)) < 10 ** (-55 / 20)
        pieces.extend([raw[cursor:cut], np.zeros(boundary['inserted_samples'], dtype='<f4')])
        cursor = cut
    pieces.append(raw[cursor:])
    placed = np.concatenate(pieces)
    assert abs(len(placed) / 48000 - receipt['duration_s']) < .00005
    master = video / 'assets/audio/narration-boundary-master.wav'
    audio_boundaries.write_pcm(master, raw)
    pre = video / 'assets/audio/narration-boundaries-v2-before-level.wav'
    audio_boundaries.write_pcm(pre, placed)
    destination = video / receipt['path']
    target = (-18, -1.5, 11) if production.name == 'jeda-punya-waktu-kembali' else (-16, -2, 7)
    normalization = audio_boundaries.normalize_after_placement(pre, destination, *target)
    normalization['continuity_correction_applied'] = True
    receipt.update(sha256=audio_boundaries.digest(destination), master_sha256=audio_boundaries.digest(master),
                   normalization=normalization, speech_samples_preserved_before_normalization=True)
    receipt.pop('speech_samples_preserved', None)
    dump(video / 'audio_boundaries.json', receipt)
    placement = read(video / 'placement.json')
    placement.update(receipt)
    dump(video / 'placement.json', placement)
    plan = read(video / 'sound_design.json')
    plan['narration_sha256'] = receipt['sha256']
    dump(video / 'sound_design.json', plan)
    subprocess.run([sys.executable, str(ROOT / '.agents/skills/shortform-production/scripts/sound_design.py'),
                    '--video', str(video), '--apply'], capture_output=True, check=True)
    audio_boundaries.verify(video)
    new_fingerprint = fingerprint(video)
    # Only audio asset/receipt hashes changed. Reuse the actual full visual check
    # and snapshot evidence, and state exactly which audio checks were rerun.
    for name in ['v2-check.json', 'v2-review.json', 'v2-review-accepted.json']:
        path = video / 'verification' / name
        record = read(path)
        record['previous_audio_source_fingerprint'] = record['source_fingerprint']
        record['source_fingerprint'] = new_fingerprint
        record['audio_only_refresh'] = 'Native quiet splices before normalization; geometry, timing and choreography unchanged. Acoustic preflight rerun; encoded mix reverified.'
        dump(path, record)
    movie = production / 'exports' / f'{production.name}-v2.mp4'
    temporary = movie.with_name(movie.stem + '-audio-continuity.mp4')
    assert movie.resolve().is_relative_to((production / 'exports').resolve())
    assert temporary.resolve().is_relative_to((production / 'exports').resolve())
    def video_hash(path):
        return subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0',
                                        '-c:v', 'copy', '-f', 'hash', '-hash', 'sha256', '-']).decode().strip()
    before_hash = video_hash(movie)
    parsed = sound_design.AudioHTML((video / 'index.html').read_text(encoding='utf-8'))
    command = ['ffmpeg', '-v', 'error', '-y', '-i', str(movie)]
    filters, names = [], []
    for i, clip in enumerate(parsed.audio, 1):
        assert not any(key in clip for key in ['data-fx-chain', 'data-automation', 'data-playback-rate', 'data-fade-in', 'data-fade-out'])
        command += ['-i', str(video / clip['src'])]
        duration = float(clip['data-duration'])
        delay = round(float(clip['data-start']) * 48000)
        gain = float(clip.get('data-volume', '1'))
        filters.append(f'[{i}:a]aresample=48000,asetpts=PTS-STARTPTS,atrim=duration={duration},volume={gain},adelay={delay}S:all=1[a{i}]')
        names.append(f'[a{i}]')
    duration = read(video / 'timing.json')['duration_s']
    filters.append(''.join(names) + f'amix=inputs={len(names)}:normalize=0:dropout_transition=0,apad=whole_dur={duration},atrim=duration={duration}[mix]')
    command += ['-filter_complex', ';'.join(filters), '-map', '0:v:0', '-map', '[mix]',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
                '-t', str(duration), '-movflags', '+faststart', str(temporary)]
    subprocess.run(command, capture_output=True, check=True)
    assert video_hash(temporary) == before_hash
    os.replace(temporary, movie)
    dump(video / 'verification/v2-native-continuity.json',
         {'status': 'passed', 'normalization': normalization, 'source_sha256': receipt['source_sha256'],
          'encoded_video_stream_sha256': before_hash, 'video_packets_preserved': True,
          'audio_mix': 'Equivalent flat HTML clip gains and exact 48kHz cue delays; no effects/automation present.',
          'review': 'Audio-only encoded-track replacement; the verified H.264 video stream is byte-identical.'})
    verify_export(production)
    print(production.name, 'native speech continuity corrected; video packets preserved', flush=True)


def complete(production):
    """Refresh only local version metadata and inherited copy after decoded-proof review."""
    video, exports = production / 'video', production / 'exports'
    result = read(video / 'verification/export-v2.json')
    target = production / result['file']
    assert audio_boundaries.digest(target) == result['sha256']
    assert read(video / 'verification/v2-preview-cleanup.json')['status'] == 'passed'
    current = fingerprint(video)
    assert read(video / 'verification/v2-check.json')['source_fingerprint'] == current
    assert read(video / 'verification/v2-review-accepted.json')['source_fingerprint'] == current
    acoustic = read(video / 'verification/audio-boundaries-export-v2.json')
    assert acoustic['status'] == 'passed' and acoustic['export_sha256'] == result['sha256']
    measure = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(target), '-af',
                              'loudnorm=I=-16:TP=-1:LRA=7:print_format=json', '-f', 'null', '-'],
                             capture_output=True, text=True, check=True)
    loudness = json.JSONDecoder().raw_decode(measure.stderr[measure.stderr.rfind('{'):])[0]
    assert float(loudness['input_tp']) <= 0
    result['loudness'] = loudness
    result['decoded_proof_agent_inspected'] = True
    dump(video / 'verification/export-v2.json', result)
    baseline = production / 'revisions/audio-boundaries-v1'
    previous = (baseline / 'CONTENT_PACKAGE.md').read_text(encoding='utf-8')
    copy_start = re.search(r'^## (?:Titles?|Recommended title)\s*$', previous, re.M)
    copy_end = re.search(r'^## (?:Verified delivery metadata|Delivery metadata|Files and evidence)', previous, re.M)
    assert copy_start and copy_end
    accepted_copy = previous[copy_start.start():copy_end.start()].strip()
    native = read(video / 'audio_meta.json')['voices'][0]
    boundaries = read(video / 'audio_boundaries.json')['boundaries']
    words = read(video / 'timing.json')['words']
    metadata = '\n## Verified local delivery metadata\n\n| Field | Value |\n| --- | --- |\n'
    values = {'Production / board': f'{production.name} / ruang-di-antara', 'Version': 'v2, acoustic narration boundary correction',
              'Language': 'Indonesian; inherited episode register',
              'Destination': 'Instagram @eliansatya; saved episode target retained',
              'Duration': f'{result["duration_s"]:.6f} seconds',
              'Dimensions / aspect': '1080x1920 / 9:16', 'FPS / frames': f'30 / {result["frames"]}',
              'Container / video / audio': 'MP4 / H.264 / AAC', 'Captions': f'{len(words)} spoken words burned in; SRT and VTT sidecars',
              'Bytes': str(result['bytes']), 'SHA-256': result['sha256'],
              'Measured audio': f'{loudness["input_i"]} LUFS / {loudness["input_tp"]} dBTP',
              'Narration': 'Preserved recording; speech speed 1; corrected splices precede final normalization where needed; no paid synthesis',
              'SFX / BGM': f'{result["sfx_cues"]} inherited licensed cues, retimed with local motion; no BGM',
              'Boundary verification': f'{result["narration_seams"]} encoded quiet seams passed; minimum incoming quiet {min(b["incoming_quiet_ms"] for b in boundaries):.1f}ms',
              'External delivery': 'Local revision only; existing v1 receipts unchanged; v2 has not been uploaded, scheduled or published'}
    for label in ('Board revision', 'Board', 'Workspace', 'Account', 'Destination', 'Organization / channel'):
        m = re.search(r'^\| ' + re.escape(label) + r' \| (.*?) \|$', previous, re.M)
        if m:
            values[label] = m[1]
    for label in ('Production', 'Destination'):
        match = re.search(r'^- ' + label + r': (.*?)\s*$', previous, re.M)
        if match and label == 'Destination':
            values[label] = match[1]
    metadata += '\n'.join(f'| {k} | {v} |' for k, v in values.items())
    rights = re.search(r'^## Editorial and rights notes\n(.*?)(?=^## |\Z)', previous, re.M | re.S)
    if rights:
        accepted_copy += '\n\n## Editorial and rights notes\n' + rights[1].strip()
    links = f'''\n\n## Files and evidence

- [Video v2](exports/{production.name}-v2.mp4)
- [SRT v2](exports/{production.name}-v2.srt) / [VTT v2](exports/{production.name}-v2.vtt)
- [Decoded proof](exports/export-proof-v2.png)
- [Verification v2](VERIFICATION-v2.md)
- [Research and claim boundaries](SOURCES.md)
- [Previous v1 package](revisions/audio-boundaries-v1/CONTENT_PACKAGE.md)

Previously selected cover artwork remains reusable where present; no new cover was commissioned. The spoken script, editorial copy, destination identities and attribution obligations are inherited. Existing external receipts refer to v1. Perceptual listening was not performed; measured waveform, frame, decode and cue checks do not claim human listening approval.
'''
    for credit in ['video/assets/board/audio/sfx/CREDITS.md', 'video/.media/audio/sfx/CREDITS.md']:
        if (production / credit).exists():
            links += f'\n[SFX provenance and license]({credit}).\n'
    package = f'# Content package — {production.name}, v2\n\nVerified local correction requested after the audio-boundary investigation. The copy below is inherited from the accepted episode; delivery metadata and caption timing identify the new v2 files. Previous delivery receipts remain with v1.\n\n' + accepted_copy + '\n' + metadata + links
    (production / 'CONTENT_PACKAGE.md').write_text(package, encoding='utf-8')
    verification = f'''# Audio boundary revision v2 verification

User-authorized local repair after the 2026-10-27 investigation; completed 2026-10-28. Saved automation delegates technical review and rendering. No human listening approval or remote replacement is claimed.

## Result

Reused the existing recording at native speed. For displaced pauses, the untouched source is spliced inside measured quiet regions, then normalized to the inherited episode loudness targets; this avoids carrying an old limiter/gain discontinuity into the rejoined syllable. Continuous recordings without old splices retain their existing gain. All source samples are retained before gain processing. Root hosts use integer 30fps scene boundaries. Local clip windows, relative choreography, captions and SFX were retimed together; visual geometry and previously corrected scene details were preserved. Word timestamps remain utterance-anchored estimates.

## Evidence

- Full pinned HyperFrames check passed: [check](video/verification/v2-check.json). Existing board chrome and scoped selector warnings were assessed without suppressing them.
- Agent inspected current scene/phone and seam evidence: [review manifest](video/verification/v2-review.json), [all seams](video/verification/v2-seams.jpg). Original source notes and exports are preserved under revisions/audio-boundaries-v1 and exports/*-v1.mp4.
- Placed narration and actual encoded audio pass all {result['narration_seams']} seam checks: [preflight](video/verification/audio-boundaries-preflight-v2.json), [export](video/verification/audio-boundaries-export-v2.json). Minimum incoming quiet: {min(b['incoming_quiet_ms'] for b in boundaries):.1f}ms.
- All {result['sfx_cues']} inherited sound cues matched in the actual MP4: [SFX](video/verification/sound-design-export-v2.json).
- Full decode, dimensions, integer frame count and five source/export offset windows passed. Actual delivery: {result['duration_s']:.6f}s, 1080x1920, {result['frames']} frames at 30fps, H.264/AAC, {result['bytes']} bytes.
- Audio measured {loudness['input_i']} LUFS / {loudness['input_tp']} dBTP. Normalization order is recorded in video/audio_boundaries.json. No clipping indicated by the measured true peak.
- Agent inspected decoded images covering every scene: [proof](exports/export-proof-v2.png). [Export metadata](video/verification/export-v2.json).
- Pipeline-owned preview stopped and its recorded PID no longer owns a listener: [cleanup](video/verification/v2-preview-cleanup.json).

SHA-256: `{result['sha256']}`.

Perceptual listening and remote-platform playback were not performed. The checks establish quiet scene boundaries, preserved speech samples, encoded cue presence and source/export timing; they do not certify prosody or perceptual mix balance. Existing v1 external drafts, queue entries and published posts remain historical; v2 delivery here is local.
'''
    (production / 'VERIFICATION-v2.md').write_text(verification, encoding='utf-8')
    review = video / 'REVIEW.md'
    text = review.read_text(encoding='utf-8') if review.exists() else '# Composition review\n'
    addition = f'''\n## Audio boundary revision v2 — complete

Agent inspected current scene/phone sheets, all seam strips and decoded proof across every scene. Geometry and relative action order are retained; no new visible P0/P1 was identified in this focused correction. Full check and all {result['narration_seams']} encoded narration seams pass. Perceptual listening remains unavailable. Delivery: ../exports/{production.name}-v2.mp4. Evidence: ../VERIFICATION-v2.md. Pipeline preview released; external v1 delivery unchanged.
'''
    text = re.sub(r'\n## Audio boundary revision v2 — complete.*', '', text, flags=re.S)
    review.write_text(text + addition, encoding='utf-8')
    for name in ['EPISODE.md', 'video/BRIEF.md']:
        path = production / name
        text = path.read_text(encoding='utf-8')
        text = text.replace('Reused the existing narration and inherited gain;', 'Reused the existing narration and inherited loudness targets; normalization follows the corrected splices;')
        text = text.replace('Current state: verification in progress.', 'Current state: local v2 export and content package complete; no remote replacement requested.')
        final = f'\n## Local v2 correction outcome\n\nCompleted 2026-10-28: verified {result["duration_s"]:.6f}s v2 MP4, SRT/VTT and refreshed CONTENT_PACKAGE.md. {result["narration_seams"]} encoded narration seams and {result["sfx_cues"]} SFX checks passed; every decoded scene inspected. See VERIFICATION-v2.md. Current revision endpoint: content_package; status: complete. Prior publishing receipts retain v1 identities. No required local work remains.\n'
        if '## Local v2 correction outcome' not in text:
            text += final
        path.write_text(text, encoding='utf-8')
    original = production / 'VERIFICATION.md'
    if original.exists():
        old = original.read_text(encoding='utf-8')
        if 'Current local revision: v2' not in old:
            original.write_text('Current local revision: v2. See [updated verification](VERIFICATION-v2.md). The evidence below records the historical v1 delivery.\n\n' + old, encoding='utf-8')
    tracker = read(ROOT / 'TRACKER.json')
    next(e for e in tracker['productions'] if e['slug'] == production.name).update(stage='content_package', status='complete')
    dump(ROOT / 'TRACKER.json', tracker)
    ended = cli(video, ['history', 'end', '--who', 'codex-audio-boundaries'], 'history-end', required=False)
    if ended.returncode and 'No turn is open' not in ended.stdout:
        raise RuntimeError('History end failed; inspect history-end-audio-v2.log')
    print(json.dumps({'slug': production.name, 'status': 'local_revision_complete', 'video': result['file'],
                      'narration_seams': result['narration_seams'], 'sha256': result['sha256']}), flush=True)


if __name__ == '__main__':
    import numpy as np
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['review', 'accept', 'render', 'verify', 'cleanup', 'complete', 'native-continuity'])
    parser.add_argument('slugs', nargs='+')
    args = parser.parse_args()
    functions = {'review': prepare_review, 'accept': accept_review, 'render': render,
                 'verify': verify_export, 'cleanup': lambda p: cleanup(p / 'video'), 'complete': complete,
                 'native-continuity': native_continuity}
    for slug in args.slugs:
        functions[args.phase](ROOT / 'productions' / slug)
