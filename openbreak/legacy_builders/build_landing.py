import json

with open('/home/user/openbreak/assets/data_uris.json') as f:
    data = json.load(f)

with open('/home/user/openbreak/assets/three.min.js') as f:
    three_min_js = f.read()

html = f"""<!DOCTYPE html>
<html lang="es" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Open Break — The AI & Kinetic Operating System for Boutique Studios</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #000000;
      --bg-surface: #0A0A0C;
      --bg-card: #111114;
      --bg-card-hover: #18181C;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-medium: rgba(255, 255, 255, 0.16);
      --border-bright: rgba(255, 255, 255, 0.35);
      --text-white: #FFFFFF;
      --text-muted: #8E8E93;
      --text-dim: #545458;
      --accent-orange: #FF5500;
      --accent-orange-glow: rgba(255, 85, 0, 0.35);
      --accent-yellow: #FACC15;
      --accent-cyan: #38BDF8;
      --accent-green: #22C55E;
      --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; background: #000000; color: #FFFFFF; }}
    body {{
      font-family: var(--font-sans);
      background-color: var(--bg);
      color: var(--text-white);
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
      line-height: 1.45;
      position: relative;
    }}

    /* TOP ANNOUNCEMENT TICKER (MELIUS EXACT STYLE) */
    .top-announcement {{
      background: var(--accent-yellow);
      color: #000000;
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: -0.01em;
      padding: 9px 16px;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 12px;
      position: relative;
      z-index: 110;
    }}
    .top-announcement a {{
      color: #000000;
      text-decoration: underline;
      text-underline-offset: 3px;
      font-weight: 800;
    }}
    .top-announcement .badge-pill {{
      background: rgba(0, 0, 0, 0.14);
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      font-family: var(--font-mono);
    }}

    /* STICKY BLURRED NAVIGATION */
    nav {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border-bottom: 1px solid var(--border-subtle);
      padding: 0 36px;
      height: 64px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .nav-left {{
      display: flex;
      align-items: center;
      gap: 40px;
    }}
    .nav-logo {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 1.15rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      color: #FFFFFF;
      text-decoration: none;
    }}
    .nav-logo-icon {{
      width: 26px;
      height: 26px;
      background: #FFFFFF;
      color: #000000;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      font-size: 0.82rem;
      box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
    }}
    .nav-menu {{
      display: flex;
      align-items: center;
      gap: 28px;
      list-style: none;
    }}
    .nav-menu a {{
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 500;
      letter-spacing: -0.01em;
      transition: color 0.15s ease;
      display: flex;
      align-items: center;
      gap: 4px;
    }}
    .nav-menu a:hover {{ color: #FFFFFF; }}
    .nav-right {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    /* BUTTONS */
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-size: 0.86rem;
      font-weight: 600;
      letter-spacing: -0.01em;
      border-radius: 8px;
      padding: 9px 20px;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
      border: 1px solid transparent;
      white-space: nowrap;
    }}
    .btn-ghost {{
      background: transparent;
      color: #FFFFFF;
      border-color: transparent;
    }}
    .btn-ghost:hover {{
      background: rgba(255, 255, 255, 0.08);
    }}
    .btn-white {{
      background: #FFFFFF;
      color: #000000;
      border-color: #FFFFFF;
    }}
    .btn-white:hover {{
      background: #E5E5EA;
      transform: translateY(-1px);
      box-shadow: 0 4px 20px rgba(255, 255, 255, 0.25);
    }}
    .btn-orange {{
      background: var(--accent-orange);
      color: #FFFFFF;
      box-shadow: 0 0 25px var(--accent-orange-glow);
    }}
    .btn-orange:hover {{
      background: #FF661A;
      transform: translateY(-1px);
      box-shadow: 0 0 35px rgba(255, 85, 0, 0.5);
    }}
    .btn-glass {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-medium);
      color: #FFFFFF;
    }}
    .btn-glass:hover {{
      background: rgba(255, 255, 255, 0.12);
      border-color: var(--border-bright);
    }}

    /* ======================================================================
       HERO STAGE WITH FULLSCREEN 3D WEBGL ENGINE (THREE.JS PARTICLES & CURVES)
       ====================================================================== */
    .hero-viewport {{
      position: relative;
      width: 100%;
      min-height: 820px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      padding: 40px 24px 60px;
    }}

    /* 3D WEBGL CANVAS BACKGROUND */
    #hero3dCanvas {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
      pointer-events: none;
    }}

    /* Subtle radial gradient overlay on 3D canvas */
    .hero-vignette {{
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      background: radial-gradient(circle at 50% 45%, rgba(0, 0, 0, 0.2) 0%, rgba(0, 0, 0, 0.85) 75%, #000000 100%);
      z-index: 2;
      pointer-events: none;
    }}

    .hero-content {{
      position: relative;
      z-index: 10;
      max-width: 1100px;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}

    .hero-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 85, 0, 0.12);
      border: 1px solid rgba(255, 85, 0, 0.3);
      color: var(--accent-orange);
      font-family: var(--font-mono);
      font-size: 0.74rem;
      font-weight: 600;
      padding: 6px 16px;
      border-radius: 999px;
      margin-bottom: 24px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      box-shadow: 0 0 20px rgba(255, 85, 0, 0.15);
    }}
    .hero-pill .pulse-dot {{
      width: 6px;
      height: 6px;
      background: var(--accent-orange);
      border-radius: 50%;
      box-shadow: 0 0 10px var(--accent-orange);
      animation: pulseAnim 2s infinite;
    }}
    @keyframes pulseAnim {{
      0%, 100% {{ transform: scale(1); opacity: 1; }}
      50% {{ transform: scale(1.6); opacity: 0.6; }}
    }}

    .hero-headline {{
      font-size: clamp(3rem, 6.5vw, 5.6rem);
      font-weight: 800;
      letter-spacing: -0.04em;
      line-height: 1.04;
      color: #FFFFFF;
      max-width: 980px;
      margin-bottom: 24px;
      text-shadow: 0 4px 40px rgba(0,0,0,0.8);
    }}

    .hero-subline {{
      font-size: clamp(1.1rem, 2vw, 1.35rem);
      color: #A1A1AA;
      max-width: 720px;
      margin-bottom: 38px;
      font-weight: 400;
      letter-spacing: -0.015em;
      line-height: 1.5;
    }}

    /* INTERACTIVE PROMPT BAR (MELIUS SEARCH BAR) */
    .prompt-bar-wrap {{
      width: 100%;
      max-width: 680px;
      background: rgba(14, 14, 16, 0.85);
      border: 1px solid var(--border-medium);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-radius: 16px;
      padding: 10px 14px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.9), 0 0 40px rgba(255, 85, 0, 0.12);
      margin-bottom: 36px;
      transition: all 0.25s ease;
    }}
    .prompt-bar-wrap:focus-within {{
      border-color: var(--accent-orange);
      box-shadow: 0 20px 60px -10px rgba(0, 0, 0, 0.95), 0 0 50px rgba(255, 85, 0, 0.35);
    }}
    .prompt-input {{
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      color: #FFFFFF;
      font-family: var(--font-sans);
      font-size: 0.96rem;
      letter-spacing: -0.01em;
    }}
    .prompt-input::placeholder {{ color: var(--text-dim); }}

    /* 3D CONTROLLER TOGGLES */
    .three-controls {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-family: var(--font-mono);
      font-size: 0.74rem;
      color: var(--text-muted);
      margin-bottom: 20px;
    }}
    .three-btn {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      color: #D4D4D8;
      padding: 4px 10px;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .three-btn:hover {{
      background: rgba(255, 255, 255, 0.12);
      color: #FFFFFF;
      border-color: var(--border-medium);
    }}

    /* CUSTOMER TICKER / PROOF */
    .hero-proof {{
      width: 100%;
      max-width: 1100px;
      border-top: 1px solid var(--border-subtle);
      border-bottom: 1px solid var(--border-subtle);
      padding: 24px 16px;
      margin-top: 40px;
    }}
    .proof-label {{
      text-align: center;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.14em;
      color: var(--text-dim);
      margin-bottom: 18px;
    }}
    .proof-row {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 44px;
      flex-wrap: wrap;
      opacity: 0.75;
    }}
    .proof-logo {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.88rem;
      font-weight: 700;
      letter-spacing: -0.01em;
      color: #A1A1AA;
    }}

    /* ======================================================================
       INTERACTIVE CANVAS WORKSPACE (MELIUS INFINITE CANVAS WITH BEZIER WIRES)
       ====================================================================== */
    .canvas-section {{
      width: 100%;
      background: #000000;
      position: relative;
      padding: 60px 0 120px;
      border-top: 1px solid var(--border-subtle);
    }}
    .canvas-container {{
      max-width: 1360px;
      margin: 0 auto;
      padding: 0 24px;
    }}

    .canvas-header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .canvas-title-group h2 {{
      font-size: 2rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      margin-bottom: 6px;
    }}
    .canvas-title-group p {{
      color: var(--text-muted);
      font-size: 0.92rem;
    }}

    .canvas-tabs-bar {{
      display: flex;
      background: #0D0D10;
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 4px;
      gap: 4px;
    }}
    .c-tab {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-family: var(--font-sans);
      font-size: 0.82rem;
      font-weight: 600;
      padding: 7px 18px;
      border-radius: 7px;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .c-tab:hover {{ color: #FFFFFF; }}
    .c-tab.active {{
      background: #1C1C22;
      color: #FFFFFF;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
    }}

    /* INFINITE CANVAS WORKSPACE BOARD */
    .infinite-canvas-board {{
      position: relative;
      background: #050507;
      border: 1px solid var(--border-medium);
      border-radius: 24px;
      height: 760px;
      overflow: hidden;
      box-shadow: 0 35px 90px -20px rgba(0, 0, 0, 0.95), 0 0 60px rgba(255, 85, 0, 0.08);
      user-select: none;
    }}
    /* DOT GRID BACKGROUND */
    .infinite-canvas-board::before {{
      content: "";
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      background-size: 26px 26px;
      background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px);
      pointer-events: none;
      z-index: 1;
    }}

    /* FLOATING TOP-LEFT TELEMETRY HUD */
    .canvas-hud {{
      position: absolute;
      top: 18px;
      left: 20px;
      z-index: 20;
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(14, 14, 18, 0.88);
      border: 1px solid var(--border-medium);
      backdrop-filter: blur(14px);
      padding: 7px 14px;
      border-radius: 10px;
      font-family: var(--font-mono);
      font-size: 0.74rem;
      color: var(--text-muted);
    }}
    .hud-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--accent-green);
      box-shadow: 0 0 10px var(--accent-green);
    }}

    /* INTERACTIVE SVG CURVES (DYNAMIC WIRES) */
    .svg-wires-canvas {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 5;
    }}

    /* CANVAS NODES (MELIUS GRAPH CARDS) */
    .graph-node {{
      position: absolute;
      z-index: 10;
      background: #0E0E12;
      border: 1px solid var(--border-medium);
      border-radius: 16px;
      width: 300px;
      box-shadow: 0 20px 45px rgba(0, 0, 0, 0.75);
      cursor: grab;
      transition: border-color 0.25s, box-shadow 0.25s, transform 0.15s ease-out;
      overflow: hidden;
    }}
    .graph-node:active {{
      cursor: grabbing;
    }}
    .graph-node:hover {{
      border-color: rgba(255, 255, 255, 0.45);
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9), 0 0 30px rgba(255, 85, 0, 0.2);
    }}
    .graph-node.active-node {{
      border-color: var(--accent-orange);
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9), 0 0 35px var(--accent-orange-glow);
    }}

    .node-header-bar {{
      padding: 10px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--text-muted);
      border-bottom: 1px solid var(--border-subtle);
      background: rgba(0, 0, 0, 0.3);
    }}
    .node-type-pill {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.68rem;
      font-weight: 700;
      letter-spacing: 0.04em;
    }}
    .pill-student {{ background: rgba(56, 189, 248, 0.15); color: #38BDF8; }}
    .pill-concurrency {{ background: rgba(239, 68, 68, 0.15); color: #F87171; }}
    .pill-credits {{ background: rgba(250, 204, 21, 0.15); color: #FDE047; }}
    .pill-stripe {{ background: rgba(34, 197, 94, 0.15); color: #4ADE80; }}

    .node-body {{
      padding: 14px;
    }}
    .node-title {{
      font-size: 1rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 6px;
      color: #FFFFFF;
    }}
    .node-desc {{
      font-size: 0.82rem;
      color: var(--text-muted);
      line-height: 1.45;
      margin-bottom: 12px;
    }}
    .node-media-view {{
      width: 100%;
      height: 154px;
      border-radius: 10px;
      overflow: hidden;
      position: relative;
      background: #000000;
      border: 1px solid var(--border-subtle);
    }}
    .node-media-view img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.4s ease;
    }}
    .graph-node:hover .node-media-view img {{
      transform: scale(1.06);
    }}

    .node-code-terminal {{
      background: #060608;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 10px 12px;
      font-family: var(--font-mono);
      font-size: 0.74rem;
      color: #A1A1AA;
      line-height: 1.55;
    }}

    /* CONNECTION PORTS */
    .port-circle {{
      width: 10px;
      height: 10px;
      background: #FFFFFF;
      border: 2px solid #000000;
      border-radius: 50%;
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      z-index: 15;
    }}
    .port-in {{ left: -5px; }}
    .port-out {{ right: -5px; }}

    /* CANVAS BOTTOM TELEMETRY */
    .canvas-telemetry-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-top: 24px;
    }}
    @media (max-width: 900px) {{
      .canvas-telemetry-row {{ grid-template-columns: 1fr 1fr; }}
    }}
    .telemetry-card {{
      background: #0A0A0D;
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 20px;
    }}
    .telemetry-card .val {{
      font-size: 1.7rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      margin-bottom: 4px;
    }}
    .telemetry-card .desc {{
      font-size: 0.8rem;
      color: var(--text-muted);
    }}

    /* ======================================================================
       SOLUTIONS SECTION (HIGH-END MOVEMENT STUDIOS)
       ====================================================================== */
    .solutions-section {{
      max-width: 1260px;
      margin: 90px auto 120px;
      padding: 0 24px;
    }}
    .section-eyebrow {{
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--accent-orange);
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-bottom: 12px;
      text-align: center;
    }}
    .section-headline {{
      font-size: clamp(2.2rem, 4.2vw, 3.4rem);
      font-weight: 800;
      letter-spacing: -0.035em;
      text-align: center;
      max-width: 860px;
      margin: 0 auto 56px;
      line-height: 1.1;
    }}

    .solutions-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
    }}
    @media (max-width: 900px) {{
      .solutions-grid {{ grid-template-columns: 1fr; }}
    }}
    .sol-card {{
      background: #0C0C0E;
      border: 1px solid var(--border-medium);
      border-radius: 20px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .sol-card:hover {{
      border-color: rgba(255, 255, 255, 0.35);
      transform: translateY(-5px);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.8);
    }}
    .sol-img-holder {{
      height: 230px;
      position: relative;
      overflow: hidden;
    }}
    .sol-img-holder img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.5s ease;
    }}
    .sol-card:hover .sol-img-holder img {{
      transform: scale(1.06);
    }}
    .sol-body {{
      padding: 26px;
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .sol-title {{
      font-size: 1.25rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }}
    .sol-text {{
      color: var(--text-muted);
      font-size: 0.88rem;
      line-height: 1.55;
      margin-bottom: 22px;
    }}
    .sol-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .sol-chip {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      padding: 3px 8px;
      border-radius: 4px;
      color: #A1A1AA;
    }}

    /* ======================================================================
       PRICING & FAIR FEES 2026
       ====================================================================== */
    .pricing-section {{
      max-width: 1220px;
      margin: 80px auto 140px;
      padding: 0 24px;
    }}
    .pricing-toggle-wrap {{
      display: flex;
      justify-content: center;
      margin-bottom: 50px;
    }}
    .pricing-toggle {{
      background: #111114;
      border: 1px solid var(--border-medium);
      border-radius: 999px;
      padding: 4px;
      display: flex;
      gap: 4px;
    }}
    .p-toggle-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-family: var(--font-sans);
      font-size: 0.84rem;
      font-weight: 600;
      padding: 8px 22px;
      border-radius: 999px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .p-toggle-btn.active {{
      background: #FFFFFF;
      color: #000000;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }}

    .pricing-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      align-items: stretch;
    }}
    @media (max-width: 900px) {{
      .pricing-grid {{ grid-template-columns: 1fr; }}
    }}
    .p-plan-card {{
      background: #0B0B0E;
      border: 1px solid var(--border-medium);
      border-radius: 22px;
      padding: 38px 30px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      transition: all 0.25s;
    }}
    .p-plan-card:hover {{
      border-color: rgba(255, 255, 255, 0.3);
      transform: translateY(-4px);
    }}
    .p-plan-card.highlight {{
      border-color: var(--accent-orange);
      background: linear-gradient(180deg, rgba(255, 85, 0, 0.08) 0%, #0B0B0E 100%);
      box-shadow: 0 0 60px rgba(255, 85, 0, 0.18);
    }}
    .p-badge-featured {{
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--accent-orange);
      color: #FFFFFF;
      font-size: 0.72rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 4px 14px;
      border-radius: 999px;
    }}
    .p-plan-title {{
      font-size: 1.3rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }}
    .p-plan-desc {{
      color: var(--text-muted);
      font-size: 0.86rem;
      min-height: 44px;
      margin-bottom: 24px;
    }}
    .p-price-row {{
      display: flex;
      align-items: baseline;
      gap: 6px;
      margin-bottom: 4px;
    }}
    .p-price-amount {{
      font-size: 3.3rem;
      font-weight: 800;
      letter-spacing: -0.04em;
    }}
    .p-price-unit {{
      color: var(--text-muted);
      font-size: 0.95rem;
    }}
    .p-price-condition {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--text-dim);
      margin-bottom: 28px;
    }}
    .p-features-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 13px;
      margin-bottom: 32px;
      font-size: 0.88rem;
    }}
    .p-features-list li {{
      display: flex;
      align-items: flex-start;
      gap: 10px;
      color: #D4D4D8;
    }}
    .p-features-list li svg {{
      flex-shrink: 0;
      margin-top: 3px;
      color: var(--accent-orange);
    }}

    /* FOOTER */
    footer {{
      border-top: 1px solid var(--border-subtle);
      padding: 60px 24px 40px;
      max-width: 1260px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
      font-size: 0.85rem;
      color: var(--text-dim);
    }}
  </style>

  <!-- INLINE THREE.JS BUNDLE (OFFLINE STANDALONE READY) -->
  <script>
  {three_min_js}
  </script>
</head>
<body>

  <!-- ANNOUNCEMENT BANNER -->
  <div class="top-announcement">
    <span class="badge-pill">MÉXICO 2026</span>
    <span>Lanzamiento del Programa de Estudios Fundadores: 0% de comisión propia y setup guiado.</span>
    <a href="#pricing">Ver Cupos Piloto →</a>
  </div>

  <!-- STICKY BLURRED NAVBAR -->
  <nav>
    <div class="nav-left">
      <a href="#" class="nav-logo">
        <div class="nav-logo-icon">OB</div>
        <span>Open Break</span>
      </a>

      <ul class="nav-menu">
        <li><a href="#canvas-section">Interactive Canvas</a></li>
        <li><a href="#solutions">Estudios Boutique</a></li>
        <li><a href="#pricing">Tarifas 2026</a></li>
        <li><a href="prototype.html" target="_blank">Prototipo Operativo ↗</a></li>
      </ul>
    </div>

    <div class="nav-right">
      <a href="prototype.html" class="btn btn-ghost">Ver Demo UX</a>
      <a href="#pricing" class="btn btn-white">Acceso Piloto</a>
    </div>
  </nav>

  <!-- ======================================================================
       HERO VIEWPORT CON ENGINE WEBGL 3D INTERACTIVO
       ====================================================================== -->
  <section class="hero-viewport">
    
    <!-- 3D WEBGL CANVAS -->
    <canvas id="hero3dCanvas"></canvas>
    <div class="hero-vignette"></div>

    <div class="hero-content">
      <div class="hero-pill">
        <span class="pulse-dot"></span>
        <span>Kinetic Architecture 2026 · Zero Oversubscription</span>
      </div>

      <h1 class="hero-headline">The kinetic operating system for boutique movement studios.</h1>

      <p class="hero-subline">
        Diseñado para estudios de Reformer Pilates, Barre y Yoga. Erradica el sobrecupo con transacciones atómicas de reserva, blinda tus paquetes de créditos y cobra directo con 0% de comisión propia.
      </p>

      <!-- INTERACTIVE PROMPT BAR -->
      <div class="prompt-bar-wrap">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FF5500" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="text" class="prompt-input" id="heroPromptInput" value="Simular: 2 alumnos reservando el último Reformer a las 07:00 AM">
        <button class="btn btn-orange" onclick="triggerSimulationPrompt()" style="padding: 7px 16px; font-size: 0.8rem;">Ejecutar Simulación</button>
      </div>

      <!-- 3D INTERACTIVITY CONTROLS -->
      <div class="three-controls">
        <span>3D SHADER MODE:</span>
        <button class="three-btn" onclick="setWaveSpeed(1.0)">Suave</button>
        <button class="three-btn" onclick="setWaveSpeed(2.5)">Cinético</button>
        <button class="three-btn" onclick="toggleGeometry()">Cambiar Malla 3D</button>
      </div>

      <!-- PROOF LOGOS -->
      <div class="hero-proof">
        <div class="proof-label">Calibrado para estudios boutique de alta demanda en México</div>
        <div class="proof-row">
          <div class="proof-logo">REFORMER BOTANICAL</div>
          <div class="proof-logo">LUNA PILATES ROMA</div>
          <div class="proof-logo">BARRE & SCULPT CONDESA</div>
          <div class="proof-logo">CADILLAC PRECISION</div>
          <div class="proof-logo">SOLARIS MOVEMENT</div>
        </div>
      </div>
    </div>
  </section>

  <!-- ======================================================================
       INTERACTIVE CANVAS SECTION (CON NODOS DRAGGABLE Y WIRES BÉZIER DINÁMICOS)
       ====================================================================== -->
  <section class="canvas-section" id="canvas-section">
    <div class="canvas-container">
      
      <div class="canvas-header-bar">
        <div class="canvas-title-group">
          <h2>Infinite Operational Canvas</h2>
          <p>Un grafo de ejecución donde cada nodo resuelve un proceso crítico de tu estudio en tiempo real.</p>
        </div>

        <div class="canvas-tabs-bar">
          <button class="c-tab active" onclick="switchCanvasTab(this, 'all')">Grafo Completo</button>
          <button class="c-tab" onclick="switchCanvasTab(this, 'concurrency')">Test de Concurrencia</button>
          <button class="c-tab" onclick="switchCanvasTab(this, 'economics')">Conciliación 0% Fee</button>
        </div>
      </div>

      <!-- THE INFINITE WORKSPACE BOARD -->
      <div class="infinite-canvas-board" id="canvasBoard">
        
        <!-- TELEMETRY HUD -->
        <div class="canvas-hud">
          <div class="hud-dot"></div>
          <span>PG_ISOLATION: READ COMMITTED</span>
          <span>·</span>
          <span>STRIPE CONNECT: 0.00% CUT</span>
          <span>·</span>
          <span style="color: #FFFFFF;">STATUS: OPERATIONAL</span>
        </div>

        <!-- SVG DYNAMIC BEZIER WIRES -->
        <svg class="svg-wires-canvas" id="wiresCanvas">
          <path id="bezier-1-2" d="" stroke="rgba(255, 255, 255, 0.3)" stroke-width="2" fill="none" stroke-dasharray="5,5"/>
          <path id="bezier-2-3" d="" stroke="rgba(255, 255, 255, 0.3)" stroke-width="2" fill="none" stroke-dasharray="5,5"/>
          <path id="bezier-3-4" d="" stroke="rgba(255, 85, 0, 0.7)" stroke-width="2.5" fill="none"/>
        </svg>

        <!-- NODE 1 -->
        <div class="graph-node active-node" id="node-1" style="left: 40px; top: 110px;">
          <div class="node-header-bar">
            <span>NODE // 01</span>
            <span class="node-type-pill pill-student">STUDENT UI</span>
          </div>
          <div class="node-body">
            <div class="node-title">Reserva Web Móvil (3-Tap)</div>
            <div class="node-desc">Agenda desde link de Instagram o WhatsApp sin instalar apps.</div>
            <div class="node-media-view">
              <img src="{data['coach_guiding']}" alt="Pilates Reformer Class">
            </div>
          </div>
          <div class="port-circle port-out" id="p1-out"></div>
        </div>

        <!-- NODE 2 -->
        <div class="graph-node" id="node-2" style="left: 450px; top: 60px;">
          <div class="port-circle port-in" id="p2-in"></div>
          <div class="node-header-bar">
            <span>NODE // 02</span>
            <span class="node-type-pill pill-concurrency">ATOMIC LOCK</span>
          </div>
          <div class="node-body">
            <div class="node-title">Bloqueo Atómico SQL</div>
            <div class="node-desc">Previene colisiones si 2 alumnos reservan al mismo instante.</div>
            <div class="node-code-terminal">
              <span style="color: #38BDF8;">BEGIN TRANSACTION;</span><br>
              <span style="color: #FACC15;">SELECT</span> * <span style="color: #FACC15;">FROM</span> session_spots<br>
              <span style="color: #F87171;">WHERE</span> spot_id = 'reformer_08'<br>
              <span style="color: #4ADE80; font-weight:700;">FOR UPDATE;</span><br>
              <span style="color: #94A3B8;">// 0 Sobrecupos</span>
            </div>
          </div>
          <div class="port-circle port-out" id="p2-out"></div>
        </div>

        <!-- NODE 3 -->
        <div class="graph-node" id="node-3" style="left: 850px; top: 170px;">
          <div class="port-circle port-in" id="p3-in"></div>
          <div class="node-header-bar">
            <span>NODE // 03</span>
            <span class="node-type-pill pill-credits">CREDIT AUDIT</span>
          </div>
          <div class="node-body">
            <div class="node-title">Bitácora Inmutable</div>
            <div class="node-desc">Resta 1 crédito. Si cancela con >6h, repone de inmediato.</div>
            <div class="node-media-view">
              <img src="{data['studio_light']}" alt="Studio Reformer Room">
            </div>
          </div>
          <div class="port-circle port-out" id="p3-out"></div>
        </div>

        <!-- NODE 4 -->
        <div class="graph-node" id="node-4" style="left: 1020px; top: 400px;">
          <div class="port-circle port-in" id="p4-in"></div>
          <div class="node-header-bar">
            <span>NODE // 04</span>
            <span class="node-type-pill pill-stripe">STRIPE DIRECT</span>
          </div>
          <div class="node-body">
            <div class="node-title">Cobro Directo 0% Fee</div>
            <div class="node-desc">El dinero va directo a tu banco. Open Break cobra $0 comisión.</div>
            <div class="node-code-terminal">
              Destination: <span style="color: #FFFFFF;">acct_studio_boutique</span><br>
              Open Break Cut: <span style="color: #4ADE80; font-weight: 700;">0.00%</span><br>
              Idempotency Key: <span style="color: #FACC15;">Verified</span>
            </div>
          </div>
        </div>

      </div>

      <!-- CANVAS BOTTOM METRICS -->
      <div class="canvas-telemetry-row">
        <div class="telemetry-card">
          <div class="val" style="color: var(--accent-green);">0.00%</div>
          <div class="desc">Tasa de sobrecupo físico comprobada en salas</div>
        </div>
        <div class="telemetry-card">
          <div class="val">$0 MXN</div>
          <div class="desc">Comisión propia sobre tus paquetes vendidos</div>
        </div>
        <div class="telemetry-card">
          <div class="val" style="color: var(--accent-orange);">6 Horas</div>
          <div class="desc">Ventana configurada para proteger cobro de profesores</div>
        </div>
        <div class="telemetry-card">
          <div class="val">< 15 segs</div>
          <div class="desc">Tiempo promedio en reservar desde web móvil</div>
        </div>
      </div>

    </div>
  </section>

  <!-- ======================================================================
       SOLUTIONS SECTION (BOUTIQUE NICHES)
       ====================================================================== -->
  <section class="solutions-section" id="solutions">
    <div class="section-eyebrow">Verticales Especializadas</div>
    <h2 class="section-headline">Un sistema calibrado para la realidad de cada disciplina boutique.</h2>

    <div class="solutions-grid">
      
      <!-- Card 1 -->
      <div class="sol-card">
        <div class="sol-img-holder">
          <img src="{data['studio_hero']}" alt="Reformer Pilates Studio">
        </div>
        <div class="sol-body">
          <div>
            <h3 class="sol-title">Reformer & Cadillac Pilates</h3>
            <p class="sol-text">
              Control riguroso de máquinas individuales (ej. 8 a 12 reformers). Si un cliente cancela a tiempo, el lugar se asigna automáticamente a quien encabeza la lista de espera.
            </p>
          </div>
          <div class="sol-tags">
            <span class="sol-chip">Cupo Máximo 12</span>
            <span class="sol-chip">Waitlist Auto</span>
            <span class="sol-chip">No-Shows = $0 Pérdida</span>
          </div>
        </div>
      </div>

      <!-- Card 2 -->
      <div class="sol-card">
        <div class="sol-img-holder">
          <img src="{data['class_action']}" alt="Barre & Movement">
        </div>
        <div class="sol-body">
          <div>
            <h3 class="sol-title">Barre, Danza & Mat Flow</h3>
            <p class="sol-text">
              Gestión de salas de mayor aforo con niveles diferenciados y cálculo de honorarios de maestros por alumno asistente o cuota fija por sesión.
            </p>
          </div>
          <div class="sol-tags">
            <span class="sol-chip">Comisión por Instructor</span>
            <span class="sol-chip">Check-in 1-Tap</span>
            <span class="sol-chip">Membresías Recurrentes</span>
          </div>
        </div>
      </div>

      <!-- Card 3 -->
      <div class="sol-card">
        <div class="sol-img-holder">
          <img src="{data['studio_minimal']}" alt="Yoga & Mindfulness Studio">
        </div>
        <div class="sol-body">
          <div>
            <h3 class="sol-title">Yoga & Mindfulness Spaces</h3>
            <p class="sol-text">
              Paquetes combinados de sesiones grupales, talleres de fin de semana y pases drop-in sin fricción para practicantes recurrentes o de paso.
            </p>
          </div>
          <div class="sol-tags">
            <span class="sol-chip">Drop-in Digital</span>
            <span class="sol-chip">Pases Múltiples</span>
            <span class="sol-chip">Conciliación CSV</span>
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- ======================================================================
       PRICING TABLE (2026 TRANSPARENT TIERS)
       ====================================================================== -->
  <section class="pricing-section" id="pricing">
    <div class="section-eyebrow">Tarifas Transparentes 2026</div>
    <h2 class="section-headline">Cuotas fijas predecibles. Sin comisiones sorpresa al fin de mes.</h2>

    <div class="pricing-toggle-wrap">
      <div class="pricing-toggle">
        <button class="p-toggle-btn active" onclick="setBillingPlan(this, 'monthly')">Facturación Mensual</button>
        <button class="p-toggle-btn" onclick="setBillingPlan(this, 'annual')">Anual (8% Ahorro)</button>
      </div>
    </div>

    <div class="pricing-grid">
      
      <!-- Inicio -->
      <div class="p-plan-card">
        <div>
          <div class="p-plan-title">Inicio</div>
          <div class="p-plan-desc">Para estudios boutique de 1 sala que quieren dejar atrás las hojas de cálculo y la conciliación por WhatsApp.</div>
          <div class="p-price-row">
            <span class="p-price-amount" id="price-val-inicio">$790</span>
            <span class="p-price-unit">MXN / mes</span>
          </div>
          <div class="p-price-condition">+ IVA · $990 MXN setup guiado</div>
          <ul class="p-features-list">
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> 1 Sede física</li>
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Hasta 120 alumnos activos</li>
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> 2 Instructores</li>
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Hasta 600 reservas al mes</li>
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> <strong>0% comisión propia de ventas</strong></li>
          </ul>
        </div>
        <a href="prototype.html" class="btn btn-glass" style="width: 100%;">Elegir Inicio</a>
      </div>

      <!-- Estudio (Highlight) -->
      <div class="p-plan-card highlight">
        <span class="p-badge-featured">Recomendado</span>
        <div>
          <div class="p-plan-title">Estudio</div>
          <div class="p-plan-desc">El estándar para estudios consolidados con alta demanda de reservas, lista de espera y profesores rotativos.</div>
          <div class="p-price-row">
            <span class="p-price-amount" id="price-val-estudio">$1,290</span>
            <span class="p-price-unit">MXN / mes</span>
          </div>
          <div class="p-price-condition">+ IVA · $2,490 MXN setup e importación</div>
          <ul class="p-features-list">
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> 1 Sede con hasta 3 salas</li>
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Hasta 300 alumnos activos</li>
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Hasta 8 instructores con cálculo de honorarios</li>
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Hasta 2,000 reservas al mes</li>
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> <strong>Lista de espera automatizada</strong></li>
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Check-in táctil de recepción</li>
          </ul>
        </div>
        <a href="prototype.html" class="btn btn-orange" style="width: 100%;">Comenzar Piloto</a>
      </div>

      <!-- Plus -->
      <div class="p-plan-card">
        <div>
          <div class="p-plan-title">Plus / Multi-sede</div>
          <div class="p-plan-desc">Para cadenas de estudios en expansión que requieren analítica consolidada y exportación contable.</div>
          <div class="p-price-row">
            <span class="p-price-amount" id="price-val-plus">$1,990</span>
            <span class="p-price-unit">MXN / mes</span>
          </div>
          <div class="p-price-condition">+ IVA · Migración multi-sucursal guiada</div>
          <ul class="p-features-list">
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Hasta 2 sedes activas</li>
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> 700 alumnos activos</li>
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Instructores ilimitados</li>
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Hasta 5,000 reservas al mes</li>
            <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> API & Conciliación bancaria avanzada</li>
          </ul>
        </div>
        <a href="prototype.html" class="btn btn-glass" style="width: 100%;">Contactar Soporte</a>
      </div>

    </div>
  </section>

  <!-- FOOTER -->
  <footer>
    <div>
      <strong style="color: #FFFFFF;">Open Break</strong>
      <span> · Portafolio Digital México 2026</span>
    </div>
    <div>
      <span>0% Comisión de Plataforma · PostgreSQL Row-Level Locking Architecture</span>
    </div>
  </footer>

  <!-- ======================================================================
       INTERACTIVE JAVASCRIPT: 3D THREE.JS WEBGL + DRAGGABLE NODES & WIRES
       ====================================================================== -->
  <script>
    /* ====================================================================
       1. THREE.JS 3D KINETIC ENGINE (CANVAS HERO SHADER / PARTICLES)
       ==================================================================== */
    let scene, camera, renderer, particleSystem, wirePlane;
    let waveSpeed = 1.0;
    let isWireGeometry = false;
    let mouseX = 0, mouseY = 0;
    let targetX = 0, targetY = 0;

    function init3DHero() {{
      const canvas = document.getElementById('hero3dCanvas');
      const width = canvas.parentElement.clientWidth;
      const height = canvas.parentElement.clientHeight;

      scene = new THREE.Scene();
      camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
      camera.position.set(0, -15, 30);
      camera.lookAt(0, 0, 0);

      renderer = new THREE.WebGLRenderer({{ canvas: canvas, alpha: true, antialias: true }});
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      // 1. PARTICULAS FLOTANTES KINÉTICAS (ESTILO MELIUS NEBULA)
      const particleCount = 1800;
      const geometry = new THREE.BufferGeometry();
      const positions = new Float32Array(particleCount * 3);
      const colors = new Float32Array(particleCount * 3);

      for (let i = 0; i < particleCount; i++) {{
        const i3 = i * 3;
        // Distribuir en un disco ondulante
        const radius = Math.random() * 45 + 5;
        const angle = Math.random() * Math.PI * 2;
        
        positions[i3] = Math.cos(angle) * radius;
        positions[i3 + 1] = Math.sin(angle) * radius * 0.4;
        positions[i3 + 2] = (Math.random() - 0.5) * 12;

        // Color degradado: Naranja Melius (#FF5500) a Blanco perla y Amarillo neón
        const mixRatio = Math.random();
        if (mixRatio > 0.6) {{
          // Orange
          colors[i3] = 1.0;
          colors[i3 + 1] = 0.33;
          colors[i3 + 2] = 0.0;
        }} else if (mixRatio > 0.3) {{
          // White
          colors[i3] = 0.9;
          colors[i3 + 1] = 0.9;
          colors[i3 + 2] = 0.95;
        }} else {{
          // Yellow
          colors[i3] = 0.98;
          colors[i3 + 1] = 0.8;
          colors[i3 + 2] = 0.1;
        }}
      }}

      geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

      const pMaterial = new THREE.PointsMaterial({{
        size: 0.28,
        vertexColors: true,
        transparent: true,
        opacity: 0.85,
        blending: THREE.AdditiveBlending
      }});

      particleSystem = new THREE.Points(geometry, pMaterial);
      scene.add(particleSystem);

      // 2. KINETIC WIRE MESH GRID (PLANE DE ONDAS MATEMÁTICAS)
      const planeGeo = new THREE.PlaneGeometry(70, 50, 48, 36);
      const wireMat = new THREE.MeshBasicMaterial({{
        color: 0xFF5500,
        wireframe: true,
        transparent: true,
        opacity: 0.12
      }});
      wirePlane = new THREE.Mesh(planeGeo, wireMat);
      wirePlane.rotation.x = -Math.PI / 3;
      wirePlane.position.z = -5;
      scene.add(wirePlane);

      // Eventos de Mouse
      window.addEventListener('resize', onWindowResize);
      window.addEventListener('mousemove', (e) => {{
        mouseX = (e.clientX / window.innerWidth) * 2 - 1;
        mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
      }});

      animate3D();
    }}

    function onWindowResize() {{
      const canvas = document.getElementById('hero3dCanvas');
      if (!canvas) return;
      const width = canvas.parentElement.clientWidth;
      const height = canvas.parentElement.clientHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    }}

    let clock = new THREE.Clock();
    function animate3D() {{
      requestAnimationFrame(animate3D);
      const elapsed = clock.getElapsedTime() * waveSpeed;

      // Movimiento de partículas
      const pos = particleSystem.geometry.attributes.position.array;
      for (let i = 0; i < pos.length; i += 3) {{
        const x = pos[i];
        const y = pos[i + 1];
        // Función sinusoidal armónica
        pos[i + 2] = Math.sin(x * 0.15 + elapsed) * Math.cos(y * 0.2 + elapsed) * 3.5;
      }}
      particleSystem.geometry.attributes.position.needsUpdate = true;

      // Ondulación de la malla alámbrica
      const planePos = wirePlane.geometry.attributes.position.array;
      for (let j = 0; j < planePos.length; j += 3) {{
        const px = planePos[j];
        const py = planePos[j + 1];
        planePos[j + 2] = Math.sin(px * 0.2 + elapsed * 1.2) * Math.cos(py * 0.2 + elapsed * 0.8) * 2.8;
      }}
      wirePlane.geometry.attributes.position.needsUpdate = true;

      // Suave seguimiento del cursor
      targetX += (mouseX * 4 - targetX) * 0.05;
      targetY += (mouseY * 3 - targetY) * 0.05;
      camera.position.x = targetX;
      camera.position.y = -15 + targetY;
      camera.lookAt(0, 0, 0);

      particleSystem.rotation.z = elapsed * 0.04;

      renderer.render(scene, camera);
    }}

    function setWaveSpeed(s) {{
      waveSpeed = s;
    }}

    function toggleGeometry() {{
      isWireGeometry = !isWireGeometry;
      wirePlane.material.color.setHex(isWireGeometry ? 0x38BDF8 : 0xFF5500);
      wirePlane.material.opacity = isWireGeometry ? 0.25 : 0.12;
    }}

    // Iniciar 3D tras carga de DOM
    window.addEventListener('DOMContentLoaded', () => {{
      init3DHero();
      initCanvasNodes();
      updateWires();
    }});


    /* ====================================================================
       2. DRAGGABLE CANVAS NODES & DYNAMIC SVG BEZIER WIRES
       ==================================================================== */
    function updateWires() {{
      const b1_2 = document.getElementById('bezier-1-2');
      const b2_3 = document.getElementById('bezier-2-3');
      const b3_4 = document.getElementById('bezier-3-4');

      const boardRect = document.getElementById('canvasBoard').getBoundingClientRect();

      const p1 = getPortCenter('p1-out', boardRect);
      const p2In = getPortCenter('p2-in', boardRect);
      const p2Out = getPortCenter('p2-out', boardRect);
      const p3In = getPortCenter('p3-in', boardRect);
      const p3Out = getPortCenter('p3-out', boardRect);
      const p4In = getPortCenter('p4-in', boardRect);

      // Calcular Curvas Bézier Cúbicas Suaves
      if (b1_2) b1_2.setAttribute('d', makeBezierPath(p1, p2In));
      if (b2_3) b2_3.setAttribute('d', makeBezierPath(p2Out, p3In));
      if (b3_4) b3_4.setAttribute('d', makeBezierPath(p3Out, p4In));
    }}

    function getPortCenter(portId, boardRect) {{
      const el = document.getElementById(portId);
      if (!el) return {{ x: 0, y: 0 }};
      const rect = el.getBoundingClientRect();
      return {{
        x: rect.left + rect.width / 2 - boardRect.left,
        y: rect.top + rect.height / 2 - boardRect.top
      }};
    }}

    function makeBezierPath(from, to) {{
      const dx = Math.abs(to.x - from.x) * 0.55;
      return `M ${{from.x}} ${{from.y}} C ${{from.x + dx}} ${{from.y}}, ${{to.x - dx}} ${{to.y}}, ${{to.x}} ${{to.y}}`;
    }}

    // Hacer nodos arrastrables con Mouse / Touch
    function initCanvasNodes() {{
      const nodes = document.querySelectorAll('.graph-node');
      const board = document.getElementById('canvasBoard');

      nodes.forEach(node => {{
        let isDragging = false;
        let startX, startY, origX, origY;

        node.addEventListener('mousedown', (e) => {{
          // Don't drag if clicking buttons
          if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A') return;
          isDragging = true;
          startX = e.clientX;
          startY = e.clientY;
          origX = node.offsetLeft;
          origY = node.offsetTop;
          
          nodes.forEach(n => n.classList.remove('active-node'));
          node.classList.add('active-node');
          node.style.zIndex = '18';
          e.preventDefault();
        }});

        window.addEventListener('mousemove', (e) => {{
          if (!isDragging) return;
          const dx = e.clientX - startX;
          const dy = e.clientY - startY;
          
          let newX = origX + dx;
          let newY = origY + dy;

          // Limitar dentro del board
          newX = Math.max(10, Math.min(board.clientWidth - node.clientWidth - 10, newX));
          newY = Math.max(10, Math.min(board.clientHeight - node.clientHeight - 10, newY));

          node.style.left = newX + 'px';
          node.style.top = newY + 'px';

          updateWires();
        }});

        window.addEventListener('mouseup', () => {{
          if (isDragging) {{
            isDragging = false;
            node.style.zIndex = '10';
          }}
        }});
      }});

      window.addEventListener('resize', updateWires);
    }}

    /* ====================================================================
       3. INTERACTIVE SIMULATION PROMPT & TABS
       ==================================================================== */
    function triggerSimulationPrompt() {{
      const node2 = document.getElementById('node-2');
      const node3 = document.getElementById('node-3');

      // Animación visual de destello en nodos de PostgreSQL y Stripe
      node2.classList.add('active-node');
      node2.style.transform = 'scale(1.05)';
      
      setTimeout(() => {{
        node2.style.transform = '';
        node3.classList.add('active-node');
        node3.style.transform = 'scale(1.05)';

        setTimeout(() => {{
          node3.style.transform = '';
          alert("⚡ SIMULACIÓN EJECUTADA EN EL CANVAS:\\n\\n" +
                "1. Alumno 1 gana el bloqueo PostgreSQL 'FOR UPDATE' sobre el último Reformer.\\n" +
                "2. Alumno 2 es redirigido en 4ms a Lista de Espera #1 con notificación push.\\n" +
                "3. Cupos en sala: 8/8 exactos (Sobrecupo = 0).\\n" +
                "4. Webhook de Stripe: $0 de comisión cobrada por Open Break.");
        }}, 400);
      }}, 400);
    }}

    function switchCanvasTab(btn, tabMode) {{
      document.querySelectorAll('.c-tab').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const n1 = document.getElementById('node-1');
      const n2 = document.getElementById('node-2');
      const n3 = document.getElementById('node-3');
      const n4 = document.getElementById('node-4');

      if (tabMode === 'concurrency') {{
        n2.classList.add('active-node');
        n1.classList.remove('active-node');
        n3.classList.remove('active-node');
        n4.classList.remove('active-node');
      }} else if (tabMode === 'economics') {{
        n4.classList.add('active-node');
        n1.classList.remove('active-node');
        n2.classList.remove('active-node');
        n3.classList.remove('active-node');
      }} else {{
        n1.classList.add('active-node');
      }}
    }}

    function setBillingPlan(btn, planType) {{
      document.querySelectorAll('.p-toggle-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const pInicio = document.getElementById('price-val-inicio');
      const pEstudio = document.getElementById('price-val-estudio');
      const pPlus = document.getElementById('price-val-plus');

      if (planType === 'annual') {{
        pInicio.innerText = '$725';
        pEstudio.innerText = '$1,185';
        pPlus.innerText = '$1,830';
      }} else {{
        pInicio.innerText = '$790';
        pEstudio.innerText = '$1,290';
        pPlus.innerText = '$1,990';
      }}
    }}
  </script>
</body>
</html>
"""

with open('/home/user/openbreak/landing_melius_style.html', 'w', encoding='utf-8') as out:
    out.write(html)

print("Landing page successfully updated with Three.js 3D WebGL engine & draggable interactive canvas!")
