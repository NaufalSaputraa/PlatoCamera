# PlatoCamera Magisk/KernelSU Module

HyperOS MiuiCamera port module for Xiaomi 12T (plato) on AOSP custom ROMs (Android 15 & 16).

## Features

- **Full HyperOS Camera Port**: Access all native Xiaomi camera modes (108MP, Night Mode, Portrait, Pro Mode, Video Stabilization).
- **Dual Support**: Fully compatible with both **Magisk** and **KernelSU Next / APatch**.
- **Automated Conflict Resolution**: Automatically hides stock AOSP camera apps (Aperture / stock Camera2) to prevent package conflicts with `com.android.camera`.
- **Auto Permission Grant**: Automatically sets correct permission policies and grants runtime user permissions on first boot.
- **SELinux Permissive for Camera HAL**: Avoids camera access crashes on AOSP ROMs by marking `mtk_hal_camera` as permissive.

## Installation & Configuration (MANDATORY)

Please follow these steps carefully to ensure the camera app launches successfully and the launcher icon appears:

1. **Prerequisites (KernelSU Users Only)**:
   - Make sure you have the **`meta-hybrid_mount`** (Hybrid Mount) module installed and active in KernelSU. This is required to support folder overlay mounting on KernelSU.
   
2. **Flash Module**:
   - Download the latest `PlatoCamera-v1.4.5-Stable.zip` from the Releases section.
   - Flash the zip file in **KernelSU Manager** or **Magisk**.
   - *Do NOT reboot your phone yet!*
   
3. **Grant Superuser (Root) Access to Camera (CRITICAL for KernelSU/SuSFS)**:
   - Open **KernelSU Next Manager** app.
   - Go to the **Superuser** tab (shield icon).
   - Find **Kamera** (`com.android.camera`) in the list.
   - Turn **ON** / **Enable** the Superuser access toggle.
   - *Why?* KernelSU and SuSFS hide modules from non-root apps. Granting root access to the Camera app bypasses this namespace restriction, allowing the app process to see and load its own files.

4. **Reboot**:
   - Reboot your device.
   
5. **Manual APK Installation for Launcher Icon (MANDATORY on AOSP)**:
   - On AOSP ROMs, the launcher often fails to scan or display icons for system apps injected via Magisk.
   - Extract the `MiuiCamera.apk` from the module zip (located inside `system/priv-app/MiuiCamera/`), or download the standalone `PlatoCamera.apk` from the GitHub release.
   - Install the APK manually on your device. This registers the app as a user app update, forcing the launcher icon to show up in your app drawer while still retaining all system libraries and permissions from the Magisk module.

6. **Clear App Data (MANDATORY)**:
   - Go to **Settings -> Apps -> Kamera -> Storage** and tap **Clear Data / Clear Storage** (Hapus Penyimpanan/Data).
   - *Why?* This is required to reset cached configuration states so the camera app registers the new patches, enabling full 60 FPS video recording and resolving visual glitches.
   - Open the app, grant all runtime permissions, and enjoy!

## How It Works

- The module overlays `MiuiCamera.apk` in `/system/priv-app/MiuiCamera/` and loads required proprietary MTK camera libraries into `/system/lib64/`.
- Includes **`libgui_shim_miuicamera.so`** in `/system/lib64/` to resolve symbol compatibility issues with the AOSP windowing library (`libgui`).
- Uses `/system/etc/device_features/plato.xml` and `/system/product/etc/device_features/plato.xml` to load device-specific configurations (sensor profile, features availability).
- Adds privileged permission allowlist to prevent permission signature issues.
- Modifies system properties (`system.prop`) to register the camera package and MIUI notch support.

