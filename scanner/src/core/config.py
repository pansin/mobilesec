# Configuration Management

import os
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """应用配置"""

    # 应用基础配置
    app_name: str = "APK Security Scanner"
    app_version: str = "1.0.0"
    debug: bool = True
    secret_key: str = "your-secret-key-change-in-production"

    # 数据库配置
    database_url: str = "postgresql://mobilesec:mobilesec123@localhost:5432/mobilesec"

    # Redis 配置
    redis_url: str = "redis://localhost:6379/0"

    # MobSF 配置
    mobsf_url: str = "http://localhost:9000"
    mobsf_api_key: str = "a474e8e5c08c2a21125e8819b916fb30fb3904b6fd2cfb7ca3a0d50e1f8d5ba6"

    # 文件上传配置
    upload_dir: str = "./uploads"
    max_upload_size: int = 524288000  # 500MB
    allowed_extensions: List[str] = ["apk", "xapk", "apks"]

    # CORS 配置
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8001", "http://localhost:3080", "http://localhost:3001"]

    # 日志配置
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"

    # Celery 配置
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()

# 导出设置实例
settings = get_settings()
