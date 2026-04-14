#!/usr/bin/env python3
"""
扫描服务层 - 处理与扫描相关的核心业务逻辑
"""

import os
import hashlib
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple, Dict
from sqlalchemy.orm import Session
from loguru import logger

from src.models import (
    ScanTask,
    ScanStatus,
    Vulnerability,
    Severity,
    ScanReport,
    ReportFormat,
    MobSFScan
)
from src.core import settings
from src.services import mobsf_client
from src.utils import file_utils

class ScanService:
    """扫描服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.mobsf = mobsf_client.MobSFAPI()

    def create_scan_task(self, filename: str, file_path: str, file_size: int) -> ScanTask:
        """创建扫描任务"""
        task_id = str(uuid.uuid4())

        # 计算文件哈希
        file_hash = file_utils.calculate_sha256(file_path)

        # 检查是否已扫描过
        existing_task = self.db.query(ScanTask).filter(
            ScanTask.file_hash == file_hash
        ).first()

        if existing_task:
            logger.info(f"File {filename} already scanned, returning existing task")
            return existing_task

        scan_task = ScanTask(
            task_id=task_id,
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            file_hash=file_hash,
            status=ScanStatus.PENDING,
            created_at=datetime.now(timezone.utc)
        )

        self.db.add(scan_task)
        self.db.commit()
        self.db.refresh(scan_task)

        logger.info(f"Created scan task: {task_id} for {filename}")

        return scan_task

    def get_scan_task(self, task_id: str) -> Optional[ScanTask]:
        """获取扫描任务"""
        return self.db.query(ScanTask).filter(
            ScanTask.task_id == task_id
        ).first()

    def get_scan_tasks(
        self,
        page: int = 1,
        per_page: int = 20,
        status: str = None
    ) -> Tuple[List[ScanTask], int]:
        """获取任务列表"""
        query = self.db.query(ScanTask)

        if status:
            query = query.filter(ScanTask.status == status)

        # 排序
        query = query.order_by(ScanTask.created_at.desc())

        # 分页
        total = query.count()
        offset = (page - 1) * per_page
        tasks = query.offset(offset).limit(per_page).all()

        return tasks, total

    def update_scan_status(
        self,
        task_id: str,
        status: str,
        progress: float = None,
        error_message: str = None
    ):
        """更新扫描状态"""
        scan_task = self.get_scan_task(task_id)
        if not scan_task:
            logger.warning(f"Task not found: {task_id}")
            return

        scan_task.status = status

        if progress is not None:
            scan_task.progress = progress

        if error_message:
            scan_task.error_message = error_message

        if status == ScanStatus.RUNNING and not scan_task.started_at:
            scan_task.started_at = datetime.now(timezone.utc)

        if status in [ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.CANCELLED]:
            if not scan_task.completed_at:
                scan_task.completed_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(scan_task)

        logger.info(f"Task {task_id} status updated to: {status}")

    def update_application_info(self, task_id: str, app_info: Dict):
        """更新应用信息"""
        scan_task = self.get_scan_task(task_id)
        if not scan_task:
            return

        scan_task.app_name = app_info.get("app_name")
        scan_task.package_name = app_info.get("package_name")
        scan_task.version_name = app_info.get("version_name")
        scan_task.version_code = app_info.get("version_code")
        scan_task.min_sdk = app_info.get("min_sdk")
        scan_task.target_sdk = app_info.get("target_sdk")

        self.db.commit()
        self.db.refresh(scan_task)

    def save_vulnerabilities(self, task_id: str, vulnerabilities: List[Dict]):
        """保存漏洞信息"""
        scan_task = self.get_scan_task(task_id)
        if not scan_task:
            return

        for vuln_data in vulnerabilities:
            vuln = Vulnerability(
                scan_task_id=scan_task.id,
                title=vuln_data.get("title"),
                description=vuln_data.get("description"),
                severity=vuln_data.get("severity", Severity.INFO),
                cwe_id=vuln_data.get("cwe_id"),
                cvss_score=vuln_data.get("cvss_score"),
                location=vuln_data.get("location"),
                line_number=vuln_data.get("line_number"),
                recommendation=vuln_data.get("recommendation"),
                references=vuln_data.get("references", []),
                raw_data=vuln_data.get("raw_data")
            )
            self.db.add(vuln)

        self.db.commit()

        logger.info(f"Saved {len(vulnerabilities)} vulnerabilities for task {task_id}")

    def save_mobsf_scan_result(self, task_id: str, scan_result: Dict):
        """保存 MobSF 扫描结果"""
        scan_task = self.get_scan_task(task_id)
        if not scan_task:
            return

        # 检查是否已有记录
        existing = self.db.query(MobSFScan).filter(
            MobSFScan.scan_task_id == scan_task.id
        ).first()

        if existing:
            existing.static_analysis_result = scan_result.get("static_analysis_result")
            existing.dynamic_analysis_result = scan_result.get("dynamic_analysis_result")
            existing.manifest_analysis = scan_result.get("manifest_analysis")
            existing.permission_analysis = scan_result.get("permission_analysis")
            existing.code_analysis = scan_result.get("code_analysis")
            existing.api_response = scan_result.get("api_response")
        else:
            mobsf_scan = MobSFScan(
                scan_task_id=scan_task.id,
                mobsf_scan_hash=scan_result.get("scan_hash"),
                static_analysis_result=scan_result.get("static_analysis_result"),
                dynamic_analysis_result=scan_result.get("dynamic_analysis_result"),
                manifest_analysis=scan_result.get("manifest_analysis"),
                permission_analysis=scan_result.get("permission_analysis"),
                code_analysis=scan_result.get("code_analysis"),
                api_response=scan_result.get("api_response")
            )
            self.db.add(mobsf_scan)

        self.db.commit()

    def create_report(self, task_id: str, format: str = ReportFormat.HTML):
        """创建扫描报告"""
        scan_task = self.get_scan_task(task_id)
        if not scan_task:
            return None

        # 统计漏洞数量
        vuln_counts = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 0,
            Severity.MEDIUM: 0,
            Severity.LOW: 0,
            Severity.INFO: 0
        }

        for vuln in scan_task.vulnerabilities:
            if vuln.severity in vuln_counts:
                vuln_counts[vuln.severity] += 1

        report = ScanReport(
            scan_task_id=scan_task.id,
            format=format,
            title=f"{scan_task.filename} - Security Scan Report",
            summary=f"{len(scan_task.vulnerabilities)} vulnerabilities detected",
            total_vulnerabilities=len(scan_task.vulnerabilities),
            critical_count=vuln_counts[Severity.CRITICAL],
            high_count=vuln_counts[Severity.HIGH],
            medium_count=vuln_counts[Severity.MEDIUM],
            low_count=vuln_counts[Severity.LOW],
            info_count=vuln_counts[Severity.INFO],
        )

        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)

        logger.info(f"Report created: {report.id} for task {task_id}")

        return report

    def get_report(self, task_id: str, format: str = ReportFormat.HTML) -> Optional[ScanReport]:
        """获取报告"""
        scan_task = self.get_scan_task(task_id)
        if not scan_task:
            return None

        report = self.db.query(ScanReport).filter(
            ScanReport.scan_task_id == scan_task.id,
            ScanReport.format == format
        ).first()

        if not report:
            report = self.create_report(task_id, format)

        return report

    def delete_scan_task(self, task_id: str):
        """删除扫描任务"""
        scan_task = self.get_scan_task(task_id)
        if not scan_task:
            return False

        try:
            # 删除文件
            if os.path.exists(scan_task.file_path):
                os.remove(scan_task.file_path)
                logger.info(f"File deleted: {scan_task.file_path}")

            self.db.delete(scan_task)
            self.db.commit()

            logger.info(f"Scan task deleted successfully: {task_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting task {task_id}: {e}")
            self.db.rollback()
            return False

    async def run_scan(self, task_id: str) -> bool:
        """执行扫描（异步方法）"""
        scan_task = self.get_scan_task(task_id)
        if not scan_task or scan_task.status != ScanStatus.PENDING:
            logger.warning(f"Task is not in pending state: {task_id}")
            return False

        try:
            self.update_scan_status(task_id, ScanStatus.RUNNING, 0.1)

            # 执行完整扫描
            full_result = await self.mobsf.full_scan(scan_task.file_path)
            scan_hash = full_result.get("scan_hash")
            scan_result = full_result.get("scan_result", {})

            self.update_scan_status(task_id, ScanStatus.RUNNING, 0.5)

            # 解析结果
            app_info = await self.mobsf.extract_application_info(scan_result)
            vulnerabilities = await self.mobsf.extract_vulnerabilities(scan_result)
            manifest_info = await self.mobsf.extract_manifest_info(scan_result)
            permissions = await self.mobsf.extract_permissions(scan_result)

            # 保存结果
            self.update_application_info(task_id, app_info)
            self.save_vulnerabilities(task_id, vulnerabilities)
            self.save_mobsf_scan_result(task_id, {
                "scan_hash": scan_hash,
                "static_analysis_result": scan_result.get("static"),
                "dynamic_analysis_result": scan_result.get("dynamic"),
                "manifest_analysis": manifest_info,
                "permission_analysis": permissions,
                "api_response": full_result
            })

            # 生成报告
            self.create_report(task_id)

            # 更新状态
            self.update_scan_status(task_id, ScanStatus.COMPLETED, 1.0)
            logger.info(f"Scan completed successfully: {task_id}")

            return True

        except MobSFAPIError as e:
            logger.error(f"MobSF API error: {e}")
            self.update_scan_status(
                task_id,
                ScanStatus.FAILED,
                0.0,
                f"MobSF API Error: {e.message}"
            )
            return False
        except Exception as e:
            logger.error(f"Scan failed: {e}", exc_info=True)
            self.update_scan_status(
                task_id,
                ScanStatus.FAILED,
                0.0,
                str(e)
            )
            return False
