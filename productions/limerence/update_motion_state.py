"""Record completed frame work and targeted seek assertions without rewriting HTML."""
from pathlib import Path
import json
import re
from html.parser import HTMLParser

prod=Path(__file__).resolve().parent
video=prod/'video'
timing=json.loads((video/'timing.json').read_text(encoding='utf-8'))
class HeadlineParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'headline' in d.get('class',''):
            self.ids.append('#'+d['id'] if d.get('id') else '.'+next(c for c in d['class'].split() if 'headline' in c))

completed=[]
root_assertions=[]
for f in timing['frames']:
    path=video/f['src']
    text=path.read_text(encoding='utf-8')
    if not text.startswith('<template>'):
        continue
    assert f'limerence-{f["i"]:02d}' in text
    assert 'paused: true' in text or 'paused:true' in text
    parsed=HeadlineParser();parsed.feed(text)
    assert parsed.ids, path
    # Assert animated leaves when the approved heading container itself is static.
    if f['i']==2: parsed.ids[0]='#limerence-02-coffee-line-1'
    if f['i']==10: parsed.ids[0]='#limerence-10-title'
    if f['i']==14: parsed.ids[0]='#limerence-14-question-1'
    if f['i']==1: parsed.ids[1]='#limerence-01-imagined-headline span:nth-child(1)'
    if f['i']==2: parsed.ids[1]='#limerence-02-thought-line-1'
    assertions=[{'kind':'appearsBy','selector':parsed.ids[0],'bySec':.5},
        {'kind':'staysInFrame','selector':parsed.ids[0]}]
    # This is a sequencing assertion rather than artificial perpetual motion.
    if len(parsed.ids)>1 and f['i'] in {1,2,12}:
        assertions.append({'kind':'before','a':parsed.ids[0],'b':parsed.ids[1]})
    path.with_suffix('.motion.json').write_text(json.dumps({
        'duration':f['duration'],'assertions':assertions},indent=2)+'\n',encoding='utf-8')
    hero = '#limerence-14-question-1' if f['i']==14 else parsed.ids[0]
    root_assertions.extend([
        {'kind':'appearsBy','selector':hero,'bySec':round(f['start']+.5,6)},
        {'kind':'staysInFrame','selector':hero}])
    if len(parsed.ids)>1 and f['i'] in {1,2,12}:
        root_assertions.append({'kind':'before','a':parsed.ids[0],'b':parsed.ids[1]})
    completed.append(f['i'])

s=video/'STORYBOARD.md'
blocks=re.split(r'(?m)(?=^## Frame \d+:)',s.read_text(encoding='utf-8'))
for n in completed:
    blocks[n]=re.sub(r'(?m)^- status: .*','- status: animated',blocks[n])
s.write_text(''.join(blocks),encoding='utf-8')
(video/'index.motion.json').write_text(json.dumps({'duration':timing['duration'],
    'assertions':root_assertions},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'animated_frames':completed}))
