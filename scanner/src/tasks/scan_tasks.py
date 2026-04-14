#!/usr/bin/env python3
"""
扫描任务 - 执行扫描和报告生成
"""

from celery import shared_task
from loguru import logger
import asyncio

from src.models import ScanTask, ScanStatus
from src.services import ScanService
from src.core import SessionLocal

@shared_task(bind=True)
def scan_apk_task(self, task_id: str):
    """扫描 APK 文件的 Celery 任务"""
    logger.info(f"Starting scan task for: {task_id}")

    db = SessionLocal()

    try:
        scan_service = ScanService(db)
        scan_task = scan_service.get_scan_task(task_id)

        if not scan_task or scan_task.status != ScanStatus.PENDING:
            logger.warning(f"Task {task_id} is not in pending state")
            return {"task_id": task_id, "status": "invalid"}

        # 使用异步函数
        success = asyncio.run(scan_service.run_scan(task_id))

        if success:
            logger.info(f"Scan task completed successfully: {task_id}")
            return {
                "task_id": task_id,
                "status": "completed",
                "total_vulnerabilities": len(scan_task.vulnerabilities)
            }
        else:
            logger.error(f"Scan task failed for: {task_id}")
            return {
                "task_id": task_id,
                "status": "failed"
            }

    except Exception as e:
        logger.error(f"Scan task failed with exception: {task_id}, {e}")
        try:
            scan_service = ScanService(db)
            scan_service.update_scan_status(
                task_id,
                ScanStatus.FAILED,
                0.0,
                str(e)
            )
        except Exception as update_error:
            logger.error(f"Error updating status for {task_id}: {update_error}")

        return {
            "task_id": task_id,
            "status": "failed",
            "error": str(e)
        }

    finally:
        db.close()

@shared_task(bind=True)
def generate_reports_task(self, task_id: str, formats: list):
    """生成多种格式的报告任务"""
    logger.info(f"Generating reports for task {task_id}, formats: {formats}")

    db = SessionLocal()

    try:
        scan_service = ScanService(db)
        scan_task = scan_service.get_scan_task(task_id)

        if not scan_task:
            return {"task_id": task_id, "status": "task_not_found"}

        from src.services.report_service import ReportService
        report_service = ReportService(db)

        results = []
        for format in formats:
            try:
                report_content = report_service.generate_report(scan_task.id, format)
                if report_content:
                    results.append({
                        "format": format,
                        "status": "success",
                        "size": len(report_content) if isinstance(report_content, bytes) else len(report_content.encode('utf-8'))
                    })
                else:
                    results.append({"format": format, "status": "failed"})
            except Exception as e:
                logger.error(f"Failed to generate {format} report: {e}")
                results.append({"format": format, "status": "failed"})

        return {"task_id": task_id, "status": "completed", "results": results}

    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        return {
            "task_id": task_id,
            "status": "failed",
            "error": str(e)
        }

    finally:
        db.close()

@shared_task(bind=True)
def scan_status_check_task(self, task_id: str):
    """扫描状态检查任务"""
    logger.debug(f"Checking scan status for task {task_id}")

    db = SessionLocal()

    try:
        scan_service = ScanService(db)
        scan_task = scan_service.get_scan_task(task_id)

        if not scan_task:
            return {"task_id": task_id, "status": "not_found"}

        return {
            "task_id": task_id,
            "status": scan_task.status,
            "progress": scan_task.progress,
            "filename": scan_task.filename
        }

    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return {
            "task_id": task_id,
            "status": "error",
            "error": str(e)
        }
    finally:
        db.close()
