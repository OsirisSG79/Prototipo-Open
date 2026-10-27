# Registro de Versiones Oficial — OpenBreak V8.1.1 (Saneamiento de Integridad & Calidad)

**Fecha de Liberación:** 26 de Octubre de 2026  
**Rama:** `fix/openbreak-v8-1-1-integrity`  
**Referencia de Auditoría:** `OPEN_BREAK_AUD-010_V8_1_0_DICTAMEN.md` y `OPEN_BREAK_V8_1_1_INSTRUCCIONES_DESARROLLO.md`  
**Entregable Maestro:** `OpenBreak_Cinematic_V8_1_1_Proyecto_Completo.zip` (5.8 MB)  
**Veredicto de Pipeline:** 13/13 Suites Automatizadas Aprobadas (100% PASS Portable)

---

## 1. Tabla de Resolución de Hallazgos AUD-010

| Código | Hallazgo Reportado | Causa Raíz Identificada | Solución Técnica Implementada en V8.1.1 | Prueba de Validación Ejecutada | Estado |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **P0-01** | CSS nuevo expuesto como texto visible encima del hero | En V8.1.0 se agregaron reglas CSS al final de `part2_css_rest.html` después de `</style></head>`, quedando texto suelto en el DOM. | Se extrajo el bloque a `src/css/melius-scroll-responsive.css` y se enlaza mediante `<link rel="stylesheet">`. Se garantizan 0 caracteres entre `</head>` y `<body>`. | `tests/test_html_syntax_and_no_leak.py` | **RESUELTO (PASS)** |
| **P0-02** | Código JS de scroll pegado después de `</html>` | En V8.1.0 se añadieron funciones JS al final de `part4_js_logic.html` después de `</html>`. | Se extrajo el bloque a `src/js/scroll-choreography.js` y se enlaza antes del cierre de `</body>`. Se garantizan 0 caracteres después de `</html>`. | `tests/test_html_syntax_and_no_leak.py` | **RESUELTO (PASS)** |
| **P0-03** | Falsa confirmación de lead ante fallos de red / HTTP 500 | Un `.catch()` transformaba errores de red en `{ok:true, simulated:true}` y `.finally()` mostraba confirmación de éxito. | Se eliminó el catch engañoso. Se gestionan estados explícitos: `server_confirmed`, `server_error`, `network_error` y `offline_demo` sin promesas falsas de contacto. | `tests/test_lead_dispatch.js` | **RESUELTO (PASS)** |
| **P0-04** | Vulnerabilidad de inyección HTML en el resumen del lead | Se interpolaban variables de entrada de usuaria mediante `innerHTML`. | Se reemplazó por construcción segura de nodos DOM (`document.createElement` y `textContent`), sanitización y límites de 80 caracteres. | `tests/test_lead_dispatch.js` | **RESUELTO (PASS)** |
| **P0-05** | Inflación del ledger de 8 a 11 y descalce contable | Había dos reservas históricas ficticias sin débito previo que permitían reembolsos indebidos. | Se impone la conservación matemática estricta: `Credits = OpeningBalance + sum(transactions)`. Solo reservas con débito previo pueden ser reembolsadas. | `tests/test_audit_010_p0_p1_integrity.py` | **RESUELTO (PASS)** |
| **P1-06** | Waitlist no creaba reserva formal para alumna promovida | Al cancelar con waitlist, se vaciaba la cola pero no se creaba registro de reserva para la alumna promovida. | La cancelación asigna una reserva formal con estado `CONFIRMED_FROM_WAITLIST`, asociando el nombre de la alumna y reteniendo `spots = 0`. | `tests/test_audit_010_p0_p1_integrity.py` | **RESUELTO (PASS)** |
| **P1-08** | QA no portable por rutas fijas `/home/user/openbreak` | Los scripts de prueba usaban rutas fijas que fallaban si el repositorio se descomprimía en otra carpeta. | Se migraron todas las rutas a relativas mediante `Path(__file__).resolve().parents[1]` y `SCRIPT_DIR`. Probado en carpeta temporal aislada. | `scripts/test_portable_execution.sh` | **RESUELTO (PASS)** |
| **P1-09** | IDs no únicos entre instancias independientes | `generateId()` dependía de un contador secuencial local por proceso. | Se migraron los IDs a UUIDs de alta entropía combinando marca de tiempo base36, microsegundos de `performance.now()` y nonce aleatorio. | `src/js/demo-store.js` | **RESUELTO (PASS)** |
| **P1-10** | Retención innecesaria de PII en localStorage | Se guardaban teléfonos y nombres sin cifrar de forma persistente. | Se eliminó la persistencia en `localStorage`; la información vive solo en la sesión activa en memoria mientras se despacha al canal de contacto. | `templates/part4_js_logic.html` | **RESUELTO (PASS)** |

---

## 2. Batería Completa de Verificación (13 Suites / 100% PASS)

Ejecutable canónico: `./run_all_audits.sh`
1. `build_site.py` — Compilación estática reproducible (152,054 bytes HTML).
2. `test_html_syntax_and_no_leak.py` — Verificación estructural de cero fugas de código CSS/JS en el DOM.
3. `test_audit_010_p0_p1_integrity.py` — Conservación matemática del ledger y ciclo de vida de la waitlist.
4. `test_audit_009_adversarial.js` — Pruebas adversariales contra doble reembolso y orden cruzado.
5. `test_responsive_viewports_audit.py` — Matriz responsive de 8 breakpoints y tipografía fluida `clamp()`.
6. `test_lead_dispatch.js` — Sanitización y despacho seguro de leads.
7. `test_store_concurrency.js` — Invariante de saldo y concurrencia.
8. `test_waitlist_fifo.js` — Cola FIFO y auto-promoción.
9. `test_telemetry.js` — Telemetría local y monitor de FPS en memoria.
10. `test_schedule.js` — Agenda semanal interactiva.
11. `qa_static.py` — Verificación estática y cero Base64.
12. `qa_visual_audit.py` — Contratos GPU, WebGL y fallback seguro.
13. `qa_suite_v7.py` — QA global de invariantes de diseño.
