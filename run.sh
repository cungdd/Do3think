#!/bin/bash
# Script chay ung dung Protocol Manager
# Created: 2026-01-15

echo "========================================"
echo "   Protocol Manager Application"
echo "========================================"
echo ""

# Kiem tra Python co duoc cai dat khong
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python chua duoc cai dat!"
    echo "Vui long cai dat Python 3.8 tro len"
    exit 1
fi

echo "[INFO] Kiem tra Python: OK"
echo ""

# Kiem tra va kich hoat moi truong ao
if [ -f "venv/bin/activate" ]; then
    echo "[INFO] Phat hien moi truong ao, dang kich hoat..."
    source venv/bin/activate
else
    echo "[WARNING] Khong tim thay moi truong ao"
    echo "[INFO] Chay voi Python toan cuc..."
fi

echo ""
echo "[INFO] Kiem tra dependencies..."
python3 -c "import PySide6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[WARNING] PySide6 chua duoc cai dat!"
    echo "[INFO] Dang cai dat dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Cai dat that bai!"
        exit 1
    fi
fi

echo "[INFO] Dependencies: OK"
echo ""
echo "[INFO] Dang khoi dong ung dung..."
echo "========================================"
echo ""

# Chay ung dung chinh
python3 main.py

# Kiem tra exit code
if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Ung dung bi loi!"
    exit 1
fi

echo ""
echo "[INFO] Ung dung da dong."
