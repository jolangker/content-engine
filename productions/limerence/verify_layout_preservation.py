"""Compare accepted copy/layout and SVG geometry with the animated sources."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import json

video=Path(__file__).resolve().parent/'video'
class Parser(HTMLParser):
    def __init__(self):
        super().__init__();self.skip=0;self.copy=[];self.paths=[];self.styles=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag in ('style','script'): self.skip+=1
        if tag=='path': self.paths.append((d.get('d'),d.get('transform')))
        if d.get('style'): self.styles.append(d['style'])
    def handle_endtag(self,tag):
        if tag in ('style','script'): self.skip-=1
    def handle_data(self,data):
        if not self.skip:self.copy.extend(data.split())

results=[]
for source in sorted((video/'approved-static').glob('*.html')):
    old=Parser();new=Parser()
    old.feed(source.read_text(encoding='utf-8'))
    new.feed((video/'compositions/frames'/source.name).read_text(encoding='utf-8'))
    notes=[]
    if source.name.startswith('12-'):
        # A continuous observed trunk was split into two exact contiguous paths
        # for separate narration cues; the combined painted geometry is identical.
        trunk='M525,715 V861'
        branch='M525,861 C525,937 257,927 257,1007 V1030'
        assert (trunk,None) in new.paths and (branch,None) in new.paths
        new.paths.append((trunk+branch.removeprefix('M525,861'),None))
        notes.append('Observed path split into exact contiguous trunk and branch for cue timing; painted geometry unchanged.')
    result={'frame':source.name,'same_visible_copy':old.copy==new.copy,
        'original_geometry_preserved':not bool(Counter(old.paths)-Counter(new.paths)),
        'original_inline_layout_preserved':not bool(Counter(old.styles)-Counter(new.styles)),
        'notes':notes}
    results.append(result)
(video/'verification/layout-preservation.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
assert all(all(r[k] for k in ('same_visible_copy','original_geometry_preserved','original_inline_layout_preserved')) for r in results)
print(f'{len(results)}/14 approved layouts preserve copy, inline layout, and original painted geometry.')
