const fs=require('fs'),path=require('path'),puppeteer=require('puppeteer'),{pathToFileURL}=require('url');
(async()=>{
 const plan=JSON.parse(fs.readFileSync(path.join(__dirname,'timing.json'),'utf8')),dir=path.join(__dirname,'verification');fs.mkdirSync(dir,{recursive:true});
 let doc='<html><head><base href="../"><script>window.__timelines={};</script><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script></head><body>';
 for(const s of plan){let h=fs.readFileSync(path.join(__dirname,'compositions',s.id+'.html'),'utf8').replace(/^<template>/,'').replace(/<\/template>$/,'');h=h.replace(/<script>([\s\S]*?)<\/script>/g,(_,x)=>'<script>(function(){'+x+'})();</script>');doc+=h;}doc+='</body></html>';fs.writeFileSync(path.join(dir,'motion-inspection.html'),doc);
 const browser=await puppeteer.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{
  const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(String(e)));await page.goto(pathToFileURL(path.join(dir,'motion-inspection.html')).href,{waitUntil:'networkidle0'});
  const results=await page.evaluate(plan=>plan.filter(s=>s.view!=='whole').map(s=>{
   const g=n=>document.getElementById(s.id+'-'+n),matrix=n=>g(n).transform.baseVal.consolidate()?.matrix;
   function state(t){
    window.__timelines[s.id].totalTime(t,false);const st=window['state_'+s.id];
    const p=new DOMPoint(-150,0).matrixTransform(matrix('pawl')).matrixTransform(matrix('pawl-wrap'));
    const rear=new DOMPoint(29,0).matrixTransform(matrix('pawl')).matrixTransform(matrix('pawl-wrap'));
    const base=new DOMPoint(410,400).matrixTransform(matrix('carrier')),center=new DOMPoint(517.988,271.302).matrixTransform(matrix('carrier'));
    const distance=Math.hypot(center.x-base.x,center.y-base.y);
    const forkAngle=(12.559+st.phi)*Math.PI/180,dx=rear.x-410,dy=rear.y-400;
    const forkCross=Math.abs(-dx*Math.sin(forkAngle)+dy*Math.cos(forkAngle)),forkAlong=dx*Math.cos(forkAngle)+dy*Math.sin(forkAngle);
    const tipRadius=Math.hypot(p.x-410,p.y-400),tipAngle=Math.atan2(p.y-400,p.x-410)*180/Math.PI;
    const phase=((tipAngle-st.theta-10)%20+20)%20,faceError=Math.min(phase,20-phase);
    return {state:st,tipRadius,tipAngle,faceError,meshCenterDistance:distance,forkCross,forkAlong,housing:g('housing').getAttribute('transform')};
   }
   const samples=[];for(let f=0;f<=Math.ceil(s.duration*30);f++)samples.push(state(Math.min(s.duration-.001,f/30)));
   const one=state(s.duration*.73);state(s.duration*.99);state(.001);const two=state(s.duration*.73);
   const finite=samples.every(x=>Object.values(x.state).every(v=>typeof v!=='number'||Number.isFinite(v)));
   const distance=samples.every(x=>Math.abs(x.meshCenterDistance-168)<.01);
   const mesh=samples.every(x=>Math.abs(x.state.pin-3*x.state.phi+2*x.state.theta)<1e-6);
   const fork=s.view==='explode'||samples.every(x=>x.forkCross<.02&&x.forkAlong>300&&x.forkAlong<355);
   const lock=samples.filter(x=>x.state.locked),seated=lock.every(x=>x.tipRadius>146&&x.tipRadius<165&&x.faceError<.1);
   const stopped=!['stop','roles','answer'].includes(s.view)||new Set(samples.map(x=>x.state.theta)).size===1;
   return {scene:s.id,samples:samples.length,seekDeterministic:JSON.stringify(one)===JSON.stringify(two),finite,meshCenterDistance:distance,meshEquation:mesh,forkContact:fork,seated,stopped,housingFixed:samples.every(x=>!x.housing),first:samples[0],last:samples.at(-1),maxForkError:Math.max(...samples.map(x=>x.forkCross))};
  }),plan);
  const seams=[];for(let k=6;k<13;k++){let a=results[k],b=results[k+1];seams.push({from:a.scene,to:b.scene,theta:Math.abs(a.last.state.theta-b.first.state.theta),pawl:Math.abs(a.last.state.pawl-b.first.state.pawl)});}
  const failed=results.filter(r=>!r.seekDeterministic||!r.finite||!r.meshCenterDistance||!r.meshEquation||!r.forkContact||!r.seated||!r.stopped||!r.housingFixed);
  const report={status:failed.length||errors.length?'failed':'passed',results,errors,seams,method:'All source scene timelines sampled at 30fps; DOM transform geometry checks center distance, pinion phase relation, rigid fork/rear projection contact, final pawl-tip radius and ratchet tooth-face phase, fixed frame, no reel rotation after lock and reverse seeks. Actual framework mounting separately checked by CLI snapshots.',limits:'Numerical at-output-frame motion inspection plus still sheets; no subjective full-speed viewing or auditory/phone-speaker listening claimed.'};fs.writeFileSync(path.join(dir,'motion.json'),JSON.stringify(report,null,2));
  if(failed.length||errors.length)throw Error(JSON.stringify({failed:failed.map(x=>({scene:x.scene,seated:x.seated,fork:x.forkContact,error:x.maxForkError,tip:x.last.tipRadius,face:x.last.faceError})),errors}));
  console.log(JSON.stringify({scenes:results.length,frames:results.reduce((n,x)=>n+x.samples,0),status:report.status,seams}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
