/**
 * Class Tracer - 追踪方法调用
 * 使用: frida -U -f com.example.app -l class-tracer.js
 */

console.log("[*] Class Tracer Script loaded");

var tracedClasses = [];

// 追踪指定类的所有方法
function traceClass(className) {
    if (tracedClasses.indexOf(className) !== -1) {
        console.log("[-] Class already traced: " + className);
        return;
    }

    try {
        var clazz = Java.use(className);
        var methods = clazz.class.getDeclaredMethods();

        console.log("[+] Tracing class: " + className);
        console.log("[+] Found " + methods.length + " methods");

        methods.forEach(function(method) {
            var methodName = method.getName();
            var overloads = clazz[methodName].overloads;

            overloads.forEach(function(overload) {
                try {
                    overload.implementation = function() {
                        var args = Array.prototype.slice.call(arguments);
                        console.log("\n[*] " + className + "." + methodName + " called");
                        console.log("    Arguments:");
                        args.forEach(function(arg, idx) {
                            console.log("      [" + idx + "]: " + arg);
                        });

                        var result = overload.apply(this, arguments);

                        console.log("    Return: " + result);
                        return result;
                    };
                } catch (e) {
                    // 忽略无法 hook 的方法
                }
            });
        });

        tracedClasses.push(className);
        console.log("[+] Successfully hooked class: " + className);
    } catch (e) {
        console.log("[-] Error tracing class " + className + ": " + e);
    }
}

// 列出所有加载的类
function listClasses(pattern) {
    console.log("[*] Listing loaded classes" + (pattern ? " matching: " + pattern : ""));
    Java.enumerateLoadedClasses({
        onMatch: function(className) {
            if (!pattern || className.indexOf(pattern) !== -1) {
                console.log("  " + className);
            }
        },
        onComplete: function() {
            console.log("[*] Class listing complete");
        }
    });
}

// 主函数
Java.perform(function() {
    console.log("\n=== Class Tracer Ready ===");
    console.log("Available functions:");
    console.log("  - traceClass(\"com.example.ClassName\") - 追踪指定类的所有方法");
    console.log("  - listClasses() - 列出所有加载的类");
    console.log("  - listClasses(\"pattern\") - 列出匹配模式的类");
    console.log("==========================\n");

    // 示例: 自动追踪一些常见的敏感类
    // traceClass("android.util.Log");
    // traceClass("javax.crypto.Cipher");
});
