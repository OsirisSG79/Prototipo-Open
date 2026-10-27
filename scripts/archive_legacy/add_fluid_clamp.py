from pathlib import Path

p_css = Path('/home/user/openbreak/templates/part2_css_rest.html')
content = p_css.read_text(encoding='utf-8')

# Let's add fluid typography clamp for section-subtext or pricing-price
target = ".section-subtext {"
replacement = """.section-subtext {
      font-size: clamp(0.92rem, 1.2vw, 1.08rem);"""

if target in content and "clamp(0.92rem" not in content:
    content = content.replace(target, replacement)
    p_css.write_text(content, encoding='utf-8')
    print("Added 5th clamp for section-subtext in part2_css_rest.html")

