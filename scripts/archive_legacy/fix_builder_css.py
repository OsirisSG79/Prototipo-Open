from pathlib import Path

p = Path('/home/user/openbreak/build_site.py')
lines = p.read_text(encoding='utf-8').splitlines()

fixed_lines = []
for line in lines:
    if line.startswith("cssrest=cssrest.replace('</head>'"):
        fixed_lines.append("cssrest=cssrest.replace('</head>','  <link rel=\"stylesheet\" href=\"src/css/editorial.css\">\\n  <link rel=\"stylesheet\" href=\"src/css/cinematic-hero.css\">\\n  <link rel=\"stylesheet\" href=\"src/css/kinetic-type.css\">\\n  <link rel=\"stylesheet\" href=\"src/css/motion.css\">\\n  <link rel=\"stylesheet\" href=\"src/css/workflow-3d.css\">\\n  <link rel=\"stylesheet\" href=\"src/css/schedule-grid.css\">\\n</head>')")
    elif 'src/css/schedule-grid.css' in line and line.strip().startswith('<link'):
        continue
    else:
        fixed_lines.append(line)

p.write_text('\n'.join(fixed_lines), encoding='utf-8')
print("Successfully fixed build_site.py string literal")
