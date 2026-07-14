import shutil
import os
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
SYSTEM_EXT = WORKSPACE / "system" / "system_ext"
SYSTEM = WORKSPACE / "system"

def move_dir_contents(src: Path, dest: Path):
    if not src.exists():
        return
    dest.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        dest_item = dest / item.name
        if item.is_dir():
            move_dir_contents(item, dest_item)
        else:
            print(f"Moving: {item.relative_to(WORKSPACE)} -> {dest_item.relative_to(WORKSPACE)}")
            if dest_item.exists():
                dest_item.unlink()
            shutil.move(str(item), str(dest_item))

def main():
    if not SYSTEM_EXT.exists():
        print("[!] system/system_ext directory does not exist. Already reorganized?")
        return

    print("Reorganizing files from system/system_ext to system...")
    
    # 1. Move priv-app/MiuiCamera
    move_dir_contents(SYSTEM_EXT / "priv-app", SYSTEM / "priv-app")
    
    # 2. Move lib64
    move_dir_contents(SYSTEM_EXT / "lib64", SYSTEM / "lib64")
    
    # 3. Move framework
    move_dir_contents(SYSTEM_EXT / "framework", SYSTEM / "framework")
    
    # 4. Move etc (cameracustomize, cameraopt, etc. and etc/permissions)
    move_dir_contents(SYSTEM_EXT / "etc", SYSTEM / "etc")
    
    # 5. Clean up empty system/system_ext directory
    print("Cleaning up system/system_ext...")
    shutil.rmtree(str(SYSTEM_EXT))
    print("[OK] Reorganization complete!")

if __name__ == "__main__":
    main()
