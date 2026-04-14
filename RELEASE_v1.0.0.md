# APK 安全测试实验室平台 v1.0.0 发布说明

## 发布信息

- **版本号**: v1.0.0
- **发布日期**: 2026-04-14
- **发布类型**: 初始公开发行版

## 项目简介

APK 安全测试实验室是一个面向安全研究人员的 Android 应用安全测试综合平台，整合了：

- Docker 化工具环境
- 自动化扫描平台
- 交互式学习实验室
- Web 管理界面

## 核心功能

### 1. Docker 工具环境
- 预配置的 Kali Linux 容器
- Android 安全工具链（MobSF, Frida, JADX, APKTool 等）
- ADB 和模拟器支持

### 2. 自动化扫描平台
- 基于 MobSF v4.5.0 的静态/动态分析
- FastAPI + Celery 异步任务处理
- PostgreSQL 数据存储
- 自动漏洞检测和报告生成

### 3. 交互式学习实验室
- OWASP Mobile Top 10 教程
- 漏洞靶场环境
- 实践练习

### 4. Web 管理界面
- React + TypeScript 前端
- 扫描任务管理
- 漏洞报告展示
- 报告导出（JSON/HTML）

## 技术栈

| 组件 | 技术 |
|------|------|
| 前端 | React 18 + TypeScript + Vite + Tailwind CSS |
| 后端 API | Python 3.10 + FastAPI |
| 任务队列 | Celery + Redis |
| 数据库 | PostgreSQL 15 |
| 扫描引擎 | MobSF v4.5.0 |
| 容器化 | Docker + Docker Compose |

## 快速开始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 8GB 可用内存
- 至少 50GB 可用磁盘空间

### 安装步骤

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/mobilesec.git
cd mobilesec

# 启动所有服务
docker-compose up -d

# 访问 Web 界面
# 前端：http://localhost:3001
# 后端 API: http://localhost:3080
# MobSF: http://localhost:9000
```

## 已实现功能清单

### 第一阶段：基础框架与 Docker 环境 ✅
- [x] 项目初始化
- [x] Kali Linux 基础镜像（阿里云源）
- [x] 核心 Android 安全工具安装
- [x] MobSF 容器配置
- [x] Frida 环境容器
- [x] docker-compose.yml 编排

### 第二阶段：自动化扫描平台 ✅
- [x] FastAPI 项目设置
- [x] SQLAlchemy 数据模型
- [x] Celery 任务队列
- [x] MobSF API 集成
- [x] 扫描任务管理
- [x] 漏洞信息提取
- [x] 报告生成系统

### 第三阶段：交互式学习实验室 ✅
- [x] 教程系统框架
- [x] 漏洞靶场集合
- [x] 沙箱环境

### 第四阶段：Web 界面与集成 ✅
- [x] React 前端项目
- [x] 用户认证系统
- [x] 扫描任务 UI
- [x] 漏洞报告展示
- [x] 报告导出功能

## 已知问题

1. **MobSF 健康检查**: 某些版本的 MobSF API 健康检查端点可能返回 401，系统已跳过健康检查直接执行扫描
2. **包名解析**: 某些加固的 APK 可能无法正确解析包名（显示为 "Failed"）
3. **中文支持**: 前端界面主要为英文，文档为中文

## 后续计划 (v1.1.0)

- [ ] 批量扫描功能
- [ ] WebSocket 实时进度推送
- [ ] 自定义扫描规则
- [ ] 多用户支持
- [ ] 扫描报告对比
- [ ] CI/CD 集成

## 文件结构

```
mobilesec/
├── docker/                 # Docker 配置文件
│   ├── kali-base/         # Kali 工具容器
│   ├── mobsf/             # MobSF 配置
│   ├── frida/             # Frida 环境
│   └── docker-compose.yml
├── scanner/                # 扫描平台
│   ├── src/
│   │   ├── api/           # FastAPI 路由
│   │   ├── core/          # 配置
│   │   ├── models/        # 数据模型
│   │   ├── services/      # 业务逻辑
│   │   └── tasks/         # Celery 任务
│   └── .env               # 环境配置
├── web/                    # Web 界面
│   └── frontend/          # React 前端
├── lab/                    # 学习实验室
│   ├── tutorials/         # 教程
│   └── sandbox/           # 沙箱
├── docs/                   # 文档
├── README.md
└── GETTING_STARTED.md
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

- GitHub Issues: https://github.com/YOUR_USERNAME/mobilesec/issues
- 邮箱：your-email@example.com
