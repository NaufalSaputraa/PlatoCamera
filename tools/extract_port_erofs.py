import subprocess
from pathlib import Path

def main():
    fsck_exe = Path(r"D:\Coding\PlatoCamera\tools\bin\fsck.erofs.exe")
    base_extracted = Path(r"D:\RHOS-Matrix-V2-3.0.3.0-plato-xz-by.RHProjects\images\super_extracted")
    
    product_img = base_extracted / "product_a.img"
    system_ext_img = base_extracted / "system_ext_a.img"
    
    # Extract product
    if product_img.exists():
        dest = base_extracted / "product"
        dest.mkdir(parents=True, exist_ok=True)
        print(f"[*] Extracting {product_img.name} -> {dest}...")
        cmd = [str(fsck_exe), f"--extract={dest}", str(product_img)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] Product extracted.")
        else:
            print(f"[!] Product extraction failed: {result.stderr or result.stdout}")
            
    # Extract system_ext
    if system_ext_img.exists():
        dest = base_extracted / "system_ext"
        dest.mkdir(parents=True, exist_ok=True)
        print(f"[*] Extracting {system_ext_img.name} -> {dest}...")
        cmd = [str(fsck_exe), f"--extract={dest}", str(system_ext_img)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] System_ext extracted.")
        else:
            print(f"[!] System_ext extraction failed: {result.stderr or result.stdout}")

if __name__ == "__main__":
    main()
