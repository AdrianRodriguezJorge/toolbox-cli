@echo off
title Toolbox CLI - Uninstallation Script
cls

REM Toolbox CLI - Uninstallation Script
REM This script removes Toolbox CLI from your system PATH and cleans up configuration files.
REM It respects the language preference set during installation.

setlocal enabledelayedexpansion

REM Detect user's home directory for config file
set "CONFIG_FILE=%USERPROFILE%\.toolbox_cli.json"

REM Default language is English
set "LANG=en"

REM Try to read language from config file using PowerShell JSON parsing
if exist "%CONFIG_FILE%" (
    for /f "tokens=*" %%A in ('powershell -Command "(Get-Content '%CONFIG_FILE%' | ConvertFrom-Json).language" 2^>nul') do (
        set "LANG=%%A"
    )
)

REM ============================================================
REM ENGLISH STRINGS
REM ============================================================
if "%LANG%"=="en" (
    set "TITLE=Toolbox CLI - Uninstallation Script"
    set "DIR_MSG=Uninstalling Toolbox CLI from:"
    set "CONFIRM_MSG=Are you sure you want to uninstall Toolbox CLI? (Y/N): "
    set "CANCELLED=Uninstallation cancelled."
    set "REMOVING_PATH=Removing from system PATH..."
    set "PATH_SUCCESS=PATH variable updated successfully."
    set "PATH_NOT_FOUND=Installation folder not found in PATH."
    set "CLEANUP_MSG=Cleaning up configuration files..."
    set "CONFIG_REMOVED=Configuration folder removed:"
    set "CONFIG_NOT_FOUND=No configuration files found."
    set "COMPLETE_TITLE=Uninstallation Complete!"
    set "COMPLETE_MSG=Toolbox CLI has been removed from your system."
    set "COMPLETE_STEPS=To complete the process, please:"
    set "STEP1=  1. Close all terminal windows"
    set "STEP2=  2. Open a NEW terminal window"
    set "STEP3=  3. Verify with: tb (should show 'command not recognized')"
)

REM ============================================================
REM SPANISH STRINGS
REM ============================================================
if "%LANG%"=="es" (
    set "TITLE=Toolbox CLI - Script de Desinstalacion"
    set "DIR_MSG=Desinstalando Toolbox CLI de:"
    set "CONFIRM_MSG=¿Estás seguro de que deseas desinstalar Toolbox CLI? (S/N): "
    set "CANCELLED=Desinstalacion cancelada."
    set "REMOVING_PATH=Eliminando del PATH del sistema..."
    set "PATH_SUCCESS=Variable PATH actualizada correctamente."
    set "PATH_NOT_FOUND=Carpeta de instalacion no encontrada en PATH."
    set "CLEANUP_MSG=Limpiando archivos de configuracion..."
    set "CONFIG_REMOVED=Carpeta de configuracion eliminada:"
    set "CONFIG_NOT_FOUND=No se encontraron archivos de configuracion."
    set "COMPLETE_TITLE=¡Desinstalacion Completada!"
    set "COMPLETE_MSG=Toolbox CLI ha sido eliminado de tu sistema."
    set "COMPLETE_STEPS=Para completar el proceso, por favor:"
    set "STEP1=  1. Cierra todas las ventanas de terminal"
    set "STEP2=  2. Abre una NUEVA ventana de terminal"
    set "STEP3=  3. Verifica con: tb (debería mostrar 'comando no reconocido')"
)

REM ============================================================
REM EXECUTION
REM ============================================================

echo.
echo ======================================================
echo     %TITLE%
echo ======================================================
echo.

REM Get the installation directory
set "SCRIPT_DIR=%~dp0"
set "INSTALL_PATH=%SCRIPT_DIR%"

echo %DIR_MSG%
echo %INSTALL_PATH%
echo.

REM Ask for confirmation (Y/y for English, S/s for Spanish)
set /p CONFIRM="%CONFIRM_MSG%"

if "%LANG%"=="es" (
    if /i not "%CONFIRM%"=="S" (
        echo %CANCELLED%
        pause
        exit /b 0
    )
) else (
    if /i not "%CONFIRM%"=="Y" (
        echo %CANCELLED%
        pause
        exit /b 0
    )
)

echo.
echo %REMOVING_PATH%

REM Remove the installation folder from PATH using PowerShell for safety
powershell -Command "$path = [Environment]::GetEnvironmentVariable('PATH', 'User'); if ($path -like '*%INSTALL_PATH%*') { $newPath = $path -replace [regex]::Escape('%INSTALL_PATH%') + ';?', ''; [Environment]::SetEnvironmentVariable('PATH', $newPath, 'User'); Write-Host '%PATH_SUCCESS%' } else { Write-Host '%PATH_NOT_FOUND%' }"

echo.
echo %CLEANUP_MSG%

REM Remove configuration folder
if exist "%APPDATA%\toolbox-cli" (
    rmdir /s /q "%APPDATA%\toolbox-cli" >nul 2>&1
    echo %CONFIG_REMOVED% %APPDATA%\toolbox-cli
) else (
    echo %CONFIG_NOT_FOUND%
)

REM Remove config file from home directory
if exist "%CONFIG_FILE%" (
    del /q "%CONFIG_FILE%" >nul 2>&1
)

echo.
echo ======================================================
echo     %COMPLETE_TITLE%
echo ======================================================
echo.
echo %COMPLETE_MSG%
echo %COMPLETE_STEPS%
echo %STEP1%
echo %STEP2%
echo %STEP3%
echo.

pause