#!/bin/bash

# 个人案件管理系统 v1.2.0 - Mac 安装脚本
# 使用方法：bash install_mac.sh
# 通过 WorkBuddy 安装：WorkBuddy 会自动运行此脚本

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "========================================="
echo "  个人案件管理系统 v1.1.0 - Mac 安装程序"
echo "========================================="
echo ""
echo "安装目录：$PROJECT_DIR"
echo ""

# ─── 步骤 1：检查 Homebrew ───
echo "【步骤 1/6】检查 Homebrew..."
if ! command -v brew &> /dev/null; then
    echo "  未检测到 Homebrew，正在安装..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # 将 Homebrew 添加到 PATH（Apple Silicon / Intel 兼容）
    if [ -f /opt/homebrew/bin/brew ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [ -f /usr/local/bin/brew ]; then
        eval "$(/usr/local/bin/brew shellenv)"
    fi
    echo "  ✅ Homebrew 安装完成"
else
    echo "  ✅ Homebrew 已安装"
fi

# ─── 步骤 2：检查 Python 3 ───
echo ""
echo "【步骤 2/6】检查 Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "  未检测到 Python 3，正在安装..."
    brew install python3
    echo "  ✅ Python 3 安装完成"
else
    PYVER=$(python3 --version 2>&1)
    echo "  ✅ $PYVER"
fi

# ─── 步骤 3：安装 Python 依赖 ───
echo ""
echo "【步骤 3/5】安装 Python 依赖包..."
python3 -m pip install --upgrade pip --quiet 2>/dev/null || true
python3 -m pip install -r requirements.txt --quiet
echo "  ✅ Python 依赖安装完成"

# ─── 步骤 4：创建数据目录 ───
echo ""
echo "【步骤 4/5】创建数据目录..."
mkdir -p data/uploads
mkdir -p logs
echo "  ✅ 目录创建完成"

# ─── 步骤 5：设置权限 ───
echo ""
echo "【步骤 5/5】设置启动权限..."
chmod +x start.sh
echo "  ✅ 权限设置完成"

echo ""
echo "========================================="
echo "  ✅ 安装完成！"
echo "========================================="
echo ""
echo "📱 启动方法："
echo "   bash start.sh"
echo ""
echo "🌐 访问地址："
echo "   http://127.0.0.1:66"
echo ""
echo "💡 提示："
echo "   - 首次访问会自动创建数据库"
echo "   - 数据存储在 data/cases.db"
echo "   - 上传的文件存储在 data/uploads/"
echo "   - 按 Ctrl+C 停止服务器"
echo ""
