
"""Module chuyển đổi trạng thái và lỗi socket cho TCP."""

from typing import Literal
from PySide6.QtNetwork import QAbstractSocket

def state_changed(state: QAbstractSocket.SocketState) -> Literal[
    'Disconnected', 'Host Lookup...', 'Connecting...', 'Connected', 'Bound', 'Closing...', 'Unknown'
]:
    if state == QAbstractSocket.SocketState.UnconnectedState:
        curr_state = 'Disconnected'
    elif state == QAbstractSocket.SocketState.HostLookupState:
        curr_state = 'Host Lookup...'
    elif state == QAbstractSocket.SocketState.ConnectingState:
        curr_state = 'Connecting...'
    elif state == QAbstractSocket.SocketState.ConnectedState:
        curr_state = 'Connected'
    elif state == QAbstractSocket.SocketState.BoundState:
        curr_state = 'Bound'
    elif state == QAbstractSocket.SocketState.ClosingState:
        curr_state = 'Closing...'
    else:
        curr_state = 'Unknown'
    return curr_state
    

def sock_error(err: QAbstractSocket.SocketError) -> Literal[
    'Connection Refused Error', 'Remote Host Closed Error', 'Host Not Found Error',
    'Socket Access Error', 'Socket Resource Error', 'Socket Timeout Error',
    'Datagram Too Large Error', 'Network Error', 'Address In Use Error',
    'Socket Address Not Available Error', 'Unsupported Socket Operation Error',
    'Proxy Authentication Required Error', 'Ssl Handshake Failed Error',
    'Unfinished Socket Operation Error', 'Proxy Connection Refused Error',
    'Proxy Connection Closed Error', 'Proxy Connection Timeout Error',
    'Proxy Not Found Error', 'Proxy Protocol Error', 'Operation Error',
    'SslInternalError', 'Ssl Invalid User Data Error', 'Temporary Error',
    'Unknown Socket Error', 'Unknown Error'
]:
        if err == QAbstractSocket.SocketError.ConnectionRefusedError:
            err_msg = 'Connection Refused Error'
        elif err == QAbstractSocket.SocketError.RemoteHostClosedError:
            err_msg = 'Remote Host Closed Error'
        elif err == QAbstractSocket.SocketError.HostNotFoundError:
            err_msg = 'Host Not Found Error'
        elif err == QAbstractSocket.SocketError.SocketAccessError:
            err_msg = 'Socket Access Error'
        elif err == QAbstractSocket.SocketError.SocketResourceError:
            err_msg = 'Socket Resource Error'
        elif err == QAbstractSocket.SocketError.SocketTimeoutError:
            err_msg = 'Socket Timeout Error'
        elif err == QAbstractSocket.SocketError.DatagramTooLargeError:
            err_msg = 'Datagram Too Large Error'
        elif err == QAbstractSocket.SocketError.NetworkError:
            err_msg = 'Network Error'
        elif err == QAbstractSocket.SocketError.AddressInUseError:
            err_msg = 'Address In Use Error'
        elif err == QAbstractSocket.SocketError.SocketAddressNotAvailableError:
            err_msg = 'Socket Address Not Available Error'
        elif err == QAbstractSocket.SocketError.UnsupportedSocketOperationError:
            err_msg = 'Unsupported Socket Operation Error'
        elif err == QAbstractSocket.SocketError.ProxyAuthenticationRequiredError:
            err_msg = 'Proxy Authentication Required Error'
        elif err == QAbstractSocket.SocketError.SslHandshakeFailedError:
            err_msg = 'Ssl Handshake Failed Error'
        elif err == QAbstractSocket.SocketError.UnfinishedSocketOperationError:
            err_msg = 'Unfinished Socket Operation Error'
        elif err == QAbstractSocket.SocketError.ProxyConnectionRefusedError:
            err_msg = 'Proxy Connection Refused Error'
        elif err == QAbstractSocket.SocketError.ProxyConnectionClosedError:
            err_msg = 'Proxy Connection Closed Error'
        elif err == QAbstractSocket.SocketError.ProxyConnectionTimeoutError:
            err_msg = 'Proxy Connection Timeout Error'
        elif err == QAbstractSocket.SocketError.ProxyNotFoundError:
            err_msg = 'Proxy Not Found Error'
        elif err == QAbstractSocket.SocketError.ProxyProtocolError:
            err_msg = 'Proxy Protocol Error'
        elif err == QAbstractSocket.SocketError.OperationError:
            err_msg = 'Operation Error'
        elif err == QAbstractSocket.SocketError.SslInternalError:
            err_msg = 'SslInternalError'
        elif err == QAbstractSocket.SocketError.SslInvalidUserDataError:
            err_msg = 'Ssl Invalid User Data Error'
        elif err == QAbstractSocket.SocketError.TemporaryError:
            err_msg = 'Temporary Error'
        elif err == QAbstractSocket.SocketError.UnknownSocketError:
            err_msg = 'Unknown Socket Error'
        else:
            err_msg = 'Unknown Error'
        return err_msg