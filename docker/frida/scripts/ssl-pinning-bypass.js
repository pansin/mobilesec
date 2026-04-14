/**
 * SSL Pinning Bypass Script
 * 使用: frida -U -f com.example.app -l ssl-pinning-bypass.js
 */

console.log("[*] SSL Pinning Bypass Script loaded");

// Android SSL Pinning Bypass
Java.perform(function() {
    console.log("[+] Starting SSL Pinning Bypass...");

    try {
        // 1. TrustManager 绕过
        var TrustManagerImpl = Java.use("com.android.org.conscrypt.TrustManagerImpl");
        TrustManagerImpl.checkTrustedRecursive.implementation = function(chain, authType, host, clientAuth, session, certs) {
            console.log("[+] Bypassing TrustManagerImpl.checkTrustedRecursive");
            return;
        };

        // 2. OkHttp v3.x - CertificatePinner 绕过
        try {
            var CertificatePinner = Java.use("okhttp3.CertificatePinner");
            CertificatePinner.check.overload('java.lang.String', 'java.util.List').implementation = function(host, certificates) {
                console.log("[+] Bypassing OkHttp CertificatePinner.check for host: " + host);
                return;
            };
            CertificatePinner.check.overload('java.lang.String', '[Ljava.security.cert.Certificate;').implementation = function(host, certificates) {
                console.log("[+] Bypassing OkHttp CertificatePinner.check (array) for host: " + host);
                return;
            };
        } catch (e) {
            console.log("[-] OkHttp CertificatePinner not found or already bypassed");
        }

        // 3. OkHttp v4.x - CertificatePinner 绕过
        try {
            var CertificatePinnerV4 = Java.use("okhttp3.CertificatePinner");
            CertificatePinnerV4.checkCertificatePinning.implementation = function(host, certificates) {
                console.log("[+] Bypassing OkHttp v4 CertificatePinner.checkCertificatePinning for host: " + host);
                return;
            };
        } catch (e) {
            console.log("[-] OkHttp v4 CertificatePinner not found or already bypassed");
        }

        // 4. HostnameVerifier 绕过
        try {
            var HostnameVerifier = Java.use("javax.net.ssl.HostnameVerifier");
            var AllHostnameVerifier = Java.registerClass({
                name: "com.mobilesec.AllHostnameVerifier",
                implements: [HostnameVerifier],
                methods: {
                    verify: function(hostname, session) {
                        console.log("[+] Bypassing HostnameVerifier.verify for hostname: " + hostname);
                        return true;
                    }
                }
            });
            var verifier = AllHostnameVerifier.$new();
            var HttpsURLConnection = Java.use("javax.net.ssl.HttpsURLConnection");
            HttpsURLConnection.setDefaultHostnameVerifier(verifier);
        } catch (e) {
            console.log("[-] HostnameVerifier bypass failed: " + e);
        }

        console.log("[+] SSL Pinning Bypass complete!");
    } catch (e) {
        console.log("[-] Error in SSL Pinning Bypass: " + e);
    }
});
