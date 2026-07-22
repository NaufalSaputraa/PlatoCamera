#!/system/bin/sh
# PlatoCamera Module Uninstall Script

# Clear camera app data
pm clear com.android.camera
pm clear com.miui.extraphoto

# Re-enable stock camera apps if they were disabled
pm enable org.lineageos.aperture
pm enable com.google.android.apps.googlecamera.fishfood

# Clean up internal storage cache directory if any
rm -rf /sdcard/.ANXCamera
rm -rf /storage/emulated/0/.ANXCamera

# Clean up PlatoCamera temp files
rm -f /data/local/tmp/platocamera_boot.txt
rm -f /data/local/tmp/platocamera_debug.log
rm -f /data/local/tmp/platocamera_setup_done
rm -f /data/local/tmp/platocamera_autolog.pid
