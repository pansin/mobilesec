#!/usr/bin/env python3
"""
工具模块 - 提供通用工具函数
"""

import os
import hashlib
import magic
from pathlib import Path
from typing import List, Optional, Dict
from fastapi import UploadFile
import re

def is_valid_apk_file(file: UploadFile) -> bool:
    """检查文件是否是有效的 APK 文件"""
    # 检查文件名扩展名
    filename = file.filename.lower() if file.filename else ""
    if not filename.endswith('.apk'):
        return False

    # 放宽验证，仅检查文件扩展名
    return True

def calculate_sha256(file_path: str) -> str:
    """计算文件的 SHA256 哈希值"""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def calculate_md5(file_path: str) -> str:
    """计算文件的 MD5 哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sanitize_filename(filename: str) -> str:
    """清理文件名"""
    return re.sub(r'[^\w\-.]', '_', filename)

def get_file_size_formatted(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def ensure_dir_exists(path: str):
    """确保目录存在，不存在则创建"""
    Path(path).mkdir(parents=True, exist_ok=True)

def get_file_info(file_path: str) -> Optional[Dict]:
    """获取文件详细信息"""
    try:
        stat = os.stat(file_path)
        file_type = magic.from_file(file_path)

        return {
            "size": stat.st_size,
            "size_formatted": get_file_size_formatted(stat.st_size),
            "modified_time": stat.st_mtime,
            "created_time": stat.st_ctime,
            "file_type": file_type,
            "extension": Path(file_path).suffix.lower().lstrip('.')
        }
    except Exception as e:
        import logging
        logging.error(f"Error getting file info: {e}")
        return None
