from pathlib import Path

# 1. Update test_responsive_viewports_audit.py
p1 = Path('/home/user/openbreak/tests/test_responsive_viewports_audit.py')
c1 = p1.read_text(encoding='utf-8')
c1 = c1.replace(
    "html = Path('/home/user/openbreak/landing_melius_style.html').read_text(encoding='utf-8')",
    "base_dir = Path(__file__).resolve().parents[1]\n    html = (base_dir / 'landing_melius_style.html').read_text(encoding='utf-8')"
)
p1.write_text(c1, encoding='utf-8')
print("Made test_responsive_viewports_audit.py portable.")

# 2. Update test_audit_matrix_completeness.py
p2 = Path('/home/user/openbreak/tests/test_audit_matrix_completeness.py')
c2 = p2.read_text(encoding='utf-8')
old_p2 = """    html = Path('/home/user/openbreak/landing_melius_style.html').read_text(encoding='utf-8')
    docs = Path('/home/user/openbreak/docs.html').read_text(encoding='utf-8')
    audit_json = json.loads(Path('/home/user/openbreak/audit_report_v8_1_0.json').read_text(encoding='utf-8'))"""

new_p2 = """    base_dir = Path(__file__).resolve().parents[1]
    html = (base_dir / 'landing_melius_style.html').read_text(encoding='utf-8')
    docs = (base_dir / 'docs.html').read_text(encoding='utf-8')
    audit_json = json.loads((base_dir / 'audit_report_v8_1_0.json').read_text(encoding='utf-8'))"""

c2 = c2.replace(old_p2, new_p2)
c2 = c2.replace("Path('/home/user/openbreak/assets/reformer_studio.glb')", "base_dir / 'assets' / 'reformer_studio.glb'")
c2 = c2.replace("Path('/home/user/openbreak/MELIUS_STORYBOARD_COMPARATIVE_UX20.md')", "base_dir / 'MELIUS_STORYBOARD_COMPARATIVE_UX20.md'")
# For ZIP, check local parent or workspace:
c2 = c2.replace(
    "zip_path = Path('/home/user/OpenBreak_Cinematic_V8_1_0_Proyecto_Completo.zip')",
    "zip_path = (base_dir.parent / 'OpenBreak_Cinematic_V8_1_1_Proyecto_Completo.zip') if (base_dir.parent / 'OpenBreak_Cinematic_V8_1_1_Proyecto_Completo.zip').exists() else (base_dir / 'OpenBreak_Cinematic_V8_1_1_Proyecto_Completo.zip')"
)

p2.write_text(c2, encoding='utf-8')
print("Made test_audit_matrix_completeness.py portable.")

