#!/usr/bin/env python3
"""Reproducible Open Break static build. Run: python build_site.py
No absolute paths, no network dependency to build. Does not edit sources.
"""
from pathlib import Path
from io import BytesIO
import base64, json, re, html
try:
    from PIL import Image
except ImportError:
    Image=None
BASE=Path(__file__).resolve().parent
read=lambda rel:(BASE/rel).read_text(encoding='utf-8')
assets=json.loads(read('assets/data_uris.json'))
outdir=BASE/'assets'/'optimized';outdir.mkdir(parents=True,exist_ok=True)
images={}
for name,value in assets.items():
    dest=outdir/f'{name}.webp'
    if Image is not None:
        binary=base64.b64decode(value.split(',',1)[1]);img=Image.open(BytesIO(binary)).convert('RGB')
        img.thumbnail((1500,1100),Image.Resampling.LANCZOS)
        img.save(dest,'WEBP',quality=82,method=6)
    elif not dest.is_file():
        raise RuntimeError('Para regenerar imágenes originales instala Pillow: pip install Pillow')
    images[name]=f'assets/optimized/{name}.webp'

def bg(src):return "background-image:url('"+src+"')"
texts=[
('01 / Agenda','Una mañana de Reformer','Espacios ordenados, sin llamadas de último minuto.','Reformer', 'studio_hero'),
('02 / Espera','Un lugar liberado','La lista de espera recibe la siguiente oportunidad.','Waitlist','studio_light'),
('03 / Reserva','Clase con cupo limitado','Una plaza asignada a cada reserva.','Agenda','studio_minimal'),
('04 / Llegada','Antes de que empiece la música','La recepción confirma quién ya llegó.','Check-in','reformer_close'),
('05 / Sesión','Tiempo para respirar','Horarios, paquetes y políticas en un mismo lugar.','Yoga','coach_guiding'),
('06 / Equipo','Movimiento sin fricción','Un equipo concentrado en la experiencia.','Pilates','class_action'),
('07 / Escala','Crecer con calma','Organización para más alumnas y más sesiones.','Crecimiento','ribbon_1'),
('08 / Gestión','Todo conectado','Una mirada a la jornada completa del estudio.','Gestión','ribbon_2'),
('09 / Horario','El siguiente horario','Visibilidad de clases y lugares disponibles.','Reserva','ribbon_3'),
('10 / Comunidad','La comunidad primero','Un recorrido más simple para tus alumnas.','Boutique','ribbon_4'),
('11 / Rutina','Una rutina que fluye','Cada detalle operativo en su momento.','Experiencia','ribbon_5'),
('12 / Recepción','El estudio a su ritmo','Menos pasos para registrar una asistencia.','Recepción','studio_hero')]
ribbon='\n'.join(f'''<div class="ribbon-card" data-idx="{i}" role="group" aria-label="Escena {i+1} de {len(texts)}: {html.escape(title)}">
  <div class="ribbon-card-img" style="{bg(images[asset])}"><div class="ribbon-card-overlay"></div><div class="ribbon-card-badge">{number}</div><div class="ribbon-card-tag">{html.escape(tag)}</div></div>
  <div class="ribbon-card-body"><h3 class="ribbon-card-title">{html.escape(title)}</h3><p class="ribbon-card-desc">{html.escape(desc)}</p></div>
</div>''' for i,(number,title,desc,tag,asset) in enumerate(texts))
disciplines=[
('reformer_close','8–14 camas','Pilates Reformer','Un lugar específico para cada alumna.'),
('coach_guiding','Barras y mat','Barre & Mat Flow','Grupos pequeños y horarios con mucha rotación.'),
('studio_light','Sesiones y talleres','Yoga & Sound Baths','Clases regulares, pases y encuentros especiales.'),
('class_action','Bicicletas asignadas','Indoor Cycling','Cupo por bicicleta y recepción organizada.')]
disc_html='\n'.join(f'''<div class="discipline-card"><div class="discipline-img" style="{bg(images[asset])}"></div><div class="discipline-info"><div class="discipline-tag">{html.escape(tag)}</div><h3 class="discipline-name">{html.escape(name)}</h3><p class="discipline-desc">{html.escape(desc)}</p></div></div>''' for asset,tag,name,desc in disciplines)
head=read('templates/part1_head_css.html')
head=head.replace('family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,400&family=JetBrains+Mono:wght@400;500;600', 'family=IBM+Plex+Sans:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,400&family=IBM+Plex+Mono:wght@400;500')
head=head.replace('  <style>', '  <meta name="theme-color" content="#FCFBF8">\n  <meta name="description" content="Open Break: una experiencia de reservas y gestión diseñada para estudios boutique. Descubre la propuesta y su demostración visual.">\n  <style>')
# Avoid expensive transition: all throughout inherited styles
head=re.sub(r'transition:\s*all\s+([^;]+);',r'transition: transform \1, opacity \1, background-color \1;',head)
cssrest=read('templates/part2_css_rest.html')
cssrest=re.sub(r'transition:\s*all\s+([^;]+);',r'transition: transform \1, opacity \1, background-color \1;',cssrest)
cssrest=cssrest.replace('</head>','  <link rel="stylesheet" href="src/css/editorial.css">\n  <link rel="stylesheet" href="src/css/cinematic-hero.css">\n  <link rel="stylesheet" href="src/css/kinetic-type.css">\n  <link rel="stylesheet" href="src/css/motion.css">\n  <link rel="stylesheet" href="src/css/workflow-3d.css">\n  <link rel="stylesheet" href="src/css/schedule-grid.css">\n  <link rel="stylesheet" href="src/css/deck-interactive.css">\n  <link rel="stylesheet" href="src/css/faq-refinements.css">\n  <link rel="stylesheet" href="src/css/nav-refinements.css">\n  <link rel="stylesheet" href="src/css/melius-scroll-responsive.css">\n</head>')
body=read('templates/part3_body_sections.html')
body=body.replace('<!-- RIBBON_CARDS_SLOT -->',ribbon)
body=body.replace('<!-- DISCIPLINE_CARDS_SLOT -->',disc_html)
body=body.replace('<!-- AGENDA_MOBILE_SLOT -->',read('src/modules/schedule_mobile_section.html'))
body=body.replace('id="webglFallbackCard"',f'id="webglFallbackCard" style="{bg(images["studio_hero"])}"')
body=body.replace('<section class="pricing-section"',read('src/modules/workflow_section.html')+'\n  <section class="pricing-section"')
body=body.replace('<div id="custom-cursor"></div>','<div id="custom-cursor" aria-hidden="true"><span id="custom-cursor-label"></span></div>')
body=body.replace('onclick="triggerCarriageGlide()"','onclick="triggerCarriageGlide()" data-reformer-control="true"')
body=body.replace('onclick="resetReformerCamera()"','onclick="resetReformerCamera()" data-reformer-control="true"')
body=body.replace('onclick="toggleReformerSprings()"','onclick="toggleReformerSprings()" data-reformer-control="true"')
legacy=read('templates/part4_js_logic.html')
more_scripts='''
<script src="src/js/demo-store.js"></script>
<script src="src/js/title-typewriter.js" defer></script>
<script src="src/js/hero-tunnel.js" defer></script>
<script src="src/js/motion-director.js" defer></script>
<script src="src/js/schedule-sync.js" defer></script>\n<script src="src/js/analytics-engine.js" defer></script>\n<script src="src/js/scroll-choreography.js" defer></script>
'''
modules='\n'.join(read(f'src/js/{name}.js').replace('export class ','class ',1) for name in ['cursor','ribbon','studio-canvas','reformer-3d'])
controller=f'''<script src="assets/three.min.js"></script>
<script src="assets/GLTFLoader.js"></script>
<script>
{modules}
let cursorInstance,ribbonInstance,canvasInstance,reformerInstance;
window.addEventListener('DOMContentLoaded',()=>{{
  cursorInstance=new ContextualCursor();
  ribbonInstance=new ParabolicRibbon('conveyorViewport','ribbonTrack');
  canvasInstance=new StudioWorkflowCanvas('workflowBoard');
  reformerInstance=new ReformerStudioViewer('reformerCanvas','webglFallbackCard');
  // Accurate mobile-drawer placement relative to the sticky navbar.
  const nav=document.querySelector('.site-nav');
  if(nav){{const sync=()=>document.documentElement.style.setProperty('--mobile-drawer-top',nav.getBoundingClientRect().bottom+'px');sync();window.addEventListener('resize',sync,{{passive:true}});}}
}});
function triggerCarriageGlide(){{reformerInstance?.glideCarriage()}}
function toggleReformerSprings(){{reformerInstance?.toggleSprings()}}
function resetReformerCamera(){{reformerInstance?.resetCamera()}}
</script>
'''
# opt-in to JS-reveal only through parent class after initial layout, preserve content if JS fails
out=head+cssrest+body+controller+more_scripts+legacy + "\n</body>\n</html>\n"
for name in ('landing_melius_style.html','index.html'):(BASE/name).write_text(out,encoding='utf-8')
print('Build complete | HTML:',len(out.encode()),'bytes | assets:',len(images),'optimized images')
