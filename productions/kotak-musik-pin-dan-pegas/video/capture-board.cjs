const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url'),puppeteer=require('puppeteer');
(async()=>{
 const plan=JSON.parse(fs.readFileSync(path.join(__dirname,'scene-plan.json'),'utf8'));
 const dir=path.join(__dirname,'boards'),files=fs.readdirSync(path.join(dir,'stills')).filter(f=>/^frame-\d+.*\.png$/.test(f)).sort();
 if(files.length!==plan.length)throw Error('Storyboard still count mismatch: '+files.length);
 const cards=plan.map((s,i)=>`<article class="frame"><img src="stills/${files[i]}" alt="${s.id}"><div class="title">${String(i+1).padStart(2,'0')}: ${s.title}</div><div class="time">${s.start.toFixed(2)}–${s.end.toFixed(2)}s · estimate</div><p class="words">${s.text}</p></article>`).join('');
 fs.writeFileSync(path.join(dir,'storyboard.html'),`<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Kotak musik · storyboard</title><style>*{box-sizing:border-box}body{margin:0;width:1920px;padding:40px;background:#ECEEE9;color:#172B3B;font-family:Arial,sans-serif}h1{font-size:40px;margin:0 0 12px}.sub{font-size:22px;margin-bottom:30px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}.frame{background:#F8F9F5;border-radius:14px;overflow:hidden;padding-bottom:18px}.frame img{width:100%;display:block}.title{font-size:23px;font-weight:bold;padding:18px 18px 7px}.time{font-size:18px;padding:0 18px}.words{font-size:19px;line-height:1.4;padding:0 18px}</style></head><body><h1>Kotak musik: pin dan pegas</h1><div class="sub">Di Balik Benda v4 · 90 seconds · 16 shots · pre-audio static layout review under delegated automation</div><main class="grid">${cards}</main></body></html>`);
 const browser=await puppeteer.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{
  const page=await browser.newPage();await page.setViewport({width:1920,height:1200,deviceScaleFactor:1});
  await page.goto(pathToFileURL(path.join(dir,'storyboard.html')).href,{waitUntil:'networkidle0'});await page.evaluate(()=>document.fonts.ready);
  const report=await page.evaluate(()=>({frames:document.querySelectorAll('.frame').length,missing:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,ids:[...document.images].map(i=>i.alt)}));
  if(report.missing.length||report.frames!==16||report.ids.join(',')!==plan.map(x=>x.id).join(','))throw Error(JSON.stringify(report));
  await page.screenshot({path:path.join(dir,'storyboard.png'),fullPage:true});fs.writeFileSync(path.join(dir,'verification.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
