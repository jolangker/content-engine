import asyncio,json,sys,re
from pathlib import Path
from playwright.async_api import async_playwright
V=Path(__file__).resolve().parent/'video'
async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,args=['--autoplay-policy=no-user-gesture-required'])
        page=await browser.new_page(viewport=dict(width=1600,height=1000)); errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        r=await page.goto('http://127.0.0.1:3002/#project/video')
        await page.wait_for_timeout(5000)
        await page.screenshot(path=str(V/'verification/studio-preview.png'),full_page=True)
        report=dict(status=r.status,url=page.url,title=await page.title(),errors=errors,frames=[f.url for f in page.frames],buttons=await page.get_by_role('button').all_text_contents())
        if '--play' in sys.argv:
            controls=await page.locator('button').evaluate_all('(els)=>els.map(e=>({label:e.getAttribute("aria-label"),title:e.getAttribute("title")})).filter(x=>/play/i.test((x.label||"")+" "+(x.title||"")))')
            print('Play controls:',json.dumps(controls),flush=True)
            button=page.get_by_role('button',name=re.compile('^Play',re.I)).first
            await button.click()
            samples=[]
            for k in range(18):
                await page.wait_for_timeout(5000)
                frame=page.frames[1]
                state=await frame.evaluate('({timelines:Object.fromEntries(Object.entries(window.__timelines||{}).filter(([k,v])=>typeof v.time==="function").map(([k,v])=>[k,v.time()])),audio:[...document.querySelectorAll("audio")].map(a=>({id:a.id,time:a.currentTime,paused:a.paused,ready:a.readyState,error:a.error?.message||null}))})')
                state['clock']=[x for x in await page.get_by_role('button').all_text_contents() if re.match(r'\d\d:\d\d',x)]
                samples.append(state)
                if k in [0,7,15]:await page.screenshot(path=str(V/f'verification/playing-{k:02}.png'))
                print('Playback sample',k+1,state['clock'],flush=True)
            report['playback_samples']=samples
            report['perceptual_listening']='Not available; full player progression and media readiness checked programmatically, illustrated states inspected separately.'
        (V/'verification/preview-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        print(json.dumps(report));await browser.close()
asyncio.run(main())
