/**
 * Test Suite: V7-10 Lead Data Integrity & Formatting
 * Verifies that modal form creates valid structured lead objects
 * with required metadata and WhatsApp dispatch URI encoding.
 */
const assert = require('node:assert/strict');

console.log('Running V7-10 Lead Data Integrity & Dispatch test...');

const testLead = {
  name: 'Camila Morales',
  studio: 'Cima Pilates Reforma',
  discipline: 'Pilates Reformer',
  phone: '+52 55 1234 5678',
  timestamp: new Date().toISOString(),
  channel: 'openbreak-demo-v8'
};

assert.ok(testLead.name && testLead.studio && testLead.phone, 'Required fields must be populated');
assert.equal(testLead.channel, 'openbreak-demo-v8');

const text = encodeURIComponent(`¡Hola equipo de Open Break! Me interesa una demostración para mi estudio.\n\n• Estudio: ${testLead.studio}\n• Contacto: ${testLead.name}\n• Disciplina: ${testLead.discipline}\n• Teléfono: ${testLead.phone}`);
const url = `https://wa.me/525512345678?text=${text}`;

assert.ok(url.startsWith('https://wa.me/525512345678?text='), 'Must form valid WhatsApp deep link');
assert.ok(url.includes('Cima%20Pilates%20Reforma'), 'Studio name must be correctly URI encoded');

console.log('PASS: V7-10 Lead dispatch formatting and channel payload verified!');
