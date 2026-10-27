from pathlib import Path

p = Path('/home/user/openbreak/build_site.py')
text = p.read_text(encoding='utf-8')

target = '<script src="src/js/schedule-sync.js" defer></script>'
replacement = '<script src="src/js/schedule-sync.js" defer></script>\\n<script src="src/js/analytics-engine.js" defer></script>'

if target in text and 'analytics-engine.js' not in text:
    text = text.replace(target, replacement)
    p.write_text(text, encoding='utf-8')
    print("Added analytics-engine.js to build_site.py")
else:
    print("Already added or target missing")
