const {chromium}=require('playwright');
const D=process.argv[2];
const jobs=[
 ['si','https://www.si.com/more-sports/2015/12/17/candace-hill-turns-professional-signs-asics-fastest-high-school-sprinter',[null,'signed a 10-year professional sponsorship contract']],
 ['cr','https://runningmagazine.ca/uncategorized/asics-signs-candace-hill-to-youngest-pro-deal-in-u-s-track-and-field/',[null]],
 ['wwd','https://wwd.com/footwear-news/shoe-industry-news/asics-signs-fastest-girl-in-the-world-in-multi-year-deal-1238703877/',[null,'10-year deal with the brand through 2025']],
 ['ms','https://www.milesplit.com/articles/167267/16-year-old-candace-hill-turns-pro',[null,'with no deductions']],
 ['wa','https://worldathletics.org/personal-best/performance/candace-hill-mental-health-awareness-month',[null,'you made the wrong decision','therapist']],
 ['rbr','https://www.runblogrun.com/2023/03/candace-hill-speaks-i-want-prs-at-the-100-meters-and-200-meters-in-2023-the-runblogrun-interview-march-2023.html',[null,'years left','I want to PR']],
];
(async()=>{const b=await chromium.launch();
for(const [k,u,phr] of jobs){
 const p=await b.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1.5});
 try{await p.goto(u,{waitUntil:'domcontentloaded',timeout:45000});await p.waitForTimeout(3500);
  for(const sel of ['text=Allow all cookies','text=Accept All','text=Show Full Article','button:has-text("Accept")']){try{await p.click(sel,{timeout:1500});await p.waitForTimeout(800);}catch(e){}}
  await p.addStyleTag({content:'[class*=cookie],[id*=cookie],[class*=consent],[id*=consent],[class*=banner],[id*=onetrust],iframe,[class*=ad-],[id*=ad-]{display:none!important}'});
  for(let i=0;i<phr.length;i++){const ph=phr[i];
   if(ph===null){await p.evaluate(()=>window.scrollTo(0,0));await p.waitForTimeout(400);
     const h=await p.$('h1'); if(h){await h.evaluate(e=>e.scrollIntoView({block:'center'}));await p.evaluate(()=>window.scrollBy(0,180));}
     await p.waitForTimeout(500);await p.screenshot({path:`${D}/${k}_0.png`});console.log(k,0,'ok');continue;}
   const found=await p.evaluate((ph)=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
     while(n=w.nextNode()){const i=n.nodeValue.toLowerCase().indexOf(ph.toLowerCase());if(i>=0){
       const r=document.createRange();r.setStart(n,i);r.setEnd(n,i+ph.length);const m=document.createElement('mark');
       m.style.cssText='background:rgba(255,40,40,.18);outline:5px solid #e8202a;outline-offset:4px;border-radius:3px;color:inherit';
       r.surroundContents(m);m.scrollIntoView({block:'center'});return true;}}return false;},ph);
   await p.waitForTimeout(600);await p.screenshot({path:`${D}/${k}_${i}.png`});console.log(k,i,found?'ok':'NOTFOUND');}
 }catch(e){console.log(k,'ERR',e.message.slice(0,120));}
 await p.close();}
await b.close();})();
