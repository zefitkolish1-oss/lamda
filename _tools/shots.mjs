import puppeteer from 'puppeteer-core';
const B='http://localhost:8787', OUT='/workspace/lamda/website/_shots';
const br=await puppeteer.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox','--disable-gpu']});
const errs=[], links=new Set();
async function shot(path,w,h,name,lang){
  const p=await br.newPage(); await p.setViewport({width:w,height:h,deviceScaleFactor:1,isMobile:w<500,hasTouch:w<500});
  p.on('console',m=>{if(['error','warning'].includes(m.type()))errs.push(`${name} console.${m.type()}: ${m.text()}`)});
  p.on('pageerror',e=>errs.push(`${name} pageerror: ${e.message}`));
  p.on('requestfailed',r=>errs.push(`${name} requestfailed: ${r.url()}`));
  p.on('response',r=>{if(r.status()>=400)errs.push(`${name} HTTP ${r.status()} ${r.url()}`)});
  await p.goto(B+path+(lang?'?lang='+lang:''),{waitUntil:'networkidle0'});
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}scrollTo(0,0)});
  await new Promise(r=>setTimeout(r,3800)); await p.evaluate(()=>{document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'));document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')}); await new Promise(r=>setTimeout(r,1200));
  (await p.$$eval('a[href]',as=>as.map(a=>a.href))).forEach(h=>links.add(h));
  await p.screenshot({path:`${OUT}/${name}.png`,fullPage:true});
  if(path==='/'){ await p.screenshot({path:`${OUT}/${name}_fold.png`}); }
  await p.close();
}
for(const [path,n] of [['/','home'],['/install.html','install'],['/pay.html','pay'],['/privacy.html','privacy'],['/terms.html','terms']]){
  await shot(path,390,844,`mobile_390_${n}`); await shot(path,1440,900,`desktop_1440_${n}`);
}
await shot('/',390,844,'mobile_390_home_en','en'); await shot('/',1440,900,'desktop_1440_home_en','en');
await shot('/install.html#samsung',390,844,'mobile_390_install_samsung');
const bad=[];
for(const l of links){ if(!l.startsWith(B)) continue; const u=l.split('#')[0]; const r=await fetch(u); if(r.status>=400) bad.push(r.status+' '+l); }
console.log(JSON.stringify({errors:errs,internalLinks:[...links].filter(l=>l.startsWith(B)).length,external:[...links].filter(l=>!l.startsWith(B)),broken:bad},null,1));
await br.close();
