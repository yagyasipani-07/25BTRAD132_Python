@echo off
title HWGuard
cd /d "%~dp0system"

:: Launch without console window
where pythonw >nul 2>&1
if %errorlevel% equ 0 (
    start "" pythonw "%~dp0system\hwguard.py"
    exit
)

if exist "%LOCALAPPDATA%\Programs\Python\Python314\pythonw.exe" (
    start "" "%LOCALAPPDATA%\Programs\Python\Python314\pythonw.exe" "%~dp0system\hwguard.py"
    exit
)
if exist "%LOCALAPPDATA%\Programs\Python\Python312\pythonw.exe" (
    start "" "%LOCALAPPDATA%\Programs\Python\Python312\pythonw.exe" "%~dp0system\hwguard.py"
    exit
)

where pyw >nul 2>&1
if %errorlevel% equ 0 (
    start "" pyw "%~dp0system\hwguard.py"
    exit
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    start "" python "%~dp0system\hwguard.py"
    exit
)

echo [ERROR] Python runtime not found.
pause
