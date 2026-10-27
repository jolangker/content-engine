"""Final consistency audit and delivery index for the local six-episode correction."""
from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess
import sys

import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
sys.path.insert(0, str(ROOT / '.agents/skills/shortform-production/scripts'))
import audio_boundaries
import sound_design
import importlib.util

spec = importlib.util.spec_from_file_location('revision_finish', OUT / 'finish_revision.py')
finish = importlib.util.module_from_spec(spec)
spec.loader.exec_module(finish)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def ensure_links(path):
    text = path.read_text(encoding='utf-8')
    links = re.findall(r'\]\(([^)]+)\)', text)
    for target in links:
        if re.match(r'^[a-z]+://', target) or target.startswith('#'):
            continue
        assert (path.parent / target).exists(), (str(path), target)
    return len(links)


tracker = read(ROOT / 'TRACKER.json')
original_tracker = json.loads(subprocess.check_output(['git', 'show', 'HEAD:TRACKER.json'], cwd=ROOT))
assert tracker['boards'] == original_tracker['boards']
original_rows = {r['slug']: r for r in original_tracker['productions']}
v1 = {p['slug']: p for p in read(OUT / 'measurements.json')['productions']}
results, local_links = [], 0
for entry in tracker['productions']:
    if entry['board'] != 'ruang-di-antara':
        assert entry == original_rows[entry['slug']]
        continue
    production = ROOT / entry['path']
    video = production / 'video'
    assert entry['stage'] == 'content_package' and entry['status'] == 'complete', entry
    receipt = read(video / 'audio_boundaries.json')
    export = read(video / 'verification/export-v2.json')
    target = production / export['file']
    assert audio_boundaries.digest(target) == export['sha256']
    current = finish.fingerprint(video)
    assert read(video / 'verification/v2-check.json')['source_fingerprint'] == current
    assert read(video / 'verification/v2-check.json')['ok']
    assert read(video / 'verification/v2-review-accepted.json')['source_fingerprint'] == current
    assert read(video / 'verification/v2-preview-cleanup.json')['status'] == 'passed'
    assert export['decoded_proof_agent_inspected']
    preflight = audio_boundaries.verify(video)
    assert len(preflight['boundaries']) == export['narration_seams']
    encoded = read(video / 'verification/audio-boundaries-export-v2.json')
    assert encoded['status'] == 'passed' and encoded['export_sha256'] == export['sha256']
    cues = read(video / 'verification/sound-design-export-v2.json')
    assert cues['status'] == 'passed' and cues['export_sha256'] == export['sha256']
    assert all(c['passed'] for c in cues['cue_matches'])
    assert audio_boundaries.digest(ROOT / v1[entry['slug']]['export']) == v1[entry['slug']]['export_sha256']
    assert audio_boundaries.digest(video / receipt['source']) == receipt['source_sha256']
    baseline = production / 'revisions/audio-boundaries-v1'
    old_meta, new_meta = read(baseline / 'video/audio_meta.json'), read(video / 'audio_meta.json')
    assert old_meta['voices'] == new_meta['voices']
    publishing = production / 'PUBLISHING.json'
    prior = subprocess.run(['git', 'show', 'HEAD:' + publishing.relative_to(ROOT).as_posix()], cwd=ROOT, capture_output=True)
    if prior.returncode == 0:
        assert json.loads(publishing.read_bytes()) == json.loads(prior.stdout), f'External receipt changed: {publishing}'
    old_placement = read(baseline / 'video/placement.json') if (baseline / 'video/placement.json').exists() else {}
    if old_placement.get('pauses'):
        assert receipt['normalization']['continuity_correction_applied']
        native = audio_boundaries.decode(video / receipt['source'])
        master = audio_boundaries.decode(video / receipt['master_path'])
        assert len(native) == len(master)
        assert float(np.max(np.abs(native-master))) <= 2e-7
        assert read(video / 'verification/v2-native-continuity.json')['video_packets_preserved']
    for document in ['CONTENT_PACKAGE.md', 'VERIFICATION-v2.md']:
        local_links += ensure_links(production / document)
    package = (production / 'CONTENT_PACKAGE.md').read_text(encoding='utf-8')
    assert export['sha256'] in package and f'{production.name}-v2.mp4' in package
    # Ready-to-paste copy retains the previously approved episode wording.
    previous = (baseline / 'CONTENT_PACKAGE.md').read_text(encoding='utf-8')
    pattern = r'^## Instagram[^\n]*\n(.*?)(?=^## |\Z)'
    assert re.search(pattern, package, re.M | re.S)[1] == re.search(pattern, previous, re.M | re.S)[1]
    results.append({'slug': production.name, 'duration_s': export['duration_s'], 'sha256': export['sha256'],
                    'file': target.relative_to(ROOT).as_posix(), 'boundaries': export['narration_seams'],
                    'sfx_cues': export['sfx_cues'], 'min_incoming_quiet_ms': min(b['incoming_quiet_ms'] for b in receipt['boundaries']),
                    'max_export_cut_rms_dbfs': max(b['export_cut_rms_dbfs'] for b in encoded['boundaries']),
                    'lufs': export['loudness']['input_i'], 'true_peak': export['loudness']['input_tp'],
                    'v1_preserved': True, 'native_voice_cache_preserved': True, 'external_receipt_preserved': True})

for path in (ROOT / '.agents/skills/shortform-production/scripts').glob('*audio_boundaries.py'):
    ast.parse(path.read_text(encoding='utf-8'))
assert len(results) == 6 and sum(r['boundaries'] for r in results) == 88
report = {'status': 'complete', 'date': '2026-10-28', 'local_document_links_verified': local_links,
          'regression_tests': {'audio_boundaries': 7, 'narration_cache': 11},
          'productions': results, 'perceptual_listening': 'not performed', 'remote_delivery_changes': 'none'}
(OUT / 'revision-results.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
table = '\n'.join(f'| [{r["slug"]}](../../{r["file"]}) | {r["duration_s"]:.3f}s | {r["boundaries"]} | {r["min_incoming_quiet_ms"]:.1f}ms |' for r in results)
text = f'''# Ruang di Antara — corrected local exports v2

Completed 2026-10-28. Six local exports and their caption/content packages are complete. All 88 narration seams and {sum(r['sfx_cues'] for r in results)} inherited sound cues pass checks on the actual encoded MP4s. Existing v1 videos, source voice caches and external delivery receipts are preserved.

| Corrected MP4 | Duration | Verified seams | Minimum quiet after new visual |
| --- | --- | --- | --- |
{table}

Each production's exports folder contains matching `*-v2.srt`, `*-v2.vtt` and `export-proof-v2.png`. Its `CONTENT_PACKAGE.md` and `VERIFICATION-v2.md` identify the current local version, actual SHA-256, evidence and listening limits.

## Changes

- Pauses are placed inside measured quiet source audio, replacing midpoint-only timestamp cuts.
- Visual cuts use the integer 30fps clock and retain quiet margins on both sides. Captions, local choreography and SFX timing share the revised scene map.
- For recordings with old inserted pauses, the untouched source is spliced first, then normalized once to the inherited episode targets. This also removes the risk of rejoining an old limiter/gain edge inside a syllable. Individual word times remain estimates anchored to each acoustic utterance.
- Original layouts, source recordings and speech speed are retained. For the final audio-only normalization correction, verified H.264 video packets were preserved byte for byte.
- The shared [boundary helper](../../.agents/skills/shortform-production/scripts/audio_boundaries.py) and [audio contract](../../.agents/skills/shortform-production/references/audio-boundaries.md) prevent recurrence. Sound-design preflight rejects stale narration/timing, active narration at a cut or an inconsistent HTML scene map. Four historical audio preparation entry points now use the shared repair.

## Verification

All six pinned HyperFrames projects passed full checks and visual scene/seam review. Audio-only normalization refreshes reused the unchanged visual checks and reran acoustic preflight and actual encoded-mix checks, as recorded in each receipt. Full MP4 decode, source/export offset matching, exact frame counts, caption coverage and source-cache preservation passed. Eighteen regression tests pass: seven boundary tests and eleven existing narration/cache tests. All {local_links} current-package/verification local links resolve. Pipeline previews were stopped and their recorded PIDs no longer owned listening ports.

The [machine-readable results](revision-results.json) contain final export hashes and per-episode measurements. [Original diagnosis](REPORT.md) and source/export excerpts are retained separately.

Perceptual listening was not performed. These checks establish acoustic/encoded timing and preserved speech, not human approval of prosody or mix balance. External v1 drafts, scheduled posts and published posts were not replaced or reposted; the corrected v2 delivery is local.
'''
(OUT / 'FIX.md').write_text(text, encoding='utf-8')
ensure_links(OUT / 'FIX.md')
print(json.dumps({'status': 'complete', 'productions': len(results), 'narration_seams': 88,
                  'sfx_cues': sum(r['sfx_cues'] for r in results), 'local_links': local_links,
                  'index': str(OUT / 'FIX.md')}))
