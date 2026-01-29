# --- file: camera_widget.py (hoặc module chứa BaseCameraWidget) ---
"""
Module cung cấp giao diện quản lý và điều khiển Camera (BaseCameraWidget).

Thiết kế dựa trên mô hình "Processor-Panel":
1. Processor: Xử lý logic kết nối, luồng ảnh (Thread/Backend).
2. Panel: Cung cấp giao diện cấu hình (UI) cho từng loại camera cụ thể.

Hệ thống hỗ trợ chuyển đổi linh hoạt giữa các giao thức camera (GigE, USB) thông qua
cơ chế Stacked Widget và Signal/Slot của PySide6.
"""



import sys
from enum import IntEnum
from typing import Optional, Any, List, Dict
from dataclasses import asdict, is_dataclass

from PySide6.QtCore import Signal, Qt, QDir
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QRadioButton,
    QStackedWidget,
    QButtonGroup,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

import cv2
import os
from datetime import datetime

from .processors.base import Processor, CamSettings

class CameraType(IntEnum):
    GIGE = 0
    USB = 1
    RTSP = 2
    DVP = 3


class BaseCameraWidget(QWidget):
    """
    Widget tổng hợp dùng để cấu hình và quản lý kết nối Camera.

    Widget này đóng vai trò là một "Container" chứa:
    - Bộ chọn loại camera (Radio Buttons).
    - Các bảng điều khiển tương ứng (Stacked Config Panels).
    - Quản lý vòng đời của các Camera Processor.

    Attributes:
        frame_ready (Signal): Phát ra ảnh (numpy.ndarray) khi có frame mới từ camera.
        triggerSignal (Signal): Tín hiệu yêu cầu camera chụp một ảnh (Single Frame).
    Layout:
      [ Gige (radio) | Usb (radio) ]
      [ Stacked config panels       ]
    """

    # Dùng object để tránh metatype issue với numpy.ndarray
    frame_ready = Signal(object)
    triggerSignal = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._processors: List[Processor] = []
        self._curr_camera: Optional[Processor] = None
        self.is_open: bool = False
        self._shot_path: str = ""
        self._last_frame: Optional[Any] = None

        self._setup_ui()

        # Thêm processors với try-except để tránh treo ứng dụng khi thiếu SDK/Camera
        print("[Info] Khoi tao cac Camera Processors...")
        
        # 1. Hikvision Camera
        try:
            from .processors.hik_cam import HikCameraProcessor
            self.add_processor(HikCameraProcessor())
        except BaseException as e:
            print(f"   [!] Loi nap HikCameraProcessor: {e}")
            
        # 2. USB Camera
        try:
            from .processors.usb_cam import UsbCameraProcessor
            self.add_processor(UsbCameraProcessor())
        except BaseException as e:
            print(f"   [!] Loi nap UsbCameraProcessor: {e}")

        # 3. RTSP Camera
        try:
            from .processors.rtsp_cam import RtspCameraProcessor
            self.add_processor(RtspCameraProcessor())
            print("   [+] RtspCameraProcessor nap thanh cong")
        except BaseException as e:
            print(f"   [!] Loi nap RtspCameraProcessor: {e}")

        # 4. DVP Camera
        # 4. DVP Camera (IPC Mode)
        try:
            from .processors.ipc_cam import IpcCameraProcessor
            # Use name 'DVP' for the processor, but the class is IpcCameraProcessor
            self.add_processor(IpcCameraProcessor())
            print("   [+] IpcCameraProcessor (DVP) nap thanh cong")
        except BaseException as e:
            print(f"   [!] Loi nap IpcCameraProcessor: {e}")

        # Mặc định chọn GIGE nếu có, nếu không chọn USB hoặc cái đầu tiên
        if self._type_group.button(CameraType.GIGE):
            self._type_group.button(CameraType.GIGE).setChecked(True)
            self._on_type_selected(int(CameraType.GIGE))
        elif self._processors:
            self._type_group.buttons()[0].setChecked(True)
            self._on_type_selected(0)


    # -----------------------
    # Qt Events
    # -----------------------
    def closeEvent(self, event: QCloseEvent) -> None:
        """Đảm bảo tất cả các processors được ngắt kết nối trước khi đóng."""
        print("[Info] Đang đóng Camera Widget, giải phóng các processors...")
        for proc in self._processors:
            try:
                proc.disconnect_camera()
            except Exception as e:
                print(f"   [!] Loi khi ngat ket noi {proc.name}: {e}")
        super().closeEvent(event)


    # -----------------------
    # UI Setup
    # -----------------------
    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        # Radio group
        radio_layout = QHBoxLayout()
        self._gige_radio = QRadioButton("Gige")
        self._usb_radio = QRadioButton("Usb")
        self._rtsp_radio = QRadioButton("RTSP")
        self._dvp_radio = QRadioButton("DVP")
        
        radio_layout.addWidget(self._gige_radio)
        radio_layout.addWidget(self._usb_radio)
        radio_layout.addWidget(self._rtsp_radio)
        radio_layout.addWidget(self._dvp_radio)
        
        # Shot Button
        self.btn_shot = QPushButton("📸 Shot")
        self.btn_shot.setFixedWidth(80)
        self.btn_shot.clicked.connect(self._on_snapshot_clicked)
        radio_layout.addWidget(self.btn_shot)
        
        layout.addLayout(radio_layout)

        # Button group
        self._type_group = QButtonGroup(self)
        self._type_group.setExclusive(True)
        self._type_group.addButton(self._gige_radio, int(CameraType.GIGE))
        self._type_group.addButton(self._usb_radio, int(CameraType.USB))
        self._type_group.addButton(self._rtsp_radio, int(CameraType.RTSP))
        self._type_group.addButton(self._dvp_radio, int(CameraType.DVP))
        self._type_group.idClicked.connect(self._on_type_selected)

        # Stacked config panels
        self._stack = QStackedWidget(self)
        layout.addWidget(self._stack)

    # -----------------------
    # Processor Management
    # -----------------------
    def add_processor(self, processor: Processor) -> None:
        """
        Đăng ký một Camera Processor mới vào hệ thống.

        Tham số:
            processor (Processor): Đối tượng xử lý camera (phải kế thừa từ Processor).
        """

        self._processors.append(processor)
        self._stack.addWidget(processor.panel)
        # Forward frames từ processor ra ngoài widget
        processor.frame_ready.connect(
            self._handle_frame, Qt.ConnectionType.UniqueConnection
        )

    def _handle_frame(self, frame):
        """Lưu frame mới nhất và phát tín hiệu ra ngoài."""
        # print(f"[Cam Debug] Frame received: {frame.shape if frame is not None else 'None'}")
        self._last_frame = frame
        self.frame_ready.emit(frame)

    def _on_snapshot_clicked(self):
        """Xử lý sự kiện chụp ảnh."""
        if self._last_frame is None:
            QMessageBox.warning(self, "Cảnh báo", "Không có hình ảnh để chụp!")
            return

        # Nếu chưa có đường dẫn -> Chọn thư mục lần đầu
        if not self._shot_path or not os.path.exists(self._shot_path):
            path = QFileDialog.getExistingDirectory(self, "Chọn thư mục lưu ảnh")
            if path:
                self._shot_path = path
            else:
                return

        # Lưu ảnh
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Shot_{timestamp}.jpg"
            filepath = os.path.join(self._shot_path, filename)
            
            # Ghi file dùng OpenCV (BGR)
            success = cv2.imwrite(filepath, self._last_frame)
            
            if success:
                print(f"[Info] Đã lưu ảnh: {filepath}")
                # Optional: Hiện status bar thông báo nếu có main window context
            else:
                QMessageBox.critical(self, "Lỗi", f"Không thể lưu ảnh vào:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi lưu ảnh: {e}")

    def _activate_processor(self, index: int) -> None:
        """
        Kích hoạt bộ xử lý camera tại vị trí chỉ định và hủy kích hoạt bộ xử lý cũ.

        Tham số:
            index (int): Chỉ số của processor trong danh sách _processors.
        """
        if not (0 <= index < len(self._processors)):
            return

        # Deactivate camera trước đó
        if self._curr_camera:
            try:
                self._curr_camera.disconnect_camera()
                self.triggerSignal.disconnect()
            except Exception:
                pass

        self._stack.setCurrentIndex(index)
        self._curr_camera = self._processors[index]
        self.triggerSignal.connect(self._curr_camera.trigger_once)

    # -----------------------
    # Slots
    # -----------------------
    def _on_type_selected(self, cam_id: int) -> None:
        """Slot xử lý khi người dùng click chọn loại camera trên UI."""
        try:
            cam_type = CameraType(cam_id)
        except ValueError:
            return
        self._activate_processor(int(cam_type))

    def connect_camera(self) -> None:
        if self._curr_camera and self._curr_camera.panel.boxEnum.currentText():
            self._curr_camera.panel.btn_toggle_connect.click()

    def trigger_once(self) -> None:
        if self._curr_camera:
            self._curr_camera.trigger_once()

    def dump_settings(self) -> Optional[Dict[str, Any]]:
        """
        Trích xuất toàn bộ cấu hình hiện tại của camera (loại cam, thông số panel).

        Trả về:
            Dict[str, Any]: Dictionary chứa thông tin camera_type và các thông số cài đặt.
        """
        settings = (
            self._curr_camera.panel.dump_settings() if self._curr_camera else None
        )
        if settings is None:
            return {}

        # Nếu là dataclass -> asdict; nếu là dict -> dùng luôn
        if is_dataclass(settings):
            settings = asdict(settings)
        cam_type = self._type_group.checkedId()
        return {
            "camera_type": int(cam_type), 
            "panel": settings,
            "shot_path": self._shot_path
        }

    def load_settings(self, settings: Dict[str, Any]) -> None:
        """
        Nạp cấu hình từ dictionary vào UI và Processor.

        Tham số:
            settings (Dict[str, Any]): Dictionary chứa cấu hình (thường đọc từ file json).
        """
        cam_type = settings.get("camera_type", CameraType.GIGE)
        self._type_group.button(cam_type).setChecked(True)
        self._on_type_selected(cam_type)
        
        self._shot_path = settings.get("shot_path", "")
        
        panel = settings.get("panel", {})
        s = CamSettings(**panel)
        if self._curr_camera:
            self._curr_camera.panel.load_settings(s)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BaseCameraWidget()
    window.show()
    sys.exit(app.exec())
