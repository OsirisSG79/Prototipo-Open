from pathlib import Path

p = Path('/home/user/openbreak/templates/part4_js_logic.html')
content = p.read_text(encoding='utf-8')

# Wire announceToScreenReader into selectDeckCard, addLedgerMovement, handleDemoSubmit, etc.
old_deck_select = """      updateDeckWires(idx);
    }"""

new_deck_select = """      updateDeckWires(idx);
      const titles = ["Reserva coordinada", "Lista de espera inteligente", "Ledger de Créditos", "0% Comisión Open Break"];
      if (typeof announceToScreenReader === 'function') {
        announceToScreenReader(`Pilar seleccionado: ${titles[idx] || 'Solución Open Break'}`);
      }
    }"""

if old_deck_select in content and "Pilar seleccionado:" not in content:
    content = content.replace(old_deck_select, new_deck_select)
    print("Wired announceToScreenReader into selectDeckCard")

old_ledger = """      renderLedgerHistory();
    }"""

new_ledger = """      renderLedgerHistory();
      if (typeof announceToScreenReader === 'function') {
        announceToScreenReader(`Transacción contable registrada: ${type === 'book' ? 'Reserva -1 crédito' : 'Reverso +1 crédito'}. Saldo actual: ${store.credits} créditos.`);
      }
    }"""

if old_ledger in content and "Transacción contable registrada:" not in content:
    content = content.replace(old_ledger, new_ledger, 1)
    print("Wired announceToScreenReader into addLedgerMovement")

p.write_text(content, encoding='utf-8')
print("Successfully wired live announcements into core interactions.")
