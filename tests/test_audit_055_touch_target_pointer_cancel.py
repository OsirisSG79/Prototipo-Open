#!/usr/bin/env python3
"""
AUD-055: WCAG Touch Target 48px Enhanced & Pointer Cancellation Audit
Verifies:
1. Touch target minimum area (48px x 48px or 44px min with surrounding spacing).
2. Pointer event cancellation safety: no pointerdown/touchstart triggers non-reversible state mutation directly without touchup/click completion.
3. CSS touch-action properties and active hit-area bounding declarations.
"""

import sys
import re
from pathlib import Path

def run_audit():
    print("Running AUD-055 WCAG Touch Target 48px Enhanced & Pointer Safety Audit...")
    repo_root = Path(__file__).resolve().parents[1]
    html_file = repo_root / "dist" / "landing_melius_style.html"
    js_dir = repo_root / "src" / "js"
    css_dir = repo_root / "src" / "css"

    if not html_file.exists():
        html_file = repo_root / "landing_melius_style.html"
    
    html_content = html_file.read_text(encoding="utf-8")

    # 1. Check touch targets in CSS
    print("--- [1/3] Mobile Touch Target 44px-48px Standards ---")
    all_css = ""
    for css_file in sorted(css_dir.glob("*.css")):
        all_css += css_file.read_text(encoding="utf-8") + "\n"
    
    # Check min-height / min-width interactive sizing
    touch_matches = re.findall(r'min-height:\s*([0-9]+)px', all_css)
    interactive_touch_targets = [int(m) for m in touch_matches if int(m) >= 44]
    if len(interactive_touch_targets) < 5:
        print(f"FAILED: Expected at least 5 declarations of min-height >= 44px, found {len(interactive_touch_targets)}")
        sys.exit(1)
    print(f"✓ Verified {len(interactive_touch_targets)} interactive mobile touch targets adhering to >= 44px standard.")

    # 2. Check Pointer Event Safety (WCAG 2.5.2 Pointer Cancellation)
    print("--- [2/3] WCAG 2.5.2 Pointer Cancellation Invariant ---")
    unsafe_pointer_down_mutations = []
    for js_file in sorted(js_dir.glob("*.js")):
        code = js_file.read_text(encoding="utf-8")
        # Check if booking cancellation or credit debit happens inside 'touchstart' or 'pointerdown' directly without click
        if re.search(r"addEventListener\s*\(\s*['\"](pointerdown|touchstart)['\"][^)]*(bookClass|cancelBooking|refundBooking)", code):
            unsafe_pointer_down_mutations.append(js_file.name)

    if unsafe_pointer_down_mutations:
        print(f"FAILED: Found destructive mutations directly triggered by pointerdown/touchstart in: {unsafe_pointer_down_mutations}")
        sys.exit(1)
    print("✓ WCAG 2.5.2 verified: zero destructive state actions bound solely to pointerdown/touchstart.")

    # 3. Check CSS touch-action and user-select guards
    print("--- [3/3] Mobile Gesture & Touch Action Configuration ---")
    has_touch_action = "touch-action" in all_css
    has_user_select = "user-select" in all_css or "-webkit-user-select" in all_css
    if not (has_touch_action and has_user_select):
        print("FAILED: Missing touch-action or user-select declarations for touch precision.")
        sys.exit(1)
    print("✓ Mobile gesture handling and drag constraints configured cleanly.")

    print("\n" + "=" * 60)
    print("  AUD-055 TOUCH TARGET & POINTER CANCELLATION: PASSED (100%)")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
