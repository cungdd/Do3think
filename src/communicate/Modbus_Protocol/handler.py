"""Bộ chuyển đổi trạng thái và lỗi cho MODBUS."""

from typing import Literal
from PySide6.QtSerialBus import QModbusDevice



def state_changed(state: QModbusDevice.State) -> Literal[
    'Disconnected', 'Host Lookup...', 'Connected', 'Closing...','Unknown'
]:
    if state == QModbusDevice.State.UnconnectedState:
        curr_state = 'Disconnected'
    elif state == QModbusDevice.State.ConnectingState:
        curr_state = 'Host Lookup...'
    elif state == QModbusDevice.State.ConnectedState:
        curr_state = 'Connected'
    elif state == QModbusDevice.State.ClosingState:
        curr_state = 'Closing...'
    else:
        curr_state = 'Unknown'
    return curr_state

def sock_error(err: QModbusDevice.Error) -> Literal[
    'No Error', 'Read Error', 'Write Error', 'Connection Error', 'Configuration Error', 'Timeout Error', 'Protocol Error', 'Reply Aborted Error', 'Unknown Error', 'Invalid Response Error'
]:
    if err == QModbusDevice.Error.NoError:
        err_msg = 'No Error'
    elif err == QModbusDevice.Error.ReadError:
        err_msg = 'Read Error'
    elif err == QModbusDevice.Error.WriteError:
        err_msg = 'Write Error'
    elif err == QModbusDevice.Error.ConnectionError:
        err_msg = 'Connection Error'
    elif err == QModbusDevice.Error.ConfigurationError:
        err_msg = 'Configuration Error'
    elif err == QModbusDevice.Error.TimeoutError:
        err_msg = 'Timeout Error'
    elif err == QModbusDevice.Error.ProtocolError:
        err_msg = 'Protocol Error'
    elif err == QModbusDevice.Error.ReplyAbortedError:
        err_msg = 'Reply Aborted Error'
    elif err == QModbusDevice.Error.UnknownError:
        err_msg = 'Unknown Error'
    elif err == QModbusDevice.Error.InvalidResponseError:
        err_msg = 'Invalid Response Error'
    else:
        err_msg = 'Unknown Error'
    return err_msg
    