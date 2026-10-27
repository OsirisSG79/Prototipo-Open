import json

with open('/home/user/openbreak/assets/data_uris.json', 'r', encoding='utf-8') as f:
    images = json.load(f)

with open('/home/user/openbreak/assets/three.min.js', 'r', encoding='utf-8') as f:
    three_min_js = f.read()

with open('/home/user/openbreak/templates/part1_head_css.html', 'r', encoding='utf-8') as f:
    part1 = f.read()

with open('/home/user/openbreak/templates/part2_css_rest.html', 'r', encoding='utf-8') as f:
    part2 = f.read()

with open('/home/user/openbreak/templates/part3_body_sections.html', 'r', encoding='utf-8') as f:
    part3 = f.read()

with open('/home/user/openbreak/templates/part4_js_logic.html', 'r', encoding='utf-8') as f:
    part4 = f.read()

# Mapeo exhaustivo y verificado con data_uris.json reales (OB-01, OB-02)
available_assets = [
    images["studio_hero"],
    images["studio_light"],
    images["studio_minimal"],
    images["reformer_close"],
    images["coach_guiding"],
    images["class_action"],
    images["ribbon_1"],
    images["ribbon_2"],
    images["ribbon_3"],
    images["ribbon_4"],
    images["ribbon_5"],
    images["studio_hero"]
]

# 12 tarjetas del ribbon con títulos descriptivos y honestos (OB-04: Casos de uso / configuraciones)
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
    # OB-11: Tarjetas con atributos semánticos limpios
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

# 4 Disciplinas con fotos reales
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

# Fallback visual HD para Reformer
part3_filled = part3_filled.replace('id="webglFallbackCard"', f'id="webglFallbackCard" style="background-image: url(\'{images["studio_hero"]}\');"')

output_path = '/home/user/openbreak/landing_melius_style.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(part1)
    f.write(part2)
    f.write(part3_filled)
    f.write("\n  <script>\n" + three_min_js + "\n  </script>\n")
    f.write(part4)

print("Assembly completed successfully. Output size:", len(open(output_path, 'r', encoding='utf-8').read()), "bytes.")
