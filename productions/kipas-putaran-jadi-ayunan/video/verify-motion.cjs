const fs=require('fs'),path=require('path'),puppeteer=require('puppeteer'),{pathToFileURL}=require('url');
(async()=>{
 const plan=JSON.parse(fs.readFileSync(path.join(__dirname,'timing.json'),'utf8')).scenes,dir=path.join(__dirname,'verification'),scratch=path.join(__dirname,'.hyperframes/artifacts');fs.mkdirSync(dir,{recursive:true});fs.mkdirSync(scratch,{recursive:true});
 let doc='<html><head><base href="../../"><script>window.__timelines={};</script><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script></head><body>';
 for(const s of plan){let h=fs.readFileSync(path.join(__dirname,'compositions',s.id+'.html'),'utf8').replace(/^<template>/,'').replace(/<\/template>$/,'');h=h.replace(/<script>([\s\S]*?)<\/script>/g,(_,x)=>'<script>(function(){'+x+'})();</script>');doc+=h;}doc+='</body></html>';fs.writeFileSync(path.join(scratch,'motion-inspection.html'),doc);
 const browser=await puppeteer.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{
  const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(String(e)));await page.goto(pathToFileURL(path.join(scratch,'motion-inspection.html')).href,{waitUntil:'networkidle0'});
  const results=await page.evaluate(plan=>plan.map(s=>{
   const sample=t=>{window.__timelines[s.id].totalTime(t,false);return JSON.parse(JSON.stringify(window.__mechanism));};
   const samples=[];for(let f=1;f<Math.round(s.duration*30);f++)samples.push(sample(f/30));
   const one=sample(s.duration*.713);sample(s.duration*.99);sample(.001);const two=sample(s.duration*.713);
   const finite=samples.every(x=>Object.values(x).every(v=>typeof v!=='number'||Number.isFinite(v)));
   const lengthError=Math.max(...samples.map(x=>Math.abs(x.length-220)));
   const monotonic=samples.every((x,n)=>n===0||x.theta>=samples[n-1].theta-1e-9);
   const endpoint=samples.every(x=>Math.abs(Math.hypot(x.Cx,x.Cy)-230)<1e-8);
   const stopped=s.key!=='blade'||samples.every(x=>x.theta===samples[0].theta);
   const signs=[];for(let k=1;k<samples.length;k++){let delta=samples[k].phi-samples[k-1].phi;if(Math.abs(delta)>1e-7)signs.push(Math.sign(delta));}
   const reversed=signs.some((v,n)=>n&&v!==signs[n-1]);
   return {scene:s.id,samples:samples.length,seekDeterministic:JSON.stringify(one)===JSON.stringify(two),finite,maxRodLengthError:lengthError,constantHeadCarrierOffset:endpoint,crankNeverReverses:monotonic,clutchStopsOutput:stopped,headReverses:reversed,phiRange:[Math.min(...samples.map(x=>x.phi)),Math.max(...samples.map(x=>x.phi))],poses:[.05,.32,.65,.95].map(q=>sample(q*s.duration))};
  }),plan);
  const failed=results.filter(r=>!r.seekDeterministic||!r.finite||r.maxRodLengthError>1e-7||!r.constantHeadCarrierOffset||!r.crankNeverReverses||!r.clutchStopsOutput);
  if(!results.find(r=>r.scene==='s10-turn').headReverses)failed.push({scene:'s10-turn',reason:'Reversal not demonstrated'});
  const report={status:failed.length||errors.length?'failed':'passed',results,errors,method:'Output30fps scene-timeline samples; exact rod length220, fixed anchors, carrier offset230 on rigid yawing head, monotonic crank, clutch stop and nonsequential seek reproducibility. Turn shot must show head reversal while crank remains forward.',limits:'Illustrative linkage dimensions and slowed motions, not a real product CAD tolerance or speed. Full mounting and actual rendered frames reviewed separately; no subjective listening claimed.'};fs.writeFileSync(path.join(dir,'motion.json'),JSON.stringify(report,null,2));
  if(failed.length||errors.length)throw Error(JSON.stringify({failed,errors}));console.log(JSON.stringify({status:report.status,scenes:results.length,frames:results.reduce((n,r)=>n+r.samples,0)}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
