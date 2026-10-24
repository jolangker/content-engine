const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url'),puppeteer=require('puppeteer');
(async()=>{
 const root=__dirname,plan=JSON.parse(fs.readFileSync(path.join(root,'scene-plan.json'),'utf8'));
 const files=fs.readdirSync(path.join(root,'boards/stills')).filter(n=>/^frame-\d+-at-.*\.png$/.test(n)).sort();
 if(files.length!==16)throw Error('Expected sixteen static scene poses');
 const cards=plan.scenes.map((s,i)=>`<article class="frame"><img src="stills/${files[i]}" alt="${s.title}"><div class="copy"><div class="title">${String(i+1).padStart(2,'0')}: ${s.title}</div><div class="time">${s.start.toFixed(1)}–${(s.start+s.duration).toFixed(1)} s</div><p class="words">${s.purpose}</p></div></article>`).join('');
 const doc=`<!doctype html><html><meta charset="utf-8"><title>Satu jahitan mesin jahit — storyboard</title><style>@font-face{font-family:Manrope;src:url('../assets/fonts/manrope.ttf')}*{box-sizing:border-box}body{margin:0;padding:40px;width:1920px;background:#DCE1DD;color:#172B3B;font:20px/1.5 Manrope}h1{font-size:42px;margin:0}header p{margin:8px 0 30px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}.frame{background:#F8F9F5;overflow:hidden;border-radius:8px}img{display:block;width:100%}.copy{padding:18px}.title{font-size:23px;font-weight:800}.time{font-size:20px;color:#536775}.words{margin:8px 0;font-size:19px;min-height:85px}</style><body><header><h1>Satu jahitan mesin jahit</h1><p>Di Balik Benda v3 · Visual 2.5D · 90 seconds · 16 explanatory shots · static layouts before synthesis and animation</p></header><main class="grid">${cards}</main></body></html>`;
 const board=path.join(root,'boards/storyboard.html');fs.writeFileSync(board,doc);
 const browser=await puppeteer.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{
  const page=await browser.newPage();await page.setViewport({width:1920,height:1200,deviceScaleFactor:1});await page.goto(pathToFileURL(board).href,{waitUntil:'networkidle0'});await page.evaluate(()=>document.fonts.ready);
  const qa=await page.evaluate(()=>({count:document.querySelectorAll('.frame').length,images:[...document.images].map(i=>({width:i.naturalWidth,height:i.naturalHeight})),width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,overflow:[...document.querySelectorAll('.title,.time,.words')].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.textContent)}));
  if(qa.count!==16||qa.images.some(i=>!i.width)||qa.overflow.length)throw Error(JSON.stringify(qa));
  await page.screenshot({path:path.join(root,'boards/storyboard.png'),fullPage:true});fs.mkdirSync(path.join(root,'verification'),{recursive:true});fs.writeFileSync(path.join(root,'verification/storyboard.json'),JSON.stringify(qa,null,2));console.log(JSON.stringify(qa));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
