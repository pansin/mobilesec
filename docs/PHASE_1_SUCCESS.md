# ✅ APK 安全测试实验室平台 - 第一阶段完成！

## 🎉 项目已成功搭建！

所有核心服务现在都已正常运行！

### 📦 运行中的服务

| 服务 | 状态 | 说明 |
|------|------|------|
| **MobSF** | ✅ 运行中 | 访问: http://localhost:9000 |
| **Kali 基础环境** | ✅ 运行中 | 包含所有核心安全工具 |
| **Frida 环境** | ✅ 运行中 | 包含预写的 Hook 脚本 |
| **Redis** | ✅ 运行中 | 任务队列 (第二阶段准备) |
| **PostgreSQL** | ✅ 运行中 | 数据库 (第二阶段准备) |

### 🔐 MobSF 登录信息

- **地址**: http://localhost:9000
- **用户名**: `mobsf`
- **密码**: `mobsf`
- **API Key**: `a474e8e5c08c2a21125e8819b916fb30fb3904b6fd2cfb7ca3a0d50e1f8d5ba6`

## 🚀 快速开始

### 1. 访问 MobSF 进行 APK 扫描

打开浏览器访问：**http://localhost:9000**

登录后上传 APK 即可获得详细的安全分析报告！

### 2. 使用 Kali 工具容器

```bash
docker exec -it mobilesec-kali bash
```

在容器中可以使用：
- `frida`, `objection`, `qark`, `androguard` - Python 安全工具
- `git`, `curl`, `wget` - 基础工具

### 3. 使用 Frida 容器

```bash
docker exec -it mobilesec-frida bash
```

预加载的脚本在 `/workspace/scripts/`：
- `ssl-pinning-bypass.js` - SSL 证书绑定绕过
- `root-detection-bypass.js` - Root 检测绕过
- `class-tracer.js` - 方法调用追踪

## 📁 项目结构

```
mobilesec/
├── README.md                    # 项目主文档
├── GETTING_STARTED.md           # 简化入门指南
├── docker/
│   ├── docker-compose.yml       # 服务编排
│   ├── quickstart.sh            # 快速启动脚本
│   ├── kali-base/              # Kali 基础镜像 (阿里云源)
│   ├── mobsf/                  # MobSF 配置
│   └── frida/                  # Frida 环境 + 脚本
└── docs/
    ├── TOOLS_GUIDE.md          # 工具使用指南
    ├── OWASP_MOBILE_TOP10.md   # 学习资源
    └── QUICKSTART.md          # 快速上手指南
```

## 🎯 已完成的功能 (第一阶段)

✅ Docker 化工具环境 (阿里云 Kali 源)  
✅ MobSF 移动安全框架 (端口 9000)  
✅ Frida 动态插桩工具 + 实用脚本  
✅ 完整的文档体系  
✅ Redis + PostgreSQL 为下一阶段准备  

## 📚 下一步计划

### 第二阶段：自动化扫描平台
- 集成 MobSF API
- 构建任务队列系统
- 实现批量扫描功能
- 自动报告生成

### 第三阶段：交互式学习实验室
- 漏洞靶场应用
- 教程系统
- 沙箱环境

### 第四阶段：Web 界面与集成
- 统一用户界面
- 任务调度与编排
- 报告查看与导出

## 🛠️ 常用命令

```bash
# 查看所有容器状态
docker-compose ps

# 查看服务日志
docker-compose logs -f

# 停止所有服务
docker-compose stop

# 启动所有服务
docker-compose start

# 重启服务
docker-compose restart

# 进入特定容器
docker exec -it mobilesec-kali bash
docker exec -it mobilesec-frida bash
```

## 📖 文档索引

- [项目主文档](../README.md)
- [工具使用指南](./TOOLS_GUIDE.md)
- [OWASP 学习资源](./OWASP_MOBILE_TOP10.md)
- [快速上手指南](./QUICKSTART.md)

---

**恭喜！你的 APK 安全测试实验室已经准备好了！** 🎊

现在你可以：
1. 访问 http://localhost:9000 开始分析 APK
2. 使用 Docker 容器进行安全测试
3. 阅读文档学习更多功能

祝你测试愉快！
