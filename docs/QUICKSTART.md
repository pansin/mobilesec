# APK 安全测试实验室 - 快速上手指南

## 概述

由于网络环境原因，完整的 Kali Linux 镜像构建可能会遇到困难。这个指南提供了几种替代方案，让你快速开始使用 APK 安全测试实验室。

## 方案一：使用预构建的容器（推荐）

### 1. 启动 MobSF（已准备好）

MobSF 容器可以直接使用：

```bash
cd docker
docker-compose up -d mobsf
```

访问 http://localhost:9000 使用 MobSF。

### 2. 使用官方 Kali Docker 镜像

```bash
# 拉取官方 Kali 镜像
docker pull kalilinux/kali-rolling:latest

# 运行并交互式安装工具
docker run -it --name mobilesec-kali \
  --privileged \
  --network=host \
  -v /dev/bus/usb:/dev/bus/usb \
  -v $(pwd)/kali-base/workspace:/workspace \
  kalilinux/kali-rolling:latest /bin/bash

# 在容器内安装工具
apt-get update
apt-get install -y git curl wget unzip python3 python3-pip adb jadx apktool wireshark
pip3 install frida-tools objection qark androguard
```

### 3. 使用 MobSF + 独立工具的组合

```bash
# 启动 MobSF
docker-compose up -d mobsf

# 在主机上直接使用 Frida、ADB 等工具
# (需要先在主机上安装这些工具)
```

## 方案二：使用预构建的 Docker 镜像

我已将项目配置为使用 Ubuntu 基础镜像，它更稳定且下载更快：

```bash
cd docker
docker build -t mobilesec/kali-base:latest ./kali-base
```

这个镜像包含：
- 基础系统工具
- Python3 和 pip
- Frida tools、Objection、QARK、Androguard
- Git、curl、wget 等

你可以在此基础上继续安装其他需要的工具。

## 方案三：分步构建（解决网络问题）

### 1. 先构建 Ubuntu 基础环境

```bash
cd docker
docker build -t mobilesec/kali-base:latest ./kali-base
```

### 2. 运行容器并在其中安装 Kali 工具

```bash
docker run -it --name mobilesec-temp mobilesec/kali-base:latest /bin/bash

# 在容器内：
echo "deb http://http.kali.org/kali kali-rolling main contrib non-free non-free-firmware" >> /etc/apt/sources.list
apt-get update --fix-missing
apt-get install -y jadx apktool
# 安装其他需要的工具...

# 保存为新镜像（在另一个终端）
docker commit mobilesec-temp mobilesec/kali-full:latest
```

## 当前已配置好的服务

即使没有完整的 Kali 镜像，你仍然可以使用：

### MobSF - 移动安全框架
- **状态**: ✅ 已配置
- **访问**: http://localhost:9000
- **用途**: APK 静态/动态分析、漏洞扫描

### Frida 脚本
- **状态**: ✅ 已准备好
- **位置**: `docker/frida/scripts/`
- **脚本**:
  - `ssl-pinning-bypass.js` - SSL 证书绑定绕过
  - `root-detection-bypass.js` - Root 检测绕过
  - `class-tracer.js` - 方法调用追踪

## 推荐的工作流

### 1. 分析 APK
```bash
# 启动 MobSF
cd docker
docker-compose up -d mobsf

# 访问 http://localhost:9000 上传 APK
```

### 2. 动态分析
```bash
# 在主机上使用 Frida（需要先安装）
frida -U -f com.example.app -l docker/frida/scripts/ssl-pinning-bypass.js
```

### 3. 静态分析
```bash
# 在主机上使用 JADX（需要先安装）
jadx-gui app.apk
```

## 在主机上安装工具（可选）

如果遇到 Docker 网络问题，可以直接在主机上安装这些工具：

### macOS (使用 Homebrew)
```bash
brew install --cask android-platform-tools
brew install jadx apktool frida
pip3 install frida-tools objection qark androguard
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install -y adb jadx apktool python3 python3-pip
pip3 install frida-tools objection qark androguard
```

## 下一步

1. **立即开始**: 启动 MobSF 并上传一个 APK 进行分析
2. **等待构建**: 继续尝试构建完整的 Docker 镜像
3. **混合使用**: 结合 Docker 容器和主机工具进行测试

## 故障排除

### 网络问题
- 使用 `--fix-missing` 参数重试 apt-get
- 尝试不同的镜像源
- 考虑使用代理或 VPN

### Docker 构建缓慢
- 分步构建，每次安装少量包
- 使用预构建的基础镜像
- 考虑在网络状况更好时构建
