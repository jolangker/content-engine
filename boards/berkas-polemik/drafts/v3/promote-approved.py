"""Promote the user-approved v3 board while preserving historical production references."""
import hashlib
import json
import re
import shutil
from pathlib import Path

DRAFT = Path(__file__).resolve().parent
BOARD = DRAFT.parent.parent
WORKSPACE = BOARD.parent.parent
ARCHIVE = BOARD / 'revisions' / 'v1'
if ARCHIVE.exists():
    raise RuntimeError('The v1 archive already exists. Review state before repeating promotion.')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# Copy only the previous root package, never recurse into drafts or the new archive.
root_files = [p for p in BOARD.iterdir() if p.is_file()]
ARCHIVE.mkdir(parents=True)
previous = {}
for path in root_files:
    shutil.copy2(path, ARCHIVE / path.name)
    previous[path.name] = sha(path)
shutil.copytree(BOARD / 'assets', ARCHIVE / 'assets')

# Preserve development snapshots and the old draft-dependent exporter for provenance.
history = BOARD / 'revisions' / 'v3-development'
shutil.copytree(DRAFT / 'revisions', history)
shutil.copy2(DRAFT / 'DIRECTION.md', history / 'draft-direction-before-approval.md')

production_hashes = {}
for slug in ('penutup-proklamasi', 'rawagede-kedaluwarsa'):
    folder = WORKSPACE / 'productions' / slug
    if folder.exists():
        for name in ('EPISODE.md', 'video/frame.md', 'video/index.html'):
            path = folder / name
            if path.exists():
                production_hashes[str(path.relative_to(WORKSPACE))] = sha(path)

# Approved documents resolve their dependencies at the canonical board root.
editorial = (DRAFT / 'EDITORIAL.md').read_text(encoding='utf-8')
editorial = re.sub(r'Status:.*?\n\n', 'Status: approved v3. The user applied the draft with “okay apply draftnya” on 20 October 2026. This is the active editorial guide for new productions selecting `berkas-polemik`.\n\n', editorial, count=1, flags=re.S)
editorial = editorial.replace('the full revised package remains pending review.', 'the full revised board package was accepted for application by the user.')
editorial = editorial.replace('revisions/editorial-before-dark-history-focus.md', 'revisions/v3-development/editorial-before-dark-history-focus.md')
(BOARD / 'EDITORIAL.md').write_text(editorial, encoding='utf-8')

frame = (DRAFT / 'frame.md').read_text(encoding='utf-8')
frame = frame.replace('version: "3-draft"', 'version: "3"\nstatus: approved')
frame = frame.replace('`../../assets/`', '`assets/`')
frame = frame.replace('The current three studies illustrate the identity', 'The three normal and two reversed studies illustrate the identity')
frame = frame.replace('## Motion and sound remain conceptual', '## Approved motion and audio direction')
frame = frame.replace('the [richer motion proposal](MOTION.md)', 'the [approved motion direction](MOTION.md)')
frame = frame.replace('the detailed choreography, timings, and mix remain proposals for future implementation.', 'the example choreography guides future implementation; episode-specific timing and mixing still require production verification.')
(BOARD / 'frame.md').write_text(frame, encoding='utf-8')

motion = (DRAFT / 'MOTION.md').read_text(encoding='utf-8')
motion = motion.replace('# Berkas Polemik — richer motion proposal', '# Berkas Polemik — motion direction v3')
motion = re.sub(r'Status:.*?\n\n', 'Status: approved v3 direction. The user applied the draft with “okay apply draftnya” on 20 October 2026. Examples remain reusable planning guidance; approval does not claim that a new episode animation has been rendered.\n\n', motion, count=1, flags=re.S)
motion = motion.replace('../../../../productions/', '../../productions/')
motion = motion.replace('revisions/motion-before-transition-feedback.md', 'revisions/v3-development/motion-before-transition-feedback.md')
motion = motion.replace('the replacement choices below remain a proposed implementation vocabulary, not an approved new render.', 'the replacement vocabulary below is approved guidance; this does not represent a newly rendered video.')
motion = motion.replace('The desired increase in motion richness is confirmed. The specific choreography and allocations below are proposals, not previously approved animation.', 'The motion language below is accepted as board guidance. The scene-by-scene distribution is an illustrative template, adaptable to the actual researched script.')
motion = motion.replace('## Proposed movement vocabulary', '## Movement vocabulary').replace('## Proposed distribution across the sixteen scenes', '## Illustrative distribution across the sixteen scenes')
motion = motion.replace('| Proposed treatment |', '| Treatment |')
(BOARD / 'MOTION.md').write_text(motion, encoding='utf-8')

# The root HTML is the editable source of truth; it does not rebuild from older drafts.
html = (DRAFT / 'style-board.html').read_text(encoding='utf-8')
html = html.replace('../../assets/', 'assets/')
html = html.replace('Refinement v3 / Draft', 'Approved v3')
html = html.replace('REFINEMENT V3 · DRAF UNTUK DITINJAU', 'V3 · DISETUJUI / BOARD AKTIF')
html = html.replace('V3 DRAF', 'V3 DISETUJUI')
html = html.replace('V1 TETAP DISETUJUI · VISUAL V3 MENUNGGU TINJAUAN', '90 DETIK · 16 ADEGAN · 14 GELAP + 2 REVERSED')
html = html.replace('SEJARAH INDONESIA / PENELUSURAN ARSIP', 'SEJARAH KELAM / DUGAAN KONSPIRASI INDONESIA')
html = html.replace('Menguji polemik sejarah dari jejak<br>yang bisa ditelusuri.', 'Membedah sejarah kelam dan dugaan konspirasi<br>di Indonesia lewat penelusuran sumber.')
html = html.replace('04 / Arah gerak: benda dulu, penjelasan menyusul.', '05 / Arah gerak: benda dulu, penjelasan menyusul.')
html = html.replace('Tanpa gerak elastis.', 'Tanpa gerak elastis.')
html = html.replace('Perlihatkan perbedaan atau penguatnya, tanpa gerak elastis.', 'Perlihatkan hubungan bukti. Transisi mengikuti isi; slide seluruh frame ditiadakan.')
html = html.replace('Kenalkan jenis dan konteks dokumen sebelum menyorot detail.', 'Bangun kedalaman meja, sumber, dan anotasi sebelum menyorot detail.')
html = html.replace('Pertanyaan → identitas sumber → baca bukti → uji tafsir → temuan dan batas.', 'Sejarah kelam dan dugaan konspirasi Indonesia. Riset dari buku, jurnal, dan dokumen. Pertanyaan → bukti → tafsir → temuan dan batas.')
reverse_html = (DRAFT / 'reversed-studies.html').read_text(encoding='utf-8')
reversed_articles = re.findall(r'<article class="frame is-reversed.*?</article>', reverse_html, re.S)
assert len(reversed_articles) == 2
reverse_css = '''
.frame.is-reversed{background:var(--paper);color:var(--bg)}
.frame.is-reversed .brand,.frame.is-reversed .sample-label,.frame.is-reversed h3{color:var(--bg)}
.frame.is-reversed h3 .mark{color:var(--red)}
.reverse-guide{padding:28px;background:var(--surface);align-self:start;border-top:4px solid var(--tape)}
.reverse-guide h3{font-size:28px;line-height:1.2;margin-bottom:18px}
.reverse-guide p{font-size:17px;line-height:1.5;margin-bottom:18px}
'''
html = html.replace('</style>', reverse_css + '\n</style>', 1)
section = '''<section class="samples reversed-palette">
<div class="sectionhead"><h2>04 / Dua momen dramatis. Warna dibalik.</h2><small>2 DARI 16 ADEGAN · POSISI MENGIKUTI NASKAH</small></div>
<p class="examples-note">Studi mandiri mode terang. Latar manila dan teks karbon; ilustrasi editorial disesuaikan, dokumen sejarah asli tetap dijaga.</p>
<div class="frames">'''
for article, label in zip(reversed_articles, ('D / Perbandingan dalam mode terang', 'E / Detail dalam mode terang')):
    section += f'<div><div class="study-window">{article}</div><div class="study-caption"><b>{label}</b></div></div>'
section += '''<aside class="reverse-guide"><h3>14 gelap + 2 reversed.</h3><p>Dua adegan terang dipilih pada momen dramatis sesuai naskah. Total tetap 16 adegan, sekitar 90 detik.</p><p>Karbon / manila: <b>14,43:1</b>.<br>Merah / manila: <b>4,41:1</b>, untuk judul besar atau penanda.</p><p>Metadata dan caption memakai karbon. Kuning dan abu-abu tidak dipakai untuk teks kecil esensial di latar manila.</p><p>Perpindahan warna mengikuti ketukan narasi. Tanpa slide seluruh frame.</p></aside></div></section>'''
html = html.replace('<section class="grammar">', section + '\n<section class="grammar">', 1)
(BOARD / 'style-board.html').write_text(html, encoding='utf-8')

exporter = (DRAFT / 'export-board.py').read_text(encoding='utf-8')
exporter = exporter.replace("page.locator('.frames').screenshot", "page.locator('.frames').first.screenshot")
exporter = exporter.replace('for index in range(3):', 'for index in range(page.locator(".frame").count()):')
exporter = exporter.replace('"human_approval": False', '"human_approval": True, "approval_basis": "User: okay apply draftnya", "version": "3", "normal_studies": 3, "reversed_studies": 2')
(BOARD / 'export-board.py').write_text(exporter, encoding='utf-8')
shutil.copy2(DRAFT / 'reversed-proof.py', BOARD / 'reversed-proof.py')

# The old optional PDF remains available in its versioned archive; do not expose it as v3.
old_pdf = BOARD / 'style-board.pdf'
if old_pdf.exists():
    assert sha(old_pdf) == sha(ARCHIVE / 'style-board.pdf')
    old_pdf.unlink()

direction = '''# Berkas Polemik — approved board v3

Status: approved. The user accepted application of the developed draft through **“okay apply draftnya”** on 20 October 2026. This is the active board for new productions selecting `berkas-polemik`.

## Editorial identity

**“Berkas Polemik membedah sejarah kelam dan dugaan konspirasi di Indonesia lewat penelusuran sumber.”**

Focus on dark Indonesian history and consequential conspiracy/plot questions. Books, journals, and documents anchor the research. Daily political news is not a separate pillar. Select a consequential event, a substantive audience question, and a traceable evidence path; distinguish established findings, attributed allegations, interpretation, and remaining uncertainty. See [EDITORIAL.md](EDITORIAL.md).

## Accepted production and visual rules

- Approximately 90 seconds with exactly sixteen primary storyboard scenes. Internal developments do not add primary scenes.
- One dominant explanatory visual per scene; sparse headline copy and no explanatory frame paragraphs by default.
- Retain carbon/manila/red and the local Space Grotesk, Space Mono, and Newsreader families.
- Fourteen dark scenes and two reversed scenes at script-driven dramatic beats: manila background with carbon text. Main contrast is approximately 14.43:1. Small text avoids yellow/steel on the light field; red is reserved for large display or graphic annotation.
- Richer spatial/object choreography and purposeful source-to-detail developments. Full-scene slide/push transitions are excluded; choose cuts, anchored matches, source/detail continuity, local masks, and selective dissolves by meaning.

Visual tokens: [frame.md](frame.md). Motion direction: [MOTION.md](MOTION.md). Timings and scene allocations are reusable planning guidance, to be fitted and checked in each actual production. Approval of the direction does not claim an episode has been animated or perceptually verified.

## Active artifacts

- [style-board.html](style-board.html): editable canonical source, with local `assets/` dependencies.
- [style-board.png](style-board.png): normal and reversed identity studies, all labelled simulation.
- [frame-studies.png](frame-studies.png): three normal-mode studies.
- [reversed-studies.png](reversed-studies.png): normal/reversed comparison.
- `study-01.png` through `study-05.png`: native 1080 × 1920 studies; 04–05 are reversed.
- `phone-study-01.png` through `phone-study-05.png`: phone-scale checks.
- [QA.json](QA.json) and [reversed-contrast-QA.json](reversed-contrast-QA.json): layout/font/contrast checks.
- [export-board.py](export-board.py) and [reversed-proof.py](reversed-proof.py): static export workflows. Edit the root HTML directly; the active source does not depend on draft builders.

These are independent identity studies, not an episode sequence or a completed sixteen-scene storyboard. Motion and audio are approved directions requiring future episode implementation and verification.

## Preservation and production continuity

The previous root package, its font assets, and the previous PDF are preserved at [revisions/v1/](revisions/v1/). The old PDF belongs to v1; current v3 review exports are PNG plus editable HTML. Earlier development notes are retained in `revisions/v3-development/` and the existing `drafts/` folders.

The separately registered `berkas-polemik-v3-draft` path remains a historical draft reference for `penutup-proklamasi` and `rawagede-kedaluwarsa`. Do not select that legacy row for a new production; use `berkas-polemik`. Existing briefs, specs, selections, media, and exports have not been rewritten or re-rendered. Continuing an existing production uses its recorded direction unless the user requests a revision.

## Current state and next action

The v3 package is approved and applied; there is no remaining board approval gate. Future episode creation or revision follows an explicit production request and the recorded execution policy. No episode was started by this promotion.
'''
(BOARD / 'DIRECTION.md').write_text(direction, encoding='utf-8')

legacy = (DRAFT / 'DIRECTION.md').read_text(encoding='utf-8')
notice = '''# Historical draft reference — superseded for new productions

The user applied the developed draft as the approved canonical [Berkas Polemik v3 board](../../DIRECTION.md) on 20 October 2026. The notes below retain their historical review statuses. This registered draft path is preserved for productions that already selected `berkas-polemik-v3-draft`; it is not the active choice for new episodes. Existing production references remain unchanged.

---

'''
(DRAFT / 'DIRECTION.md').write_text(notice + legacy, encoding='utf-8')

# Re-read and preserve the complete concurrent tracker state; change only the canonical row.
tracker_path = WORKSPACE / 'TRACKER.json'
tracker_bytes = tracker_path.read_bytes()
tracker = json.loads(tracker_bytes.decode('utf-8-sig'))
canonical = next(b for b in tracker['boards'] if b['slug'] == 'berkas-polemik')
canonical.update(status='approved', path='boards/berkas-polemik')
assert all((WORKSPACE / b['path']).is_dir() for b in tracker['boards'])
assert tracker_path.read_bytes() == tracker_bytes, 'Tracker changed during promotion; reconcile before writing.'
tracker_path.write_text(json.dumps(tracker, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
for name, expected in production_hashes.items():
    assert sha(WORKSPACE / name) == expected, f'Existing production changed: {name}'
for name, expected in previous.items():
    assert sha(ARCHIVE / name) == expected, f'Archive mismatch: {name}'
receipt = {'version':'3','status':'approved','approval':'okay apply draftnya','date':'2026-10-20',
           'previous_package':'revisions/v1','previous_root_hashes':previous,
           'existing_production_hashes':production_hashes,
           'legacy_draft_registry_entry':'preserved unchanged for historical production references',
           'visual_export_verification':'pending'}
(BOARD / 'PROMOTION.json').write_text(json.dumps(receipt,indent=2)+'\n', encoding='utf-8')
print('Approved v3 applied; previous root archived, existing production references retained.')
