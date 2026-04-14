FROM kalilinux/kali-rolling:latest

LABEL maintainer="pansinliu <pansinliu@gmail.com>"
LABEL description="Kali Linux based Android Security Testing Environment"

# 环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/platform-tools

# 使用阿里云 HTTP 镜像源（跳过 SSL 验证）
RUN echo "deb http://mirrors.aliyun.com/kali kali-rolling main non-free contrib" > /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/kali kali-rolling main non-free contrib" >> /etc/apt/sources.list

# 基础配置：只安装最核心的系统工具
RUN apt-get update -o Acquire::https::Verify-Peer=false -y && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    unzip \
    python3 \
    python3-pip \
    locales \
    && rm -rf /var/lib/apt/lists/*

# 配置 Python 依赖（使用 --break-system-packages 绕过系统保护）
RUN pip3 install --no-cache-dir --break-system-packages \
    frida-tools \
    objection \
    qark \
    androguard \
    wheel \
    setuptools

# 创建 Frida Server 目录
RUN mkdir -p /usr/local/frida-server

# 创建工作目录
RUN mkdir -p /workspace
WORKDIR /workspace

# 设置中文支持
RUN sed -i '/zh_CN.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

ENV LANG=zh_CN.UTF-8
ENV LANGUAGE=zh_CN:zh
ENV LC_ALL=zh_CN.UTF-8

# 容器启动命令
CMD ["/bin/bash"]
