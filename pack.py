import os
import zipfile
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent
OUTPUT_ZIP = WORKSPACE / "PlatoCamera-v1.1.1.zip"

EXCLUDE_PATTERNS = [
    ".git",
    ".agents",
    "tools",
    "pack.py",
    "PlatoCamera-v1.0.zip",
    "PlatoCamera-v1.1.zip",
    "PlatoCamera-v1.1.1.zip",
    "__pycache__",
    ".gitignore",
    ".gitattributes"
]

def should_exclude(path: Path) -> bool:
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path.parts or any(p.startswith(pattern) for p in path.parts):
            return True
    return False

def main():
    print("=" * 60)
    print("  PlatoCamera - Packaging Magisk/KSU Module")
    print("=" * 60)
    print()

    # Remove existing zip if any
    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()

    print(f"[*] Creating zip: {OUTPUT_ZIP.name}...")
    zip_count = 0
    with zipfile.ZipFile(str(OUTPUT_ZIP), 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(str(WORKSPACE)):
            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(WORKSPACE)
                
                if should_exclude(rel_path):
                    continue
                
                print(f"  Adding: {rel_path}")
                # Zip paths must use forward slashes
                zf.write(str(file_path), str(rel_path).replace("\\", "/"))
                zip_count += 1

    print()
    print(f"[OK] Successfully packed {zip_count} files into {OUTPUT_ZIP.name}")
    print(f"     Size: {OUTPUT_ZIP.stat().st_size / (1024**2):.2f} MB")

if __name__ == "__main__":
    main()
