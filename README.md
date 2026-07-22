# PlatoCamera Magisk/KernelSU Module

HyperOS MiuiCamera port module for Xiaomi 12T (plato) on AOSP custom ROMs (Android 15 & 16).

---

## 🇮🇩 Panduan Penggunaan (Bahasa Indonesia)

### 🌟 Fitur Utama
- **Porting Kamera HyperOS Lengkap**: Akses seluruh mode kamera bawaan (108 MP, Mode Malam, Potret, Mode Pro, Filter Leica, Stabilisasi Video).
- **Kompatibel Magisk & KernelSU**: Berjalan lancar di Magisk, KernelSU Next, maupun APatch.
- **Resolusi Konflik Otomatis**: Otomatis menonaktifkan kamera bawaan ROM AOSP (Aperture / Camera2) agar tidak bentrok.
- **Auto Permissions & Fixed ANGLE**: Ikon otomatis muncul dan masalah crash ANGLE di Android 15/16 teratasi secara otomatis.

---

### 🛠️ Cara Instalasi (WAJIB DIBACA)

1. **Pengguna KernelSU & Hybrid Mount (LANGKAH KRUSIAL)**:
   - Pastikan modul **`hybrid_mount`** sudah terpasang dan aktif di KernelSU.
   - Buka file `/data/adb/hybrid-mount/config.toml` (pakai MT Manager / Termux / Root Explorer) dan pastikan pengaturannya:
     ```toml
     disable_umount = true
     ```
   - *Alasan*: Secara default `hybrid_mount` menyembunyikan modul dari aplikasi non-root. Jika bernilai `false`, file APK kamera akan terlepas (*unmounted*) dan menyebabkan kamera crash saat dibuka (`Failed to load asset path`).

2. **Flash Modul**:
   - Unduh file `PlatoCamera-v1.4.7-Stable.zip` dari halaman Release.
   - Flash file zip tersebut di **KernelSU Manager** atau **Magisk**.

3. **Reboot HP (WAJIB REBOOT DULU)**:
   - Restart HP kamu setelah flash selesai.

4. **Beri Akses Superuser / Root (Penting untuk KernelSU)**:
   - Setelah HP menyala kembali, buka aplikasi **KernelSU Next** (atau APatch).
   - Masuk ke tab **Superuser** (ikon perisai).
   - Cari **Kamera** (`com.android.camera`) dan aktifkan izin root-nya.
   - Jika **ExtraPhoto** (`com.miui.extraphoto`) muncul, aktifkan juga izin root-nya.

5. **Hapus Data Aplikasi Kamera (WAJIB)**:
   - Buka **Pengaturan HP -> Aplikasi -> Kamera -> Penyimpanan** lalu tekan **Hapus Data / Hapus Penyimpanan**.
   - Buka aplikasi kamera, berikan semua izin yang diminta, dan kamera siap digunakan!

> 💡 **Catatan File `PlatoCamera.apk` di Release**:
> Ikon kamera **otomatis muncul** di homescreen cukup dengan memasang modul zip di atas. File `PlatoCamera.apk` yang ada di halaman Release sifatnya **Opsional (hanya cadangan)** jika ada launcher AOSP kustom tertentu yang gagal membaca ikon aplikasi sistem.

---

### 🔒 Verifikasi Keamanan (SHA256 Checksums)

Kamu bisa memverifikasi keaslian file yang diunduh menggunakan hash SHA-256 berikut:

| Nama File | SHA-256 Checksum |
|---|---|
| `PlatoCamera-v1.4.7-Stable.zip` | `cb435857827180f4527962152474e48a438762ca3712867874e3c12555e12a61` |
| `PlatoCamera.apk` | `9aaf3049d66c4afe3d64b015e107e8b3843b6b0c18248af62109192ac8de72a2` |

---

## 🇬🇧 English Guide

### Installation & Configuration (MANDATORY)

1. **Prerequisites (KernelSU & Hybrid Mount Users - CRITICAL)**:
   - Ensure **`hybrid_mount`** is installed in KernelSU.
   - Open `/data/adb/hybrid-mount/config.toml` on your device and set:
     ```toml
     disable_umount = true
     ```
   - *Why?* By default, `hybrid_mount` unmounts overlays for non-root apps. If `disable_umount = false`, OverlayFS hides `MiuiCamera.apk`, causing startup crashes.

2. **Flash Module**:
   - Download `PlatoCamera-v1.4.7-Stable.zip` from Releases.
   - Flash in **KernelSU Manager** or **Magisk**.

3. **Reboot**:
   - Reboot your device.

4. **Grant Superuser Access (KernelSU / SuSFS)**:
   - Open **KernelSU Next** -> **Superuser** tab.
   - Enable Root access for **Kamera** (`com.android.camera`) and **ExtraPhoto** (`com.miui.extraphoto`).

5. **Clear App Data**:
   - Go to **Settings -> Apps -> Camera -> Storage -> Clear Data**.
   - Open the app, grant permissions, and enjoy!

> 💡 **Note on standalone `PlatoCamera.apk` in Releases**:
> Launcher icons now **automatically appear** upon flashing the ZIP. The standalone `PlatoCamera.apk` in the Releases section is purely **optional (backup)** for custom launchers that fail to index system apps.
