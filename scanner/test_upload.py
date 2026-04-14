#!/usr/bin/env python3
"""Test upload script"""

import requests

url = "http://127.0.0.1:3080/api/v1/scans/upload"

# Create a test APK file
with open("/tmp/test.apk", "rb") as f:
    files = {"file": ("分期乐_8.10.3_APKPure.apk", f, "application/vnd.android.package-archive")}
    response = requests.post(url, files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
