"""Scoped homepage presentation layer; original templates and other routes stay intact."""
from lxml import html
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
 # These assets are only loaded on index: other pages retain their existing design.
 add(one(h,'//head'),'<link rel="stylesheet" href="home-polish.css">')
 add(body,'<script src="home-polish.js" defer></script>')
