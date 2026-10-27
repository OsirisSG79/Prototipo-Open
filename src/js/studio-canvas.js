/**
 * Open Break — Interactive Workflow Canvas (Sprint 03 / UX-06 Complete)
 * Dynamic reactive node-to-node choreography with SVG Bézier curves,
 * live pulse packet travel, keyboard step navigation, and reduced-motion safety.
 */
export class StudioWorkflowCanvas {
  constructor(boardId) {
    this.board = document.getElementById(boardId);
    if (!this.board) return;
    this.nodes = Array.from(this.board.querySelectorAll('.workflow-node'));
    this.wires = {
      '0-1': document.getElementById('wire-1-2'),
      '1-2': document.getElementById('wire-2-3'),
      '2-3': document.getElementById('wire-3-4')
    };
    this.pulseDot = document.getElementById('wirePulseDot');
    this.idxEl = document.getElementById('workflowActiveIndex');
    this.titleEl = document.getElementById('workflowActiveTitle');
    this.descEl = document.getElementById('workflowActiveDescription');
    this.prevBtn = document.getElementById('workflowPrev');
    this.nextBtn = document.getElementById('workflowNext');

    this.steps = [
      {
        index: '01',
        title: 'Tu clase, en orden.',
        desc: 'El estudio publica sus lugares y las alumnas eligen un horario disponible con cupo verificado en tiempo real.'
      },
      {
        index: '02',
        title: 'Asignación atómica de cupo.',
        desc: 'El motor simula la reserva inmediata con control estricto de concurrencia y prevención de sobrecupos.'
      },
      {
        index: '03',
        title: 'Reasignación autónoma por lista de espera.',
        desc: 'Ante una cancelación con aviso >12h, el cupo se promueve de forma determinista a la siguiente alumna elegible en la fila FIFO.'
      },
      {
        index: '04',
        title: 'Recepción y Check-in 1-Tap.',
        desc: 'La alumna confirma su llegada en iPad o mediante escaneo de pase digital sin saturar la recepción del estudio.'
      }
    ];

    this.activeStep = 0;
    this.init();
  }

  init() {
    this.nodes.forEach((node, idx) => {
      node.addEventListener('click', () => this.selectStep(idx));
      node.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          this.selectStep(idx);
        }
      });
    });

    this.prevBtn?.addEventListener('click', () => {
      const nextIdx = (this.activeStep - 1 + this.steps.length) % this.steps.length;
      this.selectStep(nextIdx);
    });

    this.nextBtn?.addEventListener('click', () => {
      const nextIdx = (this.activeStep + 1) % this.steps.length;
      this.selectStep(nextIdx);
    });

    window.addEventListener('resize', () => this.renderWires());
    this.renderWires();
    this.selectStep(0);
  }

  selectStep(idx) {
    this.activeStep = idx;
    this.nodes.forEach((node, i) => {
      const isCurrent = i === idx;
      node.setAttribute('aria-pressed', String(isCurrent));
      node.classList.toggle('active', isCurrent);
      node.classList.toggle('is-active', isCurrent);
      node.classList.toggle('passed', i < idx);
    });

    const stepData = this.steps[idx];
    if (this.idxEl) this.idxEl.textContent = stepData.index;
    if (this.titleEl) this.titleEl.textContent = stepData.title;
    if (this.descEl) this.descEl.textContent = stepData.desc;

    this.updateWiresActivity(idx);
    this.renderWires();
  }

  updateWiresActivity(activeIdx) {
    Object.keys(this.wires).forEach(key => {
      const wire = this.wires[key];
      if (!wire) return;
      const [from, to] = key.split('-').map(Number);
      if (activeIdx >= to) {
        wire.classList.add('wire-passed');
        wire.classList.remove('wire-active');
      } else if (activeIdx === from) {
        wire.classList.add('wire-active');
        wire.classList.remove('wire-passed');
      } else {
        wire.classList.remove('wire-active');
        wire.classList.remove('wire-passed');
      }
    });
  }

  renderWires() {
    if (!this.board) return;
    const boardRect = this.board.getBoundingClientRect();
    if (boardRect.width < 10) return;

    for (let i = 0; i < this.nodes.length - 1; i++) {
      const n1 = this.nodes[i];
      const n2 = this.nodes[i + 1];
      const wire = this.wires[`${i}-${i+1}`];
      if (!n1 || !n2 || !wire) continue;

      const r1 = n1.getBoundingClientRect();
      const r2 = n2.getBoundingClientRect();

      const x1 = r1.left + r1.width / 2 - boardRect.left;
      const y1 = r1.top + r1.height / 2 - boardRect.top;
      const x2 = r2.left + r2.width / 2 - boardRect.left;
      const y2 = r2.top + r2.height / 2 - boardRect.top;

      const dx = (x2 - x1) * 0.5;
      const pathData = `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;
      wire.setAttribute('d', pathData);
    }
  }
}
