# Política Operativa de Lista de Espera FIFO, Elegibilidad y Reservas

**Versión:** 1.0.0 (V8.1.5 / AUD-015)  
**Módulo:** Open Break Engine · Gestión de Cupos y Espera Determinista  

---

## 1. Principio Fundamental
El objetivo de la Lista de Espera en Open Break es maximizar la ocupación de las camas y estudios de Pilates Reformer sin incurrir en sobreventa, garantizando equidad entre las alumnas y transparencia operativa para la recepción.

---

## 2. Reglas de Encolamiento (Ingreso a la Fila)
1. **Orden Determinista FIFO:**  
   Las solicitudes de lista de espera se ordenan estrictamente por marca de tiempo (`timestamp` / `joinedAt`) de llegada al servidor.
2. **Registro de Turno Único:**  
   Una alumna no puede registrar múltiples turnos activos para la misma clase. Si ya cuenta con una reserva confirmada o ya está en la lista de espera, la solicitud es rechazada (`already_booked` / `already_on_waitlist`).
3. **Cero Retención Anticipada de Saldo:**  
   Al unirse a la lista de espera **no se debita saldo preventivo**. La deducción de créditos solo ocurre al momento de confirmarse formalmente la promoción.

---

## 3. Criterios de Elegibilidad y Promoción

Cuando una alumna con reserva confirmada cancela su plaza oportunamente (ventana de cancelación con aviso previo >12 hrs), el sistema evalúa la cola de espera de forma secuencial:

### A. Alumna Elegible (Solvente)
* Se evalúa si la alumna en la posición actual de la cola posee al menos **1 crédito válido** en su billetera.
* Si el saldo es $\ge 1$:
  1. Se promueve de inmediato a la clase (`status = CONFIRMED_FROM_WAITLIST`).
  2. Se asienta una transacción inmutable de débito en el libro mayor (`WAITLIST_PROMOTION_DEBIT`).
  3. Se genera un `bookingId` único e indexado.
  4. La capacidad disponible de la clase se preserva ocupada (`spots = 0`).

### B. Alumna Ineligible (Insolvente / Sin Saldo)
* Si la alumna que encabeza la cola cuenta con **0 créditos**:
  1. **Política de Salto y Retención en Cola:** El sistema no le cancela su antigüedad en la fila; sin embargo, para no congelar la plaza del estudio, el asignador automático evalúa inmediatamente a la **siguiente alumna solvente** en orden FIFO.
  2. **Notificación de Recarga Pendiente:** En el flujo operativo previsto, la alumna sin saldo recibe un aviso indicando que hubo una plaza disponible que no pudo asignarse por falta de saldo, invitándole a recargar paquete.
  3. Al recargar saldo, la alumna recupera su prioridad de turno para futuras cancelaciones de esa misma sesión.

---

## 4. Ventana de Cancelación y Reembolso

| Condición | Reembolso de Crédito | Acción en Lista de Espera |
| :--- | :---: | :--- |
| **Cancelación Oportuna (> 12 hrs)** | **Sí** (+1 crédito vía `BOOKING_REFUND`) | Promoción automática de la siguiente alumna elegible en FIFO. |
| **Cancelación Tardía (< 12 hrs)** | **No** (sin reintegro de crédito) | Se libera el lugar físicamente para que otra alumna en espera pueda aprovecharlo. |
| **No-Show (Inasistencia)** | **No** (sin reintegro) | Se mantiene el débito original protegiendo el honorario de la instructora. |

---

## 5. Arquitectura de Integración (Demostración vs. Producción)
* **Entorno Demostración (Frontend / Store Local):**  
  La simulación interactiva local ejecuta la máquina de estados determinista en memoria (`DemoStore`), aplicando las mismas reglas de integridad contable y de balance per-student descritas en este documento.
* **Entorno Producción Backend:**  
  La asignación atómica se orquesta a nivel de motor de base de datos con transacciones serializables (`SELECT FOR UPDATE`), garantizando cero sobrecupos y emitiendo eventos webhook para confirmaciones vía correo electrónico o canales de mensajería configurados por el estudio.
