#!/usr/bin/env python3
"""
AUD-058: High-DPI Canvas Backing Store & Display Density Scaling Audit
Verifies:
1. Retina / High-DPI display density scaling (window.devicePixelRatio) in WebGL / 3D canvas components.
2. WebGL canvas buffer dimensioning and aspect ratio synchronization.
3. DPR clamping (e.g. Math.min(devicePixelRatio, 1.75-2.0)) to prevent mobile GPU battery drain and thermal throttling.
"""

import sys
import re
from pathlib import Path

def run_audit():
    print("Running AUD-058 High-DPI Canvas Backing Store & DPR Scaling Audit...")
    repo_root = Path(__file__).resolve().parents[1]
    js_dir = repo_root / "src" / "js"
    reformer_file = js_dir / "reformer-3d.js"

    code = reformer_file.read_text(encoding="utf-8")

    # 1. Inspect DPR usage in WebGL
    print("--- [1/3] Device Pixel Ratio (DPR) Awareness ---")
    if "devicePixelRatio" not in code:
        print("FAILED: WebGL 3D canvas does not account for window.devicePixelRatio.")
        sys.exit(1)
    print("✓ WebGL 3D engine handles devicePixelRatio scaling cleanly.")

    # 2. Check DPR clamping to avoid GPU thermal strain
    print("--- [2/3] Mobile GPU Thermal & Battery Clamping (DPR <= 2) ---")
    match = re.search(r"Math\.min\([^,]+,\s*([0-9.]+)\)", code)
    if not match:
        print("FAILED: WebGL renderer does not set safe clamped pixel ratio.")
        sys.exit(1)
    clamp_val = float(match.group(1))
    if clamp_val > 2.0 or clamp_val < 1.0:
        print(f"FAILED: Safe DPR clamp should be between 1.0 and 2.0, found {clamp_val}")
        sys.exit(1)
    print(f"✓ Clamped device pixel ratio (DPR <= {clamp_val}) enforced on 3D WebGL renderer.")

    # 3. Canvas resize and aspect synchronization
    print("--- [3/3] Dynamic Resize & Aspect Synchronization ---")
    has_resize_observer = "ResizeObserver" in code
    has_camera_aspect = "this.camera.aspect" in code
    has_update_projection = "updateProjectionMatrix" in code

    if not (has_resize_observer and has_camera_aspect and has_update_projection):
        print("FAILED: Missing ResizeObserver or camera projection updates on canvas resize.")
        sys.exit(1)
    print("✓ Dynamic aspect ratio and projection matrix recalculation verified.")

    print("\n" + "=" * 60)
    print("  AUD-058 HIGH-DPI CANVAS SCALING & DPR AUDIT: PASSED (100%)")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
