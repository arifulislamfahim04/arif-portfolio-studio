"""Content integration cases that protect the new homepage and existing routes."""
import json,shutil,subprocess,sys,tempfile
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as temp:
 base=Path(temp)/'site';shutil.copytree(ROOT,base,ignore=shutil.ignore_patterns('.git','.openai','__pycache__','qa-*'))
 def save(path,data):(base/path).write_text(json.dumps(data))
 def build():subprocess.run([sys.executable,str(base/'scripts/build_editor.py')],check=True,capture_output=True)
 def doc(name='index.html'):return html.parse(str(base/'docs'/name))
 build();h=doc()
 assert len(h.xpath('//h1'))==1
 assert h.xpath('//div[@class="hero-actions"]/a[1][@download]')
 assert not h.xpath('//div[@class="home-socials"]//a[starts-with(@href,"tel:")]')
 assert h.xpath('//div[@class="home-socials"]/a[1]/@href')==['contact.html']
 assert not h.xpath('//footer/a|//*[contains(@class,"ghost-word")]')
 assert len(h.xpath('//div[@class="marquee-row"]'))==2
 assert len(h.xpath('//div[@class="slideshow-track"]/article'))==6
 assert all(s.get('fill')=='currentColor' for s in h.xpath('//svg[@class="icon-library"]/symbol'))
 assert h.xpath('//meta[@property="og:image"]/@content')==['https://arifulislamfahim04.github.io/arif-portfolio-studio/assets/ariful-portrait.jpg']
 assert h.xpath('//article[@class="update-entry"]/div/time/text()')==['12 Oct 2026','9 Oct 2026','6 Oct 2026']
 for path in (base/'docs').glob('*.html'):
  d=doc(path.name);extra=d.xpath('//link[contains(@href,"home-polish.css")]')
  assert bool(extra)==(path.name=='index.html'),path.name
  assert len(d.xpath('//button[contains(@class,"theme-toggle")]'))==1
 # Independent real stories remain unchanged in the build when homepage settings change.
 p=json.loads((base/'editor/profile.json').read_text());p['facebook']='https://www.facebook.com/example';save('editor/profile.json',p)
 s=json.loads((base/'editor/homepage.json').read_text());s.update(background_image='',background_image_small='',roles=[],seo_title='An editable search title');save('editor/homepage.json',s)
 for entry in (base/'editor/updates').glob('*.json'):entry.unlink()
 build();h=doc();assert h.xpath('//div[@class="home-socials"]/a[@aria-label="Facebook"]');assert not h.xpath('//div[@class="hero-backdrop"]|//div[@class="role-line"]');assert not h.xpath('//p[@class="updates-empty"]/@hidden');assert h.xpath('//title/text()')==['An editable search title']
 # Drafts disappear; dates order newest first; image/link optional; hostile values stay text.
 for i in range(5):save(f'editor/updates/test-{i}.json',dict(title=f'Update {i}',date=f'2026-10-{20+i}',topic='Research',text='<script>unsafe</script>',image='assets/ariful-portrait.jpg' if i==4 else '',image_alt='Research photo',link='javascript:alert(1)',published=True,sample=False))
 save('editor/updates/draft.json',dict(title='Hidden draft',published=False))
 build();h=doc();entries=h.xpath('//article[@class="update-entry"]');assert len(entries)==5;assert len([e for e in entries if 'hidden' not in e.attrib])==3;assert entries[0].xpath('.//h3/text()')==['Update 4'];assert not h.xpath('//article[@class="update-entry"]//script|//article[@class="update-entry"]//a');assert 'Hidden draft' not in h.xpath('string(//main)')
 assert len(h.xpath('//img[@class="update-photo"]'))==1
 # Missing dates are safe and do not crash a sparse form submission.
 save('editor/updates/undated.json',dict(title='Undated update',published=True));build();assert not doc().xpath('//article[.//h3[text()="Undated update"]]//time|//article[.//h3[text()="Undated update"]]//p')
 # Gallery remains usable with one image or none; placeholder badges follow their CMS flag.
 for path in (base/'editor/gallery').glob('*.json'):path.unlink()
 save('editor/gallery/one.json',dict(title='One real photo',image='assets/ariful-portrait.jpg',published=True,featured=True,placeholder=False));build();h=doc();assert h.xpath('//div[@class="marquee-row"]');assert not h.xpath('//span[@class="sample-label"]')
 (base/'editor/gallery/one.json').unlink();build();assert not doc().xpath('//div[contains(@class,"moments-showcase")]')
print('Passed: homepage-only assets, six shared routes, safe social links, gallery fallbacks, update ordering/drafts/optional fields, blank background/roles and editable SEO')
