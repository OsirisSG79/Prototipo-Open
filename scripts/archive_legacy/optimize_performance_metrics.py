import re
from pathlib import Path

# Verify and enforce caching, resource hints (preconnect, preload, dns-prefetch) in index.html & landing_melius_style.html
html_path = Path('/home/user/openbreak/templates/part1_head_css.html')
content = html_path.read_text(encoding='utf-8')

resource_hints = """  <!-- UX-15: Resource Hints & Early Asset Warmup for Optimal CWV (LCP/CLS) -->
  <link rel="preconnect" href="assets/" crossorigin>
  <link rel="preload" href="assets/optimized/studio_hero.webp" as="image" type="image/webp">
  <link rel="preload" href="assets/three.min.js" as="script">
"""

if "<link rel=\"preconnect\" href=\"assets/\"" not in content:
    target = "<head>\n  <meta charset=\"UTF-8\">"
    content = content.replace(target, target + "\n" + resource_hints)
    html_path.write_text(content, encoding='utf-8')
    print("Added CWV preconnect and preload resource hints to part1_head_css.html")

