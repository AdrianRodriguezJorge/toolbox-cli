@echo off
title Toolbox CLI Installer
cls

echo ======================================================================
echo             TOOLBOX CLI INSTALLER (Command 'tb')
echo ======================================================================
echo.

rem 1. Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python was not detected on your system.
    echo Please install Python version 3.8 or superior and check
    echo the option "Add Python to PATH" during installation.
    echo.
    pause
    exit /b
)

rem 2. Run the dependency checker and language selector
python "%~dp0toolbox_cli\install_deps.py"
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] There was a problem configuring Python dependencies.
    echo.
    pause
    exit /b
)
echo.

rem 3. Register install directory in PATH environment variable
set "TARGET_DIR=%~dp0"
set "TARGET_DIR=%TARGET_DIR:~0,-1%"

echo [INFO] Registering path in your environment variables...
powershell -Command "$path = [Environment]::GetEnvironmentVariable('PATH', 'User'); if (-not ($path -split ';' -contains '%TARGET_DIR%')) { [Environment]::SetEnvironmentVariable('PATH', $path + ';%TARGET_DIR%', 'User'); write-host 'Successfully registered folder in PATH.' } else { write-host 'Folder is already registered in PATH.' }"

echo.
echo +--------------------------------------------------------------------+
echo  * TOOLBOX CLI IS READY TO BE USED *
echo +--------------------------------------------------------------------+
echo.
echo  Usage instructions:
echo    1. Open a NEW terminal (CMD or PowerShell) to refresh PATH.
echo    2. Navigate to the directory containing your files.
echo       Example: cd C:\MyDocuments
echo    3. Type 'tb' and press Enter.
echo.
echo  Note:
echo    Toolbox CLI will automatically scan and process compatible files
echo    in the folder where you execute the command.
echo.
echo ======================================================================
pause
