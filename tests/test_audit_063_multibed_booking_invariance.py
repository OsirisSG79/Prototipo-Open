#!/usr/bin/env python3
"""
AUD-063: Multi-Bed Concurrent Booking Invariance & Non-Overwrite Audit (AUD-011 P0-01)
Verifies:
1. Two distinct students booking a 2-bed capacity class preserves BOTH records.
2. activeBookings / bookingsById indexes both bookings without overwrite.
3. Cancelling one student does not cancel or invalidate the other student.
4. Total spots, credits, and ledger balance reconcile exactly across multi-bed scenarios.
"""

import sys
import subprocess
import json
from pathlib import Path

repo_dir = Path(__file__).resolve().parents[1]
print("Running AUD-063 Multi-Bed Booking Invariance & Non-Overwrite Audit...")

node_script = """
const { DemoStore } = require('./src/js/demo-store.js');
const assert = require('assert');

const store = new DemoStore(8);
store.initClasses([{ id: 'class_2beds', title: 'Reformer Duo (2 Camas)', spots: 2 }]);

// 1. Initial balance check (P1-02A)
assert.strictEqual(store.credits, 8, 'Initial credits must be 8');
assert.strictEqual(store.transactions[0].balanceAfter, 8, 'Initial balanceAfter must be 8, not 16');

// 2. Multi-bed booking without overwrite (P0-01)
const resAna = store.bookClass('class_2beds', 'Ana Valenzuela');
const resBeto = store.bookClass('class_2beds', 'Beto Silva');

assert.strictEqual(resAna.success, true, 'Ana booking must succeed');
assert.strictEqual(resBeto.success, true, 'Beto booking must succeed');
assert.strictEqual(store.credits, 6, 'Credits after 2 bookings must be 6');

// Both must be active and distinct
assert.strictEqual(store.isBooked('class_2beds', 'Ana Valenzuela'), true, 'Ana must be booked');
assert.strictEqual(store.isBooked('class_2beds', 'Beto Silva'), true, 'Beto must be booked');

const bookings = store.getBookingsForClass('class_2beds');
assert.strictEqual(bookings.length, 2, 'Class must have exactly 2 active bookings');
assert.notStrictEqual(resAna.bookingId, resBeto.bookingId, 'Booking IDs must be distinct');

// 3. Cancel Beto without affecting Ana
const cancelBeto = store.cancelBooking('class_2beds', 'Beto Silva');
assert.strictEqual(cancelBeto.success, true, 'Beto cancellation must succeed');
assert.strictEqual(cancelBeto.creditRefunded, true, 'Beto refund must be credited');
assert.strictEqual(store.credits, 7, 'Credits after Beto cancel must be 7');

assert.strictEqual(store.isBooked('class_2beds', 'Ana Valenzuela'), true, 'Ana must STILL be booked');
assert.strictEqual(store.isBooked('class_2beds', 'Beto Silva'), false, 'Beto must no longer be booked');

// 4. Ledger consistency
const ledger = store.verifyLedgerIntegrity();
assert.strictEqual(ledger.isConsistent, true, 'Ledger must remain strictly consistent');
assert.strictEqual(ledger.currentCredits, 7);

console.log('✓ Multi-bed concurrent booking invariants verified.');
"""

res = subprocess.run(['node', '-e', node_script], cwd=str(repo_dir), capture_output=True, text=True)
if res.returncode != 0:
    print("FAILED AUD-063 Multi-Bed Concurrent Booking Audit:")
    print(res.stderr)
    sys.exit(1)

print(res.stdout.strip())
print("\n" + "=" * 60)
print("  AUD-063 MULTI-BED CONCURRENT BOOKING: PASSED (100%)")
print("=" * 60)
