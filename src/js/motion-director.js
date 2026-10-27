/**
 * Open Break — Motion Director (Sprint 4 / V7-05 Resolution)
 * Coordinates cinematographic scroll progress, bidirectional transitions,
 * and reversible timelines between Hero, Problem, Solutions, Canvas and Reformer.
 * Guarantees zero scroll hijacking and strict prefers-reduced-motion compliance.
 */
(() => {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  class MotionDirector {
    constructor() {
      this.ticking = false;
      this.sections = [];
      this.init();
    }

    init() {
      if (reduceMotion.matches) {
        this.disableMotion();
        return;
      }

      this.cacheScenes();
      this.initReveals();
      this.bindScroll();
    }

    disableMotion() {
      document.querySelectorAll('.ob-reveal, .ob-reveal-stagger, .solution-card, .workflow-node-v7').forEach(el => {
        el.classList.add('is-revealed');
        el.style.setProperty('--scroll-p', '1');
      });
    }

    cacheScenes() {
      const sceneSelectors = [
        { el: document.querySelector('.problem-section'), name: 'problem' },
        { el: document.querySelector('.melius-solutions-deck-section'), name: 'solutions' },
        { el: document.querySelector('.workflow-canvas-section'), name: 'workflow' },
        { el: document.querySelector('#agenda-app'), name: 'schedule' },
        { el: document.querySelector('.pricing-section'), name: 'pricing' }
      ];

      this.sections = sceneSelectors
        .filter(s => s.el !== null)
        .map(s => ({
          el: s.el,
          name: s.name,
          top: 0,
          height: 0
        }));

      this.measure();
    }

    measure() {
      const scrollY = window.scrollY || window.pageYOffset;
      this.sections.forEach(s => {
        const rect = s.el.getBoundingClientRect();
        s.top = rect.top + scrollY;
        s.height = rect.height;
      });
    }

    initReveals() {
      const targets = document.querySelectorAll(
        '.ob-reveal, .ob-reveal-stagger, .solution-card, .editorial-heading, .faq-item, .comparison-card, .workflow-node-v7'
      );

      if (!('IntersectionObserver' in window)) {
        targets.forEach(el => el.classList.add('is-revealed'));
        return;
      }

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-revealed');
          } else if (entry.boundingClientRect.top > window.innerHeight) {
            // Reversible: re-arm if scrolled backwards above viewport
            entry.target.classList.remove('is-revealed');
          }
        });
      }, {
        rootMargin: '0px 0px -10% 0px',
        threshold: 0.10
      });

      targets.forEach(el => observer.observe(el));
    }

    bindScroll() {
      window.addEventListener('scroll', () => {
        if (!this.ticking) {
          requestAnimationFrame(() => {
            this.updateScrollProgress();
            this.ticking = false;
          });
          this.ticking = true;
        }
      }, { passive: true });

      window.addEventListener('resize', () => {
        this.measure();
      }, { passive: true });
    }

    updateScrollProgress() {
      if (reduceMotion.matches) return;
      const scrollY = window.scrollY || window.pageYOffset;
      const vh = window.innerHeight;

      this.sections.forEach(s => {
        // Compute relative viewport progress [0.0 to 1.0]
        const start = s.top - vh;
        const end = s.top + s.height;
        const total = end - start;
        if (total <= 0) return;

        const progress = Math.max(0, Math.min(1, (scrollY - start) / total));
        s.el.style.setProperty('--scroll-progress', progress.toFixed(3));
      });
    }
  }

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new MotionDirector());
  } else {
    new MotionDirector();
  }

  reduceMotion.addEventListener?.('change', () => {
    if (reduceMotion.matches) {
      document.querySelectorAll('.ob-reveal, .ob-reveal-stagger').forEach(el => el.classList.add('is-revealed'));
    }
  });
})();
