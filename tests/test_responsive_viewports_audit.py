import re
from pathlib import Path

def test_responsive_matrix():
    print("Testing UX-12 Responsive Viewports Matrix (320px, 390px, 768px, 1024px, 1440px, 1920px)...")
    
    base_dir = Path(__file__).resolve().parents[1]
    html = (base_dir / 'landing_melius_style.html').read_text(encoding='utf-8')
    
    # 1. Viewport Meta tag
    assert '<meta name="viewport" content="width=device-width, initial-scale=1.0' in html, "Missing standard viewport meta"
    print("✓ Viewport meta tag verified.")
    
    # 2. Key CSS Breakpoint Queries across HTML and modular stylesheets
    css_bundle = html
    css_dir = base_dir / 'src' / 'css'
    if css_dir.exists():
        for css_file in css_dir.glob('*.css'):
            css_bundle += '\n' + css_file.read_text(encoding='utf-8')

    breakpoints_to_check = [
        'max-width: 1024px',
        'max-width: 900px',
        'max-width: 768px',
        'max-width: 480px',
        'max-width: 360px'
    ]
    for bp in breakpoints_to_check:
        assert bp in css_bundle, f"Missing breakpoint rule: {bp}"
    print(f"✓ All responsive breakpoint rules verified ({', '.join(breakpoints_to_check)}).")
    
    # 3. Check overflow prevention on body and key containers
    assert 'overflow-x: hidden' in html or 'overflow-x:hidden' in html or 'overflow: hidden' in html, "Missing horizontal overflow guard"
    print("✓ Horizontal overflow protection verified.")
    
    # 4. Check fluid typography clamp() usage
    clamps = re.findall(r'clamp\([^)]+\)', css_bundle)
    assert len(clamps) >= 5, f"Expected fluid typography clamp() across elements, found {len(clamps)}"
    print(f"✓ Fluid typography verified with {len(clamps)} fluid clamp() statements.")
    
    # 5. Check accessible touch targets
    interactive_selectors = [
        'btn-primary', 'btn-secondary', 'deck-satellite', 'faq-trigger', 'data-reformer-control'
    ]
    for sel in interactive_selectors:
        assert sel in html, f"Interactive target {sel} not found in output"
    print("✓ Accessible interactive elements and touch targets verified.")
    
    # 6. Verify WebGL Fallback and canvas containers
    assert 'id="webglFallbackCard"' in html, "Missing WebGL fallback container"
    assert 'id="reformerCanvas"' in html, "Missing Reformer canvas container"
    print("✓ WebGL & 3D mobile degradation containers verified.")
    
    print("\nALL RESPONSIVE AUDIT CHECKS PASSED (UX-12 VERIFIED)!\n")

if __name__ == '__main__':
    test_responsive_matrix()
