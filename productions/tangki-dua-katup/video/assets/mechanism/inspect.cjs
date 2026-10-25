const {chromium}=require('C:/Users/muhth/AppData/Local/npm-cache/_npx/86170c4cd1c5da32/node_modules/playwright');
const {pathToFileURL}=require('url');
const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});try{const p=await b.newPage({viewport:{width:900,height:1050},deviceScaleFactor:1});await p.goto(pathToFileURL(path.join(__dirname,'inspection.html')).href);await p.screenshot({path:path.join(__dirname,'inspection.png')});}finally{await b.close();}})();
