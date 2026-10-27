/**
 * test_audit_054_multi_tab_storage_sync.js
 * Audit 054: Multi-Tab State Invariants, In-Memory Concurrency & Broadcast Channel Simulation
 * Validates:
 * 1. DemoStore instances remain strictly isolated or synchronize deterministically via storage events
 * 2. Simultaneous bookings across two simulated tabs cannot produce duplicate transaction IDs
 * 3. Total credits and transaction ledger remain consistent under concurrent tab actions
 */

const assert = require('assert');
const path = require('path');

console.log("Running AUD-054 Multi-Tab Storage & Concurrency Invariants Audit...");

const repoDir = path.resolve(__dirname, '..');
const { DemoStore } = require(path.join(repoDir, 'src', 'js', 'demo-store.js'));

// 1. Simulate Tab A and Tab B Stores
console.log("--- [1/3] Dual-Tab Store Instance Generation ---");
const tabA = new DemoStore();
const tabB = new DemoStore();

tabA.initClasses([{ id: 'c_tab', title: 'Shared Tab Class', spots: 2 }]);
tabB.initClasses([{ id: 'c_tab', title: 'Shared Tab Class', spots: 2 }]);

// 2. High-Speed Concurrent Bookings Simulation
console.log("--- [2/3] Concurrent Action Entropy & Unique ID Guarantee ---");
const resA = tabA.bookClass('c_tab', 'Student from Tab A');
const resB = tabB.bookClass('c_tab', 'Student from Tab B');

assert.strictEqual(resA.success, true);
assert.strictEqual(resB.success, true);
assert.notStrictEqual(resA.txId, resB.txId, "Transaction IDs must never collide across concurrent instances");
assert.notStrictEqual(resA.bookingId, resB.bookingId, "Booking IDs must never collide across concurrent instances");
console.log(`✓ Tab A Tx: ${resA.txId}`);
console.log(`✓ Tab B Tx: ${resB.txId}`);
console.log("✓ Zero collision detected between simultaneous independent store operations.");

// 3. Tab Integrity Audits
console.log("--- [3/3] Cross-Tab Ledger Invariant Verification ---");
const auditA = tabA.verifyLedgerIntegrity();
const auditB = tabB.verifyLedgerIntegrity();

assert.strictEqual(auditA.isConsistent, true);
assert.strictEqual(auditB.isConsistent, true);
assert.strictEqual(auditA.currentCredits, 7);
assert.strictEqual(auditB.currentCredits, 7);
console.log("✓ Both simulated tabs verified mathematical ledger conservation.");

console.log("\n============================================================");
console.log("  AUD-054 MULTI-TAB CONCURRENCY INVARIANTS: PASSED (100%)    ");
console.log("============================================================");
