import shutil
from pathlib import Path

PORT_BASE = Path(r"D:\RHOS-Matrix-V2-3.0.3.0-plato-xz-by.RHProjects\images\super_extracted")
WORKSPACE = Path(r"D:\Coding\PlatoCamera")

# Target copies: (source_rel_path, dest_rel_path)
CONFIG_TARGETS = [
    ("system_ext/etc/cameracustomize.json", "system/system_ext/etc/cameracustomize.json"),
    ("system_ext/etc/cameraopt.json", "system/system_ext/etc/cameraopt.json"),
    ("system_ext/etc/cameraopt_thirdParty.json", "system/system_ext/etc/cameraopt_thirdParty.json"),
    ("system_ext/etc/camerascene.json", "system/system_ext/etc/camerascene.json"),
    ("system_ext/etc/task_profiles_cameraopt.json", "system/system_ext/etc/task_profiles_cameraopt.json"),
    ("system_ext/etc/permissions/com.xiaomi.hardware.camera.companion.xml", "system/system_ext/etc/permissions/com.xiaomi.hardware.camera.companion.xml"),
    ("system_ext/etc/permissions/miui-cameraopt.xml", "system/system_ext/etc/permissions/miui-cameraopt.xml")
]

def main():
    print("=" * 60)
    print("  PlatoCamera - Copy Port Configs to Workspace")
    print("=" * 60)
    print()

    copied = 0
    for src_rel, dest_rel in CONFIG_TARGETS:
        src = PORT_BASE / src_rel
        dest = WORKSPACE / dest_rel
        
        if not src.exists():
            print(f"[!] Source not found: {src_rel}")
            continue
            
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"[*] Copying {src_rel} -> {dest_rel}...")
        try:
            shutil.copy2(src, dest)
            copied += 1
        except Exception as e:
            print(f"[!] Copy failed: {e}")
            
    print()
    print(f"[OK] Successfully copied {copied} configuration files to workspace.")

if __name__ == "__main__":
    main()
