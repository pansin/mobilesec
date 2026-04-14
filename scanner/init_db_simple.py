#!/usr/bin/env python3
"""
初始化数据库脚本 - 简化版本，不使用 pydantic_settings
"""

import os
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 简化配置
DATABASE_URL = "postgresql://mobilesec:mobilesec123@localhost:5432/mobilesec"

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import declarative_base, sessionmaker

    # 创建引擎
    engine = create_engine(DATABASE_URL)
    Base = declarative_base()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    print("Database URL:", DATABASE_URL)

except Exception as e:
    print(f"Error importing database modules: {e}")
    print("\nUsing SQLite as fallback for demonstration...")

    # 使用 SQLite 作为后备
    from sqlalchemy import create_engine
    from sqlalchemy.orm import declarative_base, sessionmaker

    DATABASE_URL = "sqlite:///./mobilesec.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base = declarative_base()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 简单的数据模型
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Enum as SQLEnum
from enum import Enum

class ScanStatus(str, Enum):
    PENDING = "pending"
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    SCANNING = "scanning"
    ANALYZING = "analyzing"
    GENERATING_REPORT = "generating_report"
    COMPLETED = "completed"
    FAILED = "failed"

class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class ReportFormat(str, Enum):
    HTML = "html"
    PDF = "pdf"
    JSON = "json"

class ScanTask(Base):
    __tablename__ = "scan_tasks"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_size = Column(Integer)
    file_hash = Column(String)
    status = Column(SQLEnum(ScanStatus), default=ScanStatus.PENDING)
    progress = Column(Integer, default=0)
    app_name = Column(String, nullable=True)
    app_version = Column(String, nullable=True)
    package_name = Column(String, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    severity = Column(SQLEnum(Severity))
    cwe_id = Column(String, nullable=True)
    cvss_score = Column(Float, nullable=True)
    recommendation = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    evidence = Column(Text, nullable=True)
    scan_task_id = Column(String, index=True)
    created_at = Column(DateTime)

class ScanReport(Base):
    __tablename__ = "scan_reports"

    id = Column(String, primary_key=True, index=True)
    format = Column(SQLEnum(ReportFormat))
    file_path = Column(String, nullable=True)
    total_vulnerabilities = Column(Integer, default=0)
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)
    info_count = Column(Integer, default=0)
    generated_at = Column(DateTime)
    scan_task_id = Column(String, index=True)

class MobSFScan(Base):
    __tablename__ = "mobsf_scans"

    id = Column(String, primary_key=True, index=True)
    scan_hash = Column(String, index=True)
    static_analysis = Column(Text, nullable=True)
    dynamic_analysis = Column(Text, nullable=True)
    manifest = Column(Text, nullable=True)
    permissions = Column(Text, nullable=True)
    scan_task_id = Column(String, index=True)
    created_at = Column(DateTime)

def init_database():
    """初始化数据库"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

    # 显示创建的表
    print("\nCreated tables:")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")

if __name__ == "__main__":
    try:
        init_database()
        print("\nDatabase initialization completed!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)