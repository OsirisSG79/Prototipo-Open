import os
import zipfile
import stat
from pathlib import Path

repo_dir = Path(__file__).resolve().parents[1]
# Support custom target or V8.1.3 default
target_name = os.environ.get('TARGET_ZIP_NAME', 'OpenBreak_Cinematic_V8_1_3_Proyecto_Completo.zip')
target_zip = repo_dir.parent / target_name

exclude_dirs = {'.git', '__pycache__', '.pytest_cache', 'archive_legacy', 'legacy_builders', '.tmp_test_extract'}

print(f"Packaging {repo_dir} into {target_zip} with preserved UNIX execution attributes...")

with zipfile.ZipFile(target_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(repo_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            full_path = Path(root) / file
            rel_path = full_path.relative_to(repo_dir.parent)
            
            # Read file data
            data = full_path.read_bytes()
            
            # Create ZipInfo with preserved POSIX permissions
            zinfo = zipfile.ZipInfo(str(rel_path))
            zinfo.date_time = (2026, 10, 26, 12, 0, 0)
            
            # Determine permission: check if executable on filesystem or script extension
            st_mode = full_path.stat().st_mode
            is_executable = (st_mode & 0o111) or full_path.suffix in ['.sh']
            
            if is_executable:
                zinfo.external_attr = (stat.S_IFREG | 0o755) << 16
            else:
                zinfo.external_attr = (stat.S_IFREG | 0o644) << 16
                
            zipf.writestr(zinfo, data)

print(f"Generated canonical deliverable: {target_zip} ({os.path.getsize(target_zip):,} bytes)")
