# APK Security Lab - 第三阶段：交互式学习实验室

## 项目概述

第三阶段（Interactive Learning Laboratory）已经完成！这个阶段提供了一个完整的交互式学习环境，包含漏洞靶场应用、教程系统、学习路径和沙箱环境。

## 📦 完成的功能模块

### 1. 漏洞靶场应用 (vulnapps/)
- ✅ **README.md - 漏洞应用列表和使用指南
- ✅ **vulnapp_manager.py - 漏洞应用下载管理器
- ✅ 支持 InsecureBankv2、DIVA、Sieve 等靶场应用

### 2. 教程系统 (tutorials/)
- ✅ **README.md - OWASP Mobile Top 10 教程概览
- ✅ **M2-Insecure-Data-Storage.md - 不安全数据存储教程
- ✅ **M4-Insecure-Authentication.md - 不安全认证教程
- ✅ **LEARNING_PATHS.md - 学习路径设计

### 3. 沙箱环境 (sandbox/)
- ✅ **README.md - 沙箱环境使用指南
- ✅ **docker-compose.yml - 沙箱 Docker 编排配置
- ✅ **Dockerfile.sandbox - 沙箱容器镜像
- ✅ 脚本文件：
  - create_avds.sh - 创建 AVD
  - healthcheck.sh - 健康检查
  - start_emulators.sh - 启动模拟器
  - entrypoint.sh - 入口脚本

## 📁 新增文件结构

```
lab/
├── vulnapps/
│   ├── README.md          # 漏洞应用文档
│   └── vulnapp_manager.py  # 应用管理工具
├── tutorials/
│   ├── README.md          # 教程系统文档
│   ├── M2-Insecure-Data-Storage.md
│   ├── M4-Insecure-Authentication.md
│   └── LEARNING_PATHS.md
├── sandbox/
│   └── README.md          # 沙箱环境文档
└── docker/
    ├── docker-compose.yml
    ├── Dockerfile.sandbox
    ├── entrypoint.sh
    └── scripts/
        ├── create_avds.sh
        ├── healthcheck.sh
        └── start_emulators.sh
```

## 🚀 使用方式

### 快速启动沙箱环境

```bash
cd lab/docker

# 构建并启动沙箱
docker-compose up -d

# 进入沙箱
docker-compose exec sandbox bash

# 查看帮助
/opt/scripts/healthcheck.sh
```

### 使用漏洞应用管理工具

```bash
cd lab/vulnapps

# 列出可用应用
python vulnapp_manager.py list

# 下载所有应用
python vulnapp_manager.py download

# 安装应用到设备
python vulnapp_manager.py install insecurebankv2
```

### 使用教程系统

1. 查看 `lab/tutorials/README.md` 了解教程结构
2. 按照学习路径逐步学习
3. 使用沙箱环境进行实践练习

## 🎯 核心特性

### 1. 漏洞靶场应用
- 精选的漏洞 Android 应用
- 包含 OWASP Mobile Top 10 漏洞场景
- 应用下载和管理工具
- 详细的漏洞说明和使用指南

### 2. 教程系统
- 完整的 OWASP Mobile Top 10 教程
- 理论讲解 + 实践练习
- 循序渐进的学习路径
- 从基础到高级的进阶

### 3. 沙箱环境
- 隔离的测试环境
- 预配置的 Android 模拟器
- 网络隔离和监控工具
- 快速快照回滚机制

### 4. 学习路径设计
- 三个级别：初级（0-3月）、中级（3-6月）、高级（6-12月）
- 结构化的技能培养路径
- 评估和认证机制
- 循序渐进的学习体验

## 📊 学习路径概览

### 初级路径（0-3个月）
- Android 安全基础
- 静态分析工具
- 动态分析基础
- DIVA 应用实践

### 中级路径（3-6个月）
- 网络分析
- Frida 动态插桩
- InsecureBankv2 实践
- 高级 Frida 脚本

### 高级路径（6-12个月）
- 逆向工程
- 移动取证
- 漏洞利用开发
- 真实应用研究

## 💡 使用建议

1. **先阅读教程**：从 OWASP Mobile Top 10 开始学习
2. **使用沙箱环境**：在隔离环境中进行安全测试
3. **实践靶场应用**：通过练习巩固知识
4. **按照学习路径**：循序渐进提升技能

## 📝 下一步计划

### 第四阶段：Web 界面与集成
- 📋 React/Vue 前端开发
- 📋 用户系统
- 📋 完整 UI 集成
- 📋 实时通知

---

**恭喜！第三阶段已成功完成！** 🎊

你现在拥有了：
- ✅ 完整的 Docker 工具环境
- ✅ MobSF 安全扫描框架
- ✅ FastAPI 后端 API
- ✅ 交互式学习实验室
- ✅ 漏洞靶场应用
- ✅ 教程系统
- ✅ 沙箱环境

可以开始学习和实践 Android 安全测试了！