#!/system/bin/sh
# PlatoCamera Bootloop Protection Script
# Runs very early in boot (post-fs-data mode)

MODDIR=${0%/*}
COUNTER_FILE="/data/local/tmp/platocamera_boot.txt"

# Initialize count
if [ -f "$COUNTER_FILE" ]; then
    COUNT=$(cat "$COUNTER_FILE")
    # Basic validation to ensure it's a number
    case $COUNT in
        ''|*[!0-9]*) COUNT=0 ;;
    esac
else
    COUNT=0
fi

# Increment boot count
COUNT=$((COUNT + 1))
echo "$COUNT" > "$COUNTER_FILE"

# Log the boot attempt
LOG_FILE="/data/local/tmp/platocamera_debug.log"
echo "[post-fs-data] Boot attempt #$COUNT started" >> "$LOG_FILE"

# If boot fails 3 times consecutively (counter not reset by service.sh),
# disable the module automatically.
if [ "$COUNT" -gt 3 ]; then
    # Disable module in Magisk/KernelSU
    touch "$MODDIR/disable"
    echo "[FALLBACK] Boot count exceeded limit ($COUNT). PlatoCamera disabled automatically!" >> "$LOG_FILE"
fi

