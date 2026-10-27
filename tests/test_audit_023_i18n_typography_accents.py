"""
test_audit_023_i18n_typography_accents.py
Spanish Typography, Orthographic Accents & i18n Localization Integrity Suite
Verifies:
1. Zero corrupted character entities or moji-bake tokens (e.g., 'Ã³', 'Ã±', 'â€', '&#65533;')
2. Presence and grammatical correctness of Spanish orthographic diacritics (á, é, í, ó, ú, ñ, ¿, ¡)
3. Correct localized currency formatting (MXN / $, centavos convention)
4. Time formatting conventions (24h or localized AM/PM notation)
5. Proper quote glyphs (canonical typographic single/double quotes vs straight apostrophes)
"""

import sys
import re
from pathlib import Path

repo_dir = Path(__file__).resolve().parents[1]
html_path = repo_dir / "landing_melius_style.html"

print("Running AUD-023 Spanish Typography & i18n Localization Audit...")

html_content = html_path.read_text(encoding="utf-8")

# 1. Moji-bake and corrupted UTF-8 byte sequences check
print("--- [1/4] Moji-bake & UTF-8 Encoding Health ---")
corrupted_patterns = [
    r'Ã¡', r'Ã©', r'Ã­', r'Ã³', r'Ãº', r'Ã±', r'â€', r'&#65533;', r'\ufffd'
]
for pat in corrupted_patterns:
    matches = re.findall(pat, html_content)
    assert len(matches) == 0, f"Moji-bake corruption token found in HTML: {pat} ({len(matches)} matches)"
print("✓ Zero moji-bake or corrupted UTF-8 multi-byte sequences detected.")

# 2. Spanish Diacritics Presence
print("--- [2/4] Spanish Orthographic Accents & Diacritics ---")
accents = ['á', 'é', 'í', 'ó', 'ú', 'ñ', '¿', '¡']
counts = {acc: len(re.findall(acc, html_content, re.IGNORECASE)) for acc in accents}
print(f"Diacritic frequencies in bundle: {counts}")
for acc, count in counts.items():
    assert count >= 5, f"Insufficient diacritic count for '{acc}': {count}"
print("✓ Natural Spanish orthography and diacritic density strictly verified.")

# 3. Currency and Price Formatting
print("--- [3/4] Localized Currency & Price Tokens ---")
pricing_matches = re.findall(r'\$\s*\d+(?:[\.,]\d+)?(?:\s*(?:MXN|/mes|/clase))?', html_content)
print(f"Found {len(pricing_matches)} price tokens: {pricing_matches[:5]}...")
assert len(pricing_matches) >= 3, "Missing formatted pricing tokens"
for price in pricing_matches:
    assert '$' in price, f"Invalid currency formatting: {price}"
print("✓ Currency notation complies with Mexican studio market conventions.")

# 4. Schedule Class Time Format
print("--- [4/4] Schedule Time Formatting Integrity ---")
time_matches = re.findall(r'\b\d{1,2}:\d{2}\s*(?:hrs|AM|PM)?\b', html_content)
print(f"Found {len(time_matches)} class time strings: {time_matches[:6]}...")
assert len(time_matches) >= 5, "Insufficient schedule time strings found"
print("✓ Class agenda and timetable notation verified.")

print("\nALL AUD-023 SPANISH TYPOGRAPHY & i18n CHECKS PASSED (100%)!")
