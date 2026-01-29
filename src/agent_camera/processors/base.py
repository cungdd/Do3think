# --- file: processors/base.py ---
"""
Module base cung cấp các lớp cơ sở (Base Classes) và Data Classes cho hệ thống Camera.

Module này định nghĩa các giao diện (interfaces) chuẩn mà mọi camera processor (Hikvision, USB, v.v.)
phải tuân thủ, giúp tách biệt logic điều khiển phần cứng và giao diện người dùng.
"""



from dataclasses import dataclass, field
from typing import Any, Optional, Dict, Union, Sequence, List
# from collections.abc import Sequence

import numpy as np
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget

# Nếu bạn có Ui_Form được sinh bởi Qt Designer
from .ui.cam_control_ui import Ui_Form  # giữ nguyên import như bạn đang dùng


@dataclass
class CamSettings:
    """
    Data class lưu trữ các thông số cấu hình của Camera.

    Attributes:
        dev (str, optional): Tên định danh thiết bị hoặc Serial Number.
        ip (str, optional): Địa chỉ IP (dành cho GigE Camera).
        exposure (int): Giá trị thời gian phơi sáng (microseconds).
        exposure_auto (bool): Trạng thái tự động phơi sáng.
        trigger_mode (bool): Chế độ kích hoạt bằng tín hiệu (True) hoặc liên tục (False).
        advanced (dict): Các thông số mở rộng dành riêng cho từng loại camera cụ thể.
    """

    dev: Optional[str] = None
    ip: Optional[str] = None
    exposure: int = 0
    exposure_auto: bool = False
    trigger_mode: bool = False
    advanced: Dict[str, Any] = field(default_factory=dict)


class Processor(QObject):
    """
    Interface cơ bản cho camera processor.
    Kế thừa lớp này để implement cụ thể từng loại camera.
    """

    name: str = "Processor"
    is_open: bool = False
    # Dùng object để an toàn khi truyền numpy.ndarray
    frame_ready = Signal(object)
    triggerSignal = Signal()

    def configure(self, s: CamSettings) -> None: ...
    def reset(self) -> None: ...
    def connect_camera(self) -> bool: ...
    def disconnect_camera(self) -> bool: ...
    def grab_frame(self, enabled: bool) -> bool: ...
    def get_frame(self) -> Optional[np.ndarray]: ...
    def trigger_once(self) -> None: ...

    @property
    def panel(self) -> "ConfigPanel": ...


class ConfigPanel(Ui_Form, QWidget):
    """
    Panel cấu hình cho một processor.
    Lưu ý: lớp con nên phát tín hiệu `settings_changed` khi người dùng đổi thông số.
    """

    # lớp con nên khai báo: settings_changed = Signal(CamSettings)

    def enum_devices(self) -> Sequence[Union[Dict[str, Any], Any]]: ...

    @property
    def exposure(self) -> int: ...
    @exposure.setter
    def exposure(self, value: int) -> None: ...

    @property
    def exposure_auto(self) -> bool: ...
    @exposure_auto.setter
    def exposure_auto(self, enabled: bool) -> None: ...

    @property
    def trigger_mode(self) -> bool: ...
    @trigger_mode.setter
    def trigger_mode(self, mode: bool) -> None: ...

    def ui_update(self, connected: bool) -> None: ...

    def load_settings(self, s: CamSettings) -> None: ...
    def dump_settings(self) -> CamSettings: ...
