import os
import sys
import urllib.request
import zipfile
import subprocess
import shutil
from pathlib import Path

EROFS_ZIP_URL = "https://github.com/sekaiacg/erofs-utils/releases/download/v1.8.10-251217/erofs-utils-v1.8.10-gee46dd74-251217-Cygwin_x86_64.zip"

def download_erofs_tools(tools_dir: Path):
    tools_dir.mkdir(parents=True, exist_ok=True)
    zip_path = tools_dir / "erofs_tools.zip"
    erofs_exe = tools_dir / "fsck.erofs.exe"
    
    if erofs_exe.exists():
        print(f"[OK] fsck.erofs.exe already exists at {erofs_exe}")
        return erofs_exe

    print("[*] Downloading erofs-utils for Windows (Cygwin)...")
    try:
        urllib.request.urlretrieve(EROFS_ZIP_URL, str(zip_path))
        print("[OK] Download finished.")
    except Exception as e:
        print(f"[!] Failed to download erofs-utils: {e}")
        sys.exit(1)

    print("[*] Extracting erofs-utils...")
    with zipfile.ZipFile(str(zip_path), 'r') as zf:
        zf.extractall(str(tools_dir))

    # Clean up zip
    zip_path.unlink(missing_ok=True)
    
    # Check if we have fsck.erofs.exe
    # Note: the zip might have subdirectories. Let's find it.
    for root, dirs, files in os.walk(str(tools_dir)):
        for f in files:
            if f.lower() == "fsck.erofs.exe" or f.lower() == "extract.erofs.exe":
                found = Path(root) / f
                target = tools_dir / f
                if found != target:
                    shutil.copy2(str(found), str(target))
                # Also copy any dlls in that root directory to tools_dir
                for other_f in files:
                    if other_f.lower().endswith(".dll"):
                        shutil.copy2(str(Path(root) / other_f), str(tools_dir / other_f))
                print(f"[OK] Tool ready: {target}")
                return target

    print("[!] Could not find fsck.erofs.exe or extract.erofs.exe in zip.")
    sys.exit(1)

def extract_erofs_image(fsck_exe: Path, img_path: Path, dest_dir: Path):
    print(f"[*] Extracting EROFS image {img_path.name} to {dest_dir}...")
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Command for fsck.erofs is: fsck.erofs --extract=dest_dir img_path
    # or sometimes: fsck.erofs -x dest_dir img_path
    # Let's try --extract first
    cmd = [
        str(fsck_exe),
        f"--extract={dest_dir}",
        str(img_path)
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[OK] Extracted {img_path.name} successfully.")
    else:
        print(f"[!] Failed to extract {img_path.name}: {result.stderr or result.stdout}")
        # Try with -x flag
        print("[*] Retrying with -x flag...")
        cmd_alt = [str(fsck_exe), "-x", str(dest_dir), str(img_path)]
        result_alt = subprocess.run(cmd_alt, capture_output=True, text=True)
        if result_alt.returncode == 0:
            print(f"[OK] Extracted {img_path.name} successfully.")
        else:
            print(f"[!] Alternate method failed: {result_alt.stderr or result_alt.stdout}")

def main():
    tools_dir = Path(r"D:\Coding\PlatoCamera\tools\bin")
    fsck_exe = download_erofs_tools(tools_dir)
    
    base_extracted = Path(r"D:\plato_global_images_OS2.0.207.0.VLQMIXM_20250923.0000.00_15.0_global_62eb292827\plato_global_images_OS2.0.207.0.VLQMIXM_15.0\images\super_extracted")
    
    product_img = base_extracted / "product_a.img"
    system_ext_img = base_extracted / "system_ext_a.img"
    
    if product_img.exists():
        extract_erofs_image(fsck_exe, product_img, base_extracted / "product")
    else:
        print("[!] product_a.img not found")
        
    if system_ext_img.exists():
        extract_erofs_image(fsck_exe, system_ext_img, base_extracted / "system_ext")
    else:
        print("[!] system_ext_a.img not found")

if __name__ == "__main__":
    main()
