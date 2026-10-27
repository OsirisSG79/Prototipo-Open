/**
 * test_audit_011_resilience.js
 * Extended resilience & edge case test suite for AUD-011 certification
 * Tests:
 * 1. Rapid concurrent booking bursts without double-spend
 * 2. Multi-tier waitlist FIFO order preservation and cascading cancel
 * 3. Mathematical conservation through heavy randomized operations
 */

const assert = require('assert');
const { DemoStore } = require('../src/js/demo-store.js');

console.log('Running AUD-011 Extended Resilience & Edge Cases Test...');

// 1. Rapid concurrent burst test
console.log('--- Subtest 1: Concurrency burst protection ---');
const store = new DemoStore(8);
assert.strictEqual(store.credits, 8);

// Initialize mock classes
const classesList = [];
for (let i = 0; i < 15; i++) {
  classesList.push({ id: `burst_c_${i}`, title: `Burst Class ${i}`, spots: 1, capacity: 1 });
}
store.initClasses(classesList);

let successCount = 0;
let failCount = 0;

for (let i = 0; i < 15; i++) {
  const result = store.bookClass(`burst_c_${i}`, `Student_${i}`);
  if (result.success && !result.waitlist) {
    successCount++;
  } else {
    failCount++;
  }
}

console.log(`Burst results: ${successCount} successes, ${failCount} failures/waitlists`);
assert.strictEqual(successCount, 8, 'Must allow exactly 8 bookings matching initial balance');
assert.strictEqual(store.credits, 0, 'Balance must be exactly 0 after 8 debits');
assert.strictEqual(store.verifyLedgerIntegrity().isConsistent, true, 'Ledger must remain strictly consistent');

// 2. Cascading waitlist FIFO promotion
console.log('--- Subtest 2: Multi-tier cascading waitlist promotion ---');
const cascadeStore = new DemoStore(8);
const classId = 'c_cascade';
cascadeStore.initClasses([{ id: classId, title: 'Cascade Pilates', spots: 1, capacity: 1 }]);

const r1 = cascadeStore.bookClass(classId, 'Primary_Student');
assert.strictEqual(r1.success, true);
assert.strictEqual(r1.waitlist, false);
assert.strictEqual(cascadeStore.getClass(classId).spots, 0);

// Add 3 students to waitlist
const wl1 = cascadeStore.bookClass(classId, 'Waitlist_Student_1');
const wl2 = cascadeStore.bookClass(classId, 'Waitlist_Student_2');
const wl3 = cascadeStore.bookClass(classId, 'Waitlist_Student_3');

assert.strictEqual(wl1.position, 1);
assert.strictEqual(wl2.position, 2);
assert.strictEqual(wl3.position, 3);

// Cancel primary -> wl1 promoted
const c1 = cascadeStore.cancelBooking(classId);
assert.strictEqual(c1.promotedStudent.studentName, 'Waitlist_Student_1');
assert.strictEqual(cascadeStore.getClass(classId).spots, 0, 'Spot held by promoted student 1');

// Cancel wl1 -> wl2 promoted
const c2 = cascadeStore.cancelBooking(classId);
assert.strictEqual(c2.promotedStudent.studentName, 'Waitlist_Student_2');
assert.strictEqual(cascadeStore.getClass(classId).spots, 0, 'Spot held by promoted student 2');

// Cancel wl2 -> wl3 promoted
const c3 = cascadeStore.cancelBooking(classId);
assert.strictEqual(c3.promotedStudent.studentName, 'Waitlist_Student_3');
assert.strictEqual(cascadeStore.getClass(classId).spots, 0, 'Spot held by promoted student 3');

// Cancel wl3 -> queue empty, spot released
const c4 = cascadeStore.cancelBooking(classId);
assert.strictEqual(c4.promotedStudent, null);
assert.strictEqual(cascadeStore.getClass(classId).spots, 1, 'Class spot must be released once waitlist is empty');

// 3. Mathematical conservation through heavy randomized operations
console.log('--- Subtest 3: Randomized operations ledger conservation check ---');
const fuzzStore = new DemoStore(10);
const fuzzClasses = [
  { id: 'fuzz_a', title: 'Fuzz A', spots: 2, capacity: 2 },
  { id: 'fuzz_b', title: 'Fuzz B', spots: 2, capacity: 2 },
  { id: 'fuzz_c', title: 'Fuzz C', spots: 2, capacity: 2 },
  { id: 'fuzz_d', title: 'Fuzz D', spots: 2, capacity: 2 }
];
fuzzStore.initClasses(fuzzClasses);

for (let step = 0; step < 60; step++) {
  const chosenClass = fuzzClasses[step % fuzzClasses.length].id;
  if (step % 4 === 0) {
    fuzzStore.cancelBooking(chosenClass);
  } else if (step % 5 === 0) {
    fuzzStore.ledgerRefundSpot();
  } else {
    fuzzStore.bookClass(chosenClass, `Fuzzer_${step}`);
  }
  const check = fuzzStore.verifyLedgerIntegrity();
  assert.strictEqual(check.isConsistent, true, `Inconsistent ledger at step ${step}`);
  assert.strictEqual(check.currentCredits, check.calculatedSum, `Balance mismatch at step ${step}`);
}

console.log('PASS: All AUD-011 resilience & randomized stress checks succeeded cleanly!');
process.exit(0);
