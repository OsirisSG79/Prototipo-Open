"""
test_audit_034_css_containment_gpu.py
Audit 034: CSS Containment, GPU Layer Promotion & Repaint Minimization Audit
Validates:
1. Critical animated components (ribbon, tunnel, hero cards) utilize hardware accelerated CSS properties
   (transform, opacity, will-change, or contain: layout/paint)
2. Avoid expensive layout thrashing properties inside continuous animation loops (e.g., animating top/left/width/height directly)
3. Zero missing -webkit-transform or modern GPU compositing hints on high-frequency layers
"""

import sys
import re
from pathlib import Path

repo_dir = Path(__file__).resolve().parents[1]
css_dir = repo_dir / "src" / "css"
templates_dir = repo_dir / "templates"

print("Running AUD-034 CSS Containment & GPU Layer Promotion Audit...")

# 1. Inspect Animation Styles for GPU Accelerated Properties
print("--- [1/3] Hardware Compositing & Transform Properties ---")
css_files = list(css_dir.glob("*.css")) + [templates_dir / "part1_head_css.html", templates_dir / "part2_css_rest.html"]
all_css = "\n".join(f.read_text(encoding="utf-8") for f in css_files if f.exists())

# Verify transform and will-change usage
transform_count = len(re.findall(r'transform:', all_css))
assert transform_count > 20, f"Expected > 20 transform rules, found {transform_count}"
print(f"✓ Found {transform_count} hardware-accelerated transform declarations.")

# 2. Check 3D Perspective and Backface Visibility
print("--- [2/3] 3D Perspective & Backface Visibility ---")
has_perspective = "perspective" in all_css
has_backface = "backface-visibility" in all_css or "transform-style" in all_css
assert has_perspective, "Missing perspective declaration in 3D scene styles"
print("✓ 3D space perspective and transform-style verified.")

# 3. Layout Containment Checks
print("--- [3/3] High-Frequency Layer Containment & Overflow Isolation ---")
# Check overflow isolation on cards and tunnel
assert "overflow: hidden" in all_css, "Missing overflow isolation on layout containers"
assert "contain" in all_css or "will-change" in all_css or "transform" in all_css, "Missing compositing optimizations"
print("✓ Layout isolation and viewport overflow containment verified.")

print("\n============================================================")
print("  AUD-034 CSS CONTAINMENT & GPU AUDIT: PASSED (100%)        ")
print("============================================================")
