# 海之安APK 安全测试实验室平台

> 面向安全研究人员的 Android 应用安全测试综合平台

## 项目概述

APK 安全测试实验室是一个整合了 Docker 化工具环境、自动化扫描平台和交互式学习实验室的 Android 应用安全测试解决方案。

### 核心特性

- **Docker 化工具环境**：预配置的 Kali Linux 容器，包含所有必要的 Android 安全测试工具
- **自动化扫描平台**：基于 MobSF 的静态/动态分析，自动检测漏洞并生成报告
- **交互式学习实验室**：漏洞靶场、教程系统和实践环境
- **Web 管理界面**：统一的操作界面，集成所有功能

## 快速开始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 8GB 可用内存
- 至少 50GB 可用磁盘空间

### 启动平台

```bash
# 克隆项目
git clone <repository-url>
cd mobilesec

# 启动所有服务
docker-compose up -d

# 访问 Web 界面
# 前端: http://localhost:3000
# MobSF: http://localhost:9000
```

## 项目结构

```
mobilesec/
├── docker/                  # Docker 相关文件
│   ├── kali-base/          # Kali Linux 基础镜像
│   ├── mobsf/              # MobSF 容器配置
│   ├── frida/              # Frida 环境配置
│   └── docker-compose.yml  # 服务编排
├── scanner/                 # 自动化扫描平台
│   ├── src/                # 扫描引擎源码
│   ├── api/                # REST API
│   └── tests/              # 测试代码
├── lab/                     # 学习实验室
│   ├── vulnapps/           # 漏洞靶场应用
│   ├── tutorials/          # 教程内容
│   └── sandbox/            # 沙箱环境
├── web/                     # Web 界面
│   ├── frontend/           # React 前端
│   └── backend/            # API 后端
└── docs/                    # 文档
```

## 工具清单

### 静态分析工具

- **MobSF** - 移动安全框架
- **JADX** - Dex 反编译器
- **APKTool** - APK 反编译工具
- **QARK** - Android 应用安全评估工具
- **Dependency-Check** - 依赖漏洞检测

### 动态分析工具

- **Frida** - 动态插桩框架
- **Objection** - Frida 工具集
- **Xposed** - 钩子框架
- **Stetho** - Chrome DevTools 集成

### 网络分析工具

- **Burp Suite** - Web 代理 (社区版)
- **Wireshark** - 网络协议分析器
- **mitmproxy** - 中间人代理
- **tcpdump** - 网络数据包捕获

### 其他工具

- **ADB** - Android 调试桥
- **scrcpy** - 屏幕镜像
- **Ghidra** - 逆向工程框架
- **Radare2** - 二进制分析工具

## 使用指南

### 1. 扫描 APK

通过 Web 界面上传 APK 文件，系统将自动执行静态和动态分析。

```bash
# 或使用 API
curl -X POST -F "file=@app.apk" http://localhost:9000/api/v1/scan
```

### 2. 使用交互式容器

```bash
# 进入 Kali 工具容器
docker-compose exec kali bash

# 使用 Frida
frida -U -f com.example.app -l script.js
```

### 3. 学习实验室

访问 http://localhost:3000/lab 开始学习路径，包含：

- OWASP Mobile Top 10 教程
- 漏洞利用实践
- 靶场挑战

## 开发路线图

- [x] **第一阶段**: 基础框架与 Docker 环境
- [x] **第二阶段**: 自动化扫描平台
- [x] **第三阶段**: 交互式学习实验室
- [x] **第四阶段**: Web 界面与集成

## 参考资源

- [Android Application Penetration Testing Complete Guide 2025](https://blog.intelligencex.org/android-application-penetration-testing-complete-guide-2025)
- [Using Docker for Penetration Testing](https://dev.to/hassan_aftab/using-docker-for-penetration-testing-a-practical-guide-44lj)
- [OWASP Mobile Security Testing Guide (MASTG)](https://mas.owasp.org/MASTG/)
- [OWASP Mobile Top 10](https://owasp.org/www-project-mobile-top-10/)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
