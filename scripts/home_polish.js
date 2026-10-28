(()=>{'use strict';
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)],motion=matchMedia('(prefers-reduced-motion: reduce)'),clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
const stage=$('.physical-stage'),card=$('.physical-stage .tag-carrier'),grip=$('.physical-stage .tag-grip');
if(stage&&card&&grip){
 let x=0,y=0,vx=0,vy=0,angle=-2,vr=0,tx=0,ty=0,drag=null,keyboard=false,visible=false,raf=0,last=0,hoverX=0,hoverY=0;
 function bounds(px,py){const r=stage.getBoundingClientRect(),w=card.offsetWidth;return [clamp(px,16-r.left,Math.max(16-r.left,innerWidth-r.left-w-16)),clamp(py,-28,Math.max(0,innerHeight-r.top-170))]}
 function paint(){const length=Math.hypot(x,65+y);stage.style.setProperty('--card-x',x.toFixed(2)+'px');stage.style.setProperty('--card-y',y.toFixed(2)+'px');stage.style.setProperty('--card-r',angle.toFixed(2)+'deg');stage.style.setProperty('--cord-angle',(-Math.atan2(x,65+y)*180/Math.PI).toFixed(2)+'deg');stage.style.setProperty('--cord-scale',(length/65).toFixed(3))}
 function frame(now){raf=0;if(!visible||document.hidden)return;const dt=Math.min((now-(last||now-16))/1000,.04);last=now;
  const idle=now/1000;const targetX=drag||keyboard?tx:hoverX+Math.sin(idle*.8)*2.2,targetY=drag||keyboard?ty:hoverY;
  if(motion.matches){x=drag||keyboard?tx:0;y=drag||keyboard?ty:0;angle=0;vx=vy=vr=0;paint();return}
  // Fixed substeps keep the damped spring stable after a slow frame. Mass = 1.8.
  const n=Math.ceil(dt/.008),step=dt/n,k=drag?110:18,c=drag?23:5.4;
  for(let i=0;i<n;i++){vx+=((targetX-x)*k-c*vx)*step;vy+=((targetY-y)*k-c*vy)*step;x+=vx*step;y+=vy*step;const targetAngle=clamp(-2-x*.028+vx*.035+Math.sin(idle*.8)*.65,-24,24);vr+=((targetAngle-angle)*22-vr*6)*step;angle+=vr*step}
  const bounded=bounds(x,y);if(bounded[0]!==x){x=bounded[0];vx*=.2}if(bounded[1]!==y){y=bounded[1];vy*=.2}paint();raf=requestAnimationFrame(frame)
 }
 function start(){if(!raf&&visible&&!document.hidden){last=0;raf=requestAnimationFrame(frame)}}
 function release(){drag=null;keyboard=false;tx=ty=0;card.classList.remove('dragging');start()}
 card.addEventListener('pointerdown',e=>{if(e.button!==0||(e.pointerType!=='mouse'&&!e.target.closest('.tag-grip')))return;drag={id:e.pointerId,cx:e.clientX,cy:e.clientY,x,y};keyboard=false;hoverX=hoverY=0;card.setPointerCapture(e.pointerId);card.classList.add('dragging');e.preventDefault();start()});
 card.addEventListener('pointermove',e=>{if(drag&&drag.id===e.pointerId){[tx,ty]=bounds(drag.x+e.clientX-drag.cx,drag.y+e.clientY-drag.cy);if(motion.matches){x=tx;y=ty;paint()}start()}else if(e.pointerType==='mouse'&&!motion.matches){const r=card.getBoundingClientRect(),dx=(e.clientX-r.left)/r.width-.5,dy=(e.clientY-r.top)/r.height-.5;hoverX=dx*9;hoverY=dy*3;stage.style.setProperty('--foil-x',dx*100+'px');stage.style.setProperty('--foil-y',dy*80+'px')}});
 card.addEventListener('pointerleave',()=>{hoverX=hoverY=0;stage.style.setProperty('--foil-x','0px');stage.style.setProperty('--foil-y','0px')});
 for(const event of ['pointerup','pointercancel','lostpointercapture'])card.addEventListener(event,release);
 grip.addEventListener('keydown',e=>{const d={ArrowLeft:[-40,0],ArrowRight:[40,0],ArrowUp:[0,-40],ArrowDown:[0,40]}[e.key];if(d){e.preventDefault();keyboard=true;[tx,ty]=bounds(tx+d[0],ty+d[1]);start()}else if(e.key==='Escape'||e.key==='Enter'){e.preventDefault();release()}});grip.addEventListener('blur',release);
 new IntersectionObserver(es=>{visible=es[0].isIntersecting;stage.classList.toggle('is-moving',visible&&!motion.matches);if(visible)start();else{cancelAnimationFrame(raf);raf=0;release()}},{threshold:0}).observe(stage);
 document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(raf);raf=0;release()}else start()});motion.addEventListener('change',()=>{release();start()});addEventListener('resize',()=>{[x,y]=bounds(x,y);[tx,ty]=bounds(tx,ty);paint()});paint();
}
const backdrop=$('.hero-backdrop img');
if(backdrop){let queued=false,inView=false;function parallax(){queued=false;if(inView&&!motion.matches)backdrop.style.transform='translate3d(0,'+clamp(-$('.home-stage').getBoundingClientRect().top*.045,-24,24)+'px,0) scale(1.06)';else backdrop.style.transform='none'}new IntersectionObserver(es=>{inView=es[0].isIntersecting;parallax()}).observe(backdrop);addEventListener('scroll',()=>{if(inView&&!queued&&!motion.matches){queued=true;requestAnimationFrame(parallax)}},{passive:true});motion.addEventListener('change',parallax)}
const nameText=$('[data-type="name"]'),headlineText=$('[data-type="headline"]'),roleText=$('[data-type="roles"]');
if(nameText&&headlineText){const words=JSON.parse($('.role-line')?.dataset.roles||'[]'),original=[nameText.textContent,headlineText.textContent];let timer=0,phase=0,letter=0,role=0,deleting=false,active=true;
 function finalText(){clearTimeout(timer);nameText.textContent=original[0];headlineText.textContent=original[1];if(roleText)roleText.textContent=words[0]||'';$$('.typing').forEach(e=>e.classList.remove('typing'))}
 function tick(){clearTimeout(timer);if(motion.matches){finalText();return}if(!active||document.hidden)return;const el=phase===0?nameText:phase===1?headlineText:roleText;if(!el)return;const full=phase<2?original[phase]:words[role];$$('.typing').forEach(e=>e.classList.remove('typing'));el.classList.add('typing');letter+=deleting?-1:1;el.textContent=full.slice(0,Math.max(0,letter));let delay=phase===1?25:65;
  if(!deleting&&letter>=full.length){if(phase<2){phase++;letter=0;delay=450;if(phase===2&&!words.length){el.classList.remove('typing');return}}else{deleting=true;delay=2300}}else if(deleting&&letter<=0){deleting=false;role=(role+1)%words.length;delay=300}else if(deleting)delay=32;timer=setTimeout(tick,delay)
 }
 if(!motion.matches){nameText.textContent='';headlineText.textContent='';if(roleText)roleText.textContent='';tick()}
 new IntersectionObserver(es=>{active=es[0].isIntersecting;if(active&&!motion.matches)tick();else clearTimeout(timer)}).observe($('#home-title'));
 document.addEventListener('visibilitychange',()=>{if(document.hidden)clearTimeout(timer);else if(active&&!motion.matches)tick()});motion.addEventListener('change',()=>{if(motion.matches)finalText();else if(active)tick()})
}
})();
