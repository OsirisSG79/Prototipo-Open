import json

with open('/home/user/openbreak/assets/data_uris.json', 'r', encoding='utf-8') as f:
    images = json.load(f)

with open('/home/user/openbreak/assets/three.min.js', 'r', encoding='utf-8') as f:
    three_min_js = f.read()

print("Assets loaded safely via Python file I/O.")
