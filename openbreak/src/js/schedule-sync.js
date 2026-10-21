/**
 * Open Break — Synchronized Boutique Schedule & Mobile App (R3 + R4)
 * Deterministic shared state between weekly desktop calendar and student smartphone.
 */

const boutiqueScheduleData = [
  // LUNES 20
  [
    { id: 'c1', title: 'Reformer Core Foundations', time: '07:30 - 08:20', coach: 'Camila Morales', spots: 2, total: 8, tag: 'Principiantes' },
    { id: 'c2', title: 'Athletic Reformer & Springs', time: '09:00 - 09:50', coach: 'Mateo Rivas', spots: 0, total: 8, tag: 'Waitlist Activa' },
    { id: 'c3', title: 'Reformer Sculpt Pro', time: '18:00 - 18:50', coach: 'Sofía Valdés', spots: 1, total: 8, tag: 'Último Cupo' },
    { id: 'c4', title: 'Classic Reformer Flow', time: '19:30 - 20:20', coach: 'Sofía Valdés', spots: 2, total: 8, tag: 'Nivel Mixto' }
  ],
  // MARTES 21
  [
    { id: 'c5', title: 'Jumpboard Cardio & Core', time: '08:00 - 08:50', coach: 'Mateo Rivas', spots: 3, total: 8, tag: 'Alta Intensidad' },
    { id: 'c6', title: 'Precision Alignment', time: '10:00 - 10:50', coach: 'Camila Morales', spots: 4, total: 8, tag: 'Técnica Clásica' },
    { id: 'c7', title: 'Evening Stretch & Flow', time: '18:30 - 19:20', coach: 'Sofía Valdés', spots: 2, total: 8, tag: 'Recuperación' }
  ],
  // MIÉRCOLES 22
  [
    { id: 'c8', title: 'Reformer Power Hour', time: '07:00 - 07:50', coach: 'Mateo Rivas', spots: 1, total: 8, tag: 'Intensivo' },
    { id: 'c9', title: 'Reformer Flow & Mat', time: '09:30 - 10:20', coach: 'Camila Morales', spots: 5, total: 8, tag: 'Abierto' },
    { id: 'c10', title: 'Athletic Jumps & Springs', time: '19:00 - 19:50', coach: 'Mateo Rivas', spots: 0, total: 8, tag: 'Waitlist' }
  ],
  // JUEVES 23
  [
    { id: 'c11', title: 'Full Body Sculpt', time: '08:30 - 09:20', coach: 'Sofía Valdés', spots: 2, total: 8, tag: 'Tonificación' },
    { id: 'c12', title: 'Core & Glutes Signature', time: '18:00 - 18:50', coach: 'Camila Morales', spots: 1, total: 8, tag: 'Cupo Limitado' }
  ],
  // VIERNES 24
  [
    { id: 'c13', title: 'Weekend Warmup Flow', time: '09:00 - 09:50', coach: 'Sofía Valdés', spots: 4, total: 8, tag: 'Energía' },
    { id: 'c14', title: 'Candlelight Restorative', time: '18:00 - 18:50', coach: 'Camila Morales', spots: 3, total: 8, tag: 'Relajación' }
  ],
  // SÁBADO 25
  [
    { id: 'c15', title: 'Saturday Masterclass', time: '09:30 - 10:45', coach: 'Sofía & Mateo', spots: 1, total: 8, tag: 'Especial 75min' },
    { id: 'c16', title: 'Post-Workout Mobility', time: '11:15 - 12:05', coach: 'Camila Morales', spots: 5, total: 8, tag: 'Flexibilidad' }
  ],
  // DOMINGO 26
  [
    { id: 'c17', title: 'Sunday Reset Flow', time: '10:00 - 10:50', coach: 'Sofía Valdés', spots: 6, total: 8, tag: 'Suave' }
  ]
];


// Local demonstration only. Does not represent the production transaction engine.
const classById=new Map(boutiqueScheduleData.flat().map(c=>[c.id,c]));
const activeBookings=new Set(['c3']); // Example existing booking shown in the phone at first load.
const waiting=new Set();
let selectedScheduleDay=0;
let userCredits=8;
let currentBookingId='c3';
function scheduleNotice(message){
  const node=document.getElementById('scheduleFeedback');
  if(node)node.textContent=message;
  // Expose last state transition for deterministic automated QA.
  window.openbreakLastScheduleMessage=message;
}
function updateCreditsDisplay(){
  for(const id of ['appCreditsBadge','creditsDisplay']){const el=document.getElementById(id);if(el)el.textContent=`${userCredits} CR`;}
}
function syncPhone(){
  const card=document.getElementById('appBookingCard'),title=document.getElementById('appBookingTitle');
  if(!currentBookingId||!activeBookings.has(currentBookingId))currentBookingId=[...activeBookings].at(-1)||null;
  if(card)card.style.display=currentBookingId?'block':'none';
  if(title)title.textContent=currentBookingId?classById.get(currentBookingId)?.title||'Clase reservada':'';
  const qr=document.getElementById('appQrOverlay');if(qr&&!currentBookingId)qr.style.display='none';
  updateCreditsDisplay();
}
function renderScheduleDay(dayIndex){
  selectedScheduleDay=dayIndex;
  for(let i=0;i<7;i++){
    const btn=document.getElementById(`cal-day-${i}`);if(!btn)continue;
    const selected=i===dayIndex;btn.classList.toggle('active',selected);
    btn.setAttribute('aria-selected',String(selected));btn.style.border=selected?'1.5px solid var(--accent-orange)':'1px solid var(--border-subtle)';
    btn.style.background=selected?'#FFF5EE':'var(--bg-gray-subtle)';
  }
  const list=document.getElementById('calendarClassesList');if(!list)return;
  list.replaceChildren();
  for(const c of boutiqueScheduleData[dayIndex]||[]){
    const reserved=activeBookings.has(c.id),queued=waiting.has(c.id),full=c.spots===0;
    const card=document.createElement('article');card.className='ob-schedule-class';
    const info=document.createElement('div');
    const when=document.createElement('div');when.className='ob-schedule-meta';when.textContent=`${c.time} · ${c.spots} de ${c.total} cupos libres`;
    const heading=document.createElement('h4');heading.textContent=c.title;
    const coach=document.createElement('p');coach.textContent=`Coach ${c.coach} · Sala Reformer`;
    info.append(when,heading,coach);
    const button=document.createElement('button');button.type='button';button.className='ob-schedule-book';
    button.textContent=reserved?'Reservada':queued?'En espera':full?'Unirse a espera':'Reservar';
    button.disabled=reserved||queued;
    button.addEventListener('click',()=>bookFromDeskSchedule(c.id));
    card.append(info,button);list.append(card);
  }
}
function switchScheduleDay(index){renderScheduleDay(index);}
function bookFromDeskSchedule(classId){
  const c=classById.get(classId);
  if(!c){scheduleNotice('Clase no encontrada.');return false;}
  if(activeBookings.has(classId)){scheduleNotice('Esa clase ya está reservada. No se descontó otro crédito.');return false;}
  if(waiting.has(classId)){scheduleNotice('Ya estás en espera de esa clase.');return false;}
  if(c.spots<=0){waiting.add(classId);scheduleNotice(`Te agregamos a la lista de espera de ${c.title}. Sin descontar créditos.`);renderScheduleDay(selectedScheduleDay);return 'waitlist';}
  if(userCredits<=0){scheduleNotice('No tienes créditos disponibles para esta demostración.');return false;}
  c.spots--;userCredits--;activeBookings.add(classId);currentBookingId=classId;
  scheduleNotice(`Reserva de demostración confirmada: ${c.title}. Un crédito utilizado.`);
  syncPhone();renderScheduleDay(selectedScheduleDay);return true;
}
function appCancelBooking(){
  const id=currentBookingId;
  if(!id||!activeBookings.has(id)){scheduleNotice('No hay una reserva activa para cancelar.');return false;}
  activeBookings.delete(id);classById.get(id).spots++;userCredits++;
  currentBookingId=[...activeBookings].at(-1)||null;
  scheduleNotice('Reserva cancelada. Una plaza y un crédito fueron devueltos una sola vez.');
  syncPhone();renderScheduleDay(selectedScheduleDay);return true;
}
function appBookFastClass(title,time){
  const c=[...classById.values()].find(c=>c.title===title&&c.time.startsWith(time));
  if(!c){scheduleNotice('Clase de demostración no disponible.');return false;}
  return bookFromDeskSchedule(c.id);
}
function appTriggerCheckIn(){
  if(!currentBookingId){scheduleNotice('Reserva una clase primero para ver tu pase de prueba.');return;}
  const box=document.getElementById('appQrOverlay');if(box)box.style.display=box.style.display==='none'?'block':'none';
}
window.addEventListener('DOMContentLoaded',()=>{renderScheduleDay(0);syncPhone();});
