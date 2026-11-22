"""Gate a production against its contract: storyboard plan, sources, timing, review record and the rendered film."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
import statistics
import subprocess
import sys

# Starting values for every production; a contract value replaces its default, null inherits it.
DEFAULTS = {
    'format': {'width': None, 'height': None, 'fps': None},
    'duration_seconds': {'min': None, 'max': None},
    'scene_count': {'min': None, 'max': None},
    'narration': {'words': {'min': None, 'max': None}, 'max_words_per_scene': None},
    'hook': {'first_sentence_max_seconds': 5.0, 'first_motion_max_seconds': 1.0,
             'turn': {'markers': [], 'max_seconds': None}},
    'motion': {'max_static_seconds': 5.0, 'min_active_area': 0.01},
    'storyboard': {'max_same_shot_run': 2},
    'captions': {'region': None},
    'audio': {'narration': None, 'bgm': None, 'sfx': None,
              'loudness_lufs': {'min': -15.0, 'max': -13.0}, 'true_peak_max_dbtp': -0.5},
    'judged': [],
}

# Review questions every film answers, whatever its board.
STANDING = [
    {'id': 'hook-frame', 'rule': 'Frame 0 already shows the subject, result or action, with a line readable at phone size.'},
    {'id': 'pictures-alone', 'rule': 'With narration and captions covered, the beat frames still tell the story in order.'},
    {'id': 'event-density', 'rule': 'Every scene shows a new action, state change or relationship beyond its captions.'},
    {'id': 'motion-variety', 'rule': 'Neighbouring scenes differ in framing scale or kind of movement.'},
    {'id': 'subject-scale', 'rule': 'The active subject fills the usable stage at phone size.'},
    {'id': 'ear-test', 'rule': 'The narration alone is followable: every actor, pronoun and instruction resolves.'},
]

CONTRACT_NOTES = ('schema_version', 'board', 'revision', 'sources', 'overrides')
REVIEWERS = ('subagent', 'worker', 'human')
LISTENERS = ('agent', 'worker', 'human', 'silent')
STAGES = ('storyboard', 'verification', 'export')
DISCLOSED = ('failed', 'overridden', 'needs_human', 'unheard')
SAMPLE_FPS = 5
ANALYSIS_WIDTH = 270
PIXEL_DELTA = 12       # grey levels; above encoder noise in a held frame
MOVING_AREA = 0.0005   # share of unmasked pixels that must differ for the picture to count as changed
FINAL_HOLD = 3.0       # a closing hold is exempt from the static limit
MAX_MASKED = 0.25      # a caption region larger than this hides the film
MIN_EVIDENCE = 12      # characters of evidence after a judged verdict
HOOK_POSES = 3         # frame 0, the first change, the three-second state
SENTENCE_END = re.compile(r'[.!?…]["\'”’)\]]*$')
HF_ID = re.compile(r'\s+data-hf-id=(?:"[^"]*"|\x27[^\x27]*\x27)')
FRAME_HEAD = re.compile(r'^#{2,3}\s*(?:Frame|Beat|Scene)\s+(\d+)\b(.*)$', re.I)
KEY_LINE = re.compile(r'^-\s*([A-Za-z_]+)\s*:\s*(.*)$')
READ_WINDOW = re.compile(r'\(\s*(\d+(?:\.\d+)?)\s*s?\s*(?:-|–|to)\s*(\d+(?:\.\d+)?)\s*s?\s*\)')


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class Root(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.root = None
        self.hosts = []
        self.assets = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.root is None and 'data-composition-id' in a and 'data-duration' in a:
            self.root = a
        elif 'data-composition-src' in a:
            self.hosts.append(a)
        elif tag == 'script' and a.get('src'):
            self.assets.append(a['src'])
        elif tag == 'link' and a.get('rel') == 'stylesheet' and a.get('href'):
            self.assets.append(a['href'])


def load_root(video):
    parsed = Root((Path(video) / 'index.html').read_text(encoding='utf-8'))
    if parsed.root is None:
        raise ValueError('index.html needs a root composition with data-duration')
    return parsed


def is_captions(host):
    name = (host.get('id', '') + host.get('data-composition-src', '')).lower()
    return host.get('data-track-kind') == 'captions' or 'caption' in name


def composition_digest(video):
    """One hash for the root and the local files it loads, ignoring editor identity stamps."""
    video = Path(video).resolve()
    parsed = load_root(video)
    names = ['index.html', *sorted({h['data-composition-src'] for h in parsed.hosts}),
             *sorted({a for a in parsed.assets if '://' not in a})]
    h = hashlib.sha256()
    for name in names:
        path = (video / name).resolve()
        if not path.is_relative_to(video) or not path.is_file():
            raise ValueError(f'Missing/out-of-project composition file: {name}')
        data = HF_ID.sub('', path.read_text(encoding='utf-8')).encode('utf-8') if path.suffix == '.html' else path.read_bytes()
        h.update(name.encode() + b'\0' + data + b'\0')
    return h.hexdigest()


def merged(defaults, given):
    out = {}
    for key, default in defaults.items():
        value = given.get(key) if isinstance(given, dict) else None
        out[key] = merged(default, value or {}) if isinstance(default, dict) else default if value is None else value
    return out


def unknown_keys(defaults, given, prefix=''):
    extra = [prefix + k for k in given if k not in defaults]
    for key, default in defaults.items():
        if isinstance(default, dict) and isinstance(given.get(key), dict):
            extra += unknown_keys(default, given[key], f'{prefix}{key}.')
    return extra


def load_contract(folder):
    path = Path(folder) / 'CONTRACT.json'
    if not path.is_file():
        raise ValueError(f'Missing {path}: a production snapshots its contract at brief')
    raw = read_json(path)
    if raw.get('schema_version') != 1:
        raise ValueError('Expected contract schema_version 1')
    extra = unknown_keys(DEFAULTS, {k: v for k, v in raw.items() if k not in CONTRACT_NOTES})
    if extra:
        raise ValueError(f'Unknown contract fields, so their rules would not be enforced: {", ".join(extra)}')
    contract = merged(DEFAULTS, raw)
    judged = STANDING + contract['judged']
    ids = [j.get('id', '') for j in judged]
    if len(set(ids)) != len(ids) or not all(re.fullmatch(r'[a-z0-9][a-z0-9-]*', i) and j.get('rule') for i, j in zip(ids, judged)):
        raise ValueError('Judged rules need unique lowercase ids and a rule')
    overrides = {}
    for o in raw.get('overrides', []):
        if not o.get('check') or not str(o.get('reason', '')).strip() or o.get('authority') not in ('user', 'board'):
            raise ValueError('An override needs a check id, a reason and authority user|board')
        overrides[o['check']] = o
    region = contract['captions']['region']
    if region is not None and (len(region) != 4 or not all(isinstance(n, (int, float)) and n >= 0 for n in region)):
        raise ValueError('captions.region is [x, y, width, height] in delivery pixels')
    return contract, judged, overrides, digest(path)


def load_timing(video):
    path = Path(video) / 'timing.json'
    if not path.is_file():
        return None
    timing = read_json(path)
    if not isinstance(timing, dict) or not isinstance(timing.get('scenes'), list):
        raise ValueError('timing.json needs a scenes list with start and end')
    return timing


def passed(check, ok, measured=None, limit=None, detail=''):
    return {'id': check, 'status': 'passed' if ok else 'failed', 'measured': measured, 'limit': limit, 'detail': detail}


def skipped(check, detail):
    return {'id': check, 'status': 'skipped', 'measured': None, 'limit': None, 'detail': detail}


def within(value, low, high):
    return (low is None or value >= low) and (high is None or value <= high)


def analysis_size(width, height):
    return ANALYSIS_WIDTH, max(2, round(height * ANALYSIS_WIDTH / width / 2) * 2)


def unmasked(w, h, width, height, region):
    import numpy as np
    keep = np.ones((h, w), bool)
    if region:
        x, y, rw, rh = region
        sx, sy = w / width, h / height
        keep[max(0, int(y * sy) - 1):math.ceil((y + rh) * sy) + 1, max(0, int(x * sx) - 1):math.ceil((x + rw) * sx) + 1] = False
    return keep


def parse_storyboard(text):
    frames = []
    for line in text.splitlines():
        head = FRAME_HEAD.match(line)
        if head:
            frames.append({'number': int(head.group(1)), 'title': head.group(2).strip(' :—–-'), 'keys': {}})
        elif frames and (key := KEY_LINE.match(line)):
            frames[-1]['keys'].setdefault(key.group(1).lower(), key.group(2).strip())
    for frame in frames:
        seconds = re.match(r'\s*(\d+(?:\.\d+)?)', frame['keys'].get('duration', ''))
        frame['duration'] = float(seconds.group(1)) if seconds else None
    return frames


def still(path, w, h):
    import numpy as np
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-frames:v', '1', '-vf',
                        f'scale={w}:{h}:flags=area,format=gray', '-f', 'rawvideo', 'pipe:1'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(h, w).astype(np.int16)


def check_storyboard(video, root, contract):
    """Hold the plan to the same cadence the film is measured against later."""
    path = Path(video) / 'STORYBOARD.md'
    if not path.is_file():
        return [passed('storyboard-plan', False, detail='STORYBOARD.md is missing')]
    frames = parse_storyboard(path.read_text(encoding='utf-8'))
    if not frames:
        return [passed('storyboard-plan', False, detail='STORYBOARD.md has no "## Frame N" sections')]
    hold = contract['motion']['max_static_seconds']
    limit = contract['scene_count']
    out = [passed('scene-count', within(len(frames), limit['min'], limit['max']), len(frames), limit)]
    planned = sum(f['duration'] or 0 for f in frames)
    limit = contract['duration_seconds']
    out.append(passed('duration', all(f['duration'] for f in frames) and within(planned, limit['min'], limit['max']),
                      round(planned, 2), limit, 'Sum of the planned frame durations'))
    labels = [f['keys'].get('shot', '').lower() for f in frames]
    run = longest = 0
    for i, label in enumerate(labels):
        run = run + 1 if i and label == labels[i - 1] else 1
        longest = max(longest, run)
    limit = contract['storyboard']['max_same_shot_run']
    out.append(passed('shot-variety', all(labels) and longest <= limit, {'shots': labels, 'longest_run': longest}, limit,
                      'Every frame names its shot scale; a run of the same scale stays within the limit'))
    slow = {}
    for i, frame in enumerate(frames):
        starts = sorted(float(a) for a, _ in READ_WINDOW.findall(frame['keys'].get('reads', '')))
        end = frame['duration'] or 0
        allowed = hold + (FINAL_HOLD if i == len(frames) - 1 else 0) + .05
        gaps = [b - a for a, b in zip([0.0, *starts], [*starts, end])]
        if not starts or max(gaps[:-1], default=0) > hold + .05 or gaps[-1] > allowed:
            slow[frame['number']] = 'no timed reads' if not starts else f'{max(gaps):.1f}s with nothing new'
    out.append(passed('reads-cadence', not slow, slow, hold,
                      'Each read names a visible change and opens a window counted from the frame start'))
    boards = Path(video) / 'boards'
    width = contract['format']['width'] or int(root.get('data-width') or 1080)
    height = contract['format']['height'] or int(root.get('data-height') or 1920)
    w, h = analysis_size(width, height)
    keep = unmasked(w, h, width, height, contract['captions']['region'])

    def develops(files):
        return ((abs(still(files[-1], w, h) - still(files[0], w, h)) > 2 * PIXEL_DELTA) & keep).sum() >= contract['motion']['min_active_area'] * keep.sum()

    problems = {}
    hook = sorted((boards / 'poses').glob('hook-*.png'))
    if len(hook) < HOOK_POSES:
        problems['hook'] = f'{len(hook)} of {HOOK_POSES} poses'
    elif not develops(hook):
        problems['hook'] = 'frame 0 and the three-second pose are the same picture'
    for frame in frames:
        if (frame['duration'] or 0) > hold:
            poses = sorted((boards / 'poses').glob(f'{frame["number"]:02d}-*.png'))
            if len(poses) < 2:
                problems[frame['number']] = 'needs a start and an end pose'
            elif not develops(poses):
                problems[frame['number']] = 'start and end pose are the same picture'
    out.append(passed('poses', not problems, problems, {'hook': HOOK_POSES, 'frames_longer_than_seconds': hold},
                      'boards/poses holds hook-*.png and NN-*.png for every long frame'))
    stills = len(list((boards / 'stills').glob('*.png')))
    out.append(passed('storyboard-artifacts', stills >= len(frames) and (boards / 'storyboard.html').is_file()
                      and (boards / 'storyboard.png').is_file(), {'stills': stills, 'frames': len(frames)}))
    return out


def check_sources(video, hosts):
    still_scenes = []
    for host in hosts:
        if is_captions(host):
            continue
        text = (Path(video) / host['data-composition-src']).read_text(encoding='utf-8')
        if 'data-no-timeline' in text and '<video' not in text:
            still_scenes.append(host.get('id') or host['data-composition-src'])
    return passed('scene-timelines', not still_scenes, still_scenes, 'every mounted scene animates or plays footage',
                  'These scenes are still poses marked data-no-timeline' if still_scenes else '')


def check_timing(root, timing, contract):
    duration = float(root['data-duration'])
    limit = contract['duration_seconds']
    out = [passed('duration', within(duration, limit['min'], limit['max']), round(duration, 3), limit)]
    if timing is None:
        note = 'timing.json is missing'
        return out + [passed('timing', False, detail=note) if contract['audio']['narration'] == 'use' else skipped('timing', note)]
    scenes, words = timing['scenes'], timing.get('words') or []
    limit = contract['scene_count']
    out.append(passed('scene-count', within(len(scenes), limit['min'], limit['max']), len(scenes), limit))
    limit = contract['narration']['words']
    out.append(passed('narration-words', within(len(words), limit['min'], limit['max']), len(words), limit))
    per_scene = {str(s.get('id', i + 1)): sum(s['start'] <= w['start'] < s['end'] for w in words)
                 for i, s in enumerate(scenes)}
    limit = contract['narration']['max_words_per_scene']
    out.append(passed('words-per-scene', limit is None or max(per_scene.values(), default=0) <= limit, per_scene, limit))
    hook = contract['hook']
    text = lambda w: str(w.get('text', w.get('word', '')))
    first_end = next((w['end'] for w in words if SENTENCE_END.search(text(w).strip())), None)
    if first_end is None:
        out.append(skipped('hook-first-sentence', 'Word timings carry no sentence punctuation'))
    else:
        out.append(passed('hook-first-sentence', first_end <= hook['first_sentence_max_seconds'], round(first_end, 2),
                          hook['first_sentence_max_seconds'], 'Seconds until the first spoken sentence ends'))
    markers = {m.lower() for m in hook['turn']['markers']}
    if markers and hook['turn']['max_seconds'] is not None:
        turn = next((w['start'] for w in words if re.sub(r'\W+', '', text(w).lower()) in markers), None)
        out.append(passed('hook-turn', turn is not None and turn <= hook['turn']['max_seconds'],
                          None if turn is None else round(turn, 2), hook['turn']['max_seconds'],
                          f'First spoken {"/".join(sorted(markers))}'))
    return out


def check_audio_roles(video, contract):
    wanted = {role: contract['audio'][role] for role in ('narration', 'bgm', 'sfx') if contract['audio'][role]}
    if not wanted:
        return skipped('audio-roles', 'The contract sets no audio roles')
    path = Path(video) / 'sound_design.json'
    if not path.is_file():
        return passed('audio-roles', False, limit=wanted, detail='sound_design.json is missing')
    actual = {role: read_json(path).get('decisions', {}).get(role, {}).get('mode') for role in wanted}
    return passed('audio-roles', actual == wanted, actual, wanted)


def check_review(video, judged, stage):
    path = Path(video) / 'REVIEW.md'
    if not path.is_file():
        return [passed('review-record', False, detail='video/REVIEW.md is missing')]
    text = path.read_text(encoding='utf-8')

    def field(name):
        found = re.search(rf'^[-*\s]*[*`]*{name}[*`]*:[*`\s]*(.*?)[*`\s]*$', text, re.M)
        return found.group(1) if found and found.group(1) else None

    def first_word(name):
        return re.split(r'[\s,;(]', (field(name) or '').lower())[0]

    current = composition_digest(video)
    problems = []
    if field('composition_sha256') != current:
        problems.append('composition_sha256 differs from the current composition: review this version')
    if not field('weakest_shot'):
        problems.append('weakest_shot is missing')
    out = [passed('review-record', not problems, field('composition_sha256'), current, '; '.join(problems))]
    reviewer = first_word('independent_review')
    if reviewer == 'unavailable' and stage == 'verification':
        out.append({'id': 'independent-review', 'status': 'needs_human', 'measured': reviewer, 'limit': REVIEWERS,
                    'detail': 'No fresh-context reviewer: a human reviews the final preview before the delivery render'})
    else:
        out.append(passed('independent-review', reviewer in REVIEWERS, reviewer or None, REVIEWERS,
                          '' if reviewer in REVIEWERS else 'A reviewer other than the author reviews this version before delivery'))
    heard = first_word('listening')
    if heard == 'unavailable':
        out.append({'id': 'listening', 'status': 'unheard', 'measured': heard, 'limit': LISTENERS,
                    'detail': 'Nobody has heard this audio: say so at every checkpoint'})
    else:
        out.append(passed('listening', heard in LISTENERS, heard or None, [*LISTENERS, 'unavailable'],
                          '' if heard in LISTENERS else 'Record who listened to the take and the mix'))
    verdicts = {}
    for rule in judged:
        found = re.search(rf'^\s*[-*]\s*\[(pass|fail)\]\s*`?{re.escape(rule["id"])}`?(?![\w-])(.*)$', text, re.M | re.I)
        verdicts[rule['id']] = ('missing' if not found else 'no evidence' if len(found.group(2).strip(' :—–-')) < MIN_EVIDENCE
                                else found.group(1).lower())
    bad = {k: v for k, v in verdicts.items() if v != 'pass'}
    out.append(passed('judged-rules', not bad, bad or 'all pass', [r['id'] for r in judged]))
    open_p0 = re.findall(r'^\s*[-*]\s*P0\b.*\bopen\W*$', text, re.M | re.I)
    out.append(passed('open-p0', not open_p0, len(open_p0), 0))
    return out


def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)],
                       capture_output=True, text=True, encoding='utf-8', check=True)
    info = json.loads(r.stdout)
    video = next(s for s in info['streams'] if s['codec_type'] == 'video')
    num, den = video['r_frame_rate'].split('/')
    return {'width': int(video['width']), 'height': int(video['height']), 'fps': float(num) / float(den),
            'duration': float(info['format']['duration']),
            'has_audio': any(s['codec_type'] == 'audio' for s in info['streams'])}


def motion(path, info, scenes, region):
    """Sample the film with the caption region masked and measure how long each scene holds still."""
    import numpy as np
    w, h = analysis_size(info['width'], info['height'])
    keep = unmasked(w, h, info['width'], info['height'], region)
    frames = []
    with subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(path), '-an', '-vf',
                           f'fps={SAMPLE_FPS},scale={w}:{h}:flags=area,format=gray', '-f', 'rawvideo', 'pipe:1'],
                          stdout=subprocess.PIPE) as proc:
        while len(chunk := proc.stdout.read(w * h)) == w * h:
            frames.append(np.frombuffer(chunk, np.uint8).reshape(h, w).astype(np.int16))
    if proc.returncode or len(frames) < 2:
        raise ValueError(f'Could not decode frames from {path}')
    step = 1 / SAMPLE_FPS
    floor = MOVING_AREA * keep.sum()
    changed = lambda a, b: ((abs(frames[b] - frames[a]) > PIXEL_DELTA) & keep).sum() >= floor
    first = next((round(i * step, 2) for i in range(1, len(frames)) if changed(0, i)), None)
    hold_from = info['duration'] - FINAL_HOLD
    report = []
    for n, scene in enumerate(scenes):
        index = [i for i in range(len(frames)) if scene['start'] <= i * step < min(scene['end'], hold_from)]
        anchor = index[0] if index else 0
        runs = []
        for i in index[1:]:
            # Compare with the last changed frame, so a slow drift still counts as change.
            if changed(anchor, i):
                runs.append(i - 1 - anchor)
                anchor = i
        runs.append((index[-1] if index else 0) - anchor)
        stack = np.stack([frames[i] for i in index]) if index else np.zeros((1, h, w), np.int16)
        active = float((((stack.max(0) - stack.min(0)) > 2 * PIXEL_DELTA) & keep).sum() / keep.sum())
        report.append({'id': str(scene.get('id', n + 1)), 'start': round(scene['start'], 2), 'end': round(scene['end'], 2),
                       'longest_static_seconds': round(max(runs) * step, 1),
                       'held_seconds': round(sum(r for r in runs if r * step >= 1) * step, 1), 'active_area': round(active, 4)})
    return {'first_motion_seconds': first, 'masked_share': round(float(1 - keep.mean()), 3), 'scenes': report}


def loudness(path):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(path), '-vn', '-af', 'loudnorm=print_format=json',
                        '-f', 'null', '-'], capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)
    data = json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0]
    return float(data['input_i']), float(data['input_tp'])


def fingerprint(film, region=None):
    """Measure any clip the way the gate measures a film: a reference, a motion preview, an export."""
    info = probe(film)
    measured = motion(film, info, [{'id': 'film', 'start': 0, 'end': info['duration']}], region)
    whole = measured['scenes'][0]
    out = {'file': Path(film).name, 'duration_seconds': round(info['duration'], 2), 'width': info['width'], 'height': info['height'],
           'fps': round(info['fps'], 3), 'first_motion_seconds': measured['first_motion_seconds'],
           'longest_static_seconds': whole['longest_static_seconds'],
           'held_share': round(whole['held_seconds'] / max(info['duration'] - FINAL_HOLD, 1e-9), 3),
           'caption_region_masked': bool(region)}
    if info['has_audio']:
        out['integrated_lufs'], out['true_peak_dbtp'] = loudness(film)
    return out


def check_film(film, root, hosts, timing, contract, stage):
    info = probe(film)
    duration = float(root['data-duration'])
    wanted = {k: v for k, v in contract['format'].items() if v is not None}
    actual = {'width': info['width'], 'height': info['height'], 'fps': round(info['fps'], 3)}
    problems = [f'{k} is {actual[k]}, contract says {v}' for k, v in wanted.items() if abs(actual[k] - v) > 1e-3]
    if abs(info['duration'] - duration) > 1 / info['fps'] + .05:
        problems.append(f'film runs {info["duration"]:.2f}s, composition {duration:.2f}s')
    out = [passed('film-format', not problems, {**actual, 'duration': round(info['duration'], 3)}, wanted, '; '.join(problems))]
    region = contract['captions']['region']
    if region is None and any(is_captions(h) for h in hosts):
        return out + [passed('motion-floor', False, detail='The film has a captions track: set captions.region so caption '
                             'changes stay out of the motion measurement')]
    scenes = (timing or {}).get('scenes') or [{'id': h.get('id'), 'start': float(h['data-start']),
                                             'end': float(h['data-start']) + float(h['data-duration'])}
                                            for h in hosts if not is_captions(h)] or [{'id': 'film', 'start': 0, 'end': duration}]
    measured = motion(film, info, scenes, region)
    if measured['masked_share'] > MAX_MASKED:
        return out + [passed('motion-floor', False, measured['masked_share'], MAX_MASKED, 'captions.region hides too much of the frame')]
    limit = contract['motion']
    frozen = [s['id'] for s in measured['scenes'] if s['longest_static_seconds'] > limit['max_static_seconds']
              or s['active_area'] < limit['min_active_area']]
    out.append(passed('motion-floor', not frozen, measured['scenes'], limit,
                      f'Scenes holding still outside the caption region: {", ".join(frozen)}' if frozen else ''))
    first = measured['first_motion_seconds']
    out.append(passed('hook-motion', first is not None and first <= contract['hook']['first_motion_max_seconds'],
                      first, contract['hook']['first_motion_max_seconds'], 'Seconds until the picture first changes'))
    if stage == 'export':
        if not info['has_audio']:
            out.append(passed('loudness', contract['audio']['narration'] == 'none', detail='The export has no audio stream'))
        else:
            integrated, peak = loudness(film)
            lufs = contract['audio']['loudness_lufs']
            ok = within(integrated, lufs['min'], lufs['max']) and peak <= contract['audio']['true_peak_max_dbtp']
            out.append(passed('loudness', ok, {'integrated_lufs': integrated, 'true_peak_dbtp': peak},
                              {**lufs, 'true_peak_max_dbtp': contract['audio']['true_peak_max_dbtp']}))
    return out


def gate(production, stage, film=None):
    production = Path(production).resolve()
    video = production / 'video'
    contract, judged, overrides, contract_sha = load_contract(production)
    parsed = load_root(video)
    verdict = {'stage': stage, 'production': production.name, 'contract_sha256': contract_sha}
    if stage == 'storyboard':
        checks = check_storyboard(video, parsed.root, contract)
    else:
        if stage == 'export' and not film:
            raise ValueError('--stage export needs --film pointing at the delivered file')
        film = Path(film).resolve() if film else video / 'verification' / 'proof.mp4'
        if not film.is_file():
            raise ValueError(f'No film to measure at {film}: render a draft proof or pass --film')
        timing = load_timing(video)
        checks = [check_sources(video, parsed.hosts), *check_timing(parsed.root, timing, contract),
                  check_audio_roles(video, contract), *check_review(video, judged, stage),
                  *check_film(film, parsed.root, parsed.hosts, timing, contract, stage)]
        verdict.update(composition_sha256=composition_digest(video), film={
            'path': film.relative_to(production).as_posix() if film.is_relative_to(production) else str(film), 'sha256': digest(film)})
    for check in checks:
        if check['status'] == 'failed' and check['id'] in overrides:
            check.update(status='overridden', override=overrides[check['id']])
    states = {c['status'] for c in checks}
    status = 'failed' if 'failed' in states else 'needs_human_review' if 'needs_human' in states else 'passed'
    verdict = {'status': status, **verdict, 'disclose': [c for c in checks if c['status'] in DISCLOSED], 'checks': checks}
    out = video / 'verification' / f'quality-gate-{stage}.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return verdict


def voice_history(root, voice):
    """Speaking rate and film/narration ratio from every production recorded with this voice."""
    rates, ratios = [], []
    for meta_path in sorted((Path(root) / 'productions').glob('*/video/audio_meta.json')):
        try:
            meta = read_json(meta_path)
            take = meta['voices'][0]
            if meta.get('voice_id') != voice or not take.get('words') or not take.get('duration_s'):
                continue
            ratio = float(load_root(meta_path.parent).root['data-duration']) / take['duration_s']
        except (KeyError, IndexError, TypeError, ValueError, OSError):
            continue
        rates.append(len(take['words']) / take['duration_s'])
        ratios.append(ratio)
    return rates, ratios


def budget(root, words, voice, production=None):
    rates, ratios = voice_history(root, voice)
    if not rates:
        raise ValueError(f'No measured narration for voice {voice}: budget again after its first take')
    rate, ratio = statistics.median(rates), statistics.median(ratios)
    out = {'voice': voice, 'productions_measured': len(rates), 'words_per_second': round(rate, 2), 'words': words,
           'narration_seconds': round(words / rate, 1), 'film_seconds': round(words / rate * ratio, 1)}
    if production:
        limit = load_contract(production)[0]['duration_seconds']
        out.update(duration_seconds=limit, fits=within(out['film_seconds'], limit['min'], limit['max']),
                   words_for_range=[None if v is None else round(v / ratio * rate) for v in (limit['min'], limit['max'])])
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--production', type=Path, help='productions/<slug>')
    parser.add_argument('--stage', choices=STAGES, help='Gate the storyboard plan, the assembled film (draft proof) or the delivery export')
    parser.add_argument('--film', type=Path, help='Film to measure; defaults to video/verification/proof.mp4')
    parser.add_argument('--digest', action='store_true', help='Print the composition hash a review record cites')
    parser.add_argument('--contract', type=Path, metavar='DIR', help='Validate DIR/CONTRACT.json (board or production) and print the effective rules')
    parser.add_argument('--fingerprint', type=Path, metavar='CLIP', help='Measure a reference clip, motion preview or export')
    parser.add_argument('--caption-region', metavar='X,Y,W,H', help='Caption region to mask for --fingerprint, in the clip\'s pixels')
    parser.add_argument('--budget', type=int, metavar='WORDS', help='Predict runtime for a spoken word count')
    parser.add_argument('--voice', help='Voice ID for --budget')
    parser.add_argument('--project-root', type=Path, default=Path(__file__).resolve().parents[4])
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        if args.budget is not None:
            if not args.voice:
                parser.error('--budget needs --voice')
            print(json.dumps(budget(args.project_root, args.budget, args.voice, args.production), indent=2))
        elif args.fingerprint:
            region = [float(n) for n in args.caption_region.split(',')] if args.caption_region else None
            if region is not None and len(region) != 4:
                parser.error('--caption-region takes X,Y,W,H')
            print(json.dumps(fingerprint(args.fingerprint, region), ensure_ascii=False, indent=2))
        elif args.contract:
            contract, judged, overrides, sha = load_contract(args.contract)
            print(json.dumps({'sha256': sha, **contract, 'judged': judged, 'overrides': sorted(overrides)},
                             ensure_ascii=False, indent=2))
        elif args.digest and args.production:
            print(composition_digest(args.production / 'video'))
        elif args.stage and args.production:
            verdict = gate(args.production, args.stage, args.film)
            print(json.dumps({k: verdict[k] for k in ('status', 'stage', 'disclose')}, ensure_ascii=False, indent=2))
            sys.exit({'passed': 0, 'failed': 1, 'needs_human_review': 2}[verdict['status']])
        else:
            parser.error('Use --production with --stage or --digest, --contract DIR, --fingerprint CLIP, or --budget with --voice')
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f'episode_qa: {error}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
