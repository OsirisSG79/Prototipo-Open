import os, zipfile

repo_dir = '/home/user/openbreak'
target_zip = '/home/user/OpenBreak_Cinematic_V8_1_0_Proyecto_Completo.zip'

with zipfile.ZipFile(target_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(repo_dir):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.pytest_cache', 'archive_legacy', 'legacy_builders']]
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, '/home/user')
            zipf.write(full_path, rel_path)

print(f"Generated canonical V8.1.0 deliverable: {target_zip} ({os.path.getsize(target_zip)} bytes)")
