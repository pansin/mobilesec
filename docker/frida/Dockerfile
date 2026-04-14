FROM mobilesec/kali-base:latest

LABEL maintainer="pansinliu <pansinliu@gmail.com>"
LABEL description="Frida - Dynamic instrumentation toolkit for mobile security testing"

# 创建 Frida Server 目录
RUN mkdir -p /usr/local/frida-server

# 容器启动时自动下载匹配版本的 Frida Server
COPY download-frida.sh /usr/local/frida-server/
RUN chmod +x /usr/local/frida-server/download-frida.sh

# 创建 Frida 脚本目录
RUN mkdir -p /workspace/scripts
COPY scripts/ /workspace/scripts/
RUN chmod +x /workspace/scripts/*.js

# 创建工作目录
WORKDIR /workspace

# 容器启动命令 - 先下载 Frida Server，再启动 bash
ENTRYPOINT ["/bin/bash", "-c", "/usr/local/frida-server/download-frida.sh && exec /bin/bash"]
