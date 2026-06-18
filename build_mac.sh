#!/bin/bash
# 个人案件管理系统 - macOS 一键打包脚本
# 使用方法：bash build_mac.sh

set -e

echo ""
echo "=========================================="
echo "  案件管理系统 - macOS 一键打包"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# ─── 步骤 1：检查 Python 3 ───
echo "[步骤 1/5] 检查 Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python 3，请先安装 Python 3.10+"
    echo "下载地址: https://www.python.org/downloads/"
    exit 1
fi
python3 --version
echo ""

# ─── 步骤 2：安装依赖 ───
echo "[步骤 2/5] 安装 Python 依赖..."
python3 -m pip install pyinstaller flask werkzeug python-docx PyPDF2 openpyxl --quiet 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[提示] pip install 失败，尝试使用 --break-system-packages..."
    python3 -m pip install --break-system-packages pyinstaller flask werkzeug python-docx PyPDF2 openpyxl --quiet
fi
echo "[完成] 依赖安装完成"
echo ""

# ─── 步骤 3：创建数据目录 ───
echo "[步骤 3/5] 创建目录..."
mkdir -p data/uploads
echo "[完成] 目录创建完成"
echo ""

# ─── 步骤 4：PyInstaller 打包 ───
echo "[步骤 4/5] 正在打包（首次打包需要几分钟）..."
rm -rf build dist 2>/dev/null || true

# 设置 PyInstaller 缓存目录到本地，避免 macOS 沙箱权限问题
export PYINSTALLER_CONFIG_DIR="$(pwd)/build/pyinstaller-config"
mkdir -p "$PYINSTALLER_CONFIG_DIR"

pyinstaller law-case-manager.spec --clean --noconfirm 2>&1 | tail -5

if [ ! -f "dist/案件管理系统/案件管理系统" ]; then
    echo ""
    echo "[错误] 打包失败！可执行文件未生成"
    echo "常见问题："
    echo "1. Python 版本过旧 - 需要 Python 3.10+"
    echo "2. 路径包含特殊字符"
    echo "3. 依赖安装不完整"
    exit 1
fi

echo "[完成] 打包完成"
echo ""

# ─── 步骤 5：复制附加文件 ───
echo "[步骤 5/5] 复制附加文件..."
cp 启动.command "dist/案件管理系统/" 2>/dev/null || true
chmod +x "dist/案件管理系统/启动.command" 2>/dev/null || true
chmod +x "dist/案件管理系统/案件管理系统" 2>/dev/null || true
cp USAGE.md "dist/案件管理系统/使用说明.md" 2>/dev/null || true
cp README.md "dist/案件管理系统/README.md" 2>/dev/null || true
echo "[完成] 附加文件复制完成"
echo ""

# ─── 输出结果 ───
echo "=========================================="
echo "  打包成功！"
echo "=========================================="
echo ""
echo "  输出目录: $(pwd)/dist/案件管理系统"
echo ""
echo "  文件清单："
ls -la "dist/案件管理系统/"
echo ""
echo "  ──────────────────────────────"
echo "  使用方法："
echo "  1. 将"案件管理系统"文件夹拖到"应用程序"或任意位置"
echo "  2. 双击"启动.command"即可运行"
echo "  3. 浏览器会自动打开 http://127.0.0.1:5066"
echo ""
echo "  首次双击 .command 文件可能需要右键 → 打开"
echo "  来绕过 macOS Gatekeeper 安全限制"
echo "  ──────────────────────────────"
echo ""
echo "  如需分发给其他人，将整个文件夹压缩成 zip 即可"
echo "  注意：macOS 下首次运行可能会被 Gatekeeper 拦截，"
echo "  接收方需要在"系统设置 → 隐私与安全性"中允许"
echo ""
