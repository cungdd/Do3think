"""
Module triển khai điều khiển Camera Hikvision (GigE/USB) thông qua SDK MVS.

Cung cấp các lớp chuyên biệt để quản lý vòng đời kết nối, cấu hình các tham số
đặc thù của dòng camera công nghiệp Hikvision và giao diện điều khiển tương ứng.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from .base import Processor, ConfigPanel, CamSettings


class HikCameraProcessor(Processor):
    """
    Bộ xử lý trung tâm cho Camera Hikvision.

    Lớp này chịu trách nhiệm đóng gói (wrapper) các hàm gọi từ SDK Hikvision (thường là MvImport).
    Nó quản lý việc mở thiết bị bằng IP hoặc Serial Number, cấu hình thanh ghi (registers)
    của camera và thu nhận luồng ảnh thô.

    Attributes:
        name (str): Tên định danh "Hikcamera".
        frame_ready (Signal): Phát ra dữ liệu hình ảnh (numpy.ndarray) nhận được từ SDK.
    """

    name = "Hikcamera"
    frame_ready = Signal(object)

    def __init__(self):
        super().__init__()
        self._panel = HikCameraConfigPanel()

    @property
    def panel(self) -> ConfigPanel:
        return self._panel

    def connect_camera(self) -> bool:
        return False

    def disconnect_camera(self) -> bool:
        return True

    def trigger_once(self) -> None:
        pass

    # Lưu ý: Các phương thức như connect_camera, get_frame cần được implement
    # dựa trên thư viện MvImport của Hikvision.


class HikCameraConfigPanel(ConfigPanel):
    """
    Bảng điều khiển giao diện dành riêng cho cấu hình Camera Hikvision.

    Hỗ trợ các tính năng đặc thù của dòng camera GigE/Industrial như:
    - Quét thiết bị trong mạng nội bộ (GigE Enumeration).
    - Cấu hình các tham số phơi sáng, Gain, Gamma theo chuẩn GenICam.
    - Quản lý chế độ kích hoạt bằng phần mềm (Software Trigger) hoặc phần cứng (Hard Trigger).

    Attributes:
        settings_changed (Signal): Phát đi tín hiệu kèm đối tượng CamSettings mỗi khi
            người dùng thay đổi thông số trên giao diện (Exposure, IP, v.v.).
    """

    # Phát khi có bất kỳ thay đổi nào về thông số cấu hình trên giao diện
    settings_changed = Signal(CamSettings)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Nếu chưa có UI thực, tạo một label đơn giản
        from PySide6.QtWidgets import QVBoxLayout, QLabel
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Hikvision Camera Panel (Chưa có Driver SDK)"))
        
    def dump_settings(self) -> CamSettings:
        return CamSettings()

    def load_settings(self, s: CamSettings) -> None:
        pass

    def ui_update(self, connected: bool) -> None:
        pass
