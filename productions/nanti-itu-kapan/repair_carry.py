"""Preserve sources, then make the owner actually lift and carry the bag."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification'
paths=[P/'build.py',P/'animate.py',V/'compositions/frames/f14.html']
(Q/'pre-carry-source.json').write_text(json.dumps({f.relative_to(P).as_posix():f.read_text(encoding='utf-8') for f in paths},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
f=P/'build.py';s=f.read_text(encoding='utf-8').replace("actor(520,1300,.75,c)+bag(625,1250,.65,c)","actor(640,1170,.75,c)+bag(745,1120,.65,c)+path('M684 1125Q715 1110 735 1060',c,7)")
s=s.replace('Last dish is set down, owner takes the bag and the outside bin becomes the destination.','Last dish is set down; owner grips the knot, lifts the bag and carries it toward the outside bin.').replace("'owner with tied bag','outside bin with approaching route'","'owner grips tied bag','owner and bag arrive beside outside bin'")
f.write_text(s,encoding='utf-8')
f=P/'animate.py';s=f.read_text(encoding='utf-8');needle="            if move=='draw':"
replacement='''            if n==14 and b==3:
                js+=f"tl.fromTo('{sel}',{{x:-120,y:130,opacity:0}},{{x:-120,y:130,opacity:1,duration:.20}},{at:.5f});\\n"
                js+=f"tl.to('{sel}',{{x:0,y:0,duration:{min(.8,dur*.18):.5f},ease:'power2.inOut'}},{dur*.73:.5f});\\n"
            elif move=='draw':'''
assert needle in s;s=s.replace(needle,replacement);f.write_text(s,encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as f:f.write('''
## Fresh visual review and bounded repair

Fresh agent, given only storyboard and three phase sheets, reported no P0 and two proposed P1s: F14 needed actual carry action; F16 title allegedly clipped. Primary inspection of full phone/seam sheets shows the complete F16 title already wrapping within x88–936; no title clipping observed, so that proposed issue is not accepted without evidence. F14 repaired: owner visibly grips bag knot, lifts and moves with bag toward bin, holds arrival. Build/animation/prior F14 sources preserved in verification/pre-carry-source.json. Script, recording, palettes and fixed chrome unchanged. Reverify changed shot, motion hashes, complete check and relevant preview before rendering.
''')
print('Owner and bag now lift/carry together; final static pose matches arrival.')
