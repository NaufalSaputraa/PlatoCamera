import shutil
from pathlib import Path

PORT_BASE = Path(r"D:\RHOS-Matrix-V2-3.0.3.0-plato-xz-by.RHProjects\images\super_extracted")
WORKSPACE = Path(r"D:\Coding\PlatoCamera")

JARS = [
    "system_ext/framework/com.xiaomi.hardware.camera.companion-V1.jar",
    "system_ext/framework/miui-cameraopt.jar"
]

def main():
    print("=" * 60)
    print("  PlatoCamera - Copy Port Jars to Workspace")
    print("=" * 60)
    print()

    copied = 0
    for j in JARS:
        src = PORT_BASE / j
        dest = WORKSPACE / "system" / j
        
        if not src.exists():
            print(f"[!] Source not found: {j}")
            continue
            
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"[*] Copying {j} -> system/{j}...")
        try:
            shutil.copy2(src, dest)
            copied += 1
        except Exception as e:
            print(f"[!] Copy failed: {e}")
            
    print()
    print(f"[OK] Successfully copied {copied} jar files to workspace.")

if __name__ == "__main__":
    main()
