# Checkpoint 6 Summary: PlatoCamera Modding & AOSP Compatibility

Below is the compressed session state for the next AI session. Copy and paste the block below to start the next session.

---

```markdown
## PlatoCamera Project Context & State (Checkpoint 6)

### Device & OS Context
* Device: Xiaomi 12T (codename: `plato`)
* ROM: AOSP (Android 15-16)
* Root: KernelSU Next + meta-hybrid_mount (Hybrid Mount)
* User requirement: Upgrade system camera to MIUI Camera v6.1 (universal port).

### Status Summary
* **Magisk Module**: Version `v1.4.7-Stable` (versionCode `1470`).
* **Target ZIP**: `d:\Coding\PlatoCamera\PlatoCamera-v1.4.7-Stable.zip`.
* **Path**: `/system/priv-app/MiuiCamera/MiuiCamera.apk` (165 MB, Sevtinge v1.1.1 AOSP Universal Port APK).
* **Official ROM Device Tree Reference**: `https://github.com/mt6895-plato` (specifically `android_device_xiaomi_plato-miuicamera` for Xiaomi 12T AOSP builds).

### Problems Resolved & Technical Implementations
1. **Hybrid Mount OverlayFS Unmount Crash**:
   * *Cause*: KernelSU `hybrid_mount` module unmounts overlayfs for non-root apps when `disable_umount = false`, hiding `MiuiCamera.apk` from the camera namespace and causing `java.io.IOException: Failed to load asset path` / `LoadedApk.mResources = null`.
   * *Fix*: Set `disable_umount = true` in `/data/adb/hybrid-mount/config.toml`.
2. **ANGLE GraphicsEnvironment NPE**:
   * *Cause*: AOSP ROMs lacking `com.android.angle` trigger NPE in `queryAngleChoice`.
   * *Fix*: Automatic first-boot execution sets `angle_gl_driver_selection_values=native` for `com.android.camera`.
3. **MIVI Parallel Processing & Signature Validation**:
   * Integrated Sevtinge v1.1.1 universal AOSP port APK (7 DEX layers) with 12 MP (Pixel Binning) and 108 MP (Remosaic) modes fully functional.
   * Cleared `.idsig` files so PackageManager registers the launcher icon automatically.

### Official Reference & Future Maintenance
* Official AOSP device tree reference for Xiaomi 12T (`plato`): `https://github.com/mt6895-plato/android_device_xiaomi_plato-miuicamera`
```
