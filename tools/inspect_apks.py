import zipfile
import re
import sys
from pathlib import Path

# A simple helper to read the binary AndroidManifest.xml from an APK
# to extract the package name and app name
def get_apk_package(apk_path):
    try:
        with zipfile.ZipFile(apk_path, 'r') as z:
            data = z.read('AndroidManifest.xml')
            
            # Binary XML header checks
            if data[:4] != b'\x03\x00\x08\x00':
                return "Not a valid binary AndroidManifest.xml"
                
            # String pool chunk start (usually at offset 8)
            # Find the string pool chunk header
            # Chunk type for String Pool is 0x00010001 (or 0x001C0001)
            # Let's search for the package name directly using raw regex in the data
            # Since package name will be present in UTF-16 inside the string pool
            # Let's search for common package names encoded in UTF-16-LE
            targets = {
                b'c\x00o\x00m\x00.\x00a\x00n\x00d\x00r\x00o\x00i\x00d\x00.\x00c\x00a\x00m\x00e\x00r\x00a\x00': "com.android.camera",
                b'c\x00o\x00m\x00.\x00m\x00i\x00u\x00i\x00.\x00e\x00x\x00t\x00r\x00a\x00p\x00h\x00o\x00t\x00o\x00': "com.miui.extraphoto",
                b'c\x00o\x00m\x00.\x00m\x00i\x00u\x00i\x00.\x00g\x00a\x00l\x00l\x00e\x00r\x00y\x00': "com.miui.gallery",
                b'c\x00o\x00m\x00.\x00x\x00i\x00a\x00o\x00m\x00i\x00.\x00c\x00a\x00m\x00e\x00r\x00a\x00': "com.xiaomi.camera"
            }
            for pattern, name in targets.items():
                if pattern in data:
                    return name
            
            # If not found, try to extract any UTF-16-LE string matching com.*
            # We look for a pattern like: c\x00o\x00m\x00.\x00[a-z0-9_.\x00]+
            # Let's decode the whole file as UTF-16-LE (ignoring errors) and search
            text = data.decode('utf-16-le', errors='ignore')
            matches = re.findall(r'com\.[a-zA-Z0-9_\.]+', text)
            if matches:
                # Filter out garbage
                valid_pkgs = [m for m in matches if len(m) > 10 and not m.endswith('.')]
                if valid_pkgs:
                    return f"Detected packages: {list(set(valid_pkgs))[:3]}"
                    
            return "Unknown package"
    except Exception as e:
        return f"error: {e}"

def main():
    apks = [
        r"C:\Users\MP2DX\Downloads\MiuiExtraPhoto.apk",
        r"C:\Users\MP2DX\Downloads\MiuiCamera.apk"
    ]
    for apk in apks:
        p = Path(apk)
        if p.exists():
            pkg = get_apk_package(p)
            print(f"APK: {p.name}")
            print(f"  Path: {p}")
            print(f"  Size: {p.stat().st_size / (1024*1024):.2f} MB")
            print(f"  Package detected: {pkg}")
            print("-" * 40)
        else:
            print(f"APK not found: {apk}")

if __name__ == "__main__":
    main()
