"""Homepage identity tag, shared right rail, and CMS-driven Moments gallery."""
from copy import deepcopy
from lxml import html,etree

def enhance(pages,profile,moments,settings,*,esc,url,rich,image,set_html,one,select,story_body,root):
 def icon(name):return f'<svg class="icon" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><use href="#i-{name}"></use></svg>'
 def fragment(markup):return html.fragment_fromstring(markup)
 def append(parent,markup):parent.append(fragment(markup))
 def erase(e):
  if e is not None:e.getparent().remove(e)
 logo=settings.get('logo_text') or 'ariful';preferred=settings.get('preferred_name') or 'Ariful'
 # Build the new gallery from the same chrome as the other pages.
 gallery=deepcopy(pages['blogs']);one(gallery,'//body').set('data-page','gallery');one(gallery,'//title').text='Gallery — '+profile['name']
 moments=[m for m in moments if url(m.get('image'))]
 cards=[];featured=[]
 for i,m in enumerate(moments):
  key=m['_id'];category=m.get('category') or 'Moments';placeholder='<span class="sample-label">Sample image</span>' if m.get('placeholder') else ''
  meta=' · '.join(str(m.get(k)) for k in ('date','location') if m.get(k))
  picture=image(m['image'],m.get('alt') or m['title'],'moment-photo')
  caption=f'<div class="moment-caption"><span class="section-label">{esc(category)}</span><h3>{esc(m["title"])}</h3>'+(f'<p>{esc(m["caption"])}</p>' if m.get('caption') else '')+(f'<small>{esc(meta)}</small>' if meta else '')+'</div>'
  shape=(m.get('shape') or 'Landscape').lower()
  button=f'<button class="moment-image" data-moment="{esc(key)}" aria-label="Open photo story: {esc(m["title"])}">{picture}{placeholder}<span class="moment-open">{icon("gallery")}<span>View moment</span></span></button>'
  search=' '.join(str(m.get(k) or '') for k in ('title','caption','category','location','date'))
  cards.append(f'<article class="gallery-item glass shape-{esc(shape)}" id="{esc(key)}" data-gallery-category="{esc(category)}" data-gallery-search="{esc(search.lower())}">{button}{caption}</article>')
  if m.get('featured',True):featured.append(f'<article class="moment-slide glass">{button}<div class="moment-slide-caption"><span>{esc(category)}</span><h3>{esc(m["title"])}</h3></div></article>')
 filters=''.join(f'<button class="filter {"active" if i==0 else ""}" data-gallery-filter="{esc(cat)}" aria-pressed="{str(i==0).lower()}">{esc(cat)}</button>' for i,cat in enumerate(['All']+sorted({m.get('category') or 'Moments' for m in moments})))
 content='<div class="page-content shell gallery-page"><header class="gallery-heading"><span class="section-label">A LIFE IN FRAMES</span><h1>'+esc(settings.get('gallery_page_title') or 'Between the threads.')+'</h1><p>'+esc(settings.get('gallery_page_description') or '')+'</p></header>'
 if moments:content+='<div class="gallery-tools"><label class="search-box"><span class="sr-only">Search gallery</span><input type="search" id="gallery-search" placeholder="Find a moment…"></label><div class="filter-bar" role="group" aria-label="Gallery categories">'+filters+'</div></div><div class="gallery-wall">'+''.join(cards)+'</div><p id="gallery-empty" hidden>No moments match your search.</p>'
 else:content+='<p class="gallery-empty-state">New moments will appear here when they are ready.</p>'
 content+='</div>';set_html(one(gallery,'//main'),content);pages['gallery']=gallery
 # One rail owns theme, navigation, and back-to-top, so their hit areas cannot collide.
 for page,d in pages.items():
  body=one(d,'//body');nav=one(d,'//nav[@class="dock"]')
  for active in select(nav,'./a'):active.set('class','dock-item')
  append(nav,f'<a class="dock-item" href="gallery.html" aria-label="Gallery">{icon("gallery")}<span class="nav-tooltip">Gallery</span></a>')
  # Place Gallery before Contact.
  g=nav[-1];nav.remove(g);nav.insert(max(0,len(nav)-1),g)
  current=page if page in ('index','about','blogs','projects','contact','gallery') else 'blogs' if page.startswith('posts-') else 'projects'
  for link in nav:
   link.attrib.pop('aria-current',None)
   if link.get('href')==current+'.html' or (current=='index' and link.get('href')=='index.html'):link.set('class','dock-item active');link.set('aria-current','page')
  for links in select(d,'//div[@class="menu-links"]'):
   append(links,f'<a href="gallery.html"><span class="menu-number">06</span>Gallery{icon("gallery")}</a>')
  for commands in select(d,'//div[@class="command-results"]'):
   commands.insert(0,fragment(f'<a href="gallery.html" data-command="">{icon("gallery")}Gallery</a>'))
  for el in select(d,'//a[contains(concat(" ",normalize-space(@class)," ")," logo ")]'):
   set_html(el,esc(logo)+'<span>.</span><i aria-hidden="true"></i>');el.set('aria-label',preferred+' home')
  # Add the downloaded SVG Repo camera glyph to the existing inline symbol library.
  lib=one(d,'//svg[@class="icon-library"]');svg=etree.parse(str(root/'vendor/gallery-camera.svg')).getroot()
  sym=etree.Element('symbol',id='i-gallery',viewBox=svg.get('viewBox'))
  for child in svg:
   if isinstance(child.tag,str):
    child=deepcopy(child)
    for node in child.iter():
     if isinstance(node.tag,str):node.tag=etree.QName(node).localname
    child.set('fill','var(--surface)' if child.get('fill')=='white' else 'currentColor');sym.append(child)
  lib.append(sym)
  for use in select(d,'//*[@id="back-top"]//use'):use.set('href','#i-right')
  utilities=one(d,'//div[@class="utilities"]');utilities.getparent().remove(utilities)
  rail=html.Element('aside',{'class':'site-rail','aria-label':'Site controls'})
  append(rail,f'<button class="round-control rail-toggle" aria-label="Open navigation" aria-expanded="false" aria-controls="right-navigation">{icon("menu")}</button>')
  rail.append(utilities);nav.getparent().remove(nav);nav.set('id','right-navigation');rail.append(nav)
  for old in select(d,'//aside[@class="dock-rail"]'):erase(old)
  back=one(d,'//*[@id="back-top"]');back.getparent().remove(back);slot=html.Element('div',{'class':'back-top-slot'});slot.append(back);rail.append(slot);body.append(rail)
  # Move the location and local time out of the portrait card.
  header=one(d,'//header[contains(@class,"site-header")]')
  for el in select(header,'.//span[@class="header-motto"]'):erase(el)
  append(header,'<div class="header-location">'+icon('location')+'<span>'+esc(profile.get('location'))+'</span><i aria-hidden="true"></i><time data-dhaka-time=""></time></div>')
  append(body,'<dialog id="moment-viewer" class="moment-dialog" aria-labelledby="moment-title"><div class="moment-toolbar"><span id="moment-counter"></span><div><button class="round-control" data-moment-prev aria-label="Previous photo">'+icon('left')+'</button><button class="round-control" data-moment-next aria-label="Next photo">'+icon('right')+'</button><button class="round-control" data-moment-close aria-label="Close photo">'+icon('close')+'</button></div></div><div class="moment-reader"><img id="moment-full-image" alt=""><div class="moment-story"><span class="section-label" id="moment-category"></span><h2 id="moment-title"></h2><p id="moment-caption"></p><p id="moment-meta"></p><div id="moment-body"></div><p id="moment-credit"></p><a class="text-link" href="gallery.html">Explore the gallery →</a></div></div></dialog>')
 # Homepage hero: the portrait tag is one focused object, with space reserved for motion.
 h=pages['index'];one(h,'//body').set('data-home-redesign','true')
 card=one(h,'//article[contains(@class,"profile-card")]');socials=deepcopy(one(card,'.//div[@class="profile-socials"]'));socials.set('class','home-socials');photo=url(profile.get('photo'))
 portrait=image(photo,profile.get('photo_alt') or 'Portrait of '+profile['name'],'identity-portrait') if photo else '<div class="identity-monogram">'+esc(''.join(x[0] for x in profile['name'].split()[:2]))+'</div>'
 tag=f'<div class="tag-stage"><span class="tag-anchor" aria-hidden="true"></span><span class="tag-strap" aria-hidden="true"></span><div class="tag-carrier"><article class="identity-tag glass"><button class="tag-grip" aria-label="Move portrait tag. Drag or use arrow keys; Escape resets." aria-describedby="tag-help"><span class="tag-slot" aria-hidden="true"></span><span>HOLD A THREAD</span></button><div class="identity-photo">{portrait}</div><div class="identity-caption"><span class="tag-label">{esc(settings.get("tag_label") or "PERSONAL PORTFOLIO")}</span><h2>{esc(profile["name"])}</h2>'+(f'<p>{esc(settings["tagline"])}</p>' if settings.get('tagline') else '')+f'<div class="tag-bottom"><span>{esc(preferred.upper())} / 01</span><span class="tag-barcode" aria-hidden="true"></span></div></div></article></div><span id="tag-help" class="tag-hint">A little curiosity. Give it a gentle pull.</span></div>'
 card.getparent().replace(card,fragment(tag))
 copy=one(h,'//div[@class="hero-copy"]');actions=deepcopy(one(copy,'.//div[@class="hero-actions"]'))
 headline='<br>'.join(esc(line) for line in (settings.get('headline') or 'Textile engineering,\nwith a practical mind.').splitlines())
 set_html(copy,'<p class="eyebrow">'+esc(settings.get('eyebrow'))+'</p><h1 id="home-title">I’M <em>'+esc(preferred.upper())+'.</em><br>'+headline+'</h1><div class="hero-description">'+rich(settings.get('description'))+'</div>')
 copy.append(actions)
 availability=profile.get('availability')
 if availability:append(copy,'<p class="home-availability"><span aria-hidden="true"></span>'+esc(availability)+'</p>')
 copy.append(socials)
 append(copy,'<div class="home-thread-label"><span aria-hidden="true"></span><span>LEARN · MAKE · SHARE</span></div>')
 # Keep every academic statistic accurate even while the page is entering.
 for e in select(h,'//*[@data-count]'):e.attrib.pop('data-count',None);e.attrib.pop('data-decimals',None)
 for i,stat in enumerate(select(h,'//article[@class="stat"]')):stat.insert(0,fragment('<span class="stat-icon">'+icon(['book','award','users','research'][i%4])+'</span>'))
 # A single real collection feeds both the homepage preview and the Gallery page.
 limit=max(1,min(20,int(settings.get('gallery_limit') or 6)));featured=featured[:limit]
 if featured:
  controls=f'<div class="moments-controls"><button class="round-control" data-moments-prev aria-label="Previous moments">{icon("left")}</button><button class="moments-play" data-moments-play aria-pressed="false">Pause slideshow</button><span class="moments-position" role="status"></span><button class="round-control" data-moments-next aria-label="Next moments">{icon("right")}</button></div>'
  preview='<section class="moments-section shell" aria-labelledby="moments-heading"><div class="moments-heading"><div><span class="section-label">MOMENTS, COLLECTED</span><h2 id="moments-heading">'+esc(settings.get('gallery_heading') or 'Life, between the threads.')+'</h2>'+rich(settings.get('gallery_intro'))+'</div><a class="button secondary" href="gallery.html">Explore the gallery '+icon('gallery')+'</a></div><div class="moments-carousel" data-autoplay="'+str(bool(settings.get('gallery_autoplay',True))).lower()+'"><div class="moments-track" tabindex="0" aria-label="Featured moments. Swipe or use the previous and next buttons.">'+''.join(featured)+'</div>'+controls+'</div></section>'
  main=one(h,'//main');stage=one(h,'//div[@class="home-stage"]');main.insert(list(main).index(stage)+1,fragment(preview))
 return moments
