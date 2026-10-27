"""Check repeated forward/reverse seeks in the live assembled preview."""
from pathlib import Path
import hashlib,json
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification'
scenes=json.loads((V/'timing.json').read_text(encoding='utf-8'))['scenes']
with sync_playwright() as p:
    b=p.chromium.launch(headless=True);page=b.new_page(viewport=dict(width=1600,height=1000));page.goto('http://127.0.0.1:3002/#project/video');page.wait_for_timeout(2200);f=page.frames[1]
    f.wait_for_function('window.__player && window.__renderReady');f.evaluate('window.__player.pause()')
    def state(t):
        f.evaluate('(t)=>window.__player.seek(t)',t);page.wait_for_timeout(100)
        scene=next(s for s in scenes if s['start']<=t<s['end'])
        selector=f'svg g[id^="f{scene["id"]:02d}-"]'
        f.wait_for_selector(selector,state='attached')
        return f.evaluate('''(selector)=>Object.fromEntries([...document.querySelectorAll(selector)].map(e=>[e.id,{opacity:getComputedStyle(e).opacity,transform:e.getAttribute('transform')||'',origin:getComputedStyle(e).transformOrigin,paths:[...e.querySelectorAll('path,circle,rect')].map(p=>({dash:p.style.strokeDashoffset,opacity:getComputedStyle(p).opacity}))}]))''',selector)
    times=[.3,2.7,6,12,20.18,22.58,25.09,31,40,44,46,56,60,70,76,81,86,89.5]
    forward={t:state(t) for t in times};reverse={t:state(t) for t in reversed(times)}
    mismatches=[t for t in times if forward[t]!=reverse[t]]
    differences={t:{key:dict(forward=forward[t].get(key),reverse=reverse[t].get(key)) for key in set(forward[t])|set(reverse[t]) if forward[t].get(key)!=reverse[t].get(key)} for t in mismatches}
    report=dict(times=times,same_state_after_reverse_seek=not mismatches,mismatches=mismatches,differences=differences,basis='actual mounted preview player.seek; active visible scene SVG group opacity/transforms and descendant path state. Offscreen scene virtualization is excluded; an initial all-mounted-node comparison incorrectly treated neighbor eviction as visual divergence.',composition_sha256=hashlib.sha256((V/'index.html').read_bytes()).hexdigest())
    (Q/'seek-consistency.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report));b.close()
    assert not mismatches,mismatches
