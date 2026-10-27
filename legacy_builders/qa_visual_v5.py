#!/usr/bin/env python3
"""Self-contained Playwright smoke check; no external server required.
Run from any directory: python tests/qa_visual.py
Needs playwright + a Chromium installation. External font fetch intentionally avoided in test.
"""
from pathlib import Path
import base64,json,re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tests'/'screenshots';OUT.mkdir(exist_ok=True)
html=(ROOT/'index.html').read_text()
html=html.replace('<link rel="stylesheet" href="src/css/editorial.css">','<style>'+(ROOT/'src/css/editorial.css').read_text()+'</style>')
html=html.replace('<script src="assets/three.min.js"></script>','<script>'+(ROOT/'assets/three.min.js').read_text()+'</script>')
html=re.sub(r'<link[^>]*fonts.googleapis.com[^>]*>','',html)
html=re.sub(r'<link[^>]*fonts.gstatic.com[^>]*>','',html)
for item in (ROOT/'assets/optimized').glob('*.webp'):
    html=html.replace(f'assets/optimized/{item.name}','data:image/webp;base64,'+base64.b64encode(item.read_bytes()).decode())
checks=[]
with sync_playwright() as p:
    browser=p.chromium.launch(**({'executable_path':'/usr/bin/chromium'} if Path('/usr/bin/chromium').exists() else {}),headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--disable-webgl'])
    for width in (320,390,768,1440):
        page=browser.new_page(viewport={'width':width,'height':900})
        errors=[];page.on('pageerror',lambda exc:errors.append(str(exc)))
        page.set_content(html,wait_until='domcontentloaded',timeout=30000)
        page.wait_for_timeout(250)
        stats=page.evaluate('''() => ({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth,uniqueIds:new Set([...document.querySelectorAll('[id]')].map(n=>n.id)).size===document.querySelectorAll('[id]').length,cards:document.querySelectorAll('.ribbon-card').length})''')
        checks.append({'viewport':width,'no_horizontal_overflow':stats['scroll']<=stats['client'],'unique_ids':stats['uniqueIds'],'ribbon_cards':stats['cards'],'js_errors':errors})
        page.screenshot(path=str(OUT/f'hero_{width}.png'))
        page.locator('#canvas-section').scroll_into_view_if_needed()
        page.locator('#workflowNext').click()
        checks[-1]['workflow_next']=page.locator('#workflowActiveIndex').inner_text()=='02'
        page.locator('#workflowPrev').click()
        checks[-1]['workflow_back']=page.locator('#workflowActiveIndex').inner_text()=='01'
        page.screenshot(path=str(OUT/f'workflow_{width}.png'))
        if width==390:
            page.locator('#mobileMenuBtn').click()
            checks[-1]['mobile_open']=page.locator('#mobileMenuBtn').get_attribute('aria-expanded')=='true'
            page.locator('#mobileMenuBtn').click()
            checks[-1]['mobile_close']=page.locator('#mobileMenuBtn').get_attribute('aria-expanded')=='false'
        if width==1440:
            page.locator('#pauseRibbonButton').click()
            checks[-1]['pause_ribbon']=page.locator('#pauseRibbonButton').get_attribute('aria-pressed')=='true'
            page.locator('.hero-cta-group .btn-primary').click()
            checks[-1]['modal_open']=page.locator('#demoModal').is_visible()
            page.locator('#demoName').fill('Usuario de prueba')
            page.locator('#demoStudio').fill('Studio QA')
            page.locator('#demoPhone').fill('5555555555')
            page.locator('#modalFormContainer button[type="submit"]').click()
            checks[-1]['honest_demo_feedback']='No se enviaron' in page.locator('#feedbackMessage').inner_text()
            checks[-1]['no_private_leads_storage']='localStorage.setItem' not in (ROOT/'templates/part4_js_logic.html').read_text()
            page.keyboard.press('Escape')
            checks[-1]['modal_esc_close']=not page.locator('#demoModal').is_visible()
        page.close()
    browser.close()
(OUT/'results.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False))
print(json.dumps(checks,ensure_ascii=False,indent=2))
issues=[]
for x in checks:
    for key,value in x.items():
        if key!='js_errors' and isinstance(value,bool) and not value:issues.append((x['viewport'],key))
    if x['js_errors']:issues.append((x['viewport'],x['js_errors']))
if issues:raise SystemExit(f'QA FAILED: {issues}')
