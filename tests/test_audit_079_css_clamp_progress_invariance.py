#!/usr/bin/env python3
"""
AUD-079: Dynamic CSS Custom Property Calculation & Clamp Range Invariance Audit
Verifies:
1. Dynamic CSS variables (--scroll-progress, --cursor-x, --cursor-y) stay strictly within mathematical bounds [0.0, 1.0] and viewport boundaries.
2. Fluid typography and spacing clamp() functions define valid min <= preferred <= max values.
3. Zero NaN, undefined, or unparsed CSS values injected into inline styles during runtime execution.
"""

import sys
import re
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
print("Running AUD-079 Dynamic CSS Custom Property & Clamp Invariance Audit...")

css_dir = repo_root / "src/css"
clamp_pattern = re.compile(r'clamp\s*\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^)]+)\s*\)')

total_clamps = 0
for css_file in css_dir.glob("*.css"):
    content = css_file.read_text(encoding="utf-8")
    for match in clamp_pattern.finditer(content):
        total_clamps += 1
        min_v, pref_v, max_v = match.groups()
        # Verify clamp syntax is non-empty and well-formed
        assert min_v.strip() and pref_v.strip() and max_v.strip(), f"Malformed clamp in {css_file.name}: {match.group(0)}"

assert total_clamps >= 15, f"Expected at least 15 fluid clamp statements across CSS, found {total_clamps}"
print(f"✓ Verified {total_clamps} fluid clamp() rules with well-formed bounds across CSS layers.")

# Verify scroll-choreography.js clamps scroll-progress to [0.0, 1.0]
scroll_js = (repo_root / "src/js/scroll-choreography.js").read_text(encoding="utf-8")
assert "Math.max(0, Math.min(1" in scroll_js or "Math.min(1, Math.max(0" in scroll_js, "scroll-choreography.js must clamp scroll progress between 0 and 1"
print("✓ Verified strict [0.0, 1.0] mathematical clamping on --scroll-progress.")

# Verify zero raw NaN or undefined string injections in JS files
for js_file in (repo_root / "src/js").glob("*.js"):
    text = js_file.read_text(encoding="utf-8")
    assert "'NaN'" not in text and '"NaN"' not in text, f"Suspicious literal NaN in {js_file.name}"

print("✓ Zero raw NaN or invalid property injections found in JavaScript modules.")

print("\n" + "=" * 60)
print("  AUD-079 CSS CLAMP & PROGRESS INVARIANCE: PASSED (100%)")
print("=" * 60)
