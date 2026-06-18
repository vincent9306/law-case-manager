#!/bin/bash

# 个人案件管理系统 v1.2.0 - Mac 启动脚本
# 使用方法：bash start.sh

cd "$(dirname "$0")"

echo "正在启动个人案件管理系统..."
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python 3"
    echo "请先运行 install_mac.sh 安装依赖"
    exit 1
fi

# 检查端口占用，自动清理
PORT=5066
PID=$(lsof -ti:$PORT 2>/dev/null)
if [ -n "$PID" ]; then
    echo "⚠️  端口 $PORT 被占用（PID: $PID），正在停止..."
    kill -9 $PID 2>/dev/null
    sleep 1
fi

# 启动服务器
echo "✅ 正在启动服务器..."
echo "✅ 访问地址：http://127.0.0.1:5066"
echo "✅ 按 Ctrl+C 停止服务器"
echo "========================================="
echo ""

python3 app.py
