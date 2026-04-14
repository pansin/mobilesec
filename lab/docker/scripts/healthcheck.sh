#!/bin/bash
set -e

# Health check script for sandbox environment

# Check if ADB is available
if ! command -v adb &> /dev/null; then
    echo "ERROR: ADB not found"
    exit 1
fi

# Check if emulators directory exists
if [ ! -d "$ANDROID_EMULATOR_HOME" ]; then
    echo "ERROR: Emulators directory not found"
    exit 1
fi

# Check if we can list AVDs
if ! avdmanager list avd &> /dev/null; then
    echo "ERROR: Cannot list AVDs"
    exit 1
fi

echo "Sandbox is healthy!"
exit 0