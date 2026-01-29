from typing import TypedDict
from PySide6.QtCore import Slot, QTimer, Qt
from PySide6.QtWidgets import QApplication, QWidget, QSpinBox, QMessageBox, QLineEdit
from PySide6.QtSerialBus import QModbusTcpClient, QModbusDataUnit, QModbusReply, QModbusDevice

from .Modbus_Protocol_ui import Ui_Form
from ..base_protocol import BaseProtocol

from .handler import state_changed, sock_error

class _Reg(TypedDict):
    reg_type: str
    reg_addr: int

class MODBUS(Ui_Form, BaseProtocol):
    def __init__(self, parent=None, addr=None, port=None, auto=False, polling_interval=50, 
                auto_clear=False,
                read_register = _Reg(reg_type="HoldingRegisters", reg_addr=0),
                write_reg_state= _Reg(reg_type="HoldingRegisters", reg_addr=0), 
            ):
        super().__init__(parent)

        self.setupUi(self)
        self.__init_reg()

        self.modbus_client = QModbusTcpClient()

        self.__retry = 5
        self.started = False
        self.addr = addr
        self.port = port
        self._last_reg_value = None  # Biến lưu giá trị trước đó
        self.device_id = 1
        self.polling_interval.setValue(int(polling_interval))


        self.__auto_clear = auto_clear
        self.reg_read = read_register
        self.reg_wr_state = write_reg_state

        self.gridLayout_2.replaceWidget(self.holderAutoConnect, self.toggleAutoConnect)
        self.holderAutoConnect.deleteLater()

        # Timer để đọc liên tục
        self.read_timer = QTimer(self)
        self.read_timer.setInterval(50)  # 50ms
        self.read_timer.timeout.connect(self.read_input)
        self.chkAutoClear.toggled.connect(self.__on_auto_clear)

        # Kết nối tín hiệu
        self.curr_connect_notify.connect(self.update_ui)
        self.polling_interval.editingFinished.connect(lambda: self.read_timer.setInterval(self.polling_interval.value()))

        # Kết nối trạng thái của modbus client
        self.modbus_client.stateChanged.connect(self.state_changed)
        self.modbus_client.errorOccurred.connect(self.sock_error)

        # Cờ trạng hàng kết nối: True – Đang kết nối, False – Đang ngắt kết nối
        self.toggleAutoConnect.setChecked(auto)


    def __init_reg(self):
        """Initialize the register addresses."""
        register_types = ["DiscreteInputs", "Coils", "InputRegisters", "HoldingRegisters"]
        self.reg_read_type.addItems(register_types)
        self.reg_wr_state_type.addItems(register_types)
    
    @property
    def reg_read(self) -> _Reg:
        return _Reg(
            reg_type=self.reg_read_type.currentText(),
            reg_addr=self.reg_read_addr.value(),
        )

    @reg_read.setter
    def reg_read(self, value: _Reg):
        self.reg_read_type.setCurrentText(value['reg_type'])
        self.reg_read_addr.setValue(value['reg_addr'])


    @property
    def reg_wr_state(self):
        return _Reg(
            reg_type=self.reg_wr_state_type.currentText(),
            reg_addr=self.reg_wr_state_addr.value(),
        )

    @reg_wr_state.setter
    def reg_wr_state(self, value: _Reg):
        self.reg_wr_state_type.setCurrentText(value['reg_type'])
        self.reg_wr_state_addr.setValue(value['reg_addr'])

    @property
    def addr(self):
        octets: list[QSpinBox] = [self.octet, self.octet_2, self.octet_3, self.octet_4]
        return ".".join(str(octet.value()) for octet in octets)
    
    @addr.setter
    def addr(self, value: str | None):
        """Set the value of the address fields."""
        if value is None:
            value = "192.168.1.1"
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
        """Set the value of the port field."""
        self.port_field.setValue(value if value is not None else 502)


    @property
    def __auto_clear(self) -> bool:
        return self.chkAutoClear.isChecked()
    
    @__auto_clear.setter
    def __auto_clear(self, value: bool) -> None:
        self.chkAutoClear.setChecked(value)

    @property
    def settings(self):
        return {
            "addr": self.addr,
            "port": self.port,
            "auto": self.toggleAutoConnect.isChecked(),
            "polling_interval": self.polling_interval.value(),
            "read_register": self.reg_read,
            "auto_clear": self.__auto_clear,
            "write_reg_state": self.reg_wr_state
        }

    def start(self):
        if not self.started:
            self.started = True
            self.modbus_client.setConnectionParameter(
                QModbusTcpClient.ConnectionParameter.NetworkAddressParameter, self.addr
            )
            self.modbus_client.setConnectionParameter(
                QModbusTcpClient.ConnectionParameter.NetworkPortParameter, self.port
            )
            self.modbus_client.disconnectDevice()
            self.modbus_client.connectDevice()

    def stop(self):
        if self.started:
            self.started = False
            self.modbus_client.disconnectDevice()

    @Slot()
    def state_changed(self, state) -> None:
        """Handle socket state changes."""
        socket_state = state_changed(state)
        if socket_state == 'Host Lookup...':
            self.curr_connect_notify.emit(1)
            self.labelStatus.setText(f'<font color="#29B6F6">{socket_state}</font>')
        if socket_state == 'Connected':
            self.curr_connect_notify.emit(2)
            self.labelStatus.setText(f'<font color="#4CAF50">{socket_state}</font>')
            self.read_timer.start()
        if socket_state == 'Disconnected':
            self.started = False
            self.read_timer.stop()
            if self.restart():
                return
            self.labelStatus.setText(f'<font color="#C62828">{socket_state}</font>')
            self.curr_connect_notify.emit(0)

    @Slot()
    def sock_error(self, error) -> None:
        """Handle socket errors."""
        error_message = sock_error(error)
        if error_message in ['Connection Error', 'Unknown Socket Error'] and self.toggleAutoConnect.isChecked():
            if error_message == 'Unknown Socket Error':
                self.toggleAutoConnect.setEnabled(True)
        
            if self.restart() and self.__retry <=5:
                self.__retry += 1
                return
            else:
                self.__retry = 0
                return
            
        QMessageBox.warning(self, "Lỗi", f"Lỗi: {error.value} - {error_message}")

    def update_ui(self, connection_state: int) -> None:
        """Update the UI based on the connection state."""
        for widget in self.findChildren(QWidget):
            if isinstance(widget, QSpinBox):
                widget.setEnabled(connection_state == 0)
        self.toggleAutoConnect.setChecked(connection_state != 0) if connection_state == 0 else None
            
    def restart(self) -> bool:
        """Restart the connection if auto connect is enabled."""
        auto_connect_enabled = self.toggleAutoConnect.isChecked()
        self.auto_connect_notify.emit(auto_connect_enabled)
        if auto_connect_enabled:
            self.start()
            return True
        return False

    def read_input(self):
        """Read input from the device."""
        if self.started:
            read_address = self.reg_read['reg_addr']
            read_type = QModbusDataUnit.RegisterType.__members__[self.reg_read['reg_type']]
            data_unit = QModbusDataUnit(read_type, read_address, 1)
            reply = self.modbus_client.sendReadRequest(data_unit, self.device_id)
            if reply:
                if not reply.isFinished():
                    reply.finished.connect(self.onReadReady)
                else:
                    del reply

    def __on_auto_clear(self, value: bool):
        self.__auto_clear = value

    def onReadReady(self) -> None:
        """Handle the result of a read request."""
        reply = self.sender()
        if not isinstance(reply, QModbusReply):
            return

        try:
            # Lỗi thiết bị -> thoát sớm (tuỳ chọn: log/hiển thị)
            if reply.error() != QModbusDevice.Error.NoError:
                # self._log(f"Modbus read error: {reply.errorString()}")
                return

            unit: QModbusDataUnit = reply.result()
            if unit is None or not unit.isValid() or unit.valueCount() < 1:
                # self._log("Modbus read: invalid data unit")
                return

            # Lấy giá trị & chuẩn hoá
            val = unit.value(0)
            new_value = str(val)

            # Cập nhật UI chỉ khi thay đổi
            if self.reg_read_value.text() != new_value:
                self.reg_read_value.setText(new_value)

            # Auto-clear: nếu khác "0" và bật auto_clear
            if new_value != "0" and self.__auto_clear:
                self.send_to(self.reg_read, "0")

            # Emit khi thay đổi và khác "0"
            if new_value != self._last_reg_value:
                self._last_reg_value = new_value
                if new_value != "0":
                    self.rx_data.emit(new_value)

        finally:
            # Bảo đảm giải phóng reply
            reply.deleteLater()

    def send_to(self, reg: _Reg, tx_data: int | str | bytes) -> None:
        if not tx_data:
            return
        if self.started:
            write_addr = reg['reg_addr']
            write_type = QModbusDataUnit.RegisterType.__members__[reg['reg_type']]
            write_unit = QModbusDataUnit(write_type, write_addr, 1)
            write_unit.setValue(0, int(tx_data))
            reply: QModbusReply = self.modbus_client.sendWriteRequest(write_unit, self.device_id)
            if reply:
                del reply

    def write_digit_sequence(self, seq: str) -> None:
        """Ghi chuỗi số (vd '12222') vào các Holding Registers liên tiếp."""
        if not seq or not seq.isdigit() or not self.started:
            return

        base_addr = self.reg_wr_state['reg_addr']
        reg_type = QModbusDataUnit.RegisterType.__members__[self.reg_wr_state['reg_type']]

        # Tạo data unit dài bằng số ký tự
        unit = QModbusDataUnit(reg_type, base_addr, len(seq))
        for i, ch in enumerate(seq):
            unit.setValue(i, int(ch))

        reply: QModbusReply = self.modbus_client.sendWriteRequest(unit, self.device_id)
        if reply:
            # Có thể nối finished/error nếu muốn kiểm tra kết quả rồi del
            # reply.finished.connect(lambda: reply.deleteLater())
            del reply

    def send_data(self, tx_data: int | str | bytes) -> None:
        self.handle_send_data(tx_data)

    def handle_send_data(self, tx_data: int | str | bytes) -> None:
        # Nếu là chuỗi số dài hơn 1 ký tự -> ghi chuỗi theo dải
        if isinstance(tx_data, str):
            s = tx_data.strip()
            if s.isdigit():
                if len(s) > 1:
                    self.write_digit_sequence(s)
                    return
                else:
                    # 1 chữ số -> ghi đơn lẻ vào base address
                    self.send_to(self.reg_wr_state, int(s))
                    return

            # (Phần xử lý list 'ok/ng/err' giữ nguyên)
            items = s.replace("[", "").replace("]", "").split(",")
            for i in range(len(items)):
                item = items[i].strip().lower()
                if item in ['ng', 'err']:
                    value = 1
                elif item == 'n/a':
                    value = 2
                elif item == 'ok':
                    value = 0
                else:
                    continue

                current_reg = _Reg(
                    reg_type=self.reg_wr_state['reg_type'],
                    reg_addr=self.reg_wr_state['reg_addr'] + i
                )
                self.send_to(current_reg, value)

if __name__ == "__main__":
    app = QApplication()
    window = MODBUS(None, addr='192.168.1.10', port=502)
    window.show()
    app.exec()