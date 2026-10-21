import json

with open('/home/user/openbreak/assets/data_uris.json') as f:
    data = json.load(f)

with open('/home/user/openbreak/landing_melius_style.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the bottom area of Hero with exact Melius search bar and category chips
old_prompt = '''      <div class="hero-prompt-pill">
        <div class="pill-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
        </div>
        <input type="text" class="pill-input" id="heroPromptInput" value="Simular: 2 alumnos reservando el último Reformer a las 07:00 AM">
        <button class="pill-action-btn" onclick="triggerSimulation()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
        </button>
      </div>'''

new_prompt = '''      <div style="display:flex; flex-direction:column; align-items:center; width:100%; max-width:480px; gap:12px;">
        <div class="hero-prompt-pill" style="width:100%; background:#1A1A1E; border:1px solid rgba(0,0,0,0.15); box-shadow:0 14px 35px rgba(0,0,0,0.12);">
          <div class="pill-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FF5500" stroke-width="2.2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
          </div>
          <input type="text" class="pill-input" id="heroPromptInput" style="font-size:0.88rem;" value="Simular: 2 alumnos reservando el último Reformer a las 07:00 AM">
          <button class="pill-action-btn" onclick="triggerSimulation()" title="Ejecutar en Canvas">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
          </button>
        </div>
        <div style="display:flex; gap:8px; align-items:center; font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#777;">
          <span>QUICK ACTIONS:</span>
          <span style="background:rgba(0,0,0,0.06); padding:3px 8px; border-radius:4px; cursor:pointer; color:#333; font-weight:600;" onclick="setQuickPrompt('Bloqueo atómico 8/8 Reformers')">Sobrecupo 0</span>
          <span style="background:rgba(0,0,0,0.06); padding:3px 8px; border-radius:4px; cursor:pointer; color:#333; font-weight:600;" onclick="setQuickPrompt('Cancelación tardía: retener crédito')">Ventana 6h</span>
          <span style="background:rgba(0,0,0,0.06); padding:3px 8px; border-radius:4px; cursor:pointer; color:#333; font-weight:600;" onclick="setQuickPrompt('Conciliación Stripe 0% comisión')">Stripe Direct</span>
        </div>
      </div>'''

html = html.replace(old_prompt, new_prompt)

# Add setQuickPrompt helper in javascript
quick_helper = '''
    function setQuickPrompt(text) {
      document.getElementById('heroPromptInput').value = 'Simular: ' + text;
      triggerSimulation();
    }
'''

if 'function setQuickPrompt' not in html:
    script_pos = html.rfind('function triggerSimulation()')
    if script_pos != -1:
        html = html[:script_pos] + quick_helper + '\n    ' + html[script_pos:]

# 2. Add realistic shadows and edge highlights to the 3D Reformer canvas
reformer_canvas_upgrade = '''      // Enhanced Shadows & Floor Reflection
      refRenderer.shadowMap.enabled = true;
      refRenderer.shadowMap.type = THREE.PCFSoftShadowMap;
      mainLight.castShadow = true;
      mainLight.shadow.mapSize.width = 1024;
      mainLight.shadow.mapSize.height = 1024;
      mainLight.shadow.camera.near = 0.5;
      mainLight.shadow.camera.far = 100;'''

if 'PCFSoftShadowMap' not in html:
    html = html.replace('refRenderer.shadowMap.enabled = true;', reformer_canvas_upgrade)

# 3. Enhance node cards in the Sticky Canvas with real Melius tags and models badges
node_upgrade = '''            <div class="node-title">Reserva Web Móvil (3-Tap)</div>
            <div class="node-desc">Sin descargar apps; directo por enlace de Instagram/WhatsApp.</div>'''

node_upgraded = '''            <div class="node-title" style="display:flex; justify-content:space-between; align-items:center;">
              <span>Reserva Web Móvil (3-Tap)</span>
              <span style="font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:#A1A1AA;">Latency: 12ms</span>
            </div>
            <div class="node-desc">Sin descargar apps; directo por enlace de Instagram/WhatsApp.</div>'''

html = html.replace(node_upgrade, node_upgraded)

with open('/home/user/openbreak/landing_melius_style.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Injected fine-tuned Melius details!")
