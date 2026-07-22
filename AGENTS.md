# PlatoCamera — AGENTS.md

## Bahasa

Balas semua komunikasi dalam **Bahasa Indonesia** yang mudah dipahami, kecuali diminta lain.

## Uteke Memory (WAJIB)

Uteke adalah semantic memory engine (Rust, lokal, offline). Data di `%USERPROFILE%\.uteke\`.

### Session Start Protocol

1. Pastikan `uteke-serve` berjalan (port 8767). Jika tidak:
   ```powershell
   $env:PATH += ";$env:USERPROFILE\AppData\Local\bin"
   Start-Process -FilePath "uteke-serve" -WindowStyle Hidden -ArgumentList "--port 8767"
   Start-Sleep -Seconds 3
   ```
2. Recall memori relevan dengan topik sesi ini:
   ```powershell
   $body = @{ query = "<topik>" } | ConvertTo-Json
   Invoke-RestMethod -Uri "http://127.0.0.1:8767/recall" -Method Post -Body $body -ContentType "application/json"
   ```
3. Terapkan konteks dari hasil recall secara **diam-diam** (jangan disebutkan除非 diminta).

### API Endpoints (localhost:8767)

| Method | Endpoint | Fungsi |
|---|---|---|
| `POST` | `/remember` | Simpan memori `{ content, tags, memory_type }` |
| `POST` | `/recall` | Cari memori `{ query }` (semantic) |
| `POST` | `/search` | Cari memori `{ query }` (keyword) |
| `GET` | `/stats` | Statistik database |

### Kapan menyimpan

- Konteks penting tentang user (preferensi, setup, environment)
- Keputusan arsitektur yang sudah dibuat
- Masalah yang sudah terdiagnosis + solusinya
- Konvensi repo yang tidak obvious dari kode

Jangan simpan: rahasia/kunci API, path file yang bisa dicari, kode yang bisa dibaca dari file.

## What this is

Magisk/KernelSU module that ports HyperOS MiuiCamera to Xiaomi 12T (plato) on AOSP ROMs (Android 15-16). Flashable `.zip` + standalone APK.

## Build & package

```bash
python pack.py
```
Output: `PlatoCamera-v<version>-<channel>.zip` (skips `tools/`, old zips, `.git`, `.agents`, `PlatoCamera.apk` via `EXCLUDE_PATTERNS` in `pack.py`).

**Must update `EXCLUDE_PATTERNS` and `OUTPUT_ZIP` in `pack.py` when bumping version.**

CI release (`.github/workflows/release.yml`): tag `v*` push → `python pack.py` → `cp MiuiCamera.apk PlatoCamera.apk` → GitHub Release with both assets.

## Module structure

| Path | Role |
|---|---|
| `system/priv-app/MiuiCamera/MiuiCamera.apk` | Main camera APK (com.android.camera) |
| `system/product/priv-app/ExtraPhotoGlobal/ExtraPhotoGlobal.apk` | Editor/filter companion (com.miui.extraphoto) |
| `system/lib64/*.so` | Proprietary MTK camera libs + `libgui_shim_miuicamera.so` (AOSP libgui compat shim) |
| `system/framework/*.jar` | MIUI framework JARs (miui-cameraopt, companion) |
| `system/etc/device_features/plato.xml` + `system/product/etc/device_features/plato.xml` | Device sensor/feature config (both copies required) |
| `system/etc/permissions/` | Priv-app permission allowlists + hidden-api allowlist |
| `system/product/etc/permissions/privapp-permissions-extraphoto.xml` | ExtraPhoto separate permission config (Android 10+ partition-strict) |
| `system.prop` | Camera system props (HAL3, EIS, MIVI disabled, Leica spoof) |
| `sepolicy.rule` | SELinux rules (mtk_hal_camera permissive, priv_app access) |
| `post-fs-data.sh` | Bootloop protection (auto-disables module after 3 failed boots) |
| `customize.sh` | Installer: device check, permissions, generates `service.sh` |
| `uninstall.sh` | Cleanup: clears camera data, re-enables stock camera pkgs |

At install, `customize.sh` generates `service.sh` which on first boot: disables stock cameras (Aperture, GCam), grants all runtime permissions and appops for camera packages.

## Key tools (`tools/`)

All tools hardcode Windows absolute paths — must update `WORKSPACE` / APK paths before running.

| Script | Purpose |
|---|---|
| `pack.py` | Build module ZIP |
| `inject_dex.py` | Inject patched classes*.dex into port APK (preserves original compression rules) |
| `tweak_module.py` | Inject Leica feature flags into device_features XMLs + MTK props into system.prop |
| `inspect_apk.py` / `inspect_apk_libs.py` | Analyze APK contents / native libs |

## Critical APK modding conventions (from CHECKPOINT_6.md)

- Do **not** re-sign split APKs with a debug key — QiGigsaw signature validation crashes with NPE in GraphicsEnvironment. Patch: bypass `SignatureValidator.validateSplit` in smali (always return true).
- MIVI parallel processing causes JNI crash post-capture on AOSP — patch: all `isSupportAlgoUp`/`isSupportMIVI2` methods return false.
- `.so` files and `resources.arsc` must be stored (not compressed) in the APK. Only `.dex` files use deflate.
- APK path: `/system/priv-app/MiuiCamera/MiuiCamera.apk`, permissions 644.

## No standard test/lint/typecheck

Device-side verification only: `adb shell logcat -b crash -d`. No test runners, linters, or CI checks beyond build validity.
