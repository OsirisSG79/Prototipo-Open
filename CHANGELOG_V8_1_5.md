# Open Break Changelog — V8.1.5 (Corrective Release — Wallet Integrity & Multi-User Hardening)

**Fecha:** 26 de octubre de 2026  
**Rama:** `fix/openbreak-v8-1-5-wallet-integrity`  
**Referencia de auditoría:** AUD-014 Dictamen (`OPEN_BREAK_AUD-014_V8_1_4_DICTAMEN_Y_PLAN_V8_1_5.md`)  
**Próxima auditoría:** AUD-015  

## Resumen Ejecutivo
Versión correctiva estricta orientada a resolver las tres fallas de severidad P0 identificadas en el dictamen independiente AUD-014 relativas a la gestión y contabilidad de billeteras multi-alumna (`P0-01`, `P0-02`, `P0-03`). Se preservan íntegramente al 100% las 22 suites del pipeline rápido (`run_fast_audits.sh`), la totalidad de los 100 tests del runner canonical (`run_all_audits.sh`), y la integridad de todas las cinemáticas e invariantes visuales (efecto máquina de escribir cinética, túnel 3D de 12 paneles, modelo Three.js GLB del Reformer, ribbon y cursor).

---

## Detalle de Correcciones P0 (AUD-014 Remediation)

### 1. [P0-01] Abolición del cuello de botella de saldo global en reservas multi-alumna
- **Problema previo (V8.1.4):** `bookClass()` y `ledgerBookSpot()` consultaban la billetera de la alumna pero también bloqueaban arbitrariamente si `this.credits <= 0`. Al reservar una alumna (Ana), el contador global descendía a 0 y bloqueaba a otras alumnas solventes (Beto) que disponían de créditos propios.
- **Resolución V8.1.5:**
  - Se desacopló la autorización multi-alumna del contador global. Cuando una alumna cuenta con una cuenta/billetera registrada (e.g. Ana, Beto via `registerStudent`), la autorización evalúa **exclusivamente** el saldo de su propia billetera (`walletsByStudentId.get(student.id)`).
  - El saldo global `this.credits` se mantiene como vista sincronizada para la persona demo principal (`Camila Morales`) y para el pool compartido de la demostración interactiva sin desfasar el DOM.

### 2. [P0-02] Eliminación de créditos fantasma en consultas de lectura y registro formal
- **Problema previo (V8.1.4):** Una simple lectura mediante `getStudentBalance()` o consultas de existencia creaban cuentas implícitas y les acreditaban `this.openingBalance` (8 créditos) de forma automática sin transacción respaldatoria. Además, `registerStudent()` otorgaba saldo sin asentar transacciones de tipo `PURCHASE`.
- **Resolución V8.1.5:**
  - Función de búsqueda pura `_findStudent()` implementada: `getStudentBalance('Persona Desconocida')` retorna `0` limpiamente sin mutar el estado ni crear registros fantasma.
  - `registerStudent(studentId, initialCredits)` ahora crea un movimiento contable formal e inmutable `PURCHASE` vinculado al `studentId` en `transactions` y `transactionsById`.
  - Invariante matemático reforzado en `verifyLedgerIntegrity()`: verifica la suma de transacciones y valida que para cada alumna registrada, $\sum \text{tx}_{\text{alumna}} = \text{billetera}_{\text{alumna}}$.

### 3. [P0-03] Recargas transaccionales auditadas en `creditStudent()`
- **Problema previo (V8.1.4):** `creditStudent()` incrementaba el balance de la alumna sin asentar ninguna transacción en el libro mayor (`transactions`), dejando la contabilidad vulnerable a discordancias.
- **Resolución V8.1.5:**
  - `creditStudent(studentId, amount, description)` valida que el monto sea un número estrictamente positivo (> 0); entradas inválidas o negativas se rechazan con retorno `0` sin efectos secundarios.
  - Cada recarga emite una transacción formal `PURCHASE` auditada con timestamp, `studentId`, `studentName`, `amount` y balance posterior, incorporada inmediatamente a `transactions` y `transactionsById`.

---

## Cobertura de Pruebas & Certificación
1. **Nueva Suite Adversarial AUD-014 (`tests/test_audit_014_adversarial_p0.js`):**
   - Caso P0-01: Verificación de independencia de débito entre Ana y Beto con Camila en demo balance = 1.
   - Caso P0-02: Consultas puras sin creación de balance fantasma y transacciones de apertura formales en `registerStudent()`.
   - Caso P0-03: Asiento de auditoría obligatorio en `creditStudent()` y rechazo de montos negativos.
   - Caso P0-04: Rechazo de cancelaciones cruzadas y salto de candidatas insolventes en la lista de espera FIFO preservando a las solventes.
2. **Fast Integration Pipeline (`scripts/run_fast_audits.sh`):**
   - 22 suites ejecutadas en ~3.6 segundos con **100% PASS**.
3. **Canonical 100-Suite Runner (`bash ./run_all_audits.sh`):**
   - 100/100 suites verificadas con **100% PASS**.
4. **Portabilidad de Entrega:**
   - Script `scripts/test_portable_execution.sh` actualizado a V8.1.5.
