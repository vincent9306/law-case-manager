#!/bin/bash
# 个人案件管理系统 - macOS 启动脚本
# 双击此文件或在终端运行：bash 启动.command

# 获取脚本所在目录
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

# 创建数据目录
mkdir -p data/uploads

# 检查端口占用
PORT=5066
PID=$(lsof -ti:$PORT 2>/dev/null)
if [ -n "$PID" ]; then
    echo "⚠️  端口 $PORT 被占用（PID: $PID），正在释放..."
    kill -9 $PID 2>/dev/null
    sleep 1
fi

echo ""
echo "=========================================="
echo "  个人案件管理系统"
echo "  Developed by Yizhen Li"
echo "  Beijing Dacheng Law Offices, LLP (Wuxi)"
echo "  Open Source Version 1.0"
echo "=========================================="
echo ""
echo "  正在启动服务..."
echo "  请勿关闭此窗口"
echo ""
echo "  浏览器将自动打开"
echo "  如未自动打开，请访问：http://127.0.0.1:5066"
echo ""
echo "  按 Ctrl+C 停止服务"
echo "=========================================="
echo ""

# 启动程序
./案件管理系统
