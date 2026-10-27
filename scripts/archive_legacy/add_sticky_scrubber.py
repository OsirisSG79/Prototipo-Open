from pathlib import Path

# Add sticky scrubber styles to part2_css_rest.html
p_css = Path('/home/user/openbreak/templates/part2_css_rest.html')
css_content = p_css.read_text(encoding='utf-8')

scrubber_css = """
    /* UX-05: True Melius Sticky Scrubber Stage (Multi-screen Scroll Sequence) */
    .melius-sticky-stage {
      position: relative;
      height: 240vh; /* Scroll runway */
      margin: 40px 0;
    }
    .melius-sticky-viewport {
      position: sticky;
      top: 80px;
      height: calc(100vh - 100px);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      overflow: hidden;
      border-radius: 28px;
      background: radial-gradient(circle at 50% 50%, rgba(20, 22, 25, 0.95), rgba(12, 13, 14, 0.98));
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 40px 100px rgba(0, 0, 0, 0.6);
      padding: 40px 20px;
    }
    .scrubber-progress-track {
      position: absolute;
      top: 24px;
      left: 50%;
      transform: translateX(-50%);
      width: 240px;
      height: 4px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 999px;
      overflow: hidden;
      z-index: 20;
    }
    .scrubber-progress-bar {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, var(--accent-green), var(--accent-orange));
      transition: width 0.1s linear;
    }
    .scrubber-step-indicator {
      position: absolute;
      top: 36px;
      left: 50%;
      transform: translateX(-50%);
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: #A1A1AA;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      z-index: 20;
    }
    @media (prefers-reduced-motion: reduce) {
      .melius-sticky-stage { height: auto !important; }
      .melius-sticky-viewport { position: static !important; height: auto !important; }
    }
"""

if ".melius-sticky-stage" not in css_content:
    css_content += scrubber_css
    p_css.write_text(css_content, encoding='utf-8')
    print("Added melius-sticky-stage CSS to part2_css_rest.html")

# Wrap solutions deck in part3_body_sections.html with sticky stage
p_body = Path('/home/user/openbreak/templates/part3_body_sections.html')
body_content = p_body.read_text(encoding='utf-8')

old_sol_open = """  <!-- SECCIÓN 3: LA SOLUCIÓN — 3D CASCADING DECK & SATÉLITES -->
  <section class="melius-solutions-deck-section" id="solucion">"""

new_sol_open = """  <!-- SECCIÓN 3: LA SOLUCIÓN — STICKY SCRUBBER & 3D CASCADING DECK -->
  <section class="melius-solutions-deck-section melius-sticky-stage" id="solucion">
    <div class="melius-sticky-viewport" id="stickyViewport">
      <div class="scrubber-progress-track" aria-hidden="true">
        <div class="scrubber-progress-bar" id="scrubberProgressBar"></div>
      </div>
      <div class="scrubber-step-indicator" id="scrubberStepIndicator">01 / RESERVA COORDINADA</div>"""

old_sol_close = """    </div>
  </section>"""

new_sol_close = """    </div>
    </div>
  </section>"""

if old_sol_open in body_content and "melius-sticky-stage" not in body_content:
    body_content = body_content.replace(old_sol_open, new_sol_open)
    body_content = body_content.replace(old_sol_close, new_sol_close, 1)
    p_body.write_text(body_content, encoding='utf-8')
    print("Wrapped solutions section with sticky scrubber runway in part3_body_sections.html")

# Add JS scrubber scroll driver in part4_js_logic.html
p_js = Path('/home/user/openbreak/templates/part4_js_logic.html')
js_content = p_js.read_text(encoding='utf-8')

scrubber_driver_js = """
    // UX-05 Melius-Grade Sticky Scrubber: Maps scroll progress directly to 3D deck stack & satellites
    function initMeliusStickyScrubber() {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      const stage = document.getElementById('solucion');
      const bar = document.getElementById('scrubberProgressBar');
      const indicator = document.getElementById('scrubberStepIndicator');
      if (!stage || !bar || !indicator) return;

      const steps = [
        "01 / RESERVA COORDINADA",
        "02 / LISTA DE ESPERA INTELIGENTE",
        "03 / LEDGER INMUTABLE DE CRÉDITOS",
        "04 / 0% COMISIÓN ABIERTA"
      ];

      let lastIdx = -1;

      window.addEventListener('scroll', () => {
        const rect = stage.getBoundingClientRect();
        const stageHeight = stage.offsetHeight - window.innerHeight;
        if (stageHeight <= 0) return;

        // Progress from 0.0 to 1.0 while passing through sticky stage
        const scrollDist = -rect.top;
        const progress = Math.max(0, Math.min(1, scrollDist / stageHeight));
        bar.style.width = (progress * 100) + '%';

        // Map progress to 4 discreet steps (0, 1, 2, 3)
        const stepIdx = Math.min(3, Math.floor(progress * 4));
        indicator.textContent = steps[stepIdx];

        if (stepIdx !== lastIdx) {
          lastIdx = stepIdx;
          if (typeof selectDeckCard === 'function') {
            selectDeckCard(stepIdx);
          }
        }
      }, { passive: true });
    }

    window.addEventListener('DOMContentLoaded', () => {
      initMeliusStickyScrubber();
    });
"""

if "initMeliusStickyScrubber" not in js_content:
    js_content += scrubber_driver_js
    p_js.write_text(js_content, encoding='utf-8')
    print("Added initMeliusStickyScrubber to part4_js_logic.html")

