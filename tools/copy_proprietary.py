import os
import shutil
from pathlib import Path

# Paths
ROM_BASE = Path(r"D:\plato_global_images_OS2.0.207.0.VLQMIXM_20250923.0000.00_15.0_global_62eb292827\plato_global_images_OS2.0.207.0.VLQMIXM_15.0\images\super_extracted")
WORKSPACE = Path(r"D:\Coding\PlatoCamera")

# Target copies: (source_rel_path, dest_rel_path)
COPY_TARGETS = [
    # MiuiCamera APK
    ("product/priv-app/MiuiCamera/MiuiCamera.apk", "system/system_ext/priv-app/MiuiCamera/MiuiCamera.apk"),
    
    # Device features XML
    ("product/etc/device_features/plato.xml", "system/etc/device_features/plato.xml"),
    ("product/etc/device_features/plato.xml", "system/product/etc/device_features/plato.xml"),
    
    # Proprietary native libs
    ("system_ext/lib64/libcamera_algoup_jni.xiaomi.so", "system/system_ext/lib64/libcamera_algoup_jni.xiaomi.so"),
    ("system_ext/lib64/libcamera_mianode_jni.xiaomi.so", "system/system_ext/lib64/libcamera_mianode_jni.xiaomi.so"),
    ("system_ext/lib64/libcamera_ispinterface_jni.xiaomi.so", "system/system_ext/lib64/libcamera_ispinterface_jni.xiaomi.so"),
    ("system_ext/lib64/libmtkisp_metadata_sys.so", "system/system_ext/lib64/libmtkisp_metadata_sys.so"),
    ("system_ext/lib64/vendor.mediatek.hardware.camera.isphal@1.0.so", "system/system_ext/lib64/vendor.mediatek.hardware.camera.isphal@1.0.so"),
    ("system_ext/lib64/vendor.mediatek.hardware.camera.isphal-V1-ndk.so", "system/system_ext/lib64/vendor.mediatek.hardware.camera.isphal-V1-ndk.so")
]

def main():
    print("=" * 60)
    print("  PlatoCamera - Copy Proprietary Blobs to Workspace")
    print("=" * 60)
    print()

    if not ROM_BASE.exists():
        print(f"[!] ROM Base directory not found: {ROM_BASE}")
        return

    copied_count = 0
    for src_rel, dest_rel in COPY_TARGETS:
        src_path = ROM_BASE / src_rel
        dest_path = WORKSPACE / dest_rel
        
        if not src_path.exists():
            print(f"[!] Source file not found: {src_rel}")
            continue
            
        # Ensure destination dir exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"[*] Copying {src_rel} -> {dest_rel}...")
        try:
            shutil.copy2(src_path, dest_path)
            copied_count += 1
        except Exception as e:
            print(f"[!] Copy failed: {e}")
            
    print()
    print(f"[OK] Copied {copied_count} of {len(COPY_TARGETS)} target files to workspace.")

if __name__ == "__main__":
    main()
