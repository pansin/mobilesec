#!/usr/bin/env python3
"""Test Celery connection"""

from celery import Celery

# Test Redis connection
from src.core.config import settings
print(f"Redis URL: {settings.redis_url}")
print(f"Celery broker: {settings.celery_broker_url}")
print(f"Celery backend: {settings.celery_result_backend}")

# Create a simple test
app = Celery('test', broker=settings.celery_broker_url, backend=settings.celery_result_backend)

# Test connection
try:
    conn = app.connection()
    conn.connect()
    print("\nRedis connection: SUCCESS")
    conn.close()
except Exception as e:
    print(f"\nRedis connection error: {e}")
