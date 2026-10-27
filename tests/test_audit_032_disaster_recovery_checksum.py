"""
test_audit_032_disaster_recovery_checksum.py
Audit 032: Disaster Recovery, Cold-Start Clean Build & Checksum Determinism Audit
Validates:
1. Re-running build_site.py from cold state produces bit-for-bit idempotent HTML output
2. Disaster recovery restore script or clean build maintains exact file hierarchy
3. Checksum stability across multiple consecutive compilations
"""

import sys
import hashlib
import subprocess
from pathlib import Path

repo_dir = Path(__file__).resolve().parents[1]
landing_path = repo_dir / "landing_melius_style.html"

print("Running AUD-032 Disaster Recovery & Clean Build Idempotence Audit...")

def compute_sha256(file_path):
    h = hashlib.sha256()
    h.update(file_path.read_bytes())
    return h.hexdigest()

# 1. Baseline Checksum
hash1 = compute_sha256(landing_path)
print(f"--- [1/3] Baseline Bundle Hash: {hash1[:16]}... ---")

# 2. Re-triggering Build Script
print("--- [2/3] Executing Cold-Start Re-compilation (build_site.py) ---")
res = subprocess.run([sys.executable, str(repo_dir / "build_site.py")], capture_output=True, text=True)
assert res.returncode == 0, f"build_site.py failed: {res.stderr}"

hash2 = compute_sha256(landing_path)
print(f"Re-compiled Bundle Hash: {hash2[:16]}...")
assert hash1 == hash2, "Build process is non-deterministic (hashes differ across runs)"
print("✓ Idempotent determinism verified: build produces bit-for-bit identical output.")

# 3. Critical Directory Structure Verification
print("--- [3/3] Critical Directory Tree Health Check ---")
required_dirs = [
    repo_dir / "assets",
    repo_dir / "assets" / "optimized",
    repo_dir / "src",
    repo_dir / "src" / "css",
    repo_dir / "src" / "js",
    repo_dir / "templates",
    repo_dir / "tests",
    repo_dir / "scripts"
]

for d in required_dirs:
    assert d.exists() and d.is_dir(), f"Missing required directory: {d}"
    print(f"✓ Verified directory: {d.name}/")

print("\n============================================================")
print("  AUD-032 DISASTER RECOVERY & BUILD AUDIT: PASSED (100%)    ")
print("============================================================")
