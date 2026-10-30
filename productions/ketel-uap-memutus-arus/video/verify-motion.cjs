// Per-frame physical constraints against scene timelines, including reverse seeks.
const fs=require('fs'),path=require('path'),puppeteer=require('puppeteer'),{pathToFileURL}=require('url');
(async()=>{
 const V=__dirname,plan=JSON.parse(fs.readFileSync(path.join(V,'timing.json'),'utf8')).scenes,Q=path.join(V,'verification');fs.mkdirSync(Q,{recursive:true});
 let doc='<html><head><base href="../../"><script>window.__timelines={};</script><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script></head><body>';
 for(const s of plan){let h=fs.readFileSync(path.join(V,'compositions',s.id+'.html'),'utf8').replace(/^<template>/,'').replace(/<\/template>$/,'');h=h.replace(/<script>([\s\S]*?)<\/script>/g,(_,x)=>'<script>(function(){'+x+'})();</script>');doc+=h;}doc+='</body></html>';
 const scratch=path.join(V,'.hyperframes/artifacts');fs.mkdirSync(scratch,{recursive:true});const file=path.join(scratch,'mechanism-inspection.html');fs.writeFileSync(file,doc);
 const browser=await puppeteer.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{
  const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(String(e)));await page.goto(pathToFileURL(file).href,{waitUntil:'networkidle0'});
  const results=await page.evaluate(plan=>plan.map(s=>{
   const sample=t=>{window.__timelines[s.id].totalTime(t,false);return JSON.parse(JSON.stringify(window.__mechanisms[s.id]));};
   const samples=[];for(let frame=1;frame<Math.round(s.duration*30);frame++)samples.push(sample(frame/30));
   const a=sample(s.duration*.713);sample(s.duration*.99);sample(.001);const b=sample(s.duration*.713);
   const finite=samples.every(x=>Object.values(x).every(v=>typeof v!=='number'||Number.isFinite(v)));
   const bounds=samples.every(x=>x.trip>=0&&x.trip<=1&&x.link>=-1e-8&&x.link<44);
   const noPowerAcrossGap=samples.every(x=>!x.powered||Math.abs(x.contactGap)<1e-6);
   const coolingCannotRestart=s.mode!=='latch'||samples.every(x=>x.trip===1&&!x.closed&&!x.powered);
   const noPillarPenetration=samples.every(x=>!('tongueTipWorldY'in x)||x.tongueTipWorldY<=x.pillarTop+1e-8);
   const monotonicTrip=['snap','trip','open'].includes(s.mode)?samples.every((x,n)=>!n||x.trip>=samples[n-1].trip-1e-8):true;
   const contactMovesWithLink=samples.every(x=>Math.abs(x.contactGap-x.link)<1e-8);
   return {scene:s.id,frames:samples.length,seekDeterministic:JSON.stringify(a)===JSON.stringify(b),finite,bounds,noPowerAcrossGap,coolingCannotRestart,noPillarPenetration,monotonicTrip,contactMovesWithLink,poses:[.05,.33,.67,.95].map(q=>sample(q*s.duration))};
  }),plan);
  const bools=['seekDeterministic','finite','bounds','noPowerAcrossGap','coolingCannotRestart','noPillarPenetration','monotonicTrip','contactMovesWithLink'];
  const failed=results.filter(r=>bools.some(k=>!r[k]));
  const report={status:failed.length||errors.length?'failed':'passed',method:'Every output30fps scene frame and nonsequential/reverse seeks. Source-backed constraints: current only across closed contacts; fixed pillar nonpenetration; off-state latch survives disc cooling; rigid link/contact travel coupled.',results,errors,limits:'Schematic enlarged geometry, not manufacturing tolerance or a physical simulation. Static/decoded visual review and sound evidence are separate.'};fs.writeFileSync(path.join(Q,'motion.json'),JSON.stringify(report,null,2));
  if(failed.length||errors.length)throw Error(JSON.stringify({failed,errors}));console.log(JSON.stringify({status:report.status,scenes:results.length,frames:results.reduce((n,r)=>n+r.frames,0)}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
