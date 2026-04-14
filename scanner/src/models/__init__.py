# Core Configuration and Database Models

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from src.core import engine, Base

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依赖注入：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 枚举类型
class ScanStatus(str):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Severity(str):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class ReportFormat(str):
    HTML = "html"
    PDF = "pdf"
    JSON = "json"

# 数据模型
class ScanTask(Base):
    """扫描任务模型"""
    __tablename__ = "scan_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True, nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)  # 字节
    file_hash = Column(String, index=True)  # SHA256

    status = Column(String, default=ScanStatus.PENDING, index=True)
    progress = Column(Float, default=0.0)  # 0-100

    # 应用信息
    app_name = Column(String)
    package_name = Column(String, index=True)
    version_name = Column(String)
    version_code = Column(String)
    min_sdk = Column(String)
    target_sdk = Column(String)

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    # 错误信息
    error_message = Column(Text)

    # 关系
    vulnerabilities = relationship("Vulnerability", back_populates="scan_task", cascade="all, delete-orphan")
    reports = relationship("ScanReport", back_populates="scan_task", cascade="all, delete-orphan")
    mobsf_scan = relationship("MobSFScan", back_populates="scan_task", uselist=False, cascade="all, delete-orphan")

class Vulnerability(Base):
    """漏洞模型"""
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    scan_task_id = Column(Integer, ForeignKey("scan_tasks.id"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(Text)
    severity = Column(String, index=True, default=Severity.INFO)
    cwe_id = Column(String)  # CWE 编号
    cvss_score = Column(Float)  # CVSS 评分

    # 位置信息
    location = Column(String)  # 文件/类/方法
    line_number = Column(Integer)

    # 修复建议
    recommendation = Column(Text)
    references = Column(JSON)  # 参考链接列表

    # 原始数据
    raw_data = Column(JSON)  # 来自 MobSF 的原始数据

    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    scan_task = relationship("ScanTask", back_populates="vulnerabilities")

class ScanReport(Base):
    """扫描报告模型"""
    __tablename__ = "scan_reports"

    id = Column(Integer, primary_key=True, index=True)
    scan_task_id = Column(Integer, ForeignKey("scan_tasks.id"), nullable=False)

    format = Column(String, default=ReportFormat.HTML)
    title = Column(String)
    summary = Column(Text)

    # 统计信息
    total_vulnerabilities = Column(Integer, default=0)
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)
    info_count = Column(Integer, default=0)

    # 文件路径
    file_path = Column(String)
    file_size = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    scan_task = relationship("ScanTask", back_populates="reports")

class MobSFScan(Base):
    """MobSF 扫描记录"""
    __tablename__ = "mobsf_scans"

    id = Column(Integer, primary_key=True, index=True)
    scan_task_id = Column(Integer, ForeignKey("scan_tasks.id"), nullable=False, unique=True)

    mobsf_scan_hash = Column(String, index=True)  # MobSF 内部哈希
    mobsf_scan_id = Column(String)  # MobSF 扫描 ID

    # 扫描结果
    static_analysis_result = Column(JSON)
    dynamic_analysis_result = Column(JSON)
    manifest_analysis = Column(JSON)
    permission_analysis = Column(JSON)
    code_analysis = Column(JSON)

    # API 响应
    api_response = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    scan_task = relationship("ScanTask", back_populates="mobsf_scan")

# 创建所有表
def create_tables():
    Base.metadata.create_all(bind=engine)
