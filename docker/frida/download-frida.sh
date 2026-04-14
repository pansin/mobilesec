#!/bin/bash
# Frida Server 自动下载脚本 - 非阻塞版本

set +e  # 不因为错误退出

FRIDA_DIR="/usr/local/frida-server"
cd "$FRIDA_DIR" || { echo "Error: Cannot cd to $FRIDA_DIR"; exit 0; }

# 获取已安装的 frida-tools 版本
if ! FRIDA_VERSION=$(pip3 show frida-tools 2>/dev/null | grep -E 'Version:' | awk '{print $2}'); then
    echo "Warning: frida-tools not found, will skip server download"
    exit 0
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
        ((SUCCESS_COUNT++))
        continue
    fi

    echo "Downloading Frida Server for $ARCH..."
    if wget -q "https://github.com/frida/frida/releases/download/${FRIDA_VERSION}/${SERVER_FILE}.xz" -O "${SERVER_FILE}.xz"; then
        echo "Extracting..."
        if xz -d "${SERVER_FILE}.xz"; then
            mv "${SERVER_FILE}" "${OUTPUT_FILE}"
            chmod +x "${OUTPUT_FILE}"
            rm -f "${SERVER_FILE}.xz"
            echo "Successfully downloaded Frida Server for $ARCH"
            ((SUCCESS_COUNT++))
        else
            echo "Failed to extract Frida Server for $ARCH"
            rm -f "${SERVER_FILE}.xz"
        fi
    else
        echo "Failed to download Frida Server for $ARCH (will continue without it)"
        rm -f "${SERVER_FILE}.xz" 2>/dev/null
    fi
done

echo "Download process complete!"
echo "Successfully downloaded: $SUCCESS_COUNT architectures"

ls -la "$FRIDA_DIR" 2>/dev/null

echo "=== Frida container ready ==="
