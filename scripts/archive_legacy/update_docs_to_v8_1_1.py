from pathlib import Path

# 1. Update docs.html
docs_p = Path('/home/user/openbreak/docs.html')
docs_content = docs_p.read_text(encoding='utf-8')

docs_content = docs_content.replace('V8.1.0', 'V8.1.1')
docs_content = docs_content.replace('OpenBreak_Cinematic_V8_1_0_Proyecto_Completo.zip', 'OpenBreak_Cinematic_V8_1_1_Proyecto_Completo.zip')
docs_content = docs_content.replace('CHANGELOG_V8_0_1.md', 'CHANGELOG_V8_1_1.md')
docs_content = docs_content.replace('Ver Registro V8.0.1', 'Ver Registro V8.1.1')

docs_p.write_text(docs_content, encoding='utf-8')
print("Updated docs.html to V8.1.1!")

# 2. Update audit_report_v8_1_0.json -> audit_report_v8_1_1.json
audit_p = Path('/home/user/openbreak/audit_report_v8_1_0.json')
audit_content = audit_p.read_text(encoding='utf-8')
audit_content = audit_content.replace('V8.1.0', 'V8.1.1')
audit_content = audit_content.replace('OpenBreak_Cinematic_V8_1_0_Proyecto_Completo.zip', 'OpenBreak_Cinematic_V8_1_1_Proyecto_Completo.zip')
audit_content = audit_content.replace('CHANGELOG_V8_1_0.md', 'CHANGELOG_V8_1_1.md')

Path('/home/user/openbreak/audit_report_v8_1_1.json').write_text(audit_content, encoding='utf-8')
print("Created audit_report_v8_1_1.json!")

# 3. Clean up templates/part3_body_sections.html & part4_js_logic.html comments
p3 = Path('/home/user/openbreak/templates/part3_body_sections.html')
p3_text = p3.read_text(encoding='utf-8')
p3_text = p3_text.replace('V8.1.0', 'V8.1.1')
p3.write_text(p3_text, encoding='utf-8')

p4 = Path('/home/user/openbreak/templates/part4_js_logic.html')
p4_text = p4.read_text(encoding='utf-8')
p4_text = p4_text.replace('V8.1.0', 'V8.1.1')
p4.write_text(p4_text, encoding='utf-8')

print("Sanitized internal template comments to V8.1.1!")
