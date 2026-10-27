const fs=require('fs'),path=require('path'),puppeteer=require('puppeteer'),{pathToFileURL}=require('url');
(async()=>{
 const plan=JSON.parse(fs.readFileSync(path.join(__dirname,'timing.json'),'utf8')).scenes,dir=path.join(__dirname,'verification'),scratch=path.join(__dirname,'.hyperframes/artifacts');fs.mkdirSync(dir,{recursive:true});fs.mkdirSync(scratch,{recursive:true});
 let doc='<html><head><base href="../../"><script>window.__timelines={};</script><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script></head><body>';
 for(const s of plan){let h=fs.readFileSync(path.join(__dirname,'compositions',s.id+'.html'),'utf8').replace(/^<template>/,'').replace(/<\/template>$/,'');h=h.replace(/<script>([\s\S]*?)<\/script>/g,(_,x)=>'<script>(function(){'+x+'})();</script>');doc+=h;}doc+='</body></html>';fs.writeFileSync(path.join(scratch,'motion-inspection.html'),doc);
 const browser=await puppeteer.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{
  const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(String(e)));await page.goto(pathToFileURL(path.join(scratch,'motion-inspection.html')).href,{waitUntil:'networkidle0'});
  const results=await page.evaluate(plan=>plan.map(s=>{
   function sample(t){window.__timelines[s.id].totalTime(t,false);return JSON.parse(JSON.stringify(window.__mechanism));}
   const samples=[];for(let f=1;f<Math.round(s.duration*30);f++)samples.push(sample(f/30));
   const one=sample(s.duration*.713);sample(s.duration*.99);sample(.001);const two=sample(s.duration*.713);
   const drive=['drive','contact','resume','input'].includes(s.key);
   const coupled=!drive||samples.filter(x=>s.key==='drive'||s.key==='input'||s.key==='contact'&&x.time/s.duration>.42||s.key==='resume'&&x.time/s.duration>.67).every(x=>Math.abs(x.input-x.output)<1e-8&&Math.abs(x.alpha)<1e-8);
   const overrun=['independent','overtake','ramp','reset','clicks','answer','mystery'].includes(s.key);
   const fixedInput=!overrun||samples.every(x=>x.input===0);
   const safeTip=['spring'].includes(s.key)||samples.every(x=>Math.abs(x.relative)<1e-5||x.gap>=-1e-6);
   const finite=samples.every(x=>Object.values(x).every(v=>typeof v!=='number'||Number.isFinite(v)));
   const pivot=document.getElementById(s.id+'-pawl0');const pivotFixed=!pivot||samples.every(()=>{const m=pivot.transform.baseVal.consolidate()?.matrix;return !m||Math.abs(m.e)<1e-9&&Math.abs(m.f)<1e-9});
   const resetEvents=[];for(let k=1;k<samples.length;k++){if(samples[k-1].alpha-samples[k].alpha>2&&(!resetEvents.length||samples[k].time-resetEvents.at(-1)>.14))resetEvents.push(samples[k].time);}
   return {scene:s.id,samples:samples.length,resetEvents,seekDeterministic:JSON.stringify(one)===JSON.stringify(two),finite,coupledDrive:coupled,fixedCoastInput:fixedInput,pawlTipClearance:safeTip,pivotFixed,minGap:Math.min(...samples.filter(x=>Math.abs(x.relative)>1e-5).map(x=>x.gap)),alphaRange:[Math.min(...samples.map(x=>x.alpha)),Math.max(...samples.map(x=>x.alpha))]};
  }),plan);
  const failed=results.filter(r=>!r.seekDeterministic||!r.finite||!r.coupledDrive||!r.fixedCoastInput||!r.pawlTipClearance||!r.pivotFixed);
  const report={status:failed.length||errors.length?'failed':'passed',results,errors,method:'Source scene timelines sampled at output30fps; reverse seeks, finite states, shared angular drive, fixed coasting input, analytic pawl-tip/tooth-ramp clearance and fixed pivot. Actual mounting verified separately by CLI check/snapshots.',limits:'Tip clearance is a schematic contact condition, not a full solid-body collision simulation. No subjective full-speed listening or human approval claimed.'};fs.writeFileSync(path.join(dir,'motion.json'),JSON.stringify(report,null,2));
  if(failed.length||errors.length)throw Error(JSON.stringify({failed,errors}));console.log(JSON.stringify({status:report.status,scenes:results.length,frames:results.reduce((n,r)=>n+r.samples,0)}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
