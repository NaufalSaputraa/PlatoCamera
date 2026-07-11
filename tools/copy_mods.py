import shutil
from pathlib import Path

# Paths
mod_camera = Path(r"C:\Users\MP2DX\Downloads\MiuiCamera.apk")
mod_extra = Path(r"C:\Users\MP2DX\Downloads\MiuiExtraPhoto.apk")

dest_camera = Path(r"D:\Coding\PlatoCamera\system\system_ext\priv-app\MiuiCamera\MiuiCamera.apk")
dest_extra = Path(r"D:\Coding\PlatoCamera\system\product\priv-app\ExtraPhotoGlobal\ExtraPhotoGlobal.apk")

def main():
    # Copy camera apk (overwrite existing)
    print(f"Copying modded MiuiCamera.apk -> {dest_camera}")
    dest_camera.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mod_camera, dest_camera)

    # Copy extra photo apk
    print(f"Copying modded MiuiExtraPhoto.apk -> {dest_extra}")
    dest_extra.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mod_extra, dest_extra)

    print("[OK] Modded APKs copied successfully.")

if __name__ == "__main__":
    main()
