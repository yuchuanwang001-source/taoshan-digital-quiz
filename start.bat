@echo off
chcp 65001 >nul
title 淘宝闪购数智经营 — 刷题系统

echo.
echo ╔══════════════════════════════════════════════╗
echo ║   淘宝闪购数智经营生态 · 基础知识刷题        ║
echo ║   正在启动本地服务器（含钉钉代理）...        ║
echo ╚══════════════════════════════════════════════╝
echo.

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] 检测到 Python，启动代理服务器...
    echo.
    echo 请在浏览器中打开：http://localhost:8000
    echo 钉钉回传将通过本地代理自动转发
    echo 按 Ctrl+C 可停止服务器
    echo.
    start "" http://localhost:8000
    cd /d "%~dp0"
    python server.py
    goto :end
)

echo [ERROR] 未检测到 Python，请先安装 Python 3
echo 下载地址：https://www.python.org/downloads/
echo.
pause
goto :end

:end
