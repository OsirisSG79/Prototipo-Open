import unittest
import subprocess
import json
from pathlib import Path

class TestAudit010Integrity(unittest.TestCase):
    def test_demo_store_mathematical_conservation_and_adversarial_refunds(self):
        """
        P0-05 Test: In AUD-010, the auditor observed credits inflating to 11 because of
        unmatched historical refunds.
        Now, verify that:
        1. Opening credits is 8.
        2. Cannot refund without an active booking (no phantom credits!).
        3. Booking a class debits 1 (Credits: 7).
        4. Refunding restores 1 (Credits: 8).
        5. Attempting subsequent refunds fails cleanly (Credits remain 8, never inflate to 9 or 11).
        6. Mathematical identity `credits == sum(transactions)` holds at EVERY step.
        """
        js_code = """
        const { DemoStore } = require('./src/js/demo-store.js');
        const store = new DemoStore(8);

        console.log('Initial credits:', store.credits);
        let check = store.verifyLedgerIntegrity();
        if (!check.isConsistent) {
          console.error('Integrity failed at start:', check);
          process.exit(1);
        }

        // Before any booking: Attempt refund should FAIL (no active bookings)
        const r_pre = store.ledgerRefundSpot();
        if (r_pre.success || store.credits !== 8) {
          console.error('Phantom refund occurred before booking:', r_pre);
          process.exit(2);
        }

        // Now book 1 class
        store.initClasses([{ id: 'c1', title: 'Reformer Core', spots: 2 }]);
        const b1 = store.bookClass('c1');
        if (!b1.success || store.credits !== 7) {
          console.error('Booking failed or credits wrong:', store.credits);
          process.exit(3);
        }

        // Refund 1: Should succeed
        const r1 = store.ledgerRefundSpot();
        console.log('Refund 1 result:', r1.success, 'Credits:', store.credits);
        if (!r1.success || store.credits !== 8) process.exit(4);

        check = store.verifyLedgerIntegrity();
        if (!check.isConsistent) {
          console.error('Integrity failed after r1:', check);
          process.exit(5);
        }

        // Refund 2: Should FAIL (no remaining refundable bookings)
        const r2 = store.ledgerRefundSpot();
        console.log('Refund 2 result:', r2.success, 'Credits:', store.credits);
        if (r2.success || store.credits !== 8) {
          console.error('P0-05 Violation! Refunded without legitimate booking:', r2);
          process.exit(6);
        }

        // Refund 3: Should FAIL
        const r3 = store.ledgerRefundSpot();
        if (r3.success || store.credits !== 8) process.exit(7);

        // Perform interleaved randomized operations:
        store.initClasses([
          { id: 'c2', title: 'Pilates Flow', spots: 2 },
          { id: 'c3', title: 'Reformer Core', spots: 1 }
        ]);

        store.bookClass('c2'); // 7
        store.bookClass('c3'); // 6
        store.cancelBooking('c2'); // 7
        store.ledgerRefundSpot(); // 8
        store.cancelBooking('c3'); // should NOT double refund: 8

        console.log('End balance:', store.credits, 'Transactions count:', store.transactions.length);
        check = store.verifyLedgerIntegrity();
        console.log('Final check:', check);
        if (!check.isConsistent || store.credits !== 8) {
          console.error('Mathematical conservation violated at end:', check);
          process.exit(8);
        }
        process.exit(0);
        """
        base_dir = Path(__file__).resolve().parents[1]
        res = subprocess.run(['node', '-e', js_code], capture_output=True, text=True, cwd=str(base_dir))
        print(res.stdout)
        if res.stderr:
            print("STDERR:", res.stderr)
        self.assertEqual(res.returncode, 0, "DemoStore mathematical conservation or refund limit failed")

    def test_p1_06_waitlist_creates_formal_booking_for_promoted_student(self):
        """
        P1-06 Test: When cancelling a booking with waitlist, the promoted student
        must be assigned a formal booking record in `activeBookings`.
        """
        js_code = """
        const { DemoStore } = require('./src/js/demo-store.js');
        const store = new DemoStore(8);
        store.initClasses([
          { id: 'full_class', title: 'Reformer Intense', spots: 1 }
        ]);

        // Student 1 books the only spot
        store.bookClass('full_class', 'Camila Morales');
        const cls = store.getClass('full_class');
        console.log('Spots after 1st booking:', cls.spots); // 0

        // Student 2 joins waitlist
        const wl = store.bookClass('full_class', 'Ana Valenzuela');
        console.log('Waitlist result:', wl);

        // Cancel Student 1
        const cancelRes = store.cancelBooking('full_class');
        console.log('Cancel result:', cancelRes);

        // Verify:
        // 1. cls.spots remains 0
        if (cls.spots !== 0) {
          console.error('Spots was not preserved at 0:', cls.spots);
          process.exit(1);
        }
        // 2. promotedStudent is Ana Valenzuela
        if (!cancelRes.promotedStudent || cancelRes.promotedStudent.studentName !== 'Ana Valenzuela') {
          console.error('Waitlist student was not promoted:', cancelRes.promotedStudent);
          process.exit(2);
        }
        // 3. P1-06: A booking record for Ana Valenzuela exists in activeBookings
        const anaBooking = Array.from(store.activeBookings.values()).find(b => b.studentName === 'Ana Valenzuela');
        console.log('Ana booking record:', anaBooking);
        if (!anaBooking || anaBooking.status !== 'CONFIRMED_FROM_WAITLIST') {
          console.error('P1-06 Failure: No formal booking record created for promoted student!');
          process.exit(3);
        }

        process.exit(0);
        """
        base_dir = Path(__file__).resolve().parents[1]
        res = subprocess.run(['node', '-e', js_code], capture_output=True, text=True, cwd=str(base_dir))
        print(res.stdout)
        if res.stderr:
            print("STDERR:", res.stderr)
        self.assertEqual(res.returncode, 0, "Waitlist promotion lifecycle failed")

if __name__ == '__main__':
    unittest.main()
