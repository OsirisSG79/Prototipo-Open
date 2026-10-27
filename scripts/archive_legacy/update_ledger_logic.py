from pathlib import Path

path = Path('/home/user/openbreak/templates/part4_js_logic.html')
content = path.read_text(encoding='utf-8')

idx_start = content.find('// 7. DEMO 3: LEDGER INMUTABLE')
idx_end = content.find('// 8. DEMO 4: CHECK-IN QR')

assert idx_start != -1 and idx_end != -1, "Ledger markers not found"

new_ledger_block = """// 7. DEMO 3: LEDGER INMUTABLE (V7-01 fix: Delegated directly to window.OpenBreakStore)
    function addLedgerMovement(type) {
      const store = window.OpenBreakStore;
      const display = document.getElementById('creditsDisplay');
      const list = document.getElementById('ledgerHistory');
      const warning = document.getElementById('ledgerWarning');
      if (!list) return;

      const item = document.createElement('div');
      item.className = 'ledger-item';

      if (type === 'book') {
        if (store) {
          const res = store.ledgerBookSpot();
          if (!res.success) return;
        } else {
          window.credits--;
        }
        if (display) display.textContent = (store ? store.credits : window.credits) + ' CR';
        item.innerHTML = '<span>Reserva Cama Reformer (Clase programada)</span><span style="color: #EF4444; font-family: var(--font-mono); font-weight: 700;">-1 CR</span>';
        list.prepend(item);
        if (warning) warning.style.display = 'none';
      } else if (type === 'refund') {
        if (store) {
          const res = store.ledgerRefundSpot();
          if (!res.success) {
            if (warning) {
              warning.style.display = 'block';
              setTimeout(() => { warning.style.display = 'none'; }, 4000);
            }
            return;
          }
        } else {
          window.credits++;
        }
        if (display) display.textContent = (store ? store.credits : window.credits) + ' CR';
        item.innerHTML = '<span>Reverso de Reserva (Aviso >12h)</span><span style="color: var(--accent-green); font-family: var(--font-mono); font-weight: 700;">+1 CR</span>';
        list.prepend(item);
        if (warning) warning.style.display = 'none';
      }
    }

    """

content = content[:idx_start] + new_ledger_block + content[idx_end:]
path.write_text(content, encoding='utf-8')
print("Ledger block replaced cleanly in part4_js_logic.html")
