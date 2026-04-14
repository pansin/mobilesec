# Android Security Testing Base Image

基于官方 Kali Linux 构建的 Android 安全测试基础镜像，包含所有必要的工具和依赖。

## 构建命令

```bash
cd /Users/pansinliu/Documents/GitHub/mobilesec/docker/kali-base
docker build -t mobilesec/kali-base:latest .
```

## 工具清单

### Android SDK 和调试工具
- Android Debug Bridge (adb)
- Android SDK Platform-Tools
- scrcpy

### 反编译与逆向工具
- jadx
- apktool
- dex2jar
- jd-gui
- ghidra (需额外配置)

### 动态分析工具
- frida-tools
- frida-server (arm/arm64/x86/x86_64)
- objection
- xposed framework

### 静态分析工具
- qark
- androidlint
- checksec
- libchecker

### 网络分析工具
- wireshark
- tcpdump
- mitmproxy
- ngrep

### 其他工具
- python3
- python3-pip
- git
- curl
- wget
- unzip
- jq
- tmux
- vim
- nano
