from pathlib import Path

p = Path('/home/user/openbreak/build_site.py')
text = p.read_text(encoding='utf-8')

target = '<link rel="stylesheet" href="src/css/deck-interactive.css">'
replacement = '<link rel="stylesheet" href="src/css/deck-interactive.css">\\n  <link rel="stylesheet" href="src/css/faq-refinements.css">'

if target in text and 'src/css/faq-refinements.css' not in text:
    text = text.replace(target, replacement)
    p.write_text(text, encoding='utf-8')
    print("Added faq-refinements.css to build_site.py")
else:
    print("Already added or target missing")
