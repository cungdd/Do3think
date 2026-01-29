"""Package `communicate` chứa các module giao thức và tiện ích liên quan.

Bao gồm các lớp protocol (TCPClient, MODBUS) để dùng bởi ứng dụng.
"""

from .TCP_Protocol.TCPClient import TCPClient
from .Modbus_Protocol.MODBUS import MODBUS

__all__ = ["TCPClient", "MODBUS"]
