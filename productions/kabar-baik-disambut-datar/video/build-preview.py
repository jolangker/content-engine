"""Animate the accepted layouts, with a single continuous, aligned narration.

Reads the frozen storyboard instead of rebuilding or redesigning its artwork.
No synthesis, network requests, or paid services are called by this script.
"""
from pathlib import Path
import copy
import html
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent
APPROVED = ROOT / 'boards/approved-storyboard-v1'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
TEMPO = .85
TAIL = 1.5

def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')

def probe(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
        'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(path)], text=True))

raw = ROOT / 'assets/voice/narration-v1/narration.mp3'
voice = ROOT / 'assets/voice/narration-v1/narration-preview.wav'
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(raw),
    '-af', f'atempo={TEMPO}', '-ar', '44100', '-c:a', 'pcm_s16le', str(voice)], check=True)
voice_duration = probe(voice)
duration = round(voice_duration + TAIL, 3)
raw_words = json.loads((raw.parent / 'words.json').read_text(encoding='utf8'))
words = [{**w, 'start': round(w['start']/TEMPO, 4), 'end': round(w['end']/TEMPO, 4)} for w in raw_words]
frames = json.loads((APPROVED / 'boards/frames.json').read_text(encoding='utf8'))
assert ' '.join(w['text'] for w in words) == ' '.join(' '.join(f['voiceover'].split()) for f in frames)

cursor = 0
for f in frames:
    count = len(f['voiceover'].split())
    f['words'] = words[cursor:cursor+count]
    f['word_ids'] = [w['id'] for w in f['words']]
    f['start'] = 0 if cursor == 0 else round((words[cursor-1]['end'] + words[cursor]['start'])/2, 4)
    f['status'] = 'animated'
    f['layout_review'] = 'approved'
    cursor += count
for i, f in enumerate(frames):
    f['end'] = frames[i+1]['start'] if i+1 < len(frames) else duration
    f['duration'] = round(f['end']-f['start'], 4)
    f['poster'] = round(f['start']+f['duration']/2, 4)

def wrap(parent, nodes, ident):
    nodes = list(nodes)
    insert = min(list(parent).index(n) for n in nodes)
    group = ET.Element(f'{{{NS}}}g', {'id': ident, 'data-motion-part': 'true'})
    for n in nodes:
        parent.remove(n)
        group.append(n)
    parent.insert(insert, group)
    return '#' + ident

def inner(parent, ident):
    return wrap(parent, list(parent), ident)

motion_notes = []
for f in frames:
    number = f['number']
    prefix = f['id']
    source = (APPROVED / f['src']).read_text(encoding='utf8')
    svg_match = re.search(r'<svg[\s\S]+?</svg>', source)
    svg = ET.fromstring(svg_match.group())
    original = list(svg)
    groups = [n for n in original if n.tag == f'{{{NS}}}g']
    commands = []
    phases = []
    d = f['duration']

    def cue(text, fallback=0):
        key = text.casefold().strip('“”.,:!?')
        for w in f['words']:
            if w['text'].casefold().strip('“”.,:!?') == key:
                return max(0, round(w['start']-f['start'], 4))
        return fallback

    def command(method, selector, values, at):
        commands.append(f'tl.{method}({json.dumps(selector)}, {json.dumps(values)}, {round(at,4)});')

    def setv(selector, values, at=0):
        command('set', selector, values, at)

    def tween(selector, values, at, length, ease='sine.inOut'):
        length = min(length, d-at-.03)
        if length > .01:
            command('to', selector, {**values, 'duration': round(length,4), 'ease': ease}, max(0,at))

    def joint(parent, indices, name, origin):
        children = list(parent)
        sel = wrap(parent, [children[j] for j in indices], prefix+'-'+name)
        setv(sel, {'svgOrigin': origin, 'smoothOrigin': False})
        return sel

    def rig(g, name, standing=False, phone=False, busy=False, down=False):
        # Capture references before wrapping so the original z order and poses survive.
        nodes = list(g)
        head = wrap(g, nodes[5:7] if standing else nodes[6:8], prefix+'-'+name+'-head')
        setv(head, {'svgOrigin': '0 65', 'smoothOrigin': False})
        right_indices = [7,8] if standing else [8,9]
        left_indices = [9,10,11] if standing else [10,11]
        if phone:
            right_indices = [8,9,10]
            left_indices = [11,12]
        if busy:
            right_indices += [12]
        right = wrap(g, [nodes[i] for i in right_indices], prefix+'-'+name+'-right')
        left = wrap(g, [nodes[i] for i in left_indices], prefix+'-'+name+'-left')
        setv(right, {'svgOrigin': '44 127', 'smoothOrigin': False})
        setv(left, {'svgOrigin': '-47 129', 'smoothOrigin': False})
        return {'head':head, 'right':right, 'left':left}

    def nod(r, at, amount=4, length=1.1):
        tween(r['head'], {'rotation':amount}, at, length*.4)
        tween(r['head'], {'rotation':0}, at+length*.4, length*.6)

    def gesture(r, at, amount=-7, length=1.5):
        tween(r['right'], {'rotation':amount}, at, length*.4)
        tween(r['right'], {'rotation':0}, at+length*.4, length*.6)

    if number == 1:
        b = rig(groups[0], 'B', phone=True)
        a = rig(groups[1], 'A', standing=True)
        arrive = inner(groups[1], prefix+'-arrival')
        setv(arrive, {'x':-92})
        # Deliberate slow / fast / slow arrival, then the hand opens for the story.
        tween(arrive, {'x':-82.8}, 0, d*.20, 'sine.in')
        tween(arrive, {'x':-23}, d*.20, d*.18, 'none')
        tween(arrive, {'x':0}, d*.38, d*.57, 'sine.out')
        gesture(a, d*.48, -5, d*.45)
        phases = ['A masuk dari kiri.', 'A membuka telapak tangan saat membawa kabar baik.']
    elif number in (2,5,6):
        a = rig(groups[0], 'A', standing=True, down=number==6)
        if number == 6:
            # The down pose's paper belongs to the lowered left hand.
            setv(a['left'], {'rotation':-15})
            tween(a['left'], {'rotation':0}, cue('Ya'), 1.4)
            tween(a['head'], {'rotation':7}, cue('Nggak'), 1.3)
            phases = ['Kartu masih sedikit terangkat.', 'Tangan turun; kepala tertunduk, lalu ditahan.']
        else:
            gesture(a, cue('presentasi' if number==2 else 'maju.'), -8, min(2.0,d*.65))
            nod(a, cue('dipuji' if number==2 else 'penting'), -4, min(1.3,d*.3))
            if number == 5:
                tween(a['left'], {'rotation':-4}, d*.25, 1.2)
                tween(a['left'], {'rotation':0}, d*.65, 1.0)
            phases = ['Gerak tangan mengikuti cerita presentasi.', 'Kepala terangkat pada arti pujian.']
    elif number == 3:
        b = rig(groups[0], 'B', phone=True)
        tween(b['left'], {'rotation':-3}, .2, .65)
        tween(b['left'], {'rotation':0}, 1.15, .65)
        nod(b, cue('Oh'), 3, 1.0)
        phases = ['Tangan bergeser singkat di layar.', 'Jawaban pendek dengan kepala tetap mengarah ke HP.']
    elif number in (4,12):
        a = rig(groups[0], 'A' if number==4 else 'B', busy=True)
        # Two finite writing gestures rather than a perpetual loop.
        for at in ([cue('latihan'), cue('tangan')] if number==4 else [.4, d*.42]):
            gesture(a, at, -4, 1.1)
        nod(a, cue('lancar' if number==4 else 'Konteksnya'), -4, 1.5)
        phases = ['Tangan dan pena mengerjakan catatan.', 'Kepala bergerak mengikuti usaha / konteks kerja.']
    elif number == 7:
        a = wrap(svg, [original[2], original[4]], prefix+'-A-hand')
        b = wrap(svg, [original[3], original[5]], prefix+'-B-hand')
        card = inner(original[6], prefix+'-card')
        setv(a, {'x':-42}); setv(b, {'x':44}); setv(card, {'rotation':-4, 'svgOrigin':'0 0'})
        tween(a, {'x':0}, cue('berbagi'), 1.5)
        tween(b, {'x':0}, cue('orang'), 1.4)
        tween(card, {'rotation':0}, cue('dikenal'), 1.2)
        phases = ['Dua tangan mendekat ke ruang yang dibagi.', 'Kartu catatan menetap ketika konsep dikenalkan.']
    elif number in (8,9,10,13,14):
        if number in (8,14):
            a = rig(groups[0], 'A'); b = rig(groups[1], 'B')
        elif number == 9:
            a = rig(groups[0], 'A', standing=True); b = rig(groups[1], 'B')
        else:
            bgroup = next(g for g in groups if len(g) == 12)
            b = rig(bgroup, 'B')
        if number == 8:
            gesture(b, cue('antusias'), -6, 1.5)
            nod(b, cue('terlibat'), -4, 1.2)
            gesture(a, cue('kepuasan'), -5, 1.7)
            nod(b, cue('kedekatan'), 4, 1.1)
            phases = ['Gestur B membuka percakapan.', 'A ikut berbicara; B memberi anggukan mendengar.']
        elif number == 9:
            setv(b['head'], {'rotation':7}); setv(b['right'], {'rotation':12})
            tween(b['head'], {'rotation':0}, .1, d*.7)
            tween(b['right'], {'rotation':0}, d*.25, d*.65)
            phases = ['B menoleh kepada A.', 'Telapak tangan terbuka untuk mendengar.']
        elif number == 10:
            nod(b, cue('keren'), -5, 1.0)
            gesture(b, cue('Kemarin'), -8, 1.5)
            gesture(b, cue('Ceritain'), -11, 2.0)
            phases = ['Antusias pada kabar baik.', 'Tangan mengundang cerita saat “Ceritain”.']
        elif number == 13:
            gesture(b, cue('seneng'), -6, 1.5)
            gesture(b, cue('beresin'), 5, 1.3)
            nod(b, cue('ceritanya'), -4, 1.3)
            clock = original[9]
            hands = list(clock)[6]
            old = copy.deepcopy(hands)
            clock.remove(hands)
            minute = copy.deepcopy(old); minute.set('d','M0 0 L0 -44')
            hour = copy.deepcopy(old); hour.set('d','M0 0 L42 24')
            clock.insert(6, hour); clock.insert(7, minute)
            m = wrap(clock, [minute], prefix+'-minute'); h = wrap(clock, [hour], prefix+'-hour')
            setv(m, {'svgOrigin':'0 0'}); setv(h, {'svgOrigin':'0 0'})
            tween(m, {'rotation':60}, cue('sepuluh'), 2.0)
            tween(h, {'rotation':5}, cue('sepuluh'), 2.0)
            phases = ['B mengakui kabar baik.', 'Jarum jam menandai sepuluh menit.', 'B berjanji kembali mendengar.']
        else:
            gesture(b, cue('kembali'), -5, 1.4)
            gesture(a, cue('ingat'), -7, 1.8)
            nod(b, cue('tanyain'), 5, 1.4)
            tween(b['right'], {'rotation':-3}, cue('setelah'), 1.2)
            phases = ['B kembali hadir.', 'A bercerita; B mendengar.', 'Pose percakapan menetap pada akhir pertanyaan.']
    elif number == 11:
        phone = inner(original[3], prefix+'-phone')
        hand = wrap(svg, [original[4],original[5]], prefix+'-B-hand')
        a = wrap(svg, [original[6],original[7]], prefix+'-A-hand')
        setv(phone, {'y':-42}); setv(hand, {'y':-92})
        tween(phone, {'y':0}, cue('menaruh'), 1.1)
        tween(hand, {'y':0}, cue('menaruh'), 1.1)
        tween(hand, {'x':20,'y':-165}, cue('Lo'), 1.5)
        tween(a, {'rotation':-5,'svgOrigin':'180 650'}, cue('lanjut'), 1.2)
        tween(a, {'rotation':0}, cue('detail'), 1.4)
        phases = ['HP dan tangan turun ke meja.', 'Tangan B melepaskan HP.', 'Gestur A melanjutkan cerita.']

    # Preserve all three accepted emphasis layouts; reveal each only at its spoken cue.
    if number in (7,8,10):
        em = f'#{prefix}-root .emphasis'
        at = cue({7:'berbagi',8:'aktif-konstruktif',10:'Ceritain'}[number])
        setv(em, {'opacity':0})
        tween(em, {'opacity':1}, at, .45, 'sine.out')
    commands.append(f'tl.to({{}}, {{duration:{d}}}, 0);')
    script = '<script>{const tl=gsap.timeline({paused:true});\n'+'\n'.join(commands)+f'\nwindow.__timelines["{prefix}"]=tl;}}'+'</script>'
    source = source[:svg_match.start()] + ET.tostring(svg, encoding='unicode') + source[svg_match.end():]
    source = re.sub(r'data-duration="[0-9.]+"', f'data-duration="{d}"', source, count=1)
    source = re.sub(r'<script>[\s\S]+?</script>', script, source)
    (ROOT/f['src']).write_text(source, encoding='utf8')
    sidecar = {'duration':d, 'assertions':[
        {'kind':'appearsBy','selector':f'#{prefix}-root','bySec':.1},
        {'kind':'staysInFrame','selector':f'#{prefix}-root'},
        {'kind':'keepsMoving','withinSelector':f'#{prefix}-root','maxStaticSec':4.0}
    ]}
    dump((ROOT/f['src']).with_suffix('.motion.json'), sidecar)
    f['motion_phases'] = phases
    motion_notes.append(f"{number:02d}. {f['start']:.2f}–{f['end']:.2f}s — " + ' → '.join(phases))

# Caption grouping never crosses a cut or a sentence boundary. Measure in the local font.
font = ImageFont.truetype(str(ROOT/'assets/fonts/dm-sans.ttf'),48)
def width(text):
    return font.getlength(text)

def lines_for(ws):
    texts = [w['text'] for w in ws]
    whole = ' '.join(texts)
    if width(whole) <= 750:
        return [texts]
    choices=[]
    for k in range(1,len(texts)):
        l,r=' '.join(texts[:k]),' '.join(texts[k:])
        if max(width(l),width(r)) <= 750:
            choices.append((abs(width(l)-width(r)),k))
    if not choices:
        return None
    k=min(choices)[1]
    return [texts[:k],texts[k:]]

captions=[]
phrase_plan=json.loads((ROOT/'caption-phrases.json').read_text(encoding='utf8'))
assert len(phrase_plan)==len(frames)
for f,phrases in zip(frames,phrase_plan):
    assert ' '.join(phrases)==f['voiceover']
    offset=0
    for phrase in phrases:
        size=len(phrase.split())
        bucket=f['words'][offset:offset+size]
        assert ' '.join(w['text'] for w in bucket)==phrase
        assert lines_for(bucket) is not None
        captions.append({'words':bucket,'frame':f['id']})
        offset+=size
    assert offset==len(f['words'])

caption_dom=[]
caption_commands=[]
for i,c in enumerate(captions):
    c['id']=f'caption-{i:02d}'
    c['start']=c['words'][0]['start']
    next_start=captions[i+1]['words'][0]['start'] if i+1<len(captions) else duration
    frame=next(f for f in frames if f['id']==c['frame'])
    c['end']=round(min(frame['end'],next_start-.015,c['words'][-1]['end']+.22),4)
    if i+1==len(captions):c['end']=duration
    c['lines']=[' '.join(t) for t in lines_for(c['words'])]
    spans=''.join('<span class="caption-line">'+html.escape(t)+'</span>' for t in c['lines'])
    caption_dom.append(f'<div id="{c["id"]}" class="caption" data-word-ids="{" ".join(w["id"] for w in c["words"])}">{spans}</div>')
    caption_commands.append(f'tl.set("#{c["id"]}",{{opacity:1,visibility:"visible"}},{c["start"]});')
    if i+1<len(captions):
        caption_commands.append(f'tl.set("#{c["id"]}",{{opacity:0,visibility:"hidden"}},{c["end"]});')

cap_style="""@font-face{font-family:'DM Sans';src:url('../assets/fonts/dm-sans.ttf') format('truetype');font-weight:100 900;font-display:block}
#captions-root{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
#captions-root .caption{position:absolute;left:112px;right:160px;top:1510px;height:150px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'DM Sans';font-size:48px;font-weight:500;line-height:1.22;color:#302B28;text-align:center;opacity:0;visibility:hidden}
#captions-root .caption-line{display:block;white-space:nowrap;max-width:100%;background:#F3EDE3;padding:4px 16px;border-radius:5px}
"""
caption_html = '<template><style>'+cap_style+'</style>'+f'<div id="captions-root" data-composition-id="captions" data-width="1080" data-height="1920" data-duration="{duration}" data-layout-allow-caption-zone>'+''.join(caption_dom)+'</div><script>{const tl=gsap.timeline({paused:true});\n'+'\n'.join(caption_commands)+f'\ntl.to({{}},{{duration:{duration}}},0);window.__timelines["captions"]=tl;}}'+'</script></template>'
(ROOT/'compositions/captions.html').write_text(caption_html,encoding='utf8')
dump(ROOT/'assets/voice/narration-v1/words-preview.json',words)
dump(ROOT/'captions.json',captions)

main=(APPROVED/'index.html').read_text(encoding='utf8')
for f in frames:
    pattern=rf'<div id="host-{f["id"]}"[^>]+></div>'
    host=f'<div id="host-{f["id"]}" class="clip" data-composition-id="{f["id"]}" data-composition-src="{f["src"]}" data-start="{f["start"]}" data-duration="{f["duration"]}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>'
    main=re.sub(pattern,host,main)
main=main.replace('data-duration="90"',f'data-duration="{duration}"')
audio=f'<audio id="narration" src="assets/voice/narration-v1/narration-preview.wav" data-start="0" data-duration="{round(voice_duration,6)}" data-track-index="3" data-volume="1" preload="auto"></audio>'
main=main.replace('</div><script>window.__timelines["main"]',audio+'</div><script>window.__timelines["main"]')
main=main.replace('— storyboard v1','— preview v1')
(ROOT/'index.html').write_text(main,encoding='utf8')
meta=json.loads((ROOT/'audio_meta.json').read_text(encoding='utf8'))
meta['voices']=[{'id':'narration','path':'assets/voice/narration-v1/narration-preview.wav','duration_s':voice_duration,'words':words}]
meta['total_duration_s']=voice_duration
meta['source_audio']={'path':'assets/voice/narration-v1/narration.mp3','duration_s':probe(raw),'provider':'elevenlabs','tempo_filter':f'atempo={TEMPO}','alignment':'native ElevenLabs normalized_alignment, scaled by 1/tempo; WSOLA can introduce small local timing differences'}
meta['composition_duration_s']=duration
dump(ROOT/'audio_meta.json',meta)
dump(ROOT/'boards/preview-frames.json',frames)
dump(ROOT/'index.motion.json',{'duration':duration,'assertions':[
    {'kind':'keepsMoving','withinSelector':'#root','maxStaticSec':4},
    *[{'kind':'appearsBy','selector':f"#host-{f['id']}",'bySec':round(f['start']+.65,4)} for f in frames],
    *[{'kind':'staysInFrame','selector':f"#host-{f['id']}"} for f in frames]
]})
(ROOT/'MOTION.md').write_text('# Motion v1\n\nApproved poses and palette preserved. Cuts follow the continuous voice, with source-word cues.\n\n'+'\n'.join(motion_notes)+'\n',encoding='utf8')
print(json.dumps({'voice_duration':voice_duration,'composition_duration':duration,'words':len(words),'caption_groups':len(captions),'frames':len(frames),'cuts':[[f['number'],f['start'],f['end']] for f in frames]}))
