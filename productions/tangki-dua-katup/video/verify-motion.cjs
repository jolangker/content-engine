const fs=require('fs'),path=require('path'),puppeteer=require('puppeteer'),{pathToFileURL}=require('url');
const V=__dirname,plan=JSON.parse(fs.readFileSync(path.join(V,'timing.json'),'utf8'));
(async()=>{
 let doc=fs.readFileSync(path.join(V,'index.html'),'utf8');
 doc=doc.replace('<head>','<head><base href="../"><script>window.__timelines={};</script>');
 for(const s of plan){const body=fs.readFileSync(path.join(V,'compositions/frames',s.id+'.html'),'utf8').replace(/^<template>/,'').replace(/<\/template>$/,'').replaceAll('../../assets/fonts/','assets/fonts/');doc=doc.replace(new RegExp('<div id="slot-'+s.id+'"[^>]*></div>'),'<div id="slot-'+s.id+'" style="position:absolute;inset:0">'+body+'</div>');}
 fs.writeFileSync(path.join(V,'verification/motion-inspection.html'),doc);
 const browser=await puppeteer.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{
  const page=await browser.newPage();await page.setViewport({width:1080,height:1920,deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(pathToFileURL(path.join(V,'verification/motion-inspection.html')).href,{waitUntil:'networkidle0'});await page.evaluate(()=>document.fonts.ready);
  const results=await page.evaluate(plan=>{
   const state=(sid,t)=>{window.__timelines[sid].totalTime(t,false);const a=n=>document.getElementById(sid+'-'+n);return {water:a('water').getAttribute('transform'),float:a('float').getAttribute('transform'),flapper:a('flapper').getAttribute('transform'),lever:a('lever').getAttribute('transform'),chain:a('chain').getAttribute('d'),chainLength:a('chain').getTotalLength(),fill:+a('fill-flow').getAttribute('opacity'),flush:+a('flush-flow').getAttribute('opacity')};};
   return plan.map(s=>{const samples=[];for(let j=0;j<=100;j++)samples.push(state(s.id,s.duration*j/100));const t=s.duration*.73;const first=state(s.id,t);state(s.id,s.duration*.99);state(s.id,.01);const second=state(s.id,t);return {scene:s.id,samples:101,chain_length_min:Math.min(...samples.map(x=>x.chainLength)),chain_length_max:Math.max(...samples.map(x=>x.chainLength)),seek_deterministic:JSON.stringify(first)===JSON.stringify(second),first:samples[0],last:samples.at(-1),mechanism_changes:new Set(samples.map(x=>JSON.stringify(x))).size};});
  },plan);
  fs.writeFileSync(path.join(V,'verification/motion.json'),JSON.stringify({results,errors,method:'101 samples per scene through actual frame GSAP scripts; same-time reverse-seek state comparison; flattened local inspection document. Framework mount independently checked by CLI and snapshots.',limitation:'No subjective continuous audiovisual listening established.'},null,2));
  if(errors.length||results.some(r=>!r.seek_deterministic||r.chain_length_min<489||r.chain_length_max>491))throw Error(JSON.stringify({errors,failed:results.filter(r=>!r.seek_deterministic||r.chain_length_min<489||r.chain_length_max>491)}));
  console.log(JSON.stringify({scenes:results.length,samples:1616,seek_deterministic:true,chain_length_passed:true,errors}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
