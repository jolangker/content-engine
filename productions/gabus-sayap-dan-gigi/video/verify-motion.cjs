const fs=require('fs'),path=require('path'),puppeteer=require('puppeteer'),{pathToFileURL}=require('url');
(async()=>{
 const V=__dirname,plan=JSON.parse(fs.readFileSync(path.join(V,'timing.json'),'utf8')).scenes,Q=path.join(V,'verification');fs.mkdirSync(Q,{recursive:true});
 let doc='<html><head><meta charset="utf-8"><base href="../../"><script>window.__timelines={};</script><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script></head><body>';
 for(const s of plan){let h=fs.readFileSync(path.join(V,'compositions',s.id+'.html'),'utf8').replace(/^<template>/,'').replace(/<\/template>$/,'');h=h.replace(/<script>([\s\S]*?)<\/script>/g,(_,x)=>'<script>(function(){'+x+'})();</script>');doc+=h;}
 const file=path.join(V,'.hyperframes/artifacts/mechanism-inspection.html');fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,doc+'</body></html>');
 const browser=await puppeteer.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{
  const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(String(e)));await page.goto(pathToFileURL(file).href,{waitUntil:'networkidle0'});
  const results=await page.evaluate(plan=>plan.map(s=>{
   const sample=t=>{window.__timelines[s.id].totalTime(t,false);return JSON.parse(JSON.stringify(window.__mechanismStates[s.id]));};
   const samples=[];for(let f=1;f<Math.round(s.duration*30);f++)samples.push(sample(f/30));
   const a=sample(s.duration*.713);sample(s.duration*.99);sample(.001);const b=sample(s.duration*.713);
   const domCork=document.getElementById(s.id+'-cork');
   return {scene:s.id,frames:samples.length,seekDeterministic:JSON.stringify(a)===JSON.stringify(b),finite:samples.every(x=>Object.values(x).every(v=>Number.isFinite(v))),
    coupledSectors:samples.every(x=>Math.abs(x.leftAngle+x.rightAngle)<1e-7&&Math.abs(x.d-x.q*64)<1e-7),
    fixedInsertionCork:!['turn','grip','guide','rise'].includes(s.key)||samples.every(x=>x.cork===0&&Math.abs(x.phase-x.d/30*2*Math.PI)<1e-7),
    rigidExtraction:!['drive','lever','reaction','lift','clear','proof'].includes(s.key)||samples.every(x=>Math.abs(x.cork-x.d+88.96)<1e-7&&Math.abs(x.phase-88.96/30*2*Math.PI)<1e-7),
    corkTransformOnPart:domCork.tagName.toLowerCase()==='g'&&domCork.hasAttribute('transform'),
    bounds:samples.every(x=>x.q>=-.35-1e-8&&x.q<=1.39+1e-8),finalClearance:!['clear','proof'].includes(s.key)||590-(680+sample(s.duration*.99).cork)>20,poses:[.05,.33,.67,.95].map(q=>sample(q*s.duration))};
  }),plan);
  const continuity=await page.evaluate(plan=>[['turn','grip'],['grip','guide'],['guide','rise'],['rise','rings'],['rings','pivot'],['pivot','drive'],['drive','lever'],['lever','reaction'],['reaction','lift'],['lift','clear']].map(([a,b])=>{
   const x=plan.find(s=>s.key===a),y=plan.find(s=>s.key===b);window.__timelines[x.id].totalTime(x.duration,false);const p={...window.__mechanismStates[x.id]};window.__timelines[y.id].totalTime(.00001,false);const q=window.__mechanismStates[y.id];return {from:a,to:b,passed:['q','phase','cork'].every(k=>Math.abs(p[k]-q[k])<1e-6)};
  }),plan);
  const bools=['seekDeterministic','finite','coupledSectors','fixedInsertionCork','rigidExtraction','corkTransformOnPart','bounds','finalClearance'];
  const failed=results.filter(r=>bools.some(k=>!r[k]));
  const report={status:failed.length||errors.length||continuity.some(x=>!x.passed)?'failed':'passed',method:'Every30fps output frame plus reverse seeks: sector/rack pitch relation, fixed cork insertion, rigid worm/cork extraction and sequential pose continuity.',results,errors,continuity,limits:'Analytic state and DOM transforms, not a physical simulation, tooth tolerance or perceptual playback. Source-defined relationships; original geometry not to scale.'};fs.writeFileSync(path.join(Q,'motion.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify({status:report.status,scenes:results.length,frames:results.reduce((n,r)=>n+r.frames,0),failed:failed.map(x=>x.scene),continuity:continuity.filter(x=>!x.passed),errors}));if(report.status!=='passed')process.exitCode=1;
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
