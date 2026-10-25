const fs=require('fs'),path=require('path'),puppeteer=require('puppeteer'),{pathToFileURL}=require('url');
(async()=>{
const plan=JSON.parse(fs.readFileSync(path.join(__dirname,'timing.json'),'utf8')),dir=path.join(__dirname,'verification');fs.mkdirSync(dir,{recursive:true});
let doc='<html><head><base href="../"><script>window.__timelines={};</script><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script></head><body>';
for(const s of plan){let f=fs.readFileSync(path.join(__dirname,'compositions',s.id+'.html'),'utf8').replace(/^<template>/,'').replace(/<\/template>$/,'');f=f.replace(/<script>([\s\S]*?)<\/script>/g,(_,x)=>'<script>(function(){'+x+'})();</script>');doc+=f;}doc+='</body></html>';fs.writeFileSync(path.join(dir,'motion-inspection.html'),doc);
const browser=await puppeteer.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
try{const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(String(e)));await page.goto(pathToFileURL(path.join(dir,'motion-inspection.html')).href,{waitUntil:'networkidle0'});
const results=await page.evaluate(plan=>plan.map(s=>{
const state=t=>{window.__timelines[s.id].totalTime(t,false);const el=x=>document.getElementById(s.id+'-'+x);return {state:Object.fromEntries(Object.entries(window['state_'+s.id]).filter(([k,v])=>typeof v==='number')),blade:el('blade')?.getAttribute('transform'),cover:el('cover')?.getAttribute('transform'),anvil:el('anvil')?.getAttribute('transform'),staple:el('staple')?.getAttribute('d'),length:el('staple')?.getTotalLength(),follower:el('follower')?.getAttribute('transform'),wire:el('wire')?.getAttribute('transform')};};
const a=[];for(let k=0;k<=Math.ceil(s.duration*30);k++)a.push(state(Math.min(s.duration-.001,k/30)));
const first=state(s.duration*.73);state(s.duration*.99);state(.01);const second=state(s.duration*.73);const lengths=a.map(x=>x.length).filter(x=>x!==undefined);
return {scene:s.id,samples:a.length,seek_deterministic:JSON.stringify(first)===JSON.stringify(second),unique_states:new Set(a.map(x=>JSON.stringify(x))).size,anvil_fixed:new Set(a.map(x=>x.anvil)).size===1,wire_length_min:lengths.length?Math.min(...lengths):null,wire_length_max:lengths.length?Math.max(...lengths):null,first:a[0],last:a.at(-1)};
}),plan);
const failed=results.filter(r=>!r.seek_deterministic||!r.anvil_fixed||(r.wire_length_min&&r.wire_length_max-r.wire_length_min>.5));
const report={results,errors,method:'All scene GSAP scripts sampled at output 30 fps; reverse-seek equality, stationary-anvil and wire-centerline-length checks. Framework mount separately checked by CLI snapshots.',limitations:'Numerical temporal review, not subjective full-speed viewing or auditory listening.'};fs.writeFileSync(path.join(dir,'motion.json'),JSON.stringify(report,null,2));if(errors.length||failed.length)throw Error(JSON.stringify({errors,failed}));console.log(JSON.stringify({scenes:results.length,samples:results.reduce((a,x)=>a+x.samples,0),seek_deterministic:true,anvil_fixed:true,wire_length_pass:true}));
}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
