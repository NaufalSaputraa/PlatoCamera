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
* **Magisk Module**: Version `v1.4.7-Beta` (versionCode `1470`).
* **Target ZIP**: `d:\Coding\PlatoCamera\PlatoCamera-v1.4.7-Beta.zip`.
* **Path**: `/system/priv-app/MiuiCamera/MiuiCamera.apk`.
* **Note**: Smali patches below (QiGigsaw, MIVI) still apply to current version.

### Problems Resolved & Technical Implementations
1. **Startup NullPointerException in GraphicsEnvironment**:
   * *Cause*: QiGigsaw (dynamic split delivery) validates base APK signature against split APK signatures at startup inside `com.iqiyi.android.qigsaw.core.splitinstall.SignatureValidator.validateSplit`. When base APK is re-signed with a debug key, validation fails, preventing split resources from loading and crashing with NPE in `GraphicsEnvironment.queryAngleChoice`.
   * *Fix*: Modified `SignatureValidator.smali` in `smali_classes3` to bypass `validateSplit` and **always return `true`**.
2. **Post-Capture JNI Thread Crash (MIVI)**:
   * *Cause*: `ParallelDataZip` in JNI crashed after capture because the ROM lacks Xiaomi's parallel image processing daemon (MIVI/AlgoUp).
   * *Fix*: Patched `com.xiaomi.camera.mivi.MIVISDKConfig.smali` in `smali_classes3` so that all MIVI capabilities (`isSupportAlgoUp`, `isSupportMIVI2`, etc.) **always return `false`**, forcing Java capture fallback.
3. **Case Sensitivity & Android R+ Packaging Rules**:
   * Recompiling resources on Windows converted lowercase filenames (like `res/kkq.xml`) to uppercase (like `res/Kkq.xml`), causing `Resources$NotFoundException`.
   * Storing native libraries (`.so`) and `resources.arsc` compressed broke Android 11+ requirements, causing `Failed to extract native libraries` parsing errors.
   * *Fix*: Used a custom Python script to extract files, inject only the modified `classes*.dex` files, copy all original resources/libs preserving original compression (stored mode for `.so` and `resources.arsc`), and sign/zipalign with `uber-apk-signer`.

### Next Steps for the AI
1. Read `CHECKPOINT_6.md` and use the patched APK layout.
2. If further crashes occur, run `adb shell logcat -b crash -d` (device must be connected) to trace new stack traces.
3. Keep the APK path as `/system/priv-app/MiuiCamera/MiuiCamera.apk` with standard 644 permissions.
```
