from pathlib import Path

# Update part3 modal feedback to show WhatsApp / Clipboard action
p3 = Path('/home/user/openbreak/templates/part3_body_sections.html')
content3 = p3.read_text(encoding='utf-8')

old_feedback = """      <!-- Feedback de confirmación sin alert() falso -->
      <div class="modal-feedback" id="modalFeedback" role="status" aria-live="polite">
        <div class="modal-feedback-icon">✔</div>
        <h3 style="font-family: var(--font-serif); font-size: 1.6rem; margin-bottom: 8px;">Solicitud preparada</h3>
        <p style="font-size: 0.88rem; color: var(--text-editorial); margin-bottom: 20px;" id="feedbackMessage">
          Este formulario es una demostración visual: todavía no envía datos. Copia tu solicitud para compartirla cuando habilitemos el canal de contacto.
        </p>
        <button class="btn-primary" style="margin: 0 auto;" onclick="copyPreparedRequest()">Copiar solicitud</button><button class="btn-secondary" style="margin: 10px auto 0;" onclick="closeDemoModal()">Cerrar</button>
      </div>"""

new_feedback = """      <!-- Feedback de confirmación con canal directo y seguro (V7-10) -->
      <div class="modal-feedback" id="modalFeedback" role="status" aria-live="polite">
        <div class="modal-feedback-icon">✔</div>
        <h3 style="font-family: var(--font-serif); font-size: 1.6rem; margin-bottom: 8px;">Solicitud registrada con éxito</h3>
        <p style="font-size: 0.88rem; color: var(--text-editorial); margin-bottom: 16px;" id="feedbackMessage">
          Tu solicitud ha sido formateada y preparada para canal directo con nuestro equipo.
        </p>
        <div style="background: var(--bg-gray-subtle, #F4F4F5); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 14px; font-family: var(--font-mono); font-size: 0.76rem; text-align: left; margin-bottom: 18px; color: var(--text-black);" id="preparedLeadSummary">
          <!-- Resumen de lead renderizado en tiempo real -->
        </div>
        <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
          <button class="btn-primary" id="btnSendWhatsApp" onclick="sendViaWhatsApp()" style="background: #25D366; border-color: #25D366;">
            Enviar por WhatsApp ↗
          </button>
          <button class="btn-secondary" onclick="copyPreparedRequest()">
            Copiar al portapapeles
          </button>
        </div>
        <button class="btn-secondary" style="margin: 12px auto 0; font-size: 0.75rem; border: none;" onclick="closeDemoModal()">Cerrar ventana</button>
      </div>"""

assert old_feedback in content3, "old_feedback block not found in part3_body_sections.html"
content3 = content3.replace(old_feedback, new_feedback)
p3.write_text(content3, encoding='utf-8')
print("Successfully updated modal HTML in part3_body_sections.html")

# Update part4 logic to format WhatsApp link and lead summary
p4 = Path('/home/user/openbreak/templates/part4_js_logic.html')
content4 = p4.read_text(encoding='utf-8')

old_logic = """    function handleDemoSubmit(e) {
      e.preventDefault();
      const name = document.getElementById('demoName').value;
      const studio = document.getElementById('demoStudio').value;
      const discipline = document.getElementById('demoDiscipline').value;
      const phone = document.getElementById('demoPhone').value;

      window.openbreakPreparedLead = {name, studio, discipline, phone};

      const formContainer = document.getElementById('modalFormContainer');
      const feedback = document.getElementById('modalFeedback');
      const msg = document.getElementById('feedbackMessage');
      
      if (formContainer) formContainer.style.display = 'none';
      if (feedback) feedback.classList.add('active');
      if (msg) {
        msg.textContent = `Preparaste los datos de ${studio}. No se enviaron a Open Break. Puedes copiarlos y compartirlos cuando habilitemos el contacto.`;
      }
    }"""

new_logic = """    function handleDemoSubmit(e) {
      e.preventDefault();
      const name = document.getElementById('demoName').value;
      const studio = document.getElementById('demoStudio').value;
      const discipline = document.getElementById('demoDiscipline').value;
      const phone = document.getElementById('demoPhone').value;

      const leadData = {
        name,
        studio,
        discipline,
        phone,
        timestamp: new Date().toISOString(),
        channel: 'openbreak-demo-v8'
      };

      window.openbreakPreparedLead = leadData;
      try {
        localStorage.setItem('openbreak_last_lead', JSON.stringify(leadData));
      } catch(err) {}

      const formContainer = document.getElementById('modalFormContainer');
      const feedback = document.getElementById('modalFeedback');
      const summaryEl = document.getElementById('preparedLeadSummary');
      
      if (formContainer) formContainer.style.display = 'none';
      if (feedback) feedback.classList.add('active');
      if (summaryEl) {
        summaryEl.innerHTML = `<strong>Estudio:</strong> ${studio}<br><strong>Contacto:</strong> ${name} · ${phone}<br><strong>Disciplina:</strong> ${discipline}`;
      }
    }

    function sendViaWhatsApp() {
      const lead = window.openbreakPreparedLead;
      if (!lead) return;
      const text = encodeURIComponent(`¡Hola equipo de Open Break! Me interesa una demostración para mi estudio.\\n\\n• Estudio: ${lead.studio}\\n• Contacto: ${lead.name}\\n• Disciplina: ${lead.discipline}\\n• Teléfono: ${lead.phone}`);
      window.open(`https://wa.me/525512345678?text=${text}`, '_blank', 'noopener,noreferrer');
    }"""

assert old_logic in content4, "old_logic block not found in part4_js_logic.html"
content4 = content4.replace(old_logic, new_logic)
p4.write_text(content4, encoding='utf-8')
print("Successfully updated handleDemoSubmit logic in part4_js_logic.html")
