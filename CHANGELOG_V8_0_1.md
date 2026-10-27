# OPEN BREAK — REGISTRO DE CAMBIOS V8.0.1 (AUD-009 RESOLUCIÓN COMPLETA)

**Versión:** `V8.0.1`  
**Fecha:** 26 de octubre de 2026  
**Referencia de Auditoría:** `OpenBreak_AUD-009_V8_0_0_Informe_y_Versionado.md`  
**Rama:** `feat/v8-corrective-sprint`  

---

## 1. Cierre Exhaustivo de Hallazgos P0 de Auditoría AUD-009

### A. P0 — Integridad de Créditos y Erradicación del Doble Reembolso
- **Defecto Auditado:** `refundableReservationsCount` era un agregado global sin identidad transaccional; reembolsar una reserva vía ledger y luego cancelarla vía app inflaba el saldo (8 → 7 → 8 → 9 créditos).
- **Solución Implementada (`src/js/demo-store.js`):**
  - Cada reserva y débito cuenta con identificador transaccional único (`txId`) y `bookingId`.
  - Las reservas activas mapean su estado de reembolsabilidad (`refundable: boolean`).
  - Cuando el ledger reembolsa una reserva, marca su `refundable = false`.
  - La función `cancelBooking(classId)` verifica estrictamente `booking.refundable`. Si ya fue reembolsada por el ledger, la reserva se cancela **sin generar abono duplicado de crédito**.
  - Si una reserva ya fue cancelada y devuelta vía app, el ledger rechaza cualquier intento de re-reembolso.
- **Evidencia Automatizada:** `tests/test_audit_009_adversarial.js` prueba ambos escenarios cruzados (Ledger refund $\to$ App cancel, y App cancel $\to$ Ledger refund). Saldo máximo acotado e invariante: **PASS**.

### B. P0 — Consistencia Semántica de Lista de Espera en Cancelación
- **Defecto Auditado:** Al cancelar una plaza con lista de espera activa, se ejecutaba `queue.shift()`, pero el cupo quedaba en `spots = 1` permitiendo que un tercero externo reservara la plaza en simultáneo.
- **Solución Implementada (`src/js/demo-store.js`):**
  - Máquina de estados con asignación directa de plaza a la alumna promovida de la cola FIFO.
  - Al cancelar una clase con lista de espera, el cupo permanece en `spots = 0` (ocupado por la alumna promovida), impidiendo que terceros tomen la plaza de la lista de espera.
- **Evidencia Automatizada:** `tests/test_audit_009_adversarial.js` (Prueba 5). `c_full.spots` permanece en 0 y la alumna en cabeza de fila recibe la asignación: **PASS**.

---

## 2. Batería de Pruebas Automatizadas Ejecutadas (9 Suites / 100% PASS)

1. `build_site.py` — Compilación reproducible (142 KB, 11 WebP locales, 0 Base64).
2. `tests/test_audit_009_adversarial.js` — Verificación contra ataques y pruebas cruzadas de doble reembolso y listas de espera.
3. `tests/test_store_concurrency.js` — Idempotencia y transacciones concurrentes en el store.
4. `tests/test_waitlist_fifo.js` — Determinismo en cola FIFO de espera.
5. `tests/test_lead_dispatch.js` — Formato estructurado de lead y despacho seguro a WhatsApp.
6. `tests/test_telemetry.js` — Monitoreo de FPS, CLS y rendimiento local sin trackers de terceros.
7. `tests/test_schedule.js` — Integridad de reservas, cancelaciones y créditos.
8. `tests/qa_static.py` — Estructura HTML, 110 IDs únicos y WebP.
9. `tests/qa_suite_v7.py` — Invariantes globales y compatibilidad con `prefers-reduced-motion`.
