#!/sbin/sh
# PlatoCamera Installer Customization Script
# Compatible with Magisk & KernelSU Next

# Check Device Codename
CODENAME=$(getprop ro.product.device)
ui_print "- Detected device: $CODENAME"

if [ "$CODENAME" != "plato" ]; then
    ui_print "****************************************************"
    ui_print " WARNING: This module is designed for Xiaomi 12T (plato)."
    ui_print " Your device codename is reported as: $CODENAME"
    ui_print " Installing anyway, but compatibility is not guaranteed!"
    ui_print "****************************************************"
else
    ui_print "- Device is Xiaomi 12T (plato). Proceeding..."
fi

# Check Android Version (SDK Level)
API_LEVEL=$(getprop ro.build.version.sdk)
ui_print "- Android SDK level: $API_LEVEL"
if [ "$API_LEVEL" -lt 35 ]; then
    ui_print "- Android version is below Android 15 (SDK 35)."
    ui_print "  Note: This module was optimized for Android 15-16,"
    ui_print "  but it may still work on older versions."
fi

# No REPLACE logic is used to avoid overlayfs mount failures on /product/app.
# Instead, stock packages are disabled via pm disable in service.sh on boot.

# Set standard permissions for module files
ui_print "- Setting file permissions..."
set_perm_recursive $MODPATH 0 0 0755 0644
# Ensure libraries have execute permissions if required
set_perm_recursive $MODPATH/system/lib64 0 0 0755 0755

# Generate autolog script for crash/error capture
ui_print "- Creating autolog script..."
cat << 'AUTOLOG' > "$MODPATH/autolog.sh"
#!/system/bin/sh
# PlatoCamera Auto-Logger
# Captures crashes & errors automatically

TMP_DIR="/data/local/tmp/plato_logs"
SD_DIR="/sdcard/PlatoCamera_Logs"
PID_FILE="/data/local/tmp/platocamera_autolog.pid"
STAMP="$TMP_DIR/_status.txt"
mkdir -p "$TMP_DIR"

# Write status for debugging
echo "autolog: starting at $(date)" > "$STAMP"

# Only one instance
if [ -f "$PID_FILE" ] && kill -0 "$(cat $PID_FILE)" 2>/dev/null; then echo "autolog: already running" >> "$STAMP"; exit 0; fi
echo $$ > "$PID_FILE"
echo "autolog: PID $$ running" >> "$STAMP"

# Try to create sdcard dir (may fail early in boot, that's OK)
mkdir -p "$SD_DIR" 2>/dev/null && echo "autolog: sdcard OK" >> "$STAMP" || echo "autolog: sdcard not ready" >> "$STAMP"

LAST_EVENT=""

LAST_EVENT=""
while true; do
  # Check crash buffer
  CRASH=$(logcat -b crash -t 50 2>/dev/null | grep -iE "com.android.camera|com.miui.extraphoto|FATAL EXCEPTION|Native crash|DEBUG.*pid")
  # Check ANR from events buffer
  ANR=$(logcat -b events -t 20 2>/dev/null | grep -iE "am_anr.*com.android.camera|am_anr.*com.miui.extraphoto")
  # Check non-fatal errors from camera tags
  ERR=$(logcat -d -t 20 -s "Camera" "CameraService" "ExtraPhoto" "CameraDevice" "MIUICamera" 2>/dev/null | grep -iE "error|failed|exception|fatal")
  # Unique fingerprint of current state
  EVENT_SUM="$CRASH $ANR $ERR"
  if [ -n "$EVENT_SUM" ] && [ "$EVENT_SUM" != "$LAST_EVENT" ]; then
    TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
    EVENT_TYPE="log"
    [ -n "$CRASH" ] && EVENT_TYPE="crash"
    [ -n "$ANR" ] && EVENT_TYPE="anr"
    {
      echo "=== PlatoCamera Auto-Log: $TIMESTAMP ==="
      echo "=== Type: $EVENT_TYPE ==="
      echo ""
      [ -n "$CRASH" ] && echo "--- CRASH DETECTED ---" && logcat -b crash -d -v threadtime 2>/dev/null
      [ -n "$ANR" ] && echo "--- ANR DETECTED ---" && logcat -b events -d -v threadtime 2>/dev/null | grep -iE "am_anr|am_crash"
      echo "--- Camera/ExtraPhoto Logs ---"
      logcat -d -v threadtime 2>/dev/null | grep -iE "Camera|ExtraPhoto|extraphoto|mivi|algoup"
      echo ""
      echo "--- Camera Service Errors ---"
      logcat -d -v threadtime 2>/dev/null | grep -iE "CameraService|CameraDevice|ICamera"
      echo ""
      echo "--- SELinux Denials ---"
      logcat -d 2>/dev/null | grep "avc: denied"
      echo ""
      echo "--- Kernel Messages ---"
      dmesg 2>/dev/null | tail -50
      echo ""
      echo "--- Camera HAL Properties ---"
      getprop 2>/dev/null | grep -i "camera"
      echo ""
      echo "=== END ==="
    } > "$TMP_DIR/${EVENT_TYPE}_$TIMESTAMP.txt"
    # Also copy to sdcard if available
    cp "$TMP_DIR/${EVENT_TYPE}_$TIMESTAMP.txt" "$SD_DIR/" 2>/dev/null
    echo "autolog: event $EVENT_TYPE at $TIMESTAMP" >> "$STAMP"
    LAST_EVENT="$EVENT_SUM"
  fi
  # Trim old logs (keep last 20)
  ls -t "$TMP_DIR"/*.txt 2>/dev/null | tail -n +21 | xargs rm -f 2>/dev/null
  sleep 300
done
AUTOLOG

chmod 0755 "$MODPATH/autolog.sh"

# Create a persistent service.sh script to reset bootloop counter and grant permissions
ui_print "- Creating post-boot helper script..."
cat << 'EOF' > "$MODPATH/service.sh"
#!/system/bin/sh
# PlatoCamera boot helper script
# Resets bootloop counter and handles first-boot setup

LOG_FILE="/data/local/tmp/platocamera_debug.log"

# Wait for system boot to complete
while [ "$(getprop sys.boot_completed)" != "1" ]; do
  sleep 2
done

# Reset bootloop protection counter
echo "0" > "/data/local/tmp/platocamera_boot.txt"
echo "[service] System booted successfully. Counter reset to 0." >> "$LOG_FILE"

# Start autologger in background with debug log
MODDIR=${0%/*}
sh "$MODDIR/autolog.sh" >> "$LOG_FILE" 2>&1 &
echo "[service] Autolog started" >> "$LOG_FILE"

# Run setup (permissions grant and data clear) only ONCE after install/update
FLAG_FILE="/data/local/tmp/platocamera_setup_done"
if [ ! -f "$FLAG_FILE" ]; then
  echo "[service] Starting first-boot setup..." >> "$LOG_FILE"
  # Extra delay to ensure package manager is ready
  sleep 8

  # Bypass ANGLE GraphicsEnvironment NPE crash on Infinity-X ROM
  # com.android.angle package absent causes queryAngleChoice to NPE
  # Setting per-app driver selection to "default" skips the allowlist resource lookup
  settings put global angle_gl_driver_selection_pkgs "com.android.camera" > /dev/null 2>&1
  settings put global angle_gl_driver_selection_values "native" > /dev/null 2>&1
  echo "[service] ANGLE bypass set for com.android.camera" >> "$LOG_FILE"

  # Disable stock cameras to prevent dual-app layout
  for stock_pkg in org.lineageos.aperture com.google.android.apps.googlecamera.fishfood; do
    pm disable $stock_pkg >/dev/null 2>&1
    echo "[service] Disabled stock camera package: $stock_pkg" >> "$LOG_FILE"
  done

  # Loop through our packages
  for pkg in com.android.camera com.miui.extraphoto; do
    echo "[service] Granting permissions for: $pkg" >> "$LOG_FILE"
    # Clear package data to reset permissions
    pm clear $pkg >/dev/null 2>&1
    sleep 2

    # Auto grant all package permissions requested by the app
    dumpsys package $pkg | grep 'android.permission' | grep -v '/' | sed 's/:.*//g; s/ //g; /^$/d' | sort -u | while read perm; do
      pm grant $pkg $perm >/dev/null 2>&1
      echo "  Granted: $perm" >> "$LOG_FILE"
    done

    # Explicitly grant critical storage AppOps
    appops set $pkg MANAGE_EXTERNAL_STORAGE allow >/dev/null 2>&1
    appops set $pkg READ_EXTERNAL_STORAGE allow >/dev/null 2>&1
    appops set $pkg WRITE_EXTERNAL_STORAGE allow >/dev/null 2>&1

    # Enable all appops permissions
    appops get $pkg 2>/dev/null | grep -i 'mode:' | sed 's/.*Uid mode://i; s/:.*//; s/ //g; /^$/d' | sort -u | while read op; do
      appops set --uid $pkg $op allow >/dev/null 2>&1
      appops set $pkg $op allow >/dev/null 2>&1
    done
    echo "[service] Appops granted for: $pkg" >> "$LOG_FILE"
  done
  
  # Mark setup as done
  touch "$FLAG_FILE"
  echo "[service] First-boot setup completed successfully." >> "$LOG_FILE"
fi
EOF

# Ensure scripts have execute permissions
chmod 0755 "$MODPATH/service.sh"
chmod 0755 "$MODPATH/post-fs-data.sh"

# Reset setup flag to trigger permission grant on first boot
rm -f /data/local/tmp/platocamera_setup_done
rm -f /data/local/tmp/platocamera_boot.txt
rm -f /data/local/tmp/platocamera_debug.log

ui_print "- Module installation successful!"
