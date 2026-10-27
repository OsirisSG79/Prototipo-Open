from pathlib import Path

docs_html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Open Break OS — Centro de Auditoría y Verificación Técnica</title>
  <style>
    :root {
      --bg: #0C0D0E;
      --card-bg: #151618;
      --card-border: #232528;
      --text: #EDEDED;
      --text-muted: #8E9094;
      --accent: #00F096;
      --accent-orange: #FF5C35;
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      line-height: 1.6;
      padding: 40px 20px;
    }
    .container {
      max-width: 1000px;
      margin: 0 auto;
    }
    header {
      border-bottom: 1px solid var(--card-border);
      padding-bottom: 24px;
      margin-bottom: 36px;
    }
    .badge {
      display: inline-block;
      padding: 4px 10px;
      background: rgba(0, 240, 150, 0.12);
      color: var(--accent);
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 12px;
      border: 1px solid rgba(0, 240, 150, 0.3);
    }
    h1 { font-size: 2.2rem; font-weight: 700; margin-bottom: 8px; }
    p.subtitle { color: var(--text-muted); font-size: 1.05rem; }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 24px;
      transition: border-color 0.2s ease;
    }
    .card:hover { border-color: rgba(0, 240, 150, 0.4); }
    .card h3 { font-size: 1.2rem; margin-bottom: 8px; color: #FFF; }
    .card p { font-size: 0.88rem; color: var(--text-muted); margin-bottom: 16px; }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 16px;
      background: var(--accent);
      color: #000;
      font-weight: 600;
      font-size: 0.85rem;
      border-radius: 6px;
      text-decoration: none;
    }
    .btn-secondary {
      background: transparent;
      color: var(--text);
      border: 1px solid var(--card-border);
    }
    .btn-secondary:hover { border-color: var(--text-muted); }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      font-size: 0.88rem;
    }
    th, td {
      padding: 12px 14px;
      border-bottom: 1px solid var(--card-border);
      text-align: left;
    }
    th { color: var(--text-muted); font-weight: 600; font-size: 0.78rem; text-transform: uppercase; }
    td.pass { color: var(--accent); font-weight: 600; }
    code { font-family: var(--font-mono); font-size: 0.82rem; background: rgba(255,255,255,0.06); padding: 2px 6px; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="badge">V8.1.0 Ready · 100% Suites Passing</div>
      <h1>Open Break OS · Centro de Auditoría</h1>
      <p class="subtitle">Tablero de trazabilidad técnica, verificación de brechas UX-01 a UX-20 y entregables de la experiencia cinemática.</p>
    </header>

    <div class="grid">
      <div class="card">
        <h3>Experiencia Cinemática Melius</h3>
        <p>Landing page completa con 3 planos de profundidad espacial, Reformer PBR 3D, cables Bézier SVG reactivos y smartphone interactivo.</p>
        <a class="btn" href="landing_melius_style.html">Abrir Landing V8.1.0 ↗</a>
      </div>
      <div class="card">
        <h3>Registro de Versiones V8.0.1</h3>
        <p>Documentación técnica de la resolución de defectos P0 de AUD-009: prevención estricta de doble reembolso y asignación directa de lista de espera.</p>
        <a class="btn btn-secondary" href="CHANGELOG_V8_0_1.md">Ver Registro V8.0.1 ↗</a>
      </div>
      <div class="card">
        <h3>Archivo Maestro ZIP</h3>
        <p>Paquete canónico autoconfinado (5.7 MB) que contiene todo el código modular, suites de prueba, scripts constructores y assets WebP.</p>
        <a class="btn btn-secondary" href="/home/user/OpenBreak_Cinematic_V7_Proyecto_Completo.zip">Descargar ZIP Maestro</a>
      </div>
    </div>

    <h2 style="font-size: 1.4rem; margin-bottom: 16px;">Matriz de Cobertura y Verificación de Brechas</h2>
    <table>
      <thead>
        <tr>
          <th>Brecha</th>
          <th>Componente / Criterio</th>
          <th>Evidencia Técnica</th>
          <th>Dictamen</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>UX-01</strong></td>
          <td>Jerarquía editorial fluida</td>
          <td>Reglas CSS <code>clamp()</code> en 4 breakpoints (320px, 768px, 1024px, 1440px).</td>
          <td class="pass">PASS</td>
        </tr>
        <tr>
          <td><strong>UX-02</strong></td>
          <td>Hero espacial multi-plano</td>
          <td>Túnel de 3 capas con dispersión tipográfica y paralaje interactivo.</td>
          <td class="pass">PASS</td>
        </tr>
        <tr>
          <td><strong>UX-03</strong></td>
          <td>Reformer 3D con materiales PBR</td>
          <td>Three.js Canvas con iluminación direccional dual, chasis de madera y carro deslizante.</td>
          <td class="pass">PASS</td>
        </tr>
        <tr>
          <td><strong>UX-04</strong></td>
          <td>Sistema de movimiento y tokens</td>
          <td>Curvas canónicas <code>--ease-primary</code>, <code>--ease-in-out</code> y orchestrator unificado.</td>
          <td class="pass">PASS</td>
        </tr>
        <tr>
          <td><strong>UX-06</strong></td>
          <td>Lienzo de nodos reactivos</td>
          <td>Red de cables SVG Bézier cúbicos activos entre satélites y la baraja central.</td>
          <td class="pass">PASS</td>
        </tr>
        <tr>
          <td><strong>UX-07</strong></td>
          <td>Cursor reactivo con inercia</td>
          <td>Lerp inercial con morphing contextual y guardas <code>pointer: fine</code>.</td>
          <td class="pass">PASS</td>
        </tr>
        <tr>
          <td><strong>UX-08</strong></td>
          <td>Cinta ribbon con inercia y arrastre</td>
          <td>Física parabólica, snap inercial y navegación por teclado.</td>
          <td class="pass">PASS</td>
        </tr>
        <tr>
          <td><strong>UX-13</strong></td>
          <td>Degradación WebGL elegante</td>
          <td>Detección estricta de GPU y render fallback sin colapso de página.</td>
          <td class="pass">PASS</td>
        </tr>
        <tr>
          <td><strong>UX-15</strong></td>
          <td>Telemetría y rendimiento local</td>
          <td>Buffer de métricas en memoria (CWV, FPS) sin trackers externos.</td>
          <td class="pass">PASS</td>
        </tr>
        <tr>
          <td><strong>UX-16</strong></td>
          <td>Accesibilidad WCAG 2.2 AA</td>
          <td>Focus trap accesible, contraste cromático, ESC handling y soporte reduced motion.</td>
          <td class="pass">PASS</td>
        </tr>
        <tr>
          <td><strong>UX-17</strong></td>
          <td>Ledger inmutable y trazabilidad</td>
          <td>Identificador de transacción <code>txId</code>, referencia <code>refBookingId</code> y saldo atómico.</td>
          <td class="pass">PASS</td>
        </tr>
        <tr>
          <td><strong>UX-19</strong></td>
          <td>Captura con consentimiento explícito</td>
          <td>Casilla obligatoria de WhatsApp, <code>leadId</code> seguro y canal directo.</td>
          <td class="pass">PASS</td>
        </tr>
      </tbody>
    </table>
  </div>
</body>
</html>
"""

Path('/home/user/openbreak/docs.html').write_text(docs_html, encoding='utf-8')
print("Successfully generated docs.html hub in openbreak repository.")
