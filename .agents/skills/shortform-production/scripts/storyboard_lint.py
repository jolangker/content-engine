"""Mechanical pre-animation linter for STORYBOARD.md (adapted from huashu-art-motion & cinetic craft laws)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from align_narration import normalize_for_asr

FRAME_HEAD_RE = re.compile(r'^#{2,3}\s*(?:Frame|Beat|Scene)\s+(\d+)\b(.*)$', re.I)
KEY_LINE_RE = re.compile(r'^-\s*([A-Za-z_]+)\s*:\s*(.*)$')

ABSTRACT_ONLY_WORDS = {
    'title', 'subtitle', 'heading', 'headline', 'text', 'words', 'copy', 'quote', 'slogan',
    'list', 'bullets', 'bullet', 'points', 'card', 'cards', 'slide', 'background', 'backdrop',
    'gradient', 'black', 'white', 'void', 'empty', 'blank', 'icon', 'icons', 'logo', 'chart',
    'judul', 'subjudul', 'teks', 'tulisan', 'kata', 'kalimat', 'kutipan', 'poin', 'daftar',
    'kartu', 'latar', 'polos', 'hitam', 'putih', 'kosong', 'ikon',
}

WEAK_VERBS_ONLY = {
    'appear', 'appears', 'appearing', 'show', 'shows', 'shown', 'display', 'displays',
    'fade', 'fades', 'fading', 'enter', 'enters', 'stay', 'stays', 'hold', 'holds', 'static',
    'muncul', 'tampil', 'ditampilkan', 'terlihat', 'memudar', 'diam', 'statis',
}

TEXT_DOMINATED_RE = re.compile(
    r'\b(?:kinetic\s*type|title\s*card|quote\s*card|stat\s*card|text\s*card|word\s*card|'
    r'kartu\s*teks|kartu\s*judul|kartu\s*kutipan|teks\s*besar\s*saja)\b',
    re.I,
)

PUSH_MOVES = ('push', 'push-in', 'zoom-in', 'zoom in', 'snap-zoom', 'crash-zoom', 'dolly-in', 'dorong', 'perbesar')
ACCENT_MOVES = ('snap-zoom', 'crash-zoom', 'whip', 'slam', 'smash', 'hentak', 'banting')


def parse_storyboard_sections(text: str) -> list[dict]:
    frames: list[dict] = []
    in_fence = False
    for line_no, raw in enumerate(text.splitlines(), 1):
        if raw.strip().startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        head = FRAME_HEAD_RE.match(raw)
        if head:
            title_part = head.group(2).strip(' :—–-')
            # Strip trailing (0.0-5.0s) range from title if present
            clean_title = re.sub(r'\(\s*\d+(?:\.\d+)?\s*(?:s)?\s*[-–—]\s*\d+(?:\.\d+)?\s*s?\s*\)\s*$', '', title_part).strip()
            frames.append({
                'number': int(head.group(1)),
                'line': line_no,
                'title': clean_title,
                'keys': {},
            })
        elif frames and (kv := KEY_LINE_RE.match(raw)):
            frames[-1]['keys'].setdefault(kv.group(1).lower(), kv.group(2).strip())
    for f in frames:
        m = re.match(r'\s*(\d+(?:\.\d+)?)', f['keys'].get('duration', ''))
        f['duration'] = float(m.group(1)) if m else None
    return frames


def _extract_num_tokens(text: str, lang: str = 'id') -> set[str]:
    if not text.strip():
        return set()
    return {tok for tok in normalize_for_asr(text, lang=lang) if tok.startswith('#num:')}


def _is_abstract_only(scene_desc: str) -> bool:
    tokens = [re.sub(r'[^a-zA-Z]+', '', w.lower()) for w in scene_desc.split()]
    tokens = [t for t in tokens if len(t) >= 3]
    if not tokens:
        return True
    meaningful = [t for t in tokens if t not in ABSTRACT_ONLY_WORDS and t not in WEAK_VERBS_ONLY]
    return len(meaningful) == 0


def _classify_camera(cam_raw: str) -> tuple[bool, bool, str]:
    low = cam_raw.lower().strip()
    is_accent = any(k in low for k in ACCENT_MOVES)
    is_push = any(k in low for k in PUSH_MOVES)
    return is_push, is_accent, low


def lint_storyboard(
    storyboard_path: Path,
    *,
    script_path: Path | None = None,
    lang: str = 'id',
    max_copy_words: int = 8,
    max_text_heavy_share: float = 0.30,
    strict_fields: bool = False,
) -> dict:
    """Validate STORYBOARD.md for concrete visual staging, script-to-screen number sync, copy brevity, and camera variety."""
    storyboard_path = Path(storyboard_path).resolve()
    if not storyboard_path.is_file():
        return {'status': 'failed', 'errors': [{'id': 'missing-file', 'detail': f'{storyboard_path} not found'}], 'warnings': []}

    text = storyboard_path.read_text(encoding='utf-8')
    frames = parse_storyboard_sections(text)
    if not frames:
        return {'status': 'failed', 'errors': [{'id': 'empty-storyboard', 'detail': 'No ## Frame N sections found'}], 'warnings': []}

    script_text = script_path.read_text(encoding='utf-8') if (script_path and script_path.is_file()) else ''
    script_nums = _extract_num_tokens(script_text, lang=lang) if script_text else set()

    errors: list[dict] = []
    warnings: list[dict] = []
    text_dominated_frames: list[int] = []
    push_streak = 0
    max_push_streak = 0
    accent_frames: list[int] = []
    transitions: list[str] = []

    for idx, f in enumerate(frames):
        fnum = f['number']
        keys = f['keys']
        scene_desc = keys.get('scene', '').strip()
        copy_text = (keys.get('on_screen_text') or keys.get('copy') or '').strip()
        vo_text = keys.get('voiceover', '').strip()
        cam_text = keys.get('camera', '').strip()
        trans = keys.get('transition_in', '').strip().lower()
        if trans:
            transitions.append(trans)

        if strict_fields and not scene_desc:
            errors.append({'id': 'missing-scene', 'frame': fnum, 'detail': f'Frame {fnum} is missing "- scene:" concrete visual description'})

        if scene_desc:
            if _is_abstract_only(scene_desc):
                errors.append({
                    'id': 'abstract-scene',
                    'frame': fnum,
                    'detail': f'Frame {fnum} describes abstract layout/text instead of a concrete object and action: "{scene_desc}"',
                })
            if TEXT_DOMINATED_RE.search(scene_desc):
                text_dominated_frames.append(fnum)
                if idx == 0 or idx == len(frames) - 1:
                    errors.append({
                        'id': 'bookend-text-card',
                        'frame': fnum,
                        'detail': f'Frame {fnum} (opening/closing frame) cannot be a bare text-dominated card',
                    })

        if copy_text and copy_text.lower() not in ('none', '-', '—', 'n/a'):
            words = [w for w in copy_text.split() if w.strip()]
            if len(words) > max_copy_words:
                errors.append({
                    'id': 'on-screen-copy-length',
                    'frame': fnum,
                    'detail': f'Frame {fnum} on-screen copy has {len(words)} words (limit {max_copy_words}): "{copy_text}"',
                })
            screen_nums = _extract_num_tokens(copy_text, lang=lang)
            if screen_nums and (vo_text or script_nums):
                allowed_nums = _extract_num_tokens(vo_text, lang=lang) | script_nums
                unmatched = sorted(screen_nums - allowed_nums)
                if unmatched:
                    errors.append({
                        'id': 'number-sync',
                        'frame': fnum,
                        'detail': f'Frame {fnum} on-screen numbers {unmatched} do not match spoken voiceover/script numbers',
                    })

        if cam_text:
            is_push, is_accent, _ = _classify_camera(cam_text)
            push_streak = push_streak + 1 if is_push else 0
            max_push_streak = max(max_push_streak, push_streak)
            if push_streak >= 3:
                errors.append({
                    'id': 'camera-push-run',
                    'frame': fnum,
                    'detail': f'Frame {fnum} continues a streak of {push_streak} consecutive push/zoom-in moves; alternate with hold, pull, pan, or cutaway',
                })
            if is_accent:
                accent_frames.append(fnum)
        else:
            push_streak = 0

    if text_dominated_frames:
        share = len(text_dominated_frames) / len(frames)
        if share > max_text_heavy_share + 1e-6:
            errors.append({
                'id': 'text-heavy-ratio',
                'frame': text_dominated_frames,
                'detail': f'Text-dominated frames ({len(text_dominated_frames)}/{len(frames)} = {share:.0%}) exceed {max_text_heavy_share:.0%} ceiling',
            })

    if accent_frames and len(frames) >= 4 and len(accent_frames) > len(frames) / 3.0 + 1e-6:
        warnings.append({
            'id': 'accent-camera-overuse',
            'frames': accent_frames,
            'detail': f'Accent camera moves ({len(accent_frames)}/{len(frames)}) exceed 1/3 of frames; reserve snap/whip/slam for key turns',
        })

    if len(transitions) >= 6:
        hard_cuts = sum(1 for t in transitions[1:] if t in ('cut', 'hard-cut', 'hard cut'))
        if hard_cuts == len(transitions) - 1:
            warnings.append({
                'id': 'all-hard-cuts',
                'detail': f'All {hard_cuts} scene seams are plain cuts; consider carried velocity handoffs, object morphs, or camera continuity on key turns',
            })

    return {
        'status': 'passed' if not errors else 'failed',
        'frame_count': len(frames),
        'max_push_streak': max_push_streak,
        'text_dominated_share': round(len(text_dominated_frames) / len(frames), 3),
        'errors': errors,
        'warnings': warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--storyboard', type=Path, help='Path to video/STORYBOARD.md')
    parser.add_argument('--production', type=Path, help='Path to productions/<slug> (resolves video/STORYBOARD.md and SCRIPT.md)')
    parser.add_argument('--script', type=Path, help='Optional SCRIPT.md path for number-sync verification')
    parser.add_argument('--lang', default='id', help='Language code for number normalization (id or en)')
    parser.add_argument('--strict', action='store_true', help='Require explicit - scene: key on every frame')
    args = parser.parse_args()

    if args.production:
        prod = args.production.resolve()
        sb_path = args.storyboard or (prod / 'video' / 'STORYBOARD.md')
        sc_path = args.script or (prod / 'SCRIPT.md')
    elif args.storyboard:
        sb_path = args.storyboard.resolve()
        sc_path = args.script.resolve() if args.script else None
    else:
        parser.error('Provide --production or --storyboard')

    report = lint_storyboard(sb_path, script_path=sc_path, lang=args.lang, strict_fields=args.strict)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['status'] == 'passed' else 1)


if __name__ == '__main__':
    main()
