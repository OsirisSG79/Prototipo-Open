from pathlib import Path

p = Path('/home/user/openbreak/src/js/demo-store.js')
content = p.read_text(encoding='utf-8')

old_check = """    isBooked(classId) {
      const b = this.bookingsByClass.get(classId);
      return !!b && (b.status === 'CONFIRMED' || b.status === 'CONFIRMED_FROM_WAITLIST');
    }"""

new_check = """    isBooked(classId, studentName = 'Camila Morales') {
      const b = this.bookingsByClass.get(classId);
      return !!b && (b.status === 'CONFIRMED' || b.status === 'CONFIRMED_FROM_WAITLIST') && b.studentName === studentName;
    }"""

assert old_check in content
content = content.replace(old_check, new_check)

old_book_call = """      if (this.isBooked(classId)) {
        return { success: false, reason: 'already_booked' };
      }"""

new_book_call = """      if (this.isBooked(classId, studentName)) {
        return { success: false, reason: 'already_booked' };
      }"""

assert old_book_call in content
content = content.replace(old_book_call, new_book_call)

p.write_text(content, encoding='utf-8')
print("Fixed isBooked check in DemoStore!")
