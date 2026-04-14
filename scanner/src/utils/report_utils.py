#!/usr/bin/env python3
"""
报告工具模块 - 提供报告相关的工具函数
"""

import json
from io import BytesIO
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional

class ReportExporter:
    """报告导出工具类"""

    @staticmethod
    def save_to_file(content: str or bytes, file_path: str, format: str = "text"):
        """保存报告到文件"""
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)

            if isinstance(content, str) and format in ["text", "html"]:
                mode = "w"
                encoding = "utf-8"
            else:
                mode = "wb"
                encoding = None

            with open(file_path, mode, encoding=encoding) as f:
                f.write(content)

            return True

        except Exception as e:
            import logging
            logging.error(f"Failed to save report to {file_path}: {e}")
            return False

    @staticmethod
    def save_html_report(content: str, task_id: str, output_dir: str = "./reports") -> str:
        """保存 HTML 报告到文件"""
        file_name = f"{task_id}_report.html"
        file_path = str(Path(output_dir) / file_name)
        return ReportExporter.save_to_file(content, file_path, "html")

    @staticmethod
    def save_pdf_report(content: bytes, task_id: str, output_dir: str = "./reports") -> str:
        """保存 PDF 报告到文件"""
        file_name = f"{task_id}_report.pdf"
        file_path = str(Path(output_dir) / file_name)
        return ReportExporter.save_to_file(content, file_path, "binary")

    @staticmethod
    def save_json_report(data: dict, task_id: str, output_dir: str = "./reports") -> str:
        """保存 JSON 报告到文件"""
        content = json.dumps(data, ensure_ascii=False, indent=2)
        file_name = f"{task_id}_report.json"
        file_path = str(Path(output_dir) / file_name)
        return ReportExporter.save_to_file(content, file_path, "text")

    @staticmethod
    def create_zip_archive(file_paths: list, output_path: str) -> Optional[str]:
        """创建 ZIP 归档文件"""
        try:
            with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file_path in file_paths:
                    file_path = Path(file_path)
                    if file_path.exists():
                        arcname = file_path.name
                        zipf.write(file_path, arcname)
                        print(f"Added {arcname} to {output_path}")

            return output_path
        except Exception as e:
            import logging
            logging.error(f"Failed to create ZIP archive: {e}")
            return None

    @staticmethod
    def generate_download_filename(task_id: str, format: str) -> str:
        """生成下载文件名"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"apk_scan_{task_id}_{timestamp}.{format}"
