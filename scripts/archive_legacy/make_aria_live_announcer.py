from pathlib import Path

# 1. Add global ARIA live status region for assistive technologies into templates/part3_body_sections.html
p_body = Path('/home/user/openbreak/templates/part3_body_sections.html')
content_body = p_body.read_text(encoding='utf-8')

aria_announcer_html = """  <!-- UX-16: Global Screen Reader Announcer for Dynamic Interactions -->
  <div id="srLiveAnnouncer" class="sr-only" role="status" aria-live="polite" aria-atomic="true"></div>
"""

sr_only_css = """
    /* UX-16: Accessible visually-hidden class for screen reader live feedback */
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
"""

if "id=\"srLiveAnnouncer\"" not in content_body:
    target = "<!-- Atelier workflow:"
    content_body = content_body.replace(target, aria_announcer_html + "\n  " + target)
    p_body.write_text(content_body, encoding='utf-8')
    print("Added srLiveAnnouncer to part3_body_sections.html")

# 2. Add sr-only CSS into templates/part2_css_rest.html
p_css = Path('/home/user/openbreak/templates/part2_css_rest.html')
content_css = p_css.read_text(encoding='utf-8')

if ".sr-only {" not in content_css:
    content_css += sr_only_css
    p_css.write_text(content_css, encoding='utf-8')
    print("Added sr-only class to part2_css_rest.html")

# 3. Add announcement helper in part4_js_logic.html
p_js = Path('/home/user/openbreak/templates/part4_js_logic.html')
content_js = p_js.read_text(encoding='utf-8')

announcer_js = """
    // UX-16: Accessible Screen Reader Live Announcer
    function announceToScreenReader(message) {
      const announcer = document.getElementById('srLiveAnnouncer');
      if (!announcer) return;
      announcer.textContent = '';
      setTimeout(() => { announcer.textContent = message; }, 50);
    }
"""

if "function announceToScreenReader" not in content_js:
    content_js += announcer_js
    p_js.write_text(content_js, encoding='utf-8')
    print("Added announceToScreenReader helper to part4_js_logic.html")

