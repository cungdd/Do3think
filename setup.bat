@echo off
REM Script cai dat moi truong cho project
REM Created: 2026-01-15

echo ========================================
echo   CAI DAT MOI TRUONG PROJECT
echo ========================================
echo.

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chua duoc cai dat!
    echo Vui long cai dat Python tu https://www.python.org/
    pause
    exit /b 1
)

echo [INFO] Phat hien Python version:
python --version
echo.

REM Tao moi truong ao
echo [INFO] Dang tao moi truong ao (virtual environment)...
if exist "venv" (
    echo [WARNING] Moi truong ao da ton tai!
    set /p choice="Ban co muon xoa va tao lai? (y/n): "
    if /i "%choice%"=="y" (
        echo [INFO] Dang xoa moi truong ao cu...
        rmdir /s /q venv
        python -m venv venv
    ) else (
        echo [INFO] Giu nguyen moi truong ao hien tai
    )
) else (
    python -m venv venv
)

if not exist "venv" (
    echo [ERROR] Tao moi truong ao that bai!
    pause
    exit /b 1
)

echo [INFO] Tao moi truong ao thanh cong!
echo.

REM Kich hoat moi truong ao
echo [INFO] Dang kich hoat moi truong ao...
call venv\Scripts\activate.bat

REM Nang cap pip
echo [INFO] Dang nang cap pip...
python -m pip install --upgrade pip

REM Cai dat dependencies
echo.
echo [INFO] Dang cai dat cac thu vien can thiet...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo [WARNING] Khong tim thay requirements.txt
    echo [INFO] Cai dat cac package co ban...
    pip install PySide6 pytest pytest-qt pytest-cov
)

if errorlevel 1 (
    echo [ERROR] Cai dat dependencies that bai!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   CAI DAT HOAN TAT!
echo ========================================
echo.
echo [INFO] Ban co the chay ung dung bang cach:
echo   1. Double-click file run.bat
echo   2. Hoac mo terminal va chay: venv\Scripts\activate ^&^& python -m src.communicate.protocol_main
echo.
echo [INFO] De chay test: pytest
echo.
pause
