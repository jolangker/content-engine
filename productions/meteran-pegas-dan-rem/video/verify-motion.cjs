// Check coupled mechanism constraints at every output frame and reverse seeks.
const fs=require('fs'),path=require('path'),puppeteer=require('puppeteer'),{pathToFileURL}=require('url');
(async()=>{
 const V=__dirname,plan=JSON.parse(fs.readFileSync(path.join(V,'timing.json'),'utf8')).scenes,Q=path.join(V,'verification');fs.mkdirSync(Q,{recursive:true});
 let doc='<html><head><meta charset="utf-8"><base href="../../"><script>window.__timelines={};</script><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script></head><body>';
 for(const s of plan){let h=fs.readFileSync(path.join(V,'compositions',s.id+'.html'),'utf8').replace(/^<template>/,'').replace(/<\/template>$/,'');h=h.replace(/<script>([\s\S]*?)<\/script>/g,(_,x)=>'<script>(function(){'+x+'})();</script>');doc+=h;}doc+='</body></html>';
 const file=path.join(V,'.hyperframes/artifacts/mechanism-inspection.html');fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,doc);
 const browser=await puppeteer.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{
  const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(String(e)));await page.goto(pathToFileURL(file).href,{waitUntil:'networkidle0'});
  const results=await page.evaluate(plan=>plan.map(s=>{
   const sample=t=>{window.__timelines[s.id].totalTime(t,false);return JSON.parse(JSON.stringify(window.__mechanismStates[s.id]));};
   const samples=[];for(let f=1;f<Math.round(s.duration*30);f++)samples.push(sample(f/30));
   const a=sample(s.duration*.713);sample(s.duration*.99);sample(.001);const b=sample(s.duration*.713);
   const finite=samples.every(x=>Object.values(x).every(v=>typeof v!=='number'||Number.isFinite(v)));
   const bounds=samples.every(x=>x.ext>=70-1e-8&&x.ext<=300+1e-8&&x.lock>=0&&x.lock<=1);
   const noBladePenetration=samples.every(x=>x.tipy<=620+1e-8&&(!x.contact||Math.abs(x.tipy-620)<1e-8));
   const coupledReel=samples.every(x=>Math.abs(x.angle+x.ext/190*180/Math.PI)<1e-8);
   const noMotionWhileClamped=samples.every((x,n)=>!n||x.lock<.74||samples[n-1].lock<.74||Math.abs(x.ext-samples[n-1].ext)<1e-8);
   const fullClampOnSupport=samples.every(x=>x.flex<.999||x.tipx>=490&&x.tipx<=511);
   return {scene:s.id,frames:samples.length,seekDeterministic:JSON.stringify(a)===JSON.stringify(b),finite,bounds,noBladePenetration,coupledReel,noMotionWhileClamped,fullClampOnSupport,poses:[.05,.33,.67,.95].map(q=>sample(q*s.duration))};
  }),plan);
  const continuity=await page.evaluate(plan=>{const ids=[['pull','anchor'],['anchor','energy'],['energy','return'],['slider','guide'],['guide','touch'],['touch','snap'],['snap','clamp'],['clamp','held'],['held','unlock'],['unlock','rewind']];return ids.map(([a,b])=>{const x=plan.find(s=>s.key===a),y=plan.find(s=>s.key===b);window.__timelines[x.id].totalTime(x.duration,false);const p={...window.__mechanismStates[x.id]};window.__timelines[y.id].totalTime(.00001,false);const q=window.__mechanismStates[y.id];return {from:a,to:b,passed:Math.abs(p.ext-q.ext)<1e-6&&Math.abs(p.lock-q.lock)<1e-6};});},plan);
  const bools=['seekDeterministic','finite','bounds','noBladePenetration','coupledReel','noMotionWhileClamped','fullClampOnSupport'];
  const failed=results.filter(r=>bools.some(k=>!r[k]));
  const report={status:failed.length||errors.length||continuity.some(x=>!x.passed)?'failed':'passed',method:'Every30fps scene frame, nonsequential and reverse seeks; blade/reel coupling, tongue nonpenetration, locked blade hold and fixed-support contact.',results,errors,continuity,limits:'Original explanatory geometry, not a physical simulation or manufacturing tolerance. Actual frames and encoded audio verified separately.'};fs.writeFileSync(path.join(Q,'motion.json'),JSON.stringify(report,null,2));
  if(failed.length||errors.length||continuity.some(x=>!x.passed))throw Error(JSON.stringify({failed,errors}));console.log(JSON.stringify({status:report.status,scenes:results.length,frames:results.reduce((n,r)=>n+r.frames,0)}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
