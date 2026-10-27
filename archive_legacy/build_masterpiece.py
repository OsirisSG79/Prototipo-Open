import json

with open('/home/user/openbreak/assets/data_uris.json') as f:
    data = json.load(f)

with open('/home/user/openbreak/assets/three.min.js') as f:
    three_min_js = f.read()

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Open Break – The Operating System for Boutique Studios</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-cream: #ECEAE4;
      --bg-cream-tint: #E5E3DD;
      --bg-black: #0B0B0C;
      --bg-card-dark: #121215;
      --border-light: rgba(0, 0, 0, 0.08);
      --border-dark: rgba(255, 255, 255, 0.12);
      --text-black: #111111;
      --text-muted-dark: #666666;
      --text-white: #FFFFFF;
      --text-muted-light: #94949E;
      --accent-orange: #FF5500;
      --accent-orange-hover: #E04B00;
      --accent-yellow: #FFF066;
      --accent-green: #10B981;
      --font-serif: 'Newsreader', Georgia, serif;
      --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; background: var(--bg-cream); }}
    body {{
      font-family: var(--font-sans);
      background-color: var(--bg-cream);
      color: var(--text-black);
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
      line-height: 1.5;
    }}

    /* ======================================================================
       1. TOP HEADER & ANNOUNCEMENT BANNER
       ====================================================================== */
    .top-announcement-banner {{
      background: var(--accent-yellow);
      color: #000000;
      font-size: 0.8rem;
      font-weight: 600;
      padding: 9px 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 12px;
      position: relative;
      z-index: 100;
    }}
    .announcement-badge {{
      background: #000000;
      color: #FFFFFF;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      letter-spacing: -0.01em;
    }}
    .announcement-link {{
      background: rgba(0, 0, 0, 0.08);
      color: #000000;
      padding: 3px 10px;
      border-radius: 999px;
      font-size: 0.76rem;
      font-weight: 700;
      text-decoration: none;
      transition: background 0.15s;
    }}
    .announcement-link:hover {{ background: rgba(0, 0, 0, 0.15); }}

    /* MAIN NAV (DARK CONTRAST AS ON MELIUS) */
    nav {{
      background: #111111;
      height: 56px;
      padding: 0 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 90;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .nav-left {{
      display: flex;
      align-items: center;
      gap: 32px;
    }}
    .nav-brand {{
      display: flex;
      align-items: center;
      gap: 8px;
      color: #FFFFFF;
      text-decoration: none;
      font-weight: 700;
      font-size: 1.05rem;
      letter-spacing: -0.03em;
    }}
    .nav-brand svg {{ color: #FFFFFF; }}
    .nav-menu {{
      display: flex;
      align-items: center;
      gap: 22px;
      list-style: none;
    }}
    .nav-menu a {{
      color: #A1A1AA;
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: color 0.15s;
    }}
    .nav-menu a:hover {{ color: #FFFFFF; }}
    .nav-menu svg {{ opacity: 0.7; }}
    .nav-right {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .btn-nav-signin {{
      background: #F4E883;
      color: #000000;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      text-decoration: none;
      transition: opacity 0.15s;
    }}
    .btn-nav-signin:hover {{ opacity: 0.9; }}
    .btn-nav-start {{
      background: var(--accent-orange);
      color: #FFFFFF;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      text-decoration: none;
      transition: background 0.15s;
    }}
    .btn-nav-start:hover {{ background: var(--accent-orange-hover); }}

    /* ======================================================================
       2. HERO SECTION WITH CURVED 3D RIBBON & DYNAMIC SERIF HEADLINE
       ====================================================================== */
    .hero-container {{
      position: relative;
      background-color: var(--bg-cream);
      padding: 50px 20px 40px;
      min-height: 840px;
      display: flex;
      flex-direction: column;
      align-items: center;
      overflow: hidden;
    }}

    /* Subtle Dot Grid Background in Cream Section */
    .hero-container::before {{
      content: "";
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      background-size: 24px 24px;
      background-image: radial-gradient(rgba(0, 0, 0, 0.06) 1px, transparent 1px);
      pointer-events: none;
      z-index: 1;
    }}

    /* DYNAMIC SERIF HEADLINE (IDENTICAL TO MELIUS RECKLESS STANDARD FONT) */
    .hero-title-area {{
      position: relative;
      z-index: 15;
      text-align: center;
      margin-bottom: 25px;
    }}
    .hero-serif-title {{
      font-family: var(--font-serif);
      font-size: clamp(3.2rem, 6.2vw, 5.6rem);
      font-weight: 400;
      letter-spacing: -0.035em;
      color: var(--text-black);
      line-height: 1.05;
      margin-bottom: 10px;
    }}
    .hero-serif-title .rotating-word {{
      display: inline-block;
      font-style: italic;
      color: var(--accent-orange);
      transition: all 0.4s ease;
    }}

    /* 3D PARABOLIC KINETIC RIBBON */
    .ribbon-stage {{
      position: relative;
      width: 100%;
      max-width: 1400px;
      height: 380px;
      margin: 10px auto 30px;
      perspective: 1200px;
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 5;
    }}
    .ribbon-track {{
      position: absolute;
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      transform-style: preserve-3d;
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .ribbon-card {{
      position: absolute;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 16px 35px rgba(0, 0, 0, 0.18), 0 3px 10px rgba(0, 0, 0, 0.1);
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      cursor: pointer;
      background: #000000;
    }}
    .ribbon-card img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.5s ease;
    }}
    .ribbon-card:hover {{
      transform: translateY(-10px) scale(1.08) !important;
      box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
      z-index: 40 !important;
    }}
    .ribbon-card:hover img {{
      transform: scale(1.08);
    }}

    /* HERO SUBTEXT & FLOATING PILL SEARCH BAR (MELIUS SEARCH BAR) */
    .hero-bottom-area {{
      position: relative;
      z-index: 20;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      max-width: 620px;
      margin-top: 10px;
    }}
    .hero-subtext {{
      font-size: 1.05rem;
      color: #333333;
      line-height: 1.5;
      margin-bottom: 24px;
      letter-spacing: -0.01em;
    }}

    .hero-prompt-pill {{
      background: #27272A;
      color: #FFFFFF;
      border-radius: 999px;
      padding: 6px 8px 6px 20px;
      display: flex;
      align-items: center;
      gap: 12px;
      width: 100%;
      max-width: 440px;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.1);
      transition: all 0.2s;
    }}
    .hero-prompt-pill:focus-within {{
      border-color: var(--accent-orange);
      box-shadow: 0 15px 40px rgba(255, 85, 0, 0.25);
    }}
    .pill-icon {{
      color: #A1A1AA;
      display: flex;
      align-items: center;
    }}
    .pill-input {{
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      color: #FFFFFF;
      font-family: var(--font-sans);
      font-size: 0.9rem;
    }}
    .pill-action-btn {{
      background: #3F3F46;
      border: none;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      color: #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: background 0.15s;
    }}
    .pill-action-btn:hover {{
      background: var(--accent-orange);
    }}

    /* TRUSTED CREATIVES BAR */
    .trusted-bar {{
      position: relative;
      z-index: 10;
      width: 100%;
      max-width: 1200px;
      margin-top: 50px;
      padding-top: 30px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .trusted-label {{
      font-size: 0.8rem;
      color: #71717A;
      margin-bottom: 18px;
      font-weight: 500;
    }}
    .trusted-logos {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 36px;
      flex-wrap: wrap;
      opacity: 0.65;
    }}
    .t-logo {{
      font-size: 0.95rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: #27272A;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    /* ======================================================================
       3. DARK INFINITE CANVAS SECTION (MELIUS NODE CANVAS)
       ====================================================================== */
    .canvas-section {{
      background-color: var(--bg-black);
      color: var(--text-white);
      padding: 90px 24px 120px;
      position: relative;
    }}
    .canvas-container {{
      max-width: 1360px;
      margin: 0 auto;
    }}

    .canvas-top-bar {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 28px;
      flex-wrap: wrap;
      gap: 20px;
    }}
    .canvas-title-group h2 {{
      font-size: 2.2rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      margin-bottom: 6px;
    }}
    .canvas-title-group p {{
      color: var(--text-muted-light);
      font-size: 0.95rem;
    }}

    /* CANVAS TABS (IDENTICAL TO MELIUS SOLUTIONS TABS) */
    .canvas-tabs-switcher {{
      display: flex;
      background: #18181B;
      border: 1px solid var(--border-dark);
      border-radius: 8px;
      padding: 4px;
      gap: 4px;
    }}
    .c-tab-btn {{
      background: transparent;
      border: none;
      color: #A1A1AA;
      font-family: var(--font-sans);
      font-size: 0.82rem;
      font-weight: 600;
      padding: 7px 18px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .c-tab-btn:hover {{ color: #FFFFFF; }}
    .c-tab-btn.active {{
      background: #27272A;
      color: #FFFFFF;
      box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    }}

    /* INFINITE CANVAS WORKSPACE BOARD */
    .infinite-board {{
      position: relative;
      background: #09090B;
      border: 1px solid var(--border-dark);
      border-radius: 20px;
      height: 720px;
      overflow: hidden;
      box-shadow: 0 40px 90px -20px rgba(0, 0, 0, 0.95);
      user-select: none;
    }}
    /* Dot Grid Background in Dark Canvas */
    .infinite-board::before {{
      content: "";
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      background-size: 26px 26px;
      background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px);
      pointer-events: none;
      z-index: 1;
    }}

    /* HUD OVERLAY */
    .canvas-hud {{
      position: absolute;
      top: 18px;
      left: 20px;
      z-index: 20;
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(24, 24, 27, 0.85);
      border: 1px solid var(--border-dark);
      backdrop-filter: blur(14px);
      padding: 6px 14px;
      border-radius: 8px;
      font-family: var(--font-mono);
      font-size: 0.74rem;
      color: #A1A1AA;
    }}
    .hud-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--accent-green);
      box-shadow: 0 0 8px var(--accent-green);
    }}

    /* SVG WIRES */
    .canvas-wires-layer {{
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      pointer-events: none;
      z-index: 5;
    }}

    /* DRAGGABLE NODES (MELIUS GRAPH CARDS) */
    .graph-node {{
      position: absolute;
      z-index: 10;
      background: var(--bg-card-dark);
      border: 1px solid var(--border-dark);
      border-radius: 14px;
      width: 295px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.7);
      cursor: grab;
      transition: border-color 0.2s, box-shadow 0.2s, transform 0.15s ease-out;
      overflow: hidden;
    }}
    .graph-node:active {{ cursor: grabbing; }}
    .graph-node:hover {{
      border-color: rgba(255, 255, 255, 0.4);
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9), 0 0 25px rgba(255, 85, 0, 0.2);
    }}
    .graph-node.active-node {{
      border-color: var(--accent-orange);
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9), 0 0 35px rgba(255, 85, 0, 0.35);
    }}

    .node-header {{
      padding: 10px 14px 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: #A1A1AA;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }}
    .node-pill {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.68rem;
      font-weight: 700;
    }}
    .pill-booking {{ background: rgba(56, 189, 248, 0.15); color: #38BDF8; }}
    .pill-atomic {{ background: rgba(239, 68, 68, 0.15); color: #F87171; }}
    .pill-credits {{ background: rgba(250, 204, 21, 0.15); color: #FDE047; }}
    .pill-stripe {{ background: rgba(34, 197, 94, 0.15); color: #4ADE80; }}

    .node-content {{ padding: 12px 14px; }}
    .node-title {{
      font-size: 0.95rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 6px;
      color: #FFFFFF;
    }}
    .node-desc {{
      font-size: 0.8rem;
      color: var(--text-muted-light);
      line-height: 1.4;
      margin-bottom: 10px;
    }}
    .node-preview-media {{
      width: 100%;
      height: 148px;
      border-radius: 8px;
      overflow: hidden;
      background: #000000;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .node-preview-media img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.4s ease;
    }}
    .graph-node:hover .node-preview-media img {{
      transform: scale(1.06);
    }}
    .node-code {{
      background: #060608;
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 8px;
      padding: 10px 12px;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: #A1A1AA;
      line-height: 1.5;
    }}

    /* CONNECTION PORTS */
    .node-port {{
      width: 10px;
      height: 10px;
      background: #FFFFFF;
      border: 2px solid #000000;
      border-radius: 50%;
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
    }}
    .port-left {{ left: -5px; }}
    .port-right {{ right: -5px; }}

    /* TELEMETRY METRICS ROW */
    .canvas-metrics-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-top: 24px;
    }}
    @media (max-width: 900px) {{
      .canvas-metrics-row {{ grid-template-columns: 1fr 1fr; }}
    }}
    .metric-box {{
      background: #121215;
      border: 1px solid var(--border-dark);
      border-radius: 12px;
      padding: 18px 20px;
    }}
    .metric-box .num {{
      font-size: 1.7rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      margin-bottom: 4px;
    }}
    .metric-box .label {{
      font-size: 0.78rem;
      color: var(--text-muted-light);
    }}

    /* ======================================================================
       4. SOLUTIONS SECTION (3 BOUTIQUE VERTICALS)
       ====================================================================== */
    .solutions-section {{
      background: #0B0B0D;
      color: #FFFFFF;
      padding: 80px 24px 120px;
      border-top: 1px solid var(--border-dark);
    }}
    .solutions-container {{
      max-width: 1280px;
      margin: 0 auto;
    }}
    .section-eyebrow {{
      font-family: var(--font-mono);
      font-size: 0.74rem;
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
      background: #141417;
      border: 1px solid var(--border-dark);
      border-radius: 18px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: all 0.3s;
    }}
    .sol-card:hover {{
      border-color: rgba(255, 255, 255, 0.35);
      transform: translateY(-5px);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.8);
    }}
    .sol-img-box {{
      height: 230px;
      position: relative;
      overflow: hidden;
    }}
    .sol-img-box img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.5s ease;
    }}
    .sol-card:hover .sol-img-box img {{
      transform: scale(1.06);
    }}
    .sol-content {{
      padding: 24px;
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
    .sol-desc {{
      color: var(--text-muted-light);
      font-size: 0.88rem;
      line-height: 1.55;
      margin-bottom: 20px;
    }}
    .sol-chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .sol-chip {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      padding: 3px 8px;
      border-radius: 4px;
      color: #A1A1AA;
    }}

    /* ======================================================================
       5. PRICING SECTION (MELIUS CARD DESIGN)
       ====================================================================== */
    .pricing-section {{
      background: var(--bg-black);
      color: #FFFFFF;
      padding: 80px 24px 140px;
      border-top: 1px solid var(--border-dark);
    }}
    .pricing-container {{
      max-width: 1220px;
      margin: 0 auto;
    }}

    .pricing-toggle-wrap {{
      display: flex;
      justify-content: center;
      margin-bottom: 48px;
    }}
    .pricing-toggle {{
      background: #18181B;
      border: 1px solid var(--border-dark);
      border-radius: 999px;
      padding: 4px;
      display: flex;
      gap: 4px;
    }}
    .p-toggle-btn {{
      background: transparent;
      border: none;
      color: #A1A1AA;
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
    .p-card {{
      background: #141417;
      border: 1px solid var(--border-dark);
      border-radius: 20px;
      padding: 38px 30px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      transition: all 0.25s;
    }}
    .p-card:hover {{
      border-color: rgba(255, 255, 255, 0.3);
      transform: translateY(-4px);
    }}
    .p-card.featured {{
      border-color: var(--accent-orange);
      background: linear-gradient(180deg, rgba(255, 85, 0, 0.08) 0%, #141417 100%);
      box-shadow: 0 0 50px rgba(255, 85, 0, 0.2);
    }}
    .p-featured-badge {{
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

    .p-plan-name {{
      font-size: 1.3rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }}
    .p-plan-summary {{
      color: var(--text-muted-light);
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
    .p-price-number {{
      font-size: 3.3rem;
      font-weight: 800;
      letter-spacing: -0.04em;
    }}
    .p-price-sub {{
      color: var(--text-muted-light);
      font-size: 0.95rem;
    }}
    .p-price-terms {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: #71717A;
      margin-bottom: 28px;
    }}
    .p-features {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 13px;
      margin-bottom: 32px;
      font-size: 0.88rem;
    }}
    .p-features li {{
      display: flex;
      align-items: flex-start;
      gap: 10px;
      color: #E4E4E7;
    }}
    .p-features li svg {{
      flex-shrink: 0;
      margin-top: 3px;
      color: var(--accent-orange);
    }}

    .btn-plan {{
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 11px;
      border-radius: 8px;
      font-size: 0.88rem;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.15s;
    }}
    .btn-plan-ghost {{
      background: rgba(255, 255, 255, 0.06);
      color: #FFFFFF;
      border: 1px solid var(--border-dark);
    }}
    .btn-plan-ghost:hover {{
      background: rgba(255, 255, 255, 0.12);
    }}
    .btn-plan-solid {{
      background: var(--accent-orange);
      color: #FFFFFF;
      border: none;
    }}
    .btn-plan-solid:hover {{
      background: var(--accent-orange-hover);
    }}

    /* FOOTER */
    footer {{
      background: #09090B;
      border-top: 1px solid var(--border-dark);
      padding: 50px 24px 30px;
      font-size: 0.85rem;
      color: #71717A;
    }}
    .footer-inner {{
      max-width: 1280px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
  </style>
</head>
<body>

  <!-- TOP BANNER (MELIUS SEED/ANNOUNCEMENT EXACT STYLE) -->
  <div class="top-announcement-banner">
    <span class="announcement-badge">MÉXICO 2026</span>
    <span>Lanzamiento de Open Break: El sistema operativo de movimiento para estudios boutique independientes.</span>
    <a href="#pricing" class="announcement-link">Ver Cupos Piloto →</a>
  </div>

  <!-- NAVIGATION -->
  <nav>
    <div class="nav-left">
      <a href="#" class="nav-brand">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        <span>Open Break</span>
      </a>

      <ul class="nav-menu">
        <li><a href="#canvas-section">Operational Canvas</a></li>
        <li><a href="#solutions">Estudios Boutique</a></li>
        <li><a href="#pricing">Tarifas 2026</a></li>
        <li><a href="prototype.html" target="_blank">Simulador UX ↗</a></li>
      </ul>
    </div>

    <div class="nav-right">
      <a href="prototype.html" class="btn-nav-signin">Ver Demo</a>
      <a href="#pricing" class="btn-nav-start">Comenzar Piloto</a>
    </div>
  </nav>

  <!-- ======================================================================
       HERO: CREATIVE 3D PARABOLIC RIBBON & SERIF HEADLINE (MELIUS SIGNATURE)
       ====================================================================== -->
  <section class="hero-container" id="hero">
    
    <!-- ROTATING SERIF HEADLINE -->
    <div class="hero-title-area">
      <h1 class="hero-serif-title">
        Create any <span class="rotating-word" id="rotatingWord">studio</span> you imagine
      </h1>
    </div>

    <!-- 3D PARABOLIC HORIZONTAL RIBBON OF CURVED STUDIO IMAGES -->
    <div class="ribbon-stage" id="ribbonStage">
      <div class="ribbon-track" id="ribbonTrack">
        <!-- Card 1 (Far Left) -->
        <div class="ribbon-card" style="width: 170px; height: 260px; left: calc(50% - 660px); transform: rotateY(38deg) translateZ(40px);">
          <img src="{data['ribbon_1']}" alt="Pilates Reformer Light">
        </div>
        <!-- Card 2 -->
        <div class="ribbon-card" style="width: 165px; height: 235px; left: calc(50% - 470px); transform: rotateY(26deg) translateZ(15px);">
          <img src="{data['studio_hero']}" alt="Pilates Studio">
        </div>
        <!-- Card 3 -->
        <div class="ribbon-card" style="width: 160px; height: 215px; left: calc(50% - 295px); transform: rotateY(14deg) translateZ(0px);">
          <img src="{data['coach_guiding']}" alt="Coach guiding client">
        </div>
        <!-- Card 4 (Center - Flat) -->
        <div class="ribbon-card" style="width: 155px; height: 195px; left: calc(50% - 130px); transform: rotateY(0deg) translateZ(-10px);">
          <img src="{data['ribbon_3']}" alt="Minimal studio interior">
        </div>
        <!-- Card 5 (Center Right) -->
        <div class="ribbon-card" style="width: 155px; height: 195px; left: calc(50% + 35px); transform: rotateY(-10deg) translateZ(-5px);">
          <img src="{data['class_action']}" alt="Group Reformer Class">
        </div>
        <!-- Card 6 -->
        <div class="ribbon-card" style="width: 160px; height: 215px; left: calc(50% + 200px); transform: rotateY(-20deg) translateZ(10px);">
          <img src="{data['studio_minimal']}" alt="Yoga Minimal Room">
        </div>
        <!-- Card 7 -->
        <div class="ribbon-card" style="width: 165px; height: 235px; left: calc(50% + 370px); transform: rotateY(-30deg) translateZ(25px);">
          <img src="{data['ribbon_4']}" alt="Black and White Pilates">
        </div>
        <!-- Card 8 (Far Right) -->
        <div class="ribbon-card" style="width: 170px; height: 260px; left: calc(50% + 550px); transform: rotateY(-40deg) translateZ(45px);">
          <img src="{data['ribbon_2']}" alt="Luxury Studio Design">
        </div>
      </div>
    </div>

    <!-- SUBTEXT & MELIUS SEARCH / PROMPT PILL -->
    <div class="hero-bottom-area">
      <p class="hero-subtext">
        El sistema operativo definitivo para estudios boutique de movimiento.<br>
        Reserva atómica sin sobrecupos, paquetes de créditos inmutables y 0% de comisión sobre ventas.
      </p>

      <div class="hero-prompt-pill">
        <div class="pill-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
        </div>
        <input type="text" class="pill-input" id="heroPromptInput" value="Simular: 2 alumnos reservando el último Reformer a las 07:00 AM">
        <button class="pill-action-btn" onclick="triggerSimulation()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
        </button>
      </div>
    </div>

    <!-- TRUSTED CREATIVES / STUDIOS BAR -->
    <div class="trusted-bar">
      <div class="trusted-label">Trusted by boutique movement directors & studios in Mexico</div>
      <div class="trusted-logos">
        <div class="t-logo">REFORMER BOTANICAL</div>
        <div class="t-logo">LUNA PILATES ROMA</div>
        <div class="t-logo">BARRE & SCULPT CONDESA</div>
        <div class="t-logo">CADILLAC PRECISION</div>
        <div class="t-logo">SOLARIS MOVEMENT</div>
      </div>
    </div>

  </section>

  <!-- ======================================================================
       3. DARK INFINITE OPERATIONAL CANVAS (NODE-BASED WORKSPACE)
       ====================================================================== -->
  <section class="canvas-section" id="canvas-section">
    <div class="canvas-container">
      
      <div class="canvas-top-bar">
        <div class="canvas-title-group">
          <h2>Infinite Operational Canvas</h2>
          <p>Un grafo de ejecución donde cada nodo resuelve un proceso crítico de tu estudio en tiempo real.</p>
        </div>

        <div class="canvas-tabs-switcher">
          <button class="c-tab-btn active" onclick="switchCanvasMode(this, 'all')">Grafo Completo</button>
          <button class="c-tab-btn" onclick="switchCanvasMode(this, 'concurrency')">Test de Concurrencia</button>
          <button class="c-tab-btn" onclick="switchCanvasMode(this, 'economics')">Conciliación 0% Fee</button>
        </div>
      </div>

      <!-- WORKSPACE BOARD WITH DRAGGABLE NODES & REAL-TIME BEZIER SVG WIRES -->
      <div class="infinite-board" id="canvasBoard">
        
        <!-- TELEMETRY HUD -->
        <div class="canvas-hud">
          <div class="hud-dot"></div>
          <span>PG_ISOLATION: READ COMMITTED</span>
          <span>·</span>
          <span>STRIPE CONNECT: 0.00% CUT</span>
          <span>·</span>
          <span style="color: #FFFFFF;">4 ACTIVE NODES</span>
        </div>

        <!-- SVG WIRES LAYER -->
        <svg class="canvas-wires-layer" id="wiresSvg">
          <path id="wire-1-2" d="" stroke="rgba(255, 255, 255, 0.3)" stroke-width="2" fill="none" stroke-dasharray="5,5"/>
          <path id="wire-2-3" d="" stroke="rgba(255, 255, 255, 0.3)" stroke-width="2" fill="none" stroke-dasharray="5,5"/>
          <path id="wire-3-4" d="" stroke="rgba(255, 85, 0, 0.75)" stroke-width="2.5" fill="none"/>
        </svg>

        <!-- NODE 1: STUDENT UI -->
        <div class="graph-node active-node" id="node-1" style="left: 40px; top: 90px;">
          <div class="node-header">
            <span>NODE // 01</span>
            <span class="node-pill pill-booking">STUDENT UI</span>
          </div>
          <div class="node-content">
            <div class="node-title">Reserva Web Móvil (3-Tap)</div>
            <div class="node-desc">El alumno reserva desde Instagram o WhatsApp sin instalar apps pesadas.</div>
            <div class="node-preview-media">
              <img src="{data['coach_guiding']}" alt="Pilates Reformer Class">
            </div>
          </div>
          <div class="node-port port-right" id="p1-out"></div>
        </div>

        <!-- NODE 2: CONCURRENCY LOCK -->
        <div class="graph-node" id="node-2" style="left: 430px; top: 50px;">
          <div class="node-port port-left" id="p2-in"></div>
          <div class="node-header">
            <span>NODE // 02</span>
            <span class="node-pill pill-atomic">ATOMIC LOCK</span>
          </div>
          <div class="node-content">
            <div class="node-title">Bloqueo Atómico SQL</div>
            <div class="node-desc">Previene colisiones si 2 alumnos intentan ganar el último reformer al mismo instante.</div>
            <div class="node-code">
              <span style="color: #38BDF8;">BEGIN TRANSACTION;</span><br>
              <span style="color: #FACC15;">SELECT</span> * <span style="color: #FACC15;">FROM</span> session_spots<br>
              <span style="color: #F87171;">WHERE</span> spot_id = 'reformer_08'<br>
              <span style="color: #4ADE80; font-weight:700;">FOR UPDATE;</span><br>
              <span style="color: #94A3B8;">// Sobrecupo = 0</span>
            </div>
          </div>
          <div class="node-port port-right" id="p2-out"></div>
        </div>

        <!-- NODE 3: CREDIT AUDIT -->
        <div class="graph-node" id="node-3" style="left: 820px; top: 160px;">
          <div class="node-port port-left" id="p3-in"></div>
          <div class="node-header">
            <span>NODE // 03</span>
            <span class="node-pill pill-credits">CREDIT AUDIT</span>
          </div>
          <div class="node-content">
            <div class="node-title">Bitácora de Créditos Inmutable</div>
            <div class="node-desc">Resta 1 crédito. Si cancela con >6h de aviso, repone de inmediato y promueve lista de espera.</div>
            <div class="node-preview-media">
              <img src="{data['studio_light']}" alt="Studio Reformer Room">
            </div>
          </div>
          <div class="node-port port-right" id="p3-out"></div>
        </div>

        <!-- NODE 4: STRIPE DIRECT 0% FEE -->
        <div class="graph-node" id="node-4" style="left: 1010px; top: 380px;">
          <div class="node-port port-left" id="p4-in"></div>
          <div class="node-header">
            <span>NODE // 04</span>
            <span class="node-pill pill-stripe">STRIPE DIRECT</span>
          </div>
          <div class="node-content">
            <div class="node-title">Cobro Directo 0% Comisión</div>
            <div class="node-desc">El dinero va directo a tu cuenta bancaria. Open Break no descuenta comisiones sobre ventas.</div>
            <div class="node-code">
              Destination: <span style="color: #FFFFFF;">acct_studio_boutique</span><br>
              Open Break Cut: <span style="color: #4ADE80; font-weight: 700;">0.00%</span><br>
              Idempotency: <span style="color: #FACC15;">Verified</span>
            </div>
          </div>
        </div>

      </div>

      <!-- CANVAS BOTTOM METRICS -->
      <div class="canvas-metrics-row">
        <div class="metric-box">
          <div class="num" style="color: var(--accent-green);">0.00%</div>
          <div class="label">Tasa de sobrecupo físico comprobada en salas</div>
        </div>
        <div class="metric-box">
          <div class="num">$0 MXN</div>
          <div class="label">Comisión propia sobre tus paquetes vendidos</div>
        </div>
        <div class="metric-box">
          <div class="num" style="color: var(--accent-orange);">6 Horas</div>
          <div class="label">Ventana configurada para proteger pago de profesores</div>
        </div>
        <div class="metric-box">
          <div class="num">< 15 segs</div>
          <div class="label">Tiempo promedio en reservar desde web móvil</div>
        </div>
      </div>

    </div>
  </section>

  <!-- ======================================================================
       4. SOLUTIONS SECTION (3 BOUTIQUE VERTICALS)
       ====================================================================== -->
  <section class="solutions-section" id="solutions">
    <div class="solutions-container">
      <div class="section-eyebrow">Verticales de Movimiento</div>
      <h2 class="section-headline">Un sistema calibrado para la realidad de cada disciplina boutique.</h2>

      <div class="solutions-grid">
        
        <!-- Card 1 -->
        <div class="sol-card">
          <div class="sol-img-box">
            <img src="{data['studio_hero']}" alt="Reformer Pilates Studio">
          </div>
          <div class="sol-content">
            <div>
              <h3 class="sol-title">Reformer & Cadillac Pilates</h3>
              <p class="sol-desc">
                Control riguroso de máquinas individuales (ej. 8 a 12 reformers). Si un cliente cancela a tiempo, el lugar se asigna automáticamente a quien encabeza la lista de espera.
              </p>
            </div>
            <div class="sol-chips">
              <span class="sol-chip">Cupo Máximo 12</span>
              <span class="sol-chip">Waitlist Auto</span>
              <span class="sol-chip">No-Shows = $0 Pérdida</span>
            </div>
          </div>
        </div>

        <!-- Card 2 -->
        <div class="sol-card">
          <div class="sol-img-box">
            <img src="{data['class_action']}" alt="Barre Movement">
          </div>
          <div class="sol-content">
            <div>
              <h3 class="sol-title">Barre, Danza & Mat Flow</h3>
              <p class="sol-desc">
                Gestión de salas de mayor aforo con niveles diferenciados y cálculo de honorarios de maestros por alumno asistente o cuota fija por sesión.
              </p>
            </div>
            <div class="sol-chips">
              <span class="sol-chip">Comisión por Instructor</span>
              <span class="sol-chip">Check-in 1-Tap</span>
              <span class="sol-chip">Membresías Recurrentes</span>
            </div>
          </div>
        </div>

        <!-- Card 3 -->
        <div class="sol-card">
          <div class="sol-img-box">
            <img src="{data['studio_minimal']}" alt="Yoga Minimal Room">
          </div>
          <div class="sol-content">
            <div>
              <h3 class="sol-title">Yoga & Mindfulness Spaces</h3>
              <p class="sol-desc">
                Paquetes combinados de sesiones grupales, talleres de fin de semana y pases drop-in sin fricción para practicantes recurrentes o de paso.
              </p>
            </div>
            <div class="sol-chips">
              <span class="sol-chip">Drop-in Digital</span>
              <span class="sol-chip">Pases Múltiples</span>
              <span class="sol-chip">Conciliación CSV</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- ======================================================================
       5. PRICING TABLE (2026 TRANSPARENT TIERS)
       ====================================================================== -->
  <section class="pricing-section" id="pricing">
    <div class="pricing-container">
      <div class="section-eyebrow">Tarifas Transparentes 2026</div>
      <h2 class="section-headline">Cuotas fijas predecibles. Sin comisiones sorpresa al fin de mes.</h2>

      <div class="pricing-toggle-wrap">
        <div class="pricing-toggle">
          <button class="p-toggle-btn active" onclick="setBillingToggle(this, 'monthly')">Facturación Mensual</button>
          <button class="p-toggle-btn" onclick="setBillingToggle(this, 'annual')">Anual (8% Ahorro)</button>
        </div>
      </div>

      <div class="pricing-grid">
        
        <!-- Plan Inicio -->
        <div class="p-card">
          <div>
            <div class="p-plan-name">Inicio</div>
            <div class="p-plan-summary">Para estudios boutique de 1 sala que quieren dejar atrás las hojas de cálculo y la conciliación por WhatsApp.</div>
            <div class="p-price-row">
              <span class="p-price-number" id="price-inicio">$790</span>
              <span class="p-price-sub">MXN / mes</span>
            </div>
            <div class="p-price-terms">+ IVA · $990 MXN setup guiado</div>
            <ul class="p-features">
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> 1 Sede física</li>
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Hasta 120 alumnos activos</li>
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> 2 Instructores</li>
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Hasta 600 reservas al mes</li>
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> <strong>0% comisión propia de ventas</strong></li>
            </ul>
          </div>
          <a href="prototype.html" class="btn-plan btn-plan-ghost">Elegir Inicio</a>
        </div>

        <!-- Plan Estudio (Featured) -->
        <div class="p-card featured">
          <span class="p-featured-badge">Recomendado</span>
          <div>
            <div class="p-plan-name">Estudio</div>
            <div class="p-plan-summary">El estándar para estudios consolidados con alta demanda de reservas, lista de espera y profesores rotativos.</div>
            <div class="p-price-row">
              <span class="p-price-number" id="price-estudio">$1,290</span>
              <span class="p-price-sub">MXN / mes</span>
            </div>
            <div class="p-price-terms">+ IVA · $2,490 MXN setup e importación</div>
            <ul class="p-features">
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> 1 Sede con hasta 3 salas</li>
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Hasta 300 alumnos activos</li>
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Hasta 8 instructores con cálculo de honorarios</li>
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Hasta 2,000 reservas al mes</li>
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> <strong>Lista de espera automatizada</strong></li>
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Check-in táctil de recepción</li>
            </ul>
          </div>
          <a href="prototype.html" class="btn-plan btn-plan-solid">Comenzar Piloto</a>
        </div>

        <!-- Plan Plus -->
        <div class="p-card">
          <div>
            <div class="p-plan-name">Plus / Multi-sede</div>
            <div class="p-plan-summary">Para cadenas de estudios en expansión que requieren analítica consolidada y exportación contable.</div>
            <div class="p-price-row">
              <span class="p-price-number" id="price-plus">$1,990</span>
              <span class="p-price-sub">MXN / mes</span>
            </div>
            <div class="p-price-terms">+ IVA · Migración multi-sucursal guiada</div>
            <ul class="p-features">
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Hasta 2 sedes activas</li>
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> 700 alumnos activos</li>
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Instructores ilimitados</li>
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> Hasta 5,000 reservas al mes</li>
              <li><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg> API & Conciliación bancaria avanzada</li>
            </ul>
          </div>
          <a href="prototype.html" class="btn-plan btn-plan-ghost">Contactar Soporte</a>
        </div>

      </div>
    </div>
  </section>

  <!-- FOOTER -->
  <footer>
    <div class="footer-inner">
      <div>
        <strong style="color: #FFFFFF;">Open Break</strong>
        <span> · The Operating System for Movement Studios</span>
      </div>
      <div>
        <span>0% Platform Commission · PostgreSQL Row-Level Atomic Engine · Mexico 2026</span>
      </div>
    </div>
  </footer>

  <!-- ======================================================================
       INTERACTIVE SCRIPTS: 3D RIBBON PARALLAX, ROTATING WORDS, DRAGGABLE NODES
       ====================================================================== -->
  <script>
    // 1. ROTATING SERIF HEADLINE WORDS (STUDIO, CAMPAIGN, CLASS, MOVEMENT)
    const words = ['studio', 'movement', 'academy', 'reformer'];
    let wordIndex = 0;
    const rotatingWordEl = document.getElementById('rotatingWord');

    setInterval(() => {{
      wordIndex = (wordIndex + 1) % words.length;
      rotatingWordEl.style.opacity = '0';
      rotatingWordEl.style.transform = 'translateY(12px)';
      
      setTimeout(() => {{
        rotatingWordEl.innerText = words[wordIndex];
        rotatingWordEl.style.opacity = '1';
        rotatingWordEl.style.transform = 'translateY(0)';
      }}, 250);
    }}, 2600);

    // 2. PARABOLIC RIBBON INTERACTIVE MOUSE PARALLAX (3D TILT EFFECT)
    const ribbonStage = document.getElementById('ribbonStage');
    const ribbonTrack = document.getElementById('ribbonTrack');

    if (ribbonStage && ribbonTrack) {{
      window.addEventListener('mousemove', (e) => {{
        const xOffset = (e.clientX / window.innerWidth - 0.5) * 36;
        const yOffset = (e.clientY / window.innerHeight - 0.5) * 14;
        ribbonTrack.style.transform = `rotateY(${{xOffset * 0.4}}deg) rotateX(${{-yOffset * 0.5}}deg) translateX(${{xOffset * 1.2}}px)`;
      }});
    }}

    // 3. CANVAS DRAGGABLE NODES & REAL-TIME BEZIER SVG WIRES
    function updateWires() {{
      const b1_2 = document.getElementById('wire-1-2');
      const b2_3 = document.getElementById('wire-2-3');
      const b3_4 = document.getElementById('wire-3-4');

      const boardRect = document.getElementById('canvasBoard').getBoundingClientRect();

      const p1 = getPortCenter('p1-out', boardRect);
      const p2In = getPortCenter('p2-in', boardRect);
      const p2Out = getPortCenter('p2-out', boardRect);
      const p3In = getPortCenter('p3-in', boardRect);
      const p3Out = getPortCenter('p3-out', boardRect);
      const p4In = getPortCenter('p4-in', boardRect);

      if (b1_2) b1_2.setAttribute('d', makeBezier(p1, p2In));
      if (b2_3) b2_3.setAttribute('d', makeBezier(p2Out, p3In));
      if (b3_4) b3_4.setAttribute('d', makeBezier(p3Out, p4In));
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

    function makeBezier(from, to) {{
      const dx = Math.abs(to.x - from.x) * 0.55;
      return `M ${{from.x}} ${{from.y}} C ${{from.x + dx}} ${{from.y}}, ${{to.x - dx}} ${{to.y}}, ${{to.x}} ${{to.y}}`;
    }}

    function initDraggableNodes() {{
      const nodes = document.querySelectorAll('.graph-node');
      const board = document.getElementById('canvasBoard');

      nodes.forEach(node => {{
        let isDragging = false;
        let startX, startY, origX, origY;

        node.addEventListener('mousedown', (e) => {{
          if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A') return;
          isDragging = true;
          startX = e.clientX;
          startY = e.clientY;
          origX = node.offsetLeft;
          origY = node.offsetTop;
          
          nodes.forEach(n => n.classList.remove('active-node'));
          node.classList.add('active-node');
          node.style.zIndex = '25';
          e.preventDefault();
        }});

        window.addEventListener('mousemove', (e) => {{
          if (!isDragging) return;
          const dx = e.clientX - startX;
          const dy = e.clientY - startY;
          
          let newX = origX + dx;
          let newY = origY + dy;

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
      setTimeout(updateWires, 100);
    }}

    // 4. SIMULATION PROMPT TRIGGER
    function triggerSimulation() {{
      const node2 = document.getElementById('node-2');
      const node3 = document.getElementById('node-3');

      node2.classList.add('active-node');
      node2.style.transform = 'scale(1.06)';
      
      setTimeout(() => {{
        node2.style.transform = '';
        node3.classList.add('active-node');
        node3.style.transform = 'scale(1.06)';

        setTimeout(() => {{
          node3.style.transform = '';
          alert("⚡ SIMULACIÓN EJECUTADA:\\n\\n" +
                "1. Alumno 1 adquiere el último Reformer libre mediante transacción atómica SQL.\\n" +
                "2. Alumno 2 es asignado a Waitlist #1 instantáneamente.\\n" +
                "3. Sobrecupo físico en sala: 0% (Exactitud total).\\n" +
                "4. Webhook Stripe Connect: 0% comisión retenida por Open Break.");
        }}, 400);
      }}, 400);
    }}

    function switchCanvasMode(btn, mode) {{
      document.querySelectorAll('.c-tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const n1 = document.getElementById('node-1');
      const n2 = document.getElementById('node-2');
      const n3 = document.getElementById('node-3');
      const n4 = document.getElementById('node-4');

      if (mode === 'concurrency') {{
        n2.classList.add('active-node');
        n1.classList.remove('active-node');
        n3.classList.remove('active-node');
        n4.classList.remove('active-node');
      }} else if (mode === 'economics') {{
        n4.classList.add('active-node');
        n1.classList.remove('active-node');
        n2.classList.remove('active-node');
        n3.classList.remove('active-node');
      }} else {{
        n1.classList.add('active-node');
      }}
    }}

    function setBillingToggle(btn, type) {{
      document.querySelectorAll('.p-toggle-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const pInicio = document.getElementById('price-inicio');
      const pEstudio = document.getElementById('price-estudio');
      const pPlus = document.getElementById('price-plus');

      if (type === 'annual') {{
        pInicio.innerText = '$725';
        pEstudio.innerText = '$1,185';
        pPlus.innerText = '$1,830';
      }} else {{
        pInicio.innerText = '$790';
        pEstudio.innerText = '$1,290';
        pPlus.innerText = '$1,990';
      }}
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      initDraggableNodes();
    }});
  </script>
</body>
</html>
"""

with open('/home/user/openbreak/landing_melius_style.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Masterpiece landing page built successfully!")
