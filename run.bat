@echo off
REM Helper script to run the analyzer with virtual environment activated
REM Usage: run.bat --customer-id YOUR_CUSTOMER_ID [other options]

REM Check if virtual environment exists
if not exist "venv" (
    echo [ERROR] Virtual environment not found.
    echo Please run setup.bat first to create the environment.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the analyzer with all provided arguments
python search_terms_analyzer.py %*
