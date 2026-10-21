# Open Break — Plan Integral de Producto, UX y Roadmap del MVP (8-12 Semanas)

**Versión:** 1.0 · Octubre 2026  
**Documento base:** *Plan Maestro 4 Negocios 2026*  
**Stack tecnológico seleccionado:** FastAPI (Python) + PostgreSQL (Supabase) + Next.js / Tailwind CSS (Frontend)

---

## 1. Definición del Producto y Alcance del MVP

### 1.1 Objetivo del MVP
Construir una plataforma vertical ágil, limpia y sin fricción para estudios boutique (pilates, yoga, funcional, danza, artes marciales) de 80 a 300 alumnos activos, resolviendo cuatro dolores críticos:
1. **Sobrecupo cero:** Transacciones atómicas de reserva y lista de espera automática.
2. **Saldo de créditos intocable:** Bitácora inmutable de créditos adquiridos, consumidos y reintegrados con ventanas de cancelación justas.
3. **Cobros transparentes y webhook idempotente:** 0% de comisión propia sobre transacciones del estudio; pagos directos con Stripe / transferencias.
4. **Adopción móvil instantánea:** El alumno reserva desde enlace web responsive en 3 toques, sin forzar descarga de apps ni registros pesados.

---

## 2. Mapa de Experiencia de Usuario (UX Workflows)

### Flujo A: Alumno (Reserva web móvil sin fricción)
1. **Acceso:** Enlace de marca del estudio (`openbreak.app/estudio/luna-pilates` o dominio personalizado).
2. **Exploración:** Calendario interactivo filtrable por:
   * Tipo de disciplina (Reformer, Mat, Barre, etc.)
   * Instructor / Coach
   * Sala / Ubicación
   * Horario (Mañana / Tarde / Noche)
3. **Selección de Clase:**
   * Muestra cupo disponible en tiempo real (ej. `8/10 cupos ocupados`).
   * Si la clase está llena, muestra botón: `Unirse a lista de espera (Posición #2)`.
4. **Confirmación y Débito de Crédito:**
   * *Si tiene paquete activo:* Se confirma la reserva en un clic debitando 1 crédito de su paquete con mayor proximidad de expiración.
   * *Si no tiene créditos:* Se despliega selector de compra rápida de paquete (ej. Single Drop-in $250, Pack 5 clases $1,100, Pack 10 clases $1,900) con checkout integrado de Stripe.
5. **Comprobante y Calendario:** Notificación inmediata por correo, opción de añadir a Google Calendar / Apple Calendar, y ventana de cancelación clara (ej. *«Cancela hasta 6 hrs antes para recuperar tu crédito»*).

---

### Flujo B: Administrador / Recepción del Estudio
1. **Panel Principal (Dashboard del Día):**
   * Vista de hoy: Horarios, instructores, tasa de ocupación por hora y alertas de sobredemanda.
   * Check-in de recepción: Lista de asistencia con botón de 1 toque (Asistió / Falta con aviso / No-show).
2. **Gestor de Clases y Horarios:**
   * Creación de clases recurrentes (ej. Martes y Jueves 7:00 AM con Instructor Mariana, Cupo 12).
   * Modificación ágil de suplencias de instructores o cancelación excepcional con devolución automática de créditos y notificación masiva.
3. **Gestor de Paquetes y Clientes (CRM ligero):**
   * Ficha de alumno: Paquete activo, fecha de caducidad, bitácora de asistencia e historial de transacciones.
   * Ajuste manual de créditos con motivo auditado (ej. *«Cortesía por problema de tráfico reportado»*).
4. **Liquidación y Conciliación:**
   * Reporte de asistencia por instructor (para cálculo de comisiones u honorarios).
   * Exportación instantánea a CSV de todas las transacciones para conciliar con el banco.

---

## 3. Matriz de Estados de la Lógica de Negocio (Reglas Críticas)

| Escenario | Comportamiento del Sistema | Protección de la Operación |
| :--- | :--- | :--- |
| **Reserva simultánea (Concurrencia)** | Bloqueo pesimista a nivel de base de datos (`SELECT FOR UPDATE` en cupos). Si se acaba el último cupo, el segundo intento entra automáticamente en lista de espera. | Cero sobrecupos físicos en el estudio. |
| **Cancelación a tiempo (> 6 hrs antes)** | Se libera el cupo inmediatamente. Se reintegra 1 crédito al paquete original del alumno con la vigencia original. Se promueve automáticamente a la persona #1 en lista de espera enviándole notificación con ventana de 30 min para aceptar o confirmación directa. | Maximiza ocupación y trato justo al alumno. |
| **Cancelación tardía (< 6 hrs antes)** | Se libera el cupo para que alguien más pueda tomarlo, pero **no** se devuelve el crédito al alumno. | Protege el ingreso del estudio y el pago del instructor. |
| **Pago digital con Stripe** | Se procesa vía Stripe Checkout / Elements. La asignación del paquete sólo ocurre tras la recepción del webhook verificado (`checkout.session.completed`) mediante transacción idempotente. | Imposibilidad de acreditar saldo si el pago rebota o si el usuario cierra el navegador a medio proceso. |

---

## 4. Cronograma de Desarrollo (Roadmap de 10 Semanas)

```
Semanas 1-2:   Arquitectura, Modelado SQL (Postgres), Autenticación Multi-tenant y API base en FastAPI.
Semanas 3-4:   Motor de Reservas Atómicas, Bitácora de Créditos y Webhooks de Stripe.
Semanas 5-6:   Frontend de Alumnos (Next.js responsive móvil, calendario, checkout rápido).
Semanas 7-8:   Panel de Administración y Recepción (Check-in, CRM de alumnos, creador de horarios).
Semanas 9-10:  Pruebas de estrés y concurrencia, métricas, CSV export y Onboarding del Estudio Fundador.
```
