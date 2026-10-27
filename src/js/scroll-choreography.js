// UX-05 / UX-09 Cinematic Scroll Observer (Reversible, Smooth & Reduced-Motion Safe)
    function initScrollCinematicObserver() {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.querySelectorAll('.scroll-reveal-item').forEach(el => el.classList.add('is-revealed'));
        return;
      }

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-revealed');
          } else if (entry.boundingClientRect.top > window.innerHeight) {
            // Reversible when scrolling back up
            entry.target.classList.remove('is-revealed');
          }
        });
      }, {
        threshold: 0.15,
        rootMargin: '0px 0px -40px 0px'
      });

      document.querySelectorAll('.scroll-reveal-item').forEach(el => observer.observe(el));
    }

    window.addEventListener('DOMContentLoaded', () => {
      initScrollCinematicObserver();
    });

    // UX-05 Melius-Grade Sticky Scrubber: Maps scroll progress directly to 3D deck stack & satellites
    function initMeliusStickyScrubber() {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      const stage = document.getElementById('solucion');
      const bar = document.getElementById('scrubberProgressBar');
      const indicator = document.getElementById('scrubberStepIndicator');
      if (!stage || !bar || !indicator) return;

      const steps = [
        "01 / RESERVA COORDINADA",
        "02 / LISTA DE ESPERA INTELIGENTE",
        "03 / LEDGER INMUTABLE DE CRÉDITOS",
        "04 / 0% COMISIÓN ABIERTA"
      ];

      let lastIdx = -1;

      window.addEventListener('scroll', () => {
        const rect = stage.getBoundingClientRect();
        const stageHeight = stage.offsetHeight - window.innerHeight;
        if (stageHeight <= 0) return;

        // Progress from 0.0 to 1.0 while passing through sticky stage
        const scrollDist = -rect.top;
        const progress = Math.max(0, Math.min(1, scrollDist / stageHeight));
        bar.style.width = (progress * 100) + '%';

        // Map progress to 4 discreet steps (0, 1, 2, 3)
        const stepIdx = Math.min(3, Math.floor(progress * 4));
        indicator.textContent = steps[stepIdx];

        if (stepIdx !== lastIdx) {
          lastIdx = stepIdx;
          if (typeof selectDeckCard === 'function') {
            selectDeckCard(stepIdx);
          }
        }
      }, { passive: true });
    }

    window.addEventListener('DOMContentLoaded', () => {
      initMeliusStickyScrubber();
    });

    // UX-16: Accessible Screen Reader Live Announcer
    function announceToScreenReader(message) {
      const announcer = document.getElementById('srLiveAnnouncer');
      if (!announcer) return;
      announcer.textContent = '';
      setTimeout(() => { announcer.textContent = message; }, 50);
    }
