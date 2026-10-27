#!/usr/bin/env python3
"""
AUD-065: Multi-Student Independent Cancellation & Credit Conservation Audit
Verifies:
1. Scenario with 3 students booking distinct beds in a 3-bed class.
2. Independent cancellation of any middle student restores exactly 1 credit
   without disturbing the remaining 2 bookings.
3. Class inventory reflects exactly 1 spot freed up.
4. Total ledger mathematical sum matches credits at every step.
"""

import sys
import subprocess
from pathlib import Path

repo_dir = Path(__file__).resolve().parents[1]
print("Running AUD-065 Multi-Student Independent Cancellation Audit...")

node_script = """
const { DemoStore } = require('./src/js/demo-store.js');
const assert = require('assert');

const store = new DemoStore(10);
store.initClasses([{ id: 'class_trio', title: 'Reformer Trio (3 Camas)', spots: 3, total: 3 }]);

// 1. Three distinct students book
const b1 = store.bookClass('class_trio', 'Alumna Uno');
const b2 = store.bookClass('class_trio', 'Alumna Dos');
const b3 = store.bookClass('class_trio', 'Alumna Tres');

assert.strictEqual(b1.success, true);
assert.strictEqual(b2.success, true);
assert.strictEqual(b3.success, true);
assert.strictEqual(store.credits, 7);
assert.strictEqual(store.getClass('class_trio').spots, 0);

// 2. Verify all 3 are marked booked
assert.strictEqual(store.isBooked('class_trio', 'Alumna Uno'), true);
assert.strictEqual(store.isBooked('class_trio', 'Alumna Dos'), true);
assert.strictEqual(store.isBooked('class_trio', 'Alumna Tres'), true);

const activeTrio = store.getBookingsForClass('class_trio');
assert.strictEqual(activeTrio.length, 3);

// 3. Cancel middle student (Alumna Dos) specifically by bookingId
const cDos = store.cancelBooking(b2.bookingId);
assert.strictEqual(cDos.success, true);
assert.strictEqual(cDos.creditRefunded, true);
assert.strictEqual(store.credits, 8);
assert.strictEqual(store.getClass('class_trio').spots, 1);

// 4. Verify Alumna Uno and Alumna Tres remain confirmed
assert.strictEqual(store.isBooked('class_trio', 'Alumna Uno'), true, 'Alumna Uno must remain booked');
assert.strictEqual(store.isBooked('class_trio', 'Alumna Dos'), false, 'Alumna Dos must be cancelled');
assert.strictEqual(store.isBooked('class_trio', 'Alumna Tres'), true, 'Alumna Tres must remain booked');

const remainingTrio = store.getBookingsForClass('class_trio');
assert.strictEqual(remainingTrio.length, 2);

// 5. Verify ledger conservation
const ledger = store.verifyLedgerIntegrity();
assert.strictEqual(ledger.isConsistent, true);
assert.strictEqual(ledger.currentCredits, 8);

console.log('✓ Multi-student independent cancellation and credit conservation verified.');
"""

res = subprocess.run(['node', '-e', node_script], cwd=str(repo_dir), capture_output=True, text=True)
if res.returncode != 0:
    print("FAILED AUD-065 Multi-Student Independent Cancellation Audit:")
    print(res.stderr)
    sys.exit(1)

print(res.stdout.strip())
print("\n" + "=" * 60)
print("  AUD-065 MULTI-STUDENT CANCELLATION: PASSED (100%)")
print("=" * 60)
