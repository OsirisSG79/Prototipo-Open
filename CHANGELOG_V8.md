# OPEN BREAK — REGISTRO DE CAMBIOS V8 (Plan Correctivo Auditoría Estricta)

**Fecha:** 21 de octubre de 2026  
**Rama:** `feat/v8-corrective-sprint`  
**Base:** Consolidado V7 (`3651bb7`)  
**Auditoría de Referencia:** `OPEN_BREAK_V7_AUDITORIA_ESTRICTA_Y_PLAN_V8.md`

---

## 1. Correcciones P0 Resueltas con Evidencia Ejecutable

### V7-01: Inconsistencia y desincronización de créditos (P0)
- **Causa raíz:** `schedule-sync.js` utilizaba una variable léxica `let userCredits` que quedaba desfasada frente a las operaciones del ledger en `templates/part4_js_logic.html`.
- **Solución implementada:**
  - Creación del store transaccional canónico `src/js/demo-store.js` (`window.OpenBreakStore`), fuente única de verdad para saldo de créditos, reservas y colas FIFO de lista de espera.
  - Reemplazo del cómputo local en `part4_js_logic.html` para delegar directamente a `store.ledgerBookSpot()` y `store.ledgerRefundSpot()`.
  - Emisión y suscripción del evento desacoplado `openbreak:state-changed` para reactividad en tiempo real entre smartphone y escritorio.
- **Evidencia y verificación:** `tests/test_store_concurrency.js` reproduce exactamente la secuencia de auditoría (Ledger reserva → Agenda reserva c5 → Ledger reembolso → Agenda reserva c6 = 6 créditos netos garantizados). **PASS**.

### V7-02: Conexión de estilos isométricos 2.5D huérfanos (P0 visual)
- **Causa raíz:** Las clases `.workflow-section-v7`, `.workflow-canvas-isometric` y `.workflow-node-v7` definidas en `workflow-3d.css` no estaban aplicadas al DOM de `workflow_section.html`.
- **Solución implementada:**
  - Actualización de `src/modules/workflow_section.html` aplicando las clases isométrica 2.5D, tipografías y contenedores estructurados sobre los botones de nodos.
  - Se mantuvieron intactos los cables Bézier SVG dinámicos y la accesibilidad táctil/teclado.
- **Evidencia:** `python tests/qa_static.py` y `python tests/qa_suite_v7.py` confirman la presencia de los selectores activos y la eliminación de reglas huérfanas.

### V7-03: Discontinuidad y salto en el reciclaje del túnel espacial (P0 visual)
- **Causa raíz:** En `hero-tunnel.js`, la opacidad solo amortiguaba en la entrada ($t \to 0$), pero al cruzar la salida cercana ($t \to 1$ con $x=662$px, $z=+100$px, escala=1.20) el panel saltaba abruptamente al fondo lejano.
- **Solución implementada:**
  - Rediseño de la envolvente de visibilidad (*bilateral boundary smoothing*):
    - `entryFade = clamp(t / 0.15)` para entrada suave en el horizonte.
    - `exitFade = clamp((1 - t) / 0.15)` para salida suave antes de sobrepasar el plano cercano.
    - Envolvente combinada `envelope = entryFade * exitFade` que desvanece a 0 tanto en el horizonte como en el plano cercano, eliminando completamente los *pops* visuales.
- **Evidencia:** Trayectoria matemática cerrada y continua sin saltos de escala ni opacidad en `src/js/hero-tunnel.js`.

---

## 2. Batería de Pruebas de Calidad Ejecutada y Aprobada

```bash
# 1. Compilación estática limpia (sin dependencias de red)
python3 build_site.py
# Build complete | HTML: 136724 bytes | assets: 11 optimized images

# 2. Verificación estricta de invariantes V7/V8
python3 tests/qa_suite_v7.py
# ALL OPEN BREAK V7 QA CHECKS PASSED (5/5)!

# 3. Verificación de IDs únicos y cero Base64
python3 tests/qa_static.py
# PASS static: builder, IDs, hero, agenda, local image files, no Base64

# 4. Pruebas unitarias de reserva de agenda
node tests/test_schedule.js
# PASS: booking, idempotence, waitlist, credit balance and rebooking

# 5. Prueba transaccional de concurrencia y erradicación del defecto V7-01
node tests/test_store_concurrency.js
# PASS: DemoStore completely eliminates V7-01 credit inconsistency! All invariants verified.
```
