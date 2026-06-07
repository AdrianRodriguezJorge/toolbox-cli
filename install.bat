@echo off
title Toolbox CLI Installer
cls

echo ======================================================================
echo             TOOLBOX CLI INSTALLER (Command 'tb')
echo ======================================================================

rem 1. Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python was not detected on your system.
    echo Please install Python 3.8+ and check "Add Python to PATH".
    echo.
    echo [ERROR] Python no fue detectado en tu sistema.
    echo Instala Python 3.8+ y marca "Add Python to PATH".
    echo.
    pause
    exit /b
)

rem 2. Run installer (language, dependencies, PATH, success message)
python "%~dp0toolbox_cli\install_deps.py"
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed. / La instalacion fallo.
    echo.
    pause
    exit /b
)

pause
