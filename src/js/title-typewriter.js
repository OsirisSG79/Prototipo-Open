/**
 * Open Break — Kinetic Typography & Word Cycle (Per-Character Stagger Engine)
 * Words are split into individual span letters animated with cubic-bezier staggers.
 * Fully responsive, zero Cumulative Layout Shift (CLS), and prefers-reduced-motion compliant.
 */
(() => {
  'use strict';
  const target = document.getElementById('ob-hero-rotating-word');
  if (!target) return;

  const words = [
    'Pilates Reformer',
    'Barre & Mat',
    'Hot Yoga Flow',
    'Indoor Cycling',
    'Estudios Boutique'
  ];
  let currentIdx = 0;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  function renderWord(word, isInitial = false) {
    target.innerHTML = '';
    const letters = word.split('');
    letters.forEach((char, i) => {
      const span = document.createElement('span');
      span.className = 'kinetic-char';
      span.textContent = char === ' ' ? '\u00A0' : char;
      span.style.setProperty('--char-idx', i);
      span.style.animationDelay = `${i * 32}ms`;
      target.appendChild(span);
    });
  }

  // Initial render
  renderWord(words[currentIdx], true);

  if (reduce.matches) return;

  function rotateWord() {
    const chars = target.querySelectorAll('.kinetic-char');
    // Stagger exit
    chars.forEach((c, i) => {
      c.style.transitionDelay = `${i * 20}ms`;
      c.classList.add('char-leaving');
    });

    const exitDuration = (chars.length * 20) + 380;

    setTimeout(() => {
      currentIdx = (currentIdx + 1) % words.length;
      renderWord(words[currentIdx]);
    }, exitDuration);
  }

  const timer = setInterval(rotateWord, 3600);

  reduce.addEventListener?.('change', () => {
    if (reduce.matches) {
      clearInterval(timer);
      target.textContent = words[currentIdx];
    }
  });
})();
