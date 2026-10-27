from pathlib import Path

p = Path('/home/user/openbreak/templates/part3_body_sections.html')
content = p.read_text(encoding='utf-8')

old_header = """      <div class="pricing-header">
        <div class="section-eyebrow">Sin Cargos Ocultos</div>
        <h2 class="section-heading">Suscripción fija mensual. Sin comisión adicional propia.</h2>
        <p class="section-subtext">Tu dinero entra íntegro a tu cuenta de banco. Open Break no descuenta comisión porcentual de tus ventas.</p>
      </div>"""

new_header = """      <div class="pricing-header">
        <div class="section-eyebrow">Sin Cargos Ocultos</div>
        <h2 class="section-heading">Suscripción fija. Sin comisión adicional propia.</h2>
        <p class="section-subtext">Tu dinero entra íntegro a tu cuenta de banco. Open Break no descuenta comisión porcentual de tus ventas.</p>
        
        <!-- Toggle Anual / Mensual con descuento visible -->
        <div style="display: flex; justify-content: center; align-items: center; gap: 12px; margin-top: 24px;">
          <span style="font-size: 0.82rem; font-weight: 600; color: var(--text-black);" id="billingLabelMonthly">Facturación Mensual</span>
          <button type="button" onclick="toggleBillingCycle()" id="billingToggleBtn" role="switch" aria-checked="false" style="width: 48px; height: 26px; background: #E4E4E7; border-radius: 100px; border: none; position: relative; cursor: pointer; padding: 2px; transition: background 0.3s ease;" aria-label="Alternar entre facturación mensual y anual">
            <span id="billingToggleKnob" style="display: block; width: 22px; height: 22px; background: #FFF; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.15); transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);"></span>
          </button>
          <span style="font-size: 0.82rem; font-weight: 600; color: var(--text-editorial); display: inline-flex; align-items: center; gap: 6px;" id="billingLabelAnnual">
            Facturación Anual <span style="background: rgba(16, 185, 129, 0.12); color: var(--accent-green); font-size: 0.68rem; font-weight: 700; padding: 2px 6px; border-radius: 4px;">Ahorra 20%</span>
          </span>
        </div>
      </div>"""

assert old_header in content, "old_header not found in part3_body_sections.html"
content = content.replace(old_header, new_header)

old_card1 = """            <div class="pricing-price">$1,890 <span>MXN/mes · propuesto</span></div>"""
new_card1 = """            <div class="pricing-price" id="planPriceSolo">$1,890 <span id="planPeriodSolo">MXN/mes · propuesto</span></div>"""

old_card2 = """            <div class="pricing-price">$3,490 <span>MXN/mes · propuesto</span></div>"""
new_card2 = """            <div class="pricing-price" id="planPriceMulti">$3,490 <span id="planPeriodMulti">MXN/mes · propuesto</span></div>"""

assert old_card1 in content and old_card2 in content, "Pricing card prices not found"
content = content.replace(old_card1, new_card1).replace(old_card2, new_card2)

p.write_text(content, encoding='utf-8')
print("Successfully added billing toggle and dynamic IDs to pricing section HTML")

# Add toggleBillingCycle function to part4_js_logic.html
p4 = Path('/home/user/openbreak/templates/part4_js_logic.html')
content4 = p4.read_text(encoding='utf-8')

toggle_func = """
    // Facturación dinámica Mensual vs Anual (20% de descuento)
    let isAnnualBilling = false;
    function toggleBillingCycle() {
      isAnnualBilling = !isAnnualBilling;
      const btn = document.getElementById('billingToggleBtn');
      const knob = document.getElementById('billingToggleKnob');
      const labelMonthly = document.getElementById('billingLabelMonthly');
      const labelAnnual = document.getElementById('billingLabelAnnual');
      const priceSolo = document.getElementById('planPriceSolo');
      const periodSolo = document.getElementById('planPeriodSolo');
      const priceMulti = document.getElementById('planPriceMulti');
      const periodMulti = document.getElementById('planPeriodMulti');

      if (btn) {
        btn.setAttribute('aria-checked', String(isAnnualBilling));
        btn.style.background = isAnnualBilling ? 'var(--accent-orange)' : '#E4E4E7';
      }
      if (knob) {
        knob.style.transform = isAnnualBilling ? 'translateX(22px)' : 'translateX(0)';
      }
      if (labelMonthly && labelAnnual) {
        labelMonthly.style.color = isAnnualBilling ? 'var(--text-editorial)' : 'var(--text-black)';
        labelAnnual.style.color = isAnnualBilling ? 'var(--text-black)' : 'var(--text-editorial)';
      }

      if (priceSolo && periodSolo) {
        priceSolo.childNodes[0].nodeValue = isAnnualBilling ? '$1,512 ' : '$1,890 ';
        periodSolo.textContent = isAnnualBilling ? 'MXN/mes (facturado anual)' : 'MXN/mes · propuesto';
      }
      if (priceMulti && periodMulti) {
        priceMulti.childNodes[0].nodeValue = isAnnualBilling ? '$2,792 ' : '$3,490 ';
        periodMulti.textContent = isAnnualBilling ? 'MXN/mes (facturado anual)' : 'MXN/mes · propuesto';
      }
    }
"""

content4 = content4.replace("  </script>\n</body>", toggle_func + "  </script>\n</body>")
p4.write_text(content4, encoding='utf-8')
print("Successfully added toggleBillingCycle function to part4_js_logic.html")
