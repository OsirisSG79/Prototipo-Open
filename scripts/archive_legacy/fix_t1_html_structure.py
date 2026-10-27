from pathlib import Path

# 1. Clean templates/part2_css_rest.html
p2 = Path('/home/user/openbreak/templates/part2_css_rest.html')
p2_content = p2.read_text(encoding='utf-8')

# Split at </style>\n</head>
split_marker = "  </style>\n</head>"
assert split_marker in p2_content, "Marker not found in part2"

parts = p2_content.split(split_marker)
base_css = parts[0]
orphan_css = parts[1]

# Save orphan_css to src/css/melius-scroll-responsive.css
css_dest = Path('/home/user/openbreak/src/css/melius-scroll-responsive.css')
css_dest.write_text(orphan_css.strip() + "\n", encoding='utf-8')
print(f"Saved {len(orphan_css)} chars of orphan CSS to {css_dest}")

# Restore part2_css_rest.html so it ends cleanly at </style>\n</head>
p2.write_text(base_css + split_marker + "\n", encoding='utf-8')
print("Cleaned templates/part2_css_rest.html")

# 2. Clean templates/part4_js_logic.html
p4 = Path('/home/user/openbreak/templates/part4_js_logic.html')
p4_content = p4.read_text(encoding='utf-8')

js_split_marker = "  </script>\n</body>\n</html>"
assert js_split_marker in p4_content, "Marker not found in part4"

js_parts = p4_content.split(js_split_marker)
base_js = js_parts[0]
orphan_js = js_parts[1]

# Save orphan_js to src/js/scroll-choreography.js
js_dest = Path('/home/user/openbreak/src/js/scroll-choreography.js')
js_dest.write_text(orphan_js.strip() + "\n", encoding='utf-8')
print(f"Saved {len(orphan_js)} chars of orphan JS to {js_dest}")

# Clean templates/part4_js_logic.html so it ends with only </script>
# Notice that build_site.py wraps everything in body/html or templates provide it.
# Let's inspect what build_site.py does.
p4.write_text(base_js + "\n  </script>\n", encoding='utf-8')
print("Cleaned templates/part4_js_logic.html")
