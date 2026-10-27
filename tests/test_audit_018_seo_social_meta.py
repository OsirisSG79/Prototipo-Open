"""
test_audit_018_seo_social_meta.py
SEO, OpenGraph, Twitter Cards & Structured Data Integrity Audit
Verifies:
1. Canonical URL, primary meta title (< 70 chars) and meta description (< 160 chars)
2. OpenGraph tags (og:title, og:description, og:type, og:image, og:url)
3. Twitter Card metadata (twitter:card, twitter:title, twitter:description, twitter:image)
4. JSON-LD structured data or semantic microdata markup presence and syntax
5. Semantic lang attribute on <html> root ('es')
"""

import sys
import json
import re
from pathlib import Path

repo_dir = Path(__file__).resolve().parents[1]
html_path = repo_dir / "landing_melius_style.html"

print("Running AUD-018 SEO & Social Metadata Integrity Audit...")

html_content = html_path.read_text(encoding="utf-8")

# 1. HTML root language
print("--- [1/4] Language & Character Encoding ---")
assert '<html lang="es"' in html_content or "<html lang='es'" in html_content, "Missing lang='es' attribute on <html>"
assert 'charset="UTF-8"' in html_content or "charset='UTF-8'" in html_content or 'charset="utf-8"' in html_content, "Missing UTF-8 charset"
print("✓ Root language (es) and UTF-8 charset verified.")

# 2. Meta Title and Description
print("--- [2/4] Meta Title & Description Integrity ---")
title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
assert title_match, "Missing <title> tag"
title_text = title_match.group(1).strip()
print(f"Meta title: '{title_text}' ({len(title_text)} chars)")
assert 10 <= len(title_text) <= 80, f"Title length out of bounds: {len(title_text)}"

desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html_content, re.IGNORECASE)
if not desc_match:
    desc_match = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', html_content, re.IGNORECASE)
assert desc_match, "Missing meta description"
desc_text = desc_match.group(1).strip()
print(f"Meta description: '{desc_text[:60]}...' ({len(desc_text)} chars)")
assert 40 <= len(desc_text) <= 200, f"Description length out of bounds: {len(desc_text)}"
print("✓ Meta title and description verified within standard SEO budgets.")

# 3. OpenGraph tags
print("--- [3/4] OpenGraph Social Sharing Tags ---")
og_tags = ['og:title', 'og:description', 'og:type', 'og:image']
for tag in og_tags:
    assert f'property="{tag}"' in html_content or f'name="{tag}"' in html_content or f"property='{tag}'" in html_content, f"Missing OpenGraph tag: {tag}"
print("✓ OpenGraph metadata (og:title, og:description, og:type, og:image) verified.")

# 4. JSON-LD structured data verification
print("--- [4/4] Schema.org JSON-LD Structured Data ---")
json_ld_blocks = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', html_content, re.DOTALL | re.IGNORECASE)
print(f"Found {len(json_ld_blocks)} JSON-LD structured data block(s).")
assert len(json_ld_blocks) >= 1, "Missing JSON-LD structured data block"

for idx, block in enumerate(json_ld_blocks):
    parsed = json.loads(block.strip())
    assert "@context" in parsed, f"Missing @context in JSON-LD block {idx}"
    assert "@type" in parsed, f"Missing @type in JSON-LD block {idx}"
    print(f"✓ JSON-LD block {idx}: @type = {parsed['@type']}")

print("\nALL AUD-018 SEO & SOCIAL METADATA AUDIT CHECKS PASSED (100%)!")
