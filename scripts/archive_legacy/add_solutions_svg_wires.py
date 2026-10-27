from pathlib import Path

# 1. Update HTML in part3_body_sections.html to add the reactive SVG wire canvas
p_body = Path('/home/user/openbreak/templates/part3_body_sections.html')
content_body = p_body.read_text(encoding='utf-8')

old_arena_start = """    <div class="solutions-deck-arena">
      <!-- Satélites como botones accesibles (OB-11) -->"""

new_arena_start = """    <div class="solutions-deck-arena" id="solutionsDeckArena">
      <!-- UX-06 / Melius Standard: SVG Reactive Bézier Wires linking Satellites to Central Stack -->
      <svg class="deck-wires-canvas" id="deckWiresCanvas" aria-hidden="true">
        <path id="wire-0" class="deck-wire-path" d="" />
        <path id="wire-1" class="deck-wire-path" d="" />
        <path id="wire-2" class="deck-wire-path" d="" />
        <path id="wire-3" class="deck-wire-path" d="" />
      </svg>

      <!-- Satélites como botones accesibles (OB-11) -->"""

if old_arena_start in content_body:
    content_body = content_body.replace(old_arena_start, new_arena_start)
    p_body.write_text(content_body, encoding='utf-8')
    print("Added SVG wire canvas to part3_body_sections.html")
else:
    print("Warning: old_arena_start not found in part3_body_sections.html")

# 2. Add styles in part2_css_rest.html for .deck-wires-canvas and .deck-wire-path
p_css = Path('/home/user/openbreak/templates/part2_css_rest.html')
content_css = p_css.read_text(encoding='utf-8')

wire_css = """    .deck-wires-canvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 5;
    }
    .deck-wire-path {
      fill: none;
      stroke: rgba(255, 255, 255, 0.12);
      stroke-width: 1.5;
      stroke-dasharray: 4 4;
      transition: stroke 0.4s ease, stroke-width 0.4s ease, filter 0.4s ease;
    }
    .deck-wire-path.active {
      stroke: var(--accent-green);
      stroke-width: 2.5;
      stroke-dasharray: none;
      filter: drop-shadow(0 0 6px rgba(0, 240, 150, 0.45));
    }
    @media (max-width: 900px) {
      .deck-wires-canvas { display: none; }
    }
"""

if "/* DECK WIRES CANVAS */" not in content_css:
    target = ".solutions-deck-arena {"
    content_css = content_css.replace(target, "/* DECK WIRES CANVAS */\n" + wire_css + "\n    " + target)
    p_css.write_text(content_css, encoding='utf-8')
    print("Added wire styles to part2_css_rest.html")

# 3. Add JS updater in part4_js_logic.html
p_js = Path('/home/user/openbreak/templates/part4_js_logic.html')
content_js = p_js.read_text(encoding='utf-8')

wire_js = """
    // UX-06 Melius Style: Reactive Bézier wire calculator linking satellites to central deck
    function updateDeckWires(activeIdx = 0) {
      const arena = document.getElementById('solutionsDeckArena');
      const container = document.querySelector('.deck-perspective-container');
      if (!arena || !container || window.innerWidth <= 900) return;

      const arenaRect = arena.getBoundingClientRect();
      const contRect = container.getBoundingClientRect();
      const targetX = contRect.left + contRect.width / 2 - arenaRect.left;
      const targetY = contRect.top + contRect.height / 2 - arenaRect.top;

      [0, 1, 2, 3].forEach(i => {
        const sat = document.getElementById('sat-' + i);
        const wire = document.getElementById('wire-' + i);
        if (!sat || !wire) return;

        const satRect = sat.getBoundingClientRect();
        const startX = satRect.left + satRect.width / 2 - arenaRect.left;
        const startY = satRect.top + satRect.height / 2 - arenaRect.top;

        // Cubic Bézier curve with horizontal or vertical bias
        const dx = targetX - startX;
        const dy = targetY - startY;
        const cp1x = startX + dx * 0.5;
        const cp1y = startY;
        const cp2x = startX + dx * 0.5;
        const cp2y = targetY;

        wire.setAttribute('d', `M ${startX} ${startY} C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${targetX} ${targetY}`);
        if (i === activeIdx) {
          wire.classList.add('active');
        } else {
          wire.classList.remove('active');
        }
      });
    }

    window.addEventListener('resize', () => { updateDeckWires(window.currentDeckIndex || 0); });
"""

if "function updateDeckWires" not in content_js:
    # Insert before selectDeckCard
    content_js = content_js.replace("function selectDeckCard(idx) {", wire_js + "\n    function selectDeckCard(idx) {")
    # Also update selectDeckCard to call updateDeckWires
    old_select = """    function selectDeckCard(idx) {
      const cards = [0, 1, 2, 3].map(i => document.getElementById(`deck-card-${i}`));
      const satellites = [0, 1, 2, 3].map(i => document.getElementById(`sat-${i}`));
      
      cards.forEach((c, i) => {
        if (!c) return;
        c.className = 'deck-child-card';
        const offset = (i - idx + 4) % 4;
        c.classList.add(`pos-${offset}`);
      });

      satellites.forEach((s, i) => {
        if (!s) return;
        if (i === idx) s.classList.add('active');
        else s.classList.remove('active');
      });
    }"""
    
    new_select = """    function selectDeckCard(idx) {
      window.currentDeckIndex = idx;
      const cards = [0, 1, 2, 3].map(i => document.getElementById(`deck-card-${i}`));
      const satellites = [0, 1, 2, 3].map(i => document.getElementById(`sat-${i}`));
      
      cards.forEach((c, i) => {
        if (!c) return;
        c.className = 'deck-child-card';
        const offset = (i - idx + 4) % 4;
        c.classList.add(`pos-${offset}`);
      });

      satellites.forEach((s, i) => {
        if (!s) return;
        if (i === idx) s.classList.add('active');
        else s.classList.remove('active');
      });

      updateDeckWires(idx);
    }"""
    content_js = content_js.replace(old_select, new_select)
    # Also trigger on initial load
    content_js = content_js.replace("window.addEventListener('DOMContentLoaded', () => {", "window.addEventListener('DOMContentLoaded', () => {\n      setTimeout(() => updateDeckWires(0), 100);")
    p_js.write_text(content_js, encoding='utf-8')
    print("Added updateDeckWires call into part4_js_logic.html")

