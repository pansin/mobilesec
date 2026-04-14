# MobSF - Mobile Security Framework

Mobile Security Framework (MobSF) 是一个开源的移动应用自动化安全测试工具，支持 Android 和 iOS 应用的静态、动态和恶意软件分析。

## 构建命令

```bash
cd /Users/pansinliu/Documents/GitHub/mobilesec/docker/mobsf
docker build -t mobilesec/mobsf:latest .
```

## 默认配置

- **端口**: 9000
- **API 端点**: `/api/v1/`
- **API 密钥**: 需要通过 `/api/v1/auth/login` 获取

## 使用方法

### 访问 Web 界面

启动容器后，访问 `http://localhost:9000` 即可使用 MobSF 的 Web 界面。

### 使用 API 接口

```bash
# 1. 获取访问令牌
curl -X POST \
  http://localhost:9000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"admin123"}'

# 2. 上传并扫描 APK
curl -X POST \
  http://localhost:9000/api/v1/scan \
  -H 'Authorization: Token <your-token>' \
  -F 'file=@/path/to/app.apk'

# 3. 获取扫描结果
curl -X GET \
  http://localhost:9000/api/v1/report/<scan-id> \
  -H 'Authorization: Token <your-token>' \
  -H 'Accept: application/json'
```
