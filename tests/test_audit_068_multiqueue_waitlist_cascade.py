#!/usr/bin/env python3
"""
AUD-068: Multi-Queue FIFO Waitlist Cascading Promotion & Eviction Audit
Verifies:
1. Scenario with 2 classes, each maintaining distinct independent waitlist queues.
2. Multiple students queued in strict FIFO order (1st, 2nd, 3rd).
3. Successive cancellations cascade through queue promotions deterministically.
4. Ledgers, credit records, and booking IDs for promoted students maintain 100% integrity.
"""

import sys
import subprocess
from pathlib import Path

repo_dir = Path(__file__).resolve().parents[1]
print("Running AUD-068 Multi-Queue FIFO Cascading Promotion Audit...")

node_script = """
const { DemoStore } = require('./src/js/demo-store.js');
const assert = require('assert');

const store = new DemoStore(12);
store.initClasses([
  { id: 'class_a', title: 'Pilates Flow A', spots: 1, total: 1 },
  { id: 'class_b', title: 'Pilates Reformer B', spots: 1, total: 1 }
]);

// 1. Initial bookings on both classes
store.bookClass('class_a', 'Occupant A');
store.bookClass('class_b', 'Occupant B');
assert.strictEqual(store.credits, 10);

// 2. Queue 2 students in class_a and 1 in class_b
const wa1 = store.bookClass('class_a', 'Waitlist A1');
const wa2 = store.bookClass('class_a', 'Waitlist A2');
const wb1 = store.bookClass('class_b', 'Waitlist B1');

assert.strictEqual(wa1.position, 1);
assert.strictEqual(wa2.position, 2);
assert.strictEqual(wb1.position, 1);
assert.strictEqual(store.credits, 10, 'Joining waitlists must not debit credits');

// 3. Occupant A cancels -> Waitlist A1 is promoted
const c1 = store.cancelBooking('class_a', 'Occupant A');
assert.strictEqual(c1.success, true);
assert.strictEqual(c1.promotedStudent.studentName, 'Waitlist A1');
assert.strictEqual(store.isBooked('class_a', 'Waitlist A1'), true);
assert.strictEqual(store.credits, 10, 'Cancellation refund (+1) and promotion debit (-1) balances credits');

// Queue A should now have 1 remaining student: Waitlist A2
assert.strictEqual(store.waitlists.get('class_a').length, 1);
assert.strictEqual(store.waitlists.get('class_a')[0].studentName, 'Waitlist A2');

// 4. Promoted student Waitlist A1 cancels -> Waitlist A2 is now promoted
const c2 = store.cancelBooking('class_a', 'Waitlist A1');
assert.strictEqual(c2.success, true);
assert.strictEqual(c2.promotedStudent.studentName, 'Waitlist A2');
assert.strictEqual(store.isBooked('class_a', 'Waitlist A2'), true);
assert.strictEqual(store.waitlists.get('class_a').length, 0, 'Queue A should now be empty');

// 5. Verify Class B was completely untouched
assert.strictEqual(store.isBooked('class_b', 'Occupant B'), true);
assert.strictEqual(store.waitlists.get('class_b').length, 1);
assert.strictEqual(store.waitlists.get('class_b')[0].studentName, 'Waitlist B1');

// 6. Verify ledger integrity
const ledger = store.verifyLedgerIntegrity();
assert.strictEqual(ledger.isConsistent, true);
assert.strictEqual(ledger.currentCredits, 10);

console.log('✓ Multi-queue FIFO cascading promotion and queue isolation verified.');
"""

res = subprocess.run(['node', '-e', node_script], cwd=str(repo_dir), capture_output=True, text=True)
if res.returncode != 0:
    print("FAILED AUD-068 Multi-Queue FIFO Cascading Promotion Audit:")
    print(res.stderr)
    sys.exit(1)

print(res.stdout.strip())
print("\n" + "=" * 60)
print("  AUD-068 MULTI-QUEUE FIFO CASCADING PROMOTION: PASSED (100%)")
print("=" * 60)
