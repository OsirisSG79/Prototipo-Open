# Registro de Versiones Oficial — OpenBreak V8.1.0

**Fecha de Liberación:** 26 de Octubre de 2026  
**Rama:** `feat/v8-corrective-sprint`  
**Referencia de Auditoría Externa:** `OpenBreak_Auditoria_Maestra_y_Plan_de_Ejecucion.md` y `OpenBreak_AUD-009_V8_0_0_Informe_y_Versionado.md`  
**Entregable Maestro:** `OpenBreak_Cinematic_V8_1_0_Proyecto_Completo.zip` (5.7 MB)

---

## 1. Resumen de Novedades y Mejoras Implementadas

### A. Scrubber Cinemático de Scroll Estilo Melius (UX-05 / F7)
- Transformación de la sección `#solucion` en una pasarela con altura vertical de 240vh (`.melius-sticky-stage`).
- El avance de scroll calcula de forma pasiva y continua la rotación de las tarjetas espaciales 3D, el avance de la barra indicadora (`#scrubberProgressBar`) y la activación de los cables conductores.
- Compatible con accesibilidad: degradación estática total bajo la regla `@media (prefers-reduced-motion: reduce)`.

### B. Lienzo de Red Reactiva con Cables Bézier SVG Cúbicos (UX-06 / F6)
- Integración de `#deckWiresCanvas` que une matemáticamente los satélites periféricos interactivos con el centro tridimensional de la baraja.
- Al alternar pilares o avanzar el scroll, el conductor correspondiente activa un trazo esmeralda con resplandor (`filter: drop-shadow`).
- Ocultación limpia en anchos menores a 900px para garantizar la legibilidad en pantallas móviles verticales.

### C. Asset glTF 2.0 Binario y Micro-Texturas PBR para Reformer (UX-03 / F3)
- Generación del recurso binario estándar `assets/reformer_studio.glb` (2.9 KB) con jerarquía de nodos `ReformerRoot`, `ReformerFrame` y `ReformerCarriage` y materiales PBR.
- Inyección de sintetizadores en Canvas 2D (`createProceduralWoodTexture` y `createProceduralBrushedTexture`) que proyectan vetas orgánicas de madera nogal y grano de aluminio cepillado sobre las mallas de Three.js.

### D. Trazabilidad Transaccional del Ledger e Invariantes Financieros (UX-17 / AUD-009 P0)
- El panel `#ledgerHistory` renderiza dinámicamente cada movimiento emitido por `DemoStore` con su ID de transacción único (`txId`), referencia de reserva (`refBookingId`) y cálculo de saldo en créditos.
- Cero doble reembolso: las reservas canceladas vía agenda no pueden volver a acreditar saldo si ya fueron devueltas vía ledger, y viceversa.
- Asignación atómica de cupos de lista de espera: cancelar una reserva transfiere directamente la plaza a la alumna en cabeza de cola FIFO (`spots = 0`).

### E. Captura Segura con Consentimiento Explícito (UX-19)
- Formulario de demostración con casilla de consentimiento obligatoria para WhatsApp (`#demoConsent`) y generación de `leadId` para trazabilidad de contacto.

### F. Matriz Responsive Exhaustiva (UX-12 / F8)
- Pruebas automatizadas en `tests/test_responsive_viewports_audit.py` validando safe-zones y 5 declaraciones fluidas `clamp()` en 320px, 360px, 480px, 768px, 900px, 1024px, 1440px y 1920px.

---

## 2. Batería de Pruebas Automatizadas (11/11 PASS)

El orquestador `./run_all_audits.sh` ejecuta la totalidad de las 11 suites de prueba de forma determinista y sin dependencias externas:
1. `build_site.py` — Compilación canónica HTML (155 KB).
2. `test_audit_009_adversarial.js` — Pruebas adversariales contra doble reembolso y waitlist.
3. `test_responsive_viewports_audit.py` — Matriz de 8 breakpoints y tipografía fluida.
4. `test_lead_dispatch.js` — Formato y despacho seguro de leads.
5. `test_store_concurrency.js` — Invariante de saldo y concurrencia.
6. `test_waitlist_fifo.js` — Cola FIFO y auto-promoción.
7. `test_telemetry.js` — Telemetría local y monitor de FPS en memoria.
8. `test_schedule.js` — Agenda semanal interactiva.
9. `qa_static.py` — Verificación estática y cero Base64.
10. `qa_visual_audit.py` — Contratos GPU, WebGL y fallback seguro.
11. `qa_suite_v7.py` — QA global de invariantes de diseño.
