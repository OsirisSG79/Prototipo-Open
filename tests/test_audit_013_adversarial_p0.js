// tests/test_audit_013_adversarial_p0.js
const assert = require('assert');
const { DemoStore } = require('../src/js/demo-store.js');

console.log('Testing AUD-013 P0 Adversarial Scenarios...');

// 1. P0-01 Reproduction & Fix: cancelBooking('c1') without studentName when multiple bookings exist
console.log('--- Test P0-01 (AUD-013): Ambiguous cancelBooking by classId with multiple active bookings ---');
const store1 = new DemoStore(3);
store1.initClasses([{ id: 'c1', title: 'Power Flow', spots: 2, total: 2 }]);

const bAna = store1.bookClass('c1', 'Ana Valenzuela');
const bBeto = store1.bookClass('c1', 'Beto Ramos');
assert.strictEqual(bAna.success, true);
assert.strictEqual(bBeto.success, true);
assert.strictEqual(store1.credits, 1);
assert.strictEqual(store1.getClass('c1').spots, 0);

// In V8.1.3, cancelBooking('c1') would silently cancel Beto (last booking).
// In V8.1.4, cancelBooking('c1') must be rejected as 'ambiguous_booking' to protect all active bookings!
const ambiguousCancel = store1.cancelBooking('c1');
assert.strictEqual(ambiguousCancel.success, false, 'Ambiguous cancel without studentName must fail');
assert.strictEqual(ambiguousCancel.reason, 'ambiguous_booking');
assert.strictEqual(store1.credits, 1, 'Credits must not be modified');
assert.strictEqual(store1.getBookingsForClass('c1').length, 2, 'Both bookings must remain active');
assert.strictEqual(store1.getClass('c1').spots, 0, 'Class spots must remain 0');

// But cancelling with explicit bookingId or studentName succeeds:
const explicitCancelBeto = store1.cancelBooking(bBeto.bookingId);
assert.strictEqual(explicitCancelBeto.success, true, 'Explicit bookingId cancel must succeed');
assert.strictEqual(store1.credits, 2);
assert.strictEqual(store1.getBookingsForClass('c1').length, 1);
assert.strictEqual(store1.getClass('c1').spots, 1);
console.log('✓ P0-01 (AUD-013) resolved: ambiguous class cancel rejected without touching other bookings.');

// 2. P0-02 Reproduction & Fix: ledgerRefundSpot() without bookingId when multiple bookings exist
console.log('--- Test P0-02 (AUD-013): Ambiguous ledgerRefundSpot without ID with multiple active bookings ---');
const store2 = new DemoStore(8);
store2.initClasses([
  { id: 'c1', title: 'Clase 1', spots: 1, total: 1 },
  { id: 'c2', title: 'Clase 2', spots: 1, total: 1 }
]);

const b1 = store2.bookClass('c1', 'Ana Valenzuela');
const b2 = store2.bookClass('c2', 'Beto Ramos');
assert.strictEqual(store2.credits, 6);

// Invoking refund without ID when multiple bookings exist:
// Must NOT arbitrarily refund Ana or Beto!
const ambiguousRefund = store2.ledgerRefundSpot();
assert.strictEqual(ambiguousRefund.success, false, 'Ambiguous refund without bookingId must fail');
assert.strictEqual(ambiguousRefund.reason, 'ambiguous_refund_target');
assert.strictEqual(store2.credits, 6, 'Credits must not change on ambiguous refund');
assert.strictEqual(store2.getBookingsForClass('c1').length, 1);
assert.strictEqual(store2.getBookingsForClass('c2').length, 1);

// Refunding with explicit bookingId succeeds:
const explicitRefundAna = store2.ledgerRefundSpot(b1.bookingId);
assert.strictEqual(explicitRefundAna.success, true);
assert.strictEqual(store2.credits, 7);
assert.strictEqual(store2.getBookingsForClass('c1').length, 0);
assert.strictEqual(store2.getClass('c1').spots, 1);
console.log('✓ P0-02 (AUD-013) resolved: ambiguous ledger refund rejected without targeting wrong student.');

// 3. Repeat and Reverse Re-cancellation/Refund Invariance
console.log('--- Test Invariance: Repeated cancel and double refund attempt ---');
const repeatCancel = store2.cancelBooking(b1.bookingId);
assert.strictEqual(repeatCancel.success, false);
assert.strictEqual(repeatCancel.reason, 'not_booked');
assert.strictEqual(store2.credits, 7);

const repeatRefund = store2.ledgerRefundSpot(b1.bookingId);
assert.strictEqual(repeatRefund.success, false);
assert.strictEqual(store2.credits, 7);

console.log('ALL AUD-013 P0 ADVERSARIAL TESTS PASSED (100%)!');
