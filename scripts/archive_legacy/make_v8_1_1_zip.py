import os, zipfile
from pathlib import Path

repo_dir = Path(__file__).resolve().parents[1]
target_zip = repo_dir.parent / 'OpenBreak_Cinematic_V8_1_1_Proyecto_Completo.zip'

exclude_dirs = {'.git', '__pycache__', '.pytest_cache', 'archive_legacy', 'legacy_builders', '.tmp_test_extract'}

with zipfile.ZipFile(target_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(repo_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, repo_dir.parent)
            zipf.write(full_path, rel_path)

print(f"Generated canonical V8.1.1 deliverable: {target_zip} ({os.path.getsize(target_zip)} bytes)")
