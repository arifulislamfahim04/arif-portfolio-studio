"""Build the portfolio from Pages CMS content; never import the legacy generator."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import json, shutil, re
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'
TAGS=['p','br','strong','b','em','i','u','s','h2','h3','h4','h5','h6','ul','ol','li','blockquote','a','img','figure','figcaption','pre','code','hr','table','thead','tbody','tr','th','td','mark','span','div']
def esc(v):return escape(str(v or ''),quote=True)
def url(v):
 v=str(v or '').strip()
 if not v:return ''
 if v.startswith('//') or '\\' in v or any(ord(c)<32 for c in v):return ''
 if urlsplit(v).scheme.lower() not in ('','http','https','mailto','tel'):return ''
 return v

def rich(v):
 root=html.fragment_fromstring('<div>'+str(v or '')+'</div>')
 for e in list(root.iterdescendants()):
  if e.getparent() is None:continue
  if not isinstance(e.tag,str):
   e.getparent().remove(e);continue
  if e.tag in ('script','style','iframe','object','embed','svg','math','form','input','button'):
   e.drop_tree();continue
  if e.tag not in TAGS:
   e.drop_tag();continue
  allowed={'class'}|{'a':{'href','title'},'img':{'src','alt','title','width','height'},'th':{'colspan'},'td':{'colspan'}}.get(e.tag,set())
  for key in list(e.attrib):
   if key not in allowed:del e.attrib[key]
   elif key in ('href','src'):
    safe=url(e.get(key))
    if safe:e.set(key,safe)
    else:del e.attrib[key]
 return inner(root)
def read(path):return json.loads((ROOT/'editor'/path).read_text())
def entries(folder):
 result=[]
 for p in (ROOT/'editor'/folder).glob('*.json'):
  d=json.loads(p.read_text())
  if d.get('published',False):result.append(dict(d,_id=folder+'-'+p.stem))
 return sorted(result,key=lambda x:(float(x.get('order') or 0),str(x.get('date') or ''),x['_id']))
def set_html(e,markup):
 for c in list(e):e.remove(c)
 e.text=None
 wrapper=html.fragment_fromstring('<div>'+markup+'</div>');e.text=wrapper.text
 for c in wrapper:e.append(c)
def select(d,x):return d.xpath(x)
def one(d,x):return select(d,x)[0]
def inner(e):return (e.text or '')+''.join(html.tostring(c,encoding='unicode') for c in e)
def section(d,id,markup):
 e=one(d,f'//*[@id="{id}"]'); header=e[0]
 for c in list(e)[1:]:e.remove(c)
 for c in html.fragments_fromstring(markup):
  if isinstance(c,str):continue
  e.append(c)
def image(path,alt='',cls=''):
 return f'<img class="{esc(cls)}" src="{esc(url(path))}" alt="{esc(alt)}" loading="lazy">' if url(path) else ''
def attachment(path,title):
 path=url(path)
 if not path:return ''
 link=f'<p><a class="button secondary" href="{esc(path)}" target="_blank" rel="noopener">Open / download {esc(title)}</a></p>'
 if urlsplit(path).path.lower().endswith(('.jpg','.jpeg','.png','.webp','.gif')):return image(path,title)+link
 if urlsplit(path).path.lower().endswith('.pdf'):return f'<iframe class="certificate-pdf" src="{esc(path)}" title="{esc(title)}" loading="lazy"></iframe>'+link
 return link

def story_body(d):
 body=rich(d.get('body',''))
 for pic in d.get('gallery') or []:
  body+='<figure>'+image(pic.get('image'),pic.get('caption',''))+'<figcaption>'+esc(pic.get('caption',''))+'</figcaption></figure>'
 video=url(d.get('video_url',''))
 if video:
  u=urlsplit(video); host=u.netloc.lower(); vid=''
  if host in ('youtube.com','www.youtube.com'):
   from urllib.parse import parse_qs
   vid=parse_qs(u.query).get('v',[''])[0] if u.path=='/watch' else u.path.split('/')[-1]
  elif host=='youtu.be':vid=u.path.strip('/')
  if re.fullmatch(r'[A-Za-z0-9_-]{11}',vid):body+=f'<iframe class="story-video" src="https://www.youtube-nocookie.com/embed/{vid}" title="Video" allowfullscreen loading="lazy"></iframe>'
  elif u.path.lower().endswith(('.mp4','.webm')):body+=f'<video controls preload="metadata" src="{esc(video)}"></video>'
  else:body+=f'<p><a href="{esc(video)}" target="_blank" rel="noopener">Watch video</a></p>'
 return body

def build():
 OUT.mkdir(exist_ok=True)
 # Immutable original design lives in templates; uploaded media lives in docs/assets.
 pages={p.stem:html.parse(str(p)) for p in (ROOT/'templates').glob('*.html')}
 profile=read('profile.json'); about=read('about.json'); details={};documents=[]
 for d in pages.values():
  for a in select(d,'//a[@href]'):
   href=a.get('href')
   if href=='assets/ariful-islam-fahim-cv.pdf':
    a.set('href',url(profile['resume']));a.attrib.pop('download',None)
   elif href.startswith('mailto:arifulislamfahim04@gmail.com'):a.set('href','mailto:'+profile['email']+href.partition('?')[1]+href.partition('?')[2])
   elif href=='tel:+8801968718018':a.set('href','tel:'+profile['phone'])
   elif 'linkedin.com/in/ariful-islam-fahim' in href:a.set('href',url(profile['linkedin']))
  for e in select(d,'//*[@data-copy]'):
   value=e.get('data-copy')
   if '@' in value:e.set('data-copy',profile['email'])
   elif value.startswith('+880'):e.set('data-copy',profile['phone'])
  for e in select(d,'//footer//span[1]'):
   # Only replace the name text, preserving the live year.
   for child in e:
    if child.get('data-year') is not None:child.tail=' '+profile['name']+'.'
 h=pages['index']
 for selector,key in [('//div[@class="profile-content"]/h2','name'),('//p[@class="profile-role"]','role'),('//span[@class="availability"]','availability'),('//div[@class="profile-location"]/span','location')]:set_html(one(h,selector),esc(profile[key]))
 for key,x in [('cover','//div[@class="profile-photo"]/img'),('secondary_image','//div[@class="floating-swatch"]/img')]:
  for e in select(h,x):e.set('src',url(profile[key]))
 if profile.get('photo'):
  e=one(h,'//div[@class="profile-photo"]/img');e.set('src',url(profile['photo']));e.set('alt',profile.get('photo_alt',''));e.set('class','textile-photo portrait-upload')
  for e in select(h,'//span[@class="portrait-monogram"]|//div[@class="floating-swatch"]|//div[@class="yarn-spool"]|//svg[contains(@class,"needle-thread")]|//span[@class="photo-credit"]'):e.getparent().remove(e)
 title=one(h,'//*[@id="home-title"]');typebox=one(title,'.//span[@class="type-box"]');typebox.getparent().remove(typebox);set_html(title,esc(profile['hero_title']));title.append(typebox)
 title.set('aria-label',profile['hero_title']+' '+(profile.get('rotating_words') or [''])[0])
 for key,x in [('hero_description','//p[@class="hero-description"]'),('introduction','//section[.//span[text()="MY APPROACH"]]/p'),('call_to_action','//section[contains(@class,"cta-section")]/p')]:set_html(one(h,x),rich(profile[key]))
 stats=''
 for s in profile.get('stats',[]):
  value=float(s.get('value') or 0); decimals=max(0,min(3,int(s.get('decimals') or 0)))
  stats+=f'<article class="stat"><div><strong><span data-count="{value}" data-decimals="{decimals}">{value:.{decimals}f}</span><small>{esc(s.get("suffix"))}</small></strong><h3>{esc(s.get("label"))}</h3><span class="stat-detail">{esc(s.get("detail"))}</span></div></article>'
 set_html(one(h,'//div[@class="stats-glass glass"]'),stats)
 a=pages['about'];set_html(one(a,'//div[@class="bio"]'),rich(about['biography']))
 for key,x in [('information','//dl[@class="info-grid"]'),('glance','//aside[contains(@class,"at-glance")]/dl')]:
  markup=''.join(f'<div class="info-card glass"><div><dt>{esc(v["label"])}</dt><dd>{esc(v["value"])}</dd></div></div>' for v in about.get(key,[]));set_html(one(a,x),markup)
 def timeline(folder):
  cards=''
  for v in entries(folder):cards+=f'<article class="timeline-card glass" data-reveal><span class="timeline-node"></span><span class="care-chip">{esc(v.get("date"))}</span><h3>{esc(v["title"])}</h3><p class="institution">{esc(v.get("institution"))}</p>{rich(v.get("body"))}<span class="fact-chip">{esc(v.get("badge"))}</span>{attachment(v.get("file"),"document")}</article>'
  return '<div class="stitched-timeline">'+cards+'</div>' if cards else '<p>No entries published yet.</p>'
 for folder in ('education','experience'):section(a,folder,timeline(folder))
 skills='<div class="skill-grid">'
 for s in about.get('skills',[]):skills+=f'<article class="skill-card glass"><h3>{esc(s["title"])}</h3>{rich(s.get("body"))}<ul class="skill-list">'+''.join('<li>'+esc(v)+'</li>' for v in s.get('items',[]))+'</ul></article>'
 skills+='</div><div class="language-grid">'+''.join(f'<article class="language-card glass"><div><h3>{esc(v["title"])}</h3><p>{esc(v.get("description"))}</p></div></article>' for v in about.get('languages',[]))+'</div>'
 section(a,'skills',skills)
 def certificates(folder):
  cards=''
  for v in entries(folder):
   documents.append(dict(id=v['_id'],kind='Academic recognition' if folder=='achievements' else 'Certificate record',title=v['title'],body=rich(v.get('body'))+(attachment(v.get('file'),'certificate') if v.get('file') else '<p>No certificate file has been uploaded yet.</p>')))
   cards+=f'<article class="certificate-card glass" data-reveal><span class="care-chip">{esc(v.get("date"))}</span><h3>{esc(v["title"])}</h3><p class="institution">{esc(v.get("institution"))}</p>{rich(v.get("body"))}<button class="text-link" data-document="{esc(v["_id"])}">View details / certificate →</button></article>'
  return '<div class="certificate-grid">'+cards+'</div>' if cards else '<p>No entries published yet.</p>'
 section(a,'recognition',certificates('achievements'))
 section(a,'certificates',certificates('certificates')+'<div class="transcript-action"><button class="button secondary" data-document="transcript">View Transcript</button></div><h3 class="subsection-title">Workshops &amp; seminars</h3>'+timeline('workshops'))
 documents.append(dict(id='transcript',kind='Academic transcript',title='Academic transcript',body=rich(about.get('transcript_body'))+attachment(about.get('transcript'),'transcript')))
 recommendations=''.join(f'<article class="glass certificate-card"><h3>{esc(v["title"])}</h3>{rich(v.get("body"))}</article>' for v in about.get('recommendations',[])) or '<div class="recommendation-empty glass"><h3>Recommendations coming soon</h3><p>Real recommendations will appear here as they become available.</p></div>'
 references=''.join('<article class="reference-card glass">'+rich(v['body'])+'</article>' for v in about.get('references',[]))
 section(a,'recommendations',recommendations+'<details class="academic-references glass"><summary>Academic references</summary><div class="reference-grid">'+references+'</div></details>')
 # Generate both listing cards and shareable full pages from every published entry.
 for folder,page,cls,attr in [('posts','blogs','blog','data-blog-category'),('projects','projects','project','data-category')]:
  cards='';items=entries(folder);cats=[]
  for v in items:
   key=v['_id'];category=v.get('category') or 'General';cats.append(category)
   filename=key+'.html';body=story_body(v);details[key]=dict(title=v['title'],tag=v.get('label') or category,body=body)
   picture=image(v.get('cover'),v.get('cover_alt') or v['title'],'textile-photo')
   if picture:picture=f'<a class="{cls}-cover" href="{filename}" data-project="{key}">{picture}</a>'
   cards+=f'<article class="{cls}-card glass" {attr}="{esc(category)}" data-reveal>{picture}<div class="{cls}-content"><span class="section-label">{esc(v.get("label") or category)}</span><div class="blog-meta"><time>{esc(v.get("date"))}</time></div><h2><a href="{filename}" data-project="{key}">{esc(v["title"])}</a></h2><p>{esc(v.get("summary"))}</p><a class="text-link" href="{filename}" data-project="{key}">Read more →</a></div></article>'
   single=html.parse(str(ROOT/'templates'/f'{page}.html'));main=one(single,'//main');set_html(main,f'<article class="page-content shell story-page"><a class="button secondary" href="{page}.html">← Back to {page}</a><p class="section-label">{esc(category)} · {esc(v.get("date"))}</p><h1>{esc(v["title"])}</h1>{image(v.get("cover"),v.get("cover_alt") or v["title"],"story-cover")}<div class="story-body">{body}</div></article>');one(single,'//title').text=v['title']+' — '+profile['name'];pages[key]=single
  set_html(one(pages[page],f'//div[@class="{cls}-grid"]'),cards or '<p>No entries published yet.</p>')
  filterattr='data-blog-filter' if folder=='posts' else 'data-project-filter'
  markup=''.join(f'<button class="filter {"active" if i==0 else ""}" {filterattr}="{esc(c)}" aria-pressed="{str(i==0).lower()}">{esc("All" if i==0 else c)}</button>' for i,c in enumerate(['all']+sorted(set(cats))))
  set_html(one(pages[page],'//div[contains(@class,"filter-bar")]'),markup)
 # Remove previously generated post pages, so deleted/unpublished entries disappear.
 for pattern in ('posts-*.html','projects-*.html'):
  for p in OUT.glob(pattern):p.unlink()
 for name,d in pages.items():
  # All pages use the same editable contact and resume values.
  pass
  for e in select(d,'//a[@href]'):
   old=e.get('href')
   if old=='assets/ariful-islam-fahim-cv.pdf':e.set('href',url(profile['resume']));e.attrib.pop('download',None)
   elif old.startswith('mailto:arifulislamfahim04@gmail.com'):e.set('href',old.replace('arifulislamfahim04@gmail.com',profile['email']))
   elif old=='tel:+8801968718018':e.set('href','tel:'+profile['phone'])
   elif 'linkedin.com/in/ariful-islam-fahim' in old:e.set('href',url(profile['linkedin']))
  for e in select(d,'//body//*'):
   for key in ('text','tail'):
    value=getattr(e,key)
    if value:
     value=value.replace('Ariful Islam Fahim',profile['name']).replace('arifulislamfahim04@gmail.com',profile['email']).replace('+880 1968-718018',profile['phone'])
     setattr(e,key,value)
  for e in select(d,'//head'):

   e.append(html.Element('link',rel='stylesheet',href='editor.css'))
  (OUT/(name+'.html')).write_text(html.tostring(d,encoding='unicode',doctype='<!doctype html>'))
 payload='window.PORTFOLIO_DETAILS='+json.dumps(details,ensure_ascii=False)+';\nwindow.PORTFOLIO_DOCUMENTS='+json.dumps(documents,ensure_ascii=False)+';\nwindow.PORTFOLIO_PROFILE='+json.dumps(profile,ensure_ascii=False)+';'
 (OUT/'content.js').write_text(payload)
 js=(ROOT/'dist/site.js').read_text().replace("const words=['CREATOR’S CURIOSITY','ENGINEER’S MIND','STORYTELLER’S EYE','LOVE FOR AI'];","const words=window.PORTFOLIO_PROFILE.rotating_words?.length ? window.PORTFOLIO_PROFILE.rotating_words : ['CURIOUS MIND'];")
 js=js.replace('mailto:arifulislamfahim04@gmail.com?subject=',"mailto:${window.PORTFOLIO_PROFILE.email}?subject=")
 js=js.replace("h.setAttribute('aria-label','I’m Arif, a textile engineering student with a creator’s curiosity.');","h.setAttribute('aria-label',window.PORTFOLIO_PROFILE.hero_title+' '+words[0]);")
 (OUT/'site.js').write_text(js)
 (OUT/'editor.css').write_text('''.portrait-upload{object-fit:cover!important;filter:none!important}.story-page{max-width:900px}.story-page h1{font-size:clamp(2rem,5vw,4rem);line-height:1.15;margin:2rem 0}.story-body{font-size:1.1rem;line-height:1.85}.story-cover{width:100%;max-height:500px;object-fit:cover;border-radius:16px}.story-body img,#reader-body img,#document-body img{max-width:100%;height:auto;border-radius:12px}.story-body figure,#reader-body figure{margin:1.5rem 0}.story-body figcaption,#reader-body figcaption{font-size:.9rem;opacity:.75}.story-video,video{width:100%;aspect-ratio:16/9;border:0}.certificate-pdf{width:100%;height:65vh;border:0}.story-body table,#reader-body table{width:100%;border-collapse:collapse}.story-body td,.story-body th,#reader-body td,#reader-body th{padding:.5rem;border:1px solid #8886}.info-card dd{overflow-wrap:anywhere}.certificate-card .text-link{margin-top:1rem}.certificate-card img{max-width:100%}''')
 (OUT/'.nojekyll').touch()
 print(f'Built {len(pages)} pages, {len(details)} stories, {len(documents)} documents')
if __name__=='__main__':build()
