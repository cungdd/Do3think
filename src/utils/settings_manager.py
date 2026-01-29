# settings_manager.py
from __future__ import annotations
from pathlib import Path
from typing import Any, Optional
import json
from datetime import datetime

APP_DIR = Path("runtime")
APP_DIR.mkdir(parents=True, exist_ok=True)

# Base paths for global (no-product) configs
GLOBAL_PATHS = {
    "vision": APP_DIR / "vision.json",
    "service": APP_DIR / "service.json",
    "dataset": APP_DIR / "dataset.json",
}

META_PATH = APP_DIR / "products_meta.json"  # Lưu list products + current


def _parse_data_type(data_type: str) -> tuple[str, Optional[str]]:
    """Parse data_type như 'ProductA_vision' -> ('vision', 'ProductA')"""
    parts = data_type.rsplit("_", 1)
    if (
        len(parts) == 2 and parts[1] in GLOBAL_PATHS.keys()
    ):  # Use GLOBAL_PATHS.keys() for consistency
        return parts[1], parts[0]
    return data_type, None  # Fallback nếu không có prefix


def results_dir() -> Path:
    p = APP_DIR / "results"
    p.mkdir(exist_ok=True)
    return p


def load_config(data_type: str, default: Any = {}) -> dict:
    base_type, product = _parse_data_type(data_type)
    if product is None:
        p = GLOBAL_PATHS.get(base_type)
    else:
        p = APP_DIR / f"{product}_{base_type}.json"

    if p and p.exists():
        try:
            with p.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"[Warning] Failed to load {p}: {e}")
            return default
    return default


def save_config(cfg: dict, data_type: str) -> bool:
    """Save config, returns True if successful."""
    base_type, product = _parse_data_type(data_type)
    if product is None:
        p = GLOBAL_PATHS.get(base_type)
    else:
        p = APP_DIR / f"{product}_{base_type}.json"

    if p is None:
        print(f"[Error] Invalid data_type: {data_type}")
        return False

    try:
        p.parent.mkdir(
            parents=True, exist_ok=True
        )  # Ensure dir exists (redundant but safe)
        with p.open("w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=4)
        return True
    except (IOError, TypeError) as e:
        print(f"[Error] Failed to save {p}: {e}")
        return False


def delete_config(data_type: str) -> bool:
    """Delete config file for data_type, returns True if deleted."""
    base_type, product = _parse_data_type(data_type)
    if product is None:
        p = GLOBAL_PATHS.get(base_type)
    else:
        p = APP_DIR / f"{product}_{base_type}.json"

    if p and p.exists():
        try:
            p.unlink()
            print(f"[Info] Deleted {p}")
            return True
        except IOError as e:
            print(f"[Error] Failed to delete {p}: {e}")
            return False
    return False


def load_meta() -> dict:
    """Load products meta: {'available_products': [...], 'current_product': str | None}"""
    if META_PATH.exists():
        try:
            with META_PATH.open("r", encoding="utf-8") as f:
                meta = json.load(f)
                # Ensure required keys
                meta.setdefault("available_products", [])
                meta["current_product"] = meta.get("current_product")
                return meta
        except (json.JSONDecodeError, IOError) as e:
            print(f"[Warning] Failed to load meta {META_PATH}: {e}")
    return {"available_products": [], "current_product": None}


def save_meta(meta: dict) -> bool:
    """Save products meta, returns True if successful."""
    try:
        # Ensure structure
        meta.setdefault("available_products", [])
        with META_PATH.open("w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=4)
        return True
    except (IOError, TypeError) as e:
        print(f"[Error] Failed to save meta {META_PATH}: {e}")
        return False


def append_result(camera_id: int, payload: dict) -> None:
    """Lưu kết quả dạng JSONL theo ngày: 1 dòng/1 bản ghi."""
    fn = results_dir() / f"{datetime.now():%Y-%m-%d}.jsonl"
    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "camera_id": camera_id,
        **payload,
    }
    try:
        with fn.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except IOError as e:
        print(f"[Error] Failed to append result to {fn}: {e}")


class SettingsManager:
    """
    Class wrapper cho settings management API để dùng cho main application.
    
    Quản lý việc lưu/tải cấu hình của toàn bộ ứng dụng.
    """
    
    def __init__(self, config_file: str = "app_settings.json"):
        """
        Args:
            config_file: Tên file config chính (mặc định: app_settings.json)
        """
        self.config_path = APP_DIR / config_file
        
    def save_settings(self, settings: dict) -> bool:
        """
        Lưu cấu hình toàn bộ app.
        
        Args:
            settings: Dictionary chứa config của các module
            
        Returns:
            True nếu lưu thành công
        """
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with self.config_path.open("w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
            print(f"[Info] Saved settings to {self.config_path}")
            return True
        except (IOError, TypeError) as e:
            print(f"[Error] Failed to save settings: {e}")
            return False
            
    def load_settings(self) -> dict:
        """
        Tải cấu hình toàn bộ app.
        
        Returns:
            Dictionary chứa config, hoặc {} nếu chưa có
        """
        if self.config_path.exists():
            try:
                with self.config_path.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"[Warning] Failed to load settings: {e}")
                return {}
        return {}
        
    def reset_settings(self) -> bool:
        """
        Xóa file cấu hình (reset về mặc định).
        
        Returns:
            True nếu xóa thành công
        """
        if self.config_path.exists():
            try:
                self.config_path.unlink()
                print(f"[Info] Reset settings (deleted {self.config_path})")
                return True
            except IOError as e:
                print(f"[Error] Failed to delete settings: {e}")
                return False
        return False

