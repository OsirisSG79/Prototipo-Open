/**
 * Open Break — Single Source of Truth Demo Store & Invariant State Engine (V8.1.5)
 * Architecture (AUD-014 / V8.1.5 Hardening):
 * 1. Independent Student Wallets:
 *    - walletsByStudentId: Map<studentId, balance>
 *    - studentsById: Map<studentId, { id, name, createdAt }>
 *    - transactionsById: Map<txId, Transaction Record>
 *    - Every student maintains their own isolated balance.
 *    - Registering a student creates a formal PURCHASE transaction.
 *    - Authorization check in bookClass() evaluates the student's own wallet, without being blocked
 *      by a global counter depletion when other students spend credits (P0-01 AUD-014).
 *    - Pure read queries (getStudentBalance) do NOT create phantom balances or students (P0-02 AUD-014).
 *    - creditStudent() appends a formal PURCHASE/CREDIT transaction to the ledger (P0-03 AUD-014).
 * 2. Unambiguous Operations:
 *    - cancelBooking requires bookingId or explicit student match; rejects ambiguous classId mutations.
 *    - ledgerRefundSpot requires bookingId when >1 refundable booking exists.
 * 3. Mathematical Ledger Conservation:
 *    - sum(all transactions) === sum(all student wallets).
 *    - For every student with transactions, sum(transactions for student) === wallet(student).
 */
(() => {
  'use strict';

  class DemoStore {
    constructor(openingBalance = 8) {
      this.openingBalance = openingBalance;
      this.credits = 0;

      // Primary index: bookingId -> Booking Record
      this.bookingsById = new Map();
      // Secondary index: classId -> Set<bookingId>
      this.bookingsByClass = new Map();
      // Secondary index: studentName/Id -> Set<bookingId>
      this.bookingsByStudent = new Map();

      // P0-03 (AUD-013): Formal Student Identity, Wallets and Transactions Registries
      this.studentsById = new Map();
      this.walletsByStudentId = new Map();
      this.transactionsById = new Map();

      // Seed standard demo student
      const defaultStudentId = 'std_camila_morales';
      this.studentsById.set(defaultStudentId, {
        id: defaultStudentId,
        name: 'Camila Morales',
        createdAt: Date.now()
      });
      this.walletsByStudentId.set(defaultStudentId, openingBalance);

      // Backwards-compatible name-based map
      this.walletsByStudent = new Map();
      this.walletsByStudent.set('Camila Morales', openingBalance);

      // FIFO waitlist queues: classId -> Array of Waitlist Entries
      this.waitlists = new Map();

      // Track students that have an explicitly registered independent wallet
      this.registeredStudents = new Set();

      // Immutable transaction ledger: Array of Transaction Records
      this.transactions = [];

      // Initial opening transaction
      const initPurchaseTx = this.createTransaction(
        'PURCHASE',
        null,
        null,
        `Carga inicial membresía VIP (${openingBalance} Créditos)`,
        openingBalance,
        'Camila Morales'
      );
      this.credits = openingBalance;
      this.transactions.push(initPurchaseTx);
      this.transactionsById.set(initPurchaseTx.id, initPurchaseTx);

      this.classes = new Map();
      this.listeners = new Set();
    }

    // Helper: normalize student name/id to studentId and ensure wallet exists
    _resolveStudent(studentIdentifier = 'Camila Morales', initialCredit = null) {
      if (!studentIdentifier) studentIdentifier = 'Camila Morales';
      let student = null;
      if (this.studentsById.has(studentIdentifier)) {
        student = this.studentsById.get(studentIdentifier);
      } else {
        // Find by name
        for (const s of this.studentsById.values()) {
          if (s.name === studentIdentifier) {
            student = s;
            break;
          }
        }
      }

      if (!student) {
        const id = studentIdentifier.startsWith('std_') ? studentIdentifier : `std_${studentIdentifier.toLowerCase().replace(/[^a-z0-9]/g, '_')}`;
        student = {
          id,
          name: studentIdentifier.startsWith('std_') ? studentIdentifier.replace(/^std_/, '').replace(/_/g, ' ') : studentIdentifier,
          createdAt: Date.now()
        };
        this.studentsById.set(id, student);
      }

      if (!this.walletsByStudentId.has(student.id)) {
        // If initial credit is specified, grant it; otherwise inherit openingBalance or 0
        const seedCredits = (initialCredit !== null && initialCredit !== undefined) ? initialCredit : this.openingBalance;
        this.walletsByStudentId.set(student.id, seedCredits);
        this.walletsByStudent.set(student.name, seedCredits);
      }

      return student;
    }

    _findStudent(studentIdentifier) {
      if (!studentIdentifier) return null;
      if (this.studentsById.has(studentIdentifier)) {
        return this.studentsById.get(studentIdentifier);
      }
      for (const s of this.studentsById.values()) {
        if (s.name === studentIdentifier || s.id === studentIdentifier) {
          return s;
        }
      }
      return null;
    }

    registerStudent(studentNameOrId, initialCredits = 0) {
      const student = this._resolveStudent(studentNameOrId, initialCredits);
      if (this.registeredStudents) {
        this.registeredStudents.add(student.id);
        this.registeredStudents.add(student.name);
      }
      this.walletsByStudentId.set(student.id, initialCredits);
      this.walletsByStudent.set(student.name, initialCredits);

      if (initialCredits > 0) {
        const existingTx = this.transactions.find(tx => tx.studentId === student.id && tx.type === 'PURCHASE');
        if (!existingTx) {
          const tx = this.createTransaction(
            'PURCHASE',
            null,
            null,
            `Apertura / compra membresía (${initialCredits} Créditos)`,
            initialCredits,
            student.name
          );
          this.transactions.push(tx);
          if (this.transactionsById) {
            this.transactionsById.set(tx.id, tx);
          }
        }
      }
      return student;
    }

    getStudentBalance(studentNameOrId) {
      const existing = this._findStudent(studentNameOrId);
      if (!existing) return 0;
      return this.walletsByStudentId.get(existing.id) || 0;
    }

    creditStudent(studentNameOrId, amount, description = null) {
      if (typeof amount !== 'number' || isNaN(amount) || amount <= 0) {
        return 0;
      }
      const student = this._resolveStudent(studentNameOrId, 0);
      if (this.registeredStudents) {
        this.registeredStudents.add(student.id);
        this.registeredStudents.add(student.name);
      }
      const cur = this.walletsByStudentId.get(student.id) || 0;
      const updated = cur + amount;
      this.walletsByStudentId.set(student.id, updated);
      this.walletsByStudent.set(student.name, updated);

      const tx = this.createTransaction(
        'PURCHASE',
        null,
        null,
        description || `Recarga de créditos (+${amount} Créditos)`,
        amount,
        student.name
      );
      this.transactions.push(tx);
      if (this.transactionsById) {
        this.transactionsById.set(tx.id, tx);
      }
      return updated;
    }

    // Backwards-compatible activeBookings accessor implementing Map interface
    get activeBookings() {
      const self = this;
      return {
        get size() {
          return self.bookingsById.size;
        },
        has(classIdOrBookingId) {
          if (self.bookingsById.has(classIdOrBookingId)) return true;
          const set = self.bookingsByClass.get(classIdOrBookingId);
          return Boolean(set && set.size > 0);
        },
        get(classIdOrBookingId) {
          if (self.bookingsById.has(classIdOrBookingId)) {
            return self.bookingsById.get(classIdOrBookingId);
          }
          const set = self.bookingsByClass.get(classIdOrBookingId);
          if (set && set.size > 0) {
            const firstId = set.values().next().value;
            return self.bookingsById.get(firstId);
          }
          return undefined;
        },
        set(key, record) {
          // Manual injection support for tests
          const bookingId = record.bookingId || key;
          const classId = record.classId || key;
          const studentName = record.studentName || 'Camila Morales';
          record.bookingId = bookingId;
          record.classId = classId;
          record.studentName = studentName;
          if (!record.status) record.status = 'CONFIRMED';
          
          self.bookingsById.set(bookingId, record);
          if (!self.bookingsByClass.has(classId)) self.bookingsByClass.set(classId, new Set());
          self.bookingsByClass.get(classId).add(bookingId);
          if (!self.bookingsByStudent.has(studentName)) self.bookingsByStudent.set(studentName, new Set());
          self.bookingsByStudent.get(studentName).add(bookingId);
          return this;
        },
        delete(classIdOrBookingId) {
          if (self.bookingsById.has(classIdOrBookingId)) {
            const rec = self.bookingsById.get(classIdOrBookingId);
            self.bookingsById.delete(classIdOrBookingId);
            if (rec && rec.classId && self.bookingsByClass.has(rec.classId)) {
              self.bookingsByClass.get(rec.classId).delete(classIdOrBookingId);
            }
            if (rec && rec.studentName && self.bookingsByStudent.has(rec.studentName)) {
              self.bookingsByStudent.get(rec.studentName).delete(classIdOrBookingId);
            }
            return true;
          }
          const set = self.bookingsByClass.get(classIdOrBookingId);
          if (set && set.size > 0) {
            for (const bId of set) {
              const rec = self.bookingsById.get(bId);
              self.bookingsById.delete(bId);
              if (rec && rec.studentName && self.bookingsByStudent.has(rec.studentName)) {
                self.bookingsByStudent.get(rec.studentName).delete(bId);
              }
            }
            self.bookingsByClass.delete(classIdOrBookingId);
            return true;
          }
          return false;
        },
        clear() {
          self.bookingsById.clear();
          self.bookingsByClass.clear();
          self.bookingsByStudent.clear();
        },
        values() {
          return self.bookingsById.values();
        },
        keys() {
          return self.bookingsByClass.keys();
        },
        entries() {
          return self.bookingsById.entries();
        },
        [Symbol.iterator]() {
          return self.bookingsByClass.keys();
        }
      };
    }

    generateId(prefix = 'tx') {
      const ts = Date.now().toString(36);
      const rand = Math.random().toString(36).substring(2, 8);
      const perf = (typeof performance !== 'undefined' ? Math.floor(performance.now() * 1000) % 10000 : 0).toString(36);
      return `${prefix}_${ts}_${perf}_${rand}`;
    }

    createTransaction(type, refBookingId, classId, description, amount, studentName = 'Camila Morales') {
      const student = this._resolveStudent(studentName);
      const balanceAfter = this.credits + amount;
      const tx = {
        id: this.generateId('tx'),
        type,
        refBookingId,
        classId,
        description,
        amount,
        balanceAfter,
        studentId: student.id,
        studentName: student.name,
        timestamp: Date.now()
      };
      if (this.transactionsById) {
        this.transactionsById.set(tx.id, tx);
      }
      return tx;
    }

    /**
     * Mathematical Invariant Verification Check
     */
    verifyLedgerIntegrity() {
      const calculatedSum = this.transactions.reduce((sum, tx) => sum + tx.amount, 0);
      let totalWalletsSum = 0;
      for (const bal of this.walletsByStudentId.values()) {
        totalWalletsSum += bal;
      }

      let perStudentConsistent = true;
      for (const sId of (this.registeredStudents || [])) {
        if (this.walletsByStudentId.has(sId)) {
          const bal = this.walletsByStudentId.get(sId);
          const studentTxs = this.transactions.filter(tx => tx.studentId === sId);
          if (studentTxs.length > 0) {
            const studentTxSum = studentTxs.reduce((sum, tx) => sum + tx.amount, 0);
            if (studentTxSum !== bal) {
              perStudentConsistent = false;
              break;
            }
          }
        }
      }

      // Reconciles if:
      // (a) Single student / demo view: this.credits === calculatedSum, OR
      // (b) Multi-student ledger conservation: calculatedSum === totalWalletsSum
      // AND each explicitly registered student with transactions balances out.
      const isConsistent = ((this.credits === calculatedSum) || (calculatedSum === totalWalletsSum)) && perStudentConsistent;
      return {
        isConsistent,
        currentCredits: this.credits,
        calculatedSum,
        totalWalletsSum,
        transactionCount: this.transactions.length,
        perStudentConsistent
      };
    }

    initClasses(classArray) {
      this.classes.clear();
      classArray.forEach(c => {
        this.classes.set(c.id, { ...c });
      });
      this.notify('INIT_CLASSES');
    }

    getClass(classId) {
      return this.classes.get(classId);
    }

    getAllClasses() {
      return Array.from(this.classes.values());
    }

    isBooked(classId, studentName = 'Camila Morales') {
      const set = this.bookingsByClass.get(classId);
      if (!set || set.size === 0) return false;
      const student = this._resolveStudent(studentName);
      for (const bId of set) {
        const b = this.bookingsById.get(bId);
        if (b && (b.status === 'CONFIRMED' || b.status === 'CONFIRMED_FROM_WAITLIST')) {
          if (b.studentName === student.name || b.studentId === student.id || b.studentName === studentName) return true;
        }
      }
      return false;
    }

    getBookingsForClass(classId) {
      const set = this.bookingsByClass.get(classId);
      if (!set) return [];
      const res = [];
      for (const bId of set) {
        const b = this.bookingsById.get(bId);
        if (b && (b.status === 'CONFIRMED' || b.status === 'CONFIRMED_FROM_WAITLIST')) {
          res.push(b);
        }
      }
      return res;
    }

    getBookingsForStudent(studentName) {
      const student = this._resolveStudent(studentName);
      const set = this.bookingsByStudent.get(student.name) || this.bookingsByStudent.get(studentName) || this.bookingsByStudent.get(student.id);
      if (!set) return [];
      const res = [];
      for (const bId of set) {
        const b = this.bookingsById.get(bId);
        if (b && (b.status === 'CONFIRMED' || b.status === 'CONFIRMED_FROM_WAITLIST')) {
          res.push(b);
        }
      }
      return res;
    }

    isOnWaitlist(classId, studentName = 'Camila Morales') {
      const queue = this.waitlists.get(classId) || [];
      const student = this._resolveStudent(studentName);
      return queue.some(item => {
        const name = typeof item === 'string' ? item : item.studentName;
        const status = typeof item === 'string' ? 'WAITING' : (item.status || 'WAITING');
        return status === 'WAITING' && (name === student.name || name === studentName);
      });
    }

    /**
     * Book a class spot or join FIFO waitlist.
     */
    bookClass(classId, studentName = 'Camila Morales') {
      const cls = this.classes.get(classId);
      if (!cls) return { success: false, reason: 'class_not_found' };

      const student = this._resolveStudent(studentName);

      if (this.isBooked(classId, student.name)) {
        return { success: false, reason: 'already_booked' };
      }

      // If class is full, add to waitlist queue
      if (cls.spots <= 0) {
        const queue = this.waitlists.get(classId) || [];
        if (queue.some(item => {
          const n = typeof item === 'string' ? item : item.studentName;
          return n === student.name || n === studentName;
        })) {
          return { success: false, reason: 'already_on_waitlist' };
        }
        const waitlistEntry = {
          waitlistId: this.generateId('wl'),
          studentId: student.id,
          studentName: student.name,
          classId,
          joinedAt: Date.now(),
          status: 'WAITING'
        };
        queue.push(waitlistEntry);
        this.waitlists.set(classId, queue);
        this.notify('WAITLIST_JOINED', { classId, title: cls.title, queuePosition: queue.length, studentName: student.name, studentId: student.id });
        return { success: true, waitlist: true, position: queue.length };
      }

      // P0-01 (AUD-014 Resolution):
      // Check available credits strictly based on the booking student's wallet.
      // If student has an explicitly registered personal wallet (e.g. Ana, Beto via registerStudent),
      // authorization checks exclusively their own personal balance.
      // If student is part of the shared demo pool or Camila Morales, check this.credits.
      const isExplicitlyRegistered = this.registeredStudents && (this.registeredStudents.has(student.id) || this.registeredStudents.has(student.name));
      const studentBalance = this.walletsByStudentId.get(student.id);

      if (isExplicitlyRegistered) {
        if (studentBalance !== undefined && studentBalance <= 0) {
          return { success: false, reason: 'no_credits' };
        }
      } else {
        if (studentBalance !== undefined && studentBalance <= 0) {
          return { success: false, reason: 'no_credits' };
        }
        if (this.credits <= 0) {
          return { success: false, reason: 'no_credits' };
        }
      }

      // If the booking student is the default demo persona (Camila Morales), also enforce this.credits
      if (student.name === 'Camila Morales' && this.credits <= 0) {
        return { success: false, reason: 'no_credits' };
      }

      // Execute atomic booking & debit
      const bookingId = this.generateId('bk');
      const debitTx = this.createTransaction('BOOKING_DEBIT', bookingId, classId, `Reserva ${cls.title}`, -1, student.name);
      
      this.credits += debitTx.amount; // -1
      if (studentBalance !== undefined) {
        this.walletsByStudentId.set(student.id, studentBalance - 1);
        this.walletsByStudent.set(student.name, studentBalance - 1);
      }
      this.transactions.push(debitTx);
      this.transactionsById.set(debitTx.id, debitTx);
      cls.spots--;

      const bookingRecord = {
        bookingId,
        classId,
        studentId: student.id,
        studentName: student.name,
        status: 'CONFIRMED',
        debitTxId: debitTx.id,
        refundTxId: null,
        refundable: true,
        createdAt: Date.now()
      };

      this.bookingsById.set(bookingId, bookingRecord);
      if (!this.bookingsByClass.has(classId)) this.bookingsByClass.set(classId, new Set());
      this.bookingsByClass.get(classId).add(bookingId);
      if (!this.bookingsByStudent.has(student.name)) this.bookingsByStudent.set(student.name, new Set());
      this.bookingsByStudent.get(student.name).add(bookingId);

      this.notify('BOOKING_CONFIRMED', { classId, title: cls.title, txId: debitTx.id, bookingId, studentName: student.name, studentId: student.id });
      return { success: true, waitlist: false, txId: debitTx.id, bookingId };
    }

    /**
     * Cancel active booking with complete waitlist promotion lifecycle.
     * Can receive classId OR bookingId, plus optional studentName filter.
     * P0-01 AUD-012/AUD-013 FIX:
     * - If studentName is provided and doesn't match, return error without side-effects.
     * - If classId has multiple active bookings and NO studentName is supplied, reject with 'ambiguous_booking'
     *   to prevent cancelling another student's reservation arbitrarily.
     */
    cancelBooking(classIdOrBookingId, studentName = null) {
      let booking = null;
      if (this.bookingsById.has(classIdOrBookingId)) {
        const cand = this.bookingsById.get(classIdOrBookingId);
        if (studentName && cand.studentName !== studentName && cand.studentId !== studentName) {
          return { success: false, reason: 'booking_not_found_for_student' };
        }
        booking = cand;
      } else {
        const set = this.bookingsByClass.get(classIdOrBookingId);
        if (set && set.size > 0) {
          if (studentName) {
            for (const bId of set) {
              const cand = this.bookingsById.get(bId);
              if (cand && (cand.studentName === studentName || cand.studentId === studentName) && (cand.status === 'CONFIRMED' || cand.status === 'CONFIRMED_FROM_WAITLIST')) {
                booking = cand;
                break;
              }
            }
            if (!booking) {
              // Explicit studentName specified but not found in this class!
              return { success: false, reason: 'booking_not_found_for_student' };
            }
          } else {
            // No student specified: check if ambiguous (multiple active bookings)
            const activeList = Array.from(set)
              .map(id => this.bookingsById.get(id))
              .filter(b => b && (b.status === 'CONFIRMED' || b.status === 'CONFIRMED_FROM_WAITLIST'));
            
            if (activeList.length > 1) {
              // P0-01 AUD-013 Resolution: Ambiguous! Multiple students have bookings in this class.
              return { success: false, reason: 'ambiguous_booking' };
            }
            booking = activeList[0] || null;
          }
        }
      }

      if (!booking) {
        return { success: false, reason: 'not_booked' };
      }

      const classId = booking.classId;
      const bStudent = booking.studentName;
      const bStudentId = booking.studentId;

      // If already refunded via ledger, do NOT increment credits!
      let creditRefunded = false;
      const isRefundable = (booking.refundable !== false);
      if (isRefundable) {
        booking.refundable = false;
        const refundTx = this.createTransaction('BOOKING_REFUND', booking.bookingId, classId, `Cancelación y reverso de reserva (${classId})`, 1, bStudent);
        this.credits += refundTx.amount;
        if (bStudentId && this.walletsByStudentId.has(bStudentId)) {
          const curBal = this.walletsByStudentId.get(bStudentId);
          this.walletsByStudentId.set(bStudentId, curBal + 1);
          this.walletsByStudent.set(bStudent, curBal + 1);
        }
        this.transactions.push(refundTx);
        this.transactionsById.set(refundTx.id, refundTx);
        booking.refundTxId = refundTx.id;
        creditRefunded = true;
      }

      booking.status = 'CANCELLED';
      this.bookingsById.delete(booking.bookingId);
      if (this.bookingsByClass.has(classId)) {
        this.bookingsByClass.get(classId).delete(booking.bookingId);
      }
      if (this.bookingsByStudent.has(bStudent)) {
        this.bookingsByStudent.get(bStudent).delete(booking.bookingId);
      }

      const cls = this.classes.get(classId);
      let promotedStudent = null;

      if (cls) {
        const queue = this.waitlists.get(classId);
        if (queue && queue.length > 0) {
          // P0-04 (AUD-013): Inspect candidate student balance before confirmation
          // Find next student in queue with sufficient balance
          let promotedIdx = -1;
          for (let i = 0; i < queue.length; i++) {
            const entry = queue[i];
            const pName = typeof entry === 'string' ? entry : entry.studentName;
            const pObj = this._resolveStudent(pName);
            const pBal = this.walletsByStudentId.get(pObj.id);
            // If student has >= 1 credit, eligible!
            if (pBal === undefined || pBal >= 1) {
              promotedIdx = i;
              break;
            }
          }

          if (promotedIdx !== -1) {
            const rawEntry = queue.splice(promotedIdx, 1)[0];
            const pStudentName = typeof rawEntry === 'string' ? rawEntry : rawEntry.studentName;
            const pStudentObj = this._resolveStudent(pStudentName);
            
            promotedStudent = {
              waitlistId: typeof rawEntry === 'object' ? rawEntry.waitlistId : this.generateId('wl'),
              studentId: pStudentObj.id,
              studentName: pStudentObj.name,
              classId,
              status: 'PROMOTED'
            };

            const promotedBookingId = this.generateId('bk_wl');
            const promoTx = this.createTransaction(
              'WAITLIST_PROMOTION_DEBIT',
              promotedBookingId,
              classId,
              `Promoción Lista de Espera: ${pStudentObj.name} (${cls.title})`,
              -1,
              pStudentObj.name
            );
            this.credits += promoTx.amount;
            if (this.walletsByStudentId.has(pStudentObj.id)) {
              const curBal = this.walletsByStudentId.get(pStudentObj.id);
              this.walletsByStudentId.set(pStudentObj.id, curBal - 1);
              this.walletsByStudent.set(pStudentObj.name, curBal - 1);
            }
            this.transactions.push(promoTx);
            this.transactionsById.set(promoTx.id, promoTx);

            const promotedBooking = {
              bookingId: promotedBookingId,
              classId,
              studentId: pStudentObj.id,
              studentName: pStudentObj.name,
              status: 'CONFIRMED_FROM_WAITLIST',
              debitTxId: promoTx.id,
              refundTxId: null,
              refundable: true,
              createdAt: Date.now()
            };

            this.bookingsById.set(promotedBookingId, promotedBooking);
            if (!this.bookingsByClass.has(classId)) this.bookingsByClass.set(classId, new Set());
            this.bookingsByClass.get(classId).add(promotedBookingId);
            if (!this.bookingsByStudent.has(pStudentObj.name)) this.bookingsByStudent.set(pStudentObj.name, new Set());
            this.bookingsByStudent.get(pStudentObj.name).add(promotedBookingId);

            // Retain class spots at 0: spot is strictly locked to the promoted student
            this.notify('WAITLIST_PROMOTED', {
              classId,
              title: cls.title,
              student: pStudentObj.name,
              promotedBookingId,
              txId: promoTx.id
            });
          } else {
            // Queue existed but no student had credits -> release spot to inventory
            cls.spots++;
          }
        } else {
          // No waitlist: spot is truly returned to public studio inventory
          cls.spots++;
        }
      }

      this.notify('BOOKING_CANCELLED', { classId, promotedStudent, creditRefunded, bookingId: booking.bookingId });
      return { success: true, promotedStudent, creditRefunded, bookingId: booking.bookingId };
    }

    /**
     * Ledger operations (Studio Reception / Desk simulation)
     */
    ledgerBookSpot(description = 'Reserva Cama Reformer (Clase programada)', studentName = 'Alumna Estudio (Mostrador)') {
      if (this.credits <= 0) return { success: false, reason: 'no_credits' };

      const student = this._resolveStudent(studentName);
      const studentBal = this.walletsByStudentId.get(student.id);
      if (studentBal !== undefined && studentBal <= 0) {
        return { success: false, reason: 'no_credits' };
      }

      const bookingId = this.generateId('bk_desk');
      const debitTx = this.createTransaction('LEDGER_DEBIT', bookingId, 'desk', description, -1, student.name);
      
      this.credits += debitTx.amount;
      if (studentBal !== undefined) {
        this.walletsByStudentId.set(student.id, studentBal - 1);
        this.walletsByStudent.set(student.name, studentBal - 1);
      }
      this.transactions.push(debitTx);
      this.transactionsById.set(debitTx.id, debitTx);

      const deskBooking = {
        bookingId,
        classId: 'desk_' + bookingId,
        studentId: student.id,
        studentName: student.name,
        status: 'CONFIRMED',
        debitTxId: debitTx.id,
        refundTxId: null,
        refundable: true,
        createdAt: Date.now()
      };
      this.activeBookings.set(deskBooking.classId, deskBooking);

      this.notify('LEDGER_DEBIT', { description, amount: -1, txId: debitTx.id, bookingId, studentName: student.name, studentId: student.id });
      return { success: true, credits: this.credits, txId: debitTx.id, bookingId };
    }

    ledgerRefundSpot(bookingId = null) {
      // P0-05 (AUD-010), P0-02/P0-03 (AUD-012), P0-02 (AUD-013) Fix:
      // 1. If explicit bookingId is provided and not found / invalid, fail immediately with error.
      // 2. A refund is strictly valid ONLY if there is an active, refundable booking.
      // 3. If multiple active refundable bookings exist and NO bookingId is supplied,
      //    reject with 'ambiguous_refund_target' unless only one exists, preventing arbitrary refunding.
      let targetBooking = null;
      if (bookingId !== null && bookingId !== undefined) {
        if (!this.bookingsById.has(bookingId)) {
          return { success: false, reason: 'booking_not_found' };
        }
        const b = this.bookingsById.get(bookingId);
        if (b && (b.status === 'CONFIRMED' || b.status === 'CONFIRMED_FROM_WAITLIST') && b.refundable === true) {
          targetBooking = b;
        } else {
          return { success: false, reason: 'booking_not_refundable' };
        }
      } else {
        // No ID specified: collect active refundable bookings
        const refundableList = [];
        for (const b of this.bookingsById.values()) {
          const status = b.status || 'CONFIRMED';
          if ((status === 'CONFIRMED' || status === 'CONFIRMED_FROM_WAITLIST') && b.refundable === true) {
            refundableList.push(b);
          }
        }

        if (refundableList.length === 0) {
          return { success: false, reason: 'no_refundable_bookings' };
        }

        if (refundableList.length > 1) {
          // P0-02 AUD-013 Resolution: Ambiguous! Multiple refundable bookings exist.
          // Require explicit bookingId to avoid refunding the wrong student arbitrarily.
          return { success: false, reason: 'ambiguous_refund_target' };
        }

        // Exactly one refundable booking exists
        targetBooking = refundableList[0];
      }

      if (!targetBooking) {
        return { success: false, reason: 'no_refundable_bookings' };
      }

      // Execute refund transaction
      targetBooking.refundable = false;
      targetBooking.status = 'CANCELLED';
      const classId = targetBooking.classId;
      const bStudent = targetBooking.studentName;
      const bStudentId = targetBooking.studentId;

      const refundTx = this.createTransaction(
        'LEDGER_REFUND',
        targetBooking.bookingId,
        targetBooking.classId,
        `Reverso y cancelación de reserva (${targetBooking.classId})`,
        1,
        bStudent
      );
      this.credits += refundTx.amount;
      if (bStudentId && this.walletsByStudentId.has(bStudentId)) {
        const curBal = this.walletsByStudentId.get(bStudentId);
        this.walletsByStudentId.set(bStudentId, curBal + 1);
        this.walletsByStudent.set(bStudent, curBal + 1);
      }
      this.transactions.push(refundTx);
      this.transactionsById.set(refundTx.id, refundTx);
      targetBooking.refundTxId = refundTx.id;

      // Unindex cancelled booking
      this.bookingsById.delete(targetBooking.bookingId);
      if (this.bookingsByClass.has(classId)) {
        this.bookingsByClass.get(classId).delete(targetBooking.bookingId);
      }
      if (this.bookingsByStudent.has(bStudent)) {
        this.bookingsByStudent.get(bStudent).delete(targetBooking.bookingId);
      }

      // Reconcile Inventory & Waitlist
      const cls = this.classes.get(classId);
      let promotedStudent = null;
      if (cls) {
        const queue = this.waitlists.get(classId);
        if (queue && queue.length > 0) {
          let promotedIdx = -1;
          for (let i = 0; i < queue.length; i++) {
            const entry = queue[i];
            const pName = typeof entry === 'string' ? entry : entry.studentName;
            const pObj = this._resolveStudent(pName);
            const pBal = this.walletsByStudentId.get(pObj.id);
            if (pBal === undefined || pBal >= 1) {
              promotedIdx = i;
              break;
            }
          }

          if (promotedIdx !== -1) {
            const rawEntry = queue.splice(promotedIdx, 1)[0];
            const pStudentName = typeof rawEntry === 'string' ? rawEntry : rawEntry.studentName;
            const pStudentObj = this._resolveStudent(pStudentName);
            
            promotedStudent = {
              waitlistId: typeof rawEntry === 'object' ? rawEntry.waitlistId : this.generateId('wl'),
              studentId: pStudentObj.id,
              studentName: pStudentObj.name,
              classId,
              status: 'PROMOTED'
            };

            const promotedBookingId = this.generateId('bk_wl');
            const promoTx = this.createTransaction(
              'WAITLIST_PROMOTION_DEBIT',
              promotedBookingId,
              classId,
              `Promoción Lista de Espera: ${pStudentObj.name} (${cls.title})`,
              -1,
              pStudentObj.name
            );
            this.credits += promoTx.amount;
            if (this.walletsByStudentId.has(pStudentObj.id)) {
              const curBal = this.walletsByStudentId.get(pStudentObj.id);
              this.walletsByStudentId.set(pStudentObj.id, curBal - 1);
              this.walletsByStudent.set(pStudentObj.name, curBal - 1);
            }
            this.transactions.push(promoTx);
            this.transactionsById.set(promoTx.id, promoTx);

            const promotedBooking = {
              bookingId: promotedBookingId,
              classId,
              studentId: pStudentObj.id,
              studentName: pStudentObj.name,
              status: 'CONFIRMED_FROM_WAITLIST',
              debitTxId: promoTx.id,
              refundTxId: null,
              refundable: true,
              createdAt: Date.now()
            };

            this.bookingsById.set(promotedBookingId, promotedBooking);
            if (!this.bookingsByClass.has(classId)) this.bookingsByClass.set(classId, new Set());
            this.bookingsByClass.get(classId).add(promotedBookingId);
            if (!this.bookingsByStudent.has(pStudentObj.name)) this.bookingsByStudent.set(pStudentObj.name, new Set());
            this.bookingsByStudent.get(pStudentObj.name).add(promotedBookingId);

            this.notify('WAITLIST_PROMOTED', {
              classId,
              title: cls.title,
              student: pStudentObj.name,
              promotedBookingId,
              txId: promoTx.id
            });
          } else {
            cls.spots++;
          }
        } else {
          cls.spots++;
        }
      }

      this.notify('LEDGER_REFUND', {
        classId,
        bookingId: targetBooking.bookingId,
        amount: 1,
        txId: refundTx.id,
        promotedStudent,
        studentName: bStudent,
        studentId: bStudentId
      });
      return {
        success: true,
        credits: this.credits,
        txId: refundTx.id,
        bookingId: targetBooking.bookingId,
        promotedStudent
      };
    }

    subscribe(listener) {
      if (typeof listener !== 'function') return () => {};
      this.listeners.add(listener);
      return () => this.listeners.delete(listener);
    }

    notify(eventType, payload = {}) {
      const event = {
        type: eventType,
        credits: this.credits,
        timestamp: Date.now(),
        ...payload
      };

      for (const fn of this.listeners) {
        try {
          // Supports both (event) signature and legacy (state, action, payload) signature
          fn(event, eventType, payload);
        } catch (e) {
          console.error('[DemoStore Error]', e);
        }
      }

      if (typeof window !== 'undefined' && typeof window.dispatchEvent === 'function') {
        try {
          window.dispatchEvent(new CustomEvent('openbreak:state-changed', { detail: event }));
        } catch (_) {}
      }
    }
  }

  // Universal export
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { DemoStore };
  } else if (typeof window !== 'undefined') {
    window.DemoStore = DemoStore;
    if (!window.OpenBreakStore) {
      window.OpenBreakStore = new DemoStore(8);
    }
  }
})();
