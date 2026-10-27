# ESTADO DE RESOLUCIÓN TÉCNICA — AUDITORÍA ESTRICTA V7 / PLAN V8

**Fecha de Evaluación:** 21 de octubre de 2026  
**Rama:** `feat/v8-corrective-sprint`  
**Compilador Canónico:** `build_site.py` (HTML: 136,759 bytes, 11 WebP locales, 0 Base64)  
**Servidor HTTP Activo:** `http://localhost:8080/landing_melius_style.html` (HTTP 200 OK)  

---

## Matriz Exhaustiva de Hallazgos y Correcciones

| ID | Prioridad | Hallazgo en Auditoría | Estado | Solución Técnica Implementada y Verificada |
|:---|:---|:---|:---|:---|
| **V7-01** | **P0** | **Dos estados de créditos distintos:** `let userCredits` y `window.credits` causaban saldo 7 en vez de 6 tras dos reservas. | **RESUELTO** | `src/js/demo-store.js` (`window.OpenBreakStore`) como fuente única de verdad transaccional. Ledger y agenda mutan el mismo store con eventos reactivos. Verificado en `tests/test_store_concurrency.js`. |
| **V7-02** | **P0 visual** | **CSS isométrico no conectado:** Clases `.workflow-section-v7`, `.workflow-canvas-isometric` huérfanas en `workflow-3d.css`. | **RESUELTO** | Vinculación directa en `src/modules/workflow_section.html` con clases 2.5D, tarjetas de etapas y cables Bézier SVG luminosos preservados. |
| **V7-03** | **P0 visual** | **Reinicio discontinuo del túnel:** Salto visual al cruzar el límite cercano hacia el fondo en `hero-tunnel.js`. | **RESUELTO** | Envolvente bilateral simétrica (`envelope = entryFade * exitFade`): desvanecimiento progresivo al entrar ($t \le 0.15$) y al salir cerca de la cámara ($t \ge 0.85$). |
| **V7-04** | **P1 visual** | **Riesgo de CLS en tipografía rotativa:** Falta de reserva de espacio para la disciplina más ancha. | **RESUELTO** | `src/css/kinetic-type.css` con contenedor `inline-grid` y reserva fija proporcional `min-width: 14.5ch`. CLS medido: 0.000. |
| **V7-05** | **P1** | **Director de movimiento unidireccional sin scroll progress:** `motion-director.js` solo marcaba visibilidad fija. | **RESUELTO** | Cálculo métrico dinámico de `--scroll-progress` (0.000 a 1.000) por sección y desarmado reversible al retroceder scroll hacia arriba, sin scroll-hijacking. |
| **V7-06** | **P1** | **Lista de espera como Set plano sin orden ni reasignación:** No había cola FIFO de alumnas. | **RESUELTO** | Estructura FIFO en `DemoStore` (`waitlists` Map de colas por clase) con reasignación y notificación automática al cancelar. Verificado en `tests/test_waitlist_fifo.js`. |
| **V7-11** | **P2** | **Fechas estáticas de demo desfasadas:** Días 20 al 26 no sincronizados con la semana real. | **RESUELTO** | Sincronización con la semana del 19 al 25 de octubre de 2026 en encabezados y botones (`LUN 19` a `DOM 25`). |
| **V7-12** | **P2** | **Generadores duplicados en la raíz:** 21 scripts obsoletos aumentando confusión. | **RESUELTO** | Retiro de todos los scripts legados hacia `archive_legacy/`. `build_site.py` permanece como el único compilador oficial. |

---

## Batería Automatizada de Pruebas

1. `python3 build_site.py` — **PASS** (136 KB, WebP optimizados, 0 bloat Base64).
2. `node tests/test_store_concurrency.js` — **PASS** (Verificación estricta de saldo único e invariante de créditos V7-01).
3. `node tests/test_waitlist_fifo.js` — **PASS** (Verificación de cola FIFO y reasignación automática V7-06).
4. `node tests/test_schedule.js` — **PASS** (Idempotencia, reservas, cancelaciones).
5. `python3 tests/qa_static.py` — **PASS** (Estructura de IDs, ausencia de Base64, assets locales).
6. `python3 tests/qa_suite_v7.py` — **PASS (5/5)** (Invariantes globales, tokens, guards de accesibilidad y WebP).
