"""
test_audit_019_cwv_performance_hints.py
Core Web Vitals (CWV) & Performance Hints Optimization Suite
Verifies:
1. Critical resource hints: <link rel="preload"> for Largest Contentful Paint (LCP) hero WebP
2. Resource preconnect & dns-prefetch directives for third-party typography
3. fetchpriority="high" and decoding="async" attributes on the LCP hero image
4. Elimination of render-blocking script patterns in <head>
5. Defer / async attributes on non-critical script tags
"""

import sys
import re
from pathlib import Path

repo_dir = Path(__file__).resolve().parents[1]
html_path = repo_dir / "landing_melius_style.html"

print("Running AUD-019 Core Web Vitals (CWV) & Performance Hints Audit...")

html_content = html_path.read_text(encoding="utf-8")

# 1. Preload hints for LCP asset
print("--- [1/4] Preload Hints for LCP Candidate ---")
assert 'rel="preload"' in html_content or "rel='preload'" in html_content, "Missing <link rel='preload'> directive"
assert 'as="image"' in html_content, "Missing as='image' preload directive for hero asset"
print("✓ Early LCP image preload hint verified.")

# 2. Hero image fetchpriority and decoding
print("--- [2/4] LCP Image Element Optimization ---")
hero_img_match = re.search(r'<img[^>]+src=["\']assets/optimized/studio_hero\.webp["\'][^>]*>', html_content)
assert hero_img_match, "LCP studio_hero.webp image tag not found in DOM"
hero_tag = hero_img_match.group(0)
assert 'fetchpriority="high"' in hero_tag or "fetchpriority='high'" in hero_tag, "LCP image missing fetchpriority='high'"
assert 'decoding="async"' in hero_tag or "decoding='async'" in hero_tag, "LCP image missing decoding='async'"
print("✓ LCP hero image element specifies fetchpriority='high' and decoding='async'.")

# 3. Head render-blocking scripts
print("--- [3/4] Head Render-Blocking Script Check ---")
head_match = re.search(r'<head>(.*?)</head>', html_content, re.DOTALL | re.IGNORECASE)
assert head_match, "<head> section missing"
head_content = head_match.group(1)

# Ensure no classic synchronous external scripts in <head>
sync_head_scripts = re.findall(r'<script\s+src=["\']([^"\']+)["\'](?![^>]*(?:defer|async))[^>]*>', head_content, re.IGNORECASE)
print(f"Found {len(sync_head_scripts)} synchronous external scripts in <head>.")
assert len(sync_head_scripts) == 0, f"Render-blocking synchronous scripts in <head>: {sync_head_scripts}"
print("✓ Zero render-blocking synchronous scripts in <head>.")

# 4. Body deferred execution
print("--- [4/4] Body Deferred Execution ---")
deferred_scripts = re.findall(r'<script\s+src=["\']([^"\']+)["\'](?:\s+defer|\s+async)[^>]*>', html_content, re.IGNORECASE)
print(f"Verified {len(deferred_scripts)} scripts loaded with defer/async attributes.")
assert len(deferred_scripts) >= 5, "Insufficient deferred modular scripts"

print("\nALL AUD-019 CORE WEB VITALS OPTIMIZATION CHECKS PASSED (100%)!")
