const {chromium}=require('playwright');
const D=process.argv[2];
const jobs=[
 ['cr','https://runningmagazine.ca/uncategorized/asics-signs-candace-hill-to-youngest-pro-deal-in-u-s-track-and-field/',['youngest to sign pro deal']],
 ['wwd','https://wwd.com/footwear-news/shoe-industry-news/asics-signs-fastest-girl-in-the-world-in-multi-year-deal-1238703877/',['10-year deal with the brand through 2025']],
 ['rbr','https://www.runblogrun.com/2023/03/candace-hill-speaks-i-want-prs-at-the-100-meters-and-200-meters-in-2023-the-runblogrun-interview-march-2023.html',['has not run a PB in four years','three more years with her ASICS contract']],
];
(async()=>{const b=await chromium.launch();
for(const [k,u,phr] of jobs){
 const p=await b.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1.5});
 try{await p.goto(u,{waitUntil:'domcontentloaded',timeout:45000});await p.waitForTimeout(3500);
  for(const sel of ['text=Allow all cookies','text=Accept All','button:has-text("Accept")']){try{await p.click(sel,{timeout:1500});await p.waitForTimeout(800);}catch(e){}}
  for(let i=0;i<phr.length;i++){const ph=phr[i];
   const found=await p.evaluate((ph)=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
     while(n=w.nextNode()){const i=n.nodeValue.toLowerCase().indexOf(ph.toLowerCase());if(i>=0){
       const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+ph.length);const m=document.createElement('mark');
       m.style.cssText='background:rgba(255,40,40,.18);outline:5px solid #e8202a;outline-offset:4px;border-radius:3px;color:inherit';
       r.surroundContents(m);m.scrollIntoView({block:'center'});return true;}}return false;},ph);
   await p.waitForTimeout(700);
   await p.evaluate(()=>{for(const e of document.querySelectorAll('body *')){const c=getComputedStyle(e);if(c.position==='fixed'||c.position==='sticky'){e.style.display='none';}}});
   await p.screenshot({path:`${D}/${k}_h${i}.png`});console.log(k,i,found?'ok':'NOTFOUND');}
 }catch(e){console.log(k,'ERR',e.message.slice(0,120));}
 await p.close();}
await b.close();})();
