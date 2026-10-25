import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True);page=await b.new_page();await page.goto('http://127.0.0.1:3002/#project/video');await page.wait_for_timeout(4000)
        print('frames',[(f.url) for f in page.frames])
        print(await page.frames[1].evaluate('JSON.stringify({roots:[...document.querySelectorAll("[data-composition-id]")].map(x=>({id:x.id,comp:x.dataset.compositionId})),beats:[...document.querySelectorAll(".b1")].map(x=>({parent:x.closest("[data-composition-id]")?.id,cls:x.getAttribute("class")}))})'))
        await b.close()
asyncio.run(main())
