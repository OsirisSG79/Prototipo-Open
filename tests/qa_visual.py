#!/usr/bin/env python3
"""Static layout screenshots at 4 widths. Browser animation/GPU QA is separate.
Requires Playwright and installed Chromium. Does not fetch remote assets.
"""
from pathlib import Path
import base64,re,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tests'/'screenshots';OUT.mkdir(exist_ok=True)
html=(ROOT/'index.html').read_text()
for path in ['src/css/editorial.css','src/css/cinematic-hero.css']:
 html=html.replace(f'<link rel="stylesheet" href="{path}">',f'<style>{(ROOT/path).read_text()}</style>')
html=re.sub(r'<script\b[^>]*>.*?</script>','',html,flags=re.S)
html=re.sub(r'<link[^>]*(?:fonts.googleapis.com|fonts.gstatic.com)[^>]*>','',html)
for path in sorted((ROOT/'assets/optimized').glob('*.webp')):
 html=html.replace('assets/optimized/'+path.name,'data:image/webp;base64,'+base64.b64encode(path.read_bytes()).decode())
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None,args=['--no-sandbox','--disable-webgl','--disable-gpu'])
 for width,height in [(320,740),(390,844),(768,1024),(1440,900)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
  page.set_content(html,wait_until='domcontentloaded',timeout=30000)
  data=page.evaluate('''() => ({viewport:innerWidth,scroll:document.documentElement.scrollWidth,pictures:[...document.querySelectorAll('.tunnel-panel img')].filter(x=>x.naturalWidth).length})''')
  page.screenshot(path=str(OUT/f'hero_static_{width}.png'),timeout=15000)
  assert data['scroll']<=width,data
  assert data['pictures']==12,data
  results.append(data);page.close()
 browser.close()
(OUT/'static_results.json').write_text(json.dumps(results,indent=2))
print('PASS static responsive screenshots:',results)
