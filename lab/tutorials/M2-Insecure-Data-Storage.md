---
name: M2 - Insecure Data Storage
description: Tutorial on identifying and exploiting insecure data storage vulnerabilities
---

# M2: Insecure Data Storage

## Overview

Insecure data storage is one of the most common vulnerabilities in Android applications. This occurs when sensitive information is stored without proper protection, allowing attackers with physical access to the device or malicious apps to access the data.

## Common Storage Locations

### 1. Shared Preferences
```java
// INSECURE: Storing passwords in SharedPreferences
SharedPreferences prefs = getSharedPreferences("user_prefs", MODE_PRIVATE);
prefs.edit().putString("password", userPassword).apply();
```

### 2. SQLite Databases
```java
// INSECURE: Storing credit cards in unencrypted SQLite
SQLiteDatabase db = openOrCreateDatabase("payments.db", MODE_PRIVATE, null);
db.execSQL("CREATE TABLE cards (id INTEGER, number TEXT)");
db.execSQL("INSERT INTO cards VALUES (1, '4111-1111-1111-1111')");
```

### 3. External Storage
```java
// INSECURE: Writing sensitive data to SD card
File file = new File(Environment.getExternalStorageDirectory(), "user_data.txt");
FileWriter writer = new FileWriter(file);
writer.write("API Key: secret-12345");
writer.close();
```

## Detection Methods

### Using ADB to Pull Files

1. **Check Shared Preferences**:
```bash
# Get the app's shared preferences XML
adb shell "run-as com.example.app cat /data/data/com.example.app/shared_prefs/user_prefs.xml"
```

2. **Check SQLite Databases**:
```bash
# Pull database file from device
adb pull /data/data/com.example.app/databases/payments.db
```

3. **Check External Storage**:
```bash
# List files on SD card
adb shell ls -la /sdcard/
```

### Static Analysis with JADX

1. Decompile the APK:
```bash
jadx -d decompiled app.apk
```

2. Search for sensitive patterns:
```bash
# Search for SharedPreferences usage
grep -r "SharedPreferences" decompiled/

# Search for database creation
grep -r "SQLiteDatabase\|openOrCreateDatabase" decompiled/
```

## Hands-On Practice with Sieve

### Target App
**Sieve** - A password manager app with insecure data storage.

### Exercise 1: Extract Encryption Key

1. Install and launch Sieve:
```bash
adb install sieve.apk
```

2. Create a master password and store some test passwords.

3. Extract the SharedPreferences file:
```bash
adb shell "run-as com.mwr.example.sieve cat /data/data/com.mwr.example.sieve/shared_prefs/com.mwr.example.sieve_preferences.xml"
```

4. Look for the `Key` or `Password` field in the XML.

### Exercise 2: Decrypt the Database

1. Pull the encrypted database:
```bash
adb pull /data/data/com.mwr.example.sieve/databases/passwords.db
```

2. Use the extracted key to decrypt the database.

3. View the decrypted passwords.

## Defense Strategies

### 1. Use Encrypted SharedPreferences
```java
// Secure: Use EncryptedSharedPreferences
MasterKey masterKey = new MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build();

SharedPreferences encryptedPrefs = EncryptedSharedPreferences.create(
    "secure_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
);
```

### 2. Use SQLCipher for Encrypted Databases
```java
// Secure: Use SQLCipher for encrypted databases
SQLiteDatabase.loadLibs(context);
SQLiteDatabase db = SQLiteDatabase.openOrCreateDatabase(
    "encrypted.db",
    "secure-password",
    null
);
```

### 3. Avoid Storing Sensitive Data
- Don't store sensitive data unless absolutely necessary
- Use Android Keystore for cryptographic keys
- Consider biometric authentication for sensitive operations

## Challenge

Using what you've learned:

1. **Target**: InsecureBankv2
2. **Task**: Extract all stored usernames and passwords
3. **Hint**: Check the SharedPreferences and SQLite databases

## Tools Reference

- **ADB**: Debug bridge for device interaction
- **JADX**: Decompiler for static analysis
- **Frida**: Dynamic instrumentation (optional)
- **SQLCipher**: Encrypted database library

## Additional Resources

- [OWASP Mobile Security Testing Guide - Data Storage](https://mas.owasp.org/MASTG/tests/android/MSTG-STORAGE/)
- [Android Keystore System Documentation](https://developer.android.com/training/articles/keystore)