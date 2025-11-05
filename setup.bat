@echo off
REM Setup script for Google Ads Search Terms Analyzer (Windows)
REM This script creates a virtual environment and installs all dependencies

echo ================================================
echo Google Ads Search Terms Analyzer - Setup
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher and try again.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Found Python %PYTHON_VERSION%

REM Create virtual environment
set VENV_DIR=venv

if exist "%VENV_DIR%" (
    echo [WARNING] Virtual environment already exists at .\%VENV_DIR%
    set /p RECREATE="Do you want to recreate it? (y/N): "
    if /i "%RECREATE%"=="y" (
        echo Removing existing virtual environment...
        rmdir /s /q "%VENV_DIR%"
    ) else (
        echo Using existing virtual environment.
        goto :skip_create
    )
)

echo Creating virtual environment...
python -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)
echo [OK] Virtual environment created at .\%VENV_DIR%

:skip_create

REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip upgraded to latest version

REM Install requirements
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo [OK] All dependencies installed successfully

REM Check if google-ads.yaml exists
if not exist "google-ads.yaml" (
    echo.
    echo [WARNING] Configuration file not found
    echo You need to create a google-ads.yaml file with your credentials.
    echo.
    set /p COPY_CONFIG="Do you want to copy the example file now? (y/N): "
    if /i "!COPY_CONFIG!"=="y" (
        copy google-ads.yaml.example google-ads.yaml >nul
        echo [OK] Created google-ads.yaml from example
        echo [WARNING] Please edit google-ads.yaml and add your credentials.
    )
)

REM Setup complete
echo.
echo ================================================
echo Setup completed successfully!
echo ================================================
echo.
echo Next steps:
echo.
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Configure your credentials (if not done already):
echo    notepad google-ads.yaml
echo.
echo 3. Run the analyzer:
echo    python search_terms_analyzer.py --customer-id YOUR_CUSTOMER_ID
echo.
echo To deactivate the virtual environment later, just run:
echo    deactivate
echo.
pause
