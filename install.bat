@echo off
title Toolbox CLI Installer
cls

echo ======================================================================
echo             TOOLBOX CLI INSTALLER (Command 'tb')
echo ======================================================================

rem 1. Check if Python is installed
set "PYTHON_CMD=python"
where python >nul 2>nul
if %errorlevel% equ 0 goto :run_installer

rem Try to auto-detect Python in local AppData
set "FOUND_PYTHON="
for /d %%d in ("%LocalAppData%\Programs\Python\Python*") do (
    if exist "%%d\python.exe" (
        set "FOUND_PYTHON=%%d\python.exe"
    )
)

if not defined FOUND_PYTHON (
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

set "PYTHON_CMD=%FOUND_PYTHON%"

:run_installer
rem 2. Run installer (language, dependencies, PATH, success message)
"%PYTHON_CMD%" "%~dp0toolbox_cli\install_deps.py"
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed. / La instalacion fallo.
    echo.
    pause
    exit /b
)

pause
