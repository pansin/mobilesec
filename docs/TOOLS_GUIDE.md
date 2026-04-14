# APK 安全测试实验室 - 工具使用指南

## 目录

1. [静态分析工具](#静态分析工具)
2. [动态分析工具](#动态分析工具)
3. [网络分析工具](#网络分析工具)
4. [Frida 脚本使用](#frida-脚本使用)

---

## 静态分析工具

### JADX - Dex 反编译器

```bash
# 基本用法
jadx app.apk

# 输出到目录
jadx -d output_dir app.apk

# 反混淆
jadx --deobf app.apk

# 启动图形界面
jadx-gui app.apk
```

### APKTool - APK 反编译工具

```bash
# 反编译 APK
apktool d app.apk -o decompiled

# 重新编译
apktool b decompiled -o rebuilt.apk

# 重新编译并签名
apktool b decompiled -o rebuilt.apk
# 然后使用 jarsigner 或 apksigner 签名
```

### MobSF - 移动安全框架

```bash
# 通过 Web 界面使用
# 访问 http://localhost:9000
# 上传 APK 即可

# 通过 API 使用
# 1. 获取 API Token
curl -X POST http://localhost:9000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 2. 上传 APK
curl -X POST http://localhost:9000/api/v1/scan \
  -H "Authorization: Token <your-token>" \
  -F "file=@app.apk"
```

### QARK - Android 应用安全评估工具

```bash
# 基本扫描
qark --apk app.apk

# 交互式模式
qark --apk app.apk --exploit

# 生成报告
qark --apk app.apk --report-type html
```

---

## 动态分析工具

### Frida - 动态插桩框架

```bash
# 查看设备上的进程
frida-ps -U

# 附加到运行中的进程
frida -U com.example.app

# Spawn 并附加
frida -U -f com.example.app

# 加载脚本
frida -U -f com.example.app -l script.js

# 持久化脚本（持续 Hook）
frida -U -f com.example.app -l script.js --no-pause
```

### Objection - Frida 工具集

```bash
# 探索应用
objection -g com.example.app explore

# Spawn 并探索
objection -g com.example.app explore --startup-command "android sslpinning disable"

# 列出类
android hooking list classes

# 列出类的方法
android hooking list class_methods com.example.ClassName

# 搜索类
android hooking search classes keyword

# 禁用 SSL Pinning
android sslpinning disable

# 监控文件访问
android monitor watch new_file
```

---

## 网络分析工具

### Burp Suite

1. **配置 Android 设备代理**
   ```bash
   # 设置代理
   adb shell settings put global http_proxy 192.168.x.x:8080
   
   # 清除代理
   adb shell settings put global http_proxy :0
   ```

2. **安装 CA 证书**
   - 导出 Burp CA 证书 (DER 格式)
   - 转换为 PEM 格式: `openssl x509 -inform DER -in cacert.der -out cacert.pem`
   - 推送到设备: `adb push cacert.pem /sdcard/`
   - 在设备上安装证书

### mitmproxy

```bash
# 启动 mitmproxy
mitmproxy -p 8080

# 启动 mitmweb (Web 界面)
mitmweb -p 8080

# 启动 mitmdump (命令行)
mitmdump -p 8080 -w traffic.log
```

### Wireshark

```bash
# 捕获 Android 设备流量
# 使用 tcpdump 在设备上捕获
adb shell tcpdump -i any -s 0 -w /sdcard/capture.pcap

# 拉取捕获文件
adb pull /sdcard/capture.pcap

# 用 Wireshark 分析
wireshark capture.pcap
```

---

## Frida 脚本使用

### SSL Pinning Bypass

```bash
# 使用预加载的脚本
frida -U -f com.example.app -l /workspace/scripts/ssl-pinning-bypass.js
```

### Root Detection Bypass

```bash
frida -U -f com.example.app -l /workspace/scripts/root-detection-bypass.js
```

### Class Tracer

```bash
frida -U -f com.example.app -l /workspace/scripts/class-tracer.js
# 然后在 Frida REPL 中调用:
# traceClass("com.example.ClassName")
# listClasses()
# listClasses("pattern")
```

### 编写自定义 Frida 脚本

```javascript
// 基本模板
console.log("[*] My script loaded");

Java.perform(function() {
    // Hook 类
    var TargetClass = Java.use("com.example.TargetClass");

    // Hook 方法
    TargetClass.targetMethod.implementation = function(arg1, arg2) {
        console.log("[+] targetMethod called with args: " + arg1 + ", " + arg2);

        // 调用原方法
        var result = this.targetMethod(arg1, arg2);

        console.log("[+] Return value: " + result);
        return result;
    };
});
```
