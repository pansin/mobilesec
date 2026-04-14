#!/usr/bin/env python3
"""
报告服务层 - 生成和管理报告
"""

import os
import jinja2
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session
from loguru import logger
from datetime import datetime
from PIL import Image
import io

from src.core import settings
from src.models import ScanTask, ScanReport, ReportFormat
from src.services import scan_service

class ReportService:
    """报告服务类"""

    def __init__(self, db: Session):
        self.db = db
        self.template_loader = jinja2.FileSystemLoader(self._get_template_dir())
        self.template_env = jinja2.Environment(
            loader=self.template_loader,
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def _get_template_dir(self):
        """获取报告模板目录"""
        template_dir = Path(__file__).parent.parent / "templates"
        if not template_dir.exists():
            template_dir.mkdir(exist_ok=True)
            # 复制默认模板
            self._copy_default_templates(template_dir)

        return str(template_dir)

    def _copy_default_templates(self, target_dir: Path):
        """复制默认报告模板"""
        default_html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ report.title }}</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { background: #3498db; color: white; padding: 20px; text-align: center; }
        h1 { margin: 0; font-size: 24px; }
        .section { margin: 20px 0; padding: 20px; border: 1px solid #eee; }
        .vulnerability { margin: 15px 0; padding: 15px; background: #f9f9f9; border-left: 4px solid {{ severity_color(vuln.severity) }}; }
        .vuln-title { font-weight: bold; color: #2c3e50; }
        .vuln-severity { padding: 3px 8px; border-radius: 4px; color: white; font-size: 0.9em; }
        .vuln-critical { background: #e74c3c; }
        .vuln-high { background: #e67e22; }
        .vuln-medium { background: #f39c12; }
        .vuln-low { background: #3498db; }
        .vuln-info { background: #95a5a6; }
        .stats { display: flex; justify-content: space-around; flex-wrap: wrap; }
        .stat-box { text-align: center; padding: 10px; min-width: 150px; }
        .stat-number { font-size: 24px; font-weight: bold; }
        footer { text-align: center; margin: 30px 0; color: #7f8c8d; font-size: 0.9em; }
    </style>
</head>
<body>
    <header>
        <h1>{{ report.title }}</h1>
        <p>{{ task.filename }}</p>
        <p>{{ task.created_at.strftime('%Y-%m-%d %H:%M:%S') }}</p>
    </header>

    <div class="container">
        <section class="section">
            <h2>报告摘要</h2>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{{ report.total_vulnerabilities }}</div>
                    <div>总漏洞数</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{{ report.critical_count }}</div>
                    <div class="vuln-severity vuln-critical">严重</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{{ report.high_count }}</div>
                    <div class="vuln-severity vuln-high">高</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{{ report.medium_count }}</div>
                    <div class="vuln-severity vuln-medium">中</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{{ report.low_count }}</div>
                    <div class="vuln-severity vuln-low">低</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{{ report.info_count }}</div>
                    <div class="vuln-severity vuln-info">信息</div>
                </div>
            </div>
        </section>

        {% if task.app_name %}
        <section class="section">
            <h2>应用信息</h2>
            <p><strong>应用名称:</strong> {{ task.app_name }}</p>
            <p><strong>包名:</strong> {{ task.package_name }}</p>
            <p><strong>版本:</strong> {{ task.version_name }}</p>
            {% if task.version_code %}
            <p><strong>版本代码:</strong> {{ task.version_code }}</p>
            {% endif %}
            {% if task.min_sdk %}
            <p><strong>最低 SDK:</strong> {{ task.min_sdk }}</p>
            {% endif %}
            {% if task.target_sdk %}
            <p><strong>目标 SDK:</strong> {{ task.target_sdk }}</p>
            {% endif %}
        </section>
        {% endif %}

        {% if task.vulnerabilities %}
        <section class="section">
            <h2>检测到的漏洞</h2>
            {% for vuln in task.vulnerabilities %}
            <div class="vulnerability">
                <div class="vuln-title">{{ loop.index }}. {{ vuln.title }}</div>
                <span class="vuln-severity vuln-{{ vuln.severity }}">{{ severity_text(vuln.severity) }}</span>
                {% if vuln.cwe_id %}
                <span style="margin-left: 10px;">CWE {{ vuln.cwe_id }}</span>
                {% endif %}
                {% if vuln.cvss_score %}
                <span style="margin-left: 10px;">CVSS: {{ vuln.cvss_score }}</span>
                {% endif %}
                {% if vuln.description %}
                <p>{{ vuln.description }}</p>
                {% endif %}
                {% if vuln.recommendation %}
                <p><strong>修复建议:</strong> {{ vuln.recommendation }}</p>
                {% endif %}
            </div>
            {% endfor %}
        </section>
        {% else %}
        <section class="section">
            <h2>检测到的漏洞</h2>
            <p style="color: #7f8c8d;">未发现严重安全漏洞</p>
        </section>
        {% endif %}

        <section class="section">
            <h2>扫描详情</h2>
            <p><strong>任务 ID:</strong> {{ task.task_id }}</p>
            <p><strong>文件名:</strong> {{ task.filename }}</p>
            <p><strong>文件大小:</strong> {{ (task.file_size / 1024 / 1024)|round(2) }} MB</p>
            <p><strong>扫描状态:</strong> {{ task.status }}</p>
            <p><strong>创建时间:</strong> {{ task.created_at.strftime('%Y-%m-%d %H:%M:%S') }}</p>
            {% if task.started_at %}
            <p><strong>开始时间:</strong> {{ task.started_at.strftime('%Y-%m-%d %H:%M:%S') }}</p>
            {% endif %}
            {% if task.completed_at %}
            <p><strong>完成时间:</strong> {{ task.completed_at.strftime('%Y-%m-%d %H:%M:%S') }}</p>
            {% endif %}
        </section>
    </div>

    <footer>
        <p>Generated by APK Security Scanner</p>
        <p>Report generated on {{ now.strftime('%Y-%m-%d %H:%M:%S') }}</p>
    </footer>
</body>
</html>
""".strip()

        with open(target_dir / "report_template.html.jinja", "w") as f:
            f.write(default_html_template)

    def severity_color(self, severity: str) -> str:
        """获取严重程度对应的颜色"""
        colors = {
            "critical": "#e74c3c",
            "high": "#e67e22",
            "medium": "#f39c12",
            "low": "#3498db",
            "info": "#95a5a6"
        }
        return colors.get(severity.lower(), "#95a5a6")

    def severity_text(self, severity: str) -> str:
        """获取严重程度对应的文本"""
        severity_map = {
            "critical": "严重",
            "high": "高",
            "medium": "中",
            "low": "低",
            "info": "信息"
        }
        return severity_map.get(severity.lower(), "未知")

    def generate_html_report(self, report: ScanReport) -> str:
        """生成 HTML 报告"""
        scan_task = report.scan_task

        template = self.template_env.get_template("report_template.html.jinja")

        context = {
            "task": scan_task,
            "report": report,
            "now": datetime.now(),
            "severity_color": self.severity_color,
            "severity_text": self.severity_text
        }

        return template.render(context)

    def generate_json_report(self, report: ScanReport) -> dict:
        """生成 JSON 报告"""
        scan_task = report.scan_task

        return {
            "meta": {
                "report_id": report.id,
                "format": report.format,
                "title": report.title,
                "generated_at": report.created_at.isoformat(),
                "version": "1.0"
            },
            "task_info": {
                "task_id": scan_task.task_id,
                "filename": scan_task.filename,
                "file_size": scan_task.file_size,
                "status": scan_task.status,
                "created_at": scan_task.created_at.isoformat(),
                "started_at": scan_task.started_at.isoformat() if scan_task.started_at else None,
                "completed_at": scan_task.completed_at.isoformat() if scan_task.completed_at else None
            },
            "application_info": {
                "app_name": scan_task.app_name,
                "package_name": scan_task.package_name,
                "version_name": scan_task.version_name,
                "version_code": scan_task.version_code,
                "min_sdk": scan_task.min_sdk,
                "target_sdk": scan_task.target_sdk
            },
            "vulnerability_summary": {
                "total": report.total_vulnerabilities,
                "critical": report.critical_count,
                "high": report.high_count,
                "medium": report.medium_count,
                "low": report.low_count,
                "info": report.info_count
            },
            "vulnerabilities": [
                {
                    "id": vuln.id,
                    "title": vuln.title,
                    "description": vuln.description,
                    "severity": vuln.severity,
                    "cwe_id": vuln.cwe_id,
                    "cvss_score": vuln.cvss_score,
                    "location": vuln.location,
                    "line_number": vuln.line_number,
                    "recommendation": vuln.recommendation,
                    "references": vuln.references
                }
                for vuln in scan_task.vulnerabilities
            ]
        }

    def generate_pdf_report(self, report: ScanReport) -> bytes:
        """生成 PDF 报告"""
        try:
            from weasyprint import HTML

            html_content = self.generate_html_report(report)
            return HTML(string=html_content).write_pdf()

        except ImportError:
            logger.error("WeasyPrint not installed, cannot generate PDF report")
            return b""

    def generate_report(self, task_id: str, format: str = ReportFormat.HTML) -> str:
        """生成报告（根据格式）"""
        report = self.get_report(task_id, format)

        if not report:
            logger.warning(f"Report not found for task: {task_id}")
            return None

        try:
            if format == ReportFormat.HTML:
                content = self.generate_html_report(report)
            elif format == ReportFormat.PDF:
                content = self.generate_pdf_report(report)
            elif format == ReportFormat.JSON:
                content = self.generate_json_report(report)
            else:
                raise ValueError(f"Unsupported format: {format}")

            return content

        except Exception as e:
            logger.error(f"Report generation failed for task {task_id}: {e}")
            return None
