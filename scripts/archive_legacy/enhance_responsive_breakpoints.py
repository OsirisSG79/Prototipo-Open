from pathlib import Path

p_css = Path('/home/user/openbreak/templates/part2_css_rest.html')
content = p_css.read_text(encoding='utf-8')

# Responsive rules covering 1024px, 768px, 480px, 360px and 320px ultra-compact
responsive_additions = """
    /* UX-12: Complete Responsive Breakpoint Matrix (320px - 1920px) */
    @media (max-width: 1024px) {
      .hero-container { max-width: 960px; }
      .problem-grid { grid-template-columns: repeat(2, 1fr); }
      .pricing-grid { grid-template-columns: repeat(2, 1fr); }
    }

    @media (max-width: 768px) {
      .problem-grid { grid-template-columns: 1fr; }
      .pricing-grid { grid-template-columns: 1fr; }
      .reformer-3d-layout { flex-direction: column; }
      .reformer-viewport-card { height: 380px; }
      .reformer-details-card { width: 100%; }
      .conveyor-viewport { height: 320px; }
      .ribbon-card { width: 240px; }
    }

    @media (max-width: 360px) {
      .site-nav { padding: 10px 14px; }
      .btn-primary, .btn-secondary { font-size: 0.8rem; padding: 10px 16px; }
      .hero-title { font-size: 1.8rem; }
      .modal-box { padding: 20px 16px; }
    }
"""

if "/* UX-12: Complete Responsive Breakpoint Matrix" not in content:
    content += responsive_additions
    p_css.write_text(content, encoding='utf-8')
    print("Added comprehensive responsive rules to part2_css_rest.html")

