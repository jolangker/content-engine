// Static local-file export. Every Chromium process is closed in finally.
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const puppeteer = require('puppeteer');

(async()=>{
 const root=__dirname;
 const browser=await puppeteer.launch({headless:true,executablePath:process.env.CHROME_EXECUTABLE||'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try {
  const page=await browser.newPage();const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('requestfailed',r=>errors.push(r.url()+': '+r.failure()?.errorText));
  await page.setViewport({width:1740,height:1200,deviceScaleFactor:1});
  await page.goto(pathToFileURL(path.join(root,'style-board.html')).href,{waitUntil:'networkidle0'});
  await page.evaluate(()=>document.fonts.ready);
  const report=await page.evaluate(()=>({
   board:{width:document.querySelector('#board').offsetWidth,height:document.querySelector('#board').offsetHeight},
   fonts:[...document.fonts].map(f=>({family:f.family,weight:f.weight,status:f.status})),
   horizontalOverflow:document.documentElement.scrollWidth>1740,
   missingImages:[...document.images].filter(x=>!x.complete||x.naturalWidth===0).map(x=>x.src),
   overflow:[...document.querySelectorAll('h1,h2,h3,p,.mono,.chips,.pose-labels')].filter(x=>x.scrollWidth>x.clientWidth+2).map(x=>x.textContent.trim()),
   studies:[...document.querySelectorAll('.native')].map(x=>({id:x.id,width:x.offsetWidth,height:x.offsetHeight,caption:(()=>{const c=x.querySelector('.caption');return{left:c.offsetLeft,top:c.offsetTop,width:c.offsetWidth,height:c.offsetHeight}})()})),
  }));
  await page.screenshot({path:path.join(root,'style-board.png'),fullPage:true});
  await page.pdf({path:path.join(root,'style-board.pdf'),width:'1740px',height:(report.board.height+2)+'px',printBackground:true,margin:{top:0,bottom:0,left:0,right:0},preferCSSPageSize:false});
  const cast=await page.$('.acting-row');await cast.screenshot({path:path.join(root,'character-direction.png')});
  await page.setViewport({width:1080,height:1920,deviceScaleFactor:1});
  for(let i=1;i<=3;i++){
   const id='native-0'+i;
   await page.evaluate(id=>{
    const clone=document.getElementById(id).cloneNode(true);clone.id='export-clone';clone.style.cssText='position:absolute;left:0;top:0;transform:none;width:1080px;height:1920px';
    document.querySelector('#board').style.display='none';document.body.appendChild(clone);
   },id);
   await page.screenshot({path:path.join(root,'study-0'+i+'.png')});
   await page.setViewport({width:360,height:640,deviceScaleFactor:1});
   await page.evaluate(()=>{document.querySelector('#export-clone').style.transform='scale(0.3333333333)';document.querySelector('#export-clone').style.transformOrigin='top left'});
   await page.screenshot({path:path.join(root,'phone-study-0'+i+'.png')});
   await page.evaluate(()=>{document.querySelector('#export-clone').remove();document.querySelector('#board').style.display='block'});
   await page.setViewport({width:1080,height:1920,deviceScaleFactor:1});
  }
  report.browserErrors=errors;
  fs.writeFileSync(path.join(root,'export-report.json'),JSON.stringify(report,null,2)+'\n');
  if(errors.length||report.missingImages.length||report.overflow.length||report.horizontalOverflow||report.fonts.some(f=>f.status!=='loaded'))throw Error('Export requires correction: '+JSON.stringify(report));
  console.log(JSON.stringify(report,null,2));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
