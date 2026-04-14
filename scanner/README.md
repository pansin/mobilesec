# APK Security Scanner - Automation Platform

APK 安全测试自动化扫描平台，基于 FastAPI、Celery、PostgreSQL 构建。

## 技术栈

- **Web 框架**: FastAPI
- **任务队列**: Celery + Redis
- **数据库**: PostgreSQL + SQLAlchemy
- **ORM**: SQLAlchemy
- **扫描引擎**: MobSF API 集成

## 功能特性

- ✅ MobSF API 集成
- ✅ 异步任务处理
- ✅ 批量 APK 扫描
- ✅ 结构化漏洞报告
- ✅ 报告导出（HTML/PDF）
- ✅ 扫描历史管理

## 快速开始

### 环境要求

- Python 3.9+
- PostgreSQL 15+
- Redis 7+
- Docker (可选)

### 安装

```bash
# 克隆项目
cd scanner

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 配置数据库和 API 密钥

# 数据库迁移
alembic upgrade head

# 启动 Celery Worker
celery -A src.core.celery_app worker --loglevel=info

# 启动 FastAPI 应用
uvicorn src.main:app --reload --host 0.0.0.0 --port 8001
```

### 使用 Docker

```bash
# 使用项目根目录的 docker-compose
cd ../docker
docker-compose up -d scanner
```

## API 文档

启动后访问：http://localhost:8001/docs

## 项目结构

```
scanner/
├── src/
│   ├── api/              # FastAPI 路由
│   │   ├── __init__.py
│   │   ├── auth.py       # 认证相关
│   │   ├── scans.py      # 扫描任务
│   │   └── reports.py    # 报告相关
│   ├── core/             # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py     # 配置管理
│   │   ├── celery_app.py # Celery 配置
│   │   └── database.py   # 数据库连接
│   ├── models/           # 数据模型
│   │   ├── __init__.py
│   │   ├── scan.py       # 扫描任务模型
│   │   ├── report.py     # 报告模型
│   │   └── vulnerability.py # 漏洞模型
│   ├── services/         # 业务逻辑
│   │   ├── __init__.py
│   │   ├── mobsf_client.py  # MobSF API 客户端
│   │   ├── scan_service.py  # 扫描服务
│   │   └── report_service.py # 报告服务
│   ├── tasks/            # Celery 任务
│   │   ├── __init__.py
│   │   ├── scan_tasks.py # 扫描任务
│   │   └── report_tasks.py # 报告任务
│   ├── utils/            # 工具函数
│   │   ├── __init__.py
│   │   ├── file_utils.py
│   │   └── export_utils.py
│   └── main.py          # 应用入口
├── tests/                # 测试
├── alembic/              # 数据库迁移
├── requirements.txt      # Python 依赖
├── .env.example         # 环境变量示例
└── README.md
```
