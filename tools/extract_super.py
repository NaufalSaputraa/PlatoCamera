#!/usr/bin/env python3
"""
extract_super.py - Extract super.img from HyperOS ROM for PlatoCamera module
Downloads lpunpack + simg2img tools and extracts system_ext, product partitions.

Usage:
    python extract_super.py <path_to_super.img> [output_dir]
"""

import os
import sys
import subprocess
import zipfile
import shutil
import urllib.request
import tempfile
from pathlib import Path


# GitHub release for prebuilt partition tools (Windows)
# From: https://github.com/thka2016/lpunpack_and_lpmake_cmake/releases/tag/220922
LPUNPACK_URL = "https://github.com/thka2016/lpunpack_and_lpmake_cmake/releases/download/220922/lpunpack.exe"
CYGWIN_DLL_URL = "https://github.com/thka2016/lpunpack_and_lpmake_cmake/releases/download/220922/cygwin1.dll"
SIMG2IMG_URL = "https://github.com/thka2016/lpunpack_and_lpmake_cmake/releases/download/220922/simg2img.exe"


def download_file(url: str, dest: Path) -> bool:
    """Download a single file from URL."""
    try:
        print(f"    Downloading {dest.name}...")
        urllib.request.urlretrieve(url, str(dest))
        print(f"    [OK] {dest.name} ({dest.stat().st_size / 1024:.0f} KB)")
        return True
    except Exception as e:
        print(f"    [!] Failed to download {dest.name}: {e}")
        return False


def download_tools(tools_dir: Path) -> Path:
    """Download lpunpack and dependencies."""
    tools_dir.mkdir(parents=True, exist_ok=True)
    lpunpack_exe = tools_dir / "lpunpack.exe"
    cygwin_dll = tools_dir / "cygwin1.dll"
    simg2img_exe = tools_dir / "simg2img.exe"

    if lpunpack_exe.exists() and cygwin_dll.exists():
        print(f"[OK] Tools already present in {tools_dir}")
        return lpunpack_exe

    print("[*] Downloading partition tools...")

    success = True
    if not lpunpack_exe.exists():
        success = download_file(LPUNPACK_URL, lpunpack_exe) and success
    if not cygwin_dll.exists():
        success = download_file(CYGWIN_DLL_URL, cygwin_dll) and success
    if not simg2img_exe.exists():
        success = download_file(SIMG2IMG_URL, simg2img_exe) and success

    if not lpunpack_exe.exists() or not cygwin_dll.exists():
        print()
        print("=== MANUAL DOWNLOAD REQUIRED ===")
        print("Download from: https://github.com/thka2016/lpunpack_and_lpmake_cmake/releases/tag/220922")
        print("Required files: lpunpack.exe, cygwin1.dll")
        print(f"Place them in: {tools_dir}")
        sys.exit(1)

    print(f"[OK] All tools ready in {tools_dir}")
    return lpunpack_exe


def run_lpunpack(lpunpack_exe: Path, super_img: Path, output_dir: Path, slot: int = 0):
    """Run lpunpack to extract partitions from super.img."""
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[*] Extracting super.img (slot {slot})...")
    print(f"    Input:  {super_img}")
    print(f"    Output: {output_dir}")
    print(f"    Size:   {super_img.stat().st_size / (1024**3):.2f} GB")
    print()
    print("    This may take several minutes depending on disk speed...")
    print()

    cmd = [
        str(lpunpack_exe),
        f"--slot={slot}",
        str(super_img),
        str(output_dir)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        if result.returncode != 0:
            print(f"[!] lpunpack failed (exit code {result.returncode})")
            if result.stderr:
                print(f"    stderr: {result.stderr.strip()}")
            # Try without slot flag
            print("[*] Retrying without --slot flag...")
            cmd_no_slot = [str(lpunpack_exe), str(super_img), str(output_dir)]
            result = subprocess.run(cmd_no_slot, capture_output=True, text=True, timeout=1800)
            if result.returncode != 0:
                print(f"[!] lpunpack failed again: {result.stderr.strip()}")
                sys.exit(1)

        print("[OK] super.img extracted successfully!")
    except subprocess.TimeoutExpired:
        print("[!] Extraction timed out (30 min limit)")
        sys.exit(1)
    except FileNotFoundError:
        print(f"[!] Cannot execute: {lpunpack_exe}")
        sys.exit(1)


def list_extracted_partitions(output_dir: Path):
    """List extracted partition images."""
    print("\n[*] Extracted partitions:")
    partitions = []
    for f in sorted(output_dir.iterdir()):
        if f.is_file() and f.suffix == ".img":
            size_mb = f.stat().st_size / (1024**2)
            print(f"    {f.name:40s} {size_mb:>10.1f} MB")
            partitions.append(f.name)
    return partitions


def mount_ext4_image(img_path: Path, mount_dir: Path):
    """
    On Windows, we can't directly mount ext4.
    Instead, use 7-Zip or ext2read to extract.
    This function tries 7z first.
    """
    mount_dir.mkdir(parents=True, exist_ok=True)

    # Try 7z
    seven_zip_paths = [
        r"C:\Program Files\7-Zip\7z.exe",
        r"C:\Program Files (x86)\7-Zip\7z.exe",
        shutil.which("7z") or "",
    ]

    seven_zip = None
    for p in seven_zip_paths:
        if p and Path(p).exists():
            seven_zip = p
            break

    if seven_zip:
        print(f"[*] Extracting {img_path.name} using 7-Zip...")
        cmd = [seven_zip, "x", str(img_path), f"-o{mount_dir}", "-y"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            print(f"[OK] {img_path.name} extracted to {mount_dir}")
            return True
        else:
            print(f"[!] 7-Zip extraction failed: {result.stderr[:200]}")

    print(f"[!] Cannot extract {img_path.name}")
    print("    Install 7-Zip (https://7-zip.org/) and try again,")
    print(f"    or manually extract {img_path} to {mount_dir}")
    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_super.py <path_to_super.img> [output_dir]")
        print()
        print("Example:")
        print('  python extract_super.py "D:\\rom\\images\\super.img" "D:\\rom\\extracted"')
        sys.exit(1)

    super_img = Path(sys.argv[1])
    if not super_img.exists():
        print(f"[!] File not found: {super_img}")
        sys.exit(1)

    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else super_img.parent / "super_extracted"
    tools_dir = Path(__file__).parent / "bin"

    print("=" * 60)
    print("  PlatoCamera - super.img Extractor")
    print("=" * 60)
    print()

    # Step 1: Download tools
    lpunpack_exe = download_tools(tools_dir)

    # Step 2: Extract super.img
    run_lpunpack(lpunpack_exe, super_img, output_dir)

    # Step 3: List partitions
    partitions = list_extracted_partitions(output_dir)

    # Step 4: Extract relevant partition images
    target_partitions = ["product.img", "system_ext.img", "system.img"]
    print("\n[*] Now extracting relevant partition images...")

    for part_name in target_partitions:
        part_img = output_dir / part_name
        if part_img.exists() and part_img.stat().st_size > 0:
            extract_dir = output_dir / part_name.replace(".img", "")
            if extract_dir.exists() and any(extract_dir.iterdir()):
                print(f"[SKIP] {part_name} already extracted to {extract_dir}")
                continue
            mount_ext4_image(part_img, extract_dir)
        else:
            print(f"[SKIP] {part_name} not found or empty")

    # Step 5: Summary
    print()
    print("=" * 60)
    print("  Extraction Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print(f"  1. Check extracted partitions in: {output_dir}")
    print("  2. Run: python extract_camera_files.py to copy camera files")
    print()

    # Check if camera files exist
    camera_paths = [
        output_dir / "product" / "priv-app" / "MiuiCamera" / "MiuiCamera.apk",
        output_dir / "system_ext" / "lib64",
    ]
    for p in camera_paths:
        if p.exists():
            print(f"  [FOUND] {p}")
        else:
            print(f"  [MISSING] {p}")


if __name__ == "__main__":
    main()
