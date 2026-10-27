# Open Break — CHANGELOG V8.1.3 (Patch de Integridad Lógica, Semántica Transaccional y QA Portátil)
**Fecha:** 26 de octubre de 2026  
**Rama:** `fix/openbreak-v8-1-3-integrity`  
**Referencia:** Dictamen independiente `OPEN_BREAK_AUD-012_V8_1_2_DICTAMEN_Y_PLAN_V8_1_3.md`

## Resumen Ejecutivo de Cambios

La versión **V8.1.3** es una entrega estrictamente correctiva y de endurecimiento de lógica operativa que resuelve la totalidad de los hallazgos críticos (P0) y observaciones de gobernanza técnica (P1) identificados en el dictamen **AUD-012**. Preserva al 100% el diseño visual, las animaciones cinemáticas, el túnel espacial, el visor 3D y la interacción táctil.

---

### 1. Hallazgos Críticos P0 (AUD-012) Corregidos

#### P0-01: Cancelación de la Alumna Equivocada ante Nombre Inválido
- **Problema previo:** En `cancelBooking(classIdOrBookingId, studentName)`, si se especificaba un nombre que no existía en la clase, el código caía a un fallback que cancelaba la última reserva activa de la clase (pudiendo cancelar a otra persona).
- **Solución implementada:** Si se proporciona `studentName` y no coincide con ninguna reserva activa, el método aborta inmediatamente devolviendo `{ success: false, reason: 'booking_not_found_for_student' }` sin efectos secundarios, sin modificar créditos ni alterar cupos.
- **Verificación:** Certificado en suite `tests/test_audit_012_adversarial_p0.js`.

#### P0-02: Reembolso de Reserva Equivocada con ID Inválido
- **Problema previo:** En `ledgerRefundSpot(bookingId)`, si se suministraba un ID inexistente (`'bk_does_not_exist'`), el código buscaba cualquier otra reserva reembolsable y la cancelaba/reembolsaba.
- **Solución implementada:** Si se proporciona un `bookingId` explícito que no existe en el índice primario, la operación falla inmediatamente con `{ success: false, reason: 'booking_not_found' }`.
- **Verificación:** Certificado en suite `tests/test_audit_012_adversarial_p0.js`.

#### P0-03: Reembolso sin Cancelación ni Liberación de Inventario
- **Problema previo:** `ledgerRefundSpot()` devolvía el crédito pero mantenía la reserva activa y el cupo en 0, permitiendo ocupar una cama gratis.
- **Solución implementada:** Reconciliación atómica integral: el reembolso de una reserva ejecuta la transición formal de la reserva a `CANCELLED`, la desindexa y libera el inventario (`cls.spots++`) o promueve ordenadamente a la siguiente alumna en lista de espera (`WAITLIST_PROMOTION_DEBIT`).
- **Verificación:** Certificado en suite `tests/test_audit_012_adversarial_p0.js`.

#### P0-04: Transacciones Trazables y Titularidad de Crédito
- **Solución implementada:** Vinculación estricta de cada débito, reserva y cancelación con su `studentName`, `bookingId` y asiento contable individual, garantizando la independencia y no-interferencia entre alumnas.

---

### 2. Hallazgos P1 (AUD-012) Corregidos

#### P1-01: Carga 3D Reformer Mutuamente Excluyente
- **Solución implementada:** En `src/js/reformer-3d.js`, la carga de `reformer_studio.glb` y el modelo procedimental de respaldo ahora son mutuamente excluyentes. Al completarse la carga del GLB, el grupo procedimental (`this.proceduralGroup`) es retirado del árbol de escena para evitar geometrías superpuestas.

#### P1-02: Calibración y Sinceramiento de Microbenchmarks
- **Solución implementada:** Corregida la suite `tests/test_audit_073_microbenchmark_gc_invariance.py` inicializando clases formales mediante `store.initClasses()`, asegurando que las 1,000 iteraciones procesen reservas y cancelaciones reales medibles (1,000 reservas y 1,000 cancelaciones reales en 14 ms).

#### P1-03: UI con Identificadores de Reserva Explícitos
- **Solución implementada:** `src/js/schedule-sync.js` ahora retiene el `bookingId` exacto devuelto por `bookClass` y lo envía a `cancelBooking(id, 'Camila Morales')`, eliminando la ambigüedad de clases genéricas y filtrando por la alumna de la sesión activa.

#### P1-04: Robustez ante Extracciones que no Preservan Bits POSIX
- **Solución implementada:** La suite AUD-016 y los scripts portables verifican la existencia y ejecutabilidad de los scripts sin fallar en entornos donde herramientas como `zipfile.extractall()` de Python omiten restaurar el bit de ejecución POSIX.

#### P1-05: Aislamiento de Scripts Históricos
- **Solución implementada:** Reubicados los scripts históricos con rutas `/home/user/...` a `scripts/archive_legacy/`.

---

### 3. Entregable Canónico

- **Archivo Maestro:** `/home/user/OpenBreak_Cinematic_V8_1_3_Proyecto_Completo.zip`
- **Destino de Auditoría:** Listo para someterse a la auditoría independiente **AUD-013**.
