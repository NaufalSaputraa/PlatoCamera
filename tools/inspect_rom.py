import subprocess
import re
from pathlib import Path

Z7_PATH = r"C:\Program Files\7-Zip\7z.exe"
DUMP_DIR = Path(r"D:\tmp\infinity_dump")
IMAGES = ["system.img", "system_ext.img", "product.img"]

def list_files_in_image(img_name: str):
    img_path = DUMP_DIR / img_name
    if not img_path.exists():
        print(f"[-] Image {img_name} does not exist.")
        return []

    print(f"[*] Listing files in {img_name}...")
    try:
        # Run 7z l to list files
        result = subprocess.run(
            [Z7_PATH, "l", str(img_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        
        # Parse the output to find file paths
        files = []
        lines = result.stdout.splitlines()
        
        # 7z l output table columns: Date Time Attr Size Compressed Name
        # We find the table rows after the dashes line
        in_table = False
        for line in lines:
            if line.startswith("-------------------"):
                if not in_table:
                    in_table = True
                else:
                    in_table = False  # End of table
                continue
            
            if in_table:
                # Format: 2026-06-29 11:36:00 ....A         4899         4899  path/to/file
                match = re.match(r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s+[.\w]{5}\s+\d+\s+\d+\s+(.*)", line)
                if match:
                    files.append(match.group(1).strip())
        return files
    except Exception as e:
        print(f"[-] Error listing {img_name}: {e}")
        return []

def main():
    keywords = ["camera", "miui", "companion", "algoup", "mianode", "isphal"]
    
    for img in IMAGES:
        files = list_files_in_image(img)
        print(f"[*] Found {len(files)} total files in {img}. Filtering...")
        
        matched_files = []
        for file in files:
            file_lower = file.lower()
            if any(kw in file_lower for kw in keywords):
                matched_files.append(file)
                
        if matched_files:
            print(f"\n[+] Matches in {img}:")
            for f in sorted(matched_files):
                print(f"  {f}")
            print("\n" + "="*50 + "\n")
        else:
            print(f"[-] No camera-related files found in {img}.\n")

if __name__ == "__main__":
    main()
