@echo off
echo ==========================================
echo    POS AI Backend - Windows Launcher
echo ==========================================

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt > nul 2>&1

REM Check MongoDB
echo Checking MongoDB...
mongosh --eval "db.version()" > nul 2>&1
if errorlevel 1 (
    echo WARNING: MongoDB tidak terdeteksi!
    echo Pastikan MongoDB sudah diinstall dan jalan.
    echo Download: https://www.mongodb.com/try/download/community
    pause
)

REM Check Redis
echo Checking Redis...
redis-cli ping > nul 2>&1
if errorlevel 1 (
    echo WARNING: Redis tidak terdeteksi!
    echo Pastikan Redis sudah diinstall dan jalan.
    echo Download: https://github.com/microsoftarchive/redis/releases
    pause
)

REM Create .env if not exists
if not exist ".env" (
    echo Creating .env file...
    (
        echo SECRET_KEY=windows-dev-secret-key
        echo JWT_SECRET_KEY=windows-jwt-secret-key
        echo FLASK_ENV=development
        echo FLASK_DEBUG=True
        echo MONGO_URI=mongodb://localhost:27017/pos_ai_db
        echo REDIS_URL=redis://localhost:6379/0
        echo CELERY_BROKER_URL=redis://localhost:6379/0
        echo CELERY_RESULT_BACKEND=redis://localhost:6379/0
        echo AI_MODE=offline
    ) > .env
)

echo.
echo ==========================================
echo    Starting POS AI Backend...
echo    API: http://localhost:5000
echo    Press CTRL+C to stop
echo ==========================================
echo.

python app.py

pause
