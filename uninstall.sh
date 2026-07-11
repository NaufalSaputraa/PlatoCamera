#!/system/bin/sh
# PlatoCamera Module Uninstall Script

# Clear camera app data
pm clear com.android.camera

# Clean up internal storage cache directory if any
rm -rf /sdcard/.ANXCamera
rm -rf /storage/emulated/0/.ANXCamera
