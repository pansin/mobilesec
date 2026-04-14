#!/usr/bin/env python3
"""
报告任务 - 用于处理报告相关任务
"""

from celery import shared_task
from loguru import logger

from src.services.report_service import ReportService
from src.services.scan_service import ScanService
from src.core import SessionLocal

@shared_task(bind=True)
def generate_report_task(self, task_id: str, format: str = "html"):
    """生成报告任务"""
    logger.info(f"Generating {format} report for task: {task_id}")

    db = SessionLocal()

    try:
        report_service = ReportService(db)
        scan_service = ScanService(db)
        scan_task = scan_service.get_scan_task(task_id)

        if not scan_task:
            logger.warning(f"Task not found: {task_id}")
            return {"task_id": task_id, "status": "task_not_found"}

        # 确保报告存在
        report = report_service.get_report(scan_task.id, format)

        if format == "html":
            content = report_service.generate_html_report(report)
        elif format == "pdf":
            content = report_service.generate_pdf_report(report)
        elif format == "json":
            content = report_service.generate_json_report(report)
        else:
            raise ValueError(f"Unsupported report format: {format}")

        # 保存到文件
        from src.utils.report_utils import ReportExporter
        output_dir = "reports"
        file_name = f"{task_id}_report.{format}"
        ReportExporter.save_to_file(content, output_dir, file_name, format)

        logger.info(f"{format} report generated successfully for task {task_id}")

        return {
            "task_id": task_id,
            "status": "completed",
            "format": format,
            "content_type": f"text/{format}"
        }

    except Exception as e:
        logger.error(f"Failed to generate report for task {task_id}: {e}")
        return {
            "task_id": task_id,
            "status": "failed",
            "format": format,
            "error": str(e)
        }

    finally:
        db.close()

@shared_task(bind=True)
def send_email_report_task(self, task_id: str, recipient_email: str, format: str = "html"):
    """发送邮件报告任务"""
    logger.info(f"Sending report to {recipient_email} for task {task_id}")

    db = SessionLocal()

    try:
        report_service = ReportService(db)
        scan_service = ScanService(db)
        scan_task = scan_service.get_scan_task(task_id)

        if not scan_task:
            logger.warning(f"Task not found: {task_id}")
            return {"task_id": task_id, "status": "task_not_found"}

        report = report_service.get_report(scan_task.id, format)
        if format == "html":
            content = report_service.generate_html_report(report)
        elif format == "pdf":
            content = report_service.generate_pdf_report(report)
        else:
            raise ValueError(f"Unsupported format: {format}")

        # 模拟发送邮件（实际项目中可以使用 email 库）
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        logger.warning("Email sending is currently disabled")
        logger.info(f"Report content length: {len(content)} bytes")

        return {
            "task_id": task_id,
            "status": "email_disabled"
        }

    except Exception as e:
        logger.error(f"Failed to send report to {recipient_email} for task {task_id}: {e}")
        return {
            "task_id": task_id,
            "status": "failed",
            "error": str(e)
        }

    finally:
        db.close()

@shared_task(bind=True)
def export_report_to_storage_task(self, task_id: str, format: str = "json"):
    """导出报告到存储"""
    logger.info(f"Exporting report for task {task_id} to storage")

    db = SessionLocal()

    try:
        report_service = ReportService(db)
        scan_service = ScanService(db)
        scan_task = scan_service.get_scan_task(task_id)

        report = report_service.get_report(scan_task.id, format)
        content = report_service.generate_html_report(report)

        # 模拟导出到存储
        logger.info(f"Report generated and ready for export: {len(content)} bytes")
        logger.warning("Storage export is currently disabled")

        return {
            "task_id": task_id,
            "status": "storage_disabled"
        }

    except Exception as e:
        logger.error(f"Failed to export report for task {task_id}: {e}")
        return {
            "task_id": task_id,
            "status": "failed",
            "error": str(e)
        }

    finally:
        db.close()
