@echo off
REM Script chay ung dung Protocol Manager
REM Created: 2026-01-15

echo ========================================
echo   Protocol Manager Application
echo ========================================
echo.

REM Kiem tra Python co duoc cai dat khong
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chua duoc cai dat!
    echo Vui long cai dat Python tu https://www.python.org/
    pause
    exit /b 1
)

echo [INFO] Kiem tra Python: OK
echo.

REM Kiem tra va kich hoat moi truong ao
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Phat hien moi truong ao, dang kich hoat...
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] Khong tim thay moi truong ao
    echo [INFO] Chay voi Python toan cuc...
)

echo.
echo [INFO] Kiem tra dependencies...
python -c "import PySide6" 2>nul
if errorlevel 1 (
    echo [WARNING] PySide6 chua duoc cai dat!
    echo [INFO] Dang cai dat dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Cai dat that bai!
        pause
        exit /b 1
    )
)

echo [INFO] Dependencies: OK
echo.
echo [INFO] Dang khoi dong ung dung...
echo ========================================
echo.

REM Chay ung dung chinh
python main.py

REM Kiem tra exit code
if errorlevel 1 (
    echo.
    echo [ERROR] Ung dung bi loi!
    pause
    exit /b 1
)

echo.
echo [INFO] Ung dung da dong.
pause
