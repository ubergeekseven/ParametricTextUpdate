@echo off
setlocal enabledelayedexpansion

echo CombineCut Fusion 360 Add-in Installer
echo ======================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
) else (
    python3 --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=python3
    ) else (
        echo Python is not installed or not in PATH.
        echo.
        echo Please install Python 3.6 or later from https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH" during installation.
        echo.
        echo After installing Python, run this installer again.
        echo.
        pause
        exit /b 1
    )
)

:: Check if install.py exists
if not exist "install.py" (
    echo Error: install.py not found!
    echo Please make sure you extracted all files from the ZIP archive.
    echo.
    pause
    exit /b 1
)

:: Run the Python installer
echo Running installer...
echo.
%PYTHON_CMD% install.py

:: If Python script failed, show error
if %errorlevel% neq 0 (
    echo.
    echo Installation failed. Please try the manual installation method.
    echo.
    pause
    exit /b 1
)

exit /b 0 