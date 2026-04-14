#!/usr/bin/env python3
"""
MobSF API 集成服务
"""

import httpx
import json
from typing import Optional, List, Dict
from loguru import logger
from src.core import settings

class MobSFAPIError(Exception):
    """MobSF API 异常"""
    def __init__(self, status_code: int, message: str = None):
        self.status_code = status_code
        self.message = message
        super().__init__(f"MobSF API Error {status_code}: {message}")

class MobSFAPI:
    """MobSF API 客户端"""

    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or settings.mobsf_url
        self.api_key = api_key or settings.mobsf_api_key
        self.timeout = 300  # 5分钟超时

    def _headers(self):
        """获取请求头"""
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        return headers

    async def check_health(self) -> bool:
        """检查 MobSF API 可用性"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/scans",
                    headers=self._headers()
                )

            if response.status_code == 200:
                return True
            return False
        except Exception as e:
            logger.error(f"MobSF health check failed: {e}")
            return False

    async def upload_apk(self, file_path: str) -> Dict:
        """上传 APK 文件"""
        try:
            with open(file_path, "rb") as file:
                files = {"file": file}
                headers = {
                    "Authorization": self.api_key,
                }

                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/api/v1/upload",
                        headers=headers,
                        files=files
                    )

                response.raise_for_status()
                result = response.json()

                if result.get("status") != "success":
                    raise MobSFAPIError(response.status_code, result.get("message"))

                logger.info(f"APK uploaded successfully: {result.get('scan_hash')}")
                return result
        except httpx.HTTPStatusError as e:
            logger.error(f"APK upload failed: {e}")
            raise MobSFAPIError(e.response.status_code, str(e))
        except Exception as e:
            logger.error(f"APK upload exception: {e}")
            raise

    async def scan_apk(self, scan_hash: str) -> Dict:
        """扫描 APK 文件"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/scan",
                    headers={
                        "Authorization": self.api_key,
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    content=f"hash={scan_hash}"
                )

                response.raise_for_status()
                result = response.json()

                # MobSF 返回 200 即表示成功，不需要 status 字段
                logger.info(f"APK scan completed: {result.get('hash')}")
                return result
        except httpx.HTTPStatusError as e:
            logger.error(f"Scan failed: {e}")
            raise MobSFAPIError(e.response.status_code, str(e))
        except Exception as e:
            logger.error(f"Scan exception: {e}")
            raise

    async def get_report(self, scan_hash: str, format: str = "json") -> Dict:
        """获取扫描报告"""
        supported_formats = ["json", "html", "pdf"]
        if format not in supported_formats:
            raise ValueError(f"Unsupported format: {format}")

        try:
            params = {"scan_hash": scan_hash, "format": format}
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/report",
                    headers=self._headers(),
                    params=params
                )

                response.raise_for_status()

                if format == "json":
                    return response.json()
                else:
                    return response.content
        except httpx.HTTPStatusError as e:
            logger.error(f"Get report failed: {e}")
            raise MobSFAPIError(e.response.status_code, str(e))
        except Exception as e:
            logger.error(f"Get report exception: {e}")
            raise

    async def get_scan_result(self, scan_hash: str) -> Dict:
        """获取扫描结果详细信息"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/scan_result",
                    headers=self._headers(),
                    params={"scan_hash": scan_hash}
                )

                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Get scan result failed: {e}")
            raise

    async def get_manifest_analysis(self, scan_hash: str) -> Dict:
        """获取 Manifest 分析结果"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/manifest_analysis",
                    headers=self._headers(),
                    params={"scan_hash": scan_hash}
                )

                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Get manifest analysis failed: {e}")
            raise

    async def get_permission_analysis(self, scan_hash: str) -> Dict:
        """获取权限分析"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/permission_analysis",
                    headers=self._headers(),
                    params={"scan_hash": scan_hash}
                )

                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Get permission analysis failed: {e}")
            raise

    async def extract_application_info(self, scan_result: Dict) -> Dict:
        """从扫描结果中提取应用信息"""
        info = {}

        # 新格式：直接从根级别获取
        info.update({
            "app_name": scan_result.get("app_name"),
            "package_name": scan_result.get("package_name"),
            "version_name": scan_result.get("version_name"),
            "version_code": scan_result.get("version_code"),
            "min_sdk": scan_result.get("min_sdk"),
            "target_sdk": scan_result.get("target_sdk"),
        })

        return info

    async def extract_vulnerabilities(self, scan_result: Dict) -> List[Dict]:
        """从扫描结果中提取漏洞信息"""
        vulnerabilities = []

        # 从 appsec 中提取漏洞
        appsec = scan_result.get("appsec", {})

        # 处理 high severity
        for item in appsec.get("warning", []):
            vuln = {
                "title": item.get("title", "Unknown"),
                "description": item.get("description", ""),
                "severity": "high",
                "cwe_id": None,
                "cvss_score": None,
                "location": item.get("section", ""),
                "line_number": None,
                "recommendation": "",
                "references": [],
                "raw_data": item
            }
            vulnerabilities.append(vuln)

        # 处理 warning severity (hotspot)
        for item in appsec.get("hotspot", []):
            vuln = {
                "title": item.get("title", "Unknown"),
                "description": item.get("description", ""),
                "severity": "medium",
                "cwe_id": None,
                "cvss_score": None,
                "location": item.get("section", ""),
                "line_number": None,
                "recommendation": "",
                "references": [],
                "raw_data": item
            }
            vulnerabilities.append(vuln)

        return vulnerabilities

    async def extract_manifest_info(self, scan_result: Dict) -> Dict:
        """提取 Manifest 信息"""
        manifest_info = {}
        if "manifest" in scan_result:
            manifest_info.update(scan_result.get("manifest", {}))

        return manifest_info

    async def extract_permissions(self, scan_result: Dict) -> List[str]:
        """提取权限信息"""
        permissions = []
        if "permissions" in scan_result:
            permissions.extend(scan_result.get("permissions", []))

        return permissions

    async def full_scan(self, file_path: str) -> Dict:
        """执行完整的扫描流程"""
        logger.info(f"Starting full scan of: {file_path}")

        # 1. 上传
        upload_result = await self.upload_apk(file_path)
        scan_hash = upload_result.get("hash")

        # 2. 扫描
        scan_result = await self.scan_apk(scan_hash)

        return {
            "scan_hash": scan_hash,
            "upload_result": upload_result,
            "scan_result": scan_result
        }
