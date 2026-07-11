import os
from pathlib import Path

PORT_BASE = Path(r"D:\RHOS-Matrix-V2-3.0.3.0-plato-xz-by.RHProjects\images\super_extracted")
STOCK_BASE = Path(r"D:\plato_global_images_OS2.0.207.0.VLQMIXM_20250923.0000.00_15.0_global_62eb292827\plato_global_images_OS2.0.207.0.VLQMIXM_15.0\images\super_extracted")

def compare_files():
    print("=" * 60)
    print("  Comparing Custom Port vs Stock ROM camera files")
    print("=" * 60)
    print()

    # Compare plato.xml size and presence
    port_xml = PORT_BASE / "product" / "etc" / "device_features" / "plato.xml"
    stock_xml = STOCK_BASE / "product" / "etc" / "device_features" / "plato.xml"
    
    print("=== Device Features (plato.xml) ===")
    if port_xml.exists() and stock_xml.exists():
        print(f"  Stock size: {stock_xml.stat().st_size} bytes")
        print(f"  Port size:  {port_xml.stat().st_size} bytes")
        if port_xml.stat().st_size != stock_xml.stat().st_size:
            print("  [INFO] plato.xml DIFFERS! The port ROM has modified features.")
        else:
            print("  [OK] plato.xml is identical.")
    else:
        print(f"  Port XML exists: {port_xml.exists()}")
        print(f"  Stock XML exists: {stock_xml.exists()}")

    print()
    print("=== Camera APKs ===")
    port_apk = PORT_BASE / "product" / "priv-app" / "MiuiCamera" / "MiuiCamera.apk"
    stock_apk = STOCK_BASE / "product" / "priv-app" / "MiuiCamera" / "MiuiCamera.apk"
    
    if port_apk.exists():
        print(f"  Port MiuiCamera.apk size: {port_apk.stat().st_size / (1024*1024):.2f} MB")
    if stock_apk.exists():
        print(f"  Stock MiuiCamera.apk size: {stock_apk.stat().st_size / (1024*1024):.2f} MB")

    # Compare libraries
    print()
    print("=== Native Libraries (system_ext/lib64) ===")
    libs = [
        "libcamera_algoup_jni.xiaomi.so",
        "libcamera_mianode_jni.xiaomi.so",
        "libcamera_ispinterface_jni.xiaomi.so",
        "libmtkisp_metadata_sys.so",
        "vendor.mediatek.hardware.camera.isphal@1.0.so",
        "vendor.mediatek.hardware.camera.isphal-V1-ndk.so"
    ]
    
    for lib in libs:
        p_lib = PORT_BASE / "system_ext" / "lib64" / lib
        s_lib = STOCK_BASE / "system_ext" / "lib64" / lib
        
        p_exists = p_lib.exists()
        s_exists = s_lib.exists()
        
        p_size = p_lib.stat().st_size if p_exists else 0
        s_size = s_lib.stat().st_size if s_exists else 0
        
        status = "[MATCH]" if p_size == s_size else "[DIFF]"
        if not p_exists or not s_exists:
            status = "[MISSING]"
            
        print(f"  {lib:50s} Port: {p_size/1024:7.1f} KB | Stock: {s_size/1024:7.1f} KB | {status}")

if __name__ == "__main__":
    compare_files()
