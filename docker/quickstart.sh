#!/bin/bash
# APK 安全测试实验室 - 快速启动脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "  APK 安全测试实验室 - 快速启动"
echo "=========================================="
echo ""

cd "$SCRIPT_DIR"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker 未安装${NC}"
    echo "请先安装 Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}错误: Docker Compose 未安装${NC}"
    echo "请先安装 Docker Compose"
    exit 1
fi

echo -e "${GREEN}[✓] Docker 和 Docker Compose 已安装${NC}"
echo ""

# 主菜单
show_menu() {
    echo "请选择操作:"
    echo "  1) 构建所有镜像"
    echo "  2) 启动所有服务"
    echo "  3) 停止所有服务"
    echo "  4) 查看服务状态"
    echo "  5) 查看日志"
    echo "  6) 进入 Kali 容器"
    echo "  7) 清理所有数据 (危险!)"
    echo "  0) 退出"
    echo ""
    read -p "请输入选项 [0-7]: " choice
}

build_images() {
    echo ""
    echo "=========================================="
    echo "  构建 Docker 镜像"
    echo "=========================================="
    echo ""
    echo "这可能需要一些时间，请耐心等待..."
    echo ""

    # 先构建基础镜像
    echo -e "${YELLOW}[1/3] 构建 Kali 基础镜像...${NC}"
    docker build -t mobilesec/kali-base:latest ./kali-base

    # 构建其他镜像
    echo -e "${YELLOW}[2/3] 构建 MobSF 镜像...${NC}"
    docker build -t mobilesec/mobsf:latest ./mobsf

    echo -e "${YELLOW}[3/3] 构建 Frida 镜像...${NC}"
    docker build -t mobilesec/frida:latest ./frida

    echo ""
    echo -e "${GREEN}[✓] 所有镜像构建完成!${NC}"
}

start_services() {
    echo ""
    echo "=========================================="
    echo "  启动服务"
    echo "=========================================="
    echo ""

    if docker compose version &> /dev/null; then
        docker compose up -d
    else
        docker-compose up -d
    fi

    echo ""
    echo -e "${GREEN}[✓] 服务已启动!${NC}"
    echo ""
    echo "访问地址:"
    echo "  MobSF: http://localhost:9000"
    echo ""
    echo "使用命令:"
    echo "  进入 Kali: docker exec -it mobilesec-kali bash"
    echo "  进入 Frida: docker exec -it mobilesec-frida bash"
}

stop_services() {
    echo ""
    echo "=========================================="
    echo "  停止服务"
    echo "=========================================="
    echo ""

    if docker compose version &> /dev/null; then
        docker compose stop
    else
        docker-compose stop
    fi

    echo ""
    echo -e "${GREEN}[✓] 服务已停止${NC}"
}

show_status() {
    echo ""
    echo "=========================================="
    echo "  服务状态"
    echo "=========================================="
    echo ""

    if docker compose version &> /dev/null; then
        docker compose ps
    else
        docker-compose ps
    fi
}

show_logs() {
    echo ""
    echo "=========================================="
    echo "  服务日志 (Ctrl+C 退出)"
    echo "=========================================="
    echo ""

    if docker compose version &> /dev/null; then
        docker compose logs -f
    else
        docker-compose logs -f
    fi
}

enter_kali() {
    echo ""
    echo "进入 Kali 容器..."
    echo ""
    docker exec -it mobilesec-kali bash || true
}

cleanup() {
    echo ""
    echo -e "${RED}==========================================${NC}"
    echo -e "${RED}  警告: 此操作将删除所有数据!${NC}"
    echo -e "${RED}==========================================${NC}"
    echo ""
    read -p "确认要继续吗? (输入 'yes' 确认): " confirm

    if [ "$confirm" = "yes" ]; then
        echo ""
        echo "正在清理..."

        if docker compose version &> /dev/null; then
            docker compose down -v
        else
            docker-compose down -v
        fi

        echo ""
        echo -e "${GREEN}[✓] 清理完成${NC}"
    else
        echo ""
        echo "已取消"
    fi
}

# 主循环
while true; do
    echo ""
    show_menu

    case $choice in
        1)
            build_images
            ;;
        2)
            start_services
            ;;
        3)
            stop_services
            ;;
        4)
            show_status
            ;;
        5)
            show_logs
            ;;
        6)
            enter_kali
            ;;
        7)
            cleanup
            ;;
        0)
            echo ""
            echo "再见!"
            exit 0
            ;;
        *)
            echo ""
            echo -e "${RED}无效选项${NC}"
            ;;
    esac
done
