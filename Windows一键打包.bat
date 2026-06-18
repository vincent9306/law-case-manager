@echo off
chcp 65001 >nul
title 案件管理系统 - Windows 一键打包

echo.
echo ==========================================
echo   案件管理系统 - Windows 一键打包
echo ==========================================
echo.

:: 检查 Python
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.10+
    echo 下载地址: https://www.python.org/downloads/
    echo 安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)

echo [检查] Python 版本：
python --version
echo.

:: 安装依赖
echo [步骤 1/4] 安装 Python 依赖...
pip install pyinstaller flask werkzeug python-docx PyPDF2 openpyxl --quiet
if %ERRORLEVEL% neq 0 (
    echo [错误] 依赖安装失败，请检查网络连接
    pause
    exit /b 1
)
echo [完成] 依赖安装完成
echo.

:: 切换到脚本所在目录
cd /d "%~dp0"

:: 创建数据目录（打包后也会创建，这里提前建好）
echo [步骤 2/4] 创建目录...
if not exist "data\uploads" mkdir "data\uploads"
echo [完成] 目录创建完成
echo.

:: 打包
echo [步骤 3/4] 正在打包（首次打包需要几分钟）...

:: 设置 PyInstaller 缓存目录到本地（避免权限问题）
set PYINSTALLER_CONFIG_DIR=%cd%\build\pyinstaller-config
if not exist "%PYINSTALLER_CONFIG_DIR%" mkdir "%PYINSTALLER_CONFIG_DIR%"

pyinstaller law-case-manager.spec --clean --noconfirm

if %ERRORLEVEL% neq 0 (
    echo.
    echo [错误] 打包失败！
    echo 常见问题：
    echo 1. 杀毒软件拦截 - 请暂时关闭 Windows Defender
    echo 2. 路径包含中文 - 请将项目放到纯英文路径
    echo 3. Python 版本过旧 - 需要 Python 3.10+
    pause
    exit /b 1
)
echo [完成] 打包完成
echo.

:: 复制启动脚本和说明文件
echo [步骤 4/4] 复制附加文件...
copy /y "启动.bat" "dist\案件管理系统\" >nul 2>&1
copy /y "USAGE.md" "dist\案件管理系统\使用说明.md" >nul 2>&1
copy /y "README.md" "dist\案件管理系统\README.md" >nul 2>&1
echo [完成] 附加文件复制完成
echo.

:: 检查输出
if exist "dist\案件管理系统\案件管理系统.exe" (
    for %%A in ("dist\案件管理系统") do (
        echo ==========================================
        echo   打包成功！
        echo ==========================================
        echo.
        echo   输出目录: %%~fA
        echo.
        echo   文件清单：
        dir /b "dist\案件管理系统"
        echo.
        echo   ──────────────────────────────
        echo   使用方法：
        echo   1. 将"案件管理系统"整个文件夹复制到任意位置
        echo   2. 双击 "启动.bat" 即可运行
        echo   3. 浏览器会自动打开 http://127.0.0.1:5066
        echo   ──────────────────────────────
        echo.
        echo   如需分发给其他人，将整个文件夹打包成 zip 即可
        echo.
    )
) else (
    echo [警告] 未找到可执行文件，打包可能部分失败
    dir "dist" /s /b 2>nul
)

pause
