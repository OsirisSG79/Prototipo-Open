from pathlib import Path

p_build = Path('/home/user/openbreak/build_site.py')
content = p_build.read_text(encoding='utf-8')

old_controller = """controller=f'''<script src="assets/three.min.js"></script>
<script>
{modules}"""

new_controller = """controller=f'''<script src="assets/three.min.js"></script>
<script src="assets/GLTFLoader.js"></script>
<script>
{modules}"""

assert old_controller in content, "old_controller not found in build_site.py"
content = content.replace(old_controller, new_controller)
p_build.write_text(content, encoding='utf-8')
print("Successfully wired GLTFLoader.js into build_site.py")
