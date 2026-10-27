/**
 * Open Break — Synchronized Boutique Schedule & Mobile App (R3 + R4 / V8)
 * Deterministic shared state between weekly desktop calendar and student smartphone
 * backed by centralized window.OpenBreakStore (V7-01 resolution).
 */

const boutiqueScheduleData = [
  // LUNES 19
  [
    { id: 'c1', title: 'Reformer Core Foundations', time: '07:30 - 08:20', coach: 'Camila Morales', spots: 2, total: 8, tag: 'Principiantes' },
    { id: 'c2', title: 'Athletic Reformer & Springs', time: '09:00 - 09:50', coach: 'Mateo Rivas', spots: 0, total: 8, tag: 'Waitlist Activa' },
    { id: 'c3', title: 'Reformer Sculpt Pro', time: '18:00 - 18:50', coach: 'Sofía Valdés', spots: 1, total: 8, tag: 'Último Cupo' },
    { id: 'c4', title: 'Classic Reformer Flow', time: '19:30 - 20:20', coach: 'Sofía Valdés', spots: 2, total: 8, tag: 'Nivel Mixto' }
  ],
  // MARTES 20
  [
    { id: 'c5', title: 'Jumpboard Cardio & Core', time: '08:00 - 08:50', coach: 'Mateo Rivas', spots: 3, total: 8, tag: 'Alta Intensidad' },
    { id: 'c6', title: 'Precision Alignment', time: '10:00 - 10:50', coach: 'Camila Morales', spots: 4, total: 8, tag: 'Técnica Clásica' },
    { id: 'c7', title: 'Evening Stretch & Flow', time: '18:30 - 19:20', coach: 'Sofía Valdés', spots: 2, total: 8, tag: 'Recuperación' }
  ],
  // MIÉRCOLES 21
  [
    { id: 'c8', title: 'Reformer Power Hour', time: '07:00 - 07:50', coach: 'Mateo Rivas', spots: 1, total: 8, tag: 'Intensivo' },
    { id: 'c9', title: 'Reformer Flow & Mat', time: '09:30 - 10:20', coach: 'Camila Morales', spots: 5, total: 8, tag: 'Abierto' },
    { id: 'c10', title: 'Athletic Jumps & Springs', time: '19:00 - 19:50', coach: 'Mateo Rivas', spots: 0, total: 8, tag: 'Waitlist' }
  ],
  // JUEVES 22
  [
    { id: 'c11', title: 'Full Body Sculpt', time: '08:30 - 09:20', coach: 'Sofía Valdés', spots: 2, total: 8, tag: 'Tonificación' },
    { id: 'c12', title: 'Core & Glutes Signature', time: '18:00 - 18:50', coach: 'Camila Morales', spots: 1, total: 8, tag: 'Cupo Limitado' }
  ],
  // VIERNES 23
  [
    { id: 'c13', title: 'Weekend Warmup Flow', time: '09:00 - 09:50', coach: 'Sofía Valdés', spots: 4, total: 8, tag: 'Energía' },
    { id: 'c14', title: 'Candlelight Restorative', time: '18:00 - 18:50', coach: 'Camila Morales', spots: 3, total: 8, tag: 'Relajación' }
  ],
  // SÁBADO 24
  [
    { id: 'c15', title: 'Saturday Masterclass', time: '09:30 - 10:45', coach: 'Sofía & Mateo', spots: 1, total: 8, tag: 'Especial 75min' },
    { id: 'c16', title: 'Post-Workout Mobility', time: '11:15 - 12:05', coach: 'Camila Morales', spots: 5, total: 8, tag: 'Flexibilidad' }
  ],
  // DOMINGO 25
  [
    { id: 'c17', title: 'Sunday Reset Flow', time: '10:00 - 10:50', coach: 'Sofía Valdés', spots: 6, total: 8, tag: 'Suave' }
  ]
];

// Fallback standalone store if demo-store.js hasn't loaded (e.g. isolated test environments)
if (typeof window !== 'undefined' && !window.OpenBreakStore) {
  const localClasses = new Map(boutiqueScheduleData.flat().map(c => [c.id, { ...c }]));
  const localActive = new Set(['c3']);
  const localWaiting = new Set();
  let localCreds = 8;
  window.OpenBreakStore = {
    get credits() { return localCreds; },
    set credits(v) { localCreds = v; },
    get activeBookings() { return localActive; },
    get waitlists() {
      const map = new Map();
      localWaiting.forEach(id => map.set(id, ['Camila Morales']));
      return map;
    },
    getClass(id) { return localClasses.get(id); },
    getAllClasses() { return Array.from(localClasses.values()); },
    initClasses(arr) { localClasses.clear(); arr.forEach(c => localClasses.set(c.id, { ...c })); },
    bookClass(id) {
      const c = localClasses.get(id);
      if (!c) return { success: false, reason: 'not_found' };
      if (localActive.has(id)) return { success: false, reason: 'already_booked' };
      if (c.spots <= 0) { localWaiting.add(id); return { success: true, waitlist: true, position: 1 }; }
      if (localCreds <= 0) return { success: false, reason: 'no_credits' };
      c.spots--; localCreds--; localActive.add(id);
      return { success: true, waitlist: false };
    },
    cancelBooking(id) {
      if (!localActive.has(id)) return { success: false, reason: 'not_booked' };
      localActive.delete(id); localCreds++;
      const c = localClasses.get(id); if (c) c.spots++;
      return { success: true };
    },
    ledgerBookSpot() { if (localCreds <= 0) return { success: false }; localCreds--; return { success: true, credits: localCreds }; },
    ledgerRefundSpot() { localCreds++; return { success: true, credits: localCreds }; }
  };
}

// Proxies for backwards compatibility with tests and inspectability
const store = (typeof window !== 'undefined' && window.OpenBreakStore) ? window.OpenBreakStore : null;
const classById = {
  get(id) { return (typeof window !== 'undefined' && window.OpenBreakStore) ? window.OpenBreakStore.getClass(id) : null; }
};
const activeBookings = {
  has(id) { return (typeof window !== 'undefined' && window.OpenBreakStore) ? window.OpenBreakStore.activeBookings.has(id) : false; },
  delete(id) { return (typeof window !== 'undefined' && window.OpenBreakStore) ? window.OpenBreakStore.cancelBooking(id).success : false; }
};
const waiting = {
  has(id) {
    if (typeof window === 'undefined' || !window.OpenBreakStore) return false;
    const q = window.OpenBreakStore.waitlists.get(id);
    return Array.isArray(q) ? q.length > 0 : Boolean(q);
  }
};

let userCredits = 8;
if (typeof window !== 'undefined') {
  window.userCredits = userCredits;
  Object.defineProperty(window, 'userCredits', {
    get() { return window.OpenBreakStore ? window.OpenBreakStore.credits : userCredits; },
    set(v) { if (window.OpenBreakStore) window.OpenBreakStore.credits = v; userCredits = v; },
    configurable: true
  });
}

let selectedScheduleDay = 0;
let currentBookingId = 'c3';

function scheduleNotice(message) {
  const node = document.getElementById('scheduleFeedback');
  if (node) node.textContent = message;
  if (typeof window !== 'undefined') window.openbreakLastScheduleMessage = message;
}

function updateCreditsDisplay() {
  const currentCreds = (typeof window !== 'undefined' && window.OpenBreakStore) ? window.OpenBreakStore.credits : userCredits;
  userCredits = currentCreds;
  for (const id of ['appCreditsBadge', 'creditsDisplay']) {
    const el = document.getElementById(id);
    if (el) el.textContent = `${currentCreds} CR`;
  }
  const walletBalance = document.getElementById('appWalletBalance');
  if (walletBalance) {
    walletBalance.textContent = `${currentCreds} Créditos`;
  }
}

function syncPhone() {
  const currentStore = (typeof window !== 'undefined') ? window.OpenBreakStore : null;
  const currentActive = currentStore ? currentStore.activeBookings : new Set();
  const card = document.getElementById('appBookingCard');
  const title = document.getElementById('appBookingTitle');
  
  // P0-04 (AUD-013) Fix: Only derive current booking from Camila's own bookings
  const studentBookings = (typeof currentStore?.getBookingsForStudent === 'function')
    ? currentStore.getBookingsForStudent('Camila Morales')
    : [];
  
  if (!currentBookingId || (studentBookings.length > 0 && !studentBookings.some(b => b.bookingId === currentBookingId))) {
    currentBookingId = studentBookings.length > 0 ? studentBookings[studentBookings.length - 1].bookingId : null;
  }

  if (card) card.style.display = currentBookingId ? 'block' : 'none';
  if (title) {
    let bookingRecord = currentStore?.bookingsById?.get(currentBookingId);
    let classId = bookingRecord ? bookingRecord.classId : currentBookingId;
    const cls = currentStore ? currentStore.getClass(classId) : null;
    title.textContent = currentBookingId ? (cls?.title || 'Clase reservada') : '';
  }
  const qr = document.getElementById('appQrOverlay');
  if (qr && !currentBookingId) qr.style.display = 'none';

  updateCreditsDisplay();
}

function renderScheduleDay(dayIndex) {
  selectedScheduleDay = dayIndex;
  for (let i = 0; i < 7; i++) {
    const btn = document.getElementById(`cal-day-${i}`);
    if (!btn) continue;
    const selected = (i === dayIndex);
    btn.classList.toggle('active', selected);
    btn.setAttribute('aria-selected', String(selected));
    btn.style.border = selected ? '1.5px solid var(--accent-orange)' : '1px solid var(--border-subtle)';
    btn.style.background = selected ? '#FFF5EE' : 'var(--bg-gray-subtle)';
  }

  const list = document.getElementById('calendarClassesList');
  if (!list) return;
  list.replaceChildren();

  const currentStore = (typeof window !== 'undefined') ? window.OpenBreakStore : null;
  const currentActive = currentStore ? currentStore.activeBookings : new Set();
  const currentWaitlists = currentStore ? currentStore.waitlists : new Map();

  for (const raw of boutiqueScheduleData[dayIndex] || []) {
    const c = currentStore ? (currentStore.getClass(raw.id) || raw) : raw;
    const reserved = currentActive.has(c.id);
    const queue = currentWaitlists.get(c.id) || [];
    const queued = Array.isArray(queue) ? queue.includes('Camila Morales') : Boolean(queue);
    const full = c.spots === 0;

    const card = document.createElement('article');
    card.className = 'ob-schedule-class';
    const info = document.createElement('div');
    const when = document.createElement('div');
    when.className = 'ob-schedule-meta';
    when.textContent = `${c.time} · ${c.spots} de ${c.total} cupos libres`;
    const heading = document.createElement('h4');
    heading.textContent = c.title;
    const coach = document.createElement('p');
    coach.textContent = `Coach ${c.coach} · Sala Reformer`;
    info.append(when, heading, coach);

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'ob-schedule-book';
    button.textContent = reserved ? 'Reservada' : queued ? 'En espera' : full ? 'Unirse a espera' : 'Reservar';
    button.disabled = reserved || queued;
    button.addEventListener('click', () => bookFromDeskSchedule(c.id));

    card.append(info, button);
    list.append(card);
  }
}

function switchScheduleDay(index) {
  renderScheduleDay(index);
}

function bookFromDeskSchedule(classId) {
  const currentStore = (typeof window !== 'undefined') ? window.OpenBreakStore : null;
  if (!currentStore) return false;
  
  const result = currentStore.bookClass(classId);
  userCredits = currentStore.credits;
  
  if (!result.success) {
    if (result.reason === 'already_booked') scheduleNotice('Esa clase ya está reservada. No se descontó otro crédito.');
    else if (result.reason === 'already_on_waitlist') scheduleNotice('Ya estás en espera de esa clase.');
    else if (result.reason === 'no_credits') scheduleNotice('No tienes créditos disponibles para esta demostración.');
    else scheduleNotice('Clase no disponible.');
    return false;
  }

  if (result.waitlist) {
    scheduleNotice(`Te agregamos a la lista de espera (Turno #${result.position}). Sin descontar créditos.`);
  } else {
    currentBookingId = result.bookingId || classId;
    scheduleNotice(`Reserva de demostración confirmada. Un crédito utilizado.`);
  }

  syncPhone();
  renderScheduleDay(selectedScheduleDay);
  return result.waitlist ? 'waitlist' : true;
}

function appCancelBooking() {
  const currentStore = (typeof window !== 'undefined') ? window.OpenBreakStore : null;
  const id = currentBookingId;
  if (!currentStore || !id) {
    scheduleNotice('No hay una reserva activa para cancelar.');
    return false;
  }

  // P1-03 Fix: pass currentBookingId explicitly
  const result = currentStore.cancelBooking(id);
  userCredits = currentStore.credits;
  if (!result.success) {
    scheduleNotice('No hay una reserva activa para cancelar.');
    return false;
  }

  // P0-04 (AUD-013) Fix: Never derive booking ID from classId iterable
  // Maintain currentBookingId strictly from student's active bookings
  const studentBookings = (typeof currentStore.getBookingsForStudent === 'function')
    ? currentStore.getBookingsForStudent('Camila Morales')
    : [];
  currentBookingId = (studentBookings && studentBookings.length > 0)
    ? studentBookings[studentBookings.length - 1].bookingId
    : null;

  scheduleNotice('Reserva cancelada. Una plaza y un crédito fueron devueltos una sola vez.');
  syncPhone();
  renderScheduleDay(selectedScheduleDay);
  return true;
}

function appBookFastClass(title, time) {
  const currentStore = (typeof window !== 'undefined') ? window.OpenBreakStore : null;
  const all = currentStore ? currentStore.getAllClasses() : boutiqueScheduleData.flat();
  const c = all.find(cls => cls.title === title && cls.time.startsWith(time));
  if (!c) {
    scheduleNotice('Clase de demostración no disponible.');
    return false;
  }
  return bookFromDeskSchedule(c.id);
}

function appTriggerCheckIn() {
  if (!currentBookingId) {
    scheduleNotice('Reserva una clase primero para ver tu pase de prueba.');
    return;
  }
  const box = document.getElementById('appQrOverlay');
  if (box) box.style.display = box.style.display === 'none' ? 'block' : 'none';
}

// React to all global store updates
if (typeof window !== 'undefined') {
  window.addEventListener('openbreak:state-changed', () => {
    updateCreditsDisplay();
    renderScheduleDay(selectedScheduleDay);
    syncPhone();
  });

  window.addEventListener('DOMContentLoaded', () => {
    if (window.OpenBreakStore) {
      window.OpenBreakStore.initClasses(boutiqueScheduleData.flat());
    }
    renderScheduleDay(0);
    syncPhone();
  });
}

// Interactive Smartphone App Tabs Navigation
window.switchAppTab = function(tabName) {
  const tabs = {
    classes: document.getElementById('appTabClasses'),
    waitlist: document.getElementById('appTabWaitlist'),
    wallet: document.getElementById('appTabWallet')
  };
  const btns = {
    classes: document.getElementById('appNavBtnClasses'),
    waitlist: document.getElementById('appNavBtnWaitlist'),
    wallet: document.getElementById('appNavBtnWallet')
  };

  for (const [key, tabEl] of Object.entries(tabs)) {
    if (!tabEl) continue;
    tabEl.style.display = (key === tabName) ? 'block' : 'none';
  }

  for (const [key, btnEl] of Object.entries(btns)) {
    if (!btnEl) continue;
    if (key === tabName) {
      btnEl.style.color = 'var(--accent-orange)';
      btnEl.style.fontWeight = '700';
    } else {
      btnEl.style.color = 'var(--text-editorial)';
      btnEl.style.fontWeight = '500';
    }
  }

  updateCreditsDisplay();
};

// Sprint 5 / V7-07: Dual View Support (Desktop 7-Column Grid vs Day List)
window.setScheduleView = function(viewMode) {
  const dayContainer = document.getElementById('scheduleDayViewContainer');
  const gridContainer = document.getElementById('scheduleGridViewContainer');
  const btnDay = document.getElementById('viewToggleDay');
  const btnGrid = document.getElementById('viewToggleGrid');

  if (viewMode === 'grid') {
    if (dayContainer) dayContainer.style.display = 'none';
    if (gridContainer) gridContainer.style.display = 'block';
    if (btnDay) btnDay.classList.remove('active');
    if (btnGrid) btnGrid.classList.add('active');
    renderWeeklyGrid();
  } else {
    if (dayContainer) dayContainer.style.display = 'block';
    if (gridContainer) gridContainer.style.display = 'none';
    if (btnDay) btnDay.classList.add('active');
    if (btnGrid) btnGrid.classList.remove('active');
    renderScheduleDay(selectedScheduleDay);
  }
};

function renderWeeklyGrid() {
  const gridEl = document.getElementById('weeklyGridContent');
  if (!gridEl) return;
  gridEl.replaceChildren();

  const currentStore = (typeof window !== 'undefined') ? window.OpenBreakStore : null;
  const currentActive = currentStore ? currentStore.activeBookings : new Set();
  const daysInfo = [
    { name: 'LUN', num: '19' },
    { name: 'MAR', num: '20' },
    { name: 'MIÉ', num: '21' },
    { name: 'JUE', num: '22' },
    { name: 'VIE', num: '23' },
    { name: 'SÁB', num: '24' },
    { name: 'DOM', num: '25' }
  ];

  // Col 0: Sidebar hours
  const timeSidebar = document.createElement('div');
  timeSidebar.className = 'grid-time-sidebar';
  ['07:00', '09:00', '11:00', '18:00', '19:30'].forEach(t => {
    const el = document.createElement('div');
    el.textContent = t;
    timeSidebar.appendChild(el);
  });
  gridEl.appendChild(timeSidebar);

  // Cols 1 to 7: Days
  for (let i = 0; i < 7; i++) {
    const dayCol = document.createElement('div');
    dayCol.className = 'grid-day-column';

    const header = document.createElement('div');
    header.className = 'grid-header-col';
    header.innerHTML = `<div class="grid-day-label">${daysInfo[i].name}</div><div class="grid-num-label">${daysInfo[i].num}</div>`;
    dayCol.appendChild(header);

    const classes = boutiqueScheduleData[i] || [];
    classes.forEach(raw => {
      const c = currentStore ? (currentStore.getClass(raw.id) || raw) : raw;
      const reserved = currentActive.has(c.id);
      const full = c.spots === 0;

      const cell = document.createElement('div');
      cell.className = `grid-class-cell ${reserved ? 'is-reserved' : ''} ${full ? 'is-full' : ''}`;
      cell.innerHTML = `
        <div class="grid-class-time">${c.time.split(' - ')[0]}</div>
        <div class="grid-class-title">${c.title}</div>
        <div class="grid-class-spots" style="color: ${reserved ? 'var(--accent-green)' : full ? '#EF4444' : 'var(--accent-orange)'}">
          ${reserved ? '✓ Reservada' : full ? 'En espera' : `${c.spots} libres`}
        </div>
      `;
      cell.addEventListener('click', () => {
        bookFromDeskSchedule(c.id);
        renderWeeklyGrid();
      });
      dayCol.appendChild(cell);
    });

    gridEl.appendChild(dayCol);
  }
}
