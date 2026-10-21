import json

with open('/home/user/openbreak/assets/data_uris.json') as f:
    data = json.load(f)

with open('/home/user/openbreak/landing_melius_style.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the dark canvas section with Melius-authentic sticky split canvas
melius_split_canvas = f'''
  <!-- ======================================================================
       AUTHENTIC MELIUS CANVAS SHOWCASE: STICKY SPLIT SCREEN (CINEMATIC)
       ====================================================================== -->
  <section class="melius-canvas-sticky-section" id="canvas-section" style="background:#000000; position:relative; min-height:300vh;">
    
    <!-- STICKY FULLSCREEN VIEWPORT -->
    <div style="position:sticky; top:56px; height:calc(100vh - 56px); width:100%; display:grid; grid-template-columns:1fr 1fr; overflow:hidden;">
      
      <!-- LEFT PANE: CINEMATIC FULL-BLEED BACKGROUND WITH FLOATING PILL -->
      <div style="position:relative; width:100%; height:100%; overflow:hidden;">
        
        <!-- Background Imagery per vertical -->
        <div id="bg-reformer" class="canvas-split-bg" style="position:absolute; inset:0; opacity:1; transition:opacity 0.6s ease;">
          <img src="{data['studio_hero']}" style="width:100%; height:100%; object-fit:cover; filter:brightness(0.75);">
        </div>
        <div id="bg-concurrency" class="canvas-split-bg" style="position:absolute; inset:0; opacity:0; transition:opacity 0.6s ease;">
          <img src="{data['class_action']}" style="width:100%; height:100%; object-fit:cover; filter:brightness(0.7);">
        </div>
        <div id="bg-credits" class="canvas-split-bg" style="position:absolute; inset:0; opacity:0; transition:opacity 0.6s ease;">
          <img src="{data['studio_light']}" style="width:100%; height:100%; object-fit:cover; filter:brightness(0.75);">
        </div>
        <div id="bg-stripe" class="canvas-split-bg" style="position:absolute; inset:0; opacity:0; transition:opacity 0.6s ease;">
          <img src="{data['ribbon_2']}" style="width:100%; height:100%; object-fit:cover; filter:brightness(0.75);">
        </div>

        <div style="position:absolute; inset:0; background:linear-gradient(to right, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.85) 100%);"></div>

        <!-- FLOATING PROMPT PILL OVER LEFT CINEMATIC HERO (IDENTICAL TO MELIUS SCREENSHOT) -->
        <div style="position:absolute; top:28%; left:50%; transform:translate(-50%, -50%); width:88%; max-width:440px; z-index:20;">
          
          <!-- Category Tabs Pill on top -->
          <div style="background:rgba(20,20,24,0.92); border:1px solid rgba(255,255,255,0.14); backdrop-filter:blur(16px); border-radius:12px; padding:4px; display:flex; gap:3px; margin-bottom:12px;">
            <button class="m-pill-tab active" onclick="setCanvasSlide(0)" style="flex:1; border:none; background:#FF5500; color:#fff; font-family:'Plus Jakarta Sans',sans-serif; font-size:0.75rem; font-weight:700; padding:6px 8px; border-radius:8px; cursor:pointer;">Reformer</button>
            <button class="m-pill-tab" onclick="setCanvasSlide(1)" style="flex:1; border:none; background:transparent; color:#A1A1AA; font-family:'Plus Jakarta Sans',sans-serif; font-size:0.75rem; font-weight:600; padding:6px 8px; border-radius:8px; cursor:pointer;">Concurrencia</button>
            <button class="m-pill-tab" onclick="setCanvasSlide(2)" style="flex:1; border:none; background:transparent; color:#A1A1AA; font-family:'Plus Jakarta Sans',sans-serif; font-size:0.75rem; font-weight:600; padding:6px 8px; border-radius:8px; cursor:pointer;">Créditos</button>
            <button class="m-pill-tab" onclick="setCanvasSlide(3)" style="flex:1; border:none; background:transparent; color:#A1A1AA; font-family:'Plus Jakarta Sans',sans-serif; font-size:0.75rem; font-weight:600; padding:6px 8px; border-radius:8px; cursor:pointer;">0% Stripe</button>
          </div>

          <!-- Prompt description box with round arrow -->
          <div style="background:rgba(24,24,28,0.95); border:1px solid rgba(255,255,255,0.12); backdrop-filter:blur(20px); border-radius:14px; padding:12px 16px; display:flex; align-items:center; justify-content:space-between; gap:12px; box-shadow:0 20px 40px rgba(0,0,0,0.7);">
            <div style="display:flex; align-items:center; gap:10px;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FF5500" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
              <span id="canvasPromptText" style="font-size:0.86rem; color:#fff; font-weight:500;">Reservar último Reformer a las 07:00 AM con Mariana Ramos...</span>
            </div>
            <button onclick="triggerSimulation()" style="width:32px; height:32px; border-radius:50%; background:#3F3F46; border:none; color:#fff; display:flex; align-items:center; justify-content:center; cursor:pointer; flex-shrink:0;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>

        </div>

      </div>

      <!-- RIGHT PANE: INFINITE DOT-GRID WORKSPACE BOARD WITH LIVE NODES & BEZIER WIRES -->
      <div style="position:relative; width:100%; height:100%; background:#09090C; overflow:hidden; border-left:1px solid rgba(255,255,255,0.1);">
        
        <!-- Dot Grid Pattern -->
        <div style="position:absolute; inset:0; background-size:24px 24px; background-image:radial-gradient(rgba(255,255,255,0.08) 1px, transparent 1px); pointer-events:none;"></div>

        <!-- Telemetry Pill Top Right -->
        <div style="position:absolute; top:20px; right:24px; background:rgba(20,20,24,0.85); border:1px solid rgba(255,255,255,0.1); backdrop-filter:blur(10px); padding:6px 14px; border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#A1A1AA; display:flex; align-items:center; gap:8px; z-index:15;">
          <span style="width:7px; height:7px; border-radius:50%; background:#10B981; box-shadow:0 0 8px #10B981;"></span>
          <span id="canvasTelemetryText">POSTGRES READ COMMITTED · IDEMPOTENT</span>
        </div>

        <!-- SVG Live Connection Wires -->
        <svg class="canvas-wires-layer" id="wiresSvg" style="position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:5;">
          <path id="wire-1-2" d="" stroke="rgba(255, 255, 255, 0.35)" stroke-width="2" fill="none" stroke-dasharray="5,5"/>
          <path id="wire-2-3" d="" stroke="rgba(255, 255, 255, 0.35)" stroke-width="2" fill="none" stroke-dasharray="5,5"/>
          <path id="wire-3-4" d="" stroke="rgba(255, 85, 0, 0.85)" stroke-width="2.5" fill="none"/>
        </svg>

        <!-- NODE 1 (DRAGGABLE) -->
        <div class="graph-node active-node" id="node-1" style="left:30px; top:60px; width:260px;">
          <div class="node-header">
            <span>NODE // 01</span>
            <span class="node-pill pill-booking">STUDENT UI</span>
          </div>
          <div class="node-content">
            <div class="node-title">Reserva Móvil en 3 Toques</div>
            <div class="node-desc">Sin descargar apps; directo por enlace de Instagram/WhatsApp.</div>
            <div class="node-preview-media" style="height:120px;">
              <img src="{data['coach_guiding']}">
            </div>
          </div>
          <div class="node-port port-right" id="p1-out"></div>
        </div>

        <!-- NODE 2 (DRAGGABLE) -->
        <div class="graph-node" id="node-2" style="left:330px; top:40px; width:260px;">
          <div class="node-port port-left" id="p2-in"></div>
          <div class="node-header">
            <span>NODE // 02</span>
            <span class="node-pill pill-atomic">ATOMIC LOCK</span>
          </div>
          <div class="node-content">
            <div class="node-title">Bloqueo Atómico SQL</div>
            <div class="node-desc">0 Sobrecupos en sala física.</div>
            <div class="node-code" style="font-size:0.68rem; padding:8px;">
              <span style="color:#38BDF8;">SELECT</span> * <span style="color:#38BDF8;">FROM</span> spots<br>
              <span style="color:#F87171;">FOR UPDATE;</span><br>
              <span style="color:#4ADE80;">// 0 Sobrecupos</span>
            </div>
          </div>
          <div class="node-port port-right" id="p2-out"></div>
        </div>

        <!-- NODE 3 (DRAGGABLE) -->
        <div class="graph-node" id="node-3" style="left:50px; top:360px; width:260px;">
          <div class="node-port port-left" id="p3-in"></div>
          <div class="node-header">
            <span>NODE // 03</span>
            <span class="node-pill pill-credits">CREDIT AUDIT</span>
          </div>
          <div class="node-content">
            <div class="node-title">Bitácora Inmutable</div>
            <div class="node-desc">Resta 1 crédito. Repone si cancela >6h antes.</div>
            <div class="node-preview-media" style="height:110px;">
              <img src="{data['studio_light']}">
            </div>
          </div>
          <div class="node-port port-right" id="p3-out"></div>
        </div>

        <!-- NODE 4 (DRAGGABLE) -->
        <div class="graph-node" id="node-4" style="left:340px; top:370px; width:260px;">
          <div class="node-port port-left" id="p4-in"></div>
          <div class="node-header">
            <span>NODE // 04</span>
            <span class="node-pill pill-stripe">STRIPE 0% FEE</span>
          </div>
          <div class="node-content">
            <div class="node-title">Cobro Directo 0% Fee</div>
            <div class="node-desc">El 100% de tus ventas va a tu banco.</div>
            <div class="node-code" style="font-size:0.68rem; padding:8px;">
              Studio Fee: <span style="color:#4ADE80; font-weight:700;">0.00%</span><br>
              Stripe Connect: <span style="color:#FACC15;">Direct</span>
            </div>
          </div>
        </div>

      </div>

    </div>
  </section>
'''

# Replace old canvas-section
start_pos = html.find('<section class="canvas-section"')
end_pos = html.find('</section>', start_pos) + len('</section>')

if start_pos != -1 and end_pos != -1:
    html = html[:start_pos] + melius_split_canvas + html[end_pos:]

# Add slider script
slider_script = '''
    /* ====================================================================
       AUTHENTIC MELIUS CANVAS SPLIT SLIDER & SCROLL SYNC
       ==================================================================== */
    const slideData = [
      {
        bgId: 'bg-reformer',
        prompt: 'Reservar último Reformer a las 07:00 AM con Mariana Ramos...',
        telemetry: 'POSTGRES READ COMMITTED · IDEMPOTENT'
      },
      {
        bgId: 'bg-concurrency',
        prompt: 'Test Concurrencia: 2 alumnos intentan reservar Reformer #08...',
        telemetry: 'ROW LOCK ACQUIRED · FOR UPDATE ACTIVE'
      },
      {
        bgId: 'bg-credits',
        prompt: 'Alumno cancela a las 11:00 AM (8 hrs antes) -> Reintegrar crédito...',
        telemetry: 'POLICY 6H PASSED · CREDIT RESTORED #0912'
      },
      {
        bgId: 'bg-stripe',
        prompt: 'Comprar Paquete 10 Clases ($1,900 MXN) -> Transferencia Directa...',
        telemetry: 'STRIPE WEBHOOK 200 OK · 0% PLATFORM CUT'
      }
    ];

    function setCanvasSlide(idx) {
      document.querySelectorAll('.canvas-split-bg').forEach(el => el.style.opacity = '0');
      document.querySelectorAll('.m-pill-tab').forEach((b, i) => {
        b.style.background = i === idx ? '#FF5500' : 'transparent';
        b.style.color = i === idx ? '#FFFFFF' : '#A1A1AA';
      });

      const s = slideData[idx];
      const bg = document.getElementById(s.bgId);
      if (bg) bg.style.opacity = '1';
      document.getElementById('canvasPromptText').innerText = s.prompt;
      document.getElementById('canvasTelemetryText').innerText = s.telemetry;

      // Focus corresponding node
      const nodes = [document.getElementById('node-1'), document.getElementById('node-2'), document.getElementById('node-3'), document.getElementById('node-4')];
      nodes.forEach((n, i) => {
        if (i === idx) n.classList.add('active-node');
        else n.classList.remove('active-node');
      });
    }

    // Scroll listener for sticky canvas section
    window.addEventListener('scroll', () => {
      const section = document.getElementById('canvas-section');
      if (!section) return;
      const rect = section.getBoundingClientRect();
      const progress = -rect.top / (rect.height - window.innerHeight);
      if (progress >= 0 && progress <= 1) {
        const slideIdx = Math.min(3, Math.floor(progress * 4));
        setCanvasSlide(slideIdx);
      }
    });
'''

# Insert slider_script before closing script
script_end = html.rfind('</script>')
if script_end != -1:
    html = html[:script_end] + slider_script + '\n' + html[script_end:]

# Replace canvasBoard reference for drag boundary
html = html.replace("const board = document.getElementById('canvasBoard');", "const board = document.getElementById('wiresSvg').parentElement;")
html = html.replace("const boardRect = document.getElementById('canvasBoard').getBoundingClientRect();", "const boardRect = document.getElementById('wiresSvg').parentElement.getBoundingClientRect();")

with open('/home/user/openbreak/landing_melius_style.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Canvas successfully upgraded to authentic Melius Sticky Split Canvas!")
