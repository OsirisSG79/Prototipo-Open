/**
 * Open Break — Smooth Lerp Contextual Cursor (UX-07)
 * Runs strictly on fine pointers (mouse/trackpad), disabled on touch & reduced motion.
 * Contextual morphing states: DEFAULT, POINTER, DRAG, ORBIT (360°), EXPLORE.
 */
export class ContextualCursor {
  constructor() {
    this.cursorEl = document.getElementById('custom-cursor');
    this.cursorLabel = document.getElementById('custom-cursor-label');
    this.isEnabled = window.matchMedia('(pointer: fine) and (hover: hover)').matches &&
                     !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    this.mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
    this.pos = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
    this.lerpFactor = 0.16;
    this.state = 'DEFAULT';

    if (this.isEnabled && this.cursorEl) {
      this.init();
    } else if (this.cursorEl) {
      this.cursorEl.style.display = 'none';
    }
  }

  init() {
    window.addEventListener('mousemove', (e) => {
      this.mouse.x = e.clientX;
      this.mouse.y = e.clientY;
      if (this.cursorEl && !this.cursorEl.classList.contains('is-active')) {
        this.cursorEl.classList.add('is-active');
      }
    }, { passive: true });

    window.addEventListener('mouseleave', () => {
      if (this.cursorEl) this.cursorEl.classList.remove('is-active');
    });

    this.bindHoverElements();
    this.renderLoop();
  }

  setState(state, label = '') {
    this.state = state;
    if (!this.cursorEl) return;

    this.cursorEl.className = 'is-active';
    if (state !== 'DEFAULT') {
      this.cursorEl.classList.add(`cursor-${state.toLowerCase()}`);
    }
    if (this.cursorLabel) {
      this.cursorLabel.textContent = label;
      this.cursorLabel.style.display = label ? 'block' : 'none';
    }
  }

  bindHoverElements() {
    // Spatial Tunnel in Hero
    const tunnel = document.getElementById('obTunnel');
    if (tunnel) {
      tunnel.addEventListener('mouseenter', () => this.setState('DRAG', 'EXPLORAR'));
      tunnel.addEventListener('mouseleave', () => this.setState('DEFAULT'));
    }

    // Parabolic Ribbon
    const viewport = document.getElementById('conveyorViewport');
    if (viewport) {
      viewport.addEventListener('mouseenter', () => this.setState('DRAG', 'DRAG'));
      viewport.addEventListener('mouseleave', () => this.setState('DEFAULT'));
    }

    // 3D ORBIT over Reformer Canvas
    const reformerBox = document.getElementById('reformerCanvasContainer') || document.getElementById('reformerCanvas');
    if (reformerBox) {
      reformerBox.addEventListener('mouseenter', () => this.setState('ORBIT', '360°'));
      reformerBox.addEventListener('mouseleave', () => this.setState('DEFAULT'));
    }

    // Workflow Canvas Board
    const workflowBoard = document.getElementById('workflowBoard');
    if (workflowBoard) {
      workflowBoard.addEventListener('mouseenter', () => this.setState('POINTER', 'CONECTAR'));
      workflowBoard.addEventListener('mouseleave', () => this.setState('DEFAULT'));
    }

    // Interactive Buttons, Links & Cards
    document.querySelectorAll('button, a, .deck-satellite, .reformer-bed, .cal-day-btn, .workflow-node').forEach(el => {
      el.addEventListener('mouseenter', () => this.setState('POINTER'));
      el.addEventListener('mouseleave', () => this.setState('DEFAULT'));
    });
  }

  renderLoop() {
    this.pos.x += (this.mouse.x - this.pos.x) * this.lerpFactor;
    this.pos.y += (this.mouse.y - this.pos.y) * this.lerpFactor;

    if (this.cursorEl) {
      this.cursorEl.style.transform = `translate3d(${this.pos.x}px, ${this.pos.y}px, 0) translate(-50%, -50%)`;
    }

    requestAnimationFrame(() => this.renderLoop());
  }
}
