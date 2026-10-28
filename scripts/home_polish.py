"""Scoped homepage presentation layer; original templates and other routes stay intact."""
from lxml import html, etree
import json
from datetime import date
from copy import deepcopy

def polish(pages, profile, settings, updates, *, root, esc, url, rich, one, select, set_html):
 h=pages['index'];body=one(h,'//body');body.set('data-home-polish','true')
 def add(parent,s):parent.append(html.fragment_fromstring(s))
 def icon(name):return f'<svg class="icon" viewBox="0 0 16 16" aria-hidden="true"><use href="#i-{name}"></use></svg>'
 def erase(e):e.getparent().remove(e)
 # Keep layout and content decisions in the build, rather than brittle runtime replacements.
 socials=one(h,'//div[@class="home-socials"]');set_html(socials,'<a class="connect-label" href="contact.html">Connect with me</a>')
 links=[('linkedin',profile.get('linkedin'),'LinkedIn'),('contact','mailto:'+profile.get('email',''),'Email '+profile['name'])]
 facebook=profile.get('facebook') or next((v.get('url') for v in profile.get('social_links',[]) if 'facebook' in str(v).lower()),None)
 if facebook:links.append(('facebook',facebook,'Facebook'))
 for glyph,href,label in links:
  if url(href):add(socials,f'<a class="round-control" href="{esc(url(href))}" aria-label="{esc(label)}">{icon(glyph)}</a>')
 for a in select(h,'//div[@class="hero-actions"]/a'):a.attrib.pop('data-magnetic',None)
 for a in select(h,'//a[contains(@class,"cta-link")]'):a.set('href','contact.html')
 one(h,'//div[contains(@class,"identity-caption")]/h2').set('title',profile['name'])
 # A separate stage opts out of the old, tightly clamped physics implementation.
 stage=one(h,'//div[@class="tag-stage"]');stage.set('class','physical-stage')
 one(stage,'.//span[@class="tag-hint"]').text='GRAB THE CLIP · PULL A LITTLE FURTHER'
 grip=one(stage,'.//button[@class="tag-grip"]');grip.set('aria-label','Move portrait card. Drag the clip, or use arrow keys. Escape returns it.')
 photo=one(stage,'.//div[@class="identity-photo"]');add(photo,'<span class="photo-foil" aria-hidden="true"></span>')
 for img in select(photo,'.//img'):
  img.set('width','600');img.set('height','750');img.set('loading','eager');img.set('decoding','async');img.set('fetchpriority','high')
 # Full text is server rendered; reserve layers give typing the final layout from frame one.
 title=one(h,'//*[@id="home-title"]');name=(settings.get('preferred_name') or 'Ariful').upper()+'.';headline=settings.get('headline') or 'Textile engineering, with a practical mind.'
 def typed(key,text):return f'<span class="typed-line"><span class="typed-reserve" aria-hidden="true">{esc(text)}</span><span class="typed-live" data-type="{key}">{esc(text)}</span></span>'
 set_html(title,typed('name',name)+typed('headline',headline));title.set('aria-label',name+' '+headline)
 roles=[str(v).strip() for v in settings.get('roles',[]) if str(v).strip()][:12]
 if roles:
  reserve=''.join('<span class="role-reserve" aria-hidden="true">'+esc(v)+'</span>' for v in roles)
  title.addnext(html.fragment_fromstring('<div class="role-line" data-roles="'+esc(__import__('json').dumps(roles))+'"><span class="sr-only">Exploring '+esc(', '.join(roles))+'</span>'+reserve+'<span class="typed-live" data-type="roles" aria-hidden="true">'+esc(roles[0])+'</span></div>'))
 background=url(settings.get('background_image'))
 if background:
  small=url(settings.get('background_image_small'));sources=f' srcset="{esc(small)} 640w, {esc(background)} 1280w" sizes="100vw"' if small else ''
  stage=one(h,'//div[@class="home-stage"]');stage.insert(0,html.fragment_fromstring(f'<div class="hero-backdrop" aria-hidden="true"><img src="{esc(background)}"{sources} alt="" width="1280" height="853" decoding="async" fetchpriority="low"></div>'))
 # Two independently looping rows; the original single track remains the accessible slideshow.
 for showcase in select(h,'//div[@class="moments-carousel"]'):
  showcase.set('class','moments-showcase is-slideshow');showcase.set('data-default-mode',settings.get('gallery_mode') or 'Marquee')
  track=one(showcase,'.//div[@class="moments-track"]');track.set('class','slideshow-track');track.set('aria-label','Photo slideshow. Use left and right arrow keys or the previous and next buttons.')
  slides=list(track);wall=html.Element('div',{'class':'marquee-wall','aria-hidden':'true','hidden':''})
  for row in range(2):
   viewport=etree.SubElement(wall,'div',{'class':'marquee-row'});belt=etree.SubElement(viewport,'div',{'class':'marquee-belt'})
   selected=slides[row::2] or slides
   # At least three cells per group, even with a small personal collection.
   while len(selected)<3:selected=selected+selected
   for repeat in range(2):
    group=etree.SubElement(belt,'div',{'class':'marquee-group'})
    for original in selected:
     clone=deepcopy(original)
     for button in clone.xpath('.//button'):button.set('tabindex','-1')
     group.append(clone)
  showcase.insert(0,wall)
  controls=one(showcase,'.//div[@class="moments-controls"]');set_html(controls,f'<button class="gallery-mode" data-gallery-mode aria-pressed="true">Slideshow</button><button class="gallery-pause" data-gallery-pause aria-pressed="false">Pause motion</button><div class="slideshow-controls"><button class="round-control" data-slide-prev aria-label="Previous moments">{icon("left")}</button><span class="slide-position" role="status"></span><button class="round-control" data-slide-next aria-label="Next moments">{icon("right")}</button></div>')
  add(controls,'<span class="gallery-mode-help">Switch to Slideshow to browse with a keyboard or swipe.</span>')
 # A dated feed replaces the old generic overview cards on the homepage only.
 topics=['Content creation','Research','Fabric testing','Apparel manufacturing'];items=sorted(updates,key=lambda u:str(u.get('date') or ''),reverse=True)
 chips=''.join(f'<button class="update-filter" data-update-filter="{esc(t)}" aria-pressed="{str(i==0).lower()}">{esc(t)}</button>' for i,t in enumerate(['All']+topics))
 cards=[]
 for i,u in enumerate(items):
  raw=str(u.get('date') or '')[:10]
  try:label=date.fromisoformat(raw).strftime('%d %b %Y').lstrip('0')
  except ValueError:label=raw or 'Date to be announced'
  sample='<span class="update-sample">Sample update</span>' if u.get('sample') else ''
  picture=f'<img class="update-photo" src="{esc(url(u["image"]))}" alt="{esc(u.get("image_alt") or u["title"])}" loading="lazy" width="320" height="200">' if url(u.get('image')) else ''
  link=f'<a class="text-link" href="{esc(url(u["link"]))}">Read more<span class="sr-only">: {esc(u["title"])}</span> {icon("arrow")}</a>' if url(u.get('link')) else ''
  cards.append(f'<article class="update-entry" data-update-topic="{esc(u.get("topic") or topics[0])}"{(" hidden" if i>=3 else "")}><div class="update-date"><time datetime="{esc(raw)}">{esc(label)}</time>{sample}</div><div class="update-copy"><span class="update-topic">{esc(u.get("topic"))}</span><h3>{esc(u["title"])}</h3><p>On {esc(label)}, '+('this example illustrates how a new update will appear.' if u.get('sample') else esc(u.get('text')))+f'</p>{("<p>"+esc(u.get("text"))+"</p>" if u.get("sample") else "")}{link}</div>{picture}</article>')
 markup='<section class="section updates-section" id="updates" aria-labelledby="updates-title"><header class="section-heading"><span class="section-label">THE LATEST THREADS</span><h2 id="updates-title">'+esc(settings.get('updates_heading') or 'A few threads in progress.')+'</h2><p>'+esc(settings.get('updates_intro'))+'</p></header><div class="update-filters" role="group" aria-label="Filter updates by topic">'+chips+'</div><div class="updates-feed">'+''.join(cards)+'</div><p class="updates-empty"'+(' hidden' if cards else '')+'>No updates here yet. There will be more to share soon.</p><p class="updates-count" role="status">'+str(min(3,len(cards)))+' latest updates</p></section>'
 old=one(h,'//main//section[contains(@class,"section") and not(contains(@class,"cta-section")) and not(contains(@class,"moments"))]');old.getparent().replace(old,html.fragment_fromstring(markup))
 for e in select(h,'//div[@class="skills-marquee"]'):erase(e)
 # Only the homepage symbol library is replaced; original vectors remain on other routes.
 library=one(h,'//svg[@class="icon-library"]')
 for child in list(library):library.remove(child)
 manifest=json.loads((root/'vendor/home-icons/sources.json').read_text())
 for key,asset in manifest.items():
  svg=etree.parse(str(root/'vendor/home-icons'/asset['file'])).getroot()
  symbol=etree.SubElement(library,'symbol',id='i-'+key,viewBox=svg.get('viewBox'),fill='currentColor')
  for path in svg.iter():
   if isinstance(path.tag,str) and etree.QName(path).localname in ('path','polygon','circle','rect','ellipse','polyline','line'):
    item=deepcopy(path);item.tag=etree.QName(item).localname
    for key in ('id','style','fill','stroke'):item.attrib.pop(key,None)
    if path.get('fill')=='none':continue
    symbol.append(item)
 rail=one(h,'//aside[@class="site-rail"]');nav=one(rail,'.//nav');rail.insert(0,nav)
 menu=one(rail,'.//button[contains(@class,"menu-trigger")]');one(h,'//header[contains(@class,"site-header")]').append(menu)
 for u in select(h,'//*[@id="back-top"]//use'):u.set('href','#i-up')
 add(nav,'<span class="rail-marker" aria-hidden="true"></span>')
 one(h,'//div[@class="home-stage"]').set('id','home-top')
 for a in select(nav,'./a'):a.set('title',a.get('aria-label',''))
 # These assets are only loaded on index: other pages retain their existing design.
 add(one(h,'//head'),'<link rel="stylesheet" href="home-polish.css">')
 add(body,'<script src="home-polish.js" defer></script>')
