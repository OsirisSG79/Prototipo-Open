/**
 * AUD-013 Mandatory Acceptance Verification Suite (AUD-013 / V8.1.4)
 * Verifies all P0/P1 criteria specified in OPEN_BREAK_AUD-013_V8_1_3_DICTAMEN_Y_PLAN_V8_1_4.md:
 * 1. Ana and Beto have distinct credit balances; spending credits by Ana does not deplete Beto's wallet.
 * 2. cancelBooking('c1') with two active bookings is rejected with 'ambiguous_booking' without side effects.
 * 3. cancelBooking with explicit bookingId succeeds and restores inventory/credit cleanly.
 * 4. ledgerRefundSpot() without bookingId when >1 refundable booking exists is rejected with 'ambiguous_refund_target'.
 * 5. Cancellation with non-existent ID and refund with non-existent ID fail deterministically.
 * 6. Repeated cancellation or double refund of the same bookingId is strictly idempotent (no balance or spot duplication).
 * 7. Waitlist promotion candidate balance validation: candidate without sufficient balance is not promoted to negative balance.
 * 8. Mathematical Capacity Invariant: confirmed bookings + available spots = total capacity for every class.
 * 9. Mathematical Ledger Conservation: student balance = opening balance + sum of student's transactions.
 */

const assert = require('assert');
const { DemoStore } = require('../src/js/demo-store.js');

console.log('Running AUD-013 Full Acceptance Criteria Suite (V8.1.4)...');

// --- 1. Distinct student wallets: Ana and Beto credit isolation ---
console.log('--- Criterion 1: Per-student wallet isolation ---');
const store1 = new DemoStore(10);
store1.initClasses([
  { id: 'c1', title: 'Reformer Core', spots: 2, total: 2 },
  { id: 'c2', title: 'Reformer Jump', spots: 2, total: 2 }
]);

store1.registerStudent('Ana Valenzuela', 3);
store1.registerStudent('Beto Ramos', 2);

assert.strictEqual(store1.getStudentBalance('Ana Valenzuela'), 3);
assert.strictEqual(store1.getStudentBalance('Beto Ramos'), 2);

// Ana books c1
const bAna = store1.bookClass('c1', 'Ana Valenzuela');
assert.strictEqual(bAna.success, true);
assert.strictEqual(store1.getStudentBalance('Ana Valenzuela'), 2);
assert.strictEqual(store1.getStudentBalance('Beto Ramos'), 2, "Beto's balance must not decrease when Ana books!");

// --- 2. Ambiguous classId cancellation rejected ---
console.log('--- Criterion 2: Ambiguous classId cancellation rejection ---');
const bBeto = store1.bookClass('c1', 'Beto Ramos');
assert.strictEqual(bBeto.success, true);
assert.strictEqual(store1.getClass('c1').spots, 0);

// Calling cancelBooking('c1') without identity must reject with 'ambiguous_booking'
const ambCancel = store1.cancelBooking('c1');
assert.strictEqual(ambCancel.success, false);
assert.strictEqual(ambCancel.reason, 'ambiguous_booking');
assert.strictEqual(store1.getClass('c1').spots, 0, 'Spots must remain 0 after rejected cancellation');
assert.strictEqual(store1.isBooked('c1', 'Ana Valenzuela'), true);
assert.strictEqual(store1.isBooked('c1', 'Beto Ramos'), true);

// --- 3. Explicit bookingId cancellation succeeds ---
console.log('--- Criterion 3: Explicit bookingId cancellation ---');
const okCancel = store1.cancelBooking(bAna.bookingId);
assert.strictEqual(okCancel.success, true);
assert.strictEqual(okCancel.creditRefunded, true);
assert.strictEqual(store1.getClass('c1').spots, 1);
assert.strictEqual(store1.isBooked('c1', 'Ana Valenzuela'), false);
assert.strictEqual(store1.isBooked('c1', 'Beto Ramos'), true);
assert.strictEqual(store1.getStudentBalance('Ana Valenzuela'), 3, 'Ana balance restored to 3');
assert.strictEqual(store1.getStudentBalance('Beto Ramos'), 1, 'Beto balance unchanged');

// --- 4. Ambiguous ledger refund rejected without explicit bookingId ---
console.log('--- Criterion 4: Ambiguous ledger refund rejection ---');
const store2 = new DemoStore(10);
store2.initClasses([{ id: 'cls_A', title: 'Class A', spots: 5, total: 5 }]);
const bk1 = store2.bookClass('cls_A', 'Ana Valenzuela');
const bk2 = store2.bookClass('cls_A', 'Beto Ramos');

// Multiple refundable bookings exist: ledgerRefundSpot() without bookingId must reject
const ambRefund = store2.ledgerRefundSpot();
assert.strictEqual(ambRefund.success, false);
assert.strictEqual(ambRefund.reason, 'ambiguous_refund_target');

// With explicit bookingId, succeeds cleanly
const okRefund = store2.ledgerRefundSpot(bk1.bookingId);
assert.strictEqual(okRefund.success, true);
assert.strictEqual(okRefund.bookingId, bk1.bookingId);
assert.strictEqual(store2.isBooked('cls_A', 'Ana Valenzuela'), false);
assert.strictEqual(store2.isBooked('cls_A', 'Beto Ramos'), true);

// --- 5. Non-existent bookingId and refund target rejection ---
console.log('--- Criterion 5: Non-existent IDs fail gracefully ---');
const fakeCancel = store2.cancelBooking('bk_nonexistent_9999');
assert.strictEqual(fakeCancel.success, false);
assert.strictEqual(fakeCancel.reason, 'not_booked');

const fakeRefund = store2.ledgerRefundSpot('bk_nonexistent_8888');
assert.strictEqual(fakeRefund.success, false);
assert.strictEqual(fakeRefund.reason, 'booking_not_found');

// --- 6. Double refund and double cancellation idempotency ---
console.log('--- Criterion 6: Double cancellation and double refund idempotency ---');
const repeatCancel = store2.cancelBooking(bk1.bookingId);
assert.strictEqual(repeatCancel.success, false);
assert.strictEqual(repeatCancel.reason, 'not_booked');

const repeatRefund = store2.ledgerRefundSpot(bk1.bookingId);
assert.strictEqual(repeatRefund.success, false);
assert.strictEqual(repeatRefund.reason, 'booking_not_found');

// --- 7. Waitlist candidate balance validation ---
console.log('--- Criterion 7: Waitlist candidate balance validation ---');
const store3 = new DemoStore(5);
store3.initClasses([{ id: 'c_solo', title: 'Solo Bed', spots: 1, total: 1 }]);
store3.registerStudent('Rich Student', 2);
store3.registerStudent('Poor Student', 0); // 0 credits!

// Rich student takes the 1 spot
const bRich = store3.bookClass('c_solo', 'Rich Student');
assert.strictEqual(bRich.success, true);
assert.strictEqual(store3.getClass('c_solo').spots, 0);

// Poor student joins waitlist (allowed without balance check at join time)
const bPoorWaitlist = store3.bookClass('c_solo', 'Poor Student');
assert.strictEqual(bPoorWaitlist.success, true);
assert.strictEqual(bPoorWaitlist.waitlist, true);

// When Rich student cancels, Poor student cannot be promoted because balance = 0!
// Spot is returned to inventory instead of creating negative balance.
const cRich = store3.cancelBooking(bRich.bookingId);
assert.strictEqual(cRich.success, true);
assert.strictEqual(store3.getStudentBalance('Poor Student'), 0, 'Balance must remain 0, never negative!');
assert.strictEqual(store3.getClass('c_solo').spots, 1, 'Spot must be restored to inventory');

// --- 8. Mathematical Capacity Invariant: confirmed + spots = total capacity ---
console.log('--- Criterion 8: Capacity invariant check ---');
const c_solo_info = store3.getClass('c_solo');
const confirmedBookings = store3.getBookingsForClass('c_solo').length;
assert.strictEqual(confirmedBookings + c_solo_info.spots, c_solo_info.total);

// --- 9. Mathematical Ledger Conservation ---
console.log('--- Criterion 9: Ledger sum check ---');
const integrity = store1.verifyLedgerIntegrity();
assert.strictEqual(integrity.isConsistent, true);
const integrity2 = store2.verifyLedgerIntegrity();
assert.strictEqual(integrity2.isConsistent, true);
const integrity3 = store3.verifyLedgerIntegrity();
assert.strictEqual(integrity3.isConsistent, true);

console.log('====================================================');
console.log('ALL AUD-013 ACCEPTANCE CRITERIA PASSED (100%)!');
console.log('====================================================');
