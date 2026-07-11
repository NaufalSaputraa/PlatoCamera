# PlatoCamera Magisk/KernelSU Module

HyperOS MiuiCamera port module for Xiaomi 12T (plato) on AOSP custom ROMs (Android 15 & 16).

## Features

- **Full HyperOS Camera Port**: Access all native Xiaomi camera modes (108MP, Night Mode, Portrait, Pro Mode, Video Stabilization).
- **Dual Support**: Fully compatible with both **Magisk** and **KernelSU Next / APatch**.
- **Automated Conflict Resolution**: Automatically hides stock AOSP camera apps (Aperture / stock Camera2) to prevent package conflicts with `com.android.camera`.
- **Auto Permission Grant**: Automatically sets correct permission policies and grants runtime user permissions on first boot.
- **SELinux Permissive for Camera HAL**: Avoids camera access crashes on AOSP ROMs by marking `mtk_hal_camera` as permissive.

## Installation

1. Download the compiled `PlatoCamera.zip`.
2. Open **Magisk app** or **KernelSU / APatch Manager**.
3. Select **Install from storage** and choose the `PlatoCamera.zip`.
4. Reboot your device.
5. On the first boot, the helper script will automatically grant all permissions to the camera app. Allow up to 20-30 seconds after booting before opening the app.

## How It Works

- The module places `MiuiCamera.apk` in `/system/system_ext/priv-app/MiuiCamera/` and loads required proprietary MTK camera libraries into `/system/system_ext/lib64/`.
- Uses `/system/etc/device_features/plato.xml` to load device-specific configurations (sensor profile, features availability).
- Adds privileged permission allowlist to prevent permission signature issues.
- Modifies system properties (`system.prop`) to register the camera package and MIUI notch support.
