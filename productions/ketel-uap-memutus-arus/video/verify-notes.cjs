const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url'),puppeteer=require('puppeteer');
(async()=>{
 const V=__dirname,plan=JSON.parse(fs.readFileSync(path.join(V,'timing.json'),'utf8')).scenes;
 let html='<html><head><base href="../../"></head><body>';
 for(const s of plan)html+=fs.readFileSync(path.join(V,'compositions',s.id+'.html'),'utf8').replace(/^<template>/,'').replace(/<\/template>$/,'').replace(/<script>[\s\S]*?<\/script>/g,'');
 html+='</body></html>';const file=path.join(V,'.hyperframes/artifacts/note-measure.html');fs.writeFileSync(file,html);
 const b=await puppeteer.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 try{const p=await b.newPage();await p.setViewport({width:1080,height:1920});await p.goto(pathToFileURL(file).href,{waitUntil:'networkidle0'});await p.evaluate(()=>document.fonts.ready);
  const notes=await p.evaluate(()=>[...document.querySelectorAll('.note')].map(e=>{let r=e.getBoundingClientRect();return {text:e.textContent,top:r.top,bottom:r.bottom,height:r.height,clearance:1500-r.bottom,fits:r.top>=1410&&r.height<=28.1&&r.bottom<=1440};}));
  const report={status:notes.length===16&&notes.every(x=>x.fits)?'passed':'failed',notes};fs.writeFileSync(path.join(V,'verification/notes.json'),JSON.stringify(report,null,2));if(report.status!=='passed')throw Error(JSON.stringify(notes.filter(x=>!x.fits)));console.log(JSON.stringify({status:'passed',notes:16,minimumCaptionClearance:Math.min(...notes.map(x=>x.clearance))}));
 }finally{await b.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
