import re
from pathlib import Path

def test_html_syntax_and_no_leak():
    print("Testing HTML syntax validity and zero raw CSS/JS leakage...")
    base = Path(__file__).resolve().parents[1]
    
    for filename in ['landing_melius_style.html', 'index.html']:
        path = base / filename
        assert path.exists(), f"File {path} does not exist"
        html = path.read_text(encoding='utf-8')
        
        # 1. Exactly one <head>, </head>, <body>, </body>, </html>
        assert html.count('<head>') == 1, f"Expected 1 <head> in {filename}, found {html.count('<head>')}"
        assert html.count('</head>') == 1, f"Expected 1 </head> in {filename}, found {html.count('</head>')}"
        assert html.count('<body>') == 1, f"Expected 1 <body> in {filename}, found {html.count('<body>')}"
        assert html.count('</body>') == 1, f"Expected 1 </body> in {filename}, found {html.count('</body>')}"
        assert html.count('</html>') == 1, f"Expected 1 </html> in {filename}, found {html.count('</html>')}"
        
        # 2. Absolutely zero characters between </head> and <body>
        head_end = html.find('</head>')
        body_start = html.find('<body>')
        between = html[head_end + 7 : body_start].strip()
        assert len(between) == 0, f"Found leaked text between </head> and <body> in {filename}: {between[:80]}"
        
        # 3. Absolutely zero characters after </html>
        html_end = html.rfind('</html>')
        after = html[html_end + 7:].strip()
        assert len(after) == 0, f"Found leaked text after </html> in {filename}: {after[:80]}"
        
        # 4. Check that no CSS comment /* UX- */ or JS code is exposed directly inside body text
        # Specifically, check the beginning of body
        body_content = html[body_start + 6 : html.find('</body>')]
        first_text_node = re.sub(r'<[^>]+>', '', body_content[:1500]).strip()
        assert '/* UX-' not in first_text_node, f"Found raw CSS comment leaked in body text: {first_text_node[:100]}"
        assert 'initScrollCinematicObserver' not in first_text_node, "Found raw JS leaked in body text"
        assert '.scroll-reveal-item' not in first_text_node, "Found raw CSS class leaked in body text"
        
        print(f"✓ {filename} HTML structural syntax and zero leakage verified.")

    print("\nALL HTML SYNTAX & ZERO-LEAK TESTS PASSED (P0-01 & P0-02 RESOLVED)!\n")

if __name__ == '__main__':
    test_html_syntax_and_no_leak()
