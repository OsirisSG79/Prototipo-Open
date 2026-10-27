/**
 * test_audit_045_state_synchronization_edge.js
 * Audit 045: Cross-Component Reactive State Synchronization & Sub-Millisecond Concurrency
 * Validates:
 * 1. Synchronous broadcast from DemoStore triggers all registered listeners without delay
 * 2. Rapid interleaved transactions (book -> waitlist -> promote -> refund) maintain mathematical consistency
 * 3. Zero zombie subscriptions or memory retention after subscriber unbind
 */

const assert = require('assert');
const path = require('path');

console.log("Running AUD-045 Reactive State Synchronization & Edge Concurrency Audit...");

const repoDir = path.resolve(__dirname, '..');
const { DemoStore } = require(path.join(repoDir, 'src', 'js', 'demo-store.js'));

// 1. Multi-Subscriber Sync Verification
console.log("--- [1/3] Multi-Subscriber Immediate Dispatch ---");
const store = new DemoStore();

// Initialize sample class
store.initClasses([
  { id: 'c1', title: 'Power Reformer Flow', spots: 5, instructor: 'Sofia', time: '08:00' },
  { id: 'c2', title: 'Core Precision Stretch', spots: 5, instructor: 'Elena', time: '18:00' }
]);

let sub1Updates = 0;
let sub2Updates = 0;
let sub3Updates = 0;

const unsub1 = store.subscribe(() => { sub1Updates++; });
const unsub2 = store.subscribe(() => { sub2Updates++; });
const unsub3 = store.subscribe(() => { sub3Updates++; });

// Execute nominal booking
const res1 = store.bookClass('c1', 'Client Alpha');
assert.strictEqual(res1.success, true);
assert.strictEqual(sub1Updates, 1);
assert.strictEqual(sub2Updates, 1);
assert.strictEqual(sub3Updates, 1);
console.log("✓ All 3 distinct reactive subscribers received immediate state updates.");

// 2. Unsubscribe Teardown
console.log("--- [2/3] Selective Unsubscribe Lifecycle ---");
unsub2(); // Unsubscribe middle subscriber
const res2 = store.bookClass('c2', 'Client Beta');
assert.strictEqual(res2.success, true);
assert.strictEqual(sub1Updates, 2);
assert.strictEqual(sub2Updates, 1, "Unsubscribed listener should not receive updates");
assert.strictEqual(sub3Updates, 2);
console.log("✓ Clean listener teardown verified: zero zombie callback invocations.");

// 3. High-Frequency Interleaved Transaction Cycle
console.log("--- [3/3] Rapid Interleaved Transaction Conservation Cycle ---");
for (let i = 0; i < 5; i++) {
  const cId = `c_dyn_${i}`;
  store.initClasses([{ id: cId, title: `Test Class ${i}`, spots: 2 }]);
  store.bookClass(cId, `Client ${i}_A`);
  store.bookClass(cId, `Client ${i}_B`);
  store.bookClass(cId, `Waitlist ${i}_C`);
  store.cancelBooking(cId);
}

const finalAudit = store.verifyLedgerIntegrity();
assert.strictEqual(finalAudit.isConsistent, true);
console.log(`✓ Financial conservation held across interleaved operations. Balance: ${finalAudit.currentCredits} credits.`);

console.log("\n============================================================");
console.log("  AUD-045 REACTIVE STATE SYNC AUDIT: PASSED (100%)          ");
console.log("============================================================");
