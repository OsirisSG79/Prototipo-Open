from pathlib import Path

# In part3_body_sections.html, remove the srLiveAnnouncer at the very top (before <body>),
# and put it right after <body>.
p = Path('/home/user/openbreak/templates/part3_body_sections.html')
content = p.read_text(encoding='utf-8')

announcer = '<div id="srLiveAnnouncer" class="sr-only" role="status" aria-live="polite" aria-atomic="true"></div>\n'

if content.startswith(announcer):
    content = content[len(announcer):]

# Now insert it right after <body>
assert '<body>' in content
content = content.replace('<body>', '<body>\n  ' + announcer.strip())
p.write_text(content, encoding='utf-8')
print("Moved srLiveAnnouncer inside <body> in part3_body_sections.html")
