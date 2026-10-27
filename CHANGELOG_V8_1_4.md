# Open Break — CHANGELOG V8.1.4 (Endurecimiento de Integridad, Billeteras Aisladas y Enlace GLB)
**Fecha:** 26 de octubre de 2026  
**Rama:** `fix/openbreak-v8-1-4-integrity`  
**Referencia:** Dictamen independiente `OPEN_BREAK_AUD-013_V8_1_3_DICTAMEN_Y_PLAN_V8_1_4.md`

## Resumen Ejecutivo de Cambios

La versión **V8.1.4** es una entrega correctiva formal que atiende y resuelve íntegramente todas las observaciones críticas (P0) y técnicas (P1) emitidas en el dictamen **AUD-013**. Introduce aislamiento financiero formal por alumna (`studentsById`, `walletsByStudentId`, `transactionsById`), eliminación absoluta de operaciones mutantes ambiguas por `classId` en reservas múltiples, selector explícito de reserva para reembolsos en la consola contable de recepción, validación de solvencia de saldo en promociones de lista de espera para impedir balances negativos, y enlace cinemático bidireccional entre los nodos de mallas del modelo GLB (`UpholsteredCarriage`, `SteelTracksAndFootbar`) y los controles 3D interactivos.

---

### 1. Hallazgos Críticos P0 (AUD-013) Corregidos

#### P0-01: Cancelación Ambigua por `classId` sin Identidad
- **Problema en V8.1.3:** Al recibir `cancelBooking(classId)` sin `studentName` ni `bookingId` cuando una clase tenía múltiples reservas activas, el sistema cancelaba la última reserva arbitrariamente.
- **Solución implementada en V8.1.4:** Si existen múltiples reservas activas para una clase y no se especifica `studentName` ni `bookingId`, el método rechaza la petición con `{ success: false, reason: 'ambiguous_booking' }` sin modificar cupos ni transferir saldos indebidamente.
- **Verificación:** Certificado en suites `tests/test_audit_013_adversarial_p0.js` y `tests/test_audit_013_acceptance.js`.

#### P0-02: Reembolso de Mostrador sin ID Explícito
- **Problema en V8.1.3:** `ledgerRefundSpot()` sin parámetro recorría las reservas activas y reembolsaba la primera que encontraba, sin que el operador de recepción pudiera elegir a qué alumna correspondía el reintegro.
- **Solución implementada en V8.1.4:**
  1. Si existen múltiples reservas activas y se invoca `ledgerRefundSpot()` sin `bookingId`, se rechaza con `{ success: false, reason: 'ambiguous_refund_target' }`.
  2. En la interfaz (`templates/part3_body_sections.html` y `templates/part4_js_logic.html`), se integró un selector de reserva activa (`ledgerBookingSelector`) que puebla dinámicamente los registros activos con nombre de alumna, ID de clase y token de reserva, garantizando que el personal de recepción seleccione inequívocamente la reserva objeto de reembolso.
- **Verificación:** Verificado en `tests/test_audit_013_acceptance.js` y probado en terminal interactiva.

#### P0-03: Billeteras Independientes por Alumna (`studentsById`, `walletsByStudentId`, `transactionsById`)
- **Problema en V8.1.3:** `DemoStore` mantenía un saldo agregado único. Las reservas de una alumna descontaban el saldo global, permitiendo que una alumna agotara los créditos de otra.
- **Solución implementada en V8.1.4:**
  1. Estructuras formales añadidas a `DemoStore`:
     - `studentsById`: Mapeo formal de identificación de alumnas (`id`, `name`, `createdAt`).
     - `walletsByStudentId`: Saldos contables individuales y aislados por alumna.
     - `transactionsById`: Índice universal de transacciones inmutables.
  2. Métodos de gobernanza contable: `registerStudent(id, credits)`, `getStudentBalance(id)`, `creditStudent(id, amount)`.
  3. Los débitos y reservas de una alumna (ej. Ana) no disminuyen el balance disponible de otra (ej. Beto).
- **Verificación:** Certificado en suite `tests/test_audit_013_acceptance.js` (Criterio 1 y Criterio 9).

#### P0-04: Eliminación de Recaída en IDs Ambiguos en UI Mobile
- **Problema en V8.1.3:** En `src/js/schedule-sync.js`, ante una cancelación se derivaba `currentBookingId` usando `[...currentStore.activeBookings].at(-1)`, produciendo un `classId` en lugar de un `bookingId`.
- **Solución implementada en V8.1.4:** `currentBookingId` se deriva estrictamente de `getBookingsForStudent('Camila Morales')` y se asigna el `bookingId` inequívoco. Si la alumna no tiene reservas activas, pasa a `null`.
- **Verificación:** Verificado en `src/js/schedule-sync.js` y suites de integración de interfaz.

#### P0-05: Validación de Solvencia en Promoción de Lista de Espera
- **Problema en V8.1.3:** La cancelación de una reserva promovía al siguiente en lista de espera debitando crédito a ciegas, lo que podía inducir saldos negativos.
- **Solución implementada en V8.1.4:** Al liberarse un cupo, el motor inspecciona el saldo de la alumna en espera (`walletsByStudentId`). Si cuenta con crédito disponible (≥ 1), se confirma la reserva y se efectúa el débito formal; si carece de saldo, la plaza no se asigna a saldo negativo y el inventario regresa a plazas disponibles.
- **Verificación:** Certificado en `tests/test_audit_013_acceptance.js` (Criterio 7).

---

### 2. Hallazgos Técnicos P1 (AUD-013) Corregidos

#### P1-01: Enlace Cinemático de Nodos GLB a Controles Interactivos
- **Problema en V8.1.3:** Al cargar `assets/reformer_studio.glb`, se retiraba el grupo procedimental, pero los controles de "Deslizar Carro" y "Alternar Resortes" continuaban actuando sobre `this.carriageGroup` y `this.springs` (desconectados del árbol de escena).
- **Solución implementada en V8.1.4:** En `src/js/reformer-3d.js`, al cargar el GLB se realiza un recorrido recursivo vinculando el nodo de malla `UpholsteredCarriage` a `this.glbCarriageNode` y las mallas metálicas a `this.glbSpringNodes`. El bucle de animación cinemática (`animate()`) y los disparadores de evento (`glideCarriage()`, `toggleSprings()`) transforman la posición y material del GLB visible de manera idéntica al modelo de respaldo.
- **Verificación:** Inspección estructural de nodos GLTF y pruebas de ciclo de render.

#### P1-02: Documentación de Pruebas de Integración vs. Sellos Estáticos
- **Solución implementada:** Se añadieron suites de prueba de lógica pura (`test_audit_013_acceptance.js`, `test_audit_013_adversarial_p0.js`) con aserciones rigurosas de estado, tiempos de ejecución sub-100ms y diagnósticos detallados, asegurando que los reportes de gobernanza reflejen ejecuciones de motor verificadas y medibles.

---

### 3. Matriz de Invariantes Matemáticas Verificadas (100% PASS)

1. **Invariante de Capacidad:** $\text{Reservas Confirmadas} + \text{Plazas Disponibles} = \text{Capacidad Total de la Sala}$ en todo momento.
2. **Invariante de Conservación Contable:** $\text{Saldo Final} = \text{Saldo Inicial} + \sum(\text{Transacciones del Alumno})$.
3. **Invariante de Idempotencia:** Cancelaciones o reembolsos duplicados sobre el mismo `bookingId` se rechazan y tienen cero impacto en saldo y cupos.
4. **Invariante de No-Sobrecupo ni Sobregiro:** Ninguna alumna puede reservar sin saldo y ninguna promoción de espera induce saldos negativos.

---

### 4. Entregables Canónicos Generados

- **Archivo Maestro de Distribución:** `/home/user/OpenBreak_Cinematic_V8_1_4_Proyecto_Completo.zip`
- **Destino de Auditoría:** Presentado formalmente para someterse a la auditoría independiente **AUD-014**.
