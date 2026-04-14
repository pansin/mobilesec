---
name: Sandbox Environment
description: Safe and controlled environment for security testing
---

# Sandbox Environment

## Overview

The sandbox environment provides a safe, isolated space for Android security testing. It includes pre-configured Android emulators, testing tools, and network isolation to ensure testing activities don't affect production systems.

## Architecture

### Components

1. **Android Emulators** - Pre-configured with different Android versions and configurations
2. **Network Isolation** - Separate network for testing traffic
3. **Monitoring Tools** - Network capture, process monitoring, and file system monitoring
4. **Snapshot Management** - Easy rollback to clean state

## Quick Start

### Prerequisites

- Docker and Docker Compose
- KVM support (for faster emulation)
- At least 8GB RAM
- At least 50GB disk space

### Starting the Sandbox

```bash
cd lab/docker

# Build and start the sandbox environment
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Accessing the Sandbox

```bash
# Enter the sandbox container
docker-compose exec sandbox bash

# Access ADB
adb devices

# Connect to emulator
adb emu avd name
```

## Emulator Configurations

### Emulator 1: Stock Android 13
- **Name**: stock-android-13
- **API Level**: 33
- **Rooted**: No
- **Google Play**: Yes
- **Use Case**: Testing apps on standard Android
- **Ports**: 5554, 5555

### Emulator 2: Rooted Android 11
- **Name**: rooted-android-11
- **API Level**: 30
- **Rooted**: Yes (Magisk)
- **Google Play**: No
- **Use Case**: Advanced testing requiring root access
- **Ports**: 5556, 5557

### Emulator 3: Frida-Preloaded Android 12
- **Name**: frida-android-12
- **API Level**: 31
- **Rooted**: Yes
- **Frida**: Pre-installed
- **Use Case**: Dynamic analysis with Frida
- **Ports**: 5558, 5559

## Network Configuration

### Network Isolation
- **Sandbox Network**: 172.20.0.0/16
- **Isolated from host**: Yes
- **Internet access**: Optional (default: enabled)

### Network Services
- **Burp Suite**: http://localhost:8080
- **mitmproxy**: http://localhost:8081
- **Wireshark**: Capture interface available

### Network Modes

#### Mode 1: Full Internet (Default)
```yaml
network_mode: bridge
```

#### Mode 2: Isolated (No Internet)
```yaml
network_mode: none
```

#### Mode 3: MitM Proxy
```yaml
network_mode: bridge
extra_hosts:
  - "example.com:172.20.0.10"
```

## Snapshot Management

### Creating Snapshots

```bash
# Create a snapshot of emulator 1
docker-compose exec sandbox adb -s emulator-5554 emu avd snapshot save clean-state

# List snapshots
docker-compose exec sandbox adb -s emulator-5554 emu avd snapshot list
```

### Restoring Snapshots

```bash
# Restore clean state
docker-compose exec sandbox adb -s emulator-5554 emu avd snapshot load clean-state

# Restore and start
docker-compose exec sandbox adb -s emulator-5554 emu avd snapshot load clean-state && adb -s emulator-5554 emu kill && adb -s emulator-5554 emu start
```

## File System Monitoring

### Monitoring Tools

1. **inotifywait** - File system change monitoring
2. **lsof** - Open file monitoring
3. **strace** - System call tracing

### Usage Examples

```bash
# Monitor file changes in /data/data
inotifywait -m -r /data/data/com.example.app

# Monitor network connections
strace -e trace=network -p <PID>

# Monitor all system calls
strace -f -p <PID>
```

## Process Monitoring

### Process List
```bash
# List all processes
adb shell ps

# List processes by app
adb shell ps | grep com.example.app
```

### Memory Analysis
```bash
# Memory info for a process
adb shell dumpsys meminfo com.example.app

# Detailed memory map
adb shell cat /proc/<PID>/maps
```

## Security Best Practices

### 1. Always Use Snapshots
- Start from a clean state for each test
- Create snapshots before installing apps
- Never reuse contaminated instances

### 2. Network Isolation
- Use isolated mode for potentially malicious apps
- Monitor all network traffic
- Disable internet when not needed

### 3. Data Protection
- Never use real credentials or sensitive data
- Use test accounts only
- Clear app data after each test

### 4. Host Protection
- Run sandbox in dedicated VM if possible
- Keep sandbox updated
- Monitor sandbox activity

## Troubleshooting

### Emulator Won't Start
```bash
# Check KVM support
egrep -c '(vmx|svm)' /proc/cpuinfo

# Check Docker resources
docker info
```

### ADB Connection Issues
```bash
# Restart ADB server
adb kill-server
adb start-server

# Check devices
adb devices
```

### Network Problems
```bash
# Check network configuration
docker network inspect lab_sandbox

# Test connectivity
docker-compose exec sandbox ping 8.8.8.8
```

## Cleanup

```bash
# Stop sandbox
docker-compose down

# Remove volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## Advanced Usage

### Custom Emulator Configurations

Create a `custom-emulator.json` file:
```json
{
  "name": "custom-android",
  "api_level": 30,
  "rooted": true,
  "google_play": false,
  "frida": true,
  "xposed": true
}
```

Build and start:
```bash
docker-compose build --build-arg EMULATOR_CONFIG=custom-emulator.json
docker-compose up -d
```

### Integration with Scanner Platform

The sandbox can integrate with the scanner platform for automated testing:
- Emulator discovery via API
- Automated APK installation
- Test orchestration
- Result collection

See [Scanner Integration](SCANNER_INTEGRATION.md) for more details.