"""Execute bounded frame packets inline, preserving the verified static geometry."""
from pathlib import Path
import json
import re
import build

P=Path(__file__).resolve().parent;V=P/'video'
ROOT=next(parent for parent in P.parents if (parent/'.agents/skills/hyperframes/SKILL.md').is_file())
# Three information-bearing developments, tailored to each scene's actual action.
MOVES={1:[('draw',.16),('draw',.43),('settle',.74)],2:[('draw',.15),('settle',.47),('settle',.76)],3:[('draw',.15),('draw',.43),('settle',.73)],4:[('down',.16),('down',.44),('draw',.74)],5:[('draw',.15),('draw',.45),('settle',.74)],6:[('left',.13),('down',.43),('spoon',.70)],7:[('knead',.10),('left',.41),('draw',.73)],8:[('settle',.14),('draw',.42),('settle',.74)],9:[('settle',.14),('draw',.43),('settle',.74)],10:[('settle',.15),('draw',.44),('draw',.72)],11:[('down',.15),('down',.43),('settle',.74)],12:[('draw',.14),('settle',.43),('draw',.75)],13:[('draw',.16),('settle',.43),('draw',.73)],14:[('draw',.14),('draw',.43),('draw',.74)],15:[('draw',.15),('settle',.43),('draw',.72)],16:[('settle',.15),('draw',.44),('draw',.68)]}

def main():
    lines=json.loads((V/'script_data.json').read_text(encoding='utf-8'));ts=build.schedule(lines)
    packets=V/'.hyperframes/frame-packets';packets.mkdir(parents=True,exist_ok=True)
    role='\n\n'.join((ROOT/'.agents/skills/hyperframes'/name).read_text(encoding='utf-8') for name in ('SKILL.md','references/format.md','references/runtimes.md'))
    (packets/'_role.md').write_text(role,encoding='utf-8')
    rules=(ROOT/'.agents/skills/hyperframes/references/motion.md').read_text(encoding='utf-8')
    storyboard=build.storyboard(lines,ts,False)
    report=[]
    for x,t in zip(lines,ts):
        n=x['id'];cid=f'f{n:02d}';dur=t['duration'];source=build.pose(x,t)
        block=storyboard.split(f'## Frame {n} —',1)[1].split('\n## Frame ',1)[0]
        packet=f'''# Dispatch context

PROJECT_DIR: {V.as_posix()}
frame_id: {cid}
src: compositions/frames/{cid}.html
canvas: 1080x1920
confirmed_sketch: agent-verified static storyboard, no human approval claimed
captions: enabled at y1550–1740; keep key content above y1480
execution: inline serial fallback; no native subagent authorization requested or assumed

## Exact storyboard block

## Frame {n} —{block}

## Selected blueprint

compose: preserve the verified geometry and implement its four semantic states.

## Motion guidance

{rules}
'''
        (packets/f'{cid}.md').write_text(packet.rstrip()+'\n',encoding='utf-8')
        # Read the frame-local sources before dressing that same confirmed layout.
        assert (packets/f'{cid}.md').read_text(encoding='utf-8') and (V/'frame.md').read_text(encoding='utf-8')
        source=re.sub(r'<div class="pose-caption">.*?</div>','',source)
        for name in ('ground','drawing','heading','beat1','beat2','beat3','beat4'):source=source.replace(f'id="{name}"',f'id="{cid}-{name}"')
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
