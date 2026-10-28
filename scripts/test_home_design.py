"""Test homepage/gallery content lifecycle and preserve one coherent navigation."""
import json,shutil,subprocess,sys,tempfile
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as t:
 base=Path(t)/'site';shutil.copytree(ROOT,base,ignore=shutil.ignore_patterns('.git','__pycache__','qa-responsive.html'))
 def build():subprocess.run([sys.executable,str(base/'scripts/build_editor.py')],check=True,capture_output=True)
 def doc(name):return html.parse(str(base/'docs'/name))
 def save(path,data):(base/path).write_text(json.dumps(data))
 build();home=doc('index.html');g=doc('gallery.html')
 assert home.xpath('//img[contains(@class,"identity-portrait")]/@src')==['assets/ariful-portrait.jpg']
 assert home.xpath('//h1[@id="home-title"]//em/text()')==['ARIFUL.']
 assert not home.xpath('//article[@class="stat"]//*[@data-count]')
 assert not home.xpath('//div[@class="profile-location"]')
 for path in (base/'docs').glob('*.html'):
  if path.name.startswith('qa-'):continue
  d=doc(path.name);nav=d.xpath('//nav[@id="right-navigation"]/a/@href')
  assert nav==['index.html','about.html','blogs.html','projects.html','gallery.html','contact.html'],(path.name,nav)
  assert len(d.xpath('//aside[@class="site-rail"]'))==1
  assert len(d.xpath('//*[@id="moment-viewer"]'))==1
  assert len(d.xpath('//nav[@id="right-navigation"]//a[@aria-current="page"]'))==1
 assert len(g.xpath('//article[contains(@class,"gallery-item")]'))==4
 assert len(home.xpath('//article[contains(@class,"moment-slide")]'))==4
 assert len(g.xpath('//span[@class="sample-label"]'))==4
 # A new photo propagates to Gallery and homepage; hidden and unfeatured are distinct.
 item=dict(title='A real moment',image='assets/loom-spools.jpg',published=True,featured=True,order=0,body='<p>My story</p>',caption='A real caption',date='2026',location='Dhaka',category='Personal')
 save('editor/gallery/personal.json',item);build()
 assert doc('gallery.html').xpath('//*[@id="gallery-personal"]')
 assert doc('index.html').xpath('//*[@data-moment="gallery-personal"]')
 assert not doc('gallery.html').xpath('//*[@id="gallery-personal"]//span[@class="sample-label"]')
 raw=(base/'docs/content.js').read_text();moments=json.loads(raw.split('window.PORTFOLIO_MOMENTS=')[1].rstrip(';'))
 assert next(m for m in moments if m['_id']=='gallery-personal')['body']=='<p>My story</p>'
 item['featured']=False;save('editor/gallery/personal.json',item);build();assert not doc('index.html').xpath('//*[@data-moment="gallery-personal"]');assert doc('gallery.html').xpath('//*[@id="gallery-personal"]')
 item['published']=False;save('editor/gallery/personal.json',item);build();assert not doc('gallery.html').xpath('//*[@id="gallery-personal"]');assert 'A real moment' not in (base/'docs/content.js').read_text()
 # Empty galleries produce no empty homepage carousel or broken navigation.
 for p in (base/'editor/gallery').glob('*.json'):p.unlink()
 build();assert not doc('index.html').xpath('//section[contains(@class,"moments-section")]');assert doc('gallery.html').xpath('//*[contains(@class,"gallery-empty-state")]')
 # Portrait and all new identity copy stay editable after the redesign.
 p=json.loads((base/'editor/profile.json').read_text());p['photo']='';save('editor/profile.json',p)
 s=json.loads((base/'editor/homepage.json').read_text());s.update(logo_text='newname',preferred_name='Newname',headline='Updated headline',tagline='New tagline');save('editor/homepage.json',s);build()
 h=doc('index.html');assert h.xpath('//div[@class="identity-monogram"]');assert 'NEWNAME.' in h.xpath('string(//h1)');assert 'Updated headline' in h.xpath('string(//h1)');assert h.xpath('//a[@class="logo"]/text()')[0]=='newname'
print('Passed: shared six-page navigation, portrait replacement/fallback, accurate stats, featured/unfeatured/draft/gallery removal and editable homepage identity')
