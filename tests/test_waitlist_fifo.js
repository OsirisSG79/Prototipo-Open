/**
 * Test Suite: V7-06 Waitlist FIFO Queue Ordering & Auto-Promotion
 * Verifies that when a class is full:
 * 1. Multiple users can join a FIFO queue in deterministic order.
 * 2. When a spot is cancelled, the head of the waitlist is promoted and notified.
 * 3. Credits remain intact (never debited while waiting).
 */
const { DemoStore } = require('../src/js/demo-store.js');

console.log('Running V7-06 Waitlist FIFO queue test...');

const store = new DemoStore();
store.initClasses([
  { id: 'c_full', title: 'Full Masterclass', spots: 0, total: 8 }
]);

const initialCredits = store.credits;

// Join waitlist student 1
const r1 = store.bookClass('c_full');
if (!r1.waitlist || r1.position !== 1) throw new Error('Student 1 should be #1 in queue');
if (store.credits !== initialCredits) throw new Error('Waitlist must not debit credits');

// Simulate adding student 2 to queue directly in waitlist
const q = store.waitlists.get('c_full');
q.push('Lucía Méndez');
store.waitlists.set('c_full', q);

if (store.waitlists.get('c_full').length !== 2) throw new Error('Queue length must be 2');

// Now simulate an active booking on that class and cancel it
store.activeBookings.set('c_full', { bookingId: 'bk_occ', txId: 'tx_occ', classId: 'c_full', refundable: true });
let promotedStudent = null;
store.subscribe((state, action, payload) => {
  if (action === 'WAITLIST_PROMOTED') {
    promotedStudent = payload.student;
  }
});

const cancelRes = store.cancelBooking('c_full');
if (!cancelRes.success) throw new Error('Cancellation should succeed');

// Verifications
if (promotedStudent !== 'Camila Morales') {
  throw new Error(`Expected 'Camila Morales' to be promoted first (FIFO), got ${promotedStudent}`);
}

const remainingQueue = store.waitlists.get('c_full');
if (remainingQueue.length !== 1 || remainingQueue[0] !== 'Lucía Méndez') {
  throw new Error('Lucía Méndez should now be #1 in the queue');
}

console.log('PASS: V7-06 Waitlist FIFO queue order and automatic promotion verified!');
