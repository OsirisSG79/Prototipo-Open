#!/usr/bin/env python3
"""Build and packaging sanity test (not a GPU or full browser performance test)."""
from pathlib import Path
import subprocess,re
from html.parser import HTMLParser
root=Path(__file__).resolve().parents[1]
subprocess.run(['python',str(root/'build_site.py')],check=True)
html=(root/'index.html').read_text()
class Collector(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.images=[]
 def handle_starttag(self,tag,attrs):
  at=dict(attrs)
  if 'id' in at:self.ids.append(at['id'])
  if tag=='img':self.images.append(at.get('src',''))
p=Collector();p.feed(html)
assert len(p.ids)==len(set(p.ids)), 'duplicate HTML ids'
assert 'id="obTunnel"' in html and html.count('class="tunnel-panel"')==12
assert 'id="conveyorViewport"' in html and 'id="agenda-app"' in html
assert '<!-- RIBBON_CARDS_SLOT -->' not in html
assert '<!-- AGENDA_MOBILE_SLOT -->' not in html
assert not re.search(r'data:image/[^\s"\']+base64,',html),'HTML must not embed large images'
assert (root/'src/js/hero-tunnel.js').exists() and (root/'src/js/schedule-sync.js').exists()
for path in p.images:
 if path.startswith('assets/'):assert (root/path).is_file(),path
print('PASS static: builder, IDs, hero, agenda, local image files, no Base64')
