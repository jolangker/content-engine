const fs=require('fs'),path=require('path'),puppeteer=require('puppeteer'),{pathToFileURL}=require('url');
(async()=>{
const plan=JSON.parse(fs.readFileSync(path.join(__dirname,'timing.json'),'utf8')),dir=path.join(__dirname,'verification');fs.mkdirSync(dir,{recursive:true});
let doc='<html><head><base href="../"><script>window.__timelines={};</script><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script></head><body>';
for(const s of plan){let f=fs.readFileSync(path.join(__dirname,'compositions',s.id+'.html'),'utf8').replace(/^<template>/,'').replace(/<\/template>$/,'');f=f.replace(/<script>([\s\S]*?)<\/script>/g,(_,x)=>'<script>(function(){'+x+'})();</script>');doc+=f;}doc+='</body></html>';fs.writeFileSync(path.join(dir,'motion-inspection.html'),doc);
const browser=await puppeteer.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
try{const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(String(e)));await page.goto(pathToFileURL(path.join(dir,'motion-inspection.html')).href,{waitUntil:'networkidle0'});
const results=await page.evaluate(plan=>plan.map(s=>{
const state=t=>{window.__timelines[s.id].totalTime(t,false);const el=x=>document.getElementById(s.id+'-'+x);return {state:window['state_'+s.id]||{},leaf:el('leaf')?.getAttribute('d'),wall:el('fixedwall')?.getAttribute('transform'),wings:el('wings')?.getAttribute('transform'),spiral:el('spiral')?.getAttribute('d'),drive:el('drive')?.getAttribute('transform'),tooth:el('combtooth-0')?.getAttribute('d')};};
const a=[];for(let k=0;k<=Math.ceil(s.duration*30);k++)a.push(state(Math.min(s.duration-.001,k/30)));
const first=state(s.duration*.73);state(s.duration*.99);state(.01);const second=state(s.duration*.73);
const finite=a.every(x=>Object.values(x.state).every(v=>typeof v!=='number'||Number.isFinite(v)));
const states=new Set(a.map(x=>JSON.stringify(x))).size;
const leafFixed=a.every(x=>!x.leaf||x.leaf.startsWith('M65 230Q205 230 345 '));
const gearRatio=a.every(x=>x.state.driveAngle===undefined||Math.abs(x.state.drivenAngle+x.state.driveAngle*16/12)<1e-6);
return {scene:s.id,samples:a.length,seek_deterministic:JSON.stringify(first)===JSON.stringify(second),unique_states:states,finite,comb_root_fixed:leafFixed,gear_ratio:gearRatio,wall_fixed:a.every(x=>x.wall===null||x.wall===undefined),contact_frames:a.filter(x=>x.state.contact).length,released_frames:a.filter(x=>x.state.released).length,first:a[0],last:a.at(-1)};
}),plan);
const leafContinuity=Math.abs(results[7].last.state.bend-results[8].first.state.bend)<.2;
const governorContinuity=Math.abs(results[11].last.state.wingAngle-results[12].first.state.wingAngle)<.2;
const failed=results.filter(r=>!r.seek_deterministic||!r.finite||!r.comb_root_fixed||!r.gear_ratio||!r.wall_fixed||r.unique_states<2);
const report={results,errors,leafContinuity,governorContinuity,method:'All scene scripts sampled at output 30fps; reverse seeks, finite states, fixed tooth root, opposite gear ratio, fixed governor wall, lift/release and wing-state seam continuity. Real framework mounting independently checked by CLI snapshots.',limitations:'Numerical motion review and frame inspection; no subjective full-speed or auditory listening claimed.'};fs.writeFileSync(path.join(dir,'motion.json'),JSON.stringify(report,null,2));if(errors.length||failed.length||!leafContinuity||!governorContinuity)throw Error(JSON.stringify({errors,failed,leafContinuity,governorContinuity}));console.log(JSON.stringify({scenes:results.length,samples:results.reduce((a,x)=>a+x.samples,0),reverse_seek:true,fixed_roots_and_wall:true,gear_ratio:true,leafContinuity,governorContinuity}));
}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
