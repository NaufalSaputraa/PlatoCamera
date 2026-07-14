import zipfile
import re
from pathlib import Path

APK_PATH = Path(r"d:\Coding\PlatoCamera\system\system_ext\priv-app\MiuiCamera\MiuiCamera.apk")

def main():
    if not APK_PATH.exists():
        print(f"Error: {APK_PATH} not found!")
        return

    print(f"Opening {APK_PATH.name}...")
    with zipfile.ZipFile(APK_PATH, 'r') as z:
        manifest_data = z.read("AndroidManifest.xml")
        
    print("Decoding AndroidManifest.xml strings...")
    # Find all ASCII strings inside the binary XML string pool
    # Strings in binary XML are usually UTF-8 or UTF-16
    # Let's decode as UTF-16-LE first, then fallback to UTF-8
    
    # Try decoding UTF-16-LE
    text_utf16 = manifest_data.decode("utf-16-le", errors="ignore")
    # Try decoding UTF-8
    text_utf8 = manifest_data.decode("utf-8", errors="ignore")
    
    # We look for uses-library and other packages or libraries
    # Let's print all strings matching typical library/package formats
    all_strings = set()
    
    # Find UTF-8 printable strings (length >= 4)
    for m in re.finditer(b'([\x20-\x7E]{4,})', manifest_data):
        try:
            s = m.group(1).decode('utf-8')
            all_strings.add(s)
        except:
            pass
            
    # Find UTF-16 LE printable strings (length >= 4)
    # A UTF-16 character is 2 bytes, printable if the first is 0x20-0x7E and second is 0x00
    # Or just search regex in decoded text
    for m in re.finditer(r'[a-zA-Z0-9_\-\.\:\/]{4,}', text_utf16):
        all_strings.add(m.group(0))
        
    for m in re.finditer(r'[a-zA-Z0-9_\-\.\:\/]{4,}', text_utf8):
        all_strings.add(m.group(0))

    print("\n--- Libraries and Framework dependencies ---")
    library_patterns = [
        r'com\.miui\..*',
        r'com\.xiaomi\..*',
        r'mediatek\..*',
        r'uses-library',
        r'.*camera.*',
        r'android\.permission\..*',
        r'android\.hardware\..*'
    ]
    
    matched = []
    for s in all_strings:
        for pat in library_patterns:
            if re.match(pat, s, re.IGNORECASE):
                matched.append(s)
                break
                
    for m in sorted(matched):
        print(f"  {m}")

if __name__ == "__main__":
    main()
