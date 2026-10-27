from pathlib import Path

p = Path('/home/user/openbreak/build_site.py')
content = p.read_text(encoding='utf-8')

# 1. Include melius-scroll-responsive.css
old_css_link = r'''  <link rel="stylesheet" href="src/css/nav-refinements.css">\n</head>')'''
new_css_link = r'''  <link rel="stylesheet" href="src/css/nav-refinements.css">\n  <link rel="stylesheet" href="src/css/melius-scroll-responsive.css">\n</head>')'''

assert "src/css/nav-refinements.css" in content

content = content.replace(
    r"""<link rel="stylesheet" href="src/css/nav-refinements.css">\n</head>')""",
    r"""<link rel="stylesheet" href="src/css/nav-refinements.css">\n  <link rel="stylesheet" href="src/css/melius-scroll-responsive.css">\n</head>')"""
)

# 2. Include scroll-choreography.js
content = content.replace(
    '<script src="src/js/analytics-engine.js" defer></script>',
    '<script src="src/js/analytics-engine.js" defer></script>\n<script src="src/js/scroll-choreography.js" defer></script>'
)

# 3. Document closure
content = content.replace(
    'out=head+cssrest+body+controller+more_scripts+legacy',
    'out=head+cssrest+body+controller+more_scripts+legacy+"\n</body>\n</html>\n"'
)

p.write_text(content, encoding='utf-8')
print("Successfully updated build_site.py!")
