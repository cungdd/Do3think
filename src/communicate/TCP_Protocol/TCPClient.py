"""Client TCP dùng QTcpSocket để gửi/nhận dữ liệu và cập nhật giao diện.

Bao gồm xử lý trạng thái kết nối, ghi nhận log gửi/nhận (hiển thị trong QTextEdit),
quản lý auto-connect và thông báo lỗi cho người dùng.
"""

from typing import Optional
from datetime import datetime

from PySide6.QtCore import QByteArray, Signal, Slot
from PySide6.QtWidgets import QApplication, QWidget, QSpinBox, QMessageBox
from PySide6.QtNetwork import QHostAddress, QTcpSocket

# from .TCP_Protocol_ui import Ui_Form
# from ..base_protocol import BaseProtocol

# from .handler import state_changed, sock_error


from .TCP_Protocol_ui import Ui_Form
from ..base_protocol import BaseProtocol

from .handler import state_changed, sock_error


class TCPClient(Ui_Form, BaseProtocol):
    def __init__(self, parent=None, addr=None, port=None, auto=False):
        super().__init__(parent)
        self.setupUi(self)
        self.labelStatus.setText(f'<font color="#C62828">Đã ngắt kết nối</font>')

        self.sock = QTcpSocket()

        self.started = False  # Cờ trạng hái kêt nối: True – Đang kết nối, False – Đang ngắt kết nối
        self.addr = addr  # Địa chỉ server
        self.port = port  # Port server

        self.gridLayout_2.replaceWidget(self.holderAutoConnect, self.toggleAutoConnect)
        self.holderAutoConnect.deleteLater()

        self.bnSend.clicked.connect(self.send)
        self.curr_connect_notify.connect(self.update_ui)

        self.sock.readyRead.connect(self.on_port_rx)
        self.sock.stateChanged.connect(self.state_changed)
        self.sock.errorOccurred.connect(self.sock_error)

        self.toggleAutoConnect.setChecked(auto)

    @property
    def addr(self) -> str:
        """Lấy giá trị của các ô địa chỉ dưới dạng chuỗi.

        Thuộc tính này trả về 4 ô địa chỉ nối lại thành một chuỗi theo định dạng IP.

        Trả về:
            str: Địa chỉ IP (chuỗi)
        """
        octets: list[QSpinBox] = [self.octet, self.octet_2, self.octet_3, self.octet_4]
        return ".".join(str(octet.value()) for octet in octets)

    @addr.setter
    def addr(self, value: str | None):
        """Đặt giá trị các ô địa chỉ từ một chuỗi IP.

        Nếu `value` là `None` thì các ô sẽ được đặt về mặc định `127.0.0.1`.
        """
        if value is None:
            value = "127.0.0.1"

        octets = value.split(".")
        self.octet.setValue(int(octets[0]))
        self.octet_2.setValue(int(octets[1]))
        self.octet_3.setValue(int(octets[2]))
        self.octet_4.setValue(int(octets[3]))

    @property
    def port(self) -> int:
        return self.port_field.value()

    @port.setter
    def port(self, value: int | None) -> None:
        """Đặt giá trị cho trường port (cổng)."""
        self.port_field.setValue(value if value is not None else 9760)

    @property
    def settings(self) -> dict[str, int | str]:
        return {
            "addr": self.addr,
            "port": self.port,
            "auto": self.toggleAutoConnect.isChecked(),
        }

    # @settings.setter
    # def settings(self, value: dict[str, int| str] | None) -> None:
    #     if not value:
    #         self.addr = None
    #         self.port = None
    #         return
    #     self.addr = str(value.get("addr"))
    #     port_val = value.get("port")
    #     if port_val is None:
    #         self.port = None
    #     elif isinstance(port_val, int):
    #         self.port = port_val
    #     elif isinstance(port_val, str):
    #         self.port = int(port_val)  # may raise ValueError
    #     else:
    #         raise TypeError("port must be int | str | None")

    def start(self):
        if not self.started:
            self.started = True
            self.port = self.port_field.value()
            self.sock.connectToHost(QHostAddress(self.addr), self.port)

    def stop(self):
        if self.started:
            self.started = False
            self.sock.close()

    @Slot()
    def send(self):
        if self.started:
            cmd_to_send = self.any_field.text()
            self.sock.write(QByteArray(cmd_to_send.encode("utf-8")))

            # Lấy thời gian hiện tại với định dạng mong muốn
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[
                :-3
            ]  # Cắt bỏ 3 số cuối của microsecond để giống định dạng ,617
            formatted_data = (
                f'<span style="color:black">[{current_time}]# Gửi tới {self.addr} :{self.port}</span>>>><br>'
                f'<span style="color:blue">{cmd_to_send}</span><br><br>'
            )
            try:
                self.term_tx.insertHtml(formatted_data)
            except Exception:
                self.term_tx.insertPlainText("\r[có lỗi xảy ra!]\r")
            self.term_tx.ensureCursorVisible()

    def send_data(self, tx_data: int | str | bytes):
        if self.started:
            self.sock.write(QByteArray(str(tx_data).encode("utf-8")))

    def on_port_rx(self):
        num_rx_bytes = self.sock.bytesAvailable()
        rx_bytes = self.sock.read(num_rx_bytes)
        data = bytes(rx_bytes.data()).decode("utf-8")
        self.rx_data.emit(data)
        # Lấy thời gian hiện tại với định dạng mong muốn
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[
            :-3
        ]  # Cắt bỏ 3 số cuối của microsecond để giống định dạng ,617
        formatted_data = (
            f'<span style="color:black">[{current_time}]# Nhận từ {self.addr} :{self.port} </span>>>><br>'
            f'<span style="color:green">{data}</span><br><br>'
        )
        try:
            self.term_rx.insertHtml(formatted_data)
        except Exception:
            self.term_rx.insertPlainText("\r[có lỗi xảy ra!]\r")
        self.term_rx.ensureCursorVisible()

    @Slot()
    def state_changed(self, state) -> None:
        """Xử lý khi trạng thái socket thay đổi.

        Slot này được kết nối với `stateChanged` của socket. Hàm cập nhật UI và phát
        tín hiệu `curr_connect_notify` tương ứng.

        Tham số:
            state: Trạng thái socket mới.
        """
        socket_state = state_changed(state)
        if socket_state == "Host Lookup...":
            self.curr_connect_notify.emit(1)
            self.labelStatus.setText(f'<font color="#29B6F6">{socket_state}</font>')
        if socket_state == "Connected":
            self.curr_connect_notify.emit(2)
            self.labelStatus.setText(f'<font color="#4CAF50">{socket_state}</font>')

        if socket_state == "Disconnected":
            self.started = False
            if self.restart():
                return
            self.labelStatus.setText(f'<font color="#C62828">{socket_state}</font>')
            self.curr_connect_notify.emit(0)

    @Slot()
    def sock_error(self, error) -> None:
        """Xử lý lỗi socket.

        Slot này được kết nối với `errorOccurred` của socket. Hàm cập nhật UI và phát
        tín hiệu `curr_connect_notify` nếu cần.

        Tham số:
            error: Mã lỗi socket.
        """
        error_message = sock_error(error)

        if (
            error_message in ["Remote Host Closed Error", "Unknown Socket Error"]
            and self.toggleAutoConnect.isChecked()
        ):
            if error_message == "Unknown Socket Error":
                self.toggleAutoConnect.setEnabled(True)
            if self.restart():
                return

        QMessageBox.warning(self, "Lỗi", f"Lỗi: {error.value} - {error_message}")

    def update_ui(self, connection_state: int) -> None:
        """Update the UI based on the connection state.

        Disable/enable the widgets based on the connection state.

        Args:
            connection_state (int): The current connection state.
                0 for disconnected, 1 for trying to connect, 2 for connected.
        """
        for widget in self.findChildren(QWidget):
            if isinstance(widget, QSpinBox):
                widget.setEnabled(connection_state == 0)

        self.toggleAutoConnect.setEnabled(connection_state != 1)
        self.toggleAutoConnect.setChecked(
            connection_state != 0
        ) if connection_state == 0 else None

    def restart(self) -> bool:
        """Restart the connection if auto connect is enabled."""
        auto_connect_enabled = self.toggleAutoConnect.isChecked()
        self.auto_connect_notify.emit(auto_connect_enabled)
        if auto_connect_enabled:
            self.start()
            return True
        return False


if __name__ == "__main__":
    client = None
    try:
        app = QApplication()
        client = TCPClient(parent=None, addr="127.0.0.1", port=80)
        client.show()
        app.exec()
    except KeyboardInterrupt:
        client.sock.close() if client is not None else None
        exit(0)
