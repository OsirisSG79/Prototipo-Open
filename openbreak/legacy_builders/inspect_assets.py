import json

with open('/home/user/openbreak/assets/data_uris.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for k, v in data.items():
    print(f"Key: {k}, Prefix: {v[:40]}..., Length: {len(v)}")
