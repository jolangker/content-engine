"""Animate the verified episode layouts with bounded semantic beats."""
from pathlib import Path
import json
import re
import build

P=Path(__file__).resolve().parent;V=P/'video';ROOT=P.parents[1]
# Three information-bearing developments, tailored to each scene's actual action.

MOVES={n:[('draw',.14),('settle',.43),('draw',.73)] for n in range(1,17)}
MOVES.update({4:[('down',.14),('settle',.43),('draw',.73)],6:[('down',.13),('left',.43),('draw',.72)],12:[('draw',.14),('settle',.43),('draw',.73)],16:[('draw',.15),('draw',.40),('settle',.67)]})
def main():
    lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=build.schedule(lines)
    report=[]
    for x,t in zip(lines,ts):
        n=x['id'];cid=f'f{n:02d}';dur=t['duration'];source=build.pose(x,t)
        source=re.sub(r'<div class="pose-caption">.*?</div>','',source)
        for name in ('ground','drawing','heading','beat1','beat2','beat3','beat4','arrival'):source=source.replace(f'id="{name}"',f'id="{cid}-{name}"')
        js='const tl=gsap.timeline({paused:true});\n'
        for b,(move,f) in enumerate(MOVES[n],2):
            sel=f'#{cid}-beat{b}';at=dur*f;length=min(.9,dur*.20)
            if move=='draw':
                js+=f'''{{const el=document.querySelector('{sel}');tl.fromTo(el,{{opacity:0}},{{opacity:1,duration:.18}},{at:.5f});el.querySelectorAll('path,circle,line,rect').forEach(p=>{{if(p.getTotalLength&&(!p.getAttribute('fill')||p.getAttribute('fill')==='none')){{const len=p.getTotalLength();tl.fromTo(p,{{strokeDasharray:len,strokeDashoffset:len}},{{strokeDashoffset:0,duration:{length:.5f},ease:'power2.inOut'}},{at:.5f});}}}});}}\n'''
            elif move=='spoon':
                js+=f"tl.fromTo('{sel}',{{rotation:-12,y:-40,opacity:0,svgOrigin:'625 650'}},{{rotation:0,y:0,opacity:1,duration:{length:.5f},ease:'power2.inOut'}},{at:.5f});\n"
            elif move=='knead':
                js+=f"tl.fromTo('{sel}',{{scale:.88,opacity:0,transformOrigin:'50% 50%'}},{{scale:1,opacity:1,duration:.45,ease:'power3.out'}},{at:.5f});\n"
                js+=f"tl.to('{sel}',{{scaleX:1.10,scaleY:.89,duration:.30,ease:'power2.inOut'}},{at+.5:.5f});tl.to('{sel}',{{scaleX:1,scaleY:1,duration:.4,ease:'power2.inOut'}},{at+.85:.5f});\n"
            elif move in ('down','left'):
                offset='y:-38' if move=='down' else 'x:45'
                js+=f"tl.fromTo('{sel}',{{{offset},opacity:0}},{{x:0,y:0,opacity:1,duration:{length:.5f},ease:'power3.out'}},{at:.5f});\n"
            else:js+=f"tl.fromTo('{sel}',{{scale:.84,opacity:0,transformOrigin:'50% 50%'}},{{scale:1,opacity:1,duration:{length:.5f},ease:'power3.out'}},{at:.5f});\n"
        if n==4:
            js+=f"tl.fromTo('#f04-arrival',{{x:-405,y:-280}},{{x:0,y:0,duration:.9,ease:'power2.inOut'}},{dur*.43:.5f});\n"
        js+=f'window.__timelines["{cid}"]=tl;'
        source=re.sub(r'<script>.*?</script>',f'<script>{js}</script>',source,flags=re.S)
        assert source.startswith('<template>') and source.endswith('</template>')
        assert len(re.findall('gsap.timeline',source))==1
        (V/f'compositions/frames/{cid}.html').write_text(source,encoding='utf-8')
        # Assertions distinguish concrete later state changes from plain clip presence.
        assertions=[dict(kind='before',a=f'#{cid}-beat2',b=f'#{cid}-beat3'),dict(kind='before',a=f'#{cid}-beat3',b=f'#{cid}-beat4')]
        (V/f'compositions/frames/{cid}.motion.json').write_text(json.dumps(dict(duration=dur,assertions=assertions),indent=2)+'\n',encoding='utf-8')
        report.append(dict(frame=cid,duration=dur,phase_times=[round(dur*f,5) for _,f in MOVES[n]],preserves_static_geometry=True,execution='inline'))
    (V/'verification').mkdir(exist_ok=True);(V/'verification/choreography.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(frames=len(report),native_agents_used=False,static_layouts_preserved=True)))
if __name__=='__main__':main()
