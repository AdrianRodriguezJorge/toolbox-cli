@echo off
title Toolbox CLI - Uninstallation Script
@echo off
cls

rem Ensure Python is available
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python was not detected on your system.
    echo Please install Python 3.8+ and check "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

rem Delegate to the Python uninstaller which respects language settings
python "%~dp0toolbox_cli\uninstall_deps.py"
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Uninstallation failed.
    echo.
    pause
    exit /b 1
)

pause