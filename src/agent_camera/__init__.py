# src/agent_camera/__init__.py
# Sử dụng cơ chế lazy import hoặc định nghĩa rõ __all__ 
# để tránh RuntimeWarning khi chạy python -m

__all__ = ["BaseCameraWidget"]

def __getattr__(name):
    if name == "BaseCameraWidget":
        from .base_widget import BaseCameraWidget
        return BaseCameraWidget
    raise AttributeError(f"module {__name__} has no attribute {name}")
