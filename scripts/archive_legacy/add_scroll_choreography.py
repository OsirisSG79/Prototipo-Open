from pathlib import Path

# 1. Add CSS in part2_css_rest.html for reveal choreographies
p_css = Path('/home/user/openbreak/templates/part2_css_rest.html')
content_css = p_css.read_text(encoding='utf-8')

scroll_css = """
    /* UX-05 / UX-09: Cinematic Scroll Reveals with Hardware Acceleration */
    .scroll-reveal-item {
      opacity: 0;
      transform: translateY(32px) scale(0.98);
      transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1), transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
      will-change: opacity, transform;
    }
    .scroll-reveal-item.is-revealed {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
    @media (prefers-reduced-motion: reduce) {
      .scroll-reveal-item {
        opacity: 1 !important;
        transform: none !important;
        transition: none !important;
      }
    }
"""

if "/* UX-05 / UX-09:" not in content_css:
    content_css += scroll_css
    p_css.write_text(content_css, encoding='utf-8')
    print("Added scroll reveal CSS to part2_css_rest.html")

# 2. Add classes to elements in part3_body_sections.html
p_body = Path('/home/user/openbreak/templates/part3_body_sections.html')
content_body = p_body.read_text(encoding='utf-8')

content_body = content_body.replace('<div class="problem-card">', '<div class="problem-card scroll-reveal-item">')
content_body = content_body.replace('<div class="pricing-card">', '<div class="pricing-card scroll-reveal-item">')
content_body = content_body.replace('<div class="pricing-card featured">', '<div class="pricing-card featured scroll-reveal-item">')
p_body.write_text(content_body, encoding='utf-8')
print("Added scroll-reveal-item classes to cards in part3_body_sections.html")

# 3. Add IntersectionObserver scroll controller in part4_js_logic.html
p_js = Path('/home/user/openbreak/templates/part4_js_logic.html')
content_js = p_js.read_text(encoding='utf-8')

observer_js = """
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
"""

if "initScrollCinematicObserver" not in content_js:
    content_js += observer_js
    p_js.write_text(content_js, encoding='utf-8')
    print("Added initScrollCinematicObserver to part4_js_logic.html")

