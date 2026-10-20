"""Assemble the measured continuous narration and approved animated layouts.

This does not synthesize speech, rewrite scene HTML, or export a video.
"""
from pathlib import Path
import html
import json
import re
import shutil
import subprocess

prod = Path(__file__).resolve().parent
video = prod / 'video'
timing = json.loads((video / 'timing.json').read_text(encoding='utf-8'))
meta = json.loads((video / 'audio_meta.json').read_text(encoding='utf-8'))
voice = meta['voices'][0]
original = video / '.media/audio/voice/narration-full.mp3'
normalized = original.with_name('narration-mix.wav')
if not normalized.exists():
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
        '-i', str(original), '-af', 'loudnorm=I=-18:TP=-2:LRA=7',
        '-ar', '48000', '-c:a', 'pcm_s16le', str(normalized)], check=True)

sfx_dir = video / '.media/audio/sfx'
sfx_dir.mkdir(parents=True, exist_ok=True)
click = sfx_dir / 'click-soft.mp3'
shutil.copy2(prod.parents[1] / '.agents/skills/media-use/audio/assets/sfx/click-soft.mp3', click)
probe = lambda p: float(subprocess.check_output(['ffprobe', '-v', 'error',
    '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(p)], text=True))
assert abs(probe(normalized) - timing['voice_duration']) < 0.03
sfx_duration = probe(click)

# Groups respect sentence punctuation, six-word maximum, and two short lines.
# Native word times remain the only timing source; no spoken words are added.
groups = []
for frame in timing['frames']:
    current = []
    for word in frame['words']:
        if current and (len(current) == 6 or len(' '.join(w['text'] for w in current + [word])) > 57):
            groups.append({'frame': frame['i'], 'words': current, 'offset': frame['start']})
            current = []
        current.append(word)
        if re.search(r'[.!?:,][”\"]?$', word['text']) and len(current) >= 3:
            groups.append({'frame': frame['i'], 'words': current, 'offset': frame['start']})
            current = []
    if current:
        groups.append({'frame': frame['i'], 'words': current, 'offset': frame['start']})

def balanced_lines(tokens):
    text = ' '.join(tokens)
    if len(text) <= 31:
        return [text]
    candidates = [(' '.join(tokens[:i]), ' '.join(tokens[i:])) for i in range(1, len(tokens))]
    return list(min(candidates, key=lambda p: max(len(p[0]),len(p[1])) + abs(len(p[0])-len(p[1])) * .12))

for i, group in enumerate(groups):
    group['id'] = f'caption-{i+1:03d}'
    group['start'] = round(group['offset'] + group['words'][0]['start'], 6)
    next_start = groups[i+1]['offset'] + groups[i+1]['words'][0]['start'] if i+1<len(groups) else timing['duration']
    group['end'] = round(min(next_start, group['offset'] + group['words'][-1]['end'] + .12), 6)
    group['lines'] = balanced_lines([w['text'] for w in group['words']])
norm = lambda s: re.sub(r'[^\w]', '', s).casefold()
assert [norm(w['text']) for g in groups for w in g['words']] == [norm(w['text']) for w in voice['words']]
assert all(len(g['lines']) <= 2 and max(map(len, g['lines'])) <= 34 for g in groups)
(video / 'caption_groups.json').write_text(json.dumps(groups, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

duration = timing['duration']
hosts = []
for frame in timing['frames']:
    hosts.append(f'<section id="scene-{frame["i"]:02d}" class="clip" data-composition-id="limerence-{frame["i"]:02d}" data-composition-src="{frame["src"]}" data-start="{frame["start"]:.6f}" data-duration="{frame["duration"]:.6f}" data-track-index="1" data-width="1080" data-height="1920"></section>')
captions = []
for g in groups:
    lines = ''.join(f'<span class="caption-line">{html.escape(line)}</span>' for line in g['lines'])
    captions.append(f'<div id="{g["id"]}" class="caption-group"><div class="caption-pill">{lines}</div></div>')
sets = '\n'.join(f'tl.set("#{g["id"]}",{{opacity:1}},{g["start"]:.6f});tl.set("#{g["id"]}",{{opacity:0}},{g["end"]:.6f});' for g in groups)
caption_html = f'''<template><style>
@font-face{{font-family:"DM Sans";src:url("assets/fonts/dm-sans.ttf") format("truetype");font-weight:100 900;font-style:normal;font-display:block}}
#root{{position:absolute;inset:0;width:100%;height:100%}}
.caption-group{{position:absolute;left:88px;top:1588px;width:848px;height:160px;display:flex;align-items:center;justify-content:center;opacity:0}}
.caption-pill{{box-sizing:border-box;max-width:848px;background:#302B28;color:#F3EDE3;padding:14px 24px 17px;border-radius:16px;text-align:center;font:500 44px/1.28 "DM Sans",sans-serif}}
.caption-line{{display:block;white-space:nowrap;max-width:800px}}
</style><div id="root" data-composition-id="limerence-captions" data-duration="{duration:.6f}" data-width="1080" data-height="1920" data-layout-allow-caption-zone>
{chr(10).join(captions)}</div><script>(()=>{{
const tl=gsap.timeline({{paused:true}});tl.set(".caption-group",{{opacity:0}},0);
{sets}
tl.to({{p:0}},{{p:1,duration:{duration:.6f},ease:"none"}},0);
window.__timelines["limerence-captions"]=tl;
}})();</script></template>'''
(video/'compositions/captions.html').write_text(caption_html,encoding='utf-8')

# Two understated ticks support the observed / interpreted comparison only.
sfx_cues = []
for frame_no, token in [(12, 'lakukan,'), (13, 'kejadian.')]:
    f = timing['frames'][frame_no-1]
    start = f['start'] + next(w['start'] for w in f['words'] if w['text'] == token)
    sfx_cues.append({'frame':frame_no,'file':'.media/audio/sfx/click-soft.mp3',
        'offset_s':round(start-f['start'],6),'start':round(start,6),
        'duration_s':sfx_duration,'source':'local','name':'soft observation tick','volume':.13})
audio = f'<audio id="narration" src=".media/audio/voice/narration-mix.wav" data-start="{timing["voice_offset"]}" data-duration="{timing["voice_duration"]}" data-track-index="2" data-volume="1"></audio>\n'
audio += '\n'.join(f'<audio id="sfx-{i+1}" src="{s["file"]}" data-start="{s["start"]}" data-duration="{s["duration_s"]}" data-track-index="4" data-volume="{s["volume"]}"></audio>' for i,s in enumerate(sfx_cues))
document = f'''<!doctype html><html lang="id" data-resolution="portrait"><head><meta charset="utf-8">
<meta name="viewport" content="width=1080, height=1920"><title>Limerence — Ruang di Antara</title>
<script src="assets/vendor/gsap.min.js"></script><style>
@font-face{{font-family:"DM Sans";src:url("assets/fonts/dm-sans-latin.woff2") format("woff2");font-weight:100 1000;font-style:normal;font-display:block}}
*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#F3EDE3}}
#root{{position:relative;width:100%;height:100%;overflow:hidden;background:#F3EDE3}}.clip{{position:absolute;inset:0}}
#captions{{z-index:30;pointer-events:none}}
.caption-group{{position:absolute;left:88px;top:1588px;width:848px;height:160px;display:flex;align-items:center;justify-content:center;opacity:0}}
.caption-pill{{max-width:848px;background:#302B28;color:#F3EDE3;padding:14px 24px 17px;border-radius:16px;text-align:center;font:500 44px/1.28 "DM Sans",sans-serif}}
.caption-line{{display:block;white-space:nowrap;max-width:800px}}
</style></head><body><div id="root" data-composition-id="limerence" data-start="0" data-duration="{duration:.6f}" data-width="1080" data-height="1920">
{chr(10).join(hosts)}
{audio}
<section id="captions" class="clip" data-composition-id="limerence-captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{duration:.6f}" data-track-index="3" data-width="1080" data-height="1920" data-layout-allow-caption-zone></section>
</div><script>
(() => {{
const tl=gsap.timeline({{paused:true}});
tl.to({{p:0}},{{p:1,duration:{duration:.6f},ease:"none"}},0);
window.__timelines["limerence"]=tl;
}})();
</script></body></html>'''
# The accepted local font file is discovered rather than downloaded again.
font_files = list((video/'assets/fonts').glob('*'))
dm = next(p.name for p in font_files if 'dm' in p.name.lower() and p.suffix in {'.ttf','.woff2'})
document = document.replace('dm-sans-latin.woff2', dm)
if dm.endswith('.ttf'):
    document = document.replace('format("woff2")', 'format("truetype")')
(video / 'index.html').write_text(document, encoding='utf-8')
meta.update(sfx=sfx_cues,bgm=None,bgm_pending=False,mix={
    'voice_path':'.media/audio/voice/narration-mix.wav',
    'processing':'FFmpeg loudnorm I=-18 LUFS, TP=-2 dBTP, LRA=7; 48kHz PCM; no time stretch',
    'duration_s':probe(normalized),'music':'none: a quiet spoken reflection with two selective observation ticks',
    'original_voice_preserved':'.media/audio/voice/narration-full.mp3'})
(video / 'audio_meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'duration':duration,'caption_groups':len(groups),'spoken_words':sum(len(g['words']) for g in groups),'sfx':len(sfx_cues),'voice_duration':probe(normalized),'font':dm}))


# Reapply the separate sound design plan after rebuilding the root.
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".agents/skills/shortform-production/scripts"))
from sound_design import apply_plan
if (video / "sound_design.json").exists():
    apply_plan(video)
