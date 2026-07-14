#!/system/bin/sh
# PlatoCamera Module Uninstall Script

# Clear camera app data
pm clear com.android.camera

# Re-enable stock camera apps if they were disabled
pm enable org.lineageos.aperture
pm enable com.google.android.apps.googlecamera.fishfood

# Clean up internal storage cache directory if any
rm -rf /sdcard/.ANXCamera
rm -rf /storage/emulated/0/.ANXCamera
