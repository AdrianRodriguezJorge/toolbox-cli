@echo off
title Toolbox CLI - Uninstallation Script
@echo off
cls

rem Ensure Python is available
set "PYTHON_CMD=python"
where python >nul 2>nul
if %errorlevel% equ 0 goto :run_uninstaller

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
    pause
    exit /b 1
)

set "PYTHON_CMD=%FOUND_PYTHON%"

:run_uninstaller
rem Delegate to the Python uninstaller which respects language settings
"%PYTHON_CMD%" "%~dp0toolbox_cli\uninstall_deps.py"
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Uninstallation failed.
    echo.
    pause
    exit /b 1
)

pause