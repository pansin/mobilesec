/**
 * Root Detection Bypass Script
 * 使用: frida -U -f com.example.app -l root-detection-bypass.js
 */

console.log("[*] Root Detection Bypass Script loaded");

Java.perform(function() {
    console.log("[+] Starting Root Detection Bypass...");

    // 1. Build.TAGS 检查绕过
    try {
        var Build = Java.use("android.os.Build");
        var tagsField = Build.class.getDeclaredField("TAGS");
        tagsField.setAccessible(true);
        tagsField.set(null, "release-keys");
        console.log("[+] Bypassed Build.TAGS check");
    } catch (e) {
        console.log("[-] Build.TAGS bypass failed: " + e);
    }

    // 2. Common root file paths 检查绕过
    var rootPaths = [
        "/system/app/Superuser.apk",
        "/system/xbin/su",
        "/system/bin/su",
        "/system/xbin/daemonsu",
        "/system/etc/init.d/99SuperSUDaemon",
        "/system/bin/.ext/.su",
        "/system/usr/we-need-root/",
        "/system/xbin/busybox",
        "/sbin/su",
        "/data/local/su",
        "/data/local/bin/su",
        "/data/local/xbin/su",
        "/dev/com.koushikdutta.superuser.daemon/",
        "/system/app/Superuser.apk",
        "/system/app/Magisk.apk"
    ];

    try {
        var File = Java.use("java.io.File");
        File.exists.implementation = function() {
            var path = this.getAbsolutePath();
            for (var i = 0; i < rootPaths.length; i++) {
                if (path.indexOf(rootPaths[i]) !== -1) {
                    console.log("[+] Bypassed root file check: " + path);
                    return false;
                }
            }
            return this.exists.call(this);
        };
        console.log("[+] Bypassed root file paths check");
    } catch (e) {
        console.log("[-] Root file paths bypass failed: " + e);
    }

    // 3. su 命令执行检查绕过
    try {
        var Runtime = Java.use("java.lang.Runtime");
        Runtime.exec.overload('[Ljava.lang.String;').implementation = function(cmd) {
            if (cmd && cmd.length > 0) {
                if (cmd[0] === "su" || cmd[0].indexOf("su") !== -1) {
                    console.log("[+] Bypassed su command execution: " + cmd.join(" "));
                    throw Java.use("java.io.IOException").$new("Error");
                }
            }
            return this.exec.overload('[Ljava.lang.String;').call(this, cmd);
        };
        Runtime.exec.overload('java.lang.String').implementation = function(cmd) {
            if (cmd && (cmd === "su" || cmd.indexOf("su") !== -1)) {
                console.log("[+] Bypassed su command execution: " + cmd);
                throw Java.use("java.io.IOException").$new("Error");
            }
            return this.exec.overload('java.lang.String').call(this, cmd);
        };
        console.log("[+] Bypassed su command check");
    } catch (e) {
        console.log("[-] su command bypass failed: " + e);
    }

    // 4. PackageManager 检查绕过
    try {
        var PackageManager = Java.use("android.content.pm.PackageManager");
        var ApplicationPackageManager = Java.use("android.app.ApplicationPackageManager");

        var rootPackages = [
            "com.noshufou.android.su",
            "com.thirdparty.superuser",
            "eu.chainfire.supersu",
            "com.koushikdutta.superuser",
            "com.zachspong.temprootremovejb",
            "com.ramdroid.appquarantine",
            "topjohnwu.magisk"
        ];

        ApplicationPackageManager.getPackageInfo.overload('java.lang.String', 'int').implementation = function(pkg, flags) {
            for (var i = 0; i < rootPackages.length; i++) {
                if (pkg === rootPackages[i]) {
                    console.log("[+] Bypassed root package check: " + pkg);
                    throw Java.use("android.content.pm.PackageManager$NameNotFoundException").$new();
                }
            }
            return this.getPackageInfo.overload('java.lang.String', 'int').call(this, pkg, flags);
        };
        console.log("[+] Bypassed root package check");
    } catch (e) {
        console.log("[-] Root package bypass failed: " + e);
    }

    // 5. Debug Bridge 检查绕过
    try {
        var Secure = Java.use("android.provider.Settings$Secure");
        Secure.getInt.overload('android.content.ContentResolver', 'java.lang.String', 'int').implementation = function(resolver, name, def) {
            if (name === "adb_enabled") {
                console.log("[+] Bypassed ADB enabled check");
                return 0;
            }
            return this.getInt.overload('android.content.ContentResolver', 'java.lang.String', 'int').call(this, resolver, name, def);
        };
        console.log("[+] Bypassed ADB check");
    } catch (e) {
        console.log("[-] ADB check bypass failed: " + e);
    }

    console.log("[+] Root Detection Bypass complete!");
});
