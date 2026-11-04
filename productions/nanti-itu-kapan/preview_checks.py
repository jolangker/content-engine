"""Record owned preview and inspect real playback and deterministic seeks."""
from pathlib import Path
import json,hashlib,time
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parent;V=P/'video';Q=V/'verification';Q.mkdir(exist_ok=True)
owner=dict(project=str(V),pid=27624,port=3003,studio_url='http://127.0.0.1:3003/#project/video',created_by_this_run=True,retention_reason='final preview and delivery render',release='after export verification before packaging')
(Q/'preview-owner.json').write_text(json.dumps(owner,indent=2)+'\n',encoding='utf-8')
with (P/'EPISODE.md').open('a',encoding='utf-8') as out:out.write('\n## Preview ownership\n\nNo existing preview for this project. This run created PID 27624 / port3003, http://127.0.0.1:3003/#project/video. Keep through final review/render; release after verified export. Other project on port3002 remains outside this run.\n')
timing=json.loads((V/'timing.json').read_text(encoding='utf-8'));scenes=timing['scenes'];duration=timing['duration_s']
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--autoplay-policy=no-user-gesture-required']);tab=browser.new_page(viewport=dict(width=1600,height=1000));errors=[];tab.on('pageerror',lambda e:errors.append(str(e)))
    response=tab.goto(owner['studio_url']);tab.wait_for_timeout(3000);assert response.status==200
    frame=tab.frames[1];frame.wait_for_function('window.__player && window.__renderReady');frame.evaluate('window.__player.pause()')
    def state(t):
        frame.evaluate('(t)=>window.__player.seek(t)',t);tab.wait_for_timeout(90)
        s=next(s for s in scenes if s['start']<=t<s['end']);selector=f'svg g[id^="f{s["id"]:02d}-"]';frame.wait_for_selector(selector,state='attached')
        return frame.evaluate('''selector=>Object.fromEntries([...document.querySelectorAll(selector)].map(e=>[e.id,{opacity:getComputedStyle(e).opacity,transform:e.getAttribute('transform')||'',paths:[...e.querySelectorAll('path,circle,rect,ellipse')].map(p=>({dash:p.style.strokeDashoffset,opacity:getComputedStyle(p).opacity}))}]))''',selector)
    times=[round(s['start']+s['duration']*.63,6) for s in scenes];forward={t:state(t) for t in times};reverse={t:state(t) for t in reversed(times)};bad=[t for t in times if forward[t]!=reverse[t]]
    (Q/'seek-consistency.json').write_text(json.dumps(dict(times=times,same_state_after_reverse_seek=not bad,mismatches=bad,composition_sha256=hashlib.sha256((V/'index.html').read_bytes()).hexdigest()),indent=2)+'\n',encoding='utf-8');assert not bad,bad
    frame.evaluate('window.__player.seek(0)');tab.screenshot(path=str(Q/'studio-preview.png'),full_page=True)
    tab.get_by_role('button',name='Play',exact=False).first.click();samples=[];start=time.monotonic()
    while time.monotonic()-start<duration+2:
        tab.wait_for_timeout(5000)
        samples.append(frame.evaluate('''()=>({audio:[...document.querySelectorAll('audio')].map(a=>({id:a.id,time:a.currentTime,paused:a.paused,ready:a.readyState,error:a.error?.message||null})),times:Object.fromEntries(Object.entries(window.__timelines||{}).filter(([k,v])=>typeof v.time==='function').map(([k,v])=>[k,v.time()]))})'''))
        if len(samples) in (1,9,18):tab.screenshot(path=str(Q/f'playing-{len(samples):02d}.png'))
        print('Playback sample',len(samples),flush=True)
    report=dict(status=response.status,url=tab.url,errors=errors,playback_samples=samples,expected_duration=duration,perceptual_listening='unavailable; actual player progression and media readiness measured, not heard')
    (Q/'preview-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');browser.close();assert not errors,errors
print(json.dumps(dict(http_status=200,seek_samples=len(times),playback_samples=len(samples),page_errors=errors)))
