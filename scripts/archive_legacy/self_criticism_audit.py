import re
from pathlib import Path

report = []
report.append("=== AUTOEVALUACIÓN ESTRICTA Y HONESTA DE BRECHAS UX (OpenBreak V8.1.0) ===")

landing = Path('/home/user/openbreak/landing_melius_style.html').read_text()
build_py = Path('/home/user/openbreak/build_site.py').read_text()
part3 = Path('/home/user/openbreak/templates/part3_body_sections.html').read_text()
reformer_js = Path('/home/user/openbreak/src/js/reformer-3d.js').read_text()

# 1. UX-03: ¿Es un Reformer .glb fotorrealista o Three.js procedimental básico?
if "GLTFLoader" in reformer_js or ".glb" in reformer_js:
    report.append("[UX-03] Reformer 3D: TIENE GLB real.")
else:
    report.append("[UX-03 FALTA CRÍTICA] Reformer 3D es una aproximación procedural sintética (cajas Three.js BoxGeometry). NO es un modelo .glb fotorrealista con materiales PBR horneados de Blender.")

# 2. UX-06: Workflow Canvas nodo a nodo interactivo
if "workflow-node" in landing:
    report.append("[UX-06] Workflow Canvas: Maqueta interactiva presente, pero ¿es el canvas nodo a nodo dinámico completo de Melius donde creas y conectas nodos arbitrarios? No, es una sección estática con nodos fijos.")
else:
    report.append("[UX-06 FALTA CRÍTICA] No se encuentra workflow canvas completo.")

# 3. Melius Scroll Parallax / Sticky Scrubbers (UX-05)
# En Melius, el scroll controla el tiempo (scrubber) con pinned sections (GSAP ScrollTrigger style).
if "ScrollTrigger" in landing or "position: sticky" in landing:
    report.append("[UX-05] Scroll: Hay IntersectionObserver básico de entrada/salida (fade-in), pero NO un sticky container scrubber cinemático multi-pantalla real como Melius (donde el usuario scrollea y la escena 3D / tarjetas rotan según el scrollOffset exacto).")

# 4. Nombre del ZIP y versionado:
report.append("[ZIP & VERSION] El ZIP se sigue llamando 'OpenBreak_Cinematic_V7_Proyecto_Completo.zip' a pesar de que el sistema ya avanzó a V8.1.0. Esto debe corregirse a 'OpenBreak_Cinematic_V8_1_0_Proyecto_Completo.zip'.")

print("\n".join(report))
