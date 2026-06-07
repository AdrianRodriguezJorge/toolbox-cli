@echo off
REM Toolbox CLI - Uninstallation Script
REM This script removes Toolbox CLI from your system PATH and cleans up configuration files.

setlocal enabledelayedexpansion

echo.
echo ======================================================
echo     Toolbox CLI - Uninstallation Script
echo ======================================================
echo.

REM Get the installation directory
set "SCRIPT_DIR=%~dp0"
set "INSTALL_PATH=%SCRIPT_DIR%"

echo Uninstalling Toolbox CLI from: %INSTALL_PATH%
echo.

REM Ask for confirmation
set /p CONFIRM="Are you sure you want to uninstall Toolbox CLI? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo Uninstallation cancelled.
    pause
    exit /b 0
)

echo.
echo Removing from system PATH...

REM Remove the installation folder from PATH using PowerShell for safety
powershell -Command "$path = [Environment]::GetEnvironmentVariable('PATH', 'User'); if ($path -like '*%INSTALL_PATH%*') { $newPath = $path -replace [regex]::Escape('%INSTALL_PATH%') + ';?', ''; [Environment]::SetEnvironmentVariable('PATH', $newPath, 'User'); Write-Host 'PATH variable updated successfully.' } else { Write-Host 'Installation folder not found in PATH.' }"

echo.
echo Cleaning up configuration files...

REM Remove configuration folder
if exist "%APPDATA%\toolbox-cli" (
    rmdir /s /q "%APPDATA%\toolbox-cli"
    echo Configuration folder removed: %APPDATA%\toolbox-cli
) else (
    echo No configuration files found.
)

echo.
echo ======================================================
echo     Uninstallation Complete!
echo ======================================================
echo.
echo Toolbox CLI has been removed from your system.
echo To complete the process, please:
echo   1. Close all terminal windows
echo   2. Open a NEW terminal window
echo   3. Verify with: tb (should show 'command not recognized')
echo.

pause
