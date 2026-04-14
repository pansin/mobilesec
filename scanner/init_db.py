#!/usr/bin/env python3
"""
初始化数据库脚本
"""

import os
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core import engine, Base, get_db, settings
from src.models import (
    ScanTask,
    ScanStatus,
    Vulnerability,
    Severity,
    ScanReport,
    ReportFormat,
    MobSFScan
)

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
