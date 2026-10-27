# Open Break — CHANGELOG V8.1.2 (Patch de Integridad Multiusuario, QA y Empaquetado)
**Fecha:** 26 de octubre de 2026  
**Rama:** `fix/openbreak-v8-1-2-integrity`  
**Referencia:** Dictamen independiente `OPEN_BREAK_AUD-011_V8_1_1_AUDITORIA_Y_PLAN_V8_1_2.md`

## Resumen Ejecutivo de Cambios

La versión **V8.1.2** es una entrega estrictamente correctiva y de aseguramiento de calidad (QA) que erradica los hallazgos críticos (P0) y observaciones técnicas del dictamen AUD-011, preservando al 100% el diseño visual, las animaciones cinemáticas, el túnel espacial y la física interactiva.

---

### 1. Hallazgos AUD-011 Corregidos

#### P0-01: Invariante Multiusuario y Eliminación de Sobrescritura en Clases Multi-Cama
- **Problema previo:** `activeBookings` utilizaba un `Map` indexado únicamente por `classId`. Si dos alumnas reservaban una clase de 2 camas, la segunda sobrescribía a la primera en el mapa, imposibilitando la cancelación individual y perdiendo la trazabilidad.
- **Solución implementada:** Migración integral en `src/js/demo-store.js` a arquitectura multi-índice relacional:
  - `bookingsById: Map<bookingId, BookingRecord>` (clave primaria atómica).
  - `bookingsByClass: Map<classId, Set<bookingId>>` (índice secundario por clase).
  - `bookingsByStudent: Map<studentName, Set<bookingId>>` (índice por alumna).
- **Verificación:** Nueva suite automatizada `tests/test_audit_063_multibed_booking_invariance.py` ejecutada al 100% PASS.

#### P1-02A: Corrección del Saldo Inicial `balanceAfter`
- **Problema previo:** En `new DemoStore(8)`, la transacción de apertura `PURCHASE +8` calculaba `balanceAfter: 16` porque `credits` ya valía 8 antes de la llamada.
- **Solución implementada:** Inicialización de `credits = 0`, registro de apertura con `amount: 8` y asignación correcta de `balanceAfter: 8`.

#### P0-02: Promoción de Waitlist con Transacción Legítima en el Ledger
- **Problema previo:** La promoción automática creaba un registro con `debitTxId: 'promo_credit_hold'` sin una transacción real de débito en el historial financiero.
- **Solución implementada:** Generación de la transacción contable formal `WAITLIST_PROMOTION_DEBIT` (-1 crédito) con ID criptográfico, balance recalculado y vinculación directa al booking promovido.
- **Verificación:** Nueva suite automatizada `tests/test_audit_064_waitlist_promotion_debit.py` ejecutada al 100% PASS.

#### P0-03: Empaquetado Portátil con Permisos UNIX y Eliminación de Rutas Fijas
- **Problema previo:** Al descomprimir el ZIP entregado, `test_portable_execution.sh` y otros scripts carecían del bit de ejecución (`0o755`), haciendo fallar el pipeline en la décima suite. Adicionalmente, varias pruebas exigían la ruta absoluta `/home/user/...`.
- **Solución implementada:**
  - Creado `scripts/make_release_zip.py` que inyecta atributos POSIX `stat.S_IFREG | 0o755` para todos los `.sh` y `.py`.
  - Desvinculación de `/home/user/...` en favor de rutas relativas dinámicas en todas las pruebas.
  - Verificación de ejecución limpia en `/tmp` con `test_portable_execution.sh`.

#### P1-04: Carga e Integración del Modelo 3D glTF (`assets/reformer_studio.glb`)
- **Problema previo:** `src/js/reformer-3d.js` renderizaba primitivas procedimentales Three.js y nunca invocaba a `GLTFLoader.load()` para cargar el archivo binario glTF.
- **Solución implementada:** Conexión formal en `reformer-3d.js` a través del método `loadGlbOrFallback()`, cargando el GLB oficial si `GLTFLoader` está presente y conservando la degradación visual procedimental/fotográfica de forma transparente y sin bloqueos de pantalla.

---

### 2. Estado de la Batería de Pruebas

- **Total de Suites Canónicas:** **64 suites automatizadas**
- **Tasa de Aprobación:** **100% (64/64 PASS)**
- **Prueba en Directorio Aislado (`/tmp`):** **100% PASS**

---

### 3. Entregable Canónico

- **Archivo Maestro:** `/home/user/OpenBreak_Cinematic_V8_1_2_Proyecto_Completo.zip` (7,926,204 bytes)
- **Hash SHA-256:** Calculado y verificado en `AUD-025`.
- **Destino de Auditoría:** Listo para someterse a la auditoría independiente **AUD-012**.
