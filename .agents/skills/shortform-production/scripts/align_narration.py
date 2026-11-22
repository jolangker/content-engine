"""WhisperX-style two-stage narration alignment (ASR + Wav2Vec2 CTC forced alignment) and script verification."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import difflib
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
import unicodedata

import numpy as np

SAMPLE_RATE = 16000
PAD_SECONDS = 0.5
DEFAULT_CTC_MODELS = {
    'id': 'indonesian-nlp/wav2vec2-large-xlsr-indonesian',
    'en': 'facebook/wav2vec2-base-960h',
}

_TAG_RE = re.compile(r'\[([^\[\]]+)\]')
_WORD_PUNCT = '.,;:!?"()[]{}\u2026\u201c\u201d\u2018\u2019«»—–-'

_ID_UNITS = {
    'nol': 0, 'kosong': 0, 'satu': 1, 'dua': 2, 'tiga': 3, 'empat': 4,
    'lima': 5, 'enam': 6, 'tujuh': 7, 'delapan': 8, 'sembilan': 9,
    'sepuluh': 10, 'sebelas': 11, 'seratus': 100, 'seribu': 1000, 'sejuta': 1_000_000,
}
_ID_SCALES = {'puluh': 10, 'ratus': 100, 'ribu': 1000, 'juta': 1_000_000, 'miliar': 1_000_000_000}

_EN_UNITS = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
    'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12,
    'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
    'eighteen': 18, 'nineteen': 19,
    'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60,
    'seventy': 70, 'eighty': 80, 'ninety': 90,
}
_EN_SCALES = {'hundred': 100, 'thousand': 1000, 'million': 1_000_000, 'billion': 1_000_000_000}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def strip_delivery_tags(text: str) -> str:
    cleaned = _TAG_RE.sub(' ', text)
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)
    cleaned = re.sub(r' *\n *', '\n', cleaned)
    return cleaned.strip()


def extract_tagged_slots(text: str) -> list[dict]:
    """Return spoken word index before each [tag] and normalized tag words to detect spoken-aloud tags."""
    slots = []
    pos = 0
    spoken_so_far = 0
    for match in _TAG_RE.finditer(text):
        chunk = text[pos:match.start()].strip()
        if chunk:
            spoken_so_far += len(chunk.split())
        tag_words = [re.sub(r'[^a-z0-9]+', '', w.lower()) for w in match.group(1).split()]
        tag_words = [w for w in tag_words if w]
        if tag_words:
            slots.append({'word_index': spoken_so_far, 'raw': match.group(0), 'tokens': tag_words})
        pos = match.end()
    return slots


def spoken_script_words(text: str) -> list[str]:
    clean = strip_delivery_tags(text)
    words = [w.strip() for w in clean.split() if w.strip()]
    if not words:
        raise ValueError('Spoken script contains no words after removing delivery tags')
    return words


def decode_audio_16k(path: Path) -> tuple[np.ndarray, float]:
    cmd = ['ffmpeg', '-v', 'error', '-i', str(path), '-vn', '-ac', '1', '-ar', str(SAMPLE_RATE), '-f', 'f32le', 'pipe:1']
    proc = subprocess.run(cmd, capture_output=True, check=True)
    samples = np.frombuffer(proc.stdout, dtype='<f4').astype(np.float32)
    if samples.size == 0 or not np.isfinite(samples).all() or not np.any(samples):
        raise ValueError(f'Empty, silent, or invalid audio: {path}')
    probe = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(path)],
        capture_output=True, text=True, check=True,
    )
    duration = float(json.loads(probe.stdout)['format']['duration'])
    return samples, duration


def _format_num_value(val: float, pct: bool = False) -> str:
    if abs(val - round(val)) < 1e-9:
        text = str(int(round(val)))
    else:
        text = f'{val:.6f}'.rstrip('0').rstrip('.')
    return f'#num:{text}{"%" if pct else ""}'


def _parse_digit_token(raw: str, lang: str) -> tuple[float, bool] | None:
    core = raw.strip(_WORD_PUNCT)
    pct = core.endswith('%')
    if pct:
        core = core[:-1].strip()
    if not core:
        return None
    if lang == 'id':
        if re.fullmatch(r'\d{1,3}(?:\.\d{3})+(?:,\d+)?', core):
            core = core.replace('.', '').replace(',', '.')
        elif re.fullmatch(r'\d+,\d+', core):
            core = core.replace(',', '.')
    else:
        if re.fullmatch(r'\d{1,3}(?:,\d{3})+(?:\.\d+)?', core):
            core = core.replace(',', '')
    if re.fullmatch(r'\d+(?:\.\d+)?', core):
        return float(core), pct
    return None


def _consume_id_number(tokens: list[str], start: int) -> tuple[float, int] | None:
    i = start
    n = len(tokens)
    total = 0
    current = 0
    consumed = False
    while i < n:
        w = tokens[i]
        if w in _ID_UNITS:
            val = _ID_UNITS[w]
            if val >= 100:
                if val >= 1000:
                    total += (current or 0) + val
                    current = 0
                else:
                    current += val
            else:
                current += val
            consumed = True
            i += 1
        elif w == 'belas' and consumed and 1 <= current <= 9:
            current += 10
            i += 1
        elif w in _ID_SCALES and consumed:
            scale = _ID_SCALES[w]
            if scale >= 1000:
                total += (current or 1) * scale
                current = 0
            else:
                current = (current % scale) + ((current // scale) * scale) if current >= scale else (current or 1) * scale
            i += 1
        else:
            break
    if not consumed:
        return None
    value = float(total + current)
    if i + 1 < n and tokens[i] == 'koma':
        frac_digits = []
        j = i + 1
        while j < n and tokens[j] in _ID_UNITS and _ID_UNITS[tokens[j]] < 10:
            frac_digits.append(str(_ID_UNITS[tokens[j]]))
            j += 1
        if frac_digits:
            value = float(f'{int(value)}.{"".join(frac_digits)}')
            i = j
    return value, i


def _consume_en_number(tokens: list[str], start: int) -> tuple[float, int] | None:
    i = start
    n = len(tokens)
    total = 0
    current = 0
    consumed = False
    while i < n:
        w = tokens[i]
        if w == 'and' and consumed:
            i += 1
            continue
        if w in _EN_UNITS:
            current += _EN_UNITS[w]
            consumed = True
            i += 1
        elif w in _EN_SCALES and (consumed or w in ('hundred', 'thousand', 'million')):
            scale = _EN_SCALES[w]
            if scale >= 1000:
                total += (current or 1) * scale
                current = 0
            else:
                current = (current or 1) * scale
            consumed = True
            i += 1
        else:
            break
    if not consumed:
        return None
    if tokens[start] == 'and':
        return None
    value = float(total + current)
    if i + 1 < n and tokens[i] == 'point':
        frac_digits = []
        j = i + 1
        while j < n and tokens[j] in _EN_UNITS and _EN_UNITS[tokens[j]] < 10:
            frac_digits.append(str(_EN_UNITS[tokens[j]]))
            j += 1
        if frac_digits:
            value = float(f'{int(value)}.{"".join(frac_digits)}')
            i = j
    return value, i


def normalize_for_asr(text: str, lang: str = 'id', aliases: dict[str, str] | None = None) -> list[str]:
    """Normalize text into canonical lowercase lexical and #num:<val> tokens for script verification."""
    lang_code = (lang or 'id').lower().split('-')[0]
    alias_map = {k.lower().strip(): v.lower().strip() for k, v in (aliases or {}).items()}
    norm = unicodedata.normalize('NFKC', strip_delivery_tags(text))
    raw_words = []
    for tok in norm.replace('\n', ' ').split():
        # Split hyphenated words unless it is a formatted number; preserve Indonesian reduplication comparisons cleanly.
        parsed = _parse_digit_token(tok, lang_code)
        if parsed is not None:
            raw_words.append(tok)
        else:
            for sub in re.split(r'[-–—/]+', tok):
                if sub.strip(_WORD_PUNCT):
                    raw_words.append(sub)
    lexical = []
    for raw in raw_words:
        parsed = _parse_digit_token(raw, lang_code)
        if parsed is not None:
            lexical.append(('digit', parsed[0], parsed[1]))
            continue
        w = re.sub(r'[^a-z0-9%]', '', raw.lower())
        if not w:
            continue
        w = alias_map.get(w, w)
        lexical.append(('word', w, False))

    words_only = [item[1] if item[0] == 'word' else '' for item in lexical]
    pct_words = {'persen'} if lang_code == 'id' else {'percent', 'pct'}
    out: list[str] = []
    i = 0
    while i < len(lexical):
        kind, val, pct = lexical[i]
        if kind == 'digit':
            if not pct and i + 1 < len(lexical) and lexical[i + 1][0] == 'word' and lexical[i + 1][1] in pct_words:
                pct = True
                i += 1
            out.append(_format_num_value(val, pct))
            i += 1
            continue
        consumed = _consume_id_number(words_only, i) if lang_code == 'id' else _consume_en_number(words_only, i)
        if consumed is not None:
            num_val, next_i = consumed
            is_pct = next_i < len(lexical) and lexical[next_i][0] == 'word' and lexical[next_i][1] in pct_words
            if is_pct:
                next_i += 1
            out.append(_format_num_value(num_val, is_pct))
            i = next_i
            continue
        out.append(val)
        i += 1
    return out


def verify_asr_against_script(
    tagged_script: str,
    observed_text: str,
    *,
    lang: str = 'id',
    threshold: float = 0.90,
    aliases: dict[str, str] | None = None,
) -> dict:
    """Verify ASR transcript against approved script: detect spoken delivery tags, number errors, and clipped/misread words."""
    expected_tokens = normalize_for_asr(tagged_script, lang=lang, aliases=aliases)
    observed_tokens = normalize_for_asr(observed_text, lang=lang, aliases=aliases)
    raw_observed_words = [re.sub(r'[^a-z0-9]+', '', w.lower()) for w in unicodedata.normalize('NFKC', observed_text).split()]
    raw_observed_words = [w for w in raw_observed_words if w]
    raw_expected_words = [re.sub(r'[^a-z0-9]+', '', w.lower()) for w in spoken_script_words(tagged_script)]
    raw_expected_words = [w for w in raw_expected_words if w]

    # 1. Detect delivery tags read aloud at their insertion slots.
    tags_spoken = []
    raw_matcher = difflib.SequenceMatcher(a=raw_expected_words, b=raw_observed_words, autojunk=False)
    inserted_spans = [
        (i1, j1, j2, raw_observed_words[j1:j2])
        for op, i1, i2, j1, j2 in raw_matcher.get_opcodes()
        if op in ('insert', 'replace')
    ]
    for slot in extract_tagged_slots(tagged_script):
        idx = slot['word_index']
        tag_toks = slot['tokens']
        for i1, j1, j2, obs_slice in inserted_spans:
            if abs(i1 - idx) <= 1 and obs_slice:
                # Check if the inserted ASR words match the tag's words.
                joined_tag = ' '.join(tag_toks)
                joined_obs = ' '.join(obs_slice)
                if joined_tag in joined_obs or (len(tag_toks) == 1 and tag_toks[0] in obs_slice and len(tag_toks[0]) >= 4):
                    tags_spoken.append({'tag': slot['raw'], 'heard': ' '.join(obs_slice), 'at_word': idx})
                    break

    # 2. Align normalized tokens and enforce strict numeric equality.
    matcher = difflib.SequenceMatcher(a=expected_tokens, b=observed_tokens, autojunk=False)
    similarity = round(matcher.ratio(), 4)
    mismatches = []
    number_mismatches = []
    clipped_edges = []

    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'equal':
            continue
        exp_span = expected_tokens[i1:i2]
        obs_span = observed_tokens[j1:j2]
        entry = {'op': op, 'expected': exp_span, 'heard': obs_span, 'expected_range': [i1, i2]}
        mismatches.append(entry)
        if any(t.startswith('#num:') for t in exp_span) or any(t.startswith('#num:') for t in obs_span):
            number_mismatches.append(entry)
        if i1 == 0 and op in ('delete', 'replace') and not obs_span:
            clipped_edges.append('opening_words_missing')
        if i2 == len(expected_tokens) and op in ('delete', 'replace') and not obs_span:
            clipped_edges.append('closing_words_missing')

    passed = (
        similarity >= threshold
        and not tags_spoken
        and not number_mismatches
        and not clipped_edges
    )
    return {
        'passed': passed,
        'similarity': similarity,
        'threshold': threshold,
        'numbers_matched': len(number_mismatches) == 0,
        'tags_spoken': tags_spoken,
        'number_mismatches': number_mismatches,
        'clipped_edges': clipped_edges,
        'mismatches': mismatches[:20],
        'expected_token_count': len(expected_tokens),
        'observed_token_count': len(observed_tokens),
    }


@dataclass
class Point:
    token_index: int
    time_index: int
    score: float


@dataclass
class Segment:
    label: str
    start: int
    end: int
    score: float


def build_ctc_trellis(emission: np.ndarray, tokens: list[int], blank_id: int = 0) -> np.ndarray:
    """Compute CTC forced-alignment trellis (WhisperX / Viterbi log-domain dynamic programming)."""
    num_frame = emission.shape[0]
    num_tokens = len(tokens)
    if num_tokens == 0:
        raise ValueError('Cannot align empty token list')
    if num_frame < num_tokens:
        raise ValueError(f'Audio frames ({num_frame}) fewer than target characters ({num_tokens})')
    trellis = np.full((num_frame, num_tokens), -np.inf, dtype=np.float64)
    trellis[0, 0] = emission[0, blank_id]
    # Allow starting directly on first character as well as blank.
    trellis[0, 0] = np.logaddexp(emission[0, blank_id], emission[0, tokens[0]])
    for t in range(1, num_frame):
        trellis[t, 0] = trellis[t - 1, 0] + emission[t, blank_id]
    for t in range(num_frame - 1):
        stay = trellis[t, :] + emission[t + 1, blank_id]
        # Staying on the same character or blank:
        char_stay = trellis[t, :] + emission[t + 1, tokens]
        keep = np.maximum(stay, char_stay)
        # Advancing to the next character:
        move = trellis[t, :-1] + emission[t + 1, tokens[1:]]
        trellis[t + 1, 0] = keep[0]
        trellis[t + 1, 1:] = np.maximum(keep[1:], move)
    return trellis


def backtrack_ctc(trellis: np.ndarray, emission: np.ndarray, tokens: list[int], blank_id: int = 0) -> list[Point]:
    t, j = trellis.shape[0] - 1, trellis.shape[1] - 1
    path = [Point(j, t, float(np.exp(emission[t, tokens[j]])))]
    while j > 0:
        if t <= 0:
            raise ValueError('CTC backtracking exhausted frames before first token')
        p_stay_blank = emission[t, blank_id]
        p_stay_char = emission[t, tokens[j]]
        p_stay = max(p_stay_blank, p_stay_char)
        stayed = trellis[t - 1, j] + p_stay
        changed = trellis[t - 1, j - 1] + emission[t, tokens[j]]
        t -= 1
        if changed > stayed:
            j -= 1
        prob = float(np.exp(emission[t, tokens[j]]))
        path.append(Point(j, t, prob))
    while t > 0:
        prob = float(np.exp(emission[t - 1, tokens[0]]))
        path.append(Point(0, t - 1, prob))
        t -= 1
    return path[::-1]


def ctc_align_words(
    emission: np.ndarray,
    script_words: list[str],
    vocab: dict[str, int],
    duration_s: float,
    *,
    blank_id: int = 0,
    offset_s: float = 0.0,
) -> list[dict]:
    """Align exact ground-truth script_words onto CTC frame log-probabilities and return timed word dicts."""
    # Map vocabulary case-insensitively and locate word separator token ('|' or ' ').
    norm_vocab = {k: v for k, v in vocab.items()}
    lower_vocab = {k.lower(): v for k, v in vocab.items()}
    sep_char = '|' if '|' in norm_vocab else (' ' if ' ' in norm_vocab else None)

    char_stream: list[int] = []
    char_to_word: list[int] = []

    for w_idx, raw_word in enumerate(script_words):
        # Expand digits lightly to characters if present in vocab; otherwise strip non-vocab chars.
        clean = unicodedata.normalize('NFKC', raw_word)
        matched_chars: list[int] = []
        for ch in clean:
            if ch in norm_vocab and norm_vocab[ch] != blank_id:
                matched_chars.append(norm_vocab[ch])
            elif ch.lower() in lower_vocab and lower_vocab[ch.lower()] != blank_id:
                matched_chars.append(lower_vocab[ch.lower()])
            elif ch.upper() in norm_vocab and norm_vocab[ch.upper()] != blank_id:
                matched_chars.append(norm_vocab[ch.upper()])
        if matched_chars:
            for cid in matched_chars:
                char_stream.append(cid)
                char_to_word.append(w_idx)
            if sep_char is not None and w_idx < len(script_words) - 1:
                char_stream.append(norm_vocab[sep_char])
                char_to_word.append(-1)

    num_frames = emission.shape[0]
    frame_dur = duration_s / max(1, num_frames)

    if not char_stream or num_frames < len(char_stream):
        # Uniform fallback within window if pure symbols/numbers had no alphabetic CTC characters.
        step = duration_s / len(script_words)
        return [
            {
                'text': w,
                'start': round(offset_s + idx * step, 4),
                'end': round(offset_s + (idx + 1) * step, 4),
                'score': 0.5,
            }
            for idx, w in enumerate(script_words)
        ]

    trellis = build_ctc_trellis(emission, char_stream, blank_id=blank_id)
    path = backtrack_ctc(trellis, emission, char_stream, blank_id=blank_id)

    # Group contiguous points per token_index.
    token_spans: list[tuple[int, int, int, float]] = []
    i = 0
    while i < len(path):
        j = i
        while j < len(path) and path[j].token_index == path[i].token_index:
            j += 1
        tok_idx = path[i].token_index
        # Trim leading blank-heavy frames inside the first token's pre-speech silence.
        pts = path[i:j]
        if tok_idx == 0 and len(pts) > 1:
            active = [p for p in pts if emission[p.time_index, char_stream[0]] >= emission[p.time_index, blank_id] - 2.5]
            if active:
                pts = active
        if tok_idx == len(char_stream) - 1 and len(pts) > 1:
            active = [p for p in pts if emission[p.time_index, char_stream[-1]] >= emission[p.time_index, blank_id] - 2.5]
            if active:
                pts = active
        start_f = pts[0].time_index
        end_f = pts[-1].time_index + 1
        avg_score = float(np.mean([p.score for p in pts]))
        token_spans.append((tok_idx, start_f, end_f, avg_score))
        i = j

    word_frames: dict[int, list[tuple[int, int, float]]] = {}
    for tok_idx, sf, ef, sc in token_spans:
        w_idx = char_to_word[tok_idx]
        if w_idx >= 0:
            word_frames.setdefault(w_idx, []).append((sf, ef, sc))

    aligned: list[dict] = []
    prev_end = offset_s
    total_end = offset_s + duration_s
    for w_idx, raw_word in enumerate(script_words):
        spans = word_frames.get(w_idx)
        if spans:
            st = offset_s + spans[0][0] * frame_dur
            en = offset_s + spans[-1][1] * frame_dur
            sc = round(float(np.mean([s[2] for s in spans])), 4)
        else:
            # Interpolate unvoiced/numeric token between neighbors.
            next_start = total_end
            for later in range(w_idx + 1, len(script_words)):
                if later in word_frames:
                    next_start = offset_s + word_frames[later][0][0] * frame_dur
                    break
            gap = max(0.04, (next_start - prev_end) / max(1, (later - w_idx if 'later' in locals() else 1)))
            st = prev_end
            en = min(total_end, st + gap)
            sc = 0.5
        st = max(prev_end, min(st, total_end - 0.01))
        en = max(st + 0.01, min(en, total_end))
        prev_end = en
        aligned.append({'text': raw_word, 'start': round(st, 4), 'end': round(en, 4), 'score': sc})
    return aligned


def map_script_words_to_asr_words(script_words: list[str], asr_words: list[dict], duration_s: float) -> list[dict]:
    """Monotonically map exact ground-truth script words onto ASR word timestamps when CTC is skipped."""
    if not asr_words:
        raise ValueError('ASR produced no word timestamps')
    norm = lambda s: re.sub(r'[^a-z0-9]+', '', unicodedata.normalize('NFKC', s).lower())
    a_norm = [norm(w) or w for w in script_words]
    b_norm = [norm(w['text']) or w['text'] for w in asr_words]
    matcher = difflib.SequenceMatcher(a=a_norm, b=b_norm, autojunk=False)
    mapped: list[dict | None] = [None] * len(script_words)

    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'equal':
            for offset in range(i2 - i1):
                src = asr_words[j1 + offset]
                mapped[i1 + offset] = {
                    'text': script_words[i1 + offset],
                    'start': float(src['start']),
                    'end': float(src['end']),
                    'score': round(float(src.get('probability', src.get('score', 0.8))), 4),
                }
        elif op == 'replace' and (j2 - j1) > 0 and (i2 - i1) > 0:
            win_start = float(asr_words[j1]['start'])
            win_end = float(asr_words[j2 - 1]['end'])
            span = max(0.02 * (i2 - i1), win_end - win_start)
            step = span / (i2 - i1)
            for k in range(i2 - i1):
                mapped[i1 + k] = {
                    'text': script_words[i1 + k],
                    'start': win_start + k * step,
                    'end': win_start + (k + 1) * step,
                    'score': round(float(np.mean([asr_words[m].get('probability', 0.7) for m in range(j1, j2)])), 4),
                }

    # Fill any unmatched deletions monotonically between surrounding matched words.
    prev_end = max(0.0, float(asr_words[0]['start']) - 0.05)
    idx = 0
    while idx < len(mapped):
        if mapped[idx] is not None:
            st = max(prev_end, mapped[idx]['start'])
            en = max(st + 0.01, min(duration_s, mapped[idx]['end']))
            mapped[idx]['start'] = round(st, 4)
            mapped[idx]['end'] = round(en, 4)
            prev_end = en
            idx += 1
            continue
        end_idx = idx
        while end_idx < len(mapped) and mapped[end_idx] is None:
            end_idx += 1
        next_start = mapped[end_idx]['start'] if end_idx < len(mapped) else min(duration_s, float(asr_words[-1]['end']))
        count = end_idx - idx
        span = max(0.015 * count, next_start - prev_end)
        step = span / count
        for k in range(count):
            st = min(duration_s - 0.01 * (count - k), prev_end + k * step)
            en = min(duration_s, max(st + 0.01, st + step))
            mapped[idx + k] = {'text': script_words[idx + k], 'start': round(st, 4), 'end': round(en, 4), 'score': 0.5}
            prev_end = en
        idx = end_idx
    return [m for m in mapped if m is not None]


def transcribe_with_padding(
    samples_16k: np.ndarray,
    duration_s: float,
    *,
    lang: str = 'id',
    whisper_model: str = 'small',
    initial_prompt: str | None = None,
    local_files_only: bool = False,
) -> tuple[str, list[dict], list[dict]]:
    """Run faster-whisper with 0.5s silence padding on both sides so edge syllables are never clipped."""
    from faster_whisper import WhisperModel

    pad = int(round(PAD_SECONDS * SAMPLE_RATE))
    padded = np.concatenate([np.zeros(pad, dtype=np.float32), samples_16k, np.zeros(pad, dtype=np.float32)])
    model = WhisperModel(whisper_model, device='cpu', compute_type='int8', cpu_threads=4, local_files_only=local_files_only)
    lang_code = (lang or 'id').lower().split('-')[0]
    segments_iter, _ = model.transcribe(
        padded,
        language=lang_code,
        word_timestamps=True,
        beam_size=5,
        vad_filter=True,
        condition_on_previous_text=False,
        initial_prompt=initial_prompt,
    )
    asr_words: list[dict] = []
    asr_segments: list[dict] = []
    texts: list[str] = []
    for seg in segments_iter:
        s_start = max(0.0, min(duration_s, float(seg.start) - PAD_SECONDS))
        s_end = max(s_start + 0.01, min(duration_s, float(seg.end) - PAD_SECONDS))
        texts.append(seg.text.strip())
        seg_words = []
        for w in seg.words or []:
            tok = w.word.strip()
            if not tok:
                continue
            ws = max(0.0, min(duration_s - 0.01, float(w.start) - PAD_SECONDS))
            we = max(ws + 0.01, min(duration_s, float(w.end) - PAD_SECONDS))
            item = {'text': tok, 'start': round(ws, 4), 'end': round(we, 4), 'probability': round(float(w.probability), 4)}
            asr_words.append(item)
            seg_words.append(item)
        asr_segments.append({'text': seg.text.strip(), 'start': round(s_start, 4), 'end': round(s_end, 4), 'words': seg_words})
    return ' '.join(t for t in texts if t), asr_words, asr_segments


def run_wav2vec2_ctc_alignment(
    samples_16k: np.ndarray,
    duration_s: float,
    script_words: list[str],
    anchor_words: list[dict],
    *,
    lang: str = 'id',
    align_model: str | None = None,
    local_files_only: bool = False,
) -> tuple[list[dict], str]:
    """Run windowed Wav2Vec2 CTC phoneme/character forced alignment anchored by rough word windows."""
    import torch
    from transformers import AutoModelForCTC, AutoProcessor

    lang_code = (lang or 'id').lower().split('-')[0]
    model_name = align_model or DEFAULT_CTC_MODELS.get(lang_code, DEFAULT_CTC_MODELS['en'])
    processor = AutoProcessor.from_pretrained(model_name, local_files_only=local_files_only)
    model = AutoModelForCTC.from_pretrained(model_name, local_files_only=local_files_only)
    model.eval()
    vocab = processor.tokenizer.get_vocab()
    blank_id = getattr(model.config, 'pad_token_id', 0) or 0

    # Chunk into ~15-second windows along rough anchor boundaries so memory stays tiny on 90-120s episodes.
    chunks: list[tuple[int, int, float, float]] = []
    chunk_start_idx = 0
    while chunk_start_idx < len(script_words):
        chunk_end_idx = chunk_start_idx + 1
        t0 = max(0.0, anchor_words[chunk_start_idx]['start'] - 0.25)
        while chunk_end_idx < len(script_words):
            candidate_end = anchor_words[chunk_end_idx]['end']
            if candidate_end - t0 > 16.0 and chunk_end_idx - chunk_start_idx >= 6:
                break
            chunk_end_idx += 1
        t1 = min(duration_s, anchor_words[chunk_end_idx - 1]['end'] + 0.25)
        if chunk_end_idx == len(script_words):
            t1 = duration_s
        if chunk_start_idx == 0:
            t0 = 0.0
        chunks.append((chunk_start_idx, chunk_end_idx, t0, max(t0 + 0.1, t1)))
        chunk_start_idx = chunk_end_idx

    all_words: list[dict] = []
    prev_global_end = 0.0
    for i0, i1, t0, t1 in chunks:
        s0 = max(0, int(round(t0 * SAMPLE_RATE)))
        s1 = min(samples_16k.size, int(round(t1 * SAMPLE_RATE)))
        audio_slice = samples_16k[s0:s1]
        slice_dur = (s1 - s0) / SAMPLE_RATE
        inputs = processor(audio_slice, sampling_rate=SAMPLE_RATE, return_tensors='pt')
        with torch.no_grad():
            logits = model(inputs.input_values).logits[0]
            log_probs = torch.log_softmax(logits, dim=-1).cpu().numpy()
        chunk_aligned = ctc_align_words(
            log_probs,
            script_words[i0:i1],
            vocab,
            slice_dur,
            blank_id=blank_id,
            offset_s=s0 / SAMPLE_RATE,
        )
        for item in chunk_aligned:
            st = max(prev_global_end, min(duration_s - 0.01, item['start']))
            en = max(st + 0.01, min(duration_s, item['end']))
            prev_global_end = en
            all_words.append({**item, 'start': round(st, 4), 'end': round(en, 4)})
    return all_words, model_name


def align_audio_to_script(
    audio_path: Path,
    tagged_script: str,
    *,
    lang: str = 'id',
    whisper_model: str = 'small',
    align_model: str | None = None,
    threshold: float = 0.90,
    aliases: dict[str, str] | None = None,
    allow_whisper_fallback: bool = True,
    skip_ctc: bool = False,
    local_files_only: bool = False,
    enforce_asr_pass: bool = True,
) -> dict:
    """Full pipeline: decode -> padded faster-whisper ASR -> script & number verification -> Wav2Vec2 CTC alignment."""
    audio_path = Path(audio_path).resolve()
    samples, duration_s = decode_audio_16k(audio_path)
    target_words = spoken_script_words(tagged_script)
    prompt_hint = ' '.join(target_words[:40])

    observed_text, asr_words, asr_segments = transcribe_with_padding(
        samples,
        duration_s,
        lang=lang,
        whisper_model=whisper_model,
        initial_prompt=prompt_hint,
        local_files_only=local_files_only,
    )
    verification = verify_asr_against_script(
        tagged_script,
        observed_text,
        lang=lang,
        threshold=threshold,
        aliases=aliases,
    )
    if enforce_asr_pass and not verification['passed']:
        raise ValueError(
            f"ASR script verification failed (similarity={verification['similarity']}, "
            f"tags_spoken={len(verification['tags_spoken'])}, "
            f"number_mismatches={len(verification['number_mismatches'])}, "
            f"clipped={verification['clipped_edges']}): {json.dumps(verification['mismatches'][:5], ensure_ascii=False)}"
        )

    anchor_words = map_script_words_to_asr_words(target_words, asr_words, duration_s)
    alignment_method = 'faster_whisper_script_mapped'
    used_align_model = None

    if not skip_ctc:
        try:
            aligned_words, used_align_model = run_wav2vec2_ctc_alignment(
                samples,
                duration_s,
                target_words,
                anchor_words,
                lang=lang,
                align_model=align_model,
                local_files_only=local_files_only,
            )
            alignment_method = 'ctc_wav2vec2_forced'
        except Exception as exc:
            if not allow_whisper_fallback:
                raise
            aligned_words = anchor_words
            alignment_method = f'faster_whisper_script_mapped (ctc_unavailable: {type(exc).__name__})'
    else:
        aligned_words = anchor_words

    for idx, w in enumerate(aligned_words):
        w['id'] = f'w{idx:04d}'

    return {
        'audio_sha256': file_sha256(audio_path),
        'alignment_method': alignment_method,
        'asr_model': f'faster-whisper:{whisper_model}',
        'align_model': used_align_model,
        'language': (lang or 'id').lower().split('-')[0],
        'duration': round(duration_s, 4),
        'asr_verification': verification,
        'words': aligned_words,
        'segments': asr_segments,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audio', type=Path, required=True, help='Path to recorded MP3/WAV narration')
    parser.add_argument('--request', type=Path, help='Path to video/audio_request.json containing tagged narration and lang')
    parser.add_argument('--script-text', help='Inline script text if --request is not supplied')
    parser.add_argument('--lang', default=None, help='ISO language code (defaults to audio_request.json lang or id)')
    parser.add_argument('--whisper-model', default='small', help='faster-whisper model name or path (default: small)')
    parser.add_argument('--align-model', default=None, help='HuggingFace Wav2Vec2 CTC model ID or local path')
    parser.add_argument('--threshold', type=float, default=0.90, help='Minimum ASR token similarity (default: 0.90)')
    parser.add_argument('--aliases', type=Path, help='Optional JSON file mapping expected script words to phonetic ASR forms')
    parser.add_argument('--skip-ctc', action='store_true', help='Skip Wav2Vec2 CTC pass and map script onto faster-whisper words')
    parser.add_argument('--strict-ctc', action='store_true', help='Fail instead of falling back if Wav2Vec2 CTC model is unavailable')
    parser.add_argument('--local-files-only', action='store_true', help='Use only locally cached ASR/CTC models')
    parser.add_argument('--no-enforce-asr', action='store_true', help='Write output even when ASR verification fails (marks passed=false)')
    parser.add_argument('--output', type=Path, required=True, help='Destination timings JSON path')
    args = parser.parse_args()

    if bool(args.request) == bool(args.script_text):
        parser.error('Provide exactly one of --request or --script-text')

    if args.request:
        req = json.loads(args.request.read_text(encoding='utf-8-sig'))
        lines = req.get('lines') or []
        if len(lines) != 1 or not lines[0].get('text', '').strip():
            raise SystemExit('audio_request.json must contain one nonempty narration line')
        script_text = lines[0]['text']
        lang = args.lang or req.get('lang', 'id')
        inline_aliases = req.get('asr_aliases') if isinstance(req.get('asr_aliases'), dict) else None
    else:
        script_text = args.script_text
        lang = args.lang or 'id'
        inline_aliases = None

    aliases = json.loads(args.aliases.read_text(encoding='utf-8-sig')) if args.aliases else inline_aliases
    result = align_audio_to_script(
        args.audio,
        script_text,
        lang=lang,
        whisper_model=args.whisper_model,
        align_model=args.align_model,
        threshold=args.threshold,
        aliases=aliases,
        allow_whisper_fallback=not args.strict_ctc,
        skip_ctc=args.skip_ctc,
        local_files_only=args.local_files_only,
        enforce_asr_pass=not args.no_enforce_asr,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=args.output.parent, delete=False) as tmp:
        tmp_path = Path(tmp.name)
        tmp.write((json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    tmp_path.replace(args.output)
    print(json.dumps({
        'status': 'aligned',
        'output': str(args.output),
        'alignment_method': result['alignment_method'],
        'words': len(result['words']),
        'duration': result['duration'],
        'asr_passed': result['asr_verification']['passed'],
        'similarity': result['asr_verification']['similarity'],
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
