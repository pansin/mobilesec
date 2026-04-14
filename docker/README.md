# APK 安全测试实验室 - 快速启动脚本

# APK 安全测试实验室平台

基于 Docker 的 Android 应用安全测试综合平台

## 目录

## 快速开始

### 1. 构建和启动所有服务

```bash
# 克隆项目
cd mobilesec
cd docker

# 构建所有镜像
docker-compose build

# 启动所有服务
docker-compose up -d
```

### 2. 访问各服务

| 服务 | 地址 | 说明 |
|------|------|------|
| MobSF Web界面 | http://localhost:9000 | 移动安全框架 |
| Kali 容器 | `docker exec -it mobilesec-kali bash | 安全测试工具环境 |
| Frida 容器 | `docker exec -it mobilesec-frida bash | 动态插桩工具 |

### 3. 连接 Android 设备

```bash
# 在主机上启用 ADB 连接设备
adb devices

# 进入 Kali 容器
docker exec -it mobilesec-kali bash

# 验证设备应该已经通过 host 网络可访问设备
adb devices
```

### 4. 使用 MobSF 扫描 APK

1. 访问 http://localhost:9000
2. 上传 APK 文件
3. 等待扫描完成
4. 查看安全报告

### 5. 使用 Frida 进行动态分析

```bash
# 进入 Frida 容器
docker exec -it mobilesec-frida bash

# 确保设备已连接
adb devices

# 推送 Frida Server 到设备
adb push /usr/local/frida-server/frida-server-arm64 /data/local/tmp/frida-server
adb shell "chmod 755 /data/local/tmp/frida-server"

# 启动 Frida Server (后台)
adb shell "/data/local/tmp/frida-server &

# 列出设备上的进程
frida-ps -U

# 运行 SSL Pinning Bypass 脚本
frida -U -f com.example.app -l /workspace/scripts/ssl-pinning-bypass.js
```

## 详细文档

请参考各模块的 README 文件获取更多详细信息：

- [Kali 基础环境](./kali-base/README.md)
- [MobSF 服务](./mobsf/README.md)
- [Frida 环境](./frida/README.md)

## 常用命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止所有服务
docker-compose stop

# 启动所有服务
docker-compose start

# 重启服务
docker-compose restart

# 清理所有服务和 volumes
docker-compose down -v
```

## 故障排除

### ADB 设备无法访问:
- 确保容器使用 host 网络模式
- 检查主机上 ADB 正常工作
- 确认 USB 设备已正确挂载

### 内存不足:
- 调整 Docker 分配更多内存（建议 8GB+）

### 端口冲突:
- 修改 docker-compose.yml 中的端口映射
