from pathlib import Path

p = Path('/home/user/openbreak/templates/part4_js_logic.html')
content = p.read_text(encoding='utf-8')

old_form_code = """    function handleDemoSubmit(e) {
      e.preventDefault();
      const name = document.getElementById('demoName').value.trim();
      const studio = document.getElementById('demoStudio').value.trim();
      const discipline = document.getElementById('demoDiscipline').value;
      const phone = document.getElementById('demoPhone').value.trim();
      const consent = document.getElementById('demoConsent')?.checked;

      if (!consent) {
        alert('Por favor confirma tu consentimiento para ser contactado por WhatsApp.');
        return;
      }

      const submitBtn = document.getElementById('btnSubmitLead');
      const submitText = document.getElementById('btnSubmitLeadText');
      if (submitBtn) submitBtn.disabled = true;
      if (submitText) submitText.textContent = 'Verificando y enviando...';

      const leadData = {
        name,
        studio,
        discipline,
        phone,
        consentGiven: true,
        timestamp: new Date().toISOString(),
        leadId: 'lead_' + Math.random().toString(36).substr(2, 9),
        channel: 'openbreak-demo-v8'
      };

      // Mock safe API endpoint dispatch with fallback
      const dispatchPromise = window.fetch ? 
        fetch('/api/leads', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(leadData)
        }).catch(() => ({ ok: true, simulated: true })) :
        Promise.resolve({ ok: true, simulated: true });

      dispatchPromise.finally(() => {
        if (submitBtn) submitBtn.disabled = false;
        if (submitText) submitText.textContent = 'Solicitar demostración';

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
          summaryEl.innerHTML = `<strong>ID:</strong> ${leadData.leadId}<br><strong>Estudio:</strong> ${studio}<br><strong>Contacto:</strong> ${name} · ${phone}<br><strong>Disciplina:</strong> ${discipline}`;
        }
      });
    }

    function sendViaWhatsApp() {
      const lead = window.openbreakPreparedLead;
      if (!lead) return;
      const text = encodeURIComponent(`¡Hola equipo de Open Break! Me interesa una demostración para mi estudio.\\n\\n• Estudio: ${lead.studio}\\n• Contacto: ${lead.name}\\n• Disciplina: ${lead.discipline}\\n• Teléfono: ${lead.phone}`);
      window.open(`https://wa.me/525512345678?text=${text}`, '_blank', 'noopener,noreferrer');
    }"""

new_form_code = """    // P0-03 & P0-04 Fix: Secure DOM nodes (no innerHTML), explicit transmission states, zero false catch success
    async function handleDemoSubmit(e) {
      e.preventDefault();
      const nameInput = document.getElementById('demoName');
      const studioInput = document.getElementById('demoStudio');
      const disciplineInput = document.getElementById('demoDiscipline');
      const phoneInput = document.getElementById('demoPhone');
      const consentInput = document.getElementById('demoConsent');

      const name = (nameInput?.value || '').trim();
      const studio = (studioInput?.value || '').trim();
      const discipline = (disciplineInput?.value || '').trim();
      const phone = (phoneInput?.value || '').trim();
      const consent = consentInput?.checked;

      if (!consent) {
        alert('Por favor confirma tu consentimiento para ser contactado.');
        return;
      }

      // Input sanitization & length limits
      if (name.length < 2 || name.length > 80 || studio.length < 2 || studio.length > 80) {
        alert('Por favor ingresa un nombre y estudio válidos (máximo 80 caracteres).');
        return;
      }

      const submitBtn = document.getElementById('btnSubmitLead');
      const submitText = document.getElementById('btnSubmitLeadText');
      if (submitBtn) submitBtn.disabled = true;
      if (submitText) submitText.textContent = 'Enviando solicitud...';

      const leadId = 'lead_' + Date.now().toString(36) + '_' + Math.random().toString(36).substr(2, 6);
      const leadData = {
        leadId,
        name,
        studio,
        discipline,
        phone,
        consentGiven: true,
        timestamp: new Date().toISOString(),
        clientVersion: 'V8.1.1'
      };

      let statusMode = 'demo_prepared';
      let serverConfirmed = false;

      try {
        if (window.fetch && window.location.protocol.startsWith('http')) {
          const res = await fetch('/api/leads', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(leadData)
          });
          if (res.ok) {
            serverConfirmed = true;
            statusMode = 'server_confirmed';
          } else {
            statusMode = 'server_error';
          }
        } else {
          // Running in offline / file:// / static preview mode: explicitly transparent demo mode
          statusMode = 'offline_demo';
        }
      } catch (err) {
        // Network failure or backend unreachable: do NOT fake server confirmation
        statusMode = 'network_error';
      } finally {
        if (submitBtn) submitBtn.disabled = false;
        if (submitText) submitText.textContent = 'Solicitar demostración';
      }

      window.openbreakPreparedLead = leadData;
      // P1-10: Do NOT store raw phone numbers or personal PII in permanent localStorage without explicit consent
      // Instead, keep in memory on window object only for this active session.

      const formContainer = document.getElementById('modalFormContainer');
      const feedback = document.getElementById('modalFeedback');
      const summaryEl = document.getElementById('preparedLeadSummary');
      const feedbackMsg = document.getElementById('feedbackMessage');

      if (formContainer) formContainer.style.display = 'none';
      if (feedback) feedback.classList.add('active');

      if (statusMode === 'server_confirmed') {
        if (feedbackMsg) feedbackMsg.textContent = '✔ Confirmado por el servidor: Tu solicitud fue recibida formalmente por Open Break.';
      } else if (statusMode === 'server_error' || statusMode === 'network_error') {
        if (feedbackMsg) feedbackMsg.textContent = 'Nota técnica: El servidor central no está disponible en este momento. Hemos formateado tu solicitud localmente para canal directo de WhatsApp.';
      } else {
        if (feedbackMsg) feedbackMsg.textContent = 'Modo Demostración / Vista previa local: Solicitud formateada sin transmisión externa.';
      }

      // P0-04: Secure DOM node generation - ZERO innerHTML interpolation of user input
      if (summaryEl) {
        summaryEl.textContent = ''; // clear safely
        
        const rowId = document.createElement('div');
        const strongId = document.createElement('strong');
        strongId.textContent = 'ID de Solicitud: ';
        rowId.appendChild(strongId);
        rowId.appendChild(document.createTextNode(leadId));
        summaryEl.appendChild(rowId);

        const rowStudio = document.createElement('div');
        const strongStudio = document.createElement('strong');
        strongStudio.textContent = 'Estudio: ';
        rowStudio.appendChild(strongStudio);
        rowStudio.appendChild(document.createTextNode(studio));
        summaryEl.appendChild(rowStudio);

        const rowContact = document.createElement('div');
        const strongContact = document.createElement('strong');
        strongContact.textContent = 'Contacto: ';
        rowContact.appendChild(strongContact);
        rowContact.appendChild(document.createTextNode(`${name} · ${phone}`));
        summaryEl.appendChild(rowContact);

        const rowDisc = document.createElement('div');
        const strongDisc = document.createElement('strong');
        strongDisc.textContent = 'Disciplina: ';
        rowDisc.appendChild(strongDisc);
        rowDisc.appendChild(document.createTextNode(discipline));
        summaryEl.appendChild(rowDisc);
      }
    }

    function sendViaWhatsApp() {
      const lead = window.openbreakPreparedLead;
      if (!lead) return;
      const text = encodeURIComponent(`¡Hola equipo de Open Break! Me interesa una demostración para mi estudio.\\n\\n• Solicitud: ${lead.leadId}\\n• Estudio: ${lead.studio}\\n• Contacto: ${lead.name}\\n• Disciplina: ${lead.discipline}\\n• Teléfono: ${lead.phone}`);
      // P1-10: Clearly identified support inquiry link
      window.open(`https://wa.me/?text=${text}`, '_blank', 'noopener,noreferrer');
    }"""

assert old_form_code in content, "old_form_code not found in part4"
content = content.replace(old_form_code, new_form_code)
p.write_text(content, encoding='utf-8')
print("Successfully installed secure, XSS-proof form handler in part4_js_logic.html")
