# OWASP Mobile Top 10 (2024) - 学习资源

## OWASP Mobile Top 10 概述

| 序号 | 风险 | 描述 |
|------|------|------|
| M1 | 错误的凭证管理 | 不安全地存储用户凭证 |
| M2 | 不安全的数据存储 | 敏感数据存储不当，易被窃取 |
| M3 | 不安全的通信 | 网络传输数据未加密或加密方式不安全 |
| M4 | 不安全的认证 | 身份认证机制存在缺陷 |
| M5 | 不足的密码学 | 使用弱加密算法或实现错误 |
| M6 | 不安全的授权 | 授权机制存在缺陷，权限提升漏洞 |
| M7 | 客户端代码质量 | 客户端代码存在安全缺陷 |
| M8 | 代码篡改 | 应用代码或运行时环境被篡改 |
| M9 | 反向工程 | 应用易被反编译和分析 |
| M10 | 多余的功能 | 包含未使用或调试功能 |

## 学习路径

### 第一阶段：基础理论
1. 理解 OWASP MASTG (Mobile Security Testing Guide)
2. 学习 Android 应用架构
3. 掌握基础安全概念

### 第二阶段：工具使用
1. 静态分析工具 (JADX, APKTool, MobSF)
2. 动态分析工具 (Frida, Objection)
3. 网络分析工具 (Burp Suite, Wireshark)

### 第三阶段：实战练习
1. 分析漏洞应用
2. 复现常见漏洞
3. 编写利用脚本

## 推荐的易受攻击应用

### 官方靶场应用
1. **DIVA (Damn Insecure and Vulnerable App)**
   - 最经典的 Android 漏洞教学应用
   - GitHub: https://github.com/payatu/diva-android

2. **InsecureBankv2**
   - 银行应用场景的漏洞演示
   - GitHub: https://github.com/dineshshetty/Android-InsecureBankv2

3. **Sieve (from OWASP)**
   - OWASP 官方的安全测试应用
   - 包含多种典型漏洞

4. **Kotlin Goat**
   - 基于 Kotlin 的现代漏洞应用
   - GitHub: https://github.com/FSecureLABS/kotlin-goat

5. **Vulnerable Android App**
   - 包含 OWASP Mobile Top 10 的应用
   - GitHub: https://github.com/hax0rgb/InsecureShop

## 在线资源

- [OWASP Mobile Security Testing Guide](https://mas.owasp.org/MASTG/)
- [OWASP Mobile Security Checklist](https://mas.owasp.org/MASVS/)
- [Frida 官方文档](https://frida.re/docs/home/)
- [MobSF 官方文档](https://mobsf.github.io/docs/)
