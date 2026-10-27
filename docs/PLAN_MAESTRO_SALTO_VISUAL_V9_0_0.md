# Open Break — Hoja de Ruta y Arquitectura Técnica V9.0.0 (Salto Visual y Cinematográfico)
**Fecha de Actualización:** 26 de octubre de 2026  
**Referencia:** `OPEN_BREAK_AUD-014_V8_1_4_DICTAMEN_Y_PLAN_V8_1_5.md` (Condicionante de aprobación en AUD-015 para el inicio de V9.0.0)  
**Estado:** Documento de Especificación, Storyboarding y Planificación Técnica

---

## 1. Misión de V9.0.0
La versión **V8.1.5** corrigió, blindó y certificó con éxito la integridad matemática multi-alumna (`P0-01`, `P0-02`, `P0-03`), la eliminación de créditos fantasma en lecturas puras, la conservación estricta per-wallet $\sum \text{tx}_{\text{alumna}} = \text{billetera}_{\text{alumna}}$, y la formalización de la política de lista de espera FIFO (`P1-04`) junto con la sincronización de estilos en el canvas de flujo (`P1-05`).

Tras el cierre y aprobación de **AUD-015**, **V9.0.0** asumirá como único y exclusivo objetivo materializar el **Salto Visual y Cinematográfico Integral**, desglosado en los 6 ejes técnicos dictados por el auditor independiente en AUD-014:

1. **Storyboard por escenas de entrada / scroll / salida:** basado en las cinco referencias de diseño (Melius scroll, tipografía cinética escalonada, grafo espacial 2.5D, tarjetas de materialidad volumétrica, calendario boutique y smartphone interactivo).
2. **Motion Director unificado:** adopción de timeline unificado con GSAP + ScrollTrigger (o motor elástico nativo de precisión temporal) para eliminar bucles desacoplados y permitir scrubbing, pinning y reversibilidad matemáticamente fluida.
3. **Canvas espacial 2.5D/3D accesible:** perspectiva isométrica real, parallax multicapa de tarjetas satelitales, rutas Bézier dinámicas y layout adaptativo nativo para 390px mobile sin ocultar elementos esenciales.
4. **Modelado 3D Reformer profesional:** exportación Blender → GLB con geometría detallada de Reformer, materiales PBR con texturas de rugosidad y metalicidad, cinemáticas integradas para carro/poleas/resortes, e integración con el `GLTFLoader` oficial de Three.js (preservando el fallback de fotografía de alta resolución).
5. **Calendario y Smartphone de ultra fidelidad:** demostraciones audiovisuales interactivas de reserva en 1 toque, liberación de plaza y check-in físico en iPad.
6. **Protocolo de Evaluación Visual y GPU:** capturas y videograbaciones certificadas en resoluciones estándar (320px, 390px, 768px, 1440px) y evaluación WebGL en hardware compatible.

---

## 2. Especificación Técnica de los Componentes V9.0.0

### A. Reformer 3D Studio de Nueva Generación
- **Geometría y Materiales:**
  - Carro móvil sobre rieles de aluminio anodizado con texturas de rugosidad (roughness) y metalicidad (metalness) PBR.
  - Resortes helicoidales con deformación procedural o morph targets calibrados.
  - Barra de pies ajustable con mecanismo de trinquete modelado al milímetro.
  - Caja de saltos (Jumpboard) y correas de cuero cosido.
- **Optimización y Carga:**
  - Exportación en formato `.glb` optimizado mediante compresión Draco / Meshopt.
  - Peso objetivo: < 1.2 MB total (incluyendo texturas comprimidas WebP/KTX2).
  - Carga mediante `THREE.GLTFLoader` estándar oficial.
  - Fallback procedimental refinado con sombreado Phong y reflexión ambiental por gradiente para navegadores sin soporte WebGL 2.0.

### B. Coreografía Cinemática Multicapa (Melius-Style Scrollytelling)
- **Perspectiva 3D y Profundidad:**
  - Contenedor con `perspective: 1200px` y `transform-style: preserve-3d`.
  - Tarjetas flotantes satelitales con desplazamiento en eje Z (`translateZ(40px)` a `translateZ(120px)`) y desaceleración diferenciada por capa.
  - Transición fluida entre las 3 escenas principales:
    1. *Escena 1 (Apertura):* Visor 3D cinemático del Reformer y tipografía cinética flotante.
    2. *Escena 2 (Gestión en Vivo):* Tarjeta central de la clase con satélites de ocupación en tiempo real y flujo de caja.
    3. *Escena 3 (Experiencia Alumna):* Smartphone interactivo con pase QR holográfico dinámico y agenda semanal.

### C. Sistema de Smartphone y Agenda Táctil de Alta Fidelidad
- **Smartphone App Shell:**
  - Efecto de refracción de vidrio (*glassmorphism*) con desenfoque de fondo (`backdrop-filter: blur(20px)`).
  - Pestañas con transiciones por resortes y gestos táctiles de deslizamiento (*swipe*).
  - Selector de día con feedback de escala `scale(0.96) -> scale(1.0)` con curva elástica `cubic-bezier(0.34, 1.56, 0.64, 1)`.

### D. Gobernanza de Métricas y Evidencia GPU
- **Matriz de Telemetría Real:**
  - Contador de FPS nativo basado en muestreo rolling de 120 cuadros con `performance.now()`.
  - Clasificación de benchmarks:
    - *Tier 1:* Sintácticos y Unitarios (0 ms de red, ejecución local).
    - *Tier 2:* Integración y Ledger Matemático (invarianza de estado).
    - *Tier 3:* Renderizado y GPU (declarados únicamente con ejecución Playwright / Headless Chromium validada).

---

## 3. Plan de Fases de Ejecución V9.0.0

| Fase | Entregable Clave | Criterio de Éxito |
|---|---|---|
| **Fase 1: Assets 3D** | `reformer_pro_v9.glb` (PBR, resortes, carro animado) | < 1.5 MB, carga limpia con `GLTFLoader` oficial, 0 errores WebGL |
| **Fase 2: Motor de Escenas** | `scrollytelling-v9.js` (Canvas multicapa + Perspective 3D) | Scroll suave sin interferencias con el flujo de lectura accesible |
| **Fase 3: UI Smartphone** | Componente móvil con transiciones elásticas y tabs táctiles | 100% interactivo, sincronizado con DemoStore v8.1.4 |
| **Fase 4: QA y Auditoría AUD-014 / AUD-015** | Suite de pruebas de regresión visual y telemetría en vivo | Cero falsas certificaciones; reporte de FPS medidos en tiempo de ejecución |

---
*Open Break Engineering — Arquitectura y Planificación V9.0.0*
