#!/bin/bash
set -e

echo "Creating Android Virtual Devices..."

# Create stock Android 13 AVD
echo "Creating stock-android-13 (API 33)..."
echo "no" | avdmanager create avd -n stock-android-13 -k "system-images;android-33;google_apis;x86_64" -d pixel_5 --force

# Create rooted Android 11 AVD
echo "Creating rooted-android-11 (API 30)..."
echo "no" | avdmanager create avd -n rooted-android-11 -k "system-images;android-30;default;x86_64" -d pixel_4 --force

# Create Frida-preloaded Android 12 AVD
echo "Creating frida-android-12 (API 31)..."
echo "no" | avdmanager create avd -n frida-android-12 -k "system-images;android-31;default;x86_64" -d pixel_4a --force

echo "AVDs created successfully!"
echo ""
echo "Available AVDs:"
avdmanager list avd