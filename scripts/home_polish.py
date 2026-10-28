"""Scoped homepage presentation layer; original templates and other routes stay intact."""
from lxml import html, etree
import json
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
