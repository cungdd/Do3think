"""
Main Application - Module Integration Platform

Ứng dụng chính tích hợp 3 module:
1. Camera Agent - Quản lý camera
2. Detect Agent - Phát hiện đối tượng bằng YOLO
3. Protocol Manager - Quản lý giao thức truyền thông

Luồng dữ liệu: Camera → Detect → Protocol
"""

import sys
import os
from pathlib import Path

# Silence noisy system logs
os.environ["OPENCV_LOG_LEVEL"] = "ERROR"
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0" # Ưu tiên DSHOW hơn MSMF trên Windows nếu có thể

from PySide6.QtWidgets import (

    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QStatusBar,
    QMenuBar,
    QMessageBox,
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QAction, QIcon

# Import các module chính
from src.agent_camera import BaseCameraWidget
try:
    from src.agent_detect import BaseDetectWidget
except ImportError as e:
    print(f"Warning: Could not import BaseDetectWidget: {e}")
    BaseDetectWidget = None

try:
    from src.communicate.protocol_main import ProtocolMain
except ImportError as e:
    print(f"Warning: Could not import ProtocolMain: {e}")
    ProtocolMain = None
from src.utils import apply_stylesheet, center_window, ViewImage, SettingsManager


class MainWindow(QMainWindow):
    """
    Lớp chính của ứng dụng - Tích hợp và điều phối các module.
    
    Layout:
    ┌────────────────┬──────────────────────────┐
    │                │ Menu Bar                 │
    │  Video Viewer  ├──────────────────────────┤
    │  (ViewImage)   │ Control Tabs             │
    │                │ [Cam][Det][Proto][Set]   │
    └────────────────┴──────────────────────────┘
    """


    def __init__(self):
        super().__init__()
        
        # Thiết lập window
        self.setWindowTitle("Module Integration Platform - v1.1.0")
        self.setGeometry(100, 100, 1400, 850)
        
        # Khởi tạo settings manager
        self.settings_manager = SettingsManager()
        
        # Trạng thái
        self._first_frame = True
        
        # Setup UI
        self._setup_ui()
        self._setup_menu()
        self._setup_statusbar()
        
        # Kết nối các module
        self._connect_modules()
        
        # Load settings
        self._load_settings()
        
        # Căn giữa cửa sổ
        center_window(self)
        
        # Hiển thị thông báo sẵn sàng
        self.statusBar().showMessage("✓ Sẵn sàng - Video Viewer đã được kích hoạt", 4000)

    def _setup_ui(self):
        """Thiết lập giao diện tích hợp Video + Tabs."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout chính: Ngang (Trái: Video | Phải: Controls)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # --- Cột trái: Video Viewer ---
        video_container = QWidget()
        video_layout = QVBoxLayout(video_container)
        video_layout.setContentsMargins(0, 0, 0, 0)
        
        lbl_v = QLabel("<b>LIVE VIDEO PERFORMANCE</b>")
        lbl_v.setStyleSheet("color: #3498db; margin-bottom: 5px;")
        video_layout.addWidget(lbl_v)
        
        self.view_image = ViewImage(video_container)
        video_layout.addWidget(self.view_image)
        
        main_layout.addWidget(video_container, stretch=2) # Tỉ lệ 2
        
        # --- Cột phải: Control Tabs ---
        self.tab_widget = QTabWidget()
        self.tab_widget.setFixedWidth(400) # Cố định chiều rộng cột điều khiển
        main_layout.addWidget(self.tab_widget, stretch=1) # Tỉ lệ 1
        
        self._init_modules()
        
    def _init_modules(self):
        """Khởi tạo và thêm các module vào tab."""
        # Tab 1: Camera
        self.camera_widget = BaseCameraWidget()
        self.tab_widget.addTab(self.camera_widget, "📷 Camera")
        
        # Tab 2: Detect (YOLO)
        # Tab 2: Detect (YOLO)
        if BaseDetectWidget:
            self.detect_widget = BaseDetectWidget()
            self.tab_widget.addTab(self.detect_widget, "🤖 AI Detect")
        else:
            self.detect_widget = QLabel("AI Detect Module Not Available (Missing Dependencies)")
            self.detect_widget.setAlignment(Qt.AlignCenter)
            self.tab_widget.addTab(self.detect_widget, "🤖 AI Detect (N/A)")
        
        # Tab 3: Protocol Manager
        # Tab 3: Protocol Manager
        if ProtocolMain:
            self.protocol_widget = ProtocolMain()
            self.tab_widget.addTab(self.protocol_widget, "📡 Protocol")
        else:
            self.protocol_widget = QLabel("Protocol Module Not Available")
            self.protocol_widget.setAlignment(Qt.AlignCenter)
            self.tab_widget.addTab(self.protocol_widget, "📡 Protocol (N/A)")
        
        # Tab 4: Settings
        self.settings_widget = self._create_settings_tab()
        self.tab_widget.addTab(self.settings_widget, "⚙️ Settings")
        
        # Connect tab change event
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        
    def _create_settings_tab(self):
        """Tạo tab Settings."""
        from PySide6.QtWidgets import QLabel, QPushButton, QGroupBox, QFormLayout
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Info group
        info_group = QGroupBox("Thông tin hệ thống")
        info_layout = QFormLayout()
        info_layout.addRow("Phiên bản:", QLabel("1.1.0-RTSP"))
        info_layout.addRow("Engine:", QLabel("PySide6 + OpenCV + YOLO"))
        info_layout.addRow("Trạng thái:", QLabel("Tích hợp Video Viewer"))
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Actions group
        action_group = QGroupBox("Cấu hình tập trung")
        action_layout = QVBoxLayout()
        
        btn_save = QPushButton("💾 Lưu cấu hình toàn cục")
        btn_save.clicked.connect(self._save_settings)
        action_layout.addWidget(btn_save)
        
        btn_load = QPushButton("📂 Nạp cấu hình từ file")
        btn_load.clicked.connect(self._load_settings)
        action_layout.addWidget(btn_load)
        
        action_group.setLayout(action_layout)
        layout.addWidget(action_group)
        
        layout.addStretch()
        return widget
        
    def _setup_menu(self):
        """Thiết lập menu bar."""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("&File")
        
        save_action = QAction("💾 Lưu cấu hình", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save_settings)
        file_menu.addAction(save_action)
        
        load_action = QAction("📂 Tải cấu hình", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self._load_settings)
        file_menu.addAction(load_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("❌ Thoát", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View Menu
        view_menu = menubar.addMenu("&View")
        for i, name in enumerate(["Camera Controls", "Detect Config", "Protocol Manager", "Settings"]):
            action = QAction(name, self)
            action.triggered.connect(lambda checked=False, idx=i: self.tab_widget.setCurrentIndex(idx))
            view_menu.addAction(action)
            
        fit_action = QAction("🔍 Fit Video", self)
        fit_action.triggered.connect(lambda: self.view_image.refit())
        view_menu.addAction(fit_action)
            
    def _setup_statusbar(self):
        """Thiết lập status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Đang sẵn sàng...")
        
    def _connect_modules(self):
        """Kết nối signal/slot giữa các module và viewer."""
        # Camera → Detect (Pipeline)
        # Camera → Detect (Pipeline)
        if hasattr(self.camera_widget, 'frame_ready') and BaseDetectWidget and isinstance(self.detect_widget, BaseDetectWidget):
            self.camera_widget.frame_ready.connect(
                self.detect_widget.on_frame_ready,
                Qt.ConnectionType.QueuedConnection
            )
        
        # Detect (Processed Data) → Viewer (UI Display)
        if BaseDetectWidget and isinstance(self.detect_widget, BaseDetectWidget):
            self.detect_widget.frame_ready.connect(
                self._on_frame_received,
                Qt.ConnectionType.QueuedConnection
            )
        else:
            # If Detect is missing, connect Camera directly to Viewer
             if hasattr(self.camera_widget, 'frame_ready'):
                self.camera_widget.frame_ready.connect(
                    self._on_frame_received,
                    Qt.ConnectionType.QueuedConnection
                )
        
        # Detect → Status
        if BaseDetectWidget and isinstance(self.detect_widget, BaseDetectWidget):
            self.detect_widget.result_ready.connect(
                self._on_detect_result,
                Qt.ConnectionType.QueuedConnection
            )

    def _on_frame_received(self, frame):
        """Hiển thị frame lên ViewImage và tự động fit lần đầu."""
        if frame is None:
            return
            
        try:
            self.view_image.add_image(frame)
            
            if self._first_frame:
                self.view_image.refit()
                self._first_frame = False
        except Exception as e:
            print(f"Lỗi hiển thị frame: {e}")

    def _on_detect_result(self, result):
        """Xử lý kết quả từ module Detect."""
        try:
            status = result.status if hasattr(result, 'status') else str(result)
            self.status_bar.showMessage(f"AI Status: {status}", 2000)
            
            # TODO: Có thể gửi kết quả qua Protocol nếu cần
            # self.protocol_widget.send_data(result)
        except Exception as e:
            print(f"Lỗi xử lý kết quả AI: {e}")
            
    def _on_tab_changed(self, index):
        """Callback khi chuyển tab."""
        tab_names = ["Camera", "Detect", "Protocol", "Settings"]
        if 0 <= index < len(tab_names):
            self.status_bar.showMessage(f"Đã chuyển sang tab: {tab_names[index]}", 2000)

    def closeEvent(self, event):
        """Xử lý khi đóng ứng dụng - Đảm bảo dừng tất cả các thread."""
        reply = QMessageBox.question(
            self, 'Xác nhận thoát',
            "Bạn có chắc chắn muốn thoát ứng dụng?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            print("[Info] Đang đóng ứng dụng, vui lòng chờ các thread kết thúc...")
            self.statusBar().showMessage("Đang đóng các module...")
            
            # Gọi close cho các widget con để chúng tự dừng thread (nếu có closeEvent)
            try:
                self.camera_widget.close()
                if self.detect_widget and hasattr(self.detect_widget, 'close'): self.detect_widget.close()
                if self.protocol_widget and hasattr(self.protocol_widget, 'close'): self.protocol_widget.close()
            except Exception as e:
                print(f"   ⚠ Lỗi khi đóng module: {e}")
                
            event.accept()
        else:
            event.ignore()
            
    def _save_settings(self):
        """Lưu cấu hình của tất cả các module."""
        try:
            settings = {
                "detect": self.detect_widget.dump_settings() if hasattr(self.detect_widget, 'dump_settings') else {},
                "protocol": self.protocol_widget.to_dict() if hasattr(self.protocol_widget, 'to_dict') else {},
            }
            if hasattr(self.camera_widget, 'dump_settings'):
                settings["camera"] = self.camera_widget.dump_settings()
                
            self.settings_manager.save_settings(settings)
            self.status_bar.showMessage("✓ Đã lưu cấu hình thành công", 3000)
            QMessageBox.information(self, "Thành công", "Cấu hình đã được lưu!")
        except Exception as e:
            self.status_bar.showMessage(f"❌ Lỗi lưu cấu hình: {e}", 5000)
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu cấu hình:\n{e}")
            
    def _load_settings(self):
        """Tải cấu hình cho tất cả các module."""
        try:
            settings = self.settings_manager.load_settings()
            if settings:
                if "camera" in settings and hasattr(self.camera_widget, 'load_settings'):
                    self.camera_widget.load_settings(settings["camera"])
                if "detect" in settings and hasattr(self.detect_widget, 'load_settings'):
                    self.detect_widget.load_settings(settings["detect"])
                if "protocol" in settings and hasattr(self.protocol_widget, 'from_dict'):
                    self.protocol_widget.from_dict(settings["protocol"])
                self.status_bar.showMessage("✓ Đã tải cấu hình thành công", 3000)
        except Exception as e:
            print(f"Lỗi tải cấu hình: {e}")
            self.status_bar.showMessage(f"⚠️ Không thể tải cấu hình: {e}", 5000)
            
    def _reset_settings(self):
        """Reset cấu hình về mặc định."""
        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc muốn reset tất cả cấu hình?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.settings_manager.reset_settings()
            self.status_bar.showMessage("✓ Đã reset cấu hình", 3000)
            
    def _show_about(self):
        """Hiển thị dialog giới thiệu."""
        QMessageBox.about(
            self,
            "Giới thiệu",
            """<h2>Module Integration Platform</h2>
            <p><b>Phiên bản:</b> 1.0.0</p>
            <p><b>Mô tả:</b> Nền tảng tích hợp các module Camera, AI Detection và Protocol Management</p>
            <p><b>Các module:</b></p>
            <ul>
                <li>📷 Camera Agent - Quản lý camera GigE/USB</li>
                <li>🤖 AI Detect - Phát hiện đối tượng bằng YOLO</li>
                <li>📡 Protocol Manager - Quản lý TCP/MODBUS</li>
            </ul>
            <p><b>Framework:</b> PySide6, Ultralytics YOLO</p>
            """
        )
        
    def closeEvent(self, event):
        """Xử lý khi đóng ứng dụng."""
        reply = QMessageBox.question(
            self, "Xác nhận thoát", "Lưu cấu hình trước khi thoát?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
        )
        if reply == QMessageBox.StandardButton.Cancel:
            event.ignore()
        else:
            if reply == QMessageBox.StandardButton.Yes:
                self._save_settings()
            event.accept()


def main():
    """Entry point của ứng dụng."""
    # Tạo QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Module Integration Platform")
    
    # Tạo và hiển thị main window
    window = MainWindow()
    
    # Apply stylesheet nếu có
    try:
        apply_stylesheet(window)
    except:
        pass
    
    window.show()
    
    # Chạy event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
