# APK 安全测试实验室 - 最小化可用版本

## 立即启动（无需构建完整镜像）

### 1. 先启动 MobSF（立即可用）

```bash
cd docker

# 只启动 MobSF，这不需要复杂的构建
docker-compose up -d mobsf
```

访问：**http://localhost:9000**

### 2. 使用独立的工具容器

我已准备了三个简化的容器配置，你可以选择使用：

#### 选项 A：使用官方 MobSF + 主机工具
```bash
# 只需要 MobSF 容器
docker-compose up -d mobsf

# 其他工具（Frida、ADB、JADX）直接在主机上安装使用
```

#### 选项 B：分步添加工具
```bash
# 1. 使用 Ubuntu 基础镜像（已准备好）
docker build -t mobilesec/base:latest ./kali-base

# 2. 运行容器
docker run -it --name mobilesec-work \
  --privileged \
  --network=host \
  -v $(pwd)/kali-base/workspace:/workspace \
  mobilesec/base:latest /bin/bash

# 3. 在容器内按需安装工具
apt-get update
apt-get install -y jadx  # 先安装最需要的
# 然后再安装其他...
```

## 当前项目结构

```
mobilesec/
├── README.md                    # 项目说明
├── docker/
│   ├── docker-compose.yml       # 服务编排（MobSF 端口 9000）
│   ├── mobsf/                   # MobSF 配置
│   ├── frida/                   # Frida 脚本
│   │   └── scripts/
│   │       ├── ssl-pinning-bypass.js
│   │       ├── root-detection-bypass.js
│   │       └── class-tracer.js
│   ├── kali-base/              # 基础镜像（Ubuntu）
│   └── quickstart.sh           # 启动脚本
└── docs/
    ├── TOOLS_GUIDE.md          # 工具使用指南
    ├── OWASP_MOBILE_TOP10.md   # OWASP 学习资源
    └── QUICKSTART.md           # 快速上手指南
```

## 推荐的工作方式

### 方式 1：MobSF + 主机工具（最简单）

1. 启动 MobSF：
```bash
cd docker
docker-compose up -d mobsf
```

2. 在主机上安装其他工具：
```bash
# macOS
brew install --cask android-platform-tools
brew install jadx apktool frida
pip3 install frida-tools objection

# Linux
sudo apt-get install adb jadx apktool python3-pip
pip3 install frida-tools objection
```

3. 使用 Frida 脚本：
```bash
frida -U -f com.example.app -l docker/frida/scripts/ssl-pinning-bypass.js
```

### 方式 2：使用官方 Kali 镜像

```bash
# 拉取官方 Kali
docker pull kalilinux/kali-rolling:latest

# 运行
docker run -it --name kali-lab \
  --privileged \
  --network=host \
  -v /dev/bus/usb:/dev/bus/usb \
  kalilinux/kali-rolling:latest /bin/bash

# 在容器内安装工具
apt-get update
apt-get install -y jadx apktool adb python3-pip
pip3 install frida-tools objection
```

## 下一步

1. **立即开始**：先启动 MobSF 体验 APK 扫描
2. **根据需要**：选择上面的一种方式安装其他工具
3. **后续完善**：网络好时再构建完整镜像

## 已包含的工具脚本

即使没有完整镜像，你也可以使用：
- ✅ MobSF（通过 Docker）
- ✅ Frida 脚本（在 `docker/frida/scripts/`）
- ✅ 详细的使用文档

有任何问题随时问我！
