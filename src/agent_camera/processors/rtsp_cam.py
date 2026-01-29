"""Module xử lý camera qua RTSP sử dụng OpenCV.

Cung cấp lớp `RtspCameraProcessor` và bảng cấu hình `RtspCameraConfigPanel`.
"""

from __future__ import annotations

import cv2
import numpy as np
from typing import Optional, Any
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QWidget,
)

from .base import Processor, ConfigPanel, CamSettings
from .worker import Worker


class RtspCameraProcessor(Processor):
    """
    Processor cho RTSP camera dùng OpenCV.
    """

    name = "RTSPCamera"
    frame_ready = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self.settings: CamSettings = CamSettings()
        self._panel = RtspCameraConfigPanel()
        self._worker: Optional[Worker] = None
        self._cap: Optional[cv2.VideoCapture] = None
        self.is_open: bool = False

        # Wiring
        self.triggerSignal.connect(self.trigger_once)
        self._panel.settings_changed.connect(self.configure)
        self._panel.btn_toggle_connect.clicked.connect(
            self._on_toggle_connection_clicked
        )

    def _on_toggle_connection_clicked(self) -> None:
        if self.is_open:
            self.disconnect_camera()
        else:
            self.connect_camera()
        self._panel.ui_update(self.is_open)

    def configure(self, s: CamSettings) -> None:
        self.settings = s or CamSettings()

    def connect_camera(self) -> bool:
        url = self._panel.url
        if not url:
            self._panel.show_error("Chưa nhập link RTSP.")
            return False

        self.disconnect_camera()

        try:
            # Thiết lập tham số FFMPEG cho OpenCV để tối ưu RTSP (giảm delay, dùng UDP)
            import os
            os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
            
            print(f"   -> Đang kết nối tới RTSP: {url}")
            cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            
            if not cap or not cap.isOpened():
                # Thử lại không có tham số FFMPEG nếu lỗi
                cap = cv2.VideoCapture(url)
                if not cap or not cap.isOpened():
                    raise ConnectionError(f"Không thể mở luồng RTSP: {url}")

            # Đặt buffer size nhỏ để giảm độ trễ
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            self._cap = cap
            self._worker = Worker(self)
            self._worker.frame_ready.connect(
                self.__on_frame, Qt.ConnectionType.UniqueConnection
            )
            self._worker.start()

            self.is_open = True
            print("   ✓ Kết nối RTSP thành công")
            return True

        except Exception as e:
            print(f"❌ Lỗi kết nối RTSP: {e}")
            self._panel.show_error(str(e))
            self.is_open = False
            return False


    def disconnect_camera(self) -> bool:
        if self._worker:
            self._worker.stop()
            self._worker = None
        if self._cap:
            self._cap.release()
            self._cap = None
        self.is_open = False
        return True

    def get_frame(self) -> Optional[np.ndarray]:
        if not self._cap:
            return None
        
        ok, frame = self._cap.read()
        if not ok or frame is None:
            return None
            
        return frame

    def trigger_once(self) -> None:
        pass

    def __on_frame(self, frame: np.ndarray) -> None:
        self.frame_ready.emit(frame)

    @property
    def panel(self) -> ConfigPanel:
        return self._panel


class RtspCameraConfigPanel(ConfigPanel):
    """
    Panel điều khiển cho RTSP Camera.
    """

    settings_changed = Signal(CamSettings)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_simple_ui()

    def _setup_simple_ui(self):
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Link RTSP:"))
        self.le_url = QLineEdit()
        self.le_url.setPlaceholderText("rtsp://admin:password@192.168.1.100:554/stream")
        layout.addWidget(self.le_url)
        
        self.btn_toggle_connect = QPushButton("Kết nối")
        layout.addWidget(self.btn_toggle_connect)
        
        layout.addStretch()
        
        self.le_url.textChanged.connect(lambda: self.settings_changed.emit(self.dump_settings()))

    @property
    def url(self) -> str:
        return self.le_url.text().strip()

    def dump_settings(self) -> CamSettings:
        return CamSettings(dev=self.url)

    def load_settings(self, s: CamSettings) -> None:
        if s and s.dev:
            self.le_url.setText(s.dev)

    def ui_update(self, connected: bool) -> None:
        self.btn_toggle_connect.setText("Ngắt kết nối" if connected else "Kết nối")
        self.le_url.setEnabled(not connected)

    def show_error(self, msg: str) -> None:
        QMessageBox.critical(self, "Lỗi RTSP", msg)
