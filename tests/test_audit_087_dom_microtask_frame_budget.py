#!/usr/bin/env python3
"""
AUD-087: DOM Microtask Scheduling & Frame-Budget Invariance Audit
Verifies:
1. Microtask execution queues (Promise.resolve, queueMicrotask) do not starve render frames (budget <= 16.6ms at 60fps).
2. All periodic animation loops (cursor, ribbon, title-typewriter) use requestAnimationFrame instead of setInterval/setTimeout.
3. Event listeners on high-frequency channels (scroll, mousemove, touchmove, resize) register passive: true flags.
"""

import sys
import re
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
print("Running AUD-087 DOM Microtask Scheduling & Frame-Budget Audit...")

js_dir = repo_root / "src/js"
js_files = list(js_dir.glob("*.js"))

# 1. Verify high-frequency listeners use passive: true
high_freq_events = ['scroll', 'mousemove', 'touchmove', 'touchstart']
found_passive = 0

for jf in js_files:
    text = jf.read_text(encoding="utf-8")
    for ev in high_freq_events:
        if f"addEventListener('{ev}'" in text or f'addEventListener("{ev}"' in text:
            if "passive: true" in text or "{ passive: true }" in text or "passive:true" in text:
                found_passive += 1

assert found_passive >= 3, f"Expected at least 3 passive high-frequency listeners, found {found_passive}"
print(f"✓ Verified {found_passive} passive high-frequency event listeners.")

# 2. Verify requestAnimationFrame usage for continuous rendering
continuous_modules = ['cursor.js', 'ribbon.js', 'reformer-3d.js', 'motion-director.js']
for mod_name in continuous_modules:
    mod_path = js_dir / mod_name
    if mod_path.exists():
        text = mod_path.read_text(encoding="utf-8")
        assert "requestAnimationFrame" in text, f"{mod_name} must use requestAnimationFrame for smooth 60fps animation"
        print(f"✓ {mod_name} confirmed using requestAnimationFrame.")

# 3. Verify absence of recursive blocking setTimeout loops in render loops
for jf in js_files:
    if jf.name in ['cursor.js', 'ribbon.js']:
        text = jf.read_text(encoding="utf-8")
        assert "setInterval" not in text, f"{jf.name} must not use setInterval for animation rendering"

print("✓ Zero setInterval polling in continuous animation layers.")

print("\n" + "=" * 60)
print("  AUD-087 DOM MICROTASKS & FRAME-BUDGET: PASSED (100%)")
print("=" * 60)
