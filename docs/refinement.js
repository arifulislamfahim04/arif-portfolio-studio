(()=>{'use strict';
const reduced=matchMedia('(prefers-reduced-motion: reduce)'),fine=matchMedia('(hover:hover) and (pointer:fine)'),$=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const mobile=matchMedia('(max-width:800px)'),utilities=$('.tx-utilities'),dock=$('.tx-dock'),header=$('.tx-header');
function placeControls(){if(mobile.matches){header.append(utilities)}else{dock.prepend(utilities)}}placeControls();mobile.addEventListener('change',placeControls);
const targets=$$('[data-refine-reveal]');
if(!reduced.matches)document.documentElement.classList.add('rf-ready');
// Stagger sibling cards without creating a long waterfall on mobile.
$$('.personal-info dl,.stats-grid,.capability-grid,.resume-project-grid,.award-grid,.testimonial-grid').forEach(group=>[...group.children].forEach((el,i)=>el.style.setProperty('--reveal-stagger',(i%3)*80+'ms')));
const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('rf-in');observer.unobserve(e.target)}}),{threshold:.08,rootMargin:'0px 0px -32px 0px'});targets.forEach(el=>{if(reduced.matches)el.classList.add('rf-in');else observer.observe(el)});
// Copy is a distinct control so the email and telephone links keep their native action.
$$('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{try{if(navigator.clipboard?.writeText){await navigator.clipboard.writeText(button.dataset.copy)}else{const field=document.createElement('textarea');field.value=button.dataset.copy;field.style.cssText='position:fixed;left:0;top:0;opacity:0;pointer-events:none';document.body.append(field);field.select();const copied=document.execCommand('copy');field.remove();button.focus();if(!copied)throw new Error('Clipboard unavailable')}button.classList.add('is-copied');$('.rf-copy-status',button).textContent='Copied!';$('use',button).setAttribute('href','#icon-check');$('#rf-copy-announcement').textContent='Copied '+button.dataset.copy;setTimeout(()=>{button.classList.remove('is-copied');$('.rf-copy-status',button).textContent='Copy';$('use',button).setAttribute('href','#icon-copy')},2200)}catch{$('.rf-copy-status',button).textContent='Select to copy';$('#rf-copy-announcement').textContent='Clipboard unavailable. You can select and copy the address.'}}));
const ghosts=$$('.rf-ghost'),timelines=$$('.rf-timeline');let scheduled=false;
function scrollEffects(){scheduled=false;timelines.forEach(el=>{const r=el.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)return;const progress=Math.min(1,Math.max(0,(innerHeight*.75-r.top)/(r.height*.85)));el.style.setProperty('--stitch-progress',reduced.matches?1:progress)});if(!reduced.matches)ghosts.forEach(el=>{const r=el.getBoundingClientRect();if(r.bottom>-80&&r.top<innerHeight+80)el.style.setProperty('--ghost-y',Math.max(-10,Math.min(10,(innerHeight*.45-r.top)*.025))+'px')})}
addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(scrollEffects)}},{passive:true});addEventListener('resize',scrollEffects);scrollEffects();
ghosts.forEach(el=>{el.addEventListener('pointermove',e=>{if(reduced.matches||!fine.matches)return;const r=el.getBoundingClientRect();el.style.setProperty('--ghost-x',((e.clientX-r.left)/r.width-.5)*10+'px')});el.addEventListener('pointerleave',()=>el.style.setProperty('--ghost-x','0px'))});
// Existing hero code initializes all data-tilt and magnetic controls, including new About cards.
// Detail dialog text and all existing sections inherit the same tokens and surface primitives.
})();
