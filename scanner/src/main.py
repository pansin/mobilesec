#!/usr/bin/env python3
"""
APK 安全扫描平台 - 主应用入口
"""

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
from pathlib import Path
import shutil
import uuid
from datetime import datetime
import logging

from src.core import settings, get_db
from src.models import ScanTask, ScanStatus
from src.services.scan_service import ScanService
from src.utils import file_utils

# 配置应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置静态文件
if settings.debug:
    @app.get("/health")
    async def health_check():
        """健康检查"""
        return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

    @app.get("/config")
    async def get_config():
        """获取配置信息（仅调试用）"""
        return {
            "app_name": settings.app_name,
            "version": settings.app_version,
            "debug": settings.debug,
            "mobsf_url": settings.mobsf_url
        }

# 确保上传目录存在
os.makedirs(settings.upload_dir, exist_ok=True)

@app.post("/api/v1/scans/upload")
async def upload_apk(
    file: UploadFile = File(..., description="APK file to scan"),
    db: Session = Depends(get_db)
):
    """上传 APK 文件并创建扫描任务"""
    try:
        # 读取文件内容用于验证
        contents = await file.read()
        await file.seek(0)  # 重置文件指针

        # 验证文件类型 - 仅检查扩展名
        filename = file.filename.lower() if file.filename else ""
        if not filename.endswith('.apk'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Please upload an APK file."
            )

        # 验证文件大小
        file_size = len(contents)
        if file_size > settings.max_upload_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum limit of {settings.max_upload_size} bytes"
            )

        # 保存文件
        task_id = str(uuid.uuid4())
        safe_filename = file_utils.sanitize_filename(file.filename)
        file_path = Path(settings.upload_dir) / f"{task_id}_{safe_filename}"

        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        # 创建扫描任务
        service = ScanService(db)
        scan_task = service.create_scan_task(
            filename=safe_filename,
            file_path=str(file_path),
            file_size=file_size
        )

        # 启动异步扫描任务
        from src.tasks.scan_tasks import scan_apk_task
        scan_apk_task.delay(scan_task.task_id)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "File uploaded successfully",
                "task_id": scan_task.task_id,
                "filename": safe_filename,
                "status": scan_task.status
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )

@app.get("/api/v1/scans/{task_id}")
async def get_scan_status(
    task_id: str,
    db: Session = Depends(get_db)
):
    """获取扫描任务状态"""
    try:
        service = ScanService(db)
        scan_task = service.get_scan_task(task_id)
        if not scan_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scan task not found"
            )

        # 统计漏洞严重程度
        vuln_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for vuln in scan_task.vulnerabilities:
            if vuln.severity in vuln_counts:
                vuln_counts[vuln.severity] += 1

        return {
            "task_id": scan_task.task_id,
            "filename": scan_task.filename,
            "status": scan_task.status,
            "progress": scan_task.progress,
            "created_at": scan_task.created_at.isoformat(),
            "started_at": scan_task.started_at.isoformat() if scan_task.started_at else None,
            "completed_at": scan_task.completed_at.isoformat() if scan_task.completed_at else None,
            "app_name": scan_task.app_name,
            "package_name": scan_task.package_name,
            "version_name": scan_task.version_name,
            "total_vulnerabilities": len(scan_task.vulnerabilities),
            "critical_count": vuln_counts["critical"],
            "high_count": vuln_counts["high"],
            "medium_count": vuln_counts["medium"],
            "low_count": vuln_counts["low"],
            "info_count": vuln_counts["info"],
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching scan status: {str(e)}"
        )

@app.get("/api/v1/scans/{task_id}/vulnerabilities")
async def get_vulnerabilities(
    task_id: str,
    severity: str = None,
    db: Session = Depends(get_db)
):
    """获取漏洞列表"""
    try:
        service = ScanService(db)
        scan_task = service.get_scan_task(task_id)
        if not scan_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scan task not found"
            )

        vulns = scan_task.vulnerabilities
        if severity:
            vulns = [v for v in vulns if v.severity == severity]

        return [
            {
                "id": f"vuln-{vuln.id}",
                "title": vuln.title,
                "description": vuln.description,
                "severity": vuln.severity,
                "cwe_id": vuln.cwe_id,
                "cvss_score": vuln.cvss_score,
                "recommendation": vuln.recommendation,
                "location": vuln.location,
                "scan_task_id": task_id,
                "created_at": vuln.created_at.isoformat() if vuln.created_at else datetime.utcnow().isoformat(),
            }
            for vuln in vulns
        ]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching vulnerabilities: {str(e)}"
        )


@app.get("/api/v1/scans/{task_id}/report")
async def get_scan_report(
    task_id: str,
    format: str = "json",
    db: Session = Depends(get_db)
):
    """获取扫描报告"""
    try:
        service = ScanService(db)
        scan_task = service.get_scan_task(task_id)
        if not scan_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scan task not found"
            )

        if scan_task.status != ScanStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Scan task is not completed. Current status: {scan_task.status}"
            )

        # 返回 JSON 格式的报告数据
        if format == "json":
            vuln_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
            for vuln in scan_task.vulnerabilities:
                if vuln.severity in vuln_counts:
                    vuln_counts[vuln.severity] += 1

            return {
                "task_id": task_id,
                "filename": scan_task.filename,
                "app_name": scan_task.app_name,
                "package_name": scan_task.package_name,
                "version_name": scan_task.version_name,
                "scan_status": scan_task.status,
                "completed_at": scan_task.completed_at.isoformat() if scan_task.completed_at else None,
                "summary": {
                    "total_vulnerabilities": len(scan_task.vulnerabilities),
                    "critical_count": vuln_counts["critical"],
                    "high_count": vuln_counts["high"],
                    "medium_count": vuln_counts["medium"],
                    "low_count": vuln_counts["low"],
                    "info_count": vuln_counts["info"],
                },
                "vulnerabilities": [
                    {
                        "id": f"vuln-{vuln.id}",
                        "title": vuln.title,
                        "description": vuln.description,
                        "severity": vuln.severity,
                        "cwe_id": vuln.cwe_id,
                        "cvss_score": vuln.cvss_score,
                        "recommendation": vuln.recommendation,
                        "location": vuln.location,
                    }
                    for vuln in scan_task.vulnerabilities
                ],
            }
        else:
            # HTML/PDF 格式返回原始内容
            report = service.get_report(task_id, format)
            return report
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching report: {str(e)}"
        )

@app.delete("/api/v1/scans/{task_id}")
async def delete_scan_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """删除扫描任务"""
    try:
        service = ScanService(db)
        scan_task = service.get_scan_task(task_id)
        if not scan_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scan task not found"
            )

        # 删除任务和文件
        service.delete_scan_task(task_id)

        return {
            "message": "Scan task deleted successfully"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting scan task: {str(e)}"
        )

@app.get("/api/v1/scans")
async def list_scan_tasks(
    page: int = 1,
    per_page: int = 20,
    status: str = None,
    db: Session = Depends(get_db)
):
    """列出扫描任务"""
    try:
        service = ScanService(db)
        tasks, total = service.get_scan_tasks(
            page=page,
            per_page=per_page,
            status=status
        )

        return {
            "items": [
                {
                    "task_id": task.task_id,
                    "filename": task.filename,
                    "status": task.status,
                    "created_at": task.created_at.isoformat(),
                    "app_name": task.app_name,
                    "package_name": task.package_name,
                    "total_vulnerabilities": len(task.vulnerabilities)
                }
                for task in tasks
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        }
    except Exception as e:
        logging.error(f"Error listing tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list scan tasks: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn

    # 配置日志
    logging.basicConfig(
        level=logging.getLevelName(settings.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=3080,
        reload=settings.debug
    )
