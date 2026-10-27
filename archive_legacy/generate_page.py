import json

with open('/home/user/openbreak/assets/data_uris.json') as f:
    data = json.load(f)

# Load base HTML template
with open('/home/user/openbreak/landing_melius_style.html', 'r', encoding='utf-8') as f:
    current_html = f.read()

# Let's insert the Custom Cursor and the 3D Reformer section
reformer_section = f'''
  <!-- ======================================================================
       INTERACTIVE 3D PILATES REFORMER ENGINE (PARAMETRIC WEBGL SHOWCASE)
       ====================================================================== -->
  <section class="reformer-3d-section" id="reformer-3d" style="background:#070709; color:#fff; padding:90px 24px 100px; position:relative; overflow:hidden; border-top:1px solid rgba(255,255,255,0.08);">
    <div style="max-width:1360px; margin:0 auto; display:grid; grid-template-columns:1fr 1.35fr; gap:40px; align-items:center; position:relative; z-index:5;">
      
      <!-- Info Col -->
      <div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#FF5500; text-transform:uppercase; letter-spacing:0.12em; margin-bottom:12px;">
          Hardware-Level Precision · 3D Digital Twin
        </div>
        <h2 style="font-size:2.6rem; font-weight:800; letter-spacing:-0.035em; line-height:1.1; margin-bottom:16px;">
          Control visual y atómico de cada máquina en sala.
        </h2>
        <p style="color:#94949E; font-size:1rem; line-height:1.6; margin-bottom:28px;">
          En Pilates Reformer cada equipo es un activo de alto costo. Nuestro motor digitaliza cada carro deslizante, barra de pies y resortes, sincronizándolos con el inventario físico en tiempo real.
        </p>

        <div style="display:flex; flex-direction:column; gap:16px; margin-bottom:32px;">
          <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:14px 18px; display:flex; gap:14px;">
            <div style="width:32px; height:32px; border-radius:8px; background:rgba(255,85,0,0.15); color:#FF5500; display:flex; align-items:center; justify-content:center; font-weight:700;">1</div>
            <div>
              <strong style="display:block; font-size:0.95rem; color:#fff;">Carro Móvil & Resortes 3D Reactivos</strong>
              <span style="font-size:0.82rem; color:#A1A1AA;">Arrastra con el ratón para rotar el aparato en 360° e interactúa con el carro deslizante.</span>
            </div>
          </div>
          <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:14px 18px; display:flex; gap:14px;">
            <div style="width:32px; height:32px; border-radius:8px; background:rgba(255,85,0,0.15); color:#FF5500; display:flex; align-items:center; justify-content:center; font-weight:700;">2</div>
            <div>
              <strong style="display:block; font-size:0.95rem; color:#fff;">Reserva de Puesto Específico</strong>
              <span style="font-size:0.82rem; color:#A1A1AA;">Permite a tus clientes elegir máquina exacta (ventana, espejo, central) antes de llegar a la sesión.</span>
            </div>
          </div>
        </div>

        <button class="btn-nav-start" style="padding:10px 24px; font-size:0.9rem;" onclick="triggerCarriageGlide()">
          Glide Carriage Test (Deslizar Carro 3D)
        </button>
      </div>

      <!-- 3D WebGL Canvas Box -->
      <div style="position:relative; background:radial-gradient(circle at 50% 50%, #16161B 0%, #0A0A0D 100%); border:1px solid rgba(255,255,255,0.14); border-radius:24px; height:520px; overflow:hidden; box-shadow:0 30px 80px -20px rgba(0,0,0,0.95);">
        <div style="position:absolute; top:18px; left:18px; background:rgba(15,15,18,0.85); backdrop-filter:blur(12px); border:1px solid rgba(255,255,255,0.1); padding:6px 14px; border-radius:8px; font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#A1A1AA; display:flex; align-items:center; gap:8px; pointer-events:none; z-index:10;">
          <span style="width:7px; height:7px; border-radius:50%; background:#10B981; box-shadow:0 0 8px #10B981;"></span>
          <span>THREE.JS DIGITAL TWIN · 360° INTERACTIVE APPARATUS</span>
        </div>

        <canvas id="reformerCanvas" style="width:100%; height:100%; display:block; cursor:grab;"></canvas>

        <div style="position:absolute; bottom:18px; right:18px; display:flex; gap:8px; z-index:10;">
          <button style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:#fff; font-family:'JetBrains Mono',monospace; font-size:0.72rem; padding:6px 12px; border-radius:6px; cursor:pointer;" onclick="resetReformerCamera()">Centrar</button>
          <button style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:#fff; font-family:'JetBrains Mono',monospace; font-size:0.72rem; padding:6px 12px; border-radius:6px; cursor:pointer;" onclick="toggleReformerSprings()">Cambiar Tensión</button>
        </div>
      </div>

    </div>
  </section>
'''

# Check if reformer section is in current_html
if 'id="reformer-3d"' not in current_html:
    # insert before canvas-section
    pos = current_html.find('<section class="canvas-section"')
    if pos != -1:
        current_html = current_html[:pos] + reformer_section + current_html[pos:]

# Add reformer 3D script code
reformer_script = '''
    /* ====================================================================
       INTERACTIVE 3D PILATES REFORMER MACHINE (THREE.JS REAL TIME)
       ==================================================================== */
    let refScene, refCamera, refRenderer, reformerGroup, carriageMesh;
    let springs = [];
    let isDragging3D = false;
    let prevMouseX = 0, prevMouseY = 0;
    let carriageTargetZ = -2;

    function init3DReformer() {
      const canvas = document.getElementById('reformerCanvas');
      if (!canvas) return;

      const width = canvas.parentElement.clientWidth;
      const height = canvas.parentElement.clientHeight;

      refScene = new THREE.Scene();
      refCamera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
      refCamera.position.set(22, 14, 26);
      refCamera.lookAt(0, 0, 0);

      refRenderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
      refRenderer.setSize(width, height);
      refRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      // Studio Lighting
      const ambientLight = new THREE.AmbientLight(0xFFFFFF, 0.7);
      refScene.add(ambientLight);

      const mainLight = new THREE.DirectionalLight(0xFFF0DD, 1.8);
      mainLight.position.set(15, 25, 20);
      refScene.add(mainLight);

      const rimLight = new THREE.DirectionalLight(0xFF5500, 1.2);
      rimLight.position.set(-20, 10, -15);
      refScene.add(rimLight);

      reformerGroup = new THREE.Group();

      const woodMat = new THREE.MeshStandardMaterial({ color: 0xD8C4B0, roughness: 0.4, metalness: 0.1 });
      const metalMat = new THREE.MeshStandardMaterial({ color: 0xE0E0E0, roughness: 0.2, metalness: 0.85 });
      const cushionMat = new THREE.MeshStandardMaterial({ color: 0x18181B, roughness: 0.6, metalness: 0.1 });
      const springMat = new THREE.MeshStandardMaterial({ color: 0xFF5500, roughness: 0.3, metalness: 0.8 });

      // Rails
      const railGeo = new THREE.BoxGeometry(1.2, 0.8, 28);
      const leftRail = new THREE.Mesh(railGeo, woodMat);
      leftRail.position.set(-4.5, 0, 0);
      reformerGroup.add(leftRail);

      const rightRail = new THREE.Mesh(railGeo, woodMat);
      rightRail.position.set(4.5, 0, 0);
      reformerGroup.add(rightRail);

      // Frame Ends
      const endGeo = new THREE.BoxGeometry(10.2, 0.8, 1.2);
      const headEnd = new THREE.Mesh(endGeo, woodMat);
      headEnd.position.set(0, 0, -14);
      reformerGroup.add(headEnd);

      const footEnd = new THREE.Mesh(endGeo, woodMat);
      footEnd.position.set(0, 0, 14);
      reformerGroup.add(footEnd);

      // Legs
      const legGeo = new THREE.CylinderGeometry(0.5, 0.5, 3.5, 16);
      [[-4.5, -2, -13], [4.5, -2, -13], [-4.5, -2, 13], [4.5, -2, 13]].forEach(pos => {
        const leg = new THREE.Mesh(legGeo, metalMat);
        leg.position.set(...pos);
        reformerGroup.add(leg);
      });

      // Carriage
      carriageMesh = new THREE.Group();
      const carriageBase = new THREE.Mesh(new THREE.BoxGeometry(8.2, 0.5, 12), metalMat);
      carriageMesh.add(carriageBase);

      const cushion = new THREE.Mesh(new THREE.BoxGeometry(8, 0.8, 11.6), cushionMat);
      cushion.position.y = 0.6;
      carriageMesh.add(cushion);

      // Shoulder rests
      const shoulderGeo = new THREE.BoxGeometry(1.8, 1.6, 1.2);
      const shLeft = new THREE.Mesh(shoulderGeo, cushionMat);
      shLeft.position.set(-2.5, 1.5, -4.8);
      carriageMesh.add(shLeft);

      const shRight = new THREE.Mesh(shoulderGeo, cushionMat);
      shRight.position.set(2.5, 1.5, -4.8);
      carriageMesh.add(shRight);

      // Headrest
      const headrest = new THREE.Mesh(new THREE.BoxGeometry(3, 0.6, 2.5), cushionMat);
      headrest.position.set(0, 1.2, -4.8);
      carriageMesh.add(headrest);

      carriageMesh.position.set(0, 0.7, -2);
      reformerGroup.add(carriageMesh);

      // Footbar
      const footbar = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 9.6, 16), metalMat);
      footbar.rotation.z = Math.PI / 2;
      footbar.position.set(0, 4.2, 13.5);
      reformerGroup.add(footbar);

      const armL = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 4.5, 16), metalMat);
      armL.position.set(-4.5, 2.1, 13.5);
      reformerGroup.add(armL);

      const armR = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 4.5, 16), metalMat);
      armR.position.set(4.5, 2.1, 13.5);
      reformerGroup.add(armR);

      // Springs
      for (let s = -2; s <= 2; s++) {
        const spring = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 4, 12), springMat);
        spring.rotation.x = Math.PI / 2;
        spring.position.set(s * 1.2, 0.7, 5.5);
        springs.push(spring);
        reformerGroup.add(spring);
      }

      refScene.add(reformerGroup);

      // Mouse drag rotation
      canvas.addEventListener('mousedown', (e) => {
        isDragging3D = true;
        prevMouseX = e.clientX;
        prevMouseY = e.clientY;
      });
      window.addEventListener('mouseup', () => isDragging3D = false);
      window.addEventListener('mousemove', (e) => {
        if (!isDragging3D || !reformerGroup) return;
        const dx = e.clientX - prevMouseX;
        const dy = e.clientY - prevMouseY;
        reformerGroup.rotation.y += dx * 0.008;
        reformerGroup.rotation.x += dy * 0.005;
        prevMouseX = e.clientX;
        prevMouseY = e.clientY;
      });

      animateReformerScene();
    }

    function animateReformerScene() {
      requestAnimationFrame(animateReformerScene);
      if (!isDragging3D && reformerGroup) {
        reformerGroup.rotation.y += 0.003;
      }
      if (carriageMesh) {
        carriageMesh.position.z += (carriageTargetZ - carriageMesh.position.z) * 0.08;
      }
      refRenderer.render(refScene, refCamera);
    }

    function triggerCarriageGlide() {
      carriageTargetZ = carriageTargetZ === -2 ? 4 : -2;
    }

    function resetReformerCamera() {
      if (reformerGroup) {
        reformerGroup.rotation.set(0, 0, 0);
        carriageTargetZ = -2;
      }
    }

    function toggleReformerSprings() {
      springs.forEach(s => {
        s.material.color.setHex(s.material.color.getHex() === 0xFF5500 ? 0x38BDF8 : 0xFF5500);
      });
    }
'''

if 'init3DReformer()' not in current_html:
    # append script before closing script
    script_pos = current_html.rfind('window.addEventListener(\'DOMContentLoaded\'')
    if script_pos != -1:
        current_html = current_html[:script_pos] + reformer_script + '\n\n' + current_html[script_pos:]
        current_html = current_html.replace('initDraggableNodes();', 'initDraggableNodes();\n      init3DReformer();')

with open('/home/user/openbreak/landing_melius_style.html', 'w', encoding='utf-8') as f:
    f.write(current_html)

print("Updated landing page with 3D Reformer Digital Twin!")
