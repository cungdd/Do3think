# Module Integration Platform

Ứng dụng tích hợp quản lý Camera, AI Detection (YOLO) và Protocol Communication với giao diện tab thân thiện.

## Tính năng

- **Camera Agent**: Quản lý camera GigE Vision và USB với giao diện trực quan
- **AI Detect Agent**: Phát hiện đối tượng bằng YOLO với hậu xử lý thông minh
- **Protocol Manager**: Quản lý các giao thức truyền thông (TCP Client, MODBUS)
- **Giao diện Tab**: Dễ sử dụng, chuyển đổi nhanh giữa các module
- **Tích hợp luồng dữ liệu**: Camera → AI Detect → Protocol
- **Quản lý cấu hình**: Lưu/tải settings cho tất cả module
- Hệ thống test tự động với pytest

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Windows/Linux/MacOS

## Cài đặt

### 1. Tạo môi trường ảo (khuyến nghị)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cài đặt thủ công (nếu không có requirements.txt)

```bash
pip install PySide6 pytest
```

## Chạy ứng dụng

### Chạy ứng dụng chính (Giao diện Tab)

```bash
python main.py
```

### Chạy test

```bash
# Chạy tất cả test
pytest

# Chạy test cụ thể
pytest test/test_protocol_main.py
pytest test/test_camera.py
pytest test/test_detect.py

# Chạy với output chi tiết
pytest -v

# Chạy với coverage report
pytest --cov=src
```

## Cấu trúc thư mục

```
module/
├── src/                    # Mã nguồn chính
│   ├── agent_camera/      # Module xử lý camera
│   ├── agent_detect/      # Module phát hiện đối tượng
│   ├── communicate/       # Module giao thức truyền thông
│   └── utils/             # Các tiện ích chung
├── test/                   # Mã nguồn test
├── resources/              # Tài nguyên (icons, styles)
│   ├── icons/
│   └── style/
├── runtime/                # Dữ liệu runtime
└── pytest.ini             # Cấu hình pytest
```

## Sử dụng

### Giao diện Tab

Ứng dụng có 4 tab chính:

1. **📷 Camera** - Quản lý kết nối camera (GigE/USB)
2. **🤖 AI Detect** - Cấu hình mô hình YOLO và xem kết quả
3. **📡 Protocol** - Quản lý giao thức truyền thông
4. **⚙️ Settings** - Lưu/tải cấu hình

### Luồng làm việc cơ bản

1. **Tab Camera**: Chọn và kết nối camera
2. **Tab Detect**: Tải mô hình YOLO (.pt file)
3. Camera tự động gửi frame → AI xử lý → Hiển thị kết quả
4. **Tab Protocol**: Cấu hình để gửi kết quả ra ngoài (tùy chọn)

### Thao tác nhanh

- **Ctrl+S**: Lưu cấu hình
- **Ctrl+O**: Tải cấu hình
- **Ctrl+Q**: Thoát ứng dụng
- **Menu View**: Chuyển nhanh giữa các tab

## Ghi chú

- File cấu hình giao thức được lưu tại `runtime/protocol.json`
- Stylesheet mặc định: `resources/style/corporate.qss`
- Có thể thay đổi đường dẫn trong code nếu cần

## Troubleshooting

### Lỗi import PySide6

```bash
pip install --upgrade PySide6
```

### Lỗi Qt platform plugin

Trên Linux, có thể cần cài thêm:
```bash
sudo apt-get install libxcb-xinerama0
```

### Lỗi pytest

Đảm bảo đường dẫn pythonpath đúng:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## Liên hệ & Hỗ trợ

Để báo lỗi hoặc đóng góp, vui lòng tạo issue hoặc pull request.
