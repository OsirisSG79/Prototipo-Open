# OPEN BREAK — INVENTARIO DE MOVIMIENTO Y CONTROLADORES
**Fecha:** 21 de octubre de 2026

| Componente | Archivo Controlador | Selectores DOM | Triggers / Eventos | Curva de Easing & Timing | Fallback Accesible |
|:---|:---|:---|:---|:---|:---|
| **Cursor Lerp** | `src/js/cursor.js` | `#custom-cursor`, `#custom-cursor-label` | `mousemove`, `mouseenter`, `mouseleave` | `lerp(pos, target, 0.16)` por frame | Desactivado en `pointer: coarse` y `prefers-reduced-motion`. |
| **Parabolic Ribbon** | `src/js/ribbon.js` | `#conveyorViewport`, `#ribbonTrack`, `.ribbon-card` | `pointerdown`, `pointermove`, `pointerup`, `ArrowLeft/Right` | Delta-time `35px/s`, amortiguación `pow(0.88, dt*60)` | Vista plana estática con scroll horizontal nativo. |
| **Workflow Canvas** | `src/js/studio-canvas.js` | `#workflowBoard`, `.workflow-node`, `.workflow-wires-svg path` | `pointerdown` (drag), `resize`, timer (4.5s) | `cubic-bezier(0.16, 1, 0.3, 1)` | Nodos ordenados en lista lineal con cables estáticos. |
| **Reformer 3D** | `src/js/reformer-3d.js` | `#reformerCanvas`, `#webglFallbackCard` | `pointerdown`, `mousemove`, botones UI | Interpolación orbital `0.08`, glide carriage `0.08` | Tarjeta estática HD fotográfica automática si falla WebGL. |
| **Solutions Deck** | `templates/part4_js_logic.html` | `.deck-child-card`, `.deck-satellite` | `click`, `Enter`, `Space` | `translate3d(0, 140px, 100px) rotateX(25deg)` (450ms) | Tarjetas apiladas legibles con botón de rotación accesible. |
