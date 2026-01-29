"""
DVP Camera Processor implementation using dvp.pyd.
"""



import sys
import os
import time
from dataclasses import dataclass
from typing import Optional, Any, Sequence, List
# from collections.abc import Sequence

import numpy as np
import cv2

# Import PySide6
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QLabel,
    QSpinBox,
    QCheckBox,
    QMessageBox,
    QGroupBox,
    QFormLayout
)

# Base classes
from .base import Processor, ConfigPanel, CamSettings
from .worker import Worker

# Import dvp library
# Assuming dvp.pyd is in the python path or project root
try:
    import dvp
    # Check if we need to import * or just dvp
    # In OpenCV_Demo.py: from dvp import *
    # Let's inspect what's needed. Camera, Refresh, etc.
    from dvp import Camera, Refresh, Status, ImageFormat, Bits, AeOperation, AntiFlick, AeMode, dvpException
except ImportError:
    print("Warning: Could not import 'dvp'. DVP Camera will not work.")
    dvp = None

class DvpCameraProcessor(Processor):
    """
    Processor for DVP Camera using dvp.pyd.
    """
    name = "DVPCamera"
    frame_ready = Signal(object) # Emit np.ndarray

    def __init__(self) -> None:
        super().__init__()
        self.settings: CamSettings = CamSettings()
        self._panel = DvpCameraConfigPanel()
        self._worker: Optional[Worker] = None
        self._camera = None # DVP Camera instance
        self.is_open: bool = False
        
        # Trigger emulation/state
        self._want_shot: bool = False

        # Wiring
        self.triggerSignal.connect(self.trigger_once)
        self._panel.settings_changed.connect(self.configure)
        self._panel.btn_capture.clicked.connect(self.trigger_once)
        self._panel.btn_toggle_connect.clicked.connect(self._on_toggle_connection_clicked)

    def configure(self, s: CamSettings) -> None:
        """Apply settings to the camera."""
        s = s or CamSettings()
        old = self.settings
        self.settings = s

        if not self._camera or not self.is_open:
            return

        try:
            # 1. Exposure
            if s.exposure_auto != old.exposure_auto:
                self._set_auto_exposure(s.exposure_auto)
            
            if not s.exposure_auto and (s.exposure != old.exposure):
                 self._camera.Exposure = float(s.exposure)

            # 2. Trigger Mode (Handled in software/loop usually for this demo, 
            # but DVP has TriggerState. logic: 
            # "camera.TriggerState = False #Switch from trigger mode to continuous plotting mode"
            # If we want software trigger, we might keep it continuous and just gate the callback?
            # Or use hardware trigger? 
            # For consistency with UsbCam (software trigger emulation) or Hik (hardware trigger), 
            # let's check what checking 'trigger_mode' does.
            # In OpenCV_Demo.py: camera.TriggerState = False (Continuous).
            # If we want real trigger, we set it to True.
            # However, for simplicity and stability compatible with 'Worker' pulling frames,
            # we might stick to Continuous stream and just drop frames if trigger_mode is On 
            # but no trigger requested.
            
            # Implementation choice: 
            # If trigger_mode is True -> Camera is still in Continuous mode (TriggerState=False)
            # but we only emit frames when _want_shot is True. 
            pass

        except Exception as e:
            print(f"Error configuring DVP camera: {e}")

    def reset(self) -> None:
        self.settings = CamSettings()
        self._want_shot = False

    def connect_camera(self) -> bool:
        """Connect to the camera selected in the panel."""
        if dvp is None:
            self._panel.show_error("Thư viện dvp.pyd chưa được nạp.")
            return False

        dev_name = self._panel.device_name
        if not dev_name:
            self._panel.show_error("Chưa chọn thiết bị.")
            return False

        self.disconnect_camera()

        try:
            print(f"Connecting to DVP Camera: {dev_name}")
            # OpenCV_Demo uses Camera(index) or Camera(FriendlyName)
            # We will use FriendlyName if possible, or index.
            # The panel stores FriendlyName.
            self._camera = Camera(dev_name)
            
            # Initial setup
            # Set to Continuous mode by default for pulling
            self._camera.TriggerState = False 
            
            # Start stream
            self._camera.Start()
            
            self.is_open = True
            
            # Apply initial settings
            self._apply_initial_settings()

            # Start worker to pull frames
            self._worker = Worker(self)
            self._worker.frame_ready.connect(self.__on_frame, Qt.ConnectionType.UniqueConnection)
            self._worker.start()

            print("DVP Camera connected and started.")
            return True

        except dvpException as e:
            self._panel.show_error(f"Lỗi DVP: {e.Status}")
            self.disconnect_camera()
            return False
        except Exception as e:
            self._panel.show_error(f"Lỗi kết nối: {e}")
            self.disconnect_camera()
            return False

    def disconnect_camera(self) -> bool:
        if self._worker:
            self._worker.stop()
            self._worker = None

        if self._camera:
            try:
                self._camera.Stop()
                self._camera.Close()
            except Exception as e:
                print(f"Error closing DVP camera: {e}")
            finally:
                self._camera = None

        self.is_open = False
        self.reset()
        return True

    def grab_frame(self, enabled: bool) -> bool:
        # Worker calls this, but for DVP with GetFrame, we do it in get_frame
        return True

    def get_frame(self) -> Optional[np.ndarray]:
        if not self._camera:
            return None

        if self.settings.trigger_mode and not self._want_shot:
            # Drop frames if in trigger mode but no shot wanted
            # But we must keep pulling from camera buffer or it might overflow?
            # DVP GetFrame has timeout.
            # If we don't call GetFrame, the internal buffer fills up.
            # Best practice: always pull, but only return if wanted.
            pass
        
        try:
            # Timeout 3000ms
            frame = self._camera.GetFrame(3000) 
            if frame:
                # Convert to numpy
                mat = self._frame2mat(frame)
                
                if self.settings.trigger_mode:
                    if self._want_shot:
                        self._want_shot = False
                        return mat
                    else:
                        return None # Drop
                
                return mat
                
        except dvpException as e:
            # Status.DVP_STATUS_TIME_OUT
            # print(f"DVP GetFrame Error: {e.Status}")
            pass
        except Exception as e:
            print(f"GetFrame Generic Error: {e}")
            
        return None

    def trigger_once(self) -> None:
        if self.is_open and self.settings.trigger_mode:
            self._want_shot = True

    def __on_frame(self, frame: np.ndarray) -> None:
        self.frame_ready.emit(frame)

    def _frame2mat(self, frameBuffer):
        """
        Convert DVP frame buffer to numpy array (BGR).
        Based on frame2mat from OpenCV_Demo.py
        """
        frame, buffer = frameBuffer
        bits = np.uint8 if(frame.bits == Bits.BITS_8) else np.uint16
        shape = None
        
        # Determine shape
        if(frame.format >= ImageFormat.FORMAT_MONO and frame.format <= ImageFormat.FORMAT_BAYER_RG):
            shape = 1
        elif(frame.format == ImageFormat.FORMAT_BGR24 or frame.format == ImageFormat.FORMAT_RGB24):
            shape = 3
        elif(frame.format == ImageFormat.FORMAT_BGR32 or frame.format == ImageFormat.FORMAT_RGB32):
            shape = 4
        else:
            return None

        mat = np.frombuffer(buffer, bits)
        mat = mat.reshape(frame.iHeight, frame.iWidth, shape)
        return mat

    def _apply_initial_settings(self):
        # Default settings
        try:
            # Set ROI (example, maybe optional or full)
            # region = self._camera.Roi
            # region.X = 0; region.Y = 0; region.W = ...
            pass
            
            # Update settings from panel
            cur_settings = self._panel.dump_settings()
            self.configure(cur_settings)
            
        except Exception as e:
            print(f"Error applying initial settings: {e}")

    def _set_auto_exposure(self, enabled: bool):
        if not self._camera: return
        
        try:
            if enabled:
                self._camera.AeOperation = AeOperation.AE_OP_CONTINUOUS
                self._camera.AeMode = AeMode.AE_MODE_AE_ONLY
            else:
                self._camera.AeOperation = AeOperation.AE_OP_OFF
        except Exception as e:
            print(f"Set Auto Exposure Error: {e}")


    @property
    def panel(self) -> ConfigPanel:
        return self._panel


class DvpCameraConfigPanel(ConfigPanel):
    """
    Configuration Panel for DVP Camera.
    """
    settings_changed = Signal(CamSettings)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._debounce = QTimer(self)
        self._debounce.setSingleShot(True)
        self._debounce.setInterval(200)
        self._debounce.timeout.connect(self._emit_settings)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # 1. Device Selection
        hb_dev = QHBoxLayout()
        self.boxEnum = QComboBox()
        self.btn_enum_device = QPushButton("Refresh")
        self.btn_toggle_connect = QPushButton("Connect")
        
        hb_dev.addWidget(QLabel("Device:"))
        hb_dev.addWidget(self.boxEnum, 1)
        hb_dev.addWidget(self.btn_enum_device)
        layout.addLayout(hb_dev)
        layout.addWidget(self.btn_toggle_connect)

        # 2. Controls Group
        grp_ctrl = QGroupBox("Controls")
        form_layout = QFormLayout(grp_ctrl)
        
        # Exposure Auto
        self.cbExposureAuto = QCheckBox("Auto Exposure")
        self.cbExposureAuto.setChecked(True)
        form_layout.addRow(self.cbExposureAuto)

        # Exposure Time
        self.spinExposure = QSpinBox()
        self.spinExposure.setRange(1, 1000000) # Microseconds
        self.spinExposure.setValue(10000)
        self.spinExposure.setSuffix(" µs")
        self.spinExposure.setEnabled(False) # Default Auto is Checked
        form_layout.addRow("Exposure:", self.spinExposure)

        # Trigger Mode
        self.chkTrigger = QCheckBox("Trigger Mode")
        form_layout.addRow(self.chkTrigger)
        
        self.btn_capture = QPushButton("Trigger / Capture")
        self.btn_capture.setEnabled(False)
        form_layout.addRow(self.btn_capture)

        layout.addWidget(grp_ctrl)
        layout.addStretch()

        # Connections
        self.btn_enum_device.clicked.connect(self.enum_devices)
        self.cbExposureAuto.toggled.connect(self.spinExposure.setDisabled)
        self.cbExposureAuto.toggled.connect(self._on_change)
        self.spinExposure.editingFinished.connect(self._on_change)
        self.chkTrigger.toggled.connect(self.btn_capture.setEnabled)
        self.chkTrigger.toggled.connect(self._on_change)

        # Initial Enum
        # QTimer.singleShot(100, self.enum_devices)

    def _on_change(self):
        self._debounce.start()

    def _emit_settings(self):
        self.settings_changed.emit(self.dump_settings())

    def enum_devices(self) -> Sequence[str]:
        self.boxEnum.clear()
        found = []
        if dvp is None:
            return []

        try:
            # Refresh() returns list of camera info
            cameraInfo = Refresh()
            for cam in cameraInfo:
                name = cam.FriendlyName
                found.append(name)
                self.boxEnum.addItem(name)
        except Exception as e:
            print(f"Error enumerating DVP devices: {e}")
        
        return found

    @property
    def device_name(self) -> Optional[str]:
        return self.boxEnum.currentText() if self.boxEnum.count() > 0 else None

    def dump_settings(self) -> CamSettings:
        return CamSettings(
            dev=self.device_name,
            exposure=self.spinExposure.value(),
            exposure_auto=self.cbExposureAuto.isChecked(),
            trigger_mode=self.chkTrigger.isChecked(),
        )

    def load_settings(self, s: CamSettings) -> None:
        if not s: return
        if s.dev:
            self.boxEnum.setCurrentText(s.dev)
        self.spinExposure.setValue(s.exposure)
        self.cbExposureAuto.setChecked(s.exposure_auto)
        self.chkTrigger.setChecked(s.trigger_mode)

    def ui_update(self, connected: bool) -> None:
        self.btn_toggle_connect.setText("Disconnect" if connected else "Connect")
        self.boxEnum.setEnabled(not connected)
        self.btn_enum_device.setEnabled(not connected)
        
    def show_error(self, msg: str) -> None:
        QMessageBox.critical(self, "Error", msg)

