@echo off
title 个人案件管理系统

:: 切换到可执行文件所在目录
cd /d "%~dp0"

:: 创建数据目录
if not exist "data\uploads" mkdir "data\uploads"

echo.
echo ==========================================
echo   个人案件管理系统
echo   Developed by Yizhen Li
echo   Beijing Dacheng Law Offices, LLP (Wuxi)
echo   Open Source Version 1.0
echo ==========================================
echo.
echo   正在启动服务...
echo   请勿关闭此窗口
echo   浏览器将自动打开
echo.
echo   如未自动打开，请访问：http://127.0.0.1:5066
echo.
echo   按 Ctrl+C 停止服务
echo ==========================================
echo.

:: 启动程序
案件管理系统.exe

pause
