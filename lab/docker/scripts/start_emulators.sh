#!/bin/bash
set -e

echo "Starting Android Emulators..."

# Function to start an emulator
start_emulator() {
    local avd_name=$1
    local port=$2
    local options=$3

    echo "Starting $avd_name on port $port..."
    emulator -avd "$avd_name" \
        -no-window \
        -no-audio \
        -no-boot-anim \
        -port "$port" \
        $options &
}

# Start emulators
start_emulator "stock-android-13" 5554 ""
start_emulator "rooted-android-11" 5556 "-writable-system"
start_emulator "frida-android-12" 5558 "-writable-system"

echo "Emulators starting in background..."
echo "Use 'adb devices' to check status"
echo "Use 'adb -s emulator-<port> shell' to connect"