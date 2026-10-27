// tests/test_audit_012_adversarial_p0.js
const assert = require('assert');
const { DemoStore } = require('../src/js/demo-store.js');

console.log('Testing AUD-012 P0 Adversarial Scenarios...');

// 1. P0-01 Reproduction & Fix Test
console.log('--- Test P0-01: Cancel with nonexistent studentName must fail without canceling other students ---');
const store1 = new DemoStore(8);
store1.initClasses([{ id: 'c1', title: 'Clase Reformer', spots: 2, total: 2 }]);

const resAna = store1.bookClass('c1', 'Ana Valenzuela');
const resBeto = store1.bookClass('c1', 'Beto Ramos');
assert.strictEqual(resAna.success, true);
assert.strictEqual(resBeto.success, true);
assert.strictEqual(store1.credits, 6);
assert.strictEqual(store1.getClass('c1').spots, 0);

// Attempt canceling with intruder/nonexistent student
const cancelIntruder = store1.cancelBooking('c1', 'Intruso');
assert.strictEqual(cancelIntruder.success, false, 'Cancel should fail for nonexistent student');
assert.strictEqual(cancelIntruder.reason, 'booking_not_found_for_student');

// Verify neither Ana nor Beto were cancelled!
assert.strictEqual(store1.credits, 6, 'Credits must not change on failed cancel');
assert.strictEqual(store1.getBookingsForClass('c1').length, 2, 'Class must retain 2 bookings');
assert.strictEqual(store1.getClass('c1').spots, 0, 'Class spots must remain 0');

// Now cancel Beto explicitly
const cancelBeto = store1.cancelBooking('c1', 'Beto Ramos');
assert.strictEqual(cancelBeto.success, true);
assert.strictEqual(store1.credits, 7);
assert.strictEqual(store1.getBookingsForClass('c1').length, 1);
assert.strictEqual(store1.getClass('c1').spots, 1);
console.log('✓ P0-01 resolved: intruder cannot cancel other students\' bookings.');

// 2. P0-02 Reproduction & Fix Test
console.log('--- Test P0-02: Ledger refund with invalid/nonexistent bookingId must fail ---');
const store2 = new DemoStore(8);
store2.initClasses([{ id: 'c1', title: 'Clase Reformer', spots: 2, total: 2 }]);
const bAna = store2.bookClass('c1', 'Ana Valenzuela');
assert.strictEqual(store2.credits, 7);

const badRefund = store2.ledgerRefundSpot('bk_does_not_exist_999');
assert.strictEqual(badRefund.success, false, 'Refund with invalid bookingId must fail');
assert.strictEqual(badRefund.reason, 'booking_not_found');
assert.strictEqual(store2.credits, 7, 'Credits must remain 7 after invalid refund');
assert.strictEqual(store2.getClass('c1').spots, 1, 'Inventory must remain unchanged');
console.log('✓ P0-02 resolved: invalid bookingId rejected without refunding other bookings.');

// 3. P0-03 Reproduction & Fix Test
console.log('--- Test P0-03: Ledger refund must cancel reservation and release inventory or promote waitlist ---');
const store3 = new DemoStore(8);
store3.initClasses([{ id: 'c1', title: 'Clase Reformer', spots: 1, total: 1 }]);
const b1 = store3.bookClass('c1', 'Ana Valenzuela');
assert.strictEqual(store3.getClass('c1').spots, 0);
assert.strictEqual(store3.credits, 7);

// Valid refund for Ana's booking
const refundAna = store3.ledgerRefundSpot(b1.bookingId);
assert.strictEqual(refundAna.success, true);
assert.strictEqual(store3.credits, 8);
// Inventory MUST be released back to 1!
assert.strictEqual(store3.getClass('c1').spots, 1, 'Spot must be released back to 1 on refund');
assert.strictEqual(store3.getBookingsForClass('c1').length, 0, 'Class must have 0 bookings after refund');

// Second refund attempt must fail (not refundable)
const refundAnaAgain = store3.ledgerRefundSpot(b1.bookingId);
assert.strictEqual(refundAnaAgain.success, false);
console.log('✓ P0-03 resolved: refund correctly cancels booking and releases inventory.');

console.log('ALL AUD-012 P0 ADVERSARIAL TESTS PASSED (100%)!');
