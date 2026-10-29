// Inspect the authored mechanism at output-frame times and nonsequential seeks.
const fs=require('fs'),path=require('path'),puppeteer=require('puppeteer'),{pathToFileURL}=require('url');
(async()=>{
 const V=__dirname,plan=JSON.parse(fs.readFileSync(path.join(V,'timing.json'),'utf8')).scenes,Q=path.join(V,'verification');fs.mkdirSync(Q,{recursive:true});
 let doc='<html><head><base href="../../"><script>window.__timelines={};</script><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script></head><body>';
 for(const s of plan){let h=fs.readFileSync(path.join(V,'compositions',s.id+'.html'),'utf8').replace(/^<template>/,'').replace(/<\/template>$/,'');h=h.replace(/<script>([\s\S]*?)<\/script>/g,(_,x)=>'<script>(function(){'+x+'})();</script>');doc+=h;}doc+='</body></html>';
 const scratch=path.join(V,'.hyperframes/artifacts');fs.mkdirSync(scratch,{recursive:true});const file=path.join(scratch,'mechanism-inspection.html');fs.writeFileSync(file,doc);
 const browser=await puppeteer.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(String(e)));await page.goto(pathToFileURL(file).href,{waitUntil:'networkidle0'});
 const results=await page.evaluate(plan=>plan.map(s=>{
  const sample=t=>{window.__timelines[s.id].totalTime(t,false);return JSON.parse(JSON.stringify(window.__mechanisms[s.id]));};
  let samples=[];for(let frame=1;frame<Math.round(s.duration*30);frame++)samples.push(sample(frame/30));
  const a=sample(s.duration*.713);sample(s.duration*.99);sample(.001);const b=sample(s.duration*.713);
  const leadNeverRetreats=samples.every((x,n)=>n===0||x.l>=samples[n-1].l-1e-8);
  const ringWithinStops=samples.every(x=>x.r>=-1e-8&&x.r<=24+1e-8);
  const shoulderNotPenetrated=samples.every(x=>515+x.r<=539+1e-8);
  const gripCarriesLead=samples.filter(x=>x.p<.55).every(x=>Math.abs(x.q-x.l)<1e-8);
  const releasedReturnKeepsLead=samples.filter(x=>x.p>.78).every(x=>Math.abs(x.l-24)<1e-8);
  const tipFixed=samples.every(x=>x.tipFixed===true);
  const openingOnlyAfterStop=samples.filter(x=>x.p>.55&&x.p<=.78).every(x=>Math.abs(x.r-24)<1e-8);
  const pose=p=>{const u=(p-s.phase_start)/(s.phase_end-s.phase_start);return u};
  return {scene:s.id,frames:samples.length,seekDeterministic:JSON.stringify(a)===JSON.stringify(b),finite:samples.every(x=>Object.values(x).every(v=>typeof v!=='number'||Number.isFinite(v))),leadNeverRetreats,ringWithinStops,shoulderNotPenetrated,gripCarriesLead,releasedReturnKeepsLead,tipFixed,openingOnlyAfterStop,poses:[.05,.33,.67,.95].map(q=>sample(q*s.duration))};
 }),plan);
 const failed=results.filter(r=>!r.seekDeterministic||!r.finite||!r.leadNeverRetreats||!r.ringWithinStops||!r.shoulderNotPenetrated||!r.gripCarriesLead||!r.releasedReturnKeepsLead||!r.tipFixed||!r.openingOnlyAfterStop);
 const report={status:failed.length||errors.length?'failed':'passed',method:'Every output30fps scene frame; independent ring-stop, shared grip travel and retained-lead constraints; reverse/random seeking. Values are illustrative units, not product tolerances.',results,errors,limits:'Mounted full-film layout and decoded delivery frames inspected separately. This does not establish perceptual audio quality.'};fs.writeFileSync(path.join(Q,'motion.json'),JSON.stringify(report,null,2));
 if(failed.length||errors.length)throw Error(JSON.stringify({failed,errors}));console.log(JSON.stringify({status:report.status,scenes:results.length,frames:results.reduce((n,r)=>n+r.frames,0)}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
