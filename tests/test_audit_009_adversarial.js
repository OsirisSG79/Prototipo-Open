const { DemoStore } = require('../src/js/demo-store.js');

console.log('Testing AUD-009 double-refund bug protection...');

const store = new DemoStore();
// Empty initial pre-existing active bookings and historicals to isolate c1
store.activeBookings.clear();
store.historicalRefundableReservations = [];

store.initClasses([
  { id: 'c1', title: 'Reformer Core Foundations', spots: 2, total: 8 },
  { id: 'c2', title: 'Full Masterclass', spots: 0, total: 8 },
  { id: 'c3', title: 'Reformer Sculpt Pro', spots: 1, total: 8 }
]);

console.log('Initial credits:', store.credits); // 8

// 1. User books c1
const r1 = store.bookClass('c1');
console.log('After booking c1:', store.credits); // 7
if (store.credits !== 7) throw new Error('Credits should be 7');

// 2. User refunds via ledger
const r2 = store.ledgerRefundSpot();
console.log('After ledger refund:', store.credits); // 8
if (store.credits !== 8) throw new Error('Credits should be 8');

// 3. User attempts to cancel booking c1 via app/agenda
const r3 = store.cancelBooking('c1');
console.log('After app cancelBooking c1 attempt:', r3);

if (store.credits > 8) {
  throw new Error('FAILED: Double refund bug still occurred! Credits = ' + store.credits);
}

// AUD-012 P0-03 Fix: Refunding via ledger already cancelled the booking and freed the spot,
// so subsequent cancelBooking attempt correctly yields { success: false, reason: 'not_booked' }
// or creditRefunded: false without double refund.
if (store.credits === 8 && (r3.creditRefunded === false || r3.success === false)) {
  console.log('PASS: Double refund successfully prevented! Booking was cancelled without re-crediting.');
}

// 4. Test Second Scenario: Booking c1, Cancelling via app first, then attempting Ledger refund
console.log('\nTesting reverse order: App cancel first, then ledger refund attempt...');
const store2 = new DemoStore();
store2.activeBookings.clear();
store2.historicalRefundableReservations = [];
store2.initClasses([{ id: 'c1', title: 'Reformer Core', spots: 2, total: 8 }]);

store2.bookClass('c1'); // 7
store2.cancelBooking('c1'); // 8
const rLedgerSecond = store2.ledgerRefundSpot(); // Should fail: no refundable bookings left!
console.log('Ledger refund success:', rLedgerSecond.success, 'credits:', store2.credits);

if (store2.credits !== 8 || rLedgerSecond.success !== false) {
  throw new Error('FAILED: Reverse double refund occurred! Credits = ' + store2.credits);
}
console.log('PASS: Reverse double refund prevented cleanly!');

// 5. Test Waitlist Spot Allocation Invariant (AUD-009 Semantic Invariant)
console.log('\nTesting AUD-009 Waitlist Spot Consistency on Cancel...');
const store3 = new DemoStore();
store3.initClasses([{ id: 'c_full', title: 'Sold Out Class', spots: 0, total: 8 }]);

// Join waitlist student
const rW = store3.bookClass('c_full');
console.log('Waitlist join:', rW);
if (!rW.waitlist) throw new Error('Should join waitlist');

// Simulate an active occupant on that class
store3.activeBookings.set('c_full', { bookingId: 'bk_occupant', txId: 'tx_occ', classId: 'c_full', refundable: true });

// Occupant cancels booking
const rCancel = store3.cancelBooking('c_full');
console.log('Cancellation result:', rCancel);
const c_full_state = store3.getClass('c_full');

console.log('Class spots after cancellation with waitlist:', c_full_state.spots);
if (c_full_state.spots !== 0) {
  throw new Error(`FAILED: spots should remain 0 because spot was immediately allocated to promoted student (${rCancel.promotedStudent.studentName}), but got spots=${c_full_state.spots}`);
}

console.log('PASS: Waitlist semantic invariant verified! Spot remained claimed by promoted student, spots=0.');
console.log('\nALL AUD-009 ADVERSARIAL TESTS PASSED (100% RESOLUTION)!');
