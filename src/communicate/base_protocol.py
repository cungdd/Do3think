"""Gói chứa lớp base cho các Protocol widget.

`BaseProtocol` định nghĩa các signal chung và interface cần implement bởi các protocol cụ thể (TCP, MODBUS, ...).
"""

from typing import Union
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from .ui.animation.toggleButton import ToggleButton

class BaseProtocol(QWidget):
    """Lớp base cho các protocol widget.

    Cung cấp các signal chung (toggle, notify, rx/tx) và các phương thức skeleton
    (start/stop/send_data/restart) mà subclass cần triển khai.
    """
    toggle_signal = Signal(int) # Tín hiệu thay dổi trạng thái kết nối của giao thức
    curr_connect_notify = Signal(int)
    auto_connect_notify = Signal(int)
    
    rx_data = Signal(str) # Tín hiệu dữ liệu nhận được
    tx_data = Signal(str) # Tín hiệu dữ liệu chuyện đi

    def __init__(self, parent=None):
        super().__init__(parent)
        self.toggleAutoConnect = ToggleButton(parent=None, height=26)
        self.toggleAutoConnect.stateChanged.connect(self.restart)  

        # Kết nối tín hiệu
        self.toggle_signal.connect(lambda state: self.start() if state==2 else self.stop())
        self.tx_data.connect(self.send_data)

    def addr_copy(self, text):
        raise NotImplementedError("addr_copy chưa được triển khai!")

    def port_copy(self, text):
        raise NotImplementedError("port_copy chưa được triển khai!")

    def start(self):
        raise NotImplementedError("start chưa được triển khai!")

    def stop(self):
        raise NotImplementedError("stop chưa được triển khai!")
    
    def connected(self):
        raise NotImplementedError("connected chưa được triển khai!")
    
    def disconnected(self):
        raise NotImplementedError("disconnected chưa được triển khai!")

    def handle_data(self, rx_bytes):
        raise NotImplementedError("handle_data chưa được triển khai!")
    
    def send_data(self, tx_data: Union[int, str, bytes]):
        raise NotImplementedError("send_data chưa được triển khai!")
    
    def restart(self):
        raise NotImplementedError("restart chưa được triển khai!")

    @property
    def settings(self):
        raise NotImplementedError("settings chưa được triển khai!")