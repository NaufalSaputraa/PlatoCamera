import subprocess
import re
from pathlib import Path

Z7_PATH = r"C:\Program Files\7-Zip\7z.exe"
DUMP_DIR = Path(r"D:\tmp\infinity_dump")
IMAGES = ["system.img", "system_ext.img", "product.img"]

def list_files_in_image(img_name: str):
    img_path = DUMP_DIR / img_name
    if not img_path.exists():
        return []
    try:
        result = subprocess.run(
            [Z7_PATH, "l", str(img_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        files = []
        in_table = False
        for line in result.stdout.splitlines():
            if line.startswith("-------------------"):
                in_table = not in_table
                continue
            if in_table:
                match = re.match(r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s+[.\w]{5}\s+\d+\s+\d+\s+(.*)", line)
                if match:
                    files.append(match.group(1).strip())
        return files
    except Exception as e:
        print(f"Error {img_name}: {e}")
        return []

def main():
    keywords = ["device_features", "plato", "xiaomi", "media", "audio", "camera", "miui", "companion", "algoup", "mianode", "isphal"]
    
    with open("tools/rom_matches.txt", "w", encoding="utf-8") as out:
        for img in IMAGES:
            files = list_files_in_image(img)
            matched = [f for f in files if any(kw in f.lower() for kw in keywords)]
            
            out.write(f"\n=== Matches in {img} ({len(matched)} files) ===\n")
            for f in sorted(matched):
                if "android.hardware" in f or "companiondevice" in f or "system\\lib" in f:
                    continue
                out.write(f"  {f}\n")
    print("[+] Done writing results to tools/rom_matches.txt")


if __name__ == "__main__":
    main()
