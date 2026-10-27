import json

with open('/home/user/openbreak/assets/data_uris.json') as f:
    data = json.load(f)

with open('/home/user/openbreak/landing_melius_style.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Build 16 cards (8 pairs looped) with real high-res images
cards_data = [
    (data['ribbon_1'], "Botanical Reformer Room"),
    (data['studio_hero'], "Technogym Reformer Line"),
    (data['coach_guiding'], "Instructor Guiding Flow"),
    (data['ribbon_3'], "Minimal Natural Studio"),
    (data['class_action'], "Power Reformer Group"),
    (data['studio_minimal'], "Mindfulness & Mat Sanctuary"),
    (data['ribbon_4'], "Monochrome Core Precision"),
    (data['ribbon_2'], "Bondi Studio Sunset"),
    (data['ribbon_5'], "Open Flow Movement Space"),
    (data['studio_light'], "Reformer Carriage Sunset"),
    (data['ribbon_1'], "Botanical Reformer Room"),
    (data['studio_hero'], "Technogym Reformer Line"),
    (data['coach_guiding'], "Instructor Guiding Flow"),
    (data['ribbon_3'], "Minimal Natural Studio"),
    (data['class_action'], "Power Reformer Group"),
    (data['studio_minimal'], "Mindfulness & Mat Sanctuary")
]

ribbon_cards_html = ""
for i, (img_uri, title) in enumerate(cards_data):
    ribbon_cards_html += f'''
        <div class="melius-continuous-card" data-index="{i}">
          <div class="card-inner-frame">
            <img src="{img_uri}" alt="{title}">
            <div class="card-overlay-tag">
              <span>0{ (i % 8) + 1 }</span>
              <span class="live-indicator">LIVE</span>
            </div>
          </div>
        </div>'''

# CSS for the continuous parabolic conveyor
continuous_ribbon_css = '''
    /* CONTINUOUS KINETIC CONVEYOR BELT (MELIUS EXACT MOTION) */
    .ribbon-stage {
      position: relative;
      width: 100vw;
      left: 50%;
      right: 50%;
      margin-left: -50vw;
      margin-right: -50vw;
      height: 380px;
      margin-top: 15px;
      margin-bottom: 25px;
      perspective: 1400px;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 5;
    }
    .ribbon-track {
      display: flex;
      gap: 16px;
      width: max-content;
      transform-style: preserve-3d;
      will-change: transform;
      cursor: grab;
    }
    .ribbon-track:active {
      cursor: grabbing;
    }

    .melius-continuous-card {
      flex: 0 0 195px;
      height: 270px;
      border-radius: 14px;
      overflow: hidden;
      position: relative;
      box-shadow: 0 16px 35px rgba(0, 0, 0, 0.16), 0 3px 8px rgba(0, 0, 0, 0.08);
      background: #000000;
      transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s;
      transform-origin: center center;
    }
    .melius-continuous-card:hover {
      transform: translateY(-12px) scale(1.08) translateZ(30px) !important;
      box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
      z-index: 50 !important;
    }

    .card-inner-frame {
      width: 100%;
      height: 100%;
      position: relative;
    }
    .card-inner-frame img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.5s ease;
    }
    .melius-continuous-card:hover .card-inner-frame img {
      transform: scale(1.08);
    }
    .card-overlay-tag {
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(15, 15, 18, 0.75);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 6px;
      padding: 3px 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      color: #FFFFFF;
      display: flex;
      align-items: center;
      gap: 6px;
      pointer-events: none;
    }
    .card-overlay-tag .live-indicator {
      font-size: 0.58rem;
      background: #FF5500;
      padding: 1px 4px;
      border-radius: 3px;
      font-weight: 700;
    }
'''

# Replace old ribbon-stage in html
start_ribbon = html.find('<div class="ribbon-stage"')
end_ribbon = html.find('</div>\n    </div>\n\n    <!-- SUBTEXT', start_ribbon) + len('</div>\n    </div>')

if start_ribbon != -1 and end_ribbon != -1:
    new_ribbon_html = f'''<div class="ribbon-stage" id="ribbonStage">
      <div class="ribbon-track" id="ribbonTrack">
{ribbon_cards_html}
      </div>
    </div>'''
    html = html[:start_ribbon] + new_ribbon_html + html[end_ribbon:]

# Insert continuous_ribbon_css
html = html.replace('.ribbon-stage {', continuous_ribbon_css + '\n    /* old ribbon stage replaced */ .old-ribbon {')

# Add Javascript for Infinite Parabolic Conveyor Motion with Scroll & Mouse Delta
conveyor_js = '''
    /* ====================================================================
       AUTHENTIC MELIUS CONTINUOUS CONVEYOR ENGINE (PHYSICS & PARABOLA)
       ==================================================================== */
    const track = document.getElementById('ribbonTrack');
    const stage = document.getElementById('ribbonStage');
    const cards = document.querySelectorAll('.melius-continuous-card');

    let scrollPos = 0;
    let baseSpeed = 0.85; // continuous autoscroll speed
    let targetSpeed = baseSpeed;
    let currentSpeed = baseSpeed;
    let isTrackHovered = false;
    let dragStartX = 0;
    let isDraggingTrack = false;
    let mouseTiltX = 0, mouseTiltY = 0;

    // Apply continuous parabolic arch based on screen center distance
    function updateParabolicArch() {
      const stageCenter = window.innerWidth / 2;

      cards.forEach(card => {
        const rect = card.getBoundingClientRect();
        const cardCenter = rect.left + rect.width / 2;
        const distFromCenter = (cardCenter - stageCenter) / (window.innerWidth / 2);
        
        // Parabolic equation: Y = dist^2, RotY = dist * angle
        const clampedDist = Math.max(-1.5, Math.min(1.5, distFromCenter));
        const rotY = clampedDist * 28; // curve outwards
        const transZ = Math.pow(Math.abs(clampedDist), 1.6) * 35; // parabola depth
        const rotX = -mouseTiltY * 0.4;

        if (!card.matches(':hover')) {
          card.style.transform = `rotateY(${rotY}deg) rotateX(${rotX}deg) translateZ(${transZ}px)`;
        }
      });
    }

    // Animation Loop
    function animateRibbonConveyor() {
      if (!isDraggingTrack) {
        scrollPos -= currentSpeed;
        
        // Loop when half of cards have scrolled
        const singleSetWidth = (195 + 16) * 8; // 8 unique cards
        if (Math.abs(scrollPos) >= singleSetWidth) {
          scrollPos += singleSetWidth;
        } else if (scrollPos > 0) {
          scrollPos -= singleSetWidth;
        }

        track.style.transform = `translateX(${scrollPos}px) rotateY(${mouseTiltX * 0.3}deg)`;
      }

      updateParabolicArch();
      requestAnimationFrame(animateRibbonConveyor);
    }

    // Scroll Acceleration
    let lastScrollY = window.scrollY;
    window.addEventListener('scroll', () => {
      const deltaY = window.scrollY - lastScrollY;
      lastScrollY = window.scrollY;
      // scroll adds kinetic momentum to the conveyor
      currentSpeed = baseSpeed + deltaY * 0.25;
      setTimeout(() => { currentSpeed = baseSpeed; }, 200);
    });

    // Mouse Tracking for 3D Tilt
    window.addEventListener('mousemove', (e) => {
      mouseTiltX = (e.clientX / window.innerWidth - 0.5) * 20;
      mouseTiltY = (e.clientY / window.innerHeight - 0.5) * 12;
    });

    // Drag Interaction
    stage.addEventListener('mousedown', (e) => {
      isDraggingTrack = true;
      dragStartX = e.clientX - scrollPos;
    });
    window.addEventListener('mouseup', () => { isDraggingTrack = false; });
    window.addEventListener('mousemove', (e) => {
      if (!isDraggingTrack) return;
      scrollPos = e.clientX - dragStartX;
      track.style.transform = `translateX(${scrollPos}px)`;
    });

    requestAnimationFrame(animateRibbonConveyor);
'''

# Replace old ribbon script with conveyor_js
html = html.replace('// 3. PARABOLIC RIBBON INTERACTIVE MOUSE & SCROLL PARALLAX', '// 3. CONTINUOUS PARABOLIC CONVEYOR ENGINE\n' + conveyor_js + '\n    /* old script disabled */ function oldRibbon() {')

with open('/home/user/openbreak/landing_melius_style.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Infinite Parabolic Conveyor Ribbon successfully integrated!")
