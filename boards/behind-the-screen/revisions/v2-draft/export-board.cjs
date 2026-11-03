// Adapted from this workspace's established static-board exporter.
// All pages use file: URLs. No preview server is started.
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
  const errors = [];
  try {
    const page = await browser.newPage();
    page.on('pageerror', error => errors.push(error.message));
    page.on('requestfailed', request => errors.push(request.url()+': '+request.failure()?.errorText));
    await page.setViewport({width:1800,height:1200,deviceScaleFactor:1});
    await page.goto(pathToFileURL(path.join(root,'style-board.html')).href,{waitUntil:'networkidle0'});
    await page.evaluate(() => document.fonts.ready);
    const report = await page.evaluate(() => {
      const board = document.querySelector('#board').getBoundingClientRect();
      const fonts = [...document.fonts].map(f=>({family:f.family,status:f.status,weight:f.weight}));
      const overflow = [...document.querySelectorAll('h1,h2,p,figcaption,.status,.foot,.swatch')]
        .filter(el => el.scrollWidth > el.clientWidth+1)
        .map(el => el.textContent.trim());
      const svgText = [...document.querySelectorAll('.study')].map(study => {
        const svg = study.querySelector('svg');
        const bounds = svg.getBoundingClientRect();
        const out = [...svg.querySelectorAll('text')].filter(el=>{
          const r=el.getBoundingClientRect();
          return r.left<bounds.left-1 || r.right>bounds.right+1 || r.top<bounds.top-1 || r.bottom>bounds.bottom+1;
        }).map(el=>el.textContent);
        const visibleWords=[...svg.querySelectorAll('text')].map(el=>el.textContent.trim()).join(' ').split(/\s+/).filter(Boolean).length;
        return {id:study.id,width:bounds.width,height:bounds.height,outOfFrame:out,visibleWords};
      });
      return {board:{width:board.width,height:board.height},fonts,overflow,svgText,
        horizontalOverflow:document.documentElement.scrollWidth>1800};
    });
    await page.screenshot({path:path.join(root,'style-board.png'),fullPage:true});
    await (await page.$('.studies')).screenshot({path:path.join(root,'illustration-review.png')});
    await (await page.$('.poses')).screenshot({path:path.join(root,'motion-poses.png')});
    const samples=[];
    await page.setViewport({width:1080,height:1920,deviceScaleFactor:1});
    for (const name of ['passkeys','privacy','delivery']) {
      await page.goto(pathToFileURL(path.join(root,'studies',name+'.svg')).href,{waitUntil:'networkidle0'});
      await page.evaluate(() => document.fonts.ready);
      await page.screenshot({path:path.join(root,'studies',name+'.png')});
      const geometry=await page.evaluate(()=>({width:document.documentElement.getBoundingClientRect().width,
        height:document.documentElement.getBoundingClientRect().height,
        visibleTextCount:document.querySelectorAll('text').length,
        fonts:[...document.fonts].map(f=>({family:f.family,status:f.status,weight:f.weight}))}));
      samples.push({name,...geometry});
    }
    // A phone-size comparison is an additional inspection artifact, not a video.
    await page.setViewport({width:1234,height:790,deviceScaleFactor:1});
    await page.goto(pathToFileURL(path.join(root,'style-board.html')).href,{waitUntil:'networkidle0'});
    const urls=['passkeys','privacy','delivery'].map(name=>pathToFileURL(path.join(root,'studies',name+'.png')).href);
    await page.setContent('<html><body style="margin:0;padding:18px;background:#F0EFF8;display:flex;gap:24px">'+
      urls.map(url=>'<img src="'+url+'" style="display:block;width:384px;height:682.666667px">').join('')+'</body></html>');
    await page.evaluate(()=>Promise.all([...document.images].map(img=>img.decode())));
    await page.screenshot({path:path.join(root,'phone-review.png')});
    report.samples=samples;
    report.browserErrors=errors;
    fs.writeFileSync(path.join(root,'export-report.json'),JSON.stringify(report,null,2)+'\n');
    if(errors.length || report.overflow.length || report.horizontalOverflow ||
       report.fonts.some(f=>f.status!=='loaded') || report.svgText.some(s=>s.outOfFrame.length) ||
       samples.some(s=>s.width!==1080 || s.height!==1920 || (s.visibleTextCount>0 && s.fonts.some(f=>f.status!=='loaded'))) ||
       report.svgText.some(s=>s.visibleWords!==0)) {
      throw new Error('Static export needs correction: '+JSON.stringify(report));
    }
    console.log(JSON.stringify(report));
  } finally {
    await browser.close();
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
