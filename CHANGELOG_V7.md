# CHANGELOG V7 — OPEN BREAK CINEMATIC & REPOSITORIO GITHUB
**Fecha:** 21 de octubre de 2026  
**Repositorio Remoto Integrado:** `https://github.com/OsirisSG79/Prototipo-Open` (commit `866887f8`)  
**Estatus:** Sincronizado, compilado y verificado localmente.

### 1. Sincronización con el Repositorio de GitHub
- Se clonó e integró la última versión oficial de `OsirisSG79/Prototipo-Open` que incorpora el nuevo Hero Espacial Cinematográfico (`ob-cinematic-hero` / `src/js/hero-tunnel.js`), la suite de assets optimizados (`assets/optimized/` en formato WebP local), el módulo de agenda móvil (`src/modules/schedule_mobile_section.html`), y los scripts de prueba deterministas (`tests/qa_static.py` y `tests/test_schedule.js`).

### 2. Preservación y Reintroducción de la Animación de Letras (Sprint 01 / Contrato de Preservación)
- **Defecto resuelto:** La V6 de GitHub había reemplazado el titular rotativo interactivo por un título completamente estático.
- **Implementación:** Se creó `src/js/title-typewriter.js` y `src/css/kinetic-type.css`, integrando la rotación vertical con `transform` y `opacity` (`word-leaving` / `word-entering`) sobre `#ob-hero-rotating-word` alternando entre disciplinas boutique (*Pilates Reformer*, *Barre & Mat*, *Hot Yoga Flow*, *Indoor Cycling*).
- **Accesibilidad:** Respeto absoluto a `prefers-reduced-motion: reduce`, manteniendo el titular fijo y legible sin saltos geométricos ni CLS.

### 3. Pipeline de Construcción y Verificación
- El ensamblador `build_site.py` compila limpiamente generando `landing_melius_style.html` e `index.html` (130,100 bytes).
- Pruebas estáticas ejecutadas con 100% de éxito:
  - `python3 tests/qa_static.py` -> PASS.
  - `node tests/test_schedule.js` -> PASS (idempotencia, waitlists, balance de créditos y re-reserva).

### 4. Matriz de Estado
- **Hecho:** Integración del repositorio GitHub, animación de letras rotativas, túnel espacial cinemático con pausa y teclado, carrusel secundario con inercia, agenda semanal sincronizada con smartphone, simulador atómico y pruebas de QA estáticas.
- **Parcial:** Modelo Reformer 3D paramétrico procedimental (a la espera de asset externo GLB con PBR en Sprint 05).
- **Marcado Honestamente como Demo:** Pruebas de concurrencia atómica, QR de acceso y pasarelas de pago, distinguiendo claramente la simulación interactiva de las llamadas reales de backend.
