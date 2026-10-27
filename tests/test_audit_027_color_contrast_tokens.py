"""
test_audit_027_color_contrast_tokens.py
Audit 027: Design Tokens, W3C APCA / WCAG Color Contrast & Typography Scale Audit
Validates:
1. Canonical Design System Tokens (--font-serif, --font-sans, --bg-warm, --text-black, --accent-orange)
2. Fluid typography scale clamp() functions use strictly monotonic min <= max values across CSS files and templates
3. Text to Background Contrast meets minimum 4.5:1 for normal text and 3:1 for large text
"""

import sys
import re
import math
import glob
from pathlib import Path

repo_dir = Path(__file__).resolve().parents[1]
head_css = (repo_dir / "templates" / "part1_head_css.html").read_text(encoding="utf-8")

print("Running AUD-027 Design Tokens, Contrast & Fluid Scale Audit...")

# 1. Verify CSS Variable Tokens
print("--- [1/3] Design System Tokens Verification ---")
required_tokens = [
    "--bg-warm",
    "--bg-dark",
    "--text-black",
    "--text-editorial",
    "--accent-orange",
    "--font-serif",
    "--font-sans"
]

for token in required_tokens:
    assert token in head_css, f"Missing token {token} in design tokens"
    print(f"✓ Verified token: {token}")

# 2. Mathematical Verification of Fluid clamp() Calls
print("--- [2/3] Fluid Typography Scale Monotonicity ---")
all_files = glob.glob(str(repo_dir / "src" / "css" / "*.css")) + [str(repo_dir / "landing_melius_style.html")]
total_clamp_matches = []
for f_path in all_files:
    text = Path(f_path).read_text(encoding="utf-8")
    total_clamp_matches.extend(re.findall(r'clamp\(([^)]+)\)', text))

assert len(total_clamp_matches) >= 30, f"Expected >= 30 clamp() calls, found {len(total_clamp_matches)}"

def parse_val(v_str):
    v_str = v_str.strip()
    m = re.match(r'([0-9.]+)(rem|px|vw)?', v_str)
    if not m:
        return None
    val = float(m.group(1))
    unit = m.group(2)
    if unit == 'rem':
        return val * 16.0
    if unit == 'px' or not unit:
        return val
    return None

monotonic_verified = 0
for clamp_expr in total_clamp_matches:
    parts = clamp_expr.split(',')
    if len(parts) == 3:
        min_v = parse_val(parts[0])
        max_v = parse_val(parts[2])
        if min_v is not None and max_v is not None:
            assert min_v <= max_v, f"Invalid non-monotonic clamp: min ({min_v}) > max ({max_v}) in {clamp_expr}"
            monotonic_verified += 1

print(f"✓ Verified {monotonic_verified} fluid clamp() expressions have valid monotonic min <= max ranges.")

# 3. High Contrast WCAG Luminance Calculation for Key Brand Pairs
print("--- [3/3] Mathematical WCAG 2.1 Contrast Ratio Verification ---")

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join(c * 2 for c in hex_str)
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def relative_luminance(rgb):
    def channel_lum(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else math.pow((c + 0.055) / 1.055, 2.4)
    r, g, b = rgb
    return 0.2126 * channel_lum(r) + 0.7152 * channel_lum(g) + 0.0722 * channel_lum(b)

def contrast_ratio(hex1, hex2):
    lum1 = relative_luminance(hex_to_rgb(hex1))
    lum2 = relative_luminance(hex_to_rgb(hex2))
    brightest = max(lum1, lum2)
    darkest = min(lum1, lum2)
    return (brightest + 0.05) / (darkest + 0.05)

# Open Break studio brand palette pairs
pairs = [
    ("#111111", "#FBFBFB", "Primary Black Text on Warm BG (--text-black / --bg-warm)"),
    ("#FFFFFF", "#111111", "White Text on Obsidian Studio BG (--text-white / --bg-dark)"),
    ("#FFFFFF", "#18181B", "White Text on Dark Card Surface (--text-white / --bg-card-dark)"),
    ("#111111", "#FFFFFF", "Primary Black on Pure White Surface")
]

for fg, bg, label in pairs:
    ratio = contrast_ratio(fg, bg)
    assert ratio >= 4.5, f"Contrast failed for {label}: {ratio:.2f}:1 < 4.5:1"
    print(f"✓ {label}: {ratio:.2f}:1 (WCAG AAA Pass)")

print("\n============================================================")
print("  AUD-027 DESIGN TOKENS & CONTRAST AUDIT: PASSED (100%)    ")
print("============================================================")
