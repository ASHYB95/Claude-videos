const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(let i=1;i<=11;i++){await p.goto('file://'+__dirname+'/frames.html#'+i);await p.reload();await p.waitForTimeout(500);
await p.screenshot({path:__dirname+'/f'+String(i).padStart(2,'0')+'.png'});}
await b.close();})();
