# APK Security Scanner - 第二阶段自动化扫描平台

## 项目概述

第二阶段已经完成了核心的自动化扫描平台，包括：
- ✅ FastAPI 后端服务
- ✅ PostgreSQL 数据库模型
- ✅ Celery 任务队列
- ✅ MobSF API 集成
- ✅ 报告生成系统
- ✅ 文件上传和处理

## 项目结构

```
scanner/
├── src/
│   ├── api/              # API 路由
│   ├── core/             # 核心配置
│   │   ├── config.py    # 配置管理
│   │   ├── database.py   # 数据库连接
│   │   └── celery_app.py # Celery 配置
│   ├── models/           # 数据模型
│   │   └── __init__.py   # 数据库模型和枚举
│   ├── services/         # 业务逻辑
│   │   ├── mobsf_client.py # MobSF API 客户端
│   │   ├── scan_service.py   # 扫描服务
│   │   └── report_service.py # 报告服务
│   ├── tasks/            # Celery 任务
│   │   ├── scan_tasks.py   # 扫描任务
│   │   └── report_tasks.py # 报告任务
│   ├── utils/            # 工具函数
│   │   ├── file_utils.py     # 文件处理
│   │   └── report_utils.py   # 报告工具
│   └── main.py          # 应用入口
├── alembic/              # 数据库迁移
├── tests/                # 测试
├── requirements.txt      # Python 依赖
├── .env.example         # 环境变量示例
├── init_db.py          # 数据库初始化脚本
└── README.md
```

## 核心功能

### 1. API 端点

| 方法 | 端点 | 功能 |
|------|------|------|
| POST | `/api/v1/scans/upload` | 上传 APK 并创建扫描任务 |
| GET | `/api/v1/scans/{task_id}` | 获取扫描状态 |
| GET | `/api/v1/scans/{task_id}/report` | 获取扫描报告 |
| DELETE | `/api/v1/scans/{task_id}` | 删除扫描任务 |
| GET | `/api/v1/scans` | 列出扫描任务（分页） |
| GET | `/health` | 健康检查 |

### 2. 数据模型

- **ScanTask**: 扫描任务（状态、进度、应用信息等）
- **Vulnerability**: 漏洞信息（标题、描述、严重程度、修复建议）
- **ScanReport**: 扫描报告（统计、HTML/PDF/JSON 格式）
- **MobSFScan**: MobSF 扫描结果记录

### 3. 任务处理

- **scan_apk_task**: 完整的 APK 扫描流程（上传 → 扫描 → 解析 → 存储）
- **generate_reports_task**: 生成多种格式的报告
- **scan_status_check_task**: 检查扫描状态

### 4. 报告系统

- HTML 报告（带模板）
- PDF 报告（WeasyPrint）
- JSON 报告（结构化数据）
- 漏洞统计和聚合

## 快速开始

### 环境配置

```bash
cd scanner

# 复制配置
cp .env.example .env
# 编辑 .env 配置数据库和 API 密钥
```

### 初始化数据库

```bash
# 创建并初始化数据库
python3 init_db.py
```

### 启动服务

```bash
# 1. 启动 Celery Worker
celery -A src.core.celery_app worker --loglevel=info

# 2. 启动 FastAPI 应用
python3 src/main.py

# 或者使用 Uvicorn 直接启动
uvicorn src.main:app --reload --host 0.0.0.0 --port 8001
```

### 访问 API

- API 文档: http://localhost:8001/docs
- 健康检查: http://localhost:8001/health

## 使用示例

### 上传 APK 并扫描

```python
import requests
import time

# 上传文件
with open("app.apk", "rb") as f:
    response = requests.post(
        "http://localhost:8001/api/v1/scans/upload",
        files={"file": f}
    )

task_id = response.json()["task_id"]
print(f"Task created: {task_id}")

# 轮询状态
while True:
    status_response = requests.get(
        f"http://localhost:8001/api/v1/scans/{task_id}"
    )
    data = status_response.json()

    print(f"Status: {data['status']} ({data['progress']}%)")

    if data["status"] in ["completed", "failed"]:
        break

    time.sleep(5)

# 获取报告
report_response = requests.get(
    f"http://localhost:8001/api/v1/scans/{task_id}/report",
    params={"format": "json"}
)

report = report_response.json()
print(f"Found {report['total_vulnerabilities']} vulnerabilities")
```

### 使用命令行

```bash
# 上传 APK
curl -X POST -F "file=@app.apk" http://localhost:8001/api/v1/scans/upload

# 检查状态
curl http://localhost:8001/api/v1/scans/<task_id>

# 下载报告
curl -o report.json "http://localhost:8001/api/v1/scans/<task_id>/report?format=json"
```

## 集成 Docker

使用项目根目录的 `docker-compose.yml` 集成所有服务。

### 配置更新

在项目根目录的 `docker-compose.yml` 中添加 scanner 服务：

```yaml
scanner:
  build:
    context: ../scanner
    dockerfile: Dockerfile
  container_name: mobilesec-scanner
  hostname: scanner
  ports:
    - "8001:8001"
  environment:
    - DATABASE_URL=postgresql://mobilesec:mobilesec123@postgres:5432/mobilesec
    - REDIS_URL=redis://redis:6379/0
    - MOBSF_URL=http://mobsf:8000
    - MOBSF_API_KEY=a474e8e5c08c2a21125e8819b916fb30fb3904b6fd2cfb7ca3a0d50e1f8d5ba
  depends_on:
    - postgres
    - redis
    - mobsf
  volumes:
    - ../scanner/uploads:/app/uploads
    - ../scanner/reports:/app/reports
  restart: unless-stopped
```

## 下一步

1. **前端开发**: 集成 React/Vue 前端界面
2. **用户认证**: 添加用户系统和权限控制
3. **高级功能**: 批量扫描、定时任务、通知等
4. **测试**: 编写单元测试和集成测试

## 技术说明

- **异步处理**: 使用 Celery + Redis 进行异步任务处理
- **数据库**: 使用 SQLAlchemy ORM + PostgreSQL
- **API**: 使用 FastAPI 提供 RESTful 接口
- **报告**: Jinja2 模板 + WeasyPrint 生成 PDF
- **文件上传**: FastAPI 的 UploadFile 处理

## 参考资源

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Celery 文档](https://docs.celeryq.dev/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [MobSF API 文档](https://mobsf.github.io/docs/)
