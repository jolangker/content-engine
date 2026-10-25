const fs=require('fs'),path=require('path'),http=require('http'),crypto=require('crypto'),puppeteer=require('puppeteer');
const project=__dirname;const plan=JSON.parse(fs.readFileSync(path.join(project,'scene-plan.json'),'utf8'));
const out=path.join(project,'verification','world');fs.mkdirSync(out,{recursive:true});
const mime={'.js':'text/javascript','.html':'text/html','.ttf':'font/ttf','.wav':'audio/wav','.mp3':'audio/mpeg'};
(async()=>{
 const server=http.createServer((req,res)=>{let file=path.resolve(project,'.'+decodeURIComponent(req.url.split('?')[0]));if(req.url==='/')file=path.join(project,'index.html');if(!file.startsWith(project+path.sep)||!fs.existsSync(file)){res.writeHead(404);res.end();return}res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');let data=fs.readFileSync(file);if(file.endsWith('index.html'))data=data.toString().replace('<head>','<head><script>window.__timelines={};</script>');res.end(data)});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const port=server.address().port;let browser;
 try{
  browser=await puppeteer.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',args:['--enable-webgl','--ignore-gpu-blocklist']});
  const page=await browser.newPage();await page.setViewport({width:1080,height:1920,deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(String(e)));await page.goto(`http://127.0.0.1:${port}/`,{waitUntil:'networkidle0'});await page.waitForFunction('!!window.railRenderAt');await page.evaluate(()=>document.fonts.ready);
  const proof=[];
  for(let i=0;i<plan.length;i++){
   const s=plan[i];const states=[];
   for(const u of [.08,.38,.66,.94]){
    const t=s.start+u*s.duration;
    const state=await page.evaluate(t=>{window.railRenderAt(t);return window.RAIL_STATE},t);
    await page.screenshot({path:path.join(out,`${s.id}-${Math.round(u*100)}.png`)});states.push(state);
   }
   const start=states[0].camera,end=states[3].camera;const travel=Math.hypot(...start.map((v,j)=>v-end[j]));proof.push({scene:s.id,travel_metres:travel,states});
  }
  // Compare exact same time after reverse-order unrelated seeks, including load arrow transforms.
  const tests=[];
  for(let i=0;i<plan.length;i++){
   const s=plan[i],t=s.start+.73*s.duration;
   await page.evaluate(t=>window.railRenderAt(t),t);const first=await page.screenshot();
   await page.evaluate(t=>window.railRenderAt(t),plan[plan.length-1-i].start+.1);
   await page.evaluate(t=>window.railRenderAt(t),t);const second=await page.screenshot();
   tests.push({scene:s.id,identical:crypto.createHash('sha256').update(first).digest('hex')===crypto.createHash('sha256').update(second).digest('hex')});
  }
  fs.writeFileSync(path.join(out,'report.json'),JSON.stringify({port,server_owner:'review-world.cjs',cleanup:'finally closes browser and server',camera:proof,seek_determinism:tests,errors,limitation:'Sequential sampled motion frames and exact seek comparisons; no subjective real-time visual or audio playback observed.'},null,2));
  if(errors.length||tests.some(t=>!t.identical))throw Error('World proof failure: '+JSON.stringify({errors,tests}));
  console.log(JSON.stringify({camera_shots:proof.length,deterministic:tests.every(t=>t.identical),errors,temporary_port:port}));
 }finally{if(browser)await browser.close();await new Promise(r=>server.close(r));console.log('Temporary review server closed and browser released.')}
})().catch(e=>{console.error(e);process.exitCode=1});
