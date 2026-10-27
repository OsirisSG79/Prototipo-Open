from pathlib import Path

p = Path('/home/user/openbreak/templates/part3_body_sections.html')
content = p.read_text(encoding='utf-8')
if "<!-- Feedback de confirmación con canal directo y seguro (V7-10) -->" in content:
    content = content.replace("<!-- Feedback de confirmación con canal directo y seguro (V7-10) -->", "<!-- Feedback de confirmación con canal directo y seguro (UX-19 / V8.1.0) -->")
    p.write_text(content, encoding='utf-8')
    print("Sanitized legacy V7 comment in part3_body_sections.html")
