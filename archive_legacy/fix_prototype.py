import re

with open('/home/user/openbreak/prototype.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Reemplazar la lógica de reserva de executeBooking y cancelBooking para manejar colecciones de reservas y no sobrescribir innerHTML
old_js = """    let studentCredits = 3;
    let pendingBooking = null;"""

new_js = """    let studentCredits = 3;
    let pendingBooking = null;
    let activeBookings = [];

    // Base de datos de clases por día (OB-08)
    const scheduleByDay = {
      'Hoy': [
        { id: 1, title: 'Reformer Foundations', instructor: 'Sofía Valdés', time: '08:00 - 08:50', spots: 2, total: 8 },
        { id: 2, title: 'Power Flow Reformer', instructor: 'Camila Morales', time: '09:30 - 10:20', spots: 1, total: 8 },
        { id: 3, title: 'Reformer Jumpboard & Cardio', instructor: 'Mateo Rivas', time: '18:00 - 18:50', spots: 3, total: 8 }
      ],
      'Mañana': [
        { id: 4, title: 'Classic Reformer Alignment', instructor: 'Sofía Valdés', time: '07:30 - 08:20', spots: 4, total: 8 },
        { id: 5, title: 'High Intensity Athletic Pilates', instructor: 'Mateo Rivas', time: '17:30 - 18:20', spots: 2, total: 8 }
      ],
      'Mié 22': [
        { id: 6, title: 'Reformer & Mat Mobility', instructor: 'Camila Morales', time: '08:30 - 09:20', spots: 3, total: 8 }
      ],
      'Jue 23': [
        { id: 7, title: 'Power Core Reformer', instructor: 'Sofía Valdés', time: '09:00 - 09:50', spots: 1, total: 8 }
      ],
      'Vie 24': [
        { id: 8, title: 'Restorative Stretch & Springs', instructor: 'Camila Morales', time: '18:00 - 18:50', spots: 5, total: 8 }
      ]
    };"""

html = html.replace(old_js, new_js)

# Reemplazar selectDay para filtrar clases
old_select_day = """    function selectDay(element, dayLabel) {
      document.querySelectorAll('.day-chip').forEach(el => el.classList.remove('active'));
      element.classList.add('active');
      logAudit(`[UX] Filtro de fecha cambiado a: ${dayLabel}`);
    }"""

new_select_day = """    function selectDay(element, dayLabel) {
      document.querySelectorAll('.day-chip').forEach(el => el.classList.remove('active'));
      element.classList.add('active');
      logAudit(`[UX] Filtro de fecha cambiado a: ${dayLabel}`);
      renderClassList(dayLabel);
    }

    function renderClassList(dayLabel) {
      const container = document.getElementById('classListContainer') || document.querySelector('.classes-list');
      if (!container) return;
      const classes = scheduleByDay[dayLabel] || scheduleByDay['Hoy'];
      
      container.innerHTML = classes.map(c => {
        const isBooked = activeBookings.some(b => b.id === c.id);
        const spotsText = isBooked ? 'Ya estás inscrita' : `${c.spots} de ${c.total} cupos libres`;
        const btnText = isBooked ? 'Inscrita' : 'Reservar Cama';
        const btnDisabled = isBooked ? 'disabled style=\"background: #E2E8F0; color: #64748B; cursor: not-allowed;\"' : '';
        return `
          <div class="class-card" id="card-clase-${c.id}">
            <div class="class-info">
              <span class="spots-indicator ${c.spots <= 1 ? 'spots-warning' : 'spots-available'}" id="spots-${c.id}">${spotsText}</span>
              <div class="class-title">${c.title}</div>
              <div class="class-meta">
                <span>🕒 ${c.time}</span>
                <span>👤 ${c.instructor}</span>
                <span>🏠 Sala Reformer</span>
              </div>
            </div>
            <button class="reserve-btn" ${btnDisabled} onclick="reserveClass(${c.id}, '${c.title}', '${c.time}')">${btnText}</button>
          </div>
        `;
      }).join('');
    }"""

html = html.replace(old_select_day, new_select_day)

# Reemplazar executeBooking para prevenir doble reserva y apilar reservas
old_execute = """    function executeBooking() {
      if (!pendingBooking) return;
      studentCredits--;
      document.getElementById('creditCount').innerText = `${studentCredits} créditos`;
      
      // Update UI
      const card = document.getElementById('card-clase-' + pendingBooking.id);
      const spotsEl = document.getElementById('spots-' + pendingBooking.id);
      if (spotsEl) {
        spotsEl.innerText = "1 de 8 cupos libres";
        spotsEl.className = "spots-indicator spots-warning";
      }

      // Add to bookings list
      const bookingsContainer = document.getElementById('studentBookings');
      bookingsContainer.innerHTML = `
        <div style="background: #F8FAFC; border: 1px solid var(--border); border-radius: 8px; padding: 10px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div style="font-weight: 600; font-size: 0.82rem; color: #1E293B;">${pendingBooking.title}</div>
            <div style="font-size: 0.72rem; color: var(--text-muted);">Hoy · ${pendingBooking.time}</div>
          </div>
          <button style="border: none; background: #FEE2E2; color: #991B1B; font-size: 0.72rem; padding: 4px 8px; border-radius: 6px; font-weight: 600; cursor: pointer;" onclick="cancelBooking(this, '${pendingBooking.title}')">Cancelar</button>
        </div>
      `;

      logAudit(`[RESERVA_EXITOSA] Alumno reservó '${pendingBooking.title}'. Créditos restantes: ${studentCredits}`);
      closeModal();
      alert(`¡Reserva confirmada con éxito! Te hemos enviado un correo con el comprobante.`);
    }"""

new_execute = """    function executeBooking() {
      if (!pendingBooking) return;
      
      // Prevenir doble reserva (OB-08)
      if (activeBookings.some(b => b.id === pendingBooking.id)) {
        alert("Ya cuentas con una reserva activa para esta misma clase.");
        closeModal();
        return;
      }

      studentCredits--;
      document.getElementById('creditCount').innerText = `${studentCredits} créditos`;
      activeBookings.push({ ...pendingBooking });

      // Render lista acumulada de reservas
      renderStudentBookings();

      // Refrescar listado del día activo
      const activeDay = document.querySelector('.day-chip.active')?.textContent.trim() || 'Hoy';
      renderClassList(activeDay);

      logAudit(`[RESERVA_EXITOSA] Alumno reservó '${pendingBooking.title}'. Créditos restantes: ${studentCredits}`);
      closeModal();
      alert(`¡Reserva confirmada con éxito! Cama asignada en sala.`);
    }

    function renderStudentBookings() {
      const bookingsContainer = document.getElementById('studentBookings');
      if (!bookingsContainer) return;

      if (activeBookings.length === 0) {
        bookingsContainer.innerHTML = '<div style="font-size: 0.8rem; color: var(--text-muted);">No tienes reservas activas por el momento.</div>';
        return;
      }

      bookingsContainer.innerHTML = activeBookings.map(b => `
        <div style="background: #F8FAFC; border: 1px solid var(--border); border-radius: 8px; padding: 10px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div style="font-weight: 600; font-size: 0.82rem; color: #1E293B;">${b.title}</div>
            <div style="font-size: 0.72rem; color: var(--text-muted);">Sesión · ${b.time}</div>
          </div>
          <button style="border: none; background: #FEE2E2; color: #991B1B; font-size: 0.72rem; padding: 4px 8px; border-radius: 6px; font-weight: 600; cursor: pointer;" onclick="cancelBookingById(${b.id}, '${b.title}')">Cancelar</button>
        </div>
      `).join('');
    }

    function cancelBookingById(classId, title) {
      if (confirm(`¿Deseas cancelar tu reserva para '${title}'? Al ser con anticipación reglamentaria, tu crédito se reembolsará automáticamente.`)) {
        activeBookings = activeBookings.filter(b => b.id !== classId);
        studentCredits++;
        document.getElementById('creditCount').innerText = `${studentCredits} créditos`;
        renderStudentBookings();
        
        const activeDay = document.querySelector('.day-chip.active')?.textContent.trim() || 'Hoy';
        renderClassList(activeDay);

        logAudit(`[CANCELACION] Reserva cancelada para '${title}'. Crédito restituido.`);
      }
    }"""

html = html.replace(old_execute, new_execute)

with open('/home/user/openbreak/prototype.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("prototype.html successfully updated with state management and date filtering!")
