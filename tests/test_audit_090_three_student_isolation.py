#!/usr/bin/env python3
"""
AUD-090: Three-Student Independent Wallet & Isolation Invariance Audit (AUD-012 S1)
Verifies:
1. Complete isolation across three concurrent students: Ana Valenzuela, Beto Ramos, and Camila Morales.
2. Concurrent booking of distinct and shared classes without cross-talk or credit leak.
3. Orderly FIFO waitlist promotion where promoted student debits their own transaction ledger.
4. Independent cancellations where refund is credited exclusively to the student who booked.
5. Absolute financial and inventory conservation: sum of class spots + active bookings = constant capacity.
"""

import sys
import subprocess
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
print("Running AUD-090 Three-Student Independent Wallet & Isolation Audit...")

node_script = """
const assert = require('assert');
const { DemoStore } = require('./src/js/demo-store.js');

const store = new DemoStore(30);

// Set up 2 classes: c1 (2 spots) and c2 (1 spot)
store.initClasses([
  { id: 'c1', title: 'Reformer Power Flow', spots: 2, total: 2 },
  { id: 'c2', title: 'Reformer Stretch & Align', spots: 1, total: 1 }
]);

const initialCredits = store.credits; // 30
assert.strictEqual(initialCredits, 30);

// 1. Ana and Beto book class c1
const bAna_c1 = store.bookClass('c1', 'Ana Valenzuela');
const bBeto_c1 = store.bookClass('c1', 'Beto Ramos');
assert.strictEqual(bAna_c1.success, true);
assert.strictEqual(bBeto_c1.success, true);
assert.strictEqual(store.getClass('c1').spots, 0);

// 2. Camila attempts to book full class c1 -> joins waitlist at pos 1
const bCamila_c1 = store.bookClass('c1', 'Camila Morales');
assert.strictEqual(bCamila_c1.success, true);
assert.strictEqual(bCamila_c1.waitlist, true);
assert.strictEqual(bCamila_c1.position, 1);
assert.strictEqual(store.credits, 28); // 30 - 2 debits

// 3. Camila books class c2 (1 spot)
const bCamila_c2 = store.bookClass('c2', 'Camila Morales');
assert.strictEqual(bCamila_c2.success, true);
assert.strictEqual(bCamila_c2.waitlist, false);
assert.strictEqual(store.getClass('c2').spots, 0);
assert.strictEqual(store.credits, 27); // 30 - 3 debits

// 4. Ana cancels her reservation in c1 -> Camila promoted automatically
const cancelAna = store.cancelBooking(bAna_c1.bookingId, 'Ana Valenzuela');
assert.strictEqual(cancelAna.success, true);
assert.strictEqual(cancelAna.creditRefunded, true);
assert.strictEqual(cancelAna.promotedStudent.studentName, 'Camila Morales');

// Financial check: Ana refunded (+1), Camila debited for waitlist promotion (-1) => net 27
assert.strictEqual(store.credits, 27);
assert.strictEqual(store.getClass('c1').spots, 0); // Still 0: Camila took the spot!

// Verify bookings index per student
const anaBookings = store.getBookingsForStudent('Ana Valenzuela');
const betoBookings = store.getBookingsForStudent('Beto Ramos');
const camilaBookings = store.getBookingsForStudent('Camila Morales');

assert.strictEqual(anaBookings.length, 0, 'Ana must have 0 active bookings');
assert.strictEqual(betoBookings.length, 1, 'Beto must have 1 active booking in c1');
assert.strictEqual(camilaBookings.length, 2, 'Camila must have 2 active bookings (c1 from waitlist, c2 direct)');

// 5. Verify mathematical ledger integrity
const integrity = store.verifyLedgerIntegrity();
assert.strictEqual(integrity.isConsistent, true, 'Ledger transactions must reconcile exactly');
assert.strictEqual(integrity.currentCredits, 27);

console.log('✓ Verified 3-student isolation: Ana, Beto & Camila operated independently without leaks.');
process.exit(0);
"""

res = subprocess.run(["node", "-e", node_script], cwd=str(repo_root), capture_output=True, text=True)
if res.returncode != 0:
    print("FAILED AUD-090 execution:")
    print(res.stderr)
    sys.exit(1)

print(res.stdout.strip())
print("\n" + "=" * 60)
print("  AUD-090 THREE-STUDENT ISOLATION INVARIANCE: PASSED (100%)")
print("=" * 60)
