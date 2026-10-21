import json

with open('/home/user/openbreak/assets/data_uris.json') as f:
    data = json.load(f)

with open('/home/user/openbreak/landing_melius_style.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Build the 3D Parabolic Ribbon Cards exactly as image-2.png
# Total 12 cards with deep parabolic perspective and live glowing tags
ribbon_cards_data = [
    (data['ribbon_1'], "01", "Botanical Reformer", "Mat & Cadillac"),
    (data['studio_hero'], "02", "Technogym Precision", "Reformer Line"),
    (data['coach_guiding'], "03", "Private Guided Flow", "Cadillac Core"),
    (data['ribbon_3'], "04", "Minimal Sanctuary", "Yoga & Meditation"),
    (data['class_action'], "05", "Power Reformer Flow", "Group Intensity"),
    (data['studio_minimal'], "06", "Sculpt & Movement", "Barre Alignment"),
    (data['ribbon_4'], "07", "Monochrome Precision", "Tower & Springs"),
    (data['ribbon_2'], "08", "Bondi Studio Design", "High-End Architecture"),
    (data['ribbon_5'], "09", "Open Flow Space", "Functional Reformer"),
    (data['studio_light'], "10", "Sunset Flow Room", "Mind & Breath"),
    (data['ribbon_1'], "11", "Botanical Reformer", "Mat & Cadillac"),
    (data['studio_hero'], "12", "Technogym Precision", "Reformer Line"),
]

ribbon_cards_markup = ""
for img, num, title, sub in ribbon_cards_data:
    ribbon_cards_markup += f'''
        <div class="melius-ribbon-card" onclick="onRibbonCardClick(this)">
          <div class="m-card-inner">
            <img src="{img}" alt="{title}">
            <div class="m-card-badge">
              <span>{num}</span>
              <span class="m-live-dot">LIVE</span>
            </div>
            <div class="m-card-caption">
              <strong>{title}</strong>
              <span>{sub}</span>
            </div>
          </div>
        </div>'''

# Build 3D Solutions Stack Deck (Image-1.png exact replica)
solutions_stack_markup = f'''
  <!-- ======================================================================
       SOLUTIONS: 3D INTERACTIVE CARD DECK & FLOATING SATELLITES (IMAGE-1 EXACT)
       ====================================================================== -->
  <section class="melius-solutions-deck-section" id="solutions" style="background:#ECEAE4; padding:120px 24px 140px; position:relative; overflow:hidden; border-top:1px solid rgba(0,0,0,0.08);">
    
    <!-- Subtle Dot Grid in Background -->
    <div style="position:absolute; inset:0; background-size:24px 24px; background-image:radial-gradient(rgba(0,0,0,0.06) 1px, transparent 1px); pointer-events:none;"></div>

    <div style="max-width:1300px; margin:0 auto; position:relative; z-index:10;">
      
      <div style="text-align:center; margin-bottom:50px;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#FF5500; text-transform:uppercase; letter-spacing:0.12em; margin-bottom:12px;">
          Solutions By Movement Vertical
        </div>
        <h2 style="font-family:'Newsreader',serif; font-size:clamp(2.6rem, 5vw, 3.8rem); font-weight:400; letter-spacing:-0.03em; color:#111;">
          Calibrado para el modelo operativo de tu estudio.
        </h2>
        <p style="color:#666; font-size:1.05rem; max-width:640px; margin:12px auto 0;">
          Haz clic en la baraja para alternar la disciplina o interactúa con las estaciones satélite alrededor del mazo 3D.
        </p>
      </div>

      <!-- THE 3D DECK ARENA WITH FLOATING SATELLITES -->
      <div class="solutions-deck-arena" id="deckArena">
        
        <!-- SATELLITE 1 (TOP-LEFT): STORYBOARDS / PROGRAMACIÓN -->
        <div class="satellite-card sat-top-left" onclick="selectDeckCard(0)">
          <div class="sat-badge">Programación</div>
          <img src="{data['ribbon_1']}" alt="Horarios y Cupos">
          <div class="sat-footer">Horarios & Cupos</div>
        </div>

        <!-- SATELLITE 2 (TOP-RIGHT): AI SHORTS / CHECK-IN MÓVIL -->
        <div class="satellite-card sat-top-right" onclick="selectDeckCard(1)">
          <div class="sat-badge">Check-in 1-Tap</div>
          <img src="{data['coach_guiding']}" alt="Recepción Móvil">
          <div class="sat-footer">Recepción QR</div>
        </div>

        <!-- SATELLITE 3 (BOTTOM-LEFT): LOOKBOOKS / PAQUETES -->
        <div class="satellite-card sat-bottom-left" onclick="selectDeckCard(2)">
          <div class="sat-badge">Créditos</div>
          <img src="{data['ribbon_3']}" alt="Paquetes y Membresías">
          <div class="sat-footer">Saldo Inmutable</div>
        </div>

        <!-- SATELLITE 4 (BOTTOM-RIGHT): REFERENCE BOARDS / CONCILIACIÓN -->
        <div class="satellite-card sat-bottom-right" onclick="selectDeckCard(3)">
          <div class="sat-badge">Stripe Direct</div>
          <img src="{data['ribbon_4']}" alt="0% Comisión">
          <div class="sat-footer">0% Fee Ventas</div>
        </div>

        <!-- THE 3D CARD STACK (MAIN CENTER PIECE) -->
        <div class="deck-3d-stack" id="mainDeckStack" onclick="cycleDeckStack()">
          
          <!-- Card 1 (Reformer Studios) -->
          <div class="deck-card active-top" id="deck-card-0" data-idx="0">
            <div class="deck-media">
              <img src="{data['studio_hero']}" alt="Reformer Pilates Studio">
              <div class="deck-brand-stamp">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                <span>OPEN BREAK</span>
              </div>
              <div class="deck-floating-tags">
                <span class="d-tag">8-12 Reformers</span>
                <span class="d-tag">Waitlist Auto</span>
                <span class="d-tag">Bloqueo Atómico</span>
              </div>
            </div>
            <div class="deck-caption">
              <h3>Reformer & Cadillac Pilates</h3>
              <p>Control riguroso de máquinas individuales. Si un alumno cancela a tiempo (>6h), el lugar se asigna automáticamente al siguiente en la lista sin intervención de recepción.</p>
            </div>
          </div>

          <!-- Card 2 (Barre & Movement) -->
          <div class="deck-card stack-layer-1" id="deck-card-1" data-idx="1">
            <div class="deck-media">
              <img src="{data['class_action']}" alt="Barre & Flow">
              <div class="deck-brand-stamp">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                <span>OPEN BREAK</span>
              </div>
              <div class="deck-floating-tags">
                <span class="d-tag">Aforo Flexible</span>
                <span class="d-tag">Comisiones Coach</span>
                <span class="d-tag">Check-in 1-Tap</span>
              </div>
            </div>
            <div class="deck-caption">
              <h3>Barre, Danza & Mat Flow</h3>
              <p>Gestión de salas de mayor aforo con niveles diferenciados y liquidación automática de honorarios por alumno asistente o cuota fija por sesión.</p>
            </div>
          </div>

          <!-- Card 3 (Yoga & Mindfulness) -->
          <div class="deck-card stack-layer-2" id="deck-card-2" data-idx="2">
            <div class="deck-media">
              <img src="{data['studio_minimal']}" alt="Yoga Studio">
              <div class="deck-brand-stamp">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                <span>OPEN BREAK</span>
              </div>
              <div class="deck-floating-tags">
                <span class="d-tag">Pases Drop-in</span>
                <span class="d-tag">Talleres Weekend</span>
                <span class="d-tag">Multi-Sede</span>
              </div>
            </div>
            <div class="deck-caption">
              <h3>Yoga, Breathwork & Sound Baths</h3>
              <p>Membresías híbridas, venta de pases sueltos sin registro engorroso y conciliación bancaria instantánea exportable a CSV.</p>
            </div>
          </div>

          <!-- Card 4 (Functional & Performance) -->
          <div class="deck-card stack-layer-3" id="deck-card-3" data-idx="3">
            <div class="deck-media">
              <img src="{data['ribbon_2']}" alt="Functional Training">
              <div class="deck-brand-stamp">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                <span>OPEN BREAK</span>
              </div>
              <div class="deck-floating-tags">
                <span class="d-tag">Circuitos</span>
                <span class="d-tag">Estaciones</span>
                <span class="d-tag">0% Fee Stripe</span>
              </div>
            </div>
            <div class="deck-caption">
              <h3>Entrenamiento Funcional & HIIT</h3>
              <p>Reserva por turnos de estación, penalización automática por inasistencia y cobros directos sin comisiones ocultas.</p>
            </div>
          </div>

        </div>

      </div>

      <!-- INSTRUCTION HINT -->
      <div style="text-align:center; margin-top:24px; font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#777;">
        <span>TIP: HAZ CLIC EN LA BARAJA CENTRAL O EN CUALQUIER SATÉLITE PARA VER LA ANIMACIÓN 3D</span>
      </div>

    </div>
  </section>
'''

# Deck CSS and Ribbon styling
deck_and_ribbon_css = '''
    /* ======================================================================
       PARABOLIC CURVED HERO RIBBON (IMAGE-2 EXACT SPECIFICATION)
       ====================================================================== */
    .ribbon-stage {
      position: relative;
      width: 100vw;
      left: 50%;
      right: 50%;
      margin-left: -50vw;
      margin-right: -50vw;
      height: 420px;
      margin-top: 20px;
      margin-bottom: 25px;
      perspective: 1200px;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 5;
    }
    .ribbon-track {
      display: flex;
      gap: 18px;
      width: max-content;
      transform-style: preserve-3d;
      will-change: transform;
      cursor: grab;
      align-items: center;
    }
    .ribbon-track:active { cursor: grabbing; }

    .melius-ribbon-card {
      flex: 0 0 215px;
      height: 300px;
      border-radius: 14px;
      overflow: hidden;
      position: relative;
      background: #000000;
      box-shadow: 0 18px 40px rgba(0, 0, 0, 0.2), 0 4px 10px rgba(0, 0, 0, 0.1);
      transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s;
      transform-origin: center center;
    }
    .melius-ribbon-card:hover {
      transform: translateY(-16px) scale(1.1) translateZ(40px) !important;
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.35);
      z-index: 50 !important;
    }
    .m-card-inner {
      width: 100%;
      height: 100%;
      position: relative;
    }
    .m-card-inner img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.5s ease;
    }
    .melius-ribbon-card:hover .m-card-inner img {
      transform: scale(1.08);
    }
    .m-card-badge {
      position: absolute;
      top: 12px;
      left: 12px;
      background: rgba(15, 15, 18, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 6px;
      padding: 3px 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      color: #FFFFFF;
      display: flex;
      align-items: center;
      gap: 6px;
      pointer-events: none;
    }
    .m-live-dot {
      font-size: 0.6rem;
      background: #FF5500;
      color: #fff;
      padding: 1px 4px;
      border-radius: 3px;
      font-weight: 700;
    }
    .m-card-caption {
      position: absolute;
      bottom: 0; left: 0; right: 0;
      padding: 24px 12px 10px;
      background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, transparent 100%);
      color: #FFFFFF;
      pointer-events: none;
    }
    .m-card-caption strong {
      display: block;
      font-size: 0.84rem;
      font-weight: 700;
    }
    .m-card-caption span {
      font-size: 0.72rem;
      color: #C4C4CC;
    }

    /* ======================================================================
       3D SOLUTIONS STACK DECK & FLOATING SATELLITES (IMAGE-1 EXACT SPEC)
       ====================================================================== */
    .solutions-deck-arena {
      position: relative;
      width: 100%;
      height: 640px;
      margin: 0 auto;
      perspective: 1200px;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    /* Floating Satellites */
    .satellite-card {
      position: absolute;
      width: 175px;
      height: 195px;
      background: #FFFFFF;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 16px 35px rgba(0, 0, 0, 0.12), 0 2px 6px rgba(0, 0, 0, 0.06);
      cursor: pointer;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 5;
    }
    .satellite-card:hover {
      transform: translateY(-8px) scale(1.05);
      box-shadow: 0 24px 45px rgba(0, 0, 0, 0.2);
    }
    .satellite-card img {
      width: 100%;
      height: 145px;
      object-fit: cover;
      display: block;
    }
    .sat-badge {
      position: absolute;
      top: 8px;
      right: 8px;
      background: #FFF066;
      color: #000000;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.68rem;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    }
    .sat-footer {
      padding: 10px;
      font-size: 0.78rem;
      font-weight: 700;
      color: #111111;
      text-align: center;
    }

    .sat-top-left { top: 30px; left: calc(50% - 480px); }
    .sat-top-right { top: 30px; right: calc(50% - 480px); }
    .sat-bottom-left { bottom: 40px; left: calc(50% - 460px); }
    .sat-bottom-right { bottom: 40px; right: calc(50% - 460px); }

    @media (max-width: 1100px) {
      .sat-top-left { left: 20px; }
      .sat-top-right { right: 20px; }
      .sat-bottom-left { left: 20px; }
      .sat-bottom-right { right: 20px; }
    }
    @media (max-width: 768px) {
      .satellite-card { display: none; }
    }

    /* 3D Main Stack */
    .deck-3d-stack {
      position: relative;
      width: 420px;
      height: 520px;
      transform-style: preserve-3d;
      cursor: pointer;
    }

    .deck-card {
      position: absolute;
      width: 100%;
      height: 100%;
      background: #FFFFFF;
      border-radius: 18px;
      overflow: hidden;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.16), 0 4px 15px rgba(0, 0, 0, 0.08);
      transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      flex-direction: column;
    }
    .deck-media {
      width: 100%;
      height: 330px;
      position: relative;
      overflow: hidden;
    }
    .deck-media img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .deck-brand-stamp {
      position: absolute;
      top: 14px;
      left: 14px;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      color: #FFFFFF;
      padding: 5px 10px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.04em;
    }
    .deck-floating-tags {
      position: absolute;
      top: 14px;
      right: 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      align-items: flex-end;
    }
    .d-tag {
      background: #FFF066;
      color: #000000;
      font-size: 0.7rem;
      font-weight: 700;
      padding: 4px 9px;
      border-radius: 4px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    .deck-caption {
      padding: 22px 24px;
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      background: #FFFFFF;
    }
    .deck-caption h3 {
      font-family: 'Newsreader', serif;
      font-size: 1.6rem;
      font-weight: 500;
      letter-spacing: -0.02em;
      color: #111111;
      margin-bottom: 8px;
    }
    .deck-caption p {
      font-size: 0.86rem;
      color: #555555;
      line-height: 1.5;
    }

    /* 3D Stack Layer Depth Classes */
    .deck-card.active-top {
      z-index: 10;
      transform: translate3d(0, 0, 0);
      opacity: 1;
    }
    .deck-card.stack-layer-1 {
      z-index: 9;
      transform: translate3d(0, -32px, -45px) scale(0.96);
      opacity: 0.95;
    }
    .deck-card.stack-layer-2 {
      z-index: 8;
      transform: translate3d(0, -64px, -90px) scale(0.92);
      opacity: 0.88;
    }
    .deck-card.stack-layer-3 {
      z-index: 7;
      transform: translate3d(0, -96px, -135px) scale(0.88);
      opacity: 0.78;
    }
'''

# Replace old ribbon html and replace old solutions section
old_ribbon_marker = '<div class="ribbon-stage"'
end_ribbon_marker = '<!-- SUBTEXT & SEARCH PILL -->'
r_start = html.find(old_ribbon_marker)
r_end = html.find(end_ribbon_marker)

if r_start != -1 and r_end != -1:
    new_ribbon_stage = f'''<div class="ribbon-stage" id="ribbonStage">
      <div class="ribbon-track" id="ribbonTrack">
{ribbon_cards_markup}
      </div>
    </div>\n\n    '''
    html = html[:r_start] + new_ribbon_stage + html[r_end:]

# Replace old solutions section with new 3D Stack Deck section
sol_start = html.find('<section class="solutions-section"')
sol_end = html.find('</section>', sol_start) + len('</section>')

if sol_start != -1 and sol_end != -1:
    html = html[:sol_start] + solutions_stack_markup + html[sol_end:]

# Inject new CSS
css_inject_pos = html.find('</style>')
if css_inject_pos != -1:
    html = html[:css_inject_pos] + '\n' + deck_and_ribbon_css + '\n' + html[css_inject_pos:]

# Inject Javascript for 3D Deck Stack Cycling & Satellite Interaction
deck_js = '''
    /* ====================================================================
       AUTHENTIC MELIUS 3D SOLUTIONS DECK INTERACTION (IMAGE-1 EXACT)
       ==================================================================== */
    let currentDeckIndex = 0;
    const totalDeckCards = 4;

    function updateDeckClasses() {
      for (let i = 0; i < totalDeckCards; i++) {
        const card = document.getElementById('deck-card-' + i);
        if (!card) continue;

        card.className = 'deck-card';
        const relativePos = (i - currentDeckIndex + totalDeckCards) % totalDeckCards;

        if (relativePos === 0) {
          card.classList.add('active-top');
        } else if (relativePos === 1) {
          card.classList.add('stack-layer-1');
        } else if (relativePos === 2) {
          card.classList.add('stack-layer-2');
        } else {
          card.classList.add('stack-layer-3');
        }
      }
    }

    function cycleDeckStack() {
      const topCard = document.getElementById('deck-card-' + currentDeckIndex);
      if (topCard) {
        // Discard card forward and return to back
        topCard.style.transform = 'translate3d(0, 120px, 80px) rotateX(15deg) scale(1.05)';
        topCard.style.opacity = '0';

        setTimeout(() => {
          currentDeckIndex = (currentDeckIndex + 1) % totalDeckCards;
          updateDeckClasses();
          topCard.style.opacity = '';
        }, 220);
      }
    }

    function selectDeckCard(targetIdx) {
      currentDeckIndex = targetIdx % totalDeckCards;
      updateDeckClasses();
    }

    function onRibbonCardClick(cardEl) {
      cardEl.style.transform = 'translateY(-20px) scale(1.15) translateZ(60px)';
      setTimeout(() => {
        cardEl.style.transform = '';
      }, 400);
    }
'''

# Add deck_js before closing script
js_end = html.rfind('</script>')
if js_end != -1:
    html = html[:js_end] + '\n' + deck_js + '\n' + html[js_end:]

with open('/home/user/openbreak/landing_melius_style.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Masterpiece upgrade with Image-1 (3D Solutions Stack Deck) and Image-2 (Parabolic Ribbon) successfully applied!")
