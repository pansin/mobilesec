---
name: OWASP Mobile Top 10 Tutorials
description: Comprehensive tutorials for each OWASP Mobile Top 10 vulnerability category
---

# OWASP Mobile Top 10 Tutorials

This directory contains comprehensive tutorials for each vulnerability category in the OWASP Mobile Top 10. Each tutorial includes explanations, practical examples, and hands-on exercises using vulnerable Android applications.

## OWASP Mobile Top 10 Overview

### M1: Improper Platform Usage
- **Description**: Misusing Android platform features or failing to use platform security controls
- **Tutorial**: [M1-Improper-Platform-Usage.md](tutorials/M1-Improper-Platform-Usage.md)
- **Practice App**: DIVA, InsecureBankv2

### M2: Insecure Data Storage
- **Description**: Sensitive data stored insecurely on the device
- **Tutorial**: [M2-Insecure-Data-Storage.md](tutorials/M2-Insecure-Data-Storage.md)
- **Practice App**: Sieve, InsecureBankv2

### M3: Insecure Communication
- **Description**: Poorly secured communication between mobile app and backend
- **Tutorial**: [M3-Insecure-Communication.md](tutorials/M3-Insecure-Communication.md)
- **Practice App**: InsecureBankv2

### M4: Insecure Authentication
- **Description**: Weak authentication mechanisms that can be bypassed
- **Tutorial**: [M4-Insecure-Authentication.md](tutorials/M4-Insecure-Authentication.md)
- **Practice App**: InsecureBankv2

### M5: Insufficient Cryptography
- **Description**: Weak or broken cryptography protecting sensitive data
- **Tutorial**: [M5-Insufficient-Cryptography.md](tutorials/M5-Insufficient-Cryptography.md)
- **Practice App**: Sieve

### M6: Insecure Authorization
- **Description**: Failure to properly verify user permissions and roles
- **Tutorial**: [M6-Insecure-Authorization.md](tutorials/M6-Insecure-Authorization.md)
- **Practice App**: InsecureBankv2

### M7: Client Code Quality
- **Description**: Poor code quality leading to security vulnerabilities
- **Tutorial**: [M7-Client-Code-Quality.md](tutorials/M7-Client-Code-Quality.md)
- **Practice App**: DIVA

### M8: Code Tampering
- **Description**: Binary patching, runtime manipulation, and hooking
- **Tutorial**: [M8-Code-Tampering.md](tutorials/M8-Code-Tampering.md)
- **Practice App**: Use Frida scripts

### M9: Reverse Engineering
- **Description**: Analyzing and understanding compiled app code
- **Tutorial**: [M9-Reverse-Engineering.md](tutorials/M9-Reverse-Engineering.md)
- **Practice App**: Any target app

### M10: Extraneous Functionality
- **Description**: Hidden or debug functionality left in production
- **Tutorial**: [M10-Extraneous-Functionality.md](tutorials/M10-Extraneous-Functionality.md)
- **Practice App**: InsecureBankv2

## How to Use These Tutorials

1. **Start with the basics**: Begin with M1 and progress through each category
2. **Read the theory**: Understand the vulnerability and its impact
3. **Practice hands-on**: Use the recommended vulnerable apps to practice exploitation
4. **Learn defense**: Understand how to fix and prevent each vulnerability type
5. **Complete challenges**: Test your skills with the included challenges

## Prerequisites

- Android emulator or rooted device
- ADB installed and configured
- Frida setup (dynamic analysis)
- JADX or APKTool (static analysis)
- Burp Suite (network analysis)

See [Tools Setup Guide](../docs/TOOLS_GUIDE.md) for installation help.