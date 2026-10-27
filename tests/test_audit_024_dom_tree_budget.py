"""
test_audit_024_dom_tree_budget.py
DOM Tree Complexity, Depth & Performance Budget Audit
Verifies:
1. Total DOM node count within optimal Lighthouse thresholds (< 1,500 nodes)
2. Maximum DOM nesting depth (< 30 levels)
3. Elimination of naked phantom container elements (<div></div> without attrs)
"""

import sys
import re
from pathlib import Path

repo_dir = Path(__file__).resolve().parents[1]
html_path = repo_dir / "landing_melius_style.html"

print("Running AUD-024 DOM Tree Complexity & Depth Budget Audit...")

html_content = html_path.read_text(encoding="utf-8")

# 1. Total DOM Node Count
print("--- [1/3] Total DOM Node Count ---")
tag_matches = re.findall(r'<([a-zA-Z0-9\-]+)(?:\s+[^>]*)?>', html_content)
void_elements = {'meta', 'link', 'img', 'br', 'hr', 'input', 'source'}
rendered_nodes = [t.lower() for t in tag_matches if t.lower() not in void_elements]
total_nodes = len(tag_matches)

print(f"Total opening elements detected: {total_nodes} (Structural nodes: {len(rendered_nodes)})")
assert total_nodes < 1500, f"DOM node count exceeds Lighthouse threshold: {total_nodes} >= 1500"
print(f"✓ DOM element budget strictly respected ({total_nodes} < 1,500).")

# 2. Maximum Nesting Depth Estimation
print("--- [2/3] Maximum DOM Nesting Depth ---")
depth = 0
max_depth = 0
void_tags_regex = re.compile(r'<(?:meta|link|img|br|hr|input|source)[^>]*>', re.IGNORECASE)
clean_html = void_tags_regex.sub('', html_content)

tokens = re.findall(r'(</?[a-zA-Z0-9\-]+(?:\s+[^>]*)?>)', clean_html)
for token in tokens:
    if token.startswith('</'):
        depth = max(0, depth - 1)
    elif token.endswith('/>'):
        pass
    else:
        depth += 1
        if depth > max_depth:
            max_depth = depth

print(f"Maximum calculated nesting depth: {max_depth} levels")
assert max_depth < 30, f"DOM tree is excessively nested: {max_depth} >= 30"
print(f"✓ DOM nesting depth conforms to performance standards ({max_depth} < 30 levels).")

# 3. Phantom / Naked Container Audit
print("--- [3/3] Zero Naked Phantom Elements ---")
naked_divs = re.findall(r'<div>\s*</div>', html_content, re.IGNORECASE)
assert len(naked_divs) == 0, f"Naked empty container divs found: {len(naked_divs)}"
print("✓ Zero naked phantom container elements detected.")

print("\nALL AUD-024 DOM TREE COMPLEXITY & DEPTH CHECKS PASSED (100%)!")
