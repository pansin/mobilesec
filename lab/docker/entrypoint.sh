#!/bin/bash
set -e

echo "MobileSec Sandbox Entrypoint"

# Create AVDs if they don't exist
if [ ! -d "$ANDROID_EMULATOR_HOME/avd" ] || [ -z "$(ls -A $ANDROID_EMULATOR_HOME/avd 2>/dev/null)" ]; then
    echo "Creating AVDs for first time..."
    /opt/scripts/create_avds.sh
fi

# Set permissions
sudo chown -R android:android /opt/emulators /data

# Source environment
export PATH="$PATH:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/emulator"

echo ""
echo "Sandbox environment ready!"
echo ""
echo "Available commands:"
echo "  adb devices                    - List connected devices"
echo "  /opt/scripts/start_emulators.sh - Start all emulators"
echo "  frida-ps -U                    - List processes on USB device"
echo "  objection -h                   - Objection help"
echo ""
exec "$@"