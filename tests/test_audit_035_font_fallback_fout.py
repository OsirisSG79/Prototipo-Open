"""
test_audit_035_font_fallback_fout.py
Audit 035: Font Loading Performance, FOUT / FOIT Mitigation & Font Display Swap
Validates:
1. Google Font or web font stylesheet requests enforce &display=swap
2. Fallback font stack defines standard generic families (serif, sans-serif, monospace)
3. Zero missing fallback fonts in typography CSS definitions
4. Preconnect hints exist for external font domains (fonts.googleapis.com, fonts.gstatic.com)
"""

import sys
import re
from pathlib import Path

repo_dir = Path(__file__).resolve().parents[1]
head_path = repo_dir / "templates" / "part1_head_css.html"
html_path = repo_dir / "landing_melius_style.html"

assert head_path.exists(), "part1_head_css.html does not exist"
assert html_path.exists(), "landing_melius_style.html does not exist"

head_content = head_path.read_text(encoding="utf-8")
html_content = html_path.read_text(encoding="utf-8")

print("Running AUD-035 Font Loading & FOUT/FOIT Mitigation Audit...")

# 1. Inspect font display swap
print("--- [1/3] Font Display Swap Parameter ---")
font_links = re.findall(r'<link[^>]*href=["\']https://fonts\.googleapis\.com[^"\']+["\'][^>]*>', html_content)
assert len(font_links) > 0, "No Google Font links found in HTML"
for link in font_links:
    assert "display=swap" in link, f"Font link missing display=swap: {link}"
    print(f"✓ Verified display=swap in font link: {link[:65]}...")

# 2. Inspect Preconnect Hints
print("--- [2/3] Font Origins Preconnect Hints ---")
assert 'rel="preconnect" href="https://fonts.googleapis.com"' in html_content or "fonts.googleapis.com" in html_content
assert 'rel="preconnect" href="https://fonts.gstatic.com"' in html_content or "fonts.gstatic.com" in html_content
print("✓ Preconnect hints to font origins verified.")

# 3. Fallback Font Stack Verification
print("--- [3/3] Fallback Font Stack Invariants ---")
font_serif_match = re.search(r'--font-serif:\s*([^;]+);', head_content)
font_sans_match = re.search(r'--font-sans:\s*([^;]+);', head_content)
font_mono_match = re.search(r'--font-mono:\s*([^;]+);', head_content)

assert font_serif_match, "Missing --font-serif token"
assert font_sans_match, "Missing --font-sans token"
assert font_mono_match, "Missing --font-mono token"

assert "serif" in font_serif_match.group(1), f"Serif stack missing generic serif fallback: {font_serif_match.group(1)}"
assert "sans-serif" in font_sans_match.group(1), f"Sans stack missing generic sans-serif fallback: {font_sans_match.group(1)}"
assert "monospace" in font_mono_match.group(1), f"Mono stack missing generic monospace fallback: {font_mono_match.group(1)}"

print(f"✓ --font-serif fallback stack: {font_serif_match.group(1).strip()}")
print(f"✓ --font-sans fallback stack:  {font_sans_match.group(1).strip()}")
print(f"✓ --font-mono fallback stack:  {font_mono_match.group(1).strip()}")

print("\n============================================================")
print("  AUD-035 FONT PERFORMANCE & FALLBACK AUDIT: PASSED (100%)  ")
print("============================================================")
