import json

# 1. Cargar Assets
with open('/home/user/openbreak/assets/data_uris.json', 'r', encoding='utf-8') as f:
    images = json.load(f)

with open('/home/user/openbreak/assets/three.min.js', 'r', encoding='utf-8') as f:
    three_min_js = f.read()

# 2. Cargar CSS Tokens y Plantillas
with open('/home/user/openbreak/src/css/tokens.css', 'r', encoding='utf-8') as f:
    tokens_css = f.read()

with open('/home/user/openbreak/templates/part1_head_css.html', 'r', encoding='utf-8') as f:
    part1 = f.read()

with open('/home/user/openbreak/templates/part2_css_rest.html', 'r', encoding='utf-8') as f:
    part2 = f.read()

with open('/home/user/openbreak/templates/part3_body_sections.html', 'r', encoding='utf-8') as f:
    part3 = f.read()

with open('/home/user/openbreak/src/modules/workflow_section.html', 'r', encoding='utf-8') as f:
    workflow_section = f.read()

# 3. Cargar Módulos JS
with open('/home/user/openbreak/src/js/cursor.js', 'r', encoding='utf-8') as f:
    cursor_js = f.read().replace('export class', 'class')

with open('/home/user/openbreak/src/js/ribbon.js', 'r', encoding='utf-8') as f:
    ribbon_js = f.read().replace('export class', 'class')

with open('/home/user/openbreak/src/js/studio-canvas.js', 'r', encoding='utf-8') as f:
    canvas_js = f.read().replace('export class', 'class')

with open('/home/user/openbreak/src/js/reformer-3d.js', 'r', encoding='utf-8') as f:
    reformer_js = f.read().replace('export class', 'class')

with open('/home/user/openbreak/templates/part4_js_logic.html', 'r', encoding='utf-8') as f:
    part4_logic = f.read()

# 4. Construir Ribbon Cards con Data URIs
available_assets = [
    images["studio_hero"], images["studio_light"], images["studio_minimal"],
    images["reformer_close"], images["coach_guiding"], images["class_action"],
    images["ribbon_1"], images["ribbon_2"], images["ribbon_3"],
    images["ribbon_4"], images["ribbon_5"], images["studio_hero"]
]

ribbon_configs = [
    {"num": "01 DEMO", "title": "Estudio Polanco", "desc": "12 Camas Allegro 2 · CDMX", "tag": "Alta Demanda", "img": available_assets[0]},
    {"num": "02 DEMO", "title": "Estudio Condesa", "desc": "Sala Principal · 18 Barras", "tag": "Waitlist Auto", "img": available_assets[1]},
    {"num": "03 DEMO", "title": "Estudio Roma Norte", "desc": "10 Camas Custom Nogal", "tag": "Bloqueo Atómico", "img": available_assets[2]},
    {"num": "04 DEMO", "title": "Cycling Juárez", "desc": "32 Bicis Stages SC3", "tag": "Check-in 1-Tap", "img": available_assets[3]},
    {"num": "05 DEMO", "title": "Shala Cuauhtémoc", "desc": "Sala Caliente · 24 Mats", "tag": "Stripe Connect", "img": available_assets[4]},
    {"num": "06 DEMO", "title": "Estudio San Pedro", "desc": "14 Reformers Peak · NL", "tag": "Ledger Directo", "img": available_assets[5]},
    {"num": "07 DEMO", "title": "Estudio Guadalajara", "desc": "Pilates Clásico & Reformer", "tag": "Waitlist Auto", "img": available_assets[6]},
    {"num": "08 DEMO", "title": "Movement Zapopan", "desc": "Entrenamiento Funcional Boutique", "tag": "Gestión Coaches", "img": available_assets[7]},
    {"num": "09 DEMO", "title": "Estudio Querétaro", "desc": "8 Camas Reformer Studio", "tag": "1-Tap Lobby", "img": available_assets[8]},
    {"num": "10 DEMO", "title": "Barre Studio Santa Fe", "desc": "20 Barras & Studio Pilates", "tag": "0% Comisión", "img": available_assets[9]},
    {"num": "11 DEMO", "title": "Hot Yoga Puebla", "desc": "Shala Infrarrojo · 20 Mats", "tag": "Bloqueo Atómico", "img": available_assets[10]},
    {"num": "12 DEMO", "title": "Estudio Mérida", "desc": "10 Reformers · Altabrisa", "tag": "Stripe Direct", "img": available_assets[11]}
]

ribbon_cards_html = ""
for idx, c in enumerate(ribbon_configs):
    ribbon_cards_html += f"""
      <div class="ribbon-card" id="ribbon-card-{idx}" data-idx="{idx}">
        <div class="ribbon-card-img" style="background-image: url('{c['img']}');">
          <div class="ribbon-card-overlay"></div>
          <div class="ribbon-card-badge">{c['num']}</div>
          <div class="ribbon-card-tag">{c['tag']}</div>
        </div>
        <div class="ribbon-card-body">
          <h4 class="ribbon-card-title">{c['title']}</h4>
          <p class="ribbon-card-desc">{c['desc']}</p>
        </div>
      </div>"""

discipline_cards_html = f"""
      <div class="discipline-card">
        <div class="discipline-img" style="background-image: url('{images["reformer_close"]}');"></div>
        <div class="discipline-info">
          <div class="discipline-tag">8 – 14 CAMAS</div>
          <h3 class="discipline-name">Pilates Reformer</h3>
          <p class="discipline-desc">Asignación nominal de máquina y rotación estricta de grupos pequeños.</p>
        </div>
      </div>
      <div class="discipline-card">
        <div class="discipline-img" style="background-image: url('{images["coach_guiding"]}');"></div>
        <div class="discipline-info">
          <div class="discipline-tag">15 – 25 PLAZAS</div>
          <h3 class="discipline-name">Barre & Mat Flow</h3>
          <p class="discipline-desc">Control ágil de barras, tapetes y listas de espera de alta rotación.</p>
        </div>
      </div>
      <div class="discipline-card">
        <div class="discipline-img" style="background-image: url('{images["studio_light"]}');"></div>
        <div class="discipline-info">
          <div class="discipline-tag">HOT ROOM & SHALA</div>
          <h3 class="discipline-name">Yoga & Sound Baths</h3>
          <p class="discipline-desc">Pases abiertos y workshops de fin de semana con cobros directos.</p>
        </div>
      </div>
      <div class="discipline-card">
        <div class="discipline-img" style="background-image: url('{images["class_action"]}');"></div>
        <div class="discipline-info">
          <div class="discipline-tag">30+ BICICLETAS</div>
          <h3 class="discipline-name">Indoor Cycling</h3>
          <p class="discipline-desc">Selección de número de bicicleta con check-in ultra-rápido en tablet.</p>
        </div>
      </div>
"""

part3_filled = part3.replace("<!-- RIBBON_CARDS_SLOT -->", ribbon_cards_html)
part3_filled = part3_filled.replace("<!-- DISCIPLINE_CARDS_SLOT -->", discipline_cards_html)
part3_filled = part3_filled.replace('id="webglFallbackCard"', f'id="webglFallbackCard" style="background-image: url(\'{images["studio_hero"]}\');"')

# Inyectar la sección de Workflow interactiva antes de la sección de Precios
part3_filled = part3_filled.replace('<section class="pricing-section"', f"{workflow_section}\n  <section class=\"pricing-section\"")

# CSS para wires y animaciones de flujo
wires_css = """
    @keyframes wireFlow {
      from { stroke-dashoffset: 24; }
      to { stroke-dashoffset: 0; }
    }
    .workflow-node {
      user-select: none;
      transition: transform 0.2s var(--ease-primary), box-shadow 0.2s var(--ease-primary);
    }
    .workflow-node:hover {
      transform: translateY(-3px);
      box-shadow: var(--shadow-deep-dark) !important;
    }
    .workflow-node.is-dragging {
      opacity: 0.95;
      cursor: grabbing !important;
      box-shadow: 0 20px 40px rgba(0,0,0,0.2) !important;
    }
    .workflow-node.active-pulse {
      border-color: var(--accent-orange) !important;
      box-shadow: 0 0 0 3px rgba(255, 85, 0, 0.25) !important;
    }
    #custom-cursor-label {
      position: absolute;
      top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      font-family: var(--font-mono);
      font-size: 0.65rem;
      font-weight: 800;
      color: #111;
      letter-spacing: 0.05em;
      pointer-events: none;
      display: none;
    }
"""

orchestrator_js = f"""
  <script>
    // Inyección de Three.js
    {three_min_js}
  </script>

  <script>
    // Inyección de Módulos de Movimiento y Renderizado (UX-03, UX-06, UX-07, UX-08)
    {cursor_js}
    {ribbon_js}
    {canvas_js}
    {reformer_js}

    // Inicialización del Orquestador Global de la Experiencia
    let cursorInstance, ribbonInstance, canvasInstance, reformerInstance;

    window.addEventListener('DOMContentLoaded', () => {{
      // 1. Cursor Contextual con Lerp
      cursorInstance = new ContextualCursor();

      // 2. Parabolic Ribbon con Momentum Drag e Inercia
      ribbonInstance = new ParabolicRibbon('conveyorViewport', 'ribbonTrack');

      // 3. Studio Workflow Canvas con Nodos y Cables SVG Bézier
      canvasInstance = new StudioWorkflowCanvas('workflowBoard');

      // 4. Showroom 3D Reformer con PBR y Detección WebGL
      reformerInstance = new ReformerStudioViewer('reformerCanvas', 'webglFallbackCard');
    }});

    // Controles para los botones del 3D Reformer
    function triggerCarriageGlide() {{
      if (reformerInstance) reformerInstance.glideCarriage();
    }}
    function toggleReformerSprings() {{
      if (reformerInstance) reformerInstance.toggleSprings();
    }}
    function resetReformerCamera() {{
      if (reformerInstance) reformerInstance.resetCamera();
    }}
  </script>
"""

# Reemplazar cursor div para agregar label dinámico
part3_filled = part3_filled.replace('<div id="custom-cursor"></div>', '<div id="custom-cursor"><span id="custom-cursor-label"></span></div>')

# Ensamblado Final
output_path = '/home/user/openbreak/landing_melius_style.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(part1)
    f.write(tokens_css)
    f.write(wires_css)
    f.write(part2)
    f.write(part3_filled)
    f.write(orchestrator_js)
    f.write(part4_logic)

print(f"Build V4 Masterpiece completed successfully! Output: {output_path}")
print(f"Total HTML file size: {len(open(output_path, 'r', encoding='utf-8').read())} bytes")
