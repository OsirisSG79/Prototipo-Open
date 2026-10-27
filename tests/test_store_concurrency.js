/**
 * Test Suite: V7-01 Resolution & Store Invariant Reproduction
 * Verifies exact reproduction from audit:
 * Ledger book -> Agenda book -> Ledger refund -> Agenda book
 * Verifies that state never gets out of sync and total credits remain perfectly deterministic.
 */
const { DemoStore } = require('../src/js/demo-store.js');

const boutiqueClasses = [
  { id: 'c1', title: 'Reformer Core Foundations', spots: 2, total: 8 },
  { id: 'c2', title: 'Athletic Reformer & Springs', spots: 0, total: 8 },
  { id: 'c3', title: 'Reformer Sculpt Pro', spots: 1, total: 8 },
  { id: 'c5', title: 'Jumpboard Cardio & Core', spots: 3, total: 8 },
  { id: 'c6', title: 'Precision Alignment', spots: 4, total: 8 }
];

console.log('Running V7-01 reproduction and fix test...');

const store = new DemoStore();
store.initClasses(boutiqueClasses);

// Initial State: 8 credits
if (store.credits !== 8) throw new Error('Initial credits must be 8');

// Step 1: Ledger: reservar 1
const bDesk = store.ledgerBookSpot('Reserva 1');
console.log('Step 1 (Ledger book): credits =', store.credits);
if (store.credits !== 7) throw new Error(`Expected 7, got ${store.credits}`);

// Step 2: Agenda: reservar c5
const r2 = store.bookClass('c5');
if (!r2.success) throw new Error('Booking c5 should succeed');
console.log('Step 2 (Agenda book c5): credits =', store.credits);
if (store.credits !== 6) throw new Error(`Expected 6 credits after 2 bookings! Got ${store.credits}`);

// Step 3: Ledger: reembolso (P0-02 AUD-013: pass explicit target bookingId)
const r3 = store.ledgerRefundSpot(bDesk.bookingId);
if (!r3.success) throw new Error('Ledger refund should succeed');
console.log('Step 3 (Ledger refund): credits =', store.credits);
if (store.credits !== 7) throw new Error(`Expected 7 credits after refund, got ${store.credits}`);

// Step 4: Agenda: reservar c6
const r4 = store.bookClass('c6');
if (!r4.success) throw new Error('Booking c6 should succeed');
console.log('Step 4 (Agenda book c6): credits =', store.credits);
if (store.credits !== 6) throw new Error(`Expected 6 credits, got ${store.credits}`);

// Test Waitlist FIFO & Credit Invariant
const rWaitlist = store.bookClass('c2'); // c2 has 0 spots
if (!rWaitlist.waitlist || rWaitlist.position !== 1) throw new Error('Waitlist join failed');
if (store.credits !== 6) throw new Error('Waitlist must NEVER deduct credits!');

// Duplicate booking prevention
const rDuplicate = store.bookClass('c6');
if (rDuplicate.success) throw new Error('Duplicate booking must be rejected!');
if (store.credits !== 6) throw new Error('Duplicate booking must not alter credits');

console.log('PASS: DemoStore completely eliminates V7-01 credit inconsistency! All invariants verified.');
