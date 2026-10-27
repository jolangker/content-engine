// Static local-file export. No preview server is started.
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const puppeteer = require('puppeteer');

(async () => {
  const root = __dirname;
  const browser = await puppeteer.launch({
    headless: true,
    executablePath: process.env.CHROME_EXECUTABLE || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  });
  try {
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('requestfailed', request => errors.push(request.url()+': '+request.failure()?.errorText));
    await page.setViewport({width:1700,height:1200,deviceScaleFactor:1});
    await page.goto(pathToFileURL(path.join(root,'style-board.html')).href,{waitUntil:'networkidle0'});
    await page.evaluate(() => document.fonts.ready);
    const qa = await page.evaluate(() => {
      const rect = document.querySelector('#board').getBoundingClientRect();
      const overflowing = [...document.querySelectorAll('h1,h2,h3,h4,p,.meta,.foot,.story-link,.index,.segment')].filter(el => el.scrollWidth > el.clientWidth+1).map(el => el.textContent.trim());
      const cards = [...document.querySelectorAll('.study')].map(el=>({id:el.id,width:el.clientWidth+2,height:el.clientHeight+2}));
      const fontState = [...document.fonts].map(f=>({family:f.family,status:f.status,weight:f.weight}));
      const captions = [...document.querySelectorAll('.study')].map(study => {
        const caption = study.querySelector('.caption');
        const block = caption.querySelector('span');
        const artRect = study.querySelector('.art').getBoundingClientRect();
        const capRect = caption.getBoundingClientRect();
        const blockRect = block.getBoundingClientRect();
        const css = getComputedStyle(caption);
        return {id:study.id,top:parseFloat(css.top),left:parseFloat(css.left),width:capRect.width,fontSize:parseFloat(css.fontSize),fontWeight:css.fontWeight,clearance:capRect.top-artRect.bottom,fits:blockRect.width<=capRect.width+1 && blockRect.height<=2*parseFloat(css.lineHeight)+2*8.47+1};
      });
      return {board:{width:rect.width,height:rect.height},fonts:fontState,horizontalOverflow:document.documentElement.scrollWidth>1700,overflowing,cards,captions};
    });
    await page.screenshot({path:path.join(root,'style-board.png'),fullPage:true});
    for (const id of ['study-01','study-02','study-03']) {
      const el = await page.$('#'+id);
      await el.screenshot({path:path.join(root,id+'.png')});
    }
    const defaults = await page.$('.pacing');
    await defaults.screenshot({path:path.join(root,'production-defaults.png')});
    const direction = await page.$('.complexity');
    await direction.screenshot({path:path.join(root,'shot-direction.png')});
    const interactions = await page.$('.interaction-direction');
    await interactions.screenshot({path:path.join(root,'interaction-direction.png')});
    const discovery = await page.$('.discovery-direction');
    await discovery.screenshot({path:path.join(root,'discovery-direction.png')});
    const captionFraming = await page.$('.studies');
    await captionFraming.screenshot({path:path.join(root,'caption-framing.png')});
    qa.browserErrors = errors;
    fs.writeFileSync(path.join(root,'export-report.json'),JSON.stringify(qa,null,2)+'\n');
    if(errors.length || qa.overflowing.length || qa.horizontalOverflow || qa.fonts.some(f=>f.status!=='loaded') || qa.captions.some(c=>!c.fits || c.clearance < 60*508/1080 || Math.abs(c.top-1500*508/1080)>0.1 || c.fontWeight!=='600')) {
      throw new Error('Export needs correction: '+JSON.stringify(qa));
    }
    console.log(JSON.stringify(qa));
  } finally {
    await browser.close();
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
