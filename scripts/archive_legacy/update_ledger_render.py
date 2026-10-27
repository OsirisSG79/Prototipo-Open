from pathlib import Path

p = Path('/home/user/openbreak/templates/part4_js_logic.html')
content = p.read_text(encoding='utf-8')

old_ledger_js = """    // 7. DEMO 3: LEDGER INMUTABLE (V7-01 fix: Delegated directly to window.OpenBreakStore)
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
    }"""

new_ledger_js = """    // 7. DEMO 3: LEDGER INMUTABLE (V8.1.0: Real Transaction History & Idempotent Audit Trail)
    function renderLedgerHistory() {
      const store = window.OpenBreakStore;
      const list = document.getElementById('ledgerHistory');
      const display = document.getElementById('creditsDisplay');
      if (!list || !store) return;

      list.innerHTML = '';
      const txs = store.transactions || [];
      // Render transactions in reverse chronological order
      [...txs].reverse().forEach(tx => {
        const item = document.createElement('div');
        item.className = 'ledger-item';
        item.style.display = 'flex';
        item.style.justifyContent = 'space-between';
        item.style.alignItems = 'center';
        item.style.padding = '8px 0';
        item.style.borderBottom = '1px solid rgba(0,0,0,0.05)';

        const isPositive = tx.amount > 0;
        const color = isPositive ? 'var(--accent-green)' : '#EF4444';
        const sign = isPositive ? '+' : '';
        const txShortId = tx.id ? tx.id.slice(-8) : 'tx_demo';

        item.innerHTML = `
          <div>
            <div style="font-weight: 600; font-size: 0.85rem; color: var(--text-black);">${tx.description}</div>
            <div style="font-family: var(--font-mono); font-size: 0.65rem; color: #A1A1AA;">ID: ${txShortId} · Ref: ${tx.refBookingId || 'N/A'}</div>
          </div>
          <span style="color: ${color}; font-family: var(--font-mono); font-weight: 700; font-size: 0.88rem;">${sign}${tx.amount} CR</span>
        `;
        list.appendChild(item);
      });

      if (display) display.textContent = store.credits + ' CR';
    }

    function addLedgerMovement(type) {
      const store = window.OpenBreakStore;
      const warning = document.getElementById('ledgerWarning');
      if (!store) return;

      if (type === 'book') {
        const res = store.ledgerBookSpot();
        if (!res.success) return;
        if (warning) warning.style.display = 'none';
      } else if (type === 'refund') {
        const res = store.ledgerRefundSpot();
        if (!res.success) {
          if (warning) {
            warning.style.display = 'block';
            setTimeout(() => { warning.style.display = 'none'; }, 4000);
          }
          return;
        }
        if (warning) warning.style.display = 'none';
      }
      renderLedgerHistory();
    }

    window.addEventListener('DOMContentLoaded', () => {
      renderLedgerHistory();
    });
    window.addEventListener('openbreak:state-changed', () => {
      renderLedgerHistory();
    });"""

assert old_ledger_js in content, "old_ledger_js not found in part4_js_logic.html"
content = content.replace(old_ledger_js, new_ledger_js)
p.write_text(content, encoding='utf-8')
print("Successfully installed real transaction ledger renderer in part4_js_logic.html")
