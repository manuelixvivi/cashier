@echo off
REM Windows Setup Script for POS AI Backend

echo === POS AI Backend Windows Setup ===

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.11+ first.
    exit /b 1
)

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Create .env file
echo SECRET_KEY=windows-dev-key > .env
echo JWT_SECRET_KEY=windows-jwt-key >> .env
echo FLASK_ENV=development >> .env
echo MONGO_URI=mongodb://localhost:27017/pos_ai_db >> .env
echo AI_MODE=offline >> .env

echo === Setup Complete ===
echo Run: python app.py
echo Or: venv\Scripts\python.exe app.py

pause
