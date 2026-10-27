from pathlib import Path

# Add srLiveAnnouncer right after <body> in templates/part3_body_sections.html
p = Path('/home/user/openbreak/templates/part3_body_sections.html')
content = p.read_text(encoding='utf-8')

announcer = '<div id="srLiveAnnouncer" class="sr-only" role="status" aria-live="polite" aria-atomic="true"></div>\n'

if 'id="srLiveAnnouncer"' not in content:
    content = announcer + content
    p.write_text(content, encoding='utf-8')
    print("Prepend srLiveAnnouncer to part3_body_sections.html")
