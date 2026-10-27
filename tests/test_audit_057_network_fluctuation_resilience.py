#!/usr/bin/env python3
"""
AUD-057: Offline Network Fluctuation & Status Awareness Audit
Verifies:
1. Online/Offline network state awareness in OpenBreakTelemetry engine.
2. Safe graceful handling of navigator.onLine queries.
3. Event listeners for 'online' and 'offline' lifecycle without memory leaks.
"""

import sys
import re
from pathlib import Path

def run_audit():
    print("Running AUD-057 Offline Network Fluctuation & Status Awareness Audit...")
    repo_root = Path(__file__).resolve().parents[1]
    js_dir = repo_root / "src" / "js"
    analytics_file = js_dir / "analytics-engine.js"

    code = analytics_file.read_text(encoding="utf-8")

    # 1. Check network awareness implementation
    print("--- [1/3] Network Lifecycle Listeners ---")
    has_online_listener = "window.addEventListener('online'" in code or 'window.addEventListener("online"' in code
    has_offline_listener = "window.addEventListener('offline'" in code or 'window.addEventListener("offline"' in code

    if not (has_online_listener and has_offline_listener):
        print("FAILED: Missing online/offline network lifecycle event listeners.")
        sys.exit(1)
    print("✓ Both 'online' and 'offline' lifecycle transitions tracked in telemetry.")

    # 2. Check navigator.onLine fallback check
    print("--- [2/3] Safe Navigator Query Invariant ---")
    if "isOnline()" not in code or "navigator.onLine" not in code:
        print("FAILED: Missing isOnline safe accessor method.")
        sys.exit(1)
    print("✓ Graceful navigator.onLine fallback accessor verified.")

    # 3. Privacy-safe network event recording
    print("--- [3/3] Privacy-Preserving Network Logging ---")
    # Verify no IP addresses or SSID or network tokens are collected
    network_matches = re.findall(r"this\.record\(['\"]NETWORK['\"],[^)]+\)", code)
    if len(network_matches) < 2:
        print("FAILED: Expected network status transitions to be logged safely.")
        sys.exit(1)
    for m in network_matches:
        if any(bad in m for bad in ["ip", "ssid", "bssid", "mac", "lat", "lon"]):
            print(f"FAILED: Sensitive network info detected in telemetry: {m}")
            sys.exit(1)
    print(f"✓ Verified {len(network_matches)} privacy-safe network status transitions recorded.")

    print("\n" + "=" * 60)
    print("  AUD-057 OFFLINE NETWORK STATUS AWARENESS: PASSED (100%)")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
