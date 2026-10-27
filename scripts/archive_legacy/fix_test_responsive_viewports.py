from pathlib import Path

p = Path('/home/user/openbreak/tests/test_responsive_viewports_audit.py')
content = p.read_text(encoding='utf-8')

# The test inspects landing_melius_style.html and also the linked external stylesheets in src/css/
old_body = """    # 2. Key CSS Breakpoint Queries
    breakpoints_to_check = [
        'max-width: 1024px',
        'max-width: 900px',
        'max-width: 768px',
        'max-width: 480px',
        'max-width: 360px'
    ]
    for bp in breakpoints_to_check:
        assert bp in html, f"Missing breakpoint rule: {bp}"
    print(f"✓ All responsive breakpoint rules verified ({', '.join(breakpoints_to_check)}).")"""

new_body = """    # 2. Key CSS Breakpoint Queries across HTML and modular stylesheets
    css_bundle = html
    css_dir = base_dir / 'src' / 'css'
    if css_dir.exists():
        for css_file in css_dir.glob('*.css'):
            css_bundle += '\\n' + css_file.read_text(encoding='utf-8')

    breakpoints_to_check = [
        'max-width: 1024px',
        'max-width: 900px',
        'max-width: 768px',
        'max-width: 480px',
        'max-width: 360px'
    ]
    for bp in breakpoints_to_check:
        assert bp in css_bundle, f"Missing breakpoint rule: {bp}"
    print(f"✓ All responsive breakpoint rules verified ({', '.join(breakpoints_to_check)}).")"""

assert old_body in content
content = content.replace(old_body, new_body)

# Also for clamps: check html + css_bundle
old_clamps = """    clamps = re.findall(r'clamp\([^)]+\)', html)"""
new_clamps = """    clamps = re.findall(r'clamp\([^)]+\)', css_bundle)"""
content = content.replace(old_clamps, new_clamps)

p.write_text(content, encoding='utf-8')
print("Updated test_responsive_viewports_audit.py to check modular CSS stylesheets as well.")
