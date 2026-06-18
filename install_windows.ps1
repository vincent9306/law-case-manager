# 个人案件管理系统 v1.2.0 - Windows 安装脚本
# 使用方法：右键点击此文件，选择"使用 PowerShell 运行"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  个人案件管理系统 - Windows 安装程序" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python 是否安装
Write-Host "【步骤 1/5】检查 Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python 已安装：$pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未检测到 Python" -ForegroundColor Red
    Write-Host "📥 请先安装 Python：" -ForegroundColor Yellow
    Write-Host "   1. 访问 https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "   2. 下载最新版 Python" -ForegroundColor Yellow
    Write-Host "   3. 安装时勾选 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# 安装 Python 依赖
Write-Host ""
Write-Host "【步骤 2/5】安装 Python 依赖包..." -ForegroundColor Yellow
Write-Host "📦 正在安装 Flask, PyPDF2, openpyxl, python-docx..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Write-Host "✅ Python 依赖安装完成" -ForegroundColor Green

# 创建必要目录
Write-Host ""
Write-Host "【步骤 3/5】创建数据目录..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "data\uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
Write-Host "✅ 目录创建完成" -ForegroundColor Green

# 初始化数据库
Write-Host ""
Write-Host "【步骤 4/5】初始化数据库..." -ForegroundColor Yellow
$initScript = @"
import sqlite3
import os

db_path = 'data/cases.db'
os.makedirs('data', exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 创建所有表
cursor.execute('''
CREATE TABLE IF NOT EXISTS cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_number TEXT,
    case_name TEXT NOT NULL,
    case_type TEXT,
    court TEXT,
    judge TEXT,
    status TEXT DEFAULT '一审进行中',
    client_name TEXT,
    client_contact TEXT,
    create_date TEXT,
    opposing_party TEXT,
    fee_amount REAL,
    fee_status TEXT DEFAULT '未收费',
    invoice_status TEXT DEFAULT '未开票',
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT DEFAULT '个人',
    phone TEXT,
    email TEXT,
    id_number TEXT,
    address TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS case_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER,
    doc_type TEXT DEFAULT '文档',
    category TEXT DEFAULT '',
    file_name TEXT,
    file_path TEXT,
    file_size INTEGER,
    folder_path TEXT DEFAULT '',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS work_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER,
    work_date TEXT,
    work_content TEXT,
    work_hours REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS todo_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER,
    source_doc_id INTEGER,
    title TEXT NOT NULL,
    due_date TEXT,
    status TEXT DEFAULT '待办',
    priority TEXT DEFAULT '中',
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS case_followups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER,
    followup_date TEXT,
    followup_content TEXT,
    next_action TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS doc_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    content TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS timeline_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER,
    source_doc_id INTEGER,
    event_date TEXT,
    event_type TEXT,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print('✅ 数据库初始化完成')
"@

$initScript | Out-File -FilePath "init_db.py" -Encoding UTF8
python init_db.py
Remove-Item "init_db.py" -Force
Write-Host "✅ 数据库初始化完成" -ForegroundColor Green

# 创建启动脚本
Write-Host ""
Write-Host "【步骤 5/5】创建启动脚本..." -ForegroundColor Yellow
$startBatContent = @"
@echo off
chcp 65001 > nul
echo 正在启动个人案件管理系统...
echo.
python app.py
pause
"@
$startBatContent | Out-File -FilePath "start.bat" -Encoding UTF8
Write-Host "✅ 启动脚本创建完成" -ForegroundColor Green

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  ✅ 安装完成！" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 启动方法：" -ForegroundColor Yellow
Write-Host "   双击 start.bat" -ForegroundColor White
Write-Host ""
Write-Host "🌐 然后在浏览器中访问：" -ForegroundColor Yellow
Write-Host "   http://127.0.0.1:5066" -ForegroundColor White
Write-Host ""
Write-Host "💡 提示：" -ForegroundColor Yellow
Write-Host "   - 数据存储在 data/cases.db" -ForegroundColor White
Write-Host "   - 上传的文件存储在 data/uploads/" -ForegroundColor White
Write-Host ""
pause
