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

img_reformer_1 = images.get("reformer_1", "")
img_reformer_2 = images.get("reformer_2", "")
img_reformer_3 = images.get("reformer_3", "")
img_coach_1 = images.get("coach_1", "")
img_coach_2 = images.get("coach_2", "")

cards_data = [
    {"num": "01 LIVE", "title": "Cima Studio Polanco", "desc": "12 Camas Allegro 2 · CDMX", "img": img_reformer_1, "tag": "98% Ocupación"},
    {"num": "02 LIVE", "title": "Marea Barre Condesa", "desc": "Sala Principal · 18 Barras", "img": img_coach_1, "tag": "Waitlist Auto"},
    {"num": "03 LIVE", "title": "Aura Reformer Roma Norte", "desc": "10 Camas Custom Nogal", "img": img_reformer_2, "tag": "Bloqueo Atómico"},
    {"num": "04 LIVE", "title": "Pulse Cycling Juárez", "desc": "32 Bicis Stages SC3", "img": img_coach_2, "tag": "Check-in 1-Tap"},
    {"num": "05 LIVE", "title": "Zenith Yoga Cuauhtémoc", "desc": "Shala Caliente · 24 Mats", "img": img_reformer_3, "tag": "0% Stripe"},
    {"num": "06 LIVE", "title": "Komorebi San Pedro", "desc": "14 Reformers Peak · NL", "img": img_reformer_1, "tag": "Ledger Directo"},
    {"num": "07 LIVE", "title": "Lina Studio Guadalajara", "desc": "Pilates Clásico & Reformer", "img": img_coach_1, "tag": "Waitlist Auto"},
    {"num": "08 LIVE", "title": "Soma Movement Zapopan", "desc": "Entrenamiento Funcional Boutique", "img": img_reformer_2, "tag": "99% Retención"},
    {"num": "09 LIVE", "title": "Vela Movement Querétaro", "desc": "8 Camas Reformer Studio", "img": img_coach_2, "tag": "1-Tap Lobby"},
    {"num": "10 LIVE", "title": "Néctar Barre Santa Fe", "desc": "20 Barras & Studio Pilates", "img": img_reformer_3, "tag": "0% Comisión"},
    {"num": "11 LIVE", "title": "Prana Hot Yoga Puebla", "desc": "Shala Infrarrojo · 20 Mats", "img": img_reformer_1, "tag": "Bloqueo Atómico"},
    {"num": "12 LIVE", "title": "Equilibrio Studio Mérida", "desc": "10 Reformers · Altabrisa", "img": img_coach_2, "tag": "Stripe Connect"}
]

ribbon_cards_html = ""
for idx, c in enumerate(cards_data):
    ribbon_cards_html += f"""
      <div class="ribbon-card" id="ribbon-card-{idx}" data-idx="{idx}" role="button" tabindex="0" aria-label="Estudio {c['title']}">
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
        <div class="discipline-img" style="background-image: url('{img_reformer_1}');"></div>
        <div class="discipline-info">
          <div class="discipline-tag">8 – 14 CAMAS</div>
          <h3 class="discipline-name">Pilates Reformer</h3>
          <p class="discipline-desc">Asignación nominal de máquina y rotación estricta de grupos pequeños.</p>
        </div>
      </div>
      <div class="discipline-card">
        <div class="discipline-img" style="background-image: url('{img_coach_1}');"></div>
        <div class="discipline-info">
          <div class="discipline-tag">15 – 25 PLAZAS</div>
          <h3 class="discipline-name">Barre & Mat Flow</h3>
          <p class="discipline-desc">Control ágil de barras, tapetes y listas de espera de alta rotación.</p>
        </div>
      </div>
      <div class="discipline-card">
        <div class="discipline-img" style="background-image: url('{img_reformer_2}');"></div>
        <div class="discipline-info">
          <div class="discipline-tag">HOT ROOM & SHALA</div>
          <h3 class="discipline-name">Yoga & Sound Baths</h3>
          <p class="discipline-desc">Pases abiertos y workshops de fin de semana con cobros directos.</p>
        </div>
      </div>
      <div class="discipline-card">
        <div class="discipline-img" style="background-image: url('{img_coach_2}');"></div>
        <div class="discipline-info">
          <div class="discipline-tag">30+ BICICLETAS</div>
          <h3 class="discipline-name">Indoor Cycling</h3>
          <p class="discipline-desc">Selección de número de bicicleta con check-in ultra-rápido en tablet.</p>
        </div>
      </div>
"""

part3_filled = part3.replace("<!-- RIBBON_CARDS_SLOT -->", ribbon_cards_html)
part3_filled = part3_filled.replace("<!-- DISCIPLINE_CARDS_SLOT -->", discipline_cards_html)

output_path = '/home/user/openbreak/landing_melius_style.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(part1)
    f.write(part2)
    f.write(part3_filled)
    f.write("\n  <script>\n" + three_min_js + "\n  </script>\n")
    f.write(part4)

print("Assembly completed successfully. Output size:", len(open(output_path, 'r', encoding='utf-8').read()), "bytes.")
