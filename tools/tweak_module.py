import re
from pathlib import Path

WORKSPACE = Path(r"D:\Coding\PlatoCamera")

LEICA_TAGS = """
    <!-- Leica Camera Features Mod -->
    <bool name="support_leica_style">true</bool>
    <bool name="is_support_leica_camera">true</bool>
    <bool name="support_camera_leica">true</bool>
    <bool name="support_camera_leica_watermark">true</bool>
"""

def inject_leica():
    xml_paths = [
        WORKSPACE / "system" / "etc" / "device_features" / "plato.xml",
        WORKSPACE / "system" / "product" / "etc" / "device_features" / "plato.xml"
    ]
    
    for path in xml_paths:
        if not path.exists():
            print(f"[!] Path not found: {path}")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if already injected
        if "support_leica_style" in content:
            print(f"[SKIP] Leica tags already present in {path.name}")
            continue
            
        # Insert before the closing </features> tag
        new_content = content.replace("</features>", f"{LEICA_TAGS}</features>")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[OK] Injected Leica features into {path.relative_to(WORKSPACE)}")

def tweak_system_prop():
    prop_path = WORKSPACE / "system.prop"
    if not prop_path.exists():
        print("[!] system.prop not found")
        return
        
    with open(prop_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    extra_props = """
# Camera2 API / HAL3 Enabled
persist.vendor.camera.HAL3.enabled=1

# Enable Video EIS stabilization
persist.vendor.camera.eis.enable=1

# MediaTek Advanced Features (Beauty, AI, Portrait)
persist.vendor.camera.enableAdvanceFeatures=0x347
"""

    if "persist.vendor.camera.HAL3.enabled" in content:
        print("[SKIP] system.prop tweaks already applied.")
        return
        
    with open(prop_path, 'a', encoding='utf-8') as f:
        f.write(extra_props)
    print("[OK] Applied MediaTek camera tweaks to system.prop")

def main():
    print("=" * 60)
    print("  Applying Leica and MTK Camera Tweaks")
    print("=" * 60)
    print()
    inject_leica()
    tweak_system_prop()

if __name__ == "__main__":
    main()
