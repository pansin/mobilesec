#!/bin/bash
# Frida Server 自动下载脚本

set -e

FRIDA_DIR="/usr/local/frida-server"
cd "$FRIDA_DIR"

# 获取已安装的 frida-tools 版本
if ! FRIDA_VERSION=$(pip3 show frida-tools | grep -E 'Version:' | awk '{print $2}'); then
    echo "Error: frida-tools not installed. Installing now..."
    pip3 install frida-tools
    FRIDA_VERSION=$(pip3 show frida-tools | grep -E 'Version:' | awk '{print $2}')
fi

echo "Current frida-tools version: $FRIDA_VERSION"

# 需要下载的架构
ARCHITECTURES=("arm" "arm64" "x86" "x86_64")
SUCCESS_COUNT=0

for ARCH in "${ARCHITECTURES[@]}"; do
    SERVER_FILE="frida-server-${FRIDA_VERSION}-android-${ARCH}"
    OUTPUT_FILE="frida-server-${ARCH}"

    if [ -f "$OUTPUT_FILE" ]; then
        echo "Frida Server for $ARCH already exists"
        continue
    fi

    echo "Downloading Frida Server for $ARCH..."
    wget -q "https://github.com/frida/frida/releases/download/${FRIDA_VERSION}/${SERVER_FILE}.xz" -O "${SERVER_FILE}.xz"

    if [ $? -eq 0 ]; then
        echo "Extracting..."
        xz -d "${SERVER_FILE}.xz"
        mv "${SERVER_FILE}" "${OUTPUT_FILE}"
        chmod +x "${OUTPUT_FILE}"
        rm -f "${SERVER_FILE}.xz"
        echo "Successfully downloaded Frida Server for $ARCH"
        ((SUCCESS_COUNT++))
    else
        echo "Failed to download Frida Server for $ARCH"
        rm -f "${SERVER_FILE}.xz"
    fi
done

echo "Download process complete!"
echo "Successfully downloaded: $SUCCESS_COUNT architectures"

ls -la "$FRIDA_DIR"
